#!/bin/bash

# Enforce a maximum number of hyphen-separated tokens in the task folder name.
# Long slugs become unwieldy in CLI output, CI logs, and artifact paths.
#
# v1 slugs use 3 tokens (<dataset>-<root-cause>-<short-id>).
# v2/v3 slugs use 4 tokens (<task-type>-<dataset>-<root-cause>-<short-id>).
MAX_TOKENS=4

if [ $# -lt 1 ]; then
    echo "Usage: $0 <task-dir> [task-dir ...]" >&2
    exit 2
fi

failed=0
for task_dir in "$@"; do
    slug=$(basename "$task_dir")
    n=$(awk -F- '{print NF}' <<<"$slug")
    if [ "$n" -gt "$MAX_TOKENS" ]; then
        echo "FAIL $task_dir: slug has $n hyphen-separated tokens (max $MAX_TOKENS)"
        failed=1
    else
        echo "PASS $task_dir ($n tokens)"
    fi
done

exit $failed
