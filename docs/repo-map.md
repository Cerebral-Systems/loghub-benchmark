# Repository Map

This repository has two layers:

1. The committed Harbor benchmark under `tasks/`.
2. The generator and validation tooling under `tools/`, `tests/`, and
   `ci_checks/`.

The full Loghub corpora are not committed. Each task commits only the
log slice it needs; the case-builder reads the raw corpora off disk
from a path configured by `--input`.

## Core Paths

| Path | Role | Required for running tasks? |
|---|---|---|
| `tasks/` | The 180 scored Harbor tasks, opaque `lh-<hash>` ids (60 v1 + 100 v2: fp 25 / seq 28 / corr 32 / sev 15 + 20 v3 remediation). | Yes |
| `tracks/tooling/` | 20 unscored log-template-extraction tasks (contaminated GT + mechanizable; kept off the leaderboard). | Optional |
| `docs/task-id-map.json` | Maps each opaque `lh-<hash>` id back to its descriptive build slug. | Reference |
| `tools/case_builder/` | Adapters, exporter, curated rebuild, and the in-place test re-render (`rebuild_tests.py`). | Needed for regeneration |
| `tools/case_builder/curated_selection.json` | Exact manifest for the committed task set. | Needed for reproducible rebuilds |
| `tools/rubric_check/` | Moonshot-backed rubric checker. | Optional quality review |
| `tools/stress_pack_generator/` | Large non-curated stress pack generator. | Optional stress testing |
| `ci_checks/` | Static checks plus negative fixtures. | Needed for CI/static validation |
| `tests/` | Repo invariants, gameability regressions (`test_gameability.py`), the offline verifier harness (`verifier_harness.py`), and case-id + ground-truth snapshots (`snapshots/`). | Needed for CI/unit validation |
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

| Adapter | Dataset | Label source | v1 tasks |
|---|---|---|---|
| `hdfs.py` | HDFS_v1 | `preprocessed/anomaly_label.csv` | 18 |
| `hadoop.py` | Hadoop | `abnormal_label.txt` | 12 |
| `bgl.py` | BGL | Inline first-column alert tag | 15 |
| `thunderbird.py` | Thunderbird | Inline first-column alert tag | 10 |
| `openstack.py` | OpenStack | `anomaly_labels.txt` | 5 |

`build_cases.py` runs adapters and writes candidate JSON. The curated
manifest records the case IDs that make up the public benchmark. The
v2 (fp/seq/corr/sev/tmpl) and v3 (rem) task families are derived from
the same adapter slices by additional exporter dispatch paths
(`_export_fp_case`, `_export_seq_case`, `_export_corr_case`,
`_export_sev_case`, `_export_tmpl_case`, `_export_rem_case`).

## Verification Model

Every task writes `/app/answer.json` with a schema specific to its
skill type:

| Skill | Schema version |
|---|---|
| v1 anomaly localization | `loghub-sre-answer-v2` |
| `fp` false-positive triage | `loghub-sre-answer-v2-fp` |
| `seq` temporal sequence | `loghub-sre-answer-v2-seq` |
| `corr` cross-component correlation | `loghub-sre-answer-v2-corr` |
| `sev` severity classification | `loghub-sre-answer-v2-sev` |
| `rem` outcome remediation | `loghub-sre-answer-v3-remediation` |
| `tmpl` log template extraction *(unscored, `tracks/tooling/`)* | `loghub-sre-answer-v2-tmpl` |

Each schema has its own `tests/test_state.py` assertion set. v1 and
the v2 incident-shaped families share the evidence-validation pattern
described in `docs/scoring.md`; `tmpl` validates template-grouping
recall against ground-truth `EventTemplate`s; `rem` grades recovery by
**replaying** the agent's declared mitigation against a verifier-only
`tests/initial_state.json` (the agent-writable `/app/service_state.json`
is not trusted). The committed scored tasks use exact `(file, line)` evidence
checks; BGL and Thunderbird load upstream inline labels but strip the visible
tag before agents see the exported logs.

## Regeneration

Rebuild the v1 curated tasks from the corpus manifest (needs `LOGHUB_CORPUS`
and the corpus on disk; non-destructive to the v2/v3 families):

```bash
export LOGHUB_CORPUS=/path/to/loghub-full
make rebuild-curated
```

Re-render the per-task verifier/test files in place from the templates
(no corpus needed; CI asserts they never drift):

```bash
python -m tools.case_builder.rebuild_tests          # write in place
python -m tools.case_builder.rebuild_tests --check   # drift gate
```

Run the validation gates:

```bash
make unit
make static
make oracle-nop
```

`make validate-all` runs all three.
