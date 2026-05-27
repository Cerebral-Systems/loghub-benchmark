"""Regenerate instruction.md + tests/test_state.py for existing v2 tasks.

After hardening the exporter templates (blind-triage fp, table-free sev,
edge-correctness corr, ordering-strict seq) we re-render those two files
in place for every existing task. expected.json, oracle hints, logs, and
Dockerfile stay untouched — the verifier behaves the same on prior agent
runs because the schema is unchanged; only the agent-visible prompt and
the verifier's assertions got harder.

Usage:
    python -m tools.case_builder.repatch_v2_tasks --tasks-dir tasks
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from . import export_to_harbor as ex


def _slug_to_case_meta(task_dir: Path) -> dict:
    """Reconstruct just enough of a 'case' dict to feed the exporter's
    template-render functions for instruction/test renderers."""
    expected = json.loads((task_dir / "tests" / "expected.json").read_text())
    slug = task_dir.name
    parts = slug.split("-")
    by_prefix = {
        "hdfs": "HDFS_v1",
        "hadoop": "Hadoop",
        "bgl": "BGL",
        "thunderbird": "Thunderbird",
        "openstack": "OpenStack",
    }
    dataset_token = parts[1] if parts[0] in {"fp", "sev", "seq", "corr", "tmpl", "rem"} else parts[0]
    dataset_name = by_prefix[dataset_token]
    file_basenames = sorted(expected.get("files", []))
    anomaly_keys = _corr_anomaly_keys_from_existing(task_dir, expected, dataset_name)
    return {
        "dataset_name": dataset_name,
        "file_basenames": file_basenames,
        "slug": slug,
        "case_id": expected.get("case_id", "0" * 64),
        "root_cause": expected.get("root_cause_type", "other"),
        "anomaly_keys": anomaly_keys,
    }


def _corr_anomaly_keys_from_existing(task_dir: Path, expected: dict, dataset_name: str) -> tuple[str, ...]:
    if dataset_name != "HDFS_v1":
        return ()
    for entry in expected.get("causal_chain", []):
        path = task_dir / "environment" / "data" / entry.get("component", "")
        line_no = entry.get("evidence_line")
        if not path.is_file() or not isinstance(line_no, int):
            continue
        lines = path.read_text(errors="replace").splitlines()
        if not (1 <= line_no <= len(lines)):
            continue
        match = re.search(r"blk_-?\d+", lines[line_no - 1])
        if match:
            return (match.group(0),)
    return ()


def _author_from_existing(task_dir: Path) -> tuple[str, str]:
    """Read author info out of the existing task.toml; falls back to defaults
    so repatch keeps the same byline."""
    text = (task_dir / "task.toml").read_text()
    name = "Madhav Goyal"
    email = "madhav@campnetwork.xyz"
    for line in text.splitlines():
        ls = line.strip()
        if ls.startswith("author_name") and "=" in ls:
            name = ls.split("=", 1)[1].strip().strip('"')
        elif ls.startswith("author_email") and "=" in ls:
            email = ls.split("=", 1)[1].strip().strip('"')
    return name, email


def _difficulty_from_existing(task_dir: Path) -> str:
    text = (task_dir / "task.toml").read_text()
    for line in text.splitlines():
        ls = line.strip()
        if ls.startswith("difficulty") and "=" in ls:
            return ls.split("=", 1)[1].strip().strip('"')
    return "medium"


def patch_fp(task_dir: Path) -> None:
    meta = _slug_to_case_meta(task_dir)
    case = {"dataset_name": meta["dataset_name"], "root_cause": meta["root_cause"], "case_id": meta["case_id"]}
    name, email = _author_from_existing(task_dir)
    (task_dir / "instruction.md").write_text(
        ex._render_instruction_fp(case, file_basenames=meta["file_basenames"], slug=meta["slug"])
    )
    (task_dir / "tests" / "test_state.py").write_text(ex._render_test_state_py_fp())
    (task_dir / "task.toml").write_text(
        ex._render_task_toml_fp(
            slug=meta["slug"], case=case,
            difficulty=_difficulty_from_existing(task_dir),
            author_name=name, author_email=email,
        )
    )


def patch_sev(task_dir: Path) -> None:
    meta = _slug_to_case_meta(task_dir)
    case = {"dataset_name": meta["dataset_name"], "root_cause": meta["root_cause"], "case_id": meta["case_id"]}
    name, email = _author_from_existing(task_dir)
    (task_dir / "instruction.md").write_text(
        ex._render_instruction_sev(case, file_basenames=meta["file_basenames"], slug=meta["slug"])
    )
    (task_dir / "tests" / "test_state.py").write_text(ex._render_test_state_py_sev())
    (task_dir / "task.toml").write_text(
        ex._render_task_toml_sev(
            slug=meta["slug"], case=case,
            difficulty=_difficulty_from_existing(task_dir),
            author_name=name, author_email=email,
        )
    )


def patch_seq(task_dir: Path) -> None:
    meta = _slug_to_case_meta(task_dir)
    case = {"dataset_name": meta["dataset_name"], "root_cause": meta["root_cause"], "case_id": meta["case_id"]}
    name, email = _author_from_existing(task_dir)
    (task_dir / "instruction.md").write_text(
        ex._render_instruction_seq(case, file_basenames=meta["file_basenames"], slug=meta["slug"])
    )
    (task_dir / "tests" / "test_state.py").write_text(ex._render_test_state_py_seq())
    (task_dir / "task.toml").write_text(
        ex._render_task_toml_seq(
            slug=meta["slug"], case=case,
            difficulty=_difficulty_from_existing(task_dir),
            author_name=name, author_email=email,
        )
    )


def patch_corr(task_dir: Path) -> None:
    meta = _slug_to_case_meta(task_dir)
    case = {
        "dataset_name": meta["dataset_name"],
        "root_cause": meta["root_cause"],
        "case_id": meta["case_id"],
        "anomaly_keys": meta["anomaly_keys"],
    }
    name, email = _author_from_existing(task_dir)
    (task_dir / "instruction.md").write_text(
        ex._render_instruction_corr(case, file_basenames=meta["file_basenames"], slug=meta["slug"])
    )
    (task_dir / "tests" / "test_state.py").write_text(ex._render_test_state_py_corr())
    (task_dir / "task.toml").write_text(
        ex._render_task_toml_corr(
            slug=meta["slug"], case=case,
            difficulty=_difficulty_from_existing(task_dir),
            author_name=name, author_email=email,
        )
    )


def patch_tmpl(task_dir: Path) -> None:
    """tmpl tasks only need the system-wide pytest comment added to task.toml.
    Their instruction.md isn't part of the v2 hardening pass; leave it alone."""
    text = (task_dir / "task.toml").read_text()
    if "system-wide" in text:
        return
    text = text.replace(
        '# variable parts.\nversion = "1.0"',
        (
            "# variable parts.\n"
            "#\n"
            "# Pytest is installed system-wide in the Dockerfile (apt python3-pytest +\n"
            "# pip pytest-json-ctrf) so the verifier runs deterministically regardless\n"
            "# of which CLI agent / runtime the candidate uses.\n"
            'version = "1.0"'
        ),
    )
    (task_dir / "task.toml").write_text(text)


PATCHERS = {
    "fp-": patch_fp,
    "sev-": patch_sev,
    "seq-": patch_seq,
    "corr-": patch_corr,
    "tmpl-": patch_tmpl,
}


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--tasks-dir", type=Path, default=Path("tasks"))
    p.add_argument(
        "--prefixes",
        nargs="*",
        default=list(PATCHERS),
        help="task-slug prefixes to repatch (default: all of fp-, sev-, seq-, corr-)",
    )
    args = p.parse_args(argv)

    patched = 0
    for task_dir in sorted(args.tasks_dir.iterdir()):
        if not task_dir.is_dir():
            continue
        for prefix in args.prefixes:
            if task_dir.name.startswith(prefix):
                PATCHERS[prefix](task_dir)
                patched += 1
                break
    print(f"patched {patched} task(s)")


if __name__ == "__main__":
    main()
