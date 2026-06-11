# Loghub SRE Harbor benchmark

A Harbor-compatible benchmark for SRE log-investigation skills.
**180 scored tasks** built from the Loghub corpus [(`logpai/loghub`)](https://github.com/logpai/loghub),
across **6 skill types × 5 datasets**: anomaly localization (v1, 60), false-positive
triage, temporal-sequence reconstruction, cross-component correlation, severity
classification (v2, 100), and outcome-oriented remediation (v3, 20). A 7th type,
log-template extraction, ships as a **20-task unscored tooling track**
([`tracks/tooling/`](tracks/tooling/)) — see [why](docs/data-provenance.md).

Tasks carry **opaque ids** (`lh-<hash>`) so the slug leaks no dataset or
root-cause hint; the human-readable mapping is in
[docs/task-id-map.json](docs/task-id-map.json).

Each task ships a Docker environment with partitioned log files and asks the
agent to investigate and emit a structured JSON answer (`/app/answer.json`). The
verifier grades it with **gate-aware scoring**: format/integrity checks are gates
(any failure → reward 0, passing earns no credit), and the fractional reward
(`passed / non_skipped` over the substantive tests) is written to
`/logs/verifier/reward.txt`. A schema-compliant no-investigation answer scores
**0.000**. Full layout and grading:
**[docs/structure-and-grading.md](docs/structure-and-grading.md)**.

Status: ready for community testing. The committed set passes every gate —
adapter/exporter/repo-invariant tests, `make static` (12 checks × 180 tasks),
and `make oracle-nop` (oracle 180/180, nop 0/180).

## Harness / model matrix

> **v1.0 re-baseline in progress.** The rows below were measured under the
> pre-v1.0 reward (`passed / non_skipped`, zero-effort floor 0.62). v1.0
> switches to gate-aware scoring (zero-effort floor **0.000** — schema
> compliance earns nothing) and diversified remediation actions, so these
> numbers are not comparable to v1.0 runs. The v1.0 table will report
> **fully-solved rate** as the headline metric, mean reward with 95% CIs over
> ≥3 runs, per-row cost, and a published zero-effort floor row.
> Leaderboard protocol: [docs/scoring.md](docs/scoring.md).

180-task runs (May 2026). "Errors" are Harbor trial exceptions counted as zero
reward. Committed run artifacts are linked. Harness: `harbor==0.13.1`.

| Harness | Model / agent | Tasks | Mean reward | Fully solved | Errors | Artifacts |
|---|---|---:|---:|---:|---:|---|
| Mesh Loghub profile | `deepseek/deepseek-v4-flash` | 180 | **0.915** | 66 (37%) | 0 | — |
| Mesh Loghub profile | `mimo-v2.5-pro` | 180 | 0.892 | 64 (36%) | 0 | — |
| Claude Code (API key) | `claude-opus-4-7` | 180 | 0.878 | 45 (25%) | 0 | [bundle](docs/leaderboard-artifacts/claude-api-opus-180-20260528T194734Z/) |
| Raw `mini-swe-agent` | `mimo-v2.5-pro` | 171/180 | 0.861 | 32 | 2 | — |
| Raw `mini-swe-agent` | `deepseek/deepseek-v4-flash` | 180 | 0.860 | 31 (17%) | 0 | — |
| Devin (API) | `devin` | 180 | 0.747 | 38 (21%) | 26 | [bundle](docs/leaderboard-artifacts/devin-api-merged-180-20260530/) |

Reproduce a baseline:

```bash
export DEEPSEEK_API_KEY=<your key>
harbor run -p tasks/ --agent mini-swe-agent -m deepseek/deepseek-v4-flash \
  --agent-timeout-multiplier 3.0 -o baselines
```

## What's in the box

| Dataset | Anomaly source | Partition strategy |
|---|---|---|
| HDFS_v1 | 575k labelled blocks; heuristic root-cause | by component (NameNode / DataNode-a/b / FSNamesystem) |
| Hadoop | gold `abnormal_label.txt` (machine_down / disk_full / network_disconnect) | by component (MRAppMaster / mapreduce / yarn) |
| BGL | inline alert tag (KERNDTLB, APPSEV, KERNSTOR, …), **stripped from the visible logs** so localization is content-based, not label-grep | by node/location token |
| Thunderbird | same inline format as BGL, alert tag **stripped**; slices are class-balanced (not 99% VAPI) | by hostname role (compute / edge / domain) |
| OpenStack | anomalous VM UUIDs from `anomaly_labels.txt` (single injected fault → root cause is constant, so it is **evidence-only scored**) | by service (nova-api / -compute / -scheduler) |

Scored set (180):

| Layer | Skill types | Tasks |
|---|---|---:|
| v1 | anomaly localization | 60 |
| v2 | false-positive triage (25), temporal sequence (28), cross-component correlation (32), severity (15) | 100 |
| v3 | remediation & recovery | 20 |

Plus an **unscored tooling track**: log-template extraction (20), in
[`tracks/tooling/`](tracks/tooling/) — kept out of the leaderboard because its
ground truth comes from the published Loghub-2k templates (contamination) and a
deterministic templater solves it (mechanizable). Distribution and rationale:
[docs/dataset-adapters.md](docs/dataset-adapters.md), [docs/data-provenance.md](docs/data-provenance.md).

## Install

```bash
git clone https://github.com/Cerebral-Systems/loghub-benchmark
cd loghub-benchmark
uv venv .venv-tools && . .venv-tools/bin/activate
pip install 'harbor==0.13.1' pytest pytest-json-ctrf   # pinned harness + verifier deps
make unit            # adapter + exporter + invariant tests (instant)
```

Running the benchmark needs Docker (and the corpus on disk only to *regenerate*
tasks — see [docs/data-setup.md](docs/data-setup.md)).

## Run

```bash
harbor run -p tasks/lh-f53d4948 --agent oracle    # reward=1
harbor run -p tasks/lh-f53d4948 --agent nop       # reward=0
make validate-all                                           # all CI gates locally
```

To re-render the per-task verifier/test files in place from the
`export_to_harbor` templates (no corpus needed; CI asserts they never drift):

```bash
python -m tools.case_builder.rebuild_tests          # write in place
python -m tools.case_builder.rebuild_tests --check  # drift gate
```

## Structure & grading

Task anatomy, answer schemas, the verifier/reward model, evidence-validation
modes, and the determinism/canary/anti-leak gates are documented in
**[docs/structure-and-grading.md](docs/structure-and-grading.md)** (exhaustive
per-assertion list in [docs/scoring.md](docs/scoring.md)).

```
tasks/lh-<hash>/        # opaque id — the slug encodes nothing about the answer
├── instruction.md     # what the agent sees
├── task.toml          # Harbor metadata
├── environment/       # Dockerfile + data/*.log  (agent-visible)
├── solution/          # solve.sh + derive_answer.py + oracle_hints.json  (oracle-only)
└── tests/             # test.sh + test_state.py + expected.json  (verifier-only)
```

## Repo layout

```
loghub-benchmark/
├── tasks/                       # 180 scored tasks, opaque lh-<hash> ids (60 v1 + 100 v2 + 20 remediation)
├── tracks/tooling/              # 20 unscored log-template-extraction tasks
├── tools/case_builder/          # adapters + exporter + rebuild_tests
├── tools/rubric_check/          # Moonshot rubric grader
├── tests/                       # repo invariants, gameability regressions, snapshots
├── ci_checks/                   # static-check scripts (+ negative fixtures)
├── rubrics/                     # Harbor rubric TOMLs
└── .github/workflows/           # PR validation (static + oracle/nop + rubric)
```

`docs/task-id-map.json` maps each opaque id back to its descriptive build slug.

Fuller map: [docs/repo-map.md](docs/repo-map.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). New tasks come from adapter additions or
new corpora, not hand-authored single tasks — read
[docs/dataset-adapters.md](docs/dataset-adapters.md) for the adapter contract.

## Data attribution

This benchmark redistributes small slices (10k–30k lines per task) of log data
from the [**LogPAI Loghub corpus**](https://github.com/logpai/loghub), used here
under its license for **research and academic work**. The Loghub corpus is not
BSD/MIT-licensed; it carries a custom research-use license that requires
citation and reference to the source repository for any redistribution. See
[Loghub's `LICENSE`](https://github.com/logpai/loghub/blob/master/LICENSE)
for the upstream terms.

The benchmark code (adapters, exporter, verifiers, tooling) in this repo is
MIT-licensed. The log slices baked into each task's `environment/data/`
directory are governed by the Loghub license, not MIT.

### Required citations

If you use Loghub-SRE in research or publish results from it, please cite the
Loghub corpus paper:

> Jieming Zhu, Shilin He, Pinjia He, Jinyang Liu, Michael R. Lyu. *Loghub:
> A Large Collection of System Log Datasets for AI-driven Log Analytics*.
> IEEE International Symposium on Software Reliability Engineering (ISSRE), 2023.
> arXiv:2008.06448

### Per-dataset upstream citations

Each dataset has its own original publication that LogPAI asks downstream users
to cite. Tasks in this benchmark inherit those obligations:

| Tasks using this data | Required upstream citation |
|---|---|
| `*hdfs-*` | Wei Xu, Ling Huang, Armando Fox, David Patterson, Michael Jordan. *Detecting Large-Scale System Problems by Mining Console Logs*. **SOSP 2009.** |
| `*hadoop-*` | Qingwei Lin, Hongyu Zhang, Jian-Guang Lou, Yu Zhang, Xuewei Chen. *Log Clustering Based Problem Identification for Online Service Systems*. **ICSE 2016.** |
| `*openstack-*` | Min Du, Feifei Li, Guineng Zheng, Vivek Srikumar. *DeepLog: Anomaly Detection and Diagnosis from System Logs through Deep Learning*. **CCS 2017.** |
| `*bgl-*` | Adam J. Oliner, Jon Stearley. *What Supercomputers Say: A Study of Five System Logs*. **DSN 2007.** (USENIX CFDR; BGL collected at LLNL.) |
| `*thunderbird-*` | Same Oliner & Stearley, DSN 2007. Thunderbird collected at Sandia (SNL); same USENIX CFDR distribution. |

The full canonical citation text is also reproduced in each task's
`instruction.md` so attribution travels with the data.

## License

- **Benchmark code** (adapters, exporter, verifiers, tooling, this README): MIT — see [`LICENSE`](LICENSE).
- **Log data under `tasks/*/environment/data/`**: governed by the [LogPAI Loghub license](https://github.com/logpai/loghub/blob/master/LICENSE) — free for research and academic work, citation required.
- **Per-dataset upstream**: each dataset's original publication carries its own license/citation requirements; see the table above.

Commercial uses other than research/evaluation (e.g., redistributing the raw log
corpus inside a paid product) require explicit permission from LogPAI and the
upstream dataset owners. Open-source benchmark use, internal R&D evaluation, and
published comparative results are within scope of the Loghub research-use license.
