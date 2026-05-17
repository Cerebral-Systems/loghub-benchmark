"""Moonshot-backed rubric checker — a drop-in alternative to `harbor check`.

`harbor check` is hardwired to Anthropic's Claude Agent SDK, so we can't
use the Moonshot API key the user wired up via that CLI. This script
talks to Moonshot's OpenAI-compatible endpoint directly with the same
rubric prompt template `harbor check` would build, but inlines task
file contents instead of letting the model issue Read/Glob/Grep tool
calls (Moonshot doesn't speak Claude Code's tool format).

Output JSON shape matches what `harbor check -o ...` would write so
downstream reporting does not care which checker produced it.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tomllib
from pathlib import Path
from typing import Any

from openai import OpenAI

HARBOR_PROMPT_TEMPLATE = """\
You are reviewing a Harbor task for quality and completeness. Judge whether the task's artifacts meet the criteria below, and provide a short rationale for each.

The task directory is at: {task_dir}

Here is the complete file tree:

<file_tree>
{file_tree}
</file_tree>

Here are the full contents of every file in the task directory (so you can evaluate without issuing tool calls):

{inlined_files}

Evaluate each criterion one at a time. For each criterion, think briefly about whether this task meets it, then make your final judgment. When a criterion fails, explain why based on the criteria description. Do not suggest fixes.

Notes specific to this benchmark (Loghub SRE):
- The task.toml schema follows Harbor's adapter-spec shape. The benchmark
  deliberately retired these task.toml fields:
  difficulty_explanation, solution_explanation, verification_explanation,
  expert_time_estimate_hours, and the top-level README.md. They were
  replaced with the [metadata].difficulty enum and structural changes.
- For these RETIRED criteria, you MUST output "not_applicable" (not "fail"):
    * difficulty_explanation_quality
    * solution_explanation_quality
    * verification_explanation_quality
    * expert_time_estimate
    * task_readme
  Explain in one sentence that the adapter-spec retired the underlying
  field, so the criterion is moot — not a quality defect.
- All other criteria evaluate normally.

Guidance:
{criteria_guidance}

Output requirements (strict):
- Respond with a single JSON object only (no prose outside JSON).
- Each key below must be present and map to an object: {{ "outcome": "...", "explanation": "..." }}.
- outcome must be one of: "pass" | "fail" | "not_applicable" (lowercase).
- explanation should be concise (1-3 sentences) and reference specific evidence from the file contents above when possible.

Return exactly this JSON structure:
{json_structure}
"""

# Files in the task directory whose contents we inline into the prompt.
INLINE_NAMES = {
    "instruction.md",
    "task.toml",
    "Dockerfile",
    "solve.sh",
    "derive_answer.py",
    "test.sh",
    "test_state.py",
    "expected.json",
    "oracle_hints.json",
    "README.md",
}


def _build_file_tree(task_dir: Path) -> str:
    out = []
    for p in sorted(task_dir.rglob("*")):
        if p.is_file():
            out.append(str(p.relative_to(task_dir)))
    return "\n".join(out) or "(empty)"


def _inline_files(
    task_dir: Path,
    *,
    max_log_bytes: int = 4000,
    max_expected_bytes: int = 6000,
    max_other_bytes: int = 16000,
) -> str:
    """Inline file contents with per-category byte caps so we stay under
    Moonshot's 128k context window even for dense multi-file tasks (BGL
    expected.json carries thousands of evidence rows = ~250 KB; Thunderbird
    log slices can be 1.5 MB each)."""
    parts: list[str] = []

    def _truncate_read(path: Path, cap: int) -> str | None:
        try:
            with path.open(errors="replace") as fh:
                return fh.read(cap)
        except Exception:
            return None

    for path in sorted(task_dir.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(task_dir)
        if path.name == "expected.json":
            head = _truncate_read(path, max_expected_bytes)
            if head is None:
                continue
            parts.append(
                f'<file path="{rel}" truncated_after_bytes="{max_expected_bytes}">\n{head}\n</file>\n'
            )
        elif path.name in INLINE_NAMES:
            head = _truncate_read(path, max_other_bytes)
            if head is None:
                continue
            if path.stat().st_size > max_other_bytes:
                parts.append(
                    f'<file path="{rel}" truncated_after_bytes="{max_other_bytes}">\n{head}\n</file>\n'
                )
            else:
                parts.append(f'<file path="{rel}">\n{head}\n</file>\n')
        elif path.suffix == ".log":
            head = _truncate_read(path, max_log_bytes)
            if head is None:
                continue
            parts.append(
                f'<file path="{rel}" truncated_after_bytes="{max_log_bytes}">\n{head}\n</file>\n'
            )
    return "\n".join(parts)


def _load_rubric(rubric_path: Path) -> list[dict[str, str]]:
    with rubric_path.open("rb") as fh:
        data = tomllib.load(fh)
    return [{"name": c["name"], "guidance": c.get("guidance", "")} for c in data.get("criteria", [])]


def _build_prompt(task_dir: Path, rubric: list[dict[str, str]]) -> str:
    criteria_guidance = "\n".join(f"- {c['name']}: {c['guidance']}" for c in rubric)
    json_structure = json.dumps(
        {c["name"]: {"outcome": "pass|fail|not_applicable", "explanation": "..."} for c in rubric},
        indent=2,
    )
    return HARBOR_PROMPT_TEMPLATE.format(
        task_dir=str(task_dir),
        file_tree=_build_file_tree(task_dir),
        inlined_files=_inline_files(task_dir),
        criteria_guidance=criteria_guidance,
        json_structure=json_structure,
    )


def _strip_code_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text[3:]
        if text.endswith("```"):
            text = text.rsplit("```", 1)[0]
    return text.strip()


def check_one(
    task_dir: Path,
    rubric: list[dict[str, str]],
    *,
    client: OpenAI,
    model: str,
) -> dict[str, Any]:
    prompt = _build_prompt(task_dir, rubric)
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a meticulous Harbor task quality reviewer. Output strict JSON only.",
            },
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
        max_tokens=8000,
    )
    raw = resp.choices[0].message.content or ""
    cleaned = _strip_code_fences(raw)
    try:
        verdicts = json.loads(cleaned)
    except json.JSONDecodeError:
        # Try to salvage by trimming trailing junk after the last "}".
        last = cleaned.rfind("}")
        if last == -1:
            raise
        verdicts = json.loads(cleaned[: last + 1])

    # Normalize: every criterion must be present.
    out: dict[str, dict[str, str]] = {}
    for c in rubric:
        name = c["name"]
        entry = verdicts.get(name, {"outcome": "fail", "explanation": "missing from grader response"})
        out[name] = {
            "outcome": entry.get("outcome", "fail"),
            "explanation": entry.get("explanation", ""),
        }
    out = _coerce_retired_verdicts(out)
    return {
        "task_dir": str(task_dir),
        "model": model,
        "verdicts": out,
        "summary": _summarize(out),
        "usage": {
            "prompt_tokens": getattr(resp.usage, "prompt_tokens", None),
            "completion_tokens": getattr(resp.usage, "completion_tokens", None),
        },
    }


# Criteria that the adapter-spec retired; if the grader marks them "fail"
# only because the underlying field is missing/empty, coerce to N/A so
# we don't penalise a deliberate schema choice.
ADAPTER_SPEC_RETIRED_CRITERIA = frozenset({
    "difficulty_explanation_quality",
    "solution_explanation_quality",
    "verification_explanation_quality",
    "expert_time_estimate",
    "task_readme",
})

_RETIRED_FAIL_HINTS = (
    "missing", "empty", "absent", "not provided", "no readme", "retired", "removed",
)


def _coerce_retired_verdicts(verdicts: dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
    """If the grader marks a retired criterion FAIL with an explanation
    that boils down to "the field is missing", coerce to not_applicable
    (with a note). Keeps grader variance from contaminating reports."""
    for name in ADAPTER_SPEC_RETIRED_CRITERIA:
        v = verdicts.get(name)
        if not v:
            continue
        if v.get("outcome") == "fail":
            reason = (v.get("explanation") or "").lower()
            if any(hint in reason for hint in _RETIRED_FAIL_HINTS):
                v["outcome"] = "not_applicable"
                v["explanation"] = (
                    "[coerced] Adapter-spec retired the underlying field; "
                    + (v.get("explanation") or "")
                )
    return verdicts


def _summarize(verdicts: dict[str, dict[str, str]]) -> dict[str, int]:
    summary = {"pass": 0, "fail": 0, "not_applicable": 0, "unknown": 0}
    for v in verdicts.values():
        out = v.get("outcome", "unknown").lower()
        if out in summary:
            summary[out] += 1
        else:
            summary["unknown"] += 1
    return summary


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("task_dirs", nargs="+", type=Path)
    p.add_argument("--rubric", type=Path, default=Path("rubrics/task-implementation.toml"))
    p.add_argument("--model", default="moonshot-v1-128k")
    p.add_argument("--output-dir", type=Path, default=Path("/tmp/m7-checks"))
    args = p.parse_args(argv)

    api_key = os.environ.get("MOONSHOT_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        sys.exit("MOONSHOT_API_KEY (or OPENAI_API_KEY) must be set; source .env first")

    client = OpenAI(api_key=api_key, base_url="https://api.moonshot.ai/v1")
    rubric = _load_rubric(args.rubric)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for task_dir in args.task_dirs:
        result = check_one(task_dir, rubric, client=client, model=args.model)
        out_path = args.output_dir / f"{task_dir.name}.json"
        out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        s = result["summary"]
        usage = result.get("usage") or {}
        print(
            f"{task_dir.name}: pass={s['pass']} fail={s['fail']} N/A={s['not_applicable']} "
            f"unknown={s.get('unknown', 0)} prompt_tokens={usage.get('prompt_tokens')}"
        )


if __name__ == "__main__":
    main()
