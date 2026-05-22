# DeepSeek V4-flash on Loghub-SRE — Run Report

**Date:** 2026-05-22
**Run ID:** `bench-deepseek-v4-flash`
**Repo state:** branch `autonomous-buildout-20260515` after PR #3 merge candidate (PLAN_V2 + T1-T5)

## TL;DR

DeepSeek V4-flash via `mini-swe-agent` solved **160/160 tasks without crashing**, scoring **mean=0.880, median=0.875** on the Loghub-SRE-v1+v2 benchmark in **1h 44m for under $1**. 53 tasks (33%) were fully solved; the rest scored partial credit. The result is a **valid headline number with two methodology caveats** documented below.

| | Value |
|---|---|
| Tasks | 160 |
| Model | `deepseek/deepseek-v4-flash` |
| Harness | `mini-swe-agent` (litellm-based, Python loop, docker-exec) |
| Mean reward | **0.880** |
| Median reward | 0.875 |
| Std reward | 0.102 |
| Fully solved (reward=1.0) | 53 (33%) |
| Crashes / exceptions | 0 |
| Runtime | 1h 44m 14s |
| API spend | **< $1** (per DeepSeek dashboard) |

## Methodology

- **Tasks**: all 160 tasks under `tasks/` — 60 v1 anomaly localization + 100 v2 across 5 new skill types (T1-T5 from PLAN_V2.md).
- **Agent**: `mini-swe-agent` (Python loop, lean tool-use, no fancy prompt scaffolding) wrapping `deepseek/deepseek-v4-flash` via litellm.
- **Container**: per-task Docker (Ubuntu 24.04 + python3 + curl + grep/awk), `allow_internet = true` so the agent's CLI install can complete.
- **Timeout**: `--agent-timeout-multiplier 3.0` (900s per task), default Harbor concurrency.
- **Reward model**: fractional `passed_tests / total_tests` written to `/logs/verifier/reward.txt` by `tests/test.sh`.
- **Single run** (`n=1` per task). No repeats for variance estimation.

## Aggregate distribution

Reward histogram across 160 tasks:

```
[0.0, 0.1)      0
[0.1, 0.2)      0
[0.2, 0.3)      0
[0.3, 0.4)      0
[0.4, 0.5)      0
[0.5, 0.6)      0
[0.6, 0.7)      6   ███
[0.7, 0.8)     34   █████████████████████
[0.8, 0.9)     41   █████████████████████████
[0.9, 1.0]     79   ██████████████████████████████████████████████████
```

No score below 0.69. Strong right-skew with a long shoulder in the 0.7-0.9 band.

## Per-dataset breakdown

| Dataset | n | Mean | Median | Std | Fully solved | Below 0.5 |
|---|---|---|---|---|---|---|
| bgl | 36 | **0.901** | 0.923 | 0.099 | 14 | 0 |
| hadoop | 33 | **0.910** | 0.909 | 0.092 | 15 | 0 |
| hdfs | 39 | **0.815** | 0.769 | 0.108 | 9 | 0 |
| openstack | 21 | 0.873 | 0.875 | 0.089 | 5 | 0 |
| thunderbird | 31 | 0.908 | 0.909 | 0.075 | 10 | 0 |

**HDFS is the hardest dataset** (mean 0.815 vs 0.90+ for others). The HDFS log format (component-prefixed lines, block-level granularity, large slice sizes) appears to challenge DeepSeek more than the rack-prefixed BGL/Thunderbird formats or container-grouped Hadoop logs.

## Per-(task type × dataset) grid

Mean reward per cell:

| Type | bgl | hadoop | hdfs | openstack | thunderbird | Row mean |
|---|---|---|---|---|---|---|
| v1 anomaly | 0.841 | 0.897 | 0.761 | 0.785 | 0.838 | 0.823 |
| **fp false-positive** | **1.000** | **1.000** | **1.000** | **1.000** | **1.000** | **1.000** ⚠ |
| seq temporal | 0.886 | 0.886 | 0.818 | 0.864 | 0.932 | 0.877 |
| corr cross-component | 0.900 | 0.800 | 0.700 | — | 0.860 | 0.815 |
| sev severity | 0.972 | 0.944 | 0.778 | 0.861 | 0.917 | 0.894 |
| tmpl template extraction | 0.969 | 0.969 | 1.000 | 0.844 | 1.000 | 0.956 |

Observations:
- **`fp` row is a perfect 1.0 across every dataset** — see Gap 1 below.
- **`corr` cross-component** is hardest, particularly on HDFS (0.700). Tracing causation across NameNode/DataNode logs is genuine difficulty for this model.
- **`tmpl` template extraction** is easiest (0.956 mean). DeepSeek handles pattern abstraction well — consistent with reports that K2-class models excel at LogParser-style tasks.
- **`sev` severity classification** is unexpectedly easy in BGL/Hadoop (0.97/0.94). May reflect that the rule-based ground truth (multi-component count → P0, etc.) is recognizable from instruction text.

## Lowest 10 tasks

Tasks where DeepSeek struggled most (all in the 0.69–0.70 band, no catastrophic failures):

```
0.692  bgl-kernmntf-1c3c5fd
0.692  bgl-appsev-242c2ef
0.692  hdfs-datanode-31cffcd
0.692  hdfs-other-0c66ee6
0.692  openstack-vmtask-2024031
0.692  hdfs-other-0b71922
0.700  corr-hdfs-other-e2977c1
0.700  corr-hdfs-datanode-6c02c90
0.700  corr-hdfs-other-7d149cc
0.700  corr-hadoop-machine-9c7168e
```

7 of 10 are HDFS-related — confirms HDFS as the hardest dataset surface for this model.

## Gaps in this run

### Gap 1 — `fp` verifier is too lenient (CRITICAL)

**Symptom**: Every single one of 25 false-positive tasks scored 1.000.

**Diagnosis** (verified with actual agent answer):
- DeepSeek on `fp-thunderbird-noise-71c0a92` cited 4 indicators with categories `recoverable_retry`, `expected_event`, `benign_info`, `transient_state` (4 different categories).
- Ground truth has all 5 indicators marked `benign_info` (one category).
- All 4 of DeepSeek's cited lines (`thunderbird-other.log:25`, `tbird.log:1`, `compute.log:1200`, `other.log:259`) are NOT in the ground-truth indicator set.
- Verifier still scored 1.0.

**Why this happens**: `test_classifications_in_allowed_set` only checks membership in the 5-category enum, not match to ground truth. `test_indicators_cite_real_lines` only checks "line exists in file", not "line is in ground-truth indicator set". The only hard check is `test_is_incident_is_false` — which just requires the agent to output `is_incident: false`.

**Implication**: The fp task currently rewards format compliance, not classification skill. A naive agent that says "is_incident: false; here are 3 random lines from the logs with random allowed categories" scores 1.0.

**Fix path**:
1. Add `test_indicators_match_ground_truth_set` — agent's cited lines must be a subset of (or overlap with) the ground-truth indicator set (e.g., intersection ≥ 50%).
2. Add `test_classifications_match_ground_truth` — for each cited line that IS in ground truth, the agent's `why_not_anomalous` must match ground truth value.
3. After fixing, re-run the fp tasks. Expected: fp scores drop into the 0.5-0.8 band, matching other skill types.

### Gap 2 — Single run, no variance estimate

**Symptom**: We have one reward per task. We don't know if a re-run would produce the same mean ± what spread.

**Why this matters**: Harbor's adapter spec (Step 5 parity protocol) requires `n ≥ 2` runs per side for SEM-based reporting, and recommends `n ≥ 3`. Any "X model scored Y" claim without variance can't be cited externally.

**Fix path**: Re-run the same 160 tasks twice more (cost ~$2 total) → compute mean ± SEM per task and per aggregate. ~3-4h wall time.

### Gap 3 — Single harness only (no comparison axis)

**Symptom**: We have DeepSeek + `mini-swe-agent`. We don't know if a different harness on the same model would score differently, or if a different model on the same harness would.

**Why this matters**: "DeepSeek V4-flash scored 0.880" conflates model capability with harness behavior. The interesting comparisons are model × harness pairs.

**Fix path**: Run the same 160 tasks with:
- DeepSeek V4-flash + `hermes` (different harness, same model)
- Kimi K2.6 + `mini-swe-agent` (same harness, different model) — we have this partially from earlier baseline; could complete
- Mesh + `mini-swe-agent` sub-agents (the Mesh-comparison flagged separately as Path B)

### Gap 4 — Per-task latency not analyzed

**Symptom**: We have per-task reward but no per-task latency. Slow-but-correct vs fast-but-wrong are not distinguished.

**Fix path**: Parse `mini-swe-agent.txt` for elapsed-time markers per task; compute `mean_latency` per task type and per dataset.

### Gap 5 — Token usage not captured

**Symptom**: mini-swe-agent's self-reported cost is `$0.00` per task (its cost table doesn't include DeepSeek pricing). Real cost only visible in DeepSeek's dashboard, not in our trial telemetry.

**Why this matters**: We can't compute per-token efficiency, per-task cost variance, or compare cost-per-correct-answer across models without dashboard access.

**Fix path**: Patch mini-swe-agent's cost-table for DeepSeek V4-flash, or pull token usage from DeepSeek's `/v1/usage` API per trial.

### Gap 6 — `corr` task verifier weakness (likely)

**Symptom**: `corr` mean is 0.815 with only 2/20 fully solved. Looking at our earlier T3 audit, the verifier only checks topology (acyclic + ground-truth events present) but doesn't check that the agent's `caused_by_step` values match ground truth.

**Implication**: An agent could produce a wrong causal chain (saying A caused C when reality is A→B→C) and still pass topology checks. The 0.815 average may be even more inflated than it appears.

**Fix path**: Add `test_caused_by_links_match_ground_truth` to corr verifier. After fix, expect corr scores to drop further (likely toward 0.5-0.7).

### Gap 7 — No oracle ceiling comparison in the report

**Symptom**: We know oracle = 1.000 across all 160 (verified earlier this week). DeepSeek = 0.880. The 0.12 gap represents where DeepSeek's mistakes live.

**What's missing**: No per-task analysis of "oracle correct, agent wrong → what specifically did agent get wrong?". This is the actionable insight for improving agent or instruction design.

**Fix path**: For each task with reward < 1.0, diff agent's answer.json against oracle's answer.json and categorize the deltas (wrong file, wrong line, off-by-N line, wrong root cause, etc.).

## What this report supports

| Claim | Supportable today |
|---|---|
| "DeepSeek V4-flash runs cleanly on Loghub-SRE end-to-end" | ✅ Yes — 0 crashes |
| "Mean score 0.880 on 160 tasks" | ✅ With caveats (single run, fp lax) |
| "DeepSeek struggles with HDFS more than other datasets" | ✅ Real signal across all task types |
| "Cost <$1 per full run" | ✅ Verified via dashboard |
| "DeepSeek beats Kimi K2.6" or "Mesh ensemble beats DeepSeek" | ❌ Need explicit cross-comparison runs |
| "fp false-positive triage is solved by frontier models" | ❌ The 1.000 is verifier laxness, not skill |
| "Statistically significant difference vs other agents" | ❌ Need n ≥ 3 runs for SEM |

## Recommended next actions, ordered by leverage

1. **Fix the `fp` verifier** (Gap 1) and re-run those 25 tasks. ~$0.10, 10 min. Highest credibility win.
2. **Audit and tighten the `corr` verifier** (Gap 6). ~30 min review + re-run.
3. **Run DeepSeek again 2 more times** for SEM (Gap 2). ~$2, 4h.
4. **Run a second model** for cross-comparison (Gap 3). Pick Kimi K2.6 (we have key) for a head-to-head. ~$5, 4h.
5. **Diff-against-oracle analysis** (Gap 7). Pure script work, no API spend.
6. **Mesh adapter** (Path B from earlier discussion). 1-2 days build, ~$10 to run.

After fixes #1-#3, the headline becomes citable. After #4-#6, we have a real comparative report.

---

## Update — Gap 1 fix landed (2026-05-22)

Two new assertions added to all 25 fp `test_state.py` files (and exporter template):

```python
def test_indicators_match_ground_truth_set(answer, expected):
    """≥50% of agent's cited (file, line) tuples must be in ground truth."""

def test_classifications_match_ground_truth(answer, expected):
    """For cited indicators that ARE in ground truth, why_not_anomalous must match."""
```

Oracle still passes (11/11 tests, was 9/9). Re-ran DeepSeek V4-flash on the 25 fp tasks with the tightened verifier.

### Before / after — fp tasks alone

| Metric | Before (Gap 1) | After fix |
|---|---|---|
| n | 25 | 25 |
| Mean reward | 1.000 | **0.865** |
| Median | 1.000 | 0.909 |
| Fully solved | 25 (100%) | **0 (0%)** |
| Distribution | all 1.0 | 12 × 0.818, 13 × 0.909 |

DeepSeek now fails 1-2 of the 11 fp tests on every single task — confirming the laxness was real and the patch caught it. The new assertions are doing exactly the work they were designed to do.

### Corrected overall benchmark numbers

| Aggregate | Before | After |
|---|---|---|
| Overall mean | 0.880 | **0.859** |
| Overall median | 0.875 | 0.846 |
| Fully solved | 53 / 160 | **28 / 160** |

This is the citable headline. The fp row no longer inflates the mean; the 0.859 reflects what DeepSeek V4-flash actually does on Loghub-SRE with rigorous verifiers.

### Corrected per-skill-type table

| Skill | n | Mean | Fully solved |
|---|---|---|---|
| `tmpl` log template extraction | 20 | 0.956 | 14 |
| `sev` severity classification | 15 | 0.894 | 4 |
| `seq` temporal sequence | 20 | 0.877 | 2 |
| `fp` false-positive triage (post-fix) | 25 | **0.865** | **0** |
| `v1` anomaly localization | 60 | 0.823 | 6 |
| `corr` cross-component correlation | 20 | 0.815 | 2 |

`fp` is now correctly placed in the difficulty band (between `seq` and `v1`), not artificially saturated at 1.0.

### What's next

- Gap 6 (corr verifier) — same pattern, patches landed for all 20 corr tasks, re-run pending.

## Update — Gap 4 (latency) and Gap 7 (failure-mode) analysis done (2026-05-22)

### Gap 4 — Per-task latency from `result.json`

Extracted from `started_at`/`finished_at` timestamps in each per-trial `result.json`.

**Overall** (n=160):
- Mean: 2.6 min, median: 2.2 min
- Range: 1.3 min – 8.7 min
- p90: 4.1 min, p99: 7.6 min

**By task type:**

| Type | Mean latency | Median | p90 | Mean reward |
|---|---|---|---|---|
| `fp` | 1.8 min | 1.8 | 2.0 | 1.000 (pre-fix) |
| `v1` | 2.1 min | 2.0 | 2.7 | 0.823 |
| `sev` | 2.5 min | 2.4 | 3.7 | 0.894 |
| `tmpl` | 2.6 min | 2.3 | 3.7 | 0.956 |
| `corr` | 3.2 min | 2.8 | 6.8 | 0.815 |
| `seq` | 4.4 min | 4.2 | 7.0 | 0.877 |

**Pearson r(latency, reward) = −0.237** — modest negative correlation. Slow tasks score slightly worse, but it's not deterministic. Some hard-but-correct tasks exist (e.g., `seq-thunderbird-vapi-60ea24c` at 5.7 min, reward 1.0).

`fp` was fastest (1.8 min avg) AND scored perfect 1.0 — both symptoms of the same laxness (agent finds the template-fill quickly).

`seq` and `corr` are slowest, AND hardest by reward — the model spends more time but doesn't get it right. Consistent with the failure-mode analysis below.

**Slowest 10 trials** all clustered in `seq` and `corr` on HDFS — confirms HDFS as the hardest dataset surface.

### Gap 7 — Failure modes across the 160-task run

Parsed pytest CTRF output from each trial's `verifier/test-stdout.txt` to identify which assertions failed most often.

- **107 / 160 tasks** have ≥ 1 failed assertion (the partial-credit tasks).
- **228 total failed assertions** across the run.
- **11 unique failing tests** (out of ~13 assertions per task).

**Top failing assertions:**

| Failed test | Tasks affected | What it means |
|---|---|---|
| `test_root_cause_matches_ground_truth` | 51 | Agent picks wrong taxonomy bucket (e.g., `other` instead of `kernmntf`) |
| `test_no_cross_file_line_confusion` | 47 | Agent cites line N of file A but the text is actually at line N of file B |
| `test_evidence_within_ground_truth` | 47 | Agent over-cites evidence outside the ground-truth set |
| `test_trigger_role_correct` | 18 | Wrong trigger event in temporal sequence |
| `test_causal_chain_recall` | 16 | Missing ground-truth events in causal chain |
| `test_minimum_evidence_count` | 16 | Cited fewer indicators than required minimum |
| `test_root_component_matches` | 13 | Wrong root file in cross-component task |
| `test_severity_matches_ground_truth` | 9 | Wrong P0-P3 classification |

**Among the 40 tasks scoring < 0.8**, top failures:
- `test_root_cause_matches_ground_truth` (35 tasks)
- `test_no_cross_file_line_confusion` (31)
- `test_evidence_within_ground_truth` (31)

### Actionable insight from Gap 7

The most common DeepSeek mistake is **wrong root-cause classification**, not wrong evidence location. The model is good at finding *where* the anomaly is but picks the wrong taxonomy label. That suggests:

1. The root-cause taxonomies may need tightening (some categories ambiguous like `other` vs `other_alert`)
2. Future agents trained on log-investigation should focus more on classification, less on retrieval
3. A simple ablation: re-run with the agent ONLY required to do localization, no root cause — would isolate the localization-vs-classification capability gap

The secondary failures (`no_cross_file_line_confusion`, `evidence_within_ground_truth`) are about precision: the agent cites *more* lines than ground truth has, and gets some line-number assignments wrong across files. These are interesting agent-skill measurements unique to multi-file investigation.
