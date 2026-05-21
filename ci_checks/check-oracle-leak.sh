#!/bin/bash
#
# Anti-leak gate. Refuses to merge a task whose environment/ contains a
# leaf string from tests/expected.json or any constant the oracle
# solver uses (solution/derive_answer.py, solution/oracle_hints.json).
#
# The exporter already runs an equivalent check at task-write time
# (tools/case_builder/export_to_harbor.py:_enforce_no_oracle_leak),
# but this script gives reviewers a second, independent line of
# defence on PRs — and catches manual edits that bypass the exporter.
#
# Single-token English words ("timeout", "other", "cpu") naturally
# occur in real vendor logs, so log files are checked only against
# answer-shaped tokens (the schema_version string, the JSON field
# names, and any multi-word taxonomy slug). Non-log files in
# environment/ (Dockerfile, etc.) are checked against ALL leaf
# strings — they should never carry any of them.

# Note: no `set -e` — the Python helper deliberately exits non-zero on
# leak detection, and we want to capture that as $rc and keep iterating
# over the remaining task dirs.

if [ $# -lt 1 ]; then
    FILES_TO_CHECK=$(find tasks -mindepth 1 -maxdepth 1 -type d 2>/dev/null)
else
    FILES_TO_CHECK="$@"
fi

if [ -z "$FILES_TO_CHECK" ]; then
    echo "No task directories to check"
    exit 0
fi

FAILED=0
for task_dir in $FILES_TO_CHECK; do
    expected="$task_dir/tests/expected.json"
    if [ ! -f "$expected" ]; then
        echo "SKIP $task_dir: no tests/expected.json"
        continue
    fi
    env_dir="$task_dir/environment"
    if [ ! -d "$env_dir" ]; then
        echo "SKIP $task_dir: no environment/ directory"
        continue
    fi

    # Delegate the matching logic to Python so we can decode the JSON
    # leaves correctly and apply the log-vs-non-log policy from
    # _enforce_no_oracle_leak in the exporter.
    OUT=$(python3 - "$task_dir" <<'PYEOF'
import json
import sys
from pathlib import Path

task_dir = Path(sys.argv[1])
expected = json.loads((task_dir / "tests" / "expected.json").read_text())


def leaves(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, (int, float, bool)) or obj is None:
        return
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from leaves(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from leaves(v)


file_basenames = set(expected.get("files", []))
all_leaves = [
    s for s in leaves(expected)
    if s and s not in file_basenames and len(s) >= 4
]

# Answer-shaped tokens (always forbidden in any environment/ file).
schema_version = expected.get("schema_version", "")
answer_shaped = {
    schema_version,
    '"root_cause_type"',
    '"anomaly_line_ids"',
    '"recommended_action"',
}
# v2-fp (false-positive triage) tasks have a different answer schema.
if schema_version.endswith("-v2-fp"):
    answer_shaped.update({
        '"false_positive_indicators"',
        '"why_not_anomalous"',
        '"is_incident"',
        '"confidence"',
    })
    for label in expected.get("allowed_why_not_anomalous", []):
        if isinstance(label, str) and "_" in label:
            answer_shaped.add(label)
# v2-seq (temporal sequence) answers add timeline-shape tokens.
if schema_version.endswith("-v2-seq"):
    answer_shaped.update({
        '"timeline"',
        '"sequence"',
        '"trigger"',
        '"propagation"',
        '"consequence"',
    })
# v2-corr (cross-component correlation) answers add causal-chain tokens.
if schema_version.endswith("-v2-corr"):
    answer_shaped.update({
        '"causal_chain"',
        '"caused_by_step"',
        '"root_component"',
    })
# v2-sev (severity classification) answers add severity-shape tokens.
if schema_version.endswith("-v2-sev"):
    answer_shaped.update({
        '"severity"',
        '"severity_justification"',
        '"P0"', '"P1"', '"P2"', '"P3"',
    })
    for label in expected.get("allowed_justifications", []):
        if isinstance(label, str) and "_" in label:
            answer_shaped.add(label)
# v2-tmpl (template extraction) — only check non-log files for the schema
# header. The log content IS the input; templates are by-design generalizations
# of those lines, so per-template-text leak checks make no sense.
for label in [expected.get("root_cause_type"), *expected.get("allowed_root_causes", []),
              *expected.get("safe_recommendations", [])]:
    if isinstance(label, str) and ("_" in label):
        answer_shaped.add(label)
answer_shaped.discard("")

env_dir = task_dir / "environment"
failures = []

is_tmpl = schema_version.endswith("-v2-tmpl")

for path in env_dir.rglob("*"):
    if not path.is_file():
        continue
    try:
        text = path.read_text(errors="replace")
    except Exception:
        continue
    relative = path.relative_to(task_dir)
    is_log = path.suffix == ".log"
    if is_log:
        for needle in answer_shaped:
            if needle and needle in text:
                failures.append(f"{relative}: answer-shaped string {needle!r} in agent-visible log")
                break
    elif is_tmpl:
        # For v2-tmpl, template strings (the leaves) ARE legitimate
        # generalizations of input log content — checking them against
        # non-log env files is too noisy. Restrict to answer-shaped tokens.
        for needle in answer_shaped:
            if needle and needle in text:
                failures.append(f"{relative}: answer-shaped string {needle!r}")
                break
    else:
        for needle in all_leaves:
            if needle in text:
                failures.append(f"{relative}: leaf string {needle!r} from tests/expected.json")
                break

if failures:
    for f in failures:
        print("LEAK", f)
    sys.exit(1)
PYEOF
)
    rc=$?
    if [ $rc -ne 0 ]; then
        echo "FAIL $task_dir: oracle leak detected"
        echo "$OUT" | sed 's/^/  /'
        FAILED=1
    fi
done

if [ $FAILED -eq 1 ]; then
    echo ""
    echo "Some tasks leak ground-truth content into environment/ which the agent can see."
    echo "Fix by re-running tools/case_builder/export_to_harbor.py (it has its own anti-leak"
    echo "guard) or by manually removing the leaking strings from environment/ files."
    exit 1
fi

echo "All tasks clean: no oracle leakage into environment/"
