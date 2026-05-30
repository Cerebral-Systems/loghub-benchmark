# Devin API Merged 180-Task Run

Leaderboard row: `devin-api-merged-180-20260530`

This result reports Devin as a single-session API agent, not Auto-Triage. The
score is merged from two Harbor jobs because the first run exhausted Devin
credits:

- `devin-api-full-180-20260528T122056Z`: 20 scored rows from the initial run.
- `devin-api-remaining-160-20260529T095246Z`: continuation over the remaining
  160 tasks.

Merged score:

- Mean reward: `0.7470830095830095`
- Reward sum: `134.47494172494171 / 180`
- Fully solved: `38 / 180`
- Selected-task exceptions counted as zero: `26`

Files:

- `SUMMARY.json`: merged score and source job stats.
- `merged-scores.csv`: one selected reward per task.
- `devin-repro-final-20260530T051302Z-sanitized.tar.gz`: sanitized Harbor artifacts and
  adapter snapshot. This excludes credentials and `/root/.env`.
- `run-devin-api-hardened.sh`: original run wrapper used on the SSH machine.
- `run-devin-remaining-160.sh`: continuation wrapper used on the SSH machine.
- `terminate-devin-sessions-from-run.py`: cleanup helper used before the
  continuation run.

To rerun from this repository, use the tracked adapter:

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

The reported row is a merged, quota-split result. A clean future rerun should
use the same adapter and run all 180 tasks in one uninterrupted job.
