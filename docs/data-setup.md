# Data setup

The Loghub raw corpus is large (~80 GB across all datasets) and is not
committed to this repo. The case-builder (`tools/case_builder/`) reads
the dataset directly off disk; the per-task Docker images bake only the
specific slices each task needs.

## Expected layout

The case-builder accepts any corpus location via the `--input` flag; the
paths below are the conventions this repo's tooling and existing docs
use, but nothing in the code is hard-coded to them.

| Path | Purpose |
|---|---|
| `<corpus-root>/loghub/` | Read-only clone of `logpai/loghub` with the published 2k samples (~13 MB). Useful for quick inspection and for the `tmpl` adapter (which reads `<dataset>_2k.log_structured.csv`). |
| `<corpus-root>/loghub-full/<dataset>/` | Full corpora extracted from Zenodo. Roughly 80 GB total across all five datasets. |
| `tools/case_builder/tests/fixtures/` | Tiny synthetic fixtures committed for unit tests. Do not touch the real corpus from tests. |

## Datasets currently on disk

### HDFS_v1

| File | Size | SHA-256 |
|---|---|---|
| `$LOGHUB_DATA_DIR/HDFS/HDFS.log` | 1.47 GiB (11,175,629 lines) | `0783096174d7832c618337f9609e06e04abd86ddd7089b3c12b407e63bfebc52` |
| `$LOGHUB_DATA_DIR/HDFS/preprocessed/anomaly_label.csv` | 17.8 MiB (575,061 rows) | `1c711ed6c8848fc3243fb4d092f172f31d128c8a6ec7f26ebba72ab931885ed8` |
| `$LOGHUB_DATA_DIR/HDFS/HDFS_v1.zip` | 178.0 MiB | recorded in `HDFS_v1.zip.sha256` |

Source: <https://zenodo.org/records/8196385/files/HDFS_v1.zip?download=1>
(linked from the `logpai/loghub` README under "HDFS_v1").

To re-download from scratch:

```bash
DEST="${LOGHUB_DATA_DIR:-$HOME/loghub-full}/HDFS"
mkdir -p "$DEST" && cd "$DEST"
curl -sSL --retry 3 -o HDFS_v1.zip \
  'https://zenodo.org/records/8196385/files/HDFS_v1.zip?download=1'
sha256sum HDFS_v1.zip > HDFS_v1.zip.sha256
unzip -o HDFS_v1.zip
```

The zip contains the raw `HDFS.log` plus a `preprocessed/` directory with
`anomaly_label.csv` (BlockId,Label), event traces, occurrence matrix,
templates, and an HDFS.npz. The case-builder only reads `HDFS.log` and
`preprocessed/anomaly_label.csv`.

### Hadoop

| File | Size | SHA-256 |
|---|---|---|
| `$LOGHUB_DATA_DIR/Hadoop/Hadoop.zip` | 48.61 MiB | `79e63c6521e90ae164754a29d13e04e0c6c5e782490a7fe1e2b124f4f5737ced` |
| `$LOGHUB_DATA_DIR/Hadoop/abnormal_label.txt` | 2.2 KiB (55 jobs) | `b23800ec91f89ea403d18b6d6bce94d30b57092dbcfa523582357929c2be9414` |
| `$LOGHUB_DATA_DIR/Hadoop/application_*/container_*.log` | 52 MiB extracted | per-file; not pinned |

Source: <https://zenodo.org/records/8196385/files/Hadoop.zip?download=1>.

Distribution after extraction: 55 application directories (11 normal /
44 anomalous: 26 machine_down, 11 disk_full, 7 network_disconnect across
WordCount + PageRank workloads). The Hadoop adapter pairs each anomalous
job with a deterministically-chosen normal job (seed-mixed) into one
concatenated slice.

### BGL

| File | Size | SHA-256 |
|---|---|---|
| `$LOGHUB_DATA_DIR/BGL/BGL.log` | 743 MiB (4,747,963 lines) | `666130b15ef44eb32fd02bd053e6c6e007c37696b5e7e8b9d8e45b729876a5d2` |
| `$LOGHUB_DATA_DIR/BGL/BGL.zip` | 55 MiB | `d67fd82a711aea0157a9b83175892c6ee60e384a2ddf5bc51f39118453816da8` |

Source: <https://zenodo.org/records/8196385/files/BGL.zip?download=1>.

BGL has no separate label file; the 0th whitespace-delimited column is
the alert tag (`-` for normal, otherwise codes like `KERNDTLB`,
`APPSEV`, `KERNSTOR`). 348,460 of 4.75M lines are non-`-`. The top-10
alert categories used by the adapter are documented in
[`tools/case_builder/adapters/bgl_taxonomy.md`](../tools/case_builder/adapters/bgl_taxonomy.md);
anything outside that list collapses to `other_alert`.

### Thunderbird

| File | Size | SHA-256 |
|---|---|---|
| `$LOGHUB_DATA_DIR/Thunderbird/Thunderbird.log` | 29.6 GiB (211,212,192 lines) | `3e8659d6efdf048bca6d682d376c74cf742a43cac66cb2a514241a103284f289` |
| `$LOGHUB_DATA_DIR/Thunderbird/Thunderbird.tar.gz` | 1.9 GiB | `228f8589b7cd569b727c5da654c647aa538dd3dd95541e675a40523c5fff37cf` |

Source: <https://zenodo.org/records/8196385/files/Thunderbird.tar.gz?download=1>.

Like BGL, alerts are inline (0th-column tag). Vocabulary is closed — only
10 distinct alert codes appear across the corpus, dominated by VAPI
(3.23M of 3.25M anomalies = ~99.6%). See
[`tools/case_builder/adapters/thunderbird_taxonomy.md`](../tools/case_builder/adapters/thunderbird_taxonomy.md).
The adapter subclasses `BGLAdapter` and overrides only the taxonomy
and the log filename.

Because Thunderbird.log is 30 GB, the adapter family (BGL + Thunderbird)
streams the log: one pass to count lines + load tag positions, a second
pass to fill per-slice buffers. RSS stays under ~3 GB during whole-corpus
runs.

### OpenStack

| File | Size | SHA-256 |
|---|---|---|
| `$LOGHUB_DATA_DIR/OpenStack/openstack_normal1.log` | 14.8 MiB (52,312 lines) | `4e4d47347bdae198056bb3b0a8a755e1cb0100d6c6a30bbd4058684234769199` |
| `$LOGHUB_DATA_DIR/OpenStack/openstack_abnormal.log` | 5.2 MiB (18,434 lines) | `7ab718fbb2f2b804893955cecf37ad9533cfa0efaf5b03009474d5bb019b6af4` |
| `$LOGHUB_DATA_DIR/OpenStack/openstack_normal2.log` | 38.6 MiB (137,074 lines) | `3c51741dcea1fb0731d1f86588b12587707e7abea01e725ee16c9441b8b68db7` |
| `$LOGHUB_DATA_DIR/OpenStack/anomaly_labels.txt` | 243 B (4 UUIDs) | `0882aa484f285e3dda476ff39ed739603c446f27b76bb113e284cda6ebb09d0b` |
| `$LOGHUB_DATA_DIR/OpenStack/OpenStack.tar.gz` | 5.1 MiB | `87c98c5ed03262e05cdb7a6f3717033df76d88fda0f7d2db23bd9fa4200f1879` |

Source: <https://zenodo.org/records/8196385/files/OpenStack.tar.gz?download=1>.

The OpenStack corpus has only **4 anomalous VM UUIDs** by design — the
faults are injected per-instance in `openstack_abnormal.log`. To reach
the ≥10 candidate-case threshold from 4 instances, `OpenStackAdapter`
generates `VARIANTS_PER_INSTANCE` slice variants (default 3) per UUID
by mixing the seed with the variant index, yielding 12 cases at
`--max-cases 12 --seed 0`. The published anomaly type is uniform across
all 4 instances (rapid VM destruction after creation), so the heuristic
classifier returns `vm_task_failure` for every variant; the
`network_error` / `image_pull_failure` slugs in the taxonomy are kept
for future corpora.

## License

The Loghub corpus is **not** BSD/MIT-licensed; it carries a custom
research-use license that requires citation and reference to the source
repository for any redistribution. See
[Loghub's `LICENSE`](https://github.com/logpai/loghub/blob/master/LICENSE)
for the upstream terms. The slices this repo redistributes under
`tasks/*/environment/data/` are governed by that license; see the
top-level `README.md` "Data attribution" section and the per-dataset
citation table for the full picture. The standard citation is also
recorded in each generated task's `instruction.md`:

> Jieming Zhu, Shilin He, Pinjia He, Jinyang Liu, Michael R. Lyu. *Loghub:
> A Large Collection of System Log Datasets for AI-driven Log Analytics*.
> IEEE International Symposium on Software Reliability Engineering (ISSRE),
> 2023.

Plus the dataset-specific citation when one exists (e.g. Xu et al. 2009
for HDFS_v1).

## Determinism

Every case_id is `sha256(dataset_name|adapter_version|slice.offset|slice.length|anomaly_lines)`.
That makes case_ids stable as long as those inputs don't change:

- Same `HDFS.log` + same `anomaly_label.csv` + same adapter code → same case_ids.
- A bump to `HDFSAdapter.adapter_version` (in `tools/case_builder/adapters/hdfs.py`)
  is the documented way to invalidate all prior case_ids; do this any
  time you change the slice or classification logic.
- The `--seed` flag is mixed into per-block window selection so different
  seeds produce different slices. The committed task set uses `--seed 0`;
  stress packs can vary seed for breadth.
