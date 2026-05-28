# Leaderboard artifact — `claude-opus-4-7`, 180-task hardened benchmark

Authoritative proof bundle for the Claude Code (API-key) Opus 4.7 leaderboard row.

| Field | Value |
|---|---|
| Run ID | `claude-api-opus-180-20260528T194734Z` |
| Model | `claude-opus-4-7` (`ANTHROPIC_MODEL`) |
| Harness | Harbor `claude-code` agent, `claude` CLI 2.1.154 |
| Auth | **API key** (`apiKeySource: ANTHROPIC_API_KEY`, all 180 trials) — no subscription session cap |
| Tasks | 180 / 180 completed |
| **Mean reward** | **0.8777** |
| Fully solved (reward 1.0) | 45 (25%) |
| Errors / retries | 0 / 0 |
| Mean latency/task | 1.87 min |
| Wall-clock runtime | 2h 48m 11s |
| **Total cost** | **$99.55** ($0.55/task mean) |
| Concurrency | 2 |
| Per-task caps | `max_budget_usd=3.00`, `max_turns=40` |
| Date (UTC) | 2026-05-28 |

## What's in this bundle

- `result.json` — Harbor's top-level job result (per-task `reward_stats`, eval metrics, 0 errors). The authoritative scoreboard.
- `per_task.csv` — one row per trial: `trial, reward, cost_usd, apiKeySource`. Reward sourced from `result.json` `reward_stats`; cost/auth parsed from each trial's `agent/claude-code.txt`.
- `checksums.txt` — SHA-256 of the files here plus the full-run tarball.

## Full raw run (transcripts, verifier logs)

The complete 104 MB job directory (every trial's agent transcript, verifier output, artifacts) is archived **outside git** at:

```
/home/buildout/benchmark-artifacts/claude-api-opus-180-20260528T194734Z.tar.gz
```

Its SHA-256 is recorded in `checksums.txt`. `jobs/` is gitignored, so the raw run is intentionally not committed; this tarball is the durable copy.

## Reproduce the numbers

```bash
# mean reward + error count (from the committed scoreboard)
python3 -c "import json;e=json.load(open('result.json'))['stats']['evals'];k=next(iter(e));print(e[k]['metrics'][0]['mean'], 'errors=',e[k]['n_errors'])"

# total cost across all trials
awk -F, 'NR>1{s+=$3} END{printf \"$%.2f\\n\", s}' per_task.csv
```

## Context

This run replaces the broken `claude-host-auth-hardened-180` row (mean 0.361, 104 errors). Those errors were Claude.ai subscription **session-limit (HTTP 429)** failures from host-auth credentials — not a model or task issue. Switching to `ANTHROPIC_API_KEY` auth removed the session cap; the run completed 180/180 with 0 errors.
