#!/bin/bash

# Fails if task.toml does not explicitly set [environment].allow_internet = false.
#
# The Loghub SRE benchmark intentionally disables internet access during
# task execution. Runtime and verifier dependencies must be baked into the
# task image or local harness setup.
#
# The key invariant is that the policy must be explicit and consistent
# across generated tasks, docs, and CI.

set -e

# Arguments: task directories (e.g., tasks/my-task) or no args to check all
if [ $# -eq 0 ]; then
    FILES_TO_CHECK=$(find tasks -type f -name "task.toml")
else
    FILES_TO_CHECK=""
    for task_dir in "$@"; do
        if [ -d "$task_dir" ] && [ -f "$task_dir/task.toml" ]; then
            FILES_TO_CHECK="$FILES_TO_CHECK $task_dir/task.toml"
        fi
    done
fi

if [ -z "$FILES_TO_CHECK" ]; then
    echo "No task.toml files to check"
    exit 0
fi

FAILED=0
for file in $FILES_TO_CHECK; do
    if [ ! -f "$file" ]; then
        echo "File $file does not exist, skipping"
        continue
    fi

    echo "Checking $file..."

    RESULT=$(python3 - "$file" <<'PYEOF'
import sys

path = sys.argv[1]

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore

with open(path, "rb") as f:
    data = tomllib.load(f)

value = data.get("environment", {}).get("allow_internet")
if value is None:
    # Default is True per harbor.models.task.config.EnvironmentConfig.
    print("environment.allow_internet not set; Loghub SRE tasks must declare false explicitly")
    sys.exit(1)
if value is not False:
    print("environment.allow_internet is not false; Loghub SRE tasks run offline")
    sys.exit(1)
PYEOF
    ) || {
        echo "$RESULT" | while IFS= read -r line; do
            [ -n "$line" ] && echo "FAIL $file: $line"
        done
        FAILED=1
        continue
    }
done

if [ $FAILED -eq 1 ]; then
    echo ""
    echo "Some task.toml files do not explicitly disable internet access."
    echo "Loghub SRE tasks must set [environment].allow_internet = false"
    echo "and bake runtime dependencies into the image or local harness."
    exit 1
fi

echo "All task.toml files explicitly disable internet access (allow_internet = false)"
