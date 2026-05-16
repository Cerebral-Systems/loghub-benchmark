# Local-validation entry points for the Loghub SRE benchmark.
#
# `just validate-all` mirrors the gates that .github/workflows/ runs on
# every PR. Run it before pushing if you want fast feedback without
# waiting for GitHub Actions.

# Default target shows what's available.
default:
    @just --list

# All 12 ci_checks/*.sh against every task in tasks/.
static:
    #!/usr/bin/env bash
    set -e
    fail=0
    for slug in $(ls tasks 2>/dev/null | grep -v '^\.'); do
      for check in canary task-fields task-slug dockerfile-references dockerfile-sanity \
                   task-absolute-path test-file-references test-sh-sanity task-timeout \
                   instruction-timeout-match gpu-types allow-internet; do
        if ! bash ci_checks/check-${check}.sh "tasks/${slug}" >/dev/null 2>&1; then
          echo "FAIL ${slug} :: check-${check}.sh"
          fail=$((fail+1))
        fi
      done
    done
    if [ $fail -gt 0 ]; then echo ""; echo "${fail} failure(s)"; exit 1; fi
    echo "static checks: $(ls tasks | grep -v '^\.' | wc -l) tasks × 12 checks all green"

# harbor run --agent oracle (must yield 1.0) + --agent nop (must yield 0.0)
# for every task. Slow — ~60-70s per task at 6-way parallel = ~12 min for 60 tasks.
# Writes per-task results to /tmp/m4-validation.log.
oracle-nop:
    #!/usr/bin/env bash
    set -e
    : > /tmp/just-validate.log
    : > /tmp/just-validate.err
    ls tasks | grep -v '^\.' | xargs -P 6 -I {} bash /tmp/validate-task.sh {} \
        2>>/tmp/just-validate.err | tee -a /tmp/just-validate.log
    total=$(wc -l </tmp/just-validate.log)
    green=$(grep -c '^.* oracle=1.0 nop=0.0$' /tmp/just-validate.log || true)
    echo ""
    echo "oracle/nop: ${green}/${total} green"
    if [ "$green" != "$total" ]; then
      echo "fail rows:"
      grep -v 'oracle=1.0 nop=0.0$' /tmp/just-validate.log
      exit 1
    fi

# Adapter + exporter unit tests.
unit:
    .venv-tools/bin/python -m pytest tools/case_builder/tests -q

# Everything — same gates as the CI workflows.
validate-all: unit static oracle-nop
    @echo ""
    @echo "All M4-level gates green."

# Regenerate the 60-task curated set from scratch (case-builder + exporter
# + the M4 curation list). Use after corpus updates or adapter version bumps.
rebuild-tasks:
    #!/usr/bin/env bash
    set -e
    rm -rf /tmp/cases-m4-* /tmp/tasks-staging
    mkdir -p /tmp/tasks-staging
    for d in hdfs hadoop bgl thunderbird openstack; do
      max=60; [ "$d" = "hadoop" ] && max=44; [ "$d" = "openstack" ] && max=12
      input=/home/buildout/loghub-full/${d^}
      [ "$d" = "hdfs" ] && input=/home/buildout/loghub-full/HDFS
      .venv-tools/bin/python -m tools.case_builder.build_cases \
        --adapter $d --input "$input" --output /tmp/cases-m4-$d --max-cases $max --seed 0
      .venv-tools/bin/python -m tools.case_builder.export_to_harbor \
        --cases-dir /tmp/cases-m4-$d --output-dir /tmp/tasks-staging
    done
    @echo "staging populated; copy the curated slugs back into tasks/ manually"
