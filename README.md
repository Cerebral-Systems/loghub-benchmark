# Loghub SRE Harbor benchmark

A Harbor-compatible benchmark for SRE log-investigation skills.
**180 curated tasks** built from the Loghub corpus [(`logpai/loghub`)](https://github.com/logpai/loghub).

It covers 7 distinct skill types: anomaly localization (v1, 60 tasks), 5 v2 skill
axes — false-positive triage, temporal sequence reconstruction, cross-component
correlation, severity classification, and log-template extraction (100 tasks)
— plus 20 outcome-oriented remediation tasks.

Each task ships a Docker environment with partitioned log files and asks the agent to investigate the
logs and produce a structured JSON answer that the verifier grades on
schema-specific assertions. Remediation tasks also include topology, service
state, config, and local mitigation tools; the verifier checks both diagnosis
and recovered post-mitigation state. The verifier writes a fractional reward
(`passed_tests / non_skipped_tests`) to `/logs/verifier/reward.txt`, so
partial-correct answers register on a continuous 0–1 scale.

## Status

Loghub-SRE is ready for community testing as a Harbor benchmark. The
committed 180-task set (60 v1 + 100 v2 + 20 remediation) passes the
substrate gates:

- adapter/exporter/repo-invariant tests pass.
- `make static` passes all `12 × 180` static checks.
- `make oracle-nop` is green on all tasks: oracle scores `180/180`, nop
  scores `0/180`.

Latest agent leaderboard entries are below. See
[docs/baselines.md](docs/baselines.md) for the substrate validation
baseline, [docs/HARDENING_REDO_REPORT.md](docs/HARDENING_REDO_REPORT.md)
for the outcome-task hardening report.

## Harness / Model Matrix

Latest 180-task hardened benchmark runs from May 28-30, 2026. Single run per row;
"Errors" are Harbor trial exceptions. Rows marked "pre-boundary" used the
Loghub-specific Mesh profile and tools, but the adapter still performed
structured benchmark finalization. The strict-boundary harness, where the
adapter only copies `decision.reasoning.evidence_pack.domain_decision.answer`,
has passed smoke tests but still needs a full 180-task rerun.

| Harness | Model / agent | Run ID | Status | Mean reward | Fully solved | Errors | Notes |
|---|---|---|---:|---:|---:|---:|---|
| Mesh Loghub profile, pre-boundary full run | `deepseek/deepseek-v4-flash` | `mesh-runtime-c0ec8e8-deepseek-latest-180-20260528T054018Z` | 180/180 | **0.895** | 66 (37%) | 0 | Latest completed Mesh+DeepSeek full run |
| Mesh Loghub profile, pre-boundary full run | `openai/mimo-v2.5-pro` | `mesh-runtime-c0ec8e8-mimo-envmimo-latest-180-20260528T054915Z` | 180/180 | **0.892** | 64 (36%) | 0 | Latest completed Mesh+Mimo full run |
| Claude Code API-key (`claude-code` 2.1.154) | `claude-opus-4-7` | `claude-api-opus-180-20260528T194734Z` | 180/180 | 0.878 | 45 (25%) | 0 | Clean API-key Opus baseline; no subscription session cap. Proof: `docs/leaderboard-artifacts/` |
| Raw Harbor + `mini-swe-agent` | `deepseek/deepseek-v4-flash` | `bench-deepseek-v4-flash-latest-180-20260528T054018Z` | 180/180 | 0.860 | 31 (17%) | 0 | Clean raw DeepSeek baseline |
| Raw Harbor + `mini-swe-agent` | `openai/mimo-v2.5-pro` | `bench-mimo-v2.5-pro-envmimo-latest-180-20260528T054915Z` | 171/180 completed; 2 running; 7 pending | 0.861 | 32 so far | 2 | Correct `.env.mimo`; still in progress |
| Devin API, single-session | Devin | `devin-api-merged-180-20260530` | 180/180 merged | 0.747 | 38 (21%) | 26 | Merged from a 20-task partial and 160-task continuation; quota/API/timeouts counted as zero. Adapter and artifacts: [`docs/leaderboard-artifacts/devin-api-merged-180-20260530`](docs/leaderboard-artifacts/devin-api-merged-180-20260530/) |

Completed full-run deltas:

| Comparison | Baseline mean | Harness mean | Delta | Full-credit delta |
|---|---:|---:|---:|---:|
| Mesh Loghub profile + DeepSeek vs raw DeepSeek | 0.860 | **0.895** | **+0.035** | +35 |
| Mesh Loghub profile + Mimo vs raw Mimo | raw Mimo still running | **0.892** | n/a | n/a |

Quick Harbor command:

```bash
harbor run -p loghub-benchmark/tasks --agent mini-swe-agent --model <provider/model>
```

Strict-boundary smoke runs:

| Task family | Run ID | Reward | Boundary audit |
|---|---|---:|---|
| Localization | `mesh-domain-decision-boundary-smoke-20260528T100814Z` | 0.917 | `mesh_domain_decision_copy`; no semantic repair |
| Correlation | `mesh-domain-decision-boundary-3task-20260528T100913Z` | 0.727 | `mesh_domain_decision_copy`; no semantic repair |
| Template extraction | `mesh-domain-decision-boundary-tmpl-20260528T101037Z` | 0.875 | `mesh_domain_decision_copy`; no semantic repair |
| Remediation | `mesh-domain-decision-boundary-rem-20260528T101037Z` | 0.727 | Mesh mitigation applied; adapter validator surfaced one citation mismatch |

The strict-boundary adapter intentionally refuses to synthesize semantic
fields. It requires Mesh to emit the benchmark answer in
`decision.reasoning.evidence_pack.domain_decision.answer`; the adapter only
validates, copies, and records provenance. Future Mesh leaderboard rows should
come from a full 180-task strict-boundary rerun.

Historical 160-task reference:

| Model | Harness | Tasks | Mean reward | Fully solved | Crashes | Mean latency/task | Runtime | Cost | Date |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `deepseek/deepseek-v4-flash` | `mini-swe-agent` | 160 | 0.850 | 28 (18%) | 0 | 2.6 min | 1h 44m | <$1 | 2026-05-22 |

Per-skill-type, latest completed DeepSeek full runs:

| Skill | n | Mesh + DeepSeek | Raw DeepSeek | Delta |
|---|---:|---:|---:|---:|
| `bgl` v1 localization subset | 15 | 0.978 | 0.872 | +0.106 |
| `corr` cross-component correlation | 20 | 0.818 | 0.818 | +0.000 |
| `fp` false-positive triage | 25 | 0.906 | 0.866 | +0.040 |
| `hadoop` v1 localization subset | 12 | 0.821 | 0.776 | +0.045 |
| `hdfs` v1 localization subset | 18 | 0.774 | 0.748 | +0.026 |
| `openstack` v1 localization subset | 5 | 0.785 | 0.738 | +0.046 |
| `rem` outcome remediation | 20 | 0.982 | 0.905 | +0.077 |
| `seq` temporal sequence | 20 | 0.875 | 0.888 | -0.013 |
| `sev` severity classification | 15 | 0.922 | 0.878 | +0.044 |
| `thunderbird` v1 localization subset | 10 | 1.000 | 0.892 | +0.108 |
| `tmpl` log template extraction | 20 | 0.938 | 0.963 | -0.025 |

Mesh improves the raw DeepSeek baseline overall in the latest completed full
run, with most of the lift coming from remediation, severity,
false-positive triage, and v1 localization. Raw DeepSeek remains slightly
stronger on template extraction, and correlation remains a hard shared failure
mode.

**Top failure modes** in the latest DeepSeek + `mini-swe-agent` 180-task run
(152 tasks had at least one failed assertion):

| Failed assertion | Tasks affected | Skill area |
|---|---|---|
| `test_root_cause_matches_ground_truth` | 56 | Wrong taxonomy bucket |
| `test_no_cross_file_line_confusion` | 34 | Cited line N of file A but text is at line N of file B |
| `test_evidence_within_ground_truth` | 34 | Over-cited evidence outside truth set |
| `test_minimum_evidence_count` | 28 | Too little cited support |
| `test_causal_chain_recall` | 25 | Missing ground-truth events in causal chain |
| `test_trigger_role_correct` | 20 | Wrong trigger in temporal sequence |

Actionable: DeepSeek finds anomaly *locations* reasonably well but still
mis-classifies *root causes* most often. Claude Code Opus under the host-auth
adapter hit 111 trial errors in this run, so that row should be read as a
harness/CLI integration result, not a model ceiling.

> Verifier rigor history:
> - **Original** (no fixes): overall mean 0.880, `fp` mean 1.000, `corr` mean 0.815
> - **After Gap 1** (fp verifier — ground-truth set + classification match): overall 0.859, fp 0.865
> - **After Gap 6** (corr verifier — `caused_by_step` topology match): overall **0.850**, corr 0.745
> Both fixes tightened the verifier without breaking oracle (still passes 11/11 on fp tasks). The 0.850 is the historical 160-task headline; the hardened 180-task leaderboard above supersedes it for current comparisons.

Reproducing this run:

```bash
export DEEPSEEK_API_KEY=<your key>
harbor run -p tasks/ --agent mini-swe-agent -m deepseek/deepseek-v4-flash \
  --agent-timeout-multiplier 3.0 --job-name bench-deepseek-v4-flash-latest-180 -o baselines
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

v3 adds an outcome-oriented remediation family:

| Skill type | Slug prefix | Count | What it tests |
|---|---|---:|---|
| Remediation and recovery | `rem-*` | 20 | Root component diagnosis, mitigation choice, local action execution, and recovered health state |

Total: **180 tasks** across **7 skill types** × 5 datasets. See
[docs/HARDENING_REDO_REPORT.md](docs/HARDENING_REDO_REPORT.md) for v3
remediation hardening.

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
git clone https://github.com/hydrogenbond007/loghub-benchmark
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
make validate-all    # unit + static (12 checks × 180 tasks) + oracle/nop
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
rubric-graded yet; neither have the 20 remediation tasks. They are validated
via oracle/nop gates + the per-task pytest verifier assertions.

## Repo layout

```
loghub-benchmark/
├── tasks/                       # 180 curated tasks (60 v1 + 100 v2 + 20 remediation)
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

## Data attribution

This benchmark redistributes small slices (10k–30k lines per task) of log data
from the [**LogPAI Loghub corpus**](https://github.com/logpai/loghub), used here
under its license for **research and academic work**. The Loghub corpus is not
BSD/MIT-licensed; it carries a custom research-use license that requires
citation and reference to the source repository for any redistribution. See
[Loghub's `LICENSE`](https://github.com/logpai/loghub/blob/master/LICENSE)
for the upstream terms.

The benchmark code (adapters, exporter, verifiers, tooling) in this repo is
MIT-licensed via `pyproject.toml`. The log slices baked into each task's
`environment/data/` directory are governed by the Loghub license, not MIT.

### Required citations

If you use Loghub-SRE in research or publish results from it, please cite
the Loghub corpus paper:

> Jieming Zhu, Shilin He, Pinjia He, Jinyang Liu, Michael R. Lyu. *Loghub:
> A Large Collection of System Log Datasets for AI-driven Log Analytics*.
> IEEE International Symposium on Software Reliability Engineering (ISSRE), 2023.
> arXiv:2008.06448

### Per-dataset upstream citations

Each dataset has its own original publication that LogPAI asks downstream
users to cite. Tasks in this benchmark inherit those obligations:

| Tasks using this data | Required upstream citation |
|---|---|
| `hdfs-*`, `corr-hdfs-*`, `seq-hdfs-*`, `sev-hdfs-*`, `tmpl-hdfs-*`, `fp-hdfs-*` | Wei Xu, Ling Huang, Armando Fox, David Patterson, Michael Jordan. *Detecting Large-Scale System Problems by Mining Console Logs*. **SOSP 2009.** |
| `hadoop-*`, `corr-hadoop-*`, `seq-hadoop-*`, `sev-hadoop-*`, `tmpl-hadoop-*`, `fp-hadoop-*` | Qingwei Lin, Hongyu Zhang, Jian-Guang Lou, Yu Zhang, Xuewei Chen. *Log Clustering Based Problem Identification for Online Service Systems*. **ICSE 2016.** |
| `openstack-*`, `corr-openstack-*`, `seq-openstack-*`, `sev-openstack-*`, `tmpl-openstack-*`, `fp-openstack-*` | Min Du, Feifei Li, Guineng Zheng, Vivek Srikumar. *DeepLog: Anomaly Detection and Diagnosis from System Logs through Deep Learning*. **CCS 2017.** |
| `bgl-*`, `corr-bgl-*`, `seq-bgl-*`, `sev-bgl-*`, `tmpl-bgl-*`, `fp-bgl-*` | Adam J. Oliner, Jon Stearley. *What Supercomputers Say: A Study of Five System Logs*. **DSN 2007.** Originally distributed via [USENIX CFDR](https://www.usenix.org/cfdr-data) (Computer Failure Data Repository); BGL logs collected at Lawrence Livermore National Lab (LLNL). |
| `thunderbird-*`, `corr-thunderbird-*`, `seq-thunderbird-*`, `sev-thunderbird-*`, `tmpl-thunderbird-*`, `fp-thunderbird-*` | Same Oliner & Stearley, DSN 2007 paper. Thunderbird logs collected at Sandia National Labs (SNL). Same USENIX CFDR distribution. |

The full canonical citation text is also reproduced in each task's
`instruction.md` so attribution travels with the data when individual tasks
are extracted or shared.

## License

- **Benchmark code** (adapters, exporter, verifiers, tooling, this README): MIT — see `pyproject.toml`.
- **Log data redistributed under `tasks/*/environment/data/`**: governed by the LogPAI Loghub license — see `https://github.com/logpai/loghub/blob/master/LICENSE`. Free for research and academic work, citation required.
- **Per-dataset upstream**: each underlying dataset's original publication carries its own license/citation requirements; see the table above.

Commercial uses other than research/evaluation (e.g., redistributing the raw
log corpus inside a paid product) require explicit permission from LogPAI and
the upstream dataset owners. Open-source benchmark use, internal R&D evaluation,
and published comparative results are unambiguously within scope of the Loghub
research-use license.
