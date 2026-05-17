# Repository Map

This repository has two layers:

1. The committed Harbor benchmark under `tasks/`.
2. The generator and validation tooling under `tools/`, `tests/`, and
   `ci_checks/`.

The full Loghub corpora are not committed. They live on the build
machine under `/home/buildout/loghub-full/`; each task commits only the
log slice it needs.

## Core Paths

| Path | Role | Required for running tasks? |
|---|---|---|
| `tasks/` | The 60 published Harbor tasks. | Yes |
| `tools/case_builder/` | Adapters, exporter, curated rebuild tool. | Needed for regeneration |
| `tools/case_builder/curated_selection.json` | Exact manifest for the committed 60-task set. | Needed for reproducible rebuilds |
| `tools/rubric_check/` | Moonshot-backed rubric checker. | Optional quality review |
| `tools/stress_pack_generator/` | Large non-curated stress pack generator. | Optional stress testing |
| `ci_checks/` | Static checks plus negative fixtures. | Needed for CI/static validation |
| `tests/` | Repo invariant tests and case-id snapshots. | Needed for CI/unit validation |
| `rubrics/` | Harbor rubric definitions. | Needed for rubric review |
| `.github/workflows/` | CI and manual trial workflows. | Needed for GitHub validation |
| `docs/` | Public documentation. | No, but important for users |

## Task Directory Shape

Every published task uses this Harbor layout:

```text
tasks/<slug>/
├── instruction.md
├── task.toml
├── environment/
│   ├── Dockerfile
│   └── data/*.log
├── solution/
│   ├── solve.sh
│   ├── derive_answer.py
│   └── oracle_hints.json
└── tests/
    ├── expected.json
    ├── test.sh
    └── test_state.py
```

Agent-visible files are mounted under `/app`. Normal agents see the
instruction and log files; they do not see `solution/` or `tests/`.

## Data Flow

```text
raw Loghub corpus
  -> adapter in tools/case_builder/adapters/
  -> candidate case JSON
  -> tools/case_builder/curated_selection.json
  -> tools/case_builder/export_to_harbor.py
  -> tasks/<slug>/
  -> harbor run
  -> tests/test_state.py
  -> /logs/verifier/reward.txt
```

## Adapter Layer

Each dataset adapter reads one corpus format and emits `CandidateCase`
objects. Adapters never write Harbor task directories directly.

| Adapter | Dataset | Label source | Published tasks |
|---|---|---|---|
| `hdfs.py` | HDFS_v1 | `preprocessed/anomaly_label.csv` | 18 |
| `hadoop.py` | Hadoop | `abnormal_label.txt` | 12 |
| `bgl.py` | BGL | Inline first-column alert tag | 15 |
| `thunderbird.py` | Thunderbird | Inline first-column alert tag | 10 |
| `openstack.py` | OpenStack | `anomaly_labels.txt` | 5 |

`build_cases.py` runs adapters and writes candidate JSON. The curated
manifest records the case IDs that make up the public benchmark.

## Verification Model

The agent must write `/app/answer.json` with schema
`loghub-sre-answer-v2`. The verifier checks:

- valid JSON and schema version
- evidence file names are real task log basenames
- cited line numbers are in range
- snippets appear verbatim on cited lines
- evidence matches the validation mode
- root cause matches ground truth
- recommended action is from the safe action set

HDFS, Hadoop, and OpenStack use exact `(file, line)` evidence checks.
BGL and Thunderbird use inline-label validation so large slices stay
reviewable while evidence still has to map to the expected root cause.

## Regeneration

Rebuild the committed 60-task set exactly:

```bash
make rebuild-curated
```

Run the validation gates:

```bash
make unit
make static
make oracle-nop
```

`make validate-all` runs all three.
