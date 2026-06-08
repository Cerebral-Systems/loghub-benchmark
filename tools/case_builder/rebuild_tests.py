"""Re-render tests/test.sh + tests/test_state.py for every committed task
in place, from each task's tests/expected.json schema_version, using the
export_to_harbor render functions as the single source of truth.

This is the maintained, corpus-free replacement for the old one-off
repatch script. Because every task's verifier is a static per-family
template (parameterized only by the verifier-only expected.json at run
time), this never needs to re-walk the Loghub corpus.

Usage:
    python -m tools.case_builder.rebuild_tests            # write in place
    python -m tools.case_builder.rebuild_tests --check    # diff only; exit 1 on drift

`--check` is wired into the repo-invariant test suite so committed test
files can never silently drift from the templates again.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import export_to_harbor as E

# schema_version -> the render function that produces tests/test_state.py.
# test.sh is identical across all families (_render_test_sh).
STATE_RENDERERS = {
    "loghub-sre-answer-v2": E._render_test_state_py,
    "loghub-sre-answer-v2-fp": E._render_test_state_py_fp,
    "loghub-sre-answer-v2-seq": E._render_test_state_py_seq,
    "loghub-sre-answer-v2-corr": E._render_test_state_py_corr,
    "loghub-sre-answer-v2-sev": E._render_test_state_py_sev,
    "loghub-sre-answer-v2-tmpl": E._render_test_state_py_tmpl,
    "loghub-sre-answer-v3-remediation": E._render_test_state_py_rem,
}


def iter_task_dirs(tasks_dir: Path):
    for exp in sorted(tasks_dir.glob("*/tests/expected.json")):
        yield exp.parent.parent


def rendered_files(task_dir: Path) -> dict[str, str]:
    expected = json.loads((task_dir / "tests" / "expected.json").read_text())
    sv = expected["schema_version"]
    if sv not in STATE_RENDERERS:
        raise SystemExit(f"{task_dir}: unknown schema_version {sv!r}")
    out = {
        "tests/test_state.py": STATE_RENDERERS[sv](),
        "tests/test.sh": E._render_test_sh(),
    }
    if sv == "loghub-sre-answer-v3-remediation":
        # Verifier-only clean copy of the shipped (initial, pre-mitigation)
        # state, mirrored from the agent-visible service_state.json. The
        # post-mitigation verifier replays the declared mitigation against this.
        out["tests/initial_state.json"] = (
            task_dir / "environment" / "data" / "service_state.json"
        ).read_text()
    return out


def run(tasks_dir: Path, check: bool) -> int:
    drift: list[str] = []
    written = 0
    for task_dir in iter_task_dirs(tasks_dir):
        for rel, content in rendered_files(task_dir).items():
            target = task_dir / rel
            current = target.read_text() if target.exists() else None
            if current == content:
                continue
            if check:
                drift.append(str(target))
            else:
                target.write_text(content)
                written += 1
    if check:
        if drift:
            print(f"DRIFT: {len(drift)} rendered test file(s) differ from committed:")
            for d in drift[:60]:
                print("  ", d)
            return 1
        print("OK: all committed test files match the export_to_harbor templates")
        return 0
    print(f"re-rendered {written} file(s) across {sum(1 for _ in iter_task_dirs(tasks_dir))} tasks")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--tasks-dir", type=Path, default=Path("tasks"))
    p.add_argument("--check", action="store_true", help="diff only; exit 1 on drift")
    args = p.parse_args(argv)
    return run(args.tasks_dir, args.check)


if __name__ == "__main__":
    raise SystemExit(main())
