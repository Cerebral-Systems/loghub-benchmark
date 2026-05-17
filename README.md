# Loghub SRE Harbor benchmark

A Harbor-compatible benchmark for SRE log-investigation skills.
60 curated tasks built from the Loghub corpus (`logpai/loghub`).
Each task ships a Docker environment with 3–6 partitioned log files
totalling 5k–30k lines and asks the agent to **locate the anomaly**,
**cite verbatim evidence** as `(file, line, snippet)` tuples,
**classify the root cause** against a dataset-specific taxonomy, and
**recommend a safe SRE action**. The verifier writes a fractional reward (`passed_tests / non_skipped_tests`) to `/logs/verifier/reward.txt`, so partial-correct answers register on a continuous 0–1 scale.

## Status

Loghub-SRE is ready for community testing as a Harbor benchmark. The
committed 60-task set passes the substrate gates:

- `266` adapter/exporter/repo-invariant tests pass.
- `make static` passes all `12 × 60` static checks.
- `make oracle-nop` is green on all tasks: oracle scores `60/60`, nop
  scores `0/60`.

Real-agent leaderboard runs are intentionally not included yet; see
[docs/baselines.md](docs/baselines.md) for the current validation
baseline and remaining benchmarking caveats.

## What's in the box

| Dataset | Tasks | Anomaly source | Partition strategy |
|---|---|---|---|
| HDFS_v1 | 18 | 575k labelled blocks; heuristic root-cause from `Got exception while serving`, `BLOCK_NOT_FOUND`, replication patterns | by Component (NameNode / DataNode-a / DataNode-b / FSNamesystem) |
| Hadoop | 12 | Gold labels from `abnormal_label.txt` (machine_down / disk_full / network_disconnect) | by component (MRAppMaster / mapreduce / yarn) |
| BGL | 15 | Inline 0th-column alert tag (KERNDTLB, APPSEV, KERNSTOR, …) | by full node/location token |
| Thunderbird | 10 | Same inline format as BGL | by hostname role (compute / edge / domain / …) |
| OpenStack | 5 | 4 anomalous VM UUIDs from `anomaly_labels.txt` (rapid-destroy faults) | by OpenStack service (nova-api / nova-compute / nova-scheduler) |

Total: 60 tasks. Distribution and rationale: see [docs/dataset-adapters.md](docs/dataset-adapters.md).

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
make validate-all    # unit + static (12 checks × 60 tasks) + oracle/nop
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

Latest 60-task pass report: [docs/rubric-pass-report.md](docs/rubric-pass-report.md)
(0 fails on both runs at ~$3 total spend).

## Repo layout

```
loghub-benchmark/
├── tasks/                       # 60 curated tasks (committed)
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
