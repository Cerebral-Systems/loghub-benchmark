# Loghub SRE Harbor benchmark

A Harbor-compatible benchmark for SRE log-investigation skills.
**160 curated tasks** built from the Loghub corpus (`logpai/loghub`), covering
6 distinct skill types: anomaly localization (v1, 60 tasks), plus 5 v2 skill
axes — false-positive triage, temporal sequence reconstruction, cross-component
correlation, severity classification, and log-template extraction (100 tasks).
Each task ships a Docker environment with 3–6 partitioned log files
totalling 5k–30k lines and asks the agent to investigate the logs and produce
a structured JSON answer that the verifier grades on schema-specific
assertions. The verifier writes a fractional reward (`passed_tests / non_skipped_tests`)
to `/logs/verifier/reward.txt`, so partial-correct answers register on a
continuous 0–1 scale.

## Status

Loghub-SRE is ready for community testing as a Harbor benchmark. The
committed 160-task set (60 v1 + 100 v2) passes the substrate gates:

- adapter/exporter/repo-invariant tests pass.
- `make static` passes all `12 × 160` static checks.
- `make oracle-nop` is green on all tasks: oracle scores `160/160`, nop
  scores `0/160`. Verified end-to-end via `harbor run --agent oracle`
  on every task (11m 25s, 0 exceptions).

First real-agent leaderboard entry below. See
[docs/baselines.md](docs/baselines.md) for the substrate validation
baseline and [docs/REPORT_DEEPSEEK_V4_FLASH.md](docs/REPORT_DEEPSEEK_V4_FLASH.md)
for the full DeepSeek run report (per-dataset, per-skill, identified gaps).

## Leaderboard

| Model | Harness | Tasks | Mean reward | Fully solved | Crashes | Mean latency/task | Runtime | Cost | Date |
|---|---|---|---|---|---|---|---|---|---|
| `deepseek/deepseek-v4-flash` | `mini-swe-agent` | 160 | **0.859** | 28 (18%) | 0 | 2.6 min | 1h 44m | <$1 | 2026-05-22 |

Per-dataset (DeepSeek V4-flash):

| Dataset | n | Mean |
|---|---|---|
| Hadoop | 33 | 0.910 |
| Thunderbird | 31 | 0.908 |
| BGL | 36 | 0.901 |
| OpenStack | 21 | 0.873 |
| HDFS | 39 | 0.815 |

Per-skill-type (DeepSeek V4-flash):

| Skill | n | Mean | Mean latency | Notes |
|---|---|---|---|---|
| `tmpl` log template extraction | 20 | 0.956 | 2.6 min | LogParser-style; strongest |
| `sev` severity classification | 15 | 0.894 | 2.5 min | P0–P3 calibration |
| `seq` temporal sequence | 20 | 0.877 | 4.4 min | Trigger ID + ordering (slowest) |
| `fp` false-positive triage | 25 | 0.865 | 1.8 min | After Gap 1 verifier fix (was 1.000 before tightening) |
| `v1` anomaly localization | 60 | 0.823 | 2.1 min | Original 60-task suite |
| `corr` cross-component | 20 | 0.815 | 3.2 min | Hardest skill — causal chain |

**Latency correlation:** Pearson r(latency, reward) = **−0.237** — slow tasks score slightly worse on average, but the relationship is weak. Some hard tasks are slow AND correct (e.g., `seq-thunderbird-vapi-60ea24c` at 5.7 min, reward 1.0).

**Top failure modes** (across the 107 tasks scoring < 1.0):

| Failed assertion | Tasks affected | Skill area |
|---|---|---|
| `test_root_cause_matches_ground_truth` | 51 | Wrong taxonomy bucket (most common error) |
| `test_no_cross_file_line_confusion` | 47 | Cited line N of file A but text is at line N of file B |
| `test_evidence_within_ground_truth` | 47 | Over-cited evidence outside truth set |
| `test_trigger_role_correct` | 18 | Wrong trigger in temporal sequence |
| `test_causal_chain_recall` | 16 | Missing ground-truth events in causal chain |

Actionable: DeepSeek finds anomaly *locations* well but mis-classifies *root causes* most often. The biggest skill gap is taxonomy mapping, not retrieval.

> The `fp` row was previously 1.000 across all 25 tasks because the verifier only
> checked enum membership. Gap 1 fix landed (2 new tests: indicators must overlap
> ground truth ≥ 50%, classifications must match where indicators overlap). Re-run
> dropped fp mean from 1.000 → 0.865 and overall mean from 0.880 → 0.859. The
> 0.865 fp number is now a real classification-skill measurement, not format-compliance.

Reproducing this run:

```bash
export DEEPSEEK_API_KEY=sk-...
harbor run -p tasks/ --agent mini-swe-agent -m deepseek/deepseek-v4-flash \
  --agent-timeout-multiplier 3.0 --job-name bench-deepseek-v4-flash -o baselines
```

## What's in the box

| Dataset | Tasks | Anomaly source | Partition strategy |
|---|---|---|---|
| HDFS_v1 | 18 | 575k labelled blocks; heuristic root-cause from `Got exception while serving`, `BLOCK_NOT_FOUND`, replication patterns | by Component (NameNode / DataNode-a / DataNode-b / FSNamesystem) |
| Hadoop | 12 | Gold labels from `abnormal_label.txt` (machine_down / disk_full / network_disconnect) | by component (MRAppMaster / mapreduce / yarn) |
| BGL | 15 | Inline 0th-column alert tag (KERNDTLB, APPSEV, KERNSTOR, …) | by full node/location token |
| Thunderbird | 10 | Same inline format as BGL | by hostname role (compute / edge / domain / …) |
| OpenStack | 5 | 4 anomalous VM UUIDs from `anomaly_labels.txt` (rapid-destroy faults) | by OpenStack service (nova-api / nova-compute / nova-scheduler) |

v1 anomaly-localization subtotal: 60 tasks. Distribution and rationale: see [docs/dataset-adapters.md](docs/dataset-adapters.md).

v2 added 100 more tasks across 5 new skill axes — same 5 datasets, different answer schemas and verifier assertions:

| Skill type | Slug prefix | Count | What it tests |
|---|---|---|---|
| False-positive triage | `fp-*` | 25 | `is_incident: false` discrimination + categorize benign noise |
| Temporal sequence | `seq-*` | 20 | Ordered evidence + trigger ID + propagation roles |
| Cross-component correlation | `corr-*` | 20 | Root component + causal chain across files (4 datasets; OpenStack omitted — anomalies don't span components) |
| Severity classification | `sev-*` | 15 | P0–P3 calibration with justification consistency |
| Log template extraction | `tmpl-*` | 20 | Partition raw lines into EventTemplates (LogParser-style) |

Total: **160 tasks** across **6 skill types** × 5 datasets. See [docs/PLAN_V2.md](docs/PLAN_V2.md) for v2 design and [docs/REPORT_DEEPSEEK_V4_FLASH.md](docs/REPORT_DEEPSEEK_V4_FLASH.md) for per-skill agent performance.

## How a task works

```
tasks/<slug>/
├── instruction.md       # what the agent sees
├── task.toml            # Harbor metadata (adapter-spec schema)
├── environment/
│   ├── Dockerfile       # ubuntu:24.04 + python3-pytest, allow_internet=true
│   └── data/
│       ├── <component-1>.log
│       └── <component-N>.log
├── solution/
│   ├── solve.sh         # oracle path
│   ├── derive_answer.py # builds answer.json by reading the visible logs
│   └── oracle_hints.json # (file, line) coords + root cause; oracle-only
└── tests/
    ├── test.sh          # pytest entry the verifier runs
    ├── test_state.py    # verifier assertions against /app/answer.json
    └── expected.json    # verifier ground truth + evidence validation mode
```

## Answer schema

The agent must emit `/app/answer.json` matching:

```json
{
  "schema_version": "loghub-sre-answer-v2",
  "is_incident": true,
  "evidence": [
    { "file": "hdfs-datanode-a.log", "line": 47,
      "snippet": "Got exception while serving blk_-..." }
  ],
  "anomaly_keys": ["blk_-..."],
  "root_cause_type": "datanode_unreachable",
  "recommended_action": "investigate"
}
```

Verifier assertions (`tests/test_state.py`): valid JSON, schema match,
referenced files exist, line numbers in range, snippets present
verbatim, evidence matches the task's validation mode, `root_cause_type`
is in the dataset's allowed taxonomy and matches the gold label, and
`recommended_action` is one of `{escalate, investigate, no_action,
open_incident, page_owner}`. HDFS/Hadoop/OpenStack use exact `(file,
line)` evidence locations; BGL/Thunderbird accept any cited line whose
visible inline alert tag maps to the expected root cause.

Full per-test breakdown: [docs/scoring.md](docs/scoring.md).

## Install

```bash
pip install harbor  # the test harness
git clone https://github.com/<owner>/loghub-benchmark
cd loghub-benchmark
make unit            # adapter + exporter tests (instant)
```

To run the benchmark itself you need Docker and the corpus on disk —
see [docs/data-setup.md](docs/data-setup.md).

## Run a task

```bash
harbor run -p tasks/hdfs-datanode-0b694b5 --agent oracle    # reward=1
harbor run -p tasks/hdfs-datanode-0b694b5 --agent nop       # reward=0
```

Run every gate the CI workflows run, locally:

```bash
make validate-all    # unit + static (12 checks × 160 tasks) + oracle/nop
```

Regenerate the committed curated set exactly from its manifest:

```bash
make rebuild-curated
```

## Run the rubric grader

`harbor check` requires `ANTHROPIC_API_KEY`. For cheaper graders, we
ship a Moonshot-backed alternative:

```bash
set -a; . .env; set +a    # MOONSHOT_API_KEY
.venv-tools/bin/python -m tools.rubric_check.moonshot_check \
    tasks/hdfs-datanode-0b694b5 \
    --model moonshot-v1-128k \
    --output-dir /tmp/m7-checks
```

Latest v1 60-task rubric pass report: [docs/rubric-pass-report.md](docs/rubric-pass-report.md)
(0 fails on both runs at ~$3 total spend). The 100 v2 tasks haven't been
rubric-graded yet; they're validated via oracle/nop gates + the per-task pytest
verifier assertions.

## Repo layout

```
loghub-benchmark/
├── tasks/                       # 160 curated tasks (60 v1 + 100 v2)
├── tools/
│   ├── case_builder/            # adapters + exporter + tests
│   └── rubric_check/            # Moonshot rubric grader
├── tests/
│   ├── test_repo_invariants.py  # repo gates: canary, leak, schema, snapshots
│   └── snapshots/case_ids.json  # determinism lock-in
├── ci_checks/                   # 15 static-check scripts (Bash)
│   └── test-tasks/              # negative fixtures (must FAIL each check)
├── rubrics/                     # Harbor rubric TOML files
└── .github/workflows/           # PR validation (static + oracle/nop + rubric)
```

For a fuller map of the repository and data flow, see
[docs/repo-map.md](docs/repo-map.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). New tasks come from adapter
additions or new corpora, not from hand-authoring single tasks —
read [docs/dataset-adapters.md](docs/dataset-adapters.md) for the
adapter contract.

## Citing

If you use the benchmark, please cite the underlying Loghub paper plus
the dataset-specific papers your task draws from:

> Jieming Zhu, Shilin He, Pinjia He, Jinyang Liu, Michael R. Lyu. *Loghub:
> A Large Collection of System Log Datasets for AI-driven Log Analytics*.
> IEEE International Symposium on Software Reliability Engineering (ISSRE), 2023.

HDFS_v1 tasks also cite:

> Wei Xu, Ling Huang, Armando Fox, David Patterson, Michael Jordan.
> *Detecting Large-Scale System Problems by Mining Console Logs*.
> SOSP 2009.

## License

The benchmark code is MIT-licensed; see `pyproject.toml`. The log slices
baked into each task image inherit Loghub's BSD license. Citation lives
in each task's `instruction.md` so the attribution travels with the
data.
