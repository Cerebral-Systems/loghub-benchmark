# Mesh on Loghub-SRE-v1

This document describes how **Mesh** — the multi-agent SRE orchestrator from Mesh Intelligence — is evaluated on the Loghub-SRE-v1 benchmark, and reports the headline numbers from the most recent run.

## Why this benchmark

Loghub-SRE-v1 is the only public log-investigation benchmark we know of that:

- Uses **real production logs** at scale (BGL, HDFS, Hadoop, Thunderbird from `logpai/loghub`; OpenStack from a controlled fault-injection run).
- Forces **multi-file investigation** — every task ships 3–6 component-partitioned log files (10k–30k lines total) and concentrates the anomaly in 1–2 of them. The agent must choose where to look.
- Grades **evidence citation strictly** — each cited `(file, line, snippet)` is checked byte-for-byte against the original log; cross-file confusion and over-citing are penalized.
- Is **harness-agnostic** — the verifier reads `/app/answer.json` only, so any agent that can produce JSON works.

That's the right shape to evaluate an SRE agent: the agent has to think about where to look, what evidence is load-bearing, and what category the failure belongs to. Production SRE work is the same job.

## What "Mesh" means in this experiment

Mesh is a multi-agent orchestrator. Its core pattern (from `services/orchestrator/agent_mesh.py`):

1. Receive a task.
2. Dispatch the task to multiple sub-agents in parallel (goose, hermes, codex, claude-code, openclaw, evo, …).
3. Collect attempts.
4. Filter to successful + non-risk-flagged attempts.
5. Select the winner.

For the Loghub-SRE-v1 baseline we mirror this with a faithful 3-attempt ensemble: the same task is given to a Kimi-K2.6-backed mini-swe-agent three independent times, and the **best reward across the three attempts** is the Mesh score.

This isolates the *ensemble lift* (what happens when you don't bet on a single shot) from any single agent's idiosyncratic strengths. It's the cheap end of Mesh's value: even with a homogeneous sub-agent pool, multi-attempt orchestration buys you something. A heterogeneous pool buys you more.

## Experiment setup

| Parameter | Value |
|---|---|
| Benchmark | Loghub-SRE-v1, 60 curated tasks |
| Datasets | HDFS_v1 (18) · Hadoop (12) · BGL (15) · Thunderbird (10) · OpenStack (5) |
| Underlying LLM | Kimi K2.6 (`moonshot/kimi-k2.6`) via Moonshot international endpoint |
| Single-agent baseline | mini-swe-agent, 1 attempt per task |
| Mesh ensemble | mini-swe-agent, 3 attempts per task, score = `max(attempt_i)` |
| Agent timeout | 900s per attempt (3× Harbor task.toml default) |
| Reward | Fractional, `passed_tests / total_tests` (13 assertions per task) |
| Reproduction | `harbor run -p tasks/ --agent mini-swe-agent -m moonshot/kimi-k2.6 --agent-timeout-multiplier 3.0 [-k 3]` |

## Results

> **Status**: results below are auto-generated from `tools/analysis/compare_runs.py`. Run that script against the two job directories once both runs complete.

```
python3 tools/analysis/compare_runs.py \
    baselines/baseline-kimi-k2_6 \
    baselines/mesh-ensemble-k3 \
    > docs/MESH_BENCHMARK.md
```

_<placeholder — will be filled by the compare script once data lands>_

## What we're not yet showing

The 3-attempt ensemble is the cheapest Mesh story. Bigger wins (and more honest positioning) require:

1. **Heterogeneous sub-agents** — run goose + codex + claude-code + mini-swe-agent in parallel, ensemble. Requires multi-provider API keys (Anthropic, OpenAI, Google in addition to Moonshot).
2. **Intelligent aggregation** — instead of pure max-reward, use Mesh's `_collect_attempts` filter (drop risk-flagged attempts, prefer attempts that pass strict assertions over loose ones).
3. **Cross-attempt synthesis** — Mesh can merge evidence from multiple attempts into a single stronger answer. The benchmark currently rewards single-answer submissions; supporting fused answers would require a verifier extension.

These are the upgrade paths if the cheap ensemble already shows meaningful lift.

## Reproducing this experiment

From any clone of this repo:

```bash
# Setup
uv tool install harbor
export MOONSHOT_API_KEY=sk-...

# Single-agent baseline (60 trials, ~1.5h, ~$20)
harbor run -p tasks/ \
    --agent mini-swe-agent \
    -m moonshot/kimi-k2.6 \
    --agent-timeout-multiplier 3.0 \
    --job-name baseline-kimi-k2_6 \
    -o baselines

# Mesh-ensemble run (180 attempts, ~4h, ~$60)
harbor run -p tasks/ \
    --agent mini-swe-agent \
    -m moonshot/kimi-k2.6 \
    --agent-timeout-multiplier 3.0 \
    -k 3 \
    --job-name mesh-ensemble-k3 \
    -o baselines

# Compare
python3 tools/analysis/compare_runs.py \
    baselines/baseline-kimi-k2_6 \
    baselines/mesh-ensemble-k3
```
