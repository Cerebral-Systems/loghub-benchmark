#!/usr/bin/env bash
set -euo pipefail

cd "${LOGHUB_BENCHMARK_DIR:-/home/buildout/loghub-benchmark-hardening}"

export PATH="/root/.local/bin:${PATH}"
export PYTHONPATH=".context:${PYTHONPATH:-}"

: "${DEVIN_API_KEY:?DEVIN_API_KEY must be set or provided by --env-file}"
export DEVIN_MAX_ACU_LIMIT="${DEVIN_MAX_ACU_LIMIT:-5}"
export DEVIN_WALL_TIMEOUT_SEC="${DEVIN_WALL_TIMEOUT_SEC:-1200}"
export DEVIN_POLL_INTERVAL_SEC="${DEVIN_POLL_INTERVAL_SEC:-20}"

echo "START $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "adapter=.context/devin_harbor_agent.py"
echo "agent_import_path=devin_harbor_agent:DevinHarborAgent"
echo "devin_max_acu_limit=${DEVIN_MAX_ACU_LIMIT}"
echo "devin_wall_timeout_sec=${DEVIN_WALL_TIMEOUT_SEC}"

extra_args=()
if [[ -n "${HARBOR_N_TASKS:-}" ]]; then
  extra_args+=(--n-tasks "${HARBOR_N_TASKS}")
fi

harbor run \
  -p "${HARBOR_TASK_PATH:-tasks}" \
  --agent-import-path devin_harbor_agent:DevinHarborAgent \
  --n-concurrent "${HARBOR_N_CONCURRENT:-2}" \
  --agent-timeout-multiplier "${HARBOR_AGENT_TIMEOUT_MULTIPLIER:-4.0}" \
  --job-name "${HARBOR_JOB_NAME:-devin-api-single-session-hardened-180}" \
  -o "${HARBOR_JOBS_DIR:-jobs}" \
  -y \
  --quiet \
  --artifact /app/answer.json \
  "${extra_args[@]}"

echo "END $(date -u +%Y-%m-%dT%H:%M:%SZ)"
