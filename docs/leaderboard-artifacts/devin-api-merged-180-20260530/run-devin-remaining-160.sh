#!/usr/bin/env bash
set -euo pipefail

cd "${LOGHUB_BENCHMARK_DIR:-/home/buildout/loghub-benchmark-hardening}"

if [[ -f .context/devin.env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .context/devin.env
  set +a
fi

export HARBOR_TASK_PATH="${HARBOR_TASK_PATH:-.context/devin-remaining-160/tasks}"
export HARBOR_JOB_NAME="${HARBOR_JOB_NAME:-devin-api-remaining-160-$(date -u +%Y%m%dT%H%M%SZ)}"
export HARBOR_N_CONCURRENT="${HARBOR_N_CONCURRENT:-1}"
export HARBOR_AGENT_TIMEOUT_MULTIPLIER="${HARBOR_AGENT_TIMEOUT_MULTIPLIER:-4.0}"

export DEVIN_MAX_ACU_LIMIT="${DEVIN_MAX_ACU_LIMIT:-3}"
export DEVIN_WALL_TIMEOUT_SEC="${DEVIN_WALL_TIMEOUT_SEC:-900}"
export DEVIN_POLL_INTERVAL_SEC="${DEVIN_POLL_INTERVAL_SEC:-20}"

log_path=".context/${HARBOR_JOB_NAME}.log"
echo "job_name=${HARBOR_JOB_NAME}"
echo "task_path=${HARBOR_TASK_PATH}"
echo "n_concurrent=${HARBOR_N_CONCURRENT}"
echo "devin_max_acu_limit=${DEVIN_MAX_ACU_LIMIT}"
echo "devin_wall_timeout_sec=${DEVIN_WALL_TIMEOUT_SEC}"
echo "log_path=${log_path}"

.context/run-devin-api-hardened.sh 2>&1 | tee "${log_path}"
