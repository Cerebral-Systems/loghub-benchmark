"""Compare an agent's answer to the task's expected.json (or oracle hints).

This module exposes one entry point — `diff_answer_to_expected` — that takes
a per-trial directory (one with `verifier/test-stdout.txt` and the agent's
`answer.json`) plus the task directory (containing `tests/expected.json`)
and returns a structured diff:

  {
    "task_slug": ...,
    "trial_id": ...,
    "fields": {
      "root_cause_type": {"agent": "...", "expected": "...", "match": bool},
      "mitigation.action": ...,
      "mitigation.target": ...,
      "evidence_recall": {"recall": 0.42, "ground_truth_count": N, ...},
      ...
    },
    "summary": {"matches": K, "mismatches": M, "missing_fields": L},
  }

Designed to compose with summarize_runs and failure_modes for the final
quality report.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def _evidence_set(answer: dict, key: str = "evidence") -> set[tuple[str, int]]:
    out: set[tuple[str, int]] = set()
    for entry in answer.get(key, []) or []:
        f = entry.get("file")
        ln = entry.get("line")
        if isinstance(f, str) and isinstance(ln, int):
            out.add((f, ln))
    return out


def _causal_chain_components(answer: dict) -> set[str]:
    return {e.get("component") for e in answer.get("causal_chain", []) or [] if e.get("component")}


def diff_answer_to_expected(answer: dict, expected: dict) -> dict:
    """Return a structured field-by-field diff dictionary."""
    diff: dict = {"fields": {}}

    def cmp(key: str) -> None:
        a = answer.get(key)
        e = expected.get(key)
        diff["fields"][key] = {"agent": a, "expected": e, "match": a == e}

    # Common scalar fields
    for k in ("schema_version", "is_incident", "root_cause_type"):
        if k in expected:
            cmp(k)

    if "root_component" in expected:
        cmp("root_component")
    if "severity" in expected:
        cmp("severity")
    if "severity_justification" in expected:
        cmp("severity_justification")

    # Mitigation block (v3 remediation)
    if "mitigation" in expected and isinstance(expected["mitigation"], dict):
        agent_mit = answer.get("mitigation") if isinstance(answer.get("mitigation"), dict) else {}
        for sub in ("action", "target"):
            ek = f"mitigation.{sub}"
            diff["fields"][ek] = {
                "agent": agent_mit.get(sub),
                "expected": expected["mitigation"].get(sub),
                "match": agent_mit.get(sub) == expected["mitigation"].get(sub),
            }
    if "expected_health" in expected:
        agent_health = (answer.get("postcheck") or {}).get("health_status")
        diff["fields"]["postcheck.health_status"] = {
            "agent": agent_health,
            "expected": expected["expected_health"],
            "match": agent_health == expected["expected_health"],
        }

    # Evidence-style recall metrics
    if "evidence" in expected:
        gt = _evidence_set(expected, "evidence")
        pr = _evidence_set(answer, "evidence")
        recall = len(gt & pr) / len(gt) if gt else 1.0
        precision = len(gt & pr) / len(pr) if pr else 1.0
        diff["fields"]["evidence"] = {
            "agent_count": len(pr),
            "ground_truth_count": len(gt),
            "recall": round(recall, 4),
            "precision": round(precision, 4),
            "match": gt.issubset(pr) and bool(gt),
        }
    if "false_positive_indicators" in expected:
        gt = _evidence_set(expected, "false_positive_indicators")
        pr = _evidence_set(answer, "false_positive_indicators")
        diff["fields"]["false_positive_indicators"] = {
            "agent_count": len(pr),
            "ground_truth_count": len(gt),
            "overlap": len(gt & pr),
            "match": bool(gt) and gt.issubset(pr),
        }
    if "timeline" in expected:
        gt_seq = [(e.get("file"), e.get("line")) for e in expected["timeline"]]
        pr_seq = sorted(
            answer.get("timeline", []) or [],
            key=lambda e: e.get("sequence", 0),
        )
        pr_seq = [(e.get("file"), e.get("line")) for e in pr_seq]
        diff["fields"]["timeline_order"] = {
            "agent": pr_seq,
            "expected": gt_seq,
            "match": pr_seq == gt_seq,
        }
    if "causal_chain" in expected:
        gt_components = {e["component"] for e in expected["causal_chain"]}
        pr_components = _causal_chain_components(answer)
        diff["fields"]["causal_chain_components"] = {
            "agent": sorted(pr_components),
            "expected": sorted(gt_components),
            "recall": round(
                (len(gt_components & pr_components) / len(gt_components))
                if gt_components else 1.0,
                4,
            ),
            "match": gt_components == pr_components,
        }

    matches = sum(1 for v in diff["fields"].values() if isinstance(v, dict) and v.get("match"))
    mismatches = sum(
        1 for v in diff["fields"].values() if isinstance(v, dict) and v.get("match") is False
    )
    diff["summary"] = {
        "matches": matches,
        "mismatches": mismatches,
        "n_fields": len(diff["fields"]),
        "field_accuracy": round(matches / len(diff["fields"]), 4) if diff["fields"] else 0.0,
    }
    return diff


def _find_answer_json(trial_dir: Path) -> Path | None:
    """Look in a few standard locations for a per-trial copy of /app/answer.json."""
    candidates = [
        trial_dir / "app" / "answer.json",
        trial_dir / "agent" / "answer.json",
        trial_dir / "answer.json",
    ]
    for p in candidates:
        if p.is_file():
            return p
    return None


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--task-dir", type=Path, required=True,
                   help="Path to tasks/<slug>/ (must contain tests/expected.json).")
    p.add_argument("--answer", type=Path,
                   help="Path to the agent's answer.json. Required if --trial-dir omitted.")
    p.add_argument("--trial-dir", type=Path,
                   help="Path to a Harbor trial directory; the tool will hunt for answer.json.")
    p.add_argument("--out", type=Path, default=None, help="Write JSON diff to this path.")
    args = p.parse_args(argv)

    expected = _load_json(args.task_dir / "tests" / "expected.json")
    if args.answer:
        answer = _load_json(args.answer)
    elif args.trial_dir:
        ap = _find_answer_json(args.trial_dir)
        if ap is None:
            raise SystemExit(f"no answer.json found under {args.trial_dir}")
        answer = _load_json(ap)
    else:
        raise SystemExit("provide --answer or --trial-dir")

    diff = diff_answer_to_expected(answer, expected)
    diff["task_slug"] = args.task_dir.name
    if args.out:
        args.out.write_text(json.dumps(diff, indent=2, sort_keys=True) + "\n")
    print(json.dumps(diff, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
