# Devin API Agent

This benchmark reports Devin as `Devin API, single-session`, not Devin
Auto-Triage. Each Harbor task creates one fresh Devin API session with no
cross-task memory, uploads a line-numbered `/app` snapshot as an attachment, and
asks Devin to return the benchmark answer through `structured_output`.

The runnable adapter is [`tools/agents/devin_harbor_agent.py`](../../tools/agents/devin_harbor_agent.py).

## Run A Full Benchmark

```bash
export DEVIN_API_KEY=...
export PYTHONPATH="tools/agents:${PYTHONPATH:-}"
export DEVIN_MAX_ACU_LIMIT=3
export DEVIN_WALL_TIMEOUT_SEC=900
export DEVIN_POLL_INTERVAL_SEC=20

harbor run \
  -p tasks \
  --agent-import-path devin_harbor_agent:DevinHarborAgent \
  --n-concurrent 1 \
  --agent-timeout-multiplier 4.0 \
  --job-name devin-api-single-session-180 \
  -o jobs \
  -y \
  --quiet \
  --artifact /app/answer.json
```

The May 30, 2026 leaderboard row used the same per-task ACU cap (`3`) and
adapter-side wall timeout (`900s`). It was merged from an initial partial run
and a continuation run after credits were replenished; quota/API/timeouts are
counted as zero in the merged score.

## Adapter Behavior

- Collects only visible `/app` files from the task container.
- Excludes `/app/answer.json`.
- Builds a text bundle with 1-based line numbers for every visible file.
- Uploads that bundle through Devin's attachment API.
- Selects the Draft-7 structured-output schema for the task family.
- Writes Devin's structured output to `/app/answer.json`.
- For remediation tasks, applies the selected mitigation inside Harbor and
  records the real postcheck result.
- Terminates the Devin session after answer capture to avoid continuing ACU use.

Artifacts for the reported row are in
[`docs/leaderboard-artifacts/devin-api-merged-180-20260530`](../leaderboard-artifacts/devin-api-merged-180-20260530/).
