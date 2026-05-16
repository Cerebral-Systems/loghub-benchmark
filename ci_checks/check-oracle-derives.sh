#!/bin/bash
#
# Enforces CLAUDE.md's "Oracle solution rule": solve.sh must DERIVE the
# answer via computation on the visible log, not `cp /tests/expected.json
# /app/answer.json` or any equivalent shortcut. This is the static-time
# guard that catches the failure the M7 `solution_quality` rubric
# criterion catches at review time.

set -e

if [ $# -lt 1 ]; then
    TASK_DIRS=$(find tasks -mindepth 1 -maxdepth 1 -type d 2>/dev/null)
else
    TASK_DIRS="$@"
fi

if [ -z "$TASK_DIRS" ]; then
    echo "No task directories to check"
    exit 0
fi

FAILED=0
for task_dir in $TASK_DIRS; do
    solve="$task_dir/solution/solve.sh"
    [ -f "$solve" ] || continue
    # Flag any direct cat/cp of expected.json into the agent's /app/ tree.
    if grep -qE '(cp|cat)\s+.*/tests/expected\.json' "$solve"; then
        echo "FAIL $task_dir: solve.sh shortcuts the oracle by copying tests/expected.json"
        echo "   Oracle's solve.sh must read the log and compute the answer, per CLAUDE.md."
        FAILED=1
    fi
    if grep -qE 'cat\s+.*expected\.json.*>\s*/app/answer\.json' "$solve"; then
        echo "FAIL $task_dir: solve.sh pipes expected.json directly into /app/answer.json"
        FAILED=1
    fi
done

if [ $FAILED -eq 1 ]; then
    echo ""
    echo "Some solve.sh scripts shortcut the oracle. Replace the cat/cp with a"
    echo "real derivation: read /app/*.log + /solution/oracle_hints.json and"
    echo "build the answer fields from the log content."
    exit 1
fi

echo "All solve.sh scripts derive their answer (no expected.json shortcut)"
