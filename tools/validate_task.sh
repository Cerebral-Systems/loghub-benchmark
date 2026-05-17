#!/bin/bash
# Validate one Harbor task with oracle and nop agents.

set -u

SLUG="$1"
ROOT="${ROOT:-$(pwd)}"
HARBOR_BIN="${HARBOR_BIN:-harbor}"

if [ "$HARBOR_BIN" = "harbor" ] && [ -x "$ROOT/.venv-tools/bin/harbor" ]; then
    HARBOR_BIN="$ROOT/.venv-tools/bin/harbor"
fi

TMPJ=$(mktemp -d -t harbor-XXXXXXXX)
trap 'rm -rf "$TMPJ"' EXIT

"$HARBOR_BIN" run -p "$ROOT/tasks/$SLUG" --agent oracle --jobs-dir "$TMPJ" > "$TMPJ/oracle.stdout" 2>&1
ORACLE=$(cat "$TMPJ"/*/result.json 2>/dev/null \
    | python3 -c "import sys,json; d=json.load(sys.stdin); print(list(d['stats']['evals'].values())[0]['metrics'][0]['mean'])" 2>/dev/null || echo ERR)

# Clear the jobs dir before nop run so we read the right result.json.
rm -rf "$TMPJ"/[0-9]*

"$HARBOR_BIN" run -p "$ROOT/tasks/$SLUG" --agent nop --jobs-dir "$TMPJ" > "$TMPJ/nop.stdout" 2>&1
NOP=$(cat "$TMPJ"/*/result.json 2>/dev/null \
    | python3 -c "import sys,json; d=json.load(sys.stdin); print(list(d['stats']['evals'].values())[0]['metrics'][0]['mean'])" 2>/dev/null || echo ERR)

echo "$SLUG oracle=$ORACLE nop=$NOP"
