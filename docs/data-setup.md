# Data setup

The Loghub raw corpus is large (~80 GB across all datasets) and is not
committed to this repo. The case-builder (`tools/case_builder/`) reads
the dataset directly off disk; the per-task Docker images bake only the
specific slices each task needs.

## Layout on this VM

| Path | Purpose |
|---|---|
| `/opt/mesh-benchmarks/external/loghub/` | Read-only clone of `logpai/loghub` with the published 2k samples (~13 MB). Useful for quick inspection. |
| `/home/buildout/loghub-full/<dataset>/` | Full corpora extracted from Zenodo. Writable, ~480 GB free. |
| `tools/case_builder/tests/fixtures/` | Tiny synthetic fixtures committed for unit tests. Do not touch the real corpus from tests. |

We intentionally do **not** use `/opt/mesh-benchmarks/external/loghub-full/`
because `/opt/mesh-benchmarks/` is root-owned on this VM and the autonomous
build agent does not have passwordless `sudo`. If a future setup grants
write access there, the case-builder accepts any path via `--input` so
the only thing to update is this document.

## Datasets currently on disk

### HDFS_v1

| File | Size | SHA-256 |
|---|---|---|
| `/home/buildout/loghub-full/HDFS/HDFS.log` | 1.47 GiB (11,175,629 lines) | `0783096174d7832c618337f9609e06e04abd86ddd7089b3c12b407e63bfebc52` |
| `/home/buildout/loghub-full/HDFS/preprocessed/anomaly_label.csv` | 17.8 MiB (575,061 rows) | `1c711ed6c8848fc3243fb4d092f172f31d128c8a6ec7f26ebba72ab931885ed8` |
| `/home/buildout/loghub-full/HDFS/HDFS_v1.zip` | 178.0 MiB | recorded in `HDFS_v1.zip.sha256` |

Source: <https://zenodo.org/records/8196385/files/HDFS_v1.zip?download=1>
(linked from the `logpai/loghub` README under "HDFS_v1").

To re-download from scratch:

```bash
DEST=/home/buildout/loghub-full/HDFS
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
| `/home/buildout/loghub-full/Hadoop/Hadoop.zip` | 48.61 MiB | `79e63c6521e90ae164754a29d13e04e0c6c5e782490a7fe1e2b124f4f5737ced` |
| `/home/buildout/loghub-full/Hadoop/abnormal_label.txt` | 2.2 KiB (55 jobs) | `b23800ec91f89ea403d18b6d6bce94d30b57092dbcfa523582357929c2be9414` |
| `/home/buildout/loghub-full/Hadoop/application_*/container_*.log` | 52 MiB extracted | per-file; not pinned |

Source: <https://zenodo.org/records/8196385/files/Hadoop.zip?download=1>.

Distribution after extraction: 55 application directories (11 normal /
44 anomalous: 26 machine_down, 11 disk_full, 7 network_disconnect across
WordCount + PageRank workloads). The Hadoop adapter pairs each anomalous
job with a deterministically-chosen normal job (seed-mixed) into one
concatenated slice.

### BGL

| File | Size | SHA-256 |
|---|---|---|
| `/home/buildout/loghub-full/BGL/BGL.log` | 743 MiB (4,747,963 lines) | `666130b15ef44eb32fd02bd053e6c6e007c37696b5e7e8b9d8e45b729876a5d2` |
| `/home/buildout/loghub-full/BGL/BGL.zip` | 55 MiB | `d67fd82a711aea0157a9b83175892c6ee60e384a2ddf5bc51f39118453816da8` |

Source: <https://zenodo.org/records/8196385/files/BGL.zip?download=1>.

BGL has no separate label file; the 0th whitespace-delimited column is
the alert tag (`-` for normal, otherwise codes like `KERNDTLB`,
`APPSEV`, `KERNSTOR`). 348,460 of 4.75M lines are non-`-`. The top-10
alert categories used by the adapter are documented in
[`tools/case_builder/adapters/bgl_taxonomy.md`](../tools/case_builder/adapters/bgl_taxonomy.md);
anything outside that list collapses to `other_alert`.

### Other datasets

Not yet downloaded. The remaining adapters land in M2d-M2e. When needed,
fetch from `https://zenodo.org/records/8196385/` (Thunderbird.tar.gz,
OpenStack.tar.gz) into `/home/buildout/loghub-full/<dataset>/` and record
sizes + SHA-256 here.

## License

Loghub is BSD-licensed; Loghub-2.0 is CC-BY-4.0. Per both licenses we
may redistribute slices baked into Docker images provided we retain the
upstream citation. The standard citation is recorded in each generated
task's `instruction.md` (added by the M3 exporter):

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
  seeds produce different slices. The autonomous build keeps `--seed 0`
  for the committed task set; stress packs can vary seed for breadth.
