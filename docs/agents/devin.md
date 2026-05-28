# Devin API Benchmark Adapter

Use the Devin API path for this benchmark, not a `mini-swe-agent` model swap.
Devin is not a LiteLLM model behind the mini-SWE loop; it is a hosted agent
session with its own VM, file attachment API, session lifecycle, and structured
output field. The Harbor adapter is the correct boundary because Harbor owns the
task container and verifier, while Devin owns the remote investigation session.

The adapter in `.context/devin_harbor_agent.py` runs one fresh Devin session per
Harbor task:

1. Reads the task instruction and visible `/app` files from the Harbor
   container.
2. Builds a line-numbered text bundle so Devin can cite exact file/line
   evidence.
3. Uploads that bundle through the Devin attachment API.
4. Creates a Devin session with a Draft-7 structured-output schema matching the
   task family (`v2`, `fp`, `seq`, `corr`, `sev`, `tmpl`, or `v3-remediation`).
5. Polls the session until terminal status or the wall-clock cap.
6. Writes Devin's `structured_output` back to `/app/answer.json`.
7. For remediation tasks, executes the exact `mitigation.action` and
   `mitigation.target` selected by Devin via `/app/bin/apply_mitigation`, then
   records the real `/app/bin/check_health` result in `postcheck`.

This should be reported as `Devin (API, single-session, no memory)`, not
`Devin Auto-Triage`. Auto-Triage's product-specific pieces (parent monitor,
Slack/webhook trigger, cross-incident scratchpad, routing/dedup memory) are not
part of this independent per-task Harbor run and would contaminate scores.

## Run

From a machine with Docker, Harbor, and `DEVIN_API_KEY` available:

```bash
export DEVIN_API_KEY=...
export PYTHONPATH=".context:${PYTHONPATH:-}"

harbor run \
  -p tasks \
  --agent-import-path devin_harbor_agent:DevinHarborAgent \
  --n-concurrent 2 \
  --agent-timeout-multiplier 4.0 \
  --job-name devin-api-single-session-hardened-180 \
  -o jobs \
  -y \
  --quiet \
  --artifact /app/answer.json
```

Or use the wrapper:

```bash
DEVIN_API_KEY=... .context/run-devin-api-hardened.sh
```

Useful knobs:

| Env var | Default | Purpose |
|---|---:|---|
| `DEVIN_MAX_ACU_LIMIT` | `5` | Per-task ACU cap sent to Devin. Publish this with results. |
| `DEVIN_WALL_TIMEOUT_SEC` | `1200` | Adapter-side polling cap. |
| `DEVIN_POLL_INTERVAL_SEC` | `20` | Session polling interval. |
| `HARBOR_N_CONCURRENT` | `2` | Parallel task count for the wrapper script. |
| `HARBOR_TASK_PATH` | `tasks` | Full run or a task/slice path for pilots. |
| `HARBOR_JOB_NAME` | `devin-api-single-session-hardened-180` | Output job id. |
| `HARBOR_JOBS_DIR` | `jobs` | Job output directory. |

Start with a small pilot before spending a full run:

```bash
HARBOR_TASK_PATH=tasks/hdfs-datanode-0b694b5 \
HARBOR_JOB_NAME=devin-api-pilot-hdfs \
HARBOR_N_CONCURRENT=1 \
.context/run-devin-api-hardened.sh
```

## Caveats

- The adapter transfers task evidence into Devin; Devin cannot directly browse
  the Harbor container.
- Remediation execution is mechanical: Devin chooses the action and target, the
  adapter applies exactly those values.
- Large tasks upload multi-megabyte line-numbered bundles, so API latency and
  ACU use will be higher than mini-SWE local model calls.
- If Devin returns no structured output, the adapter writes a minimal schema
  placeholder so the Harbor trial completes with verifier failures rather than
  a harness exception.
