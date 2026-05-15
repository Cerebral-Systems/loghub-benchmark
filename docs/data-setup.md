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

### Other datasets

Not yet downloaded. The corresponding adapters land in M2b-M2e. When
needed, fetch from `https://zenodo.org/records/8196385/` (HDFS_v1.zip,
Hadoop.zip, BGL.zip, Thunderbird.tar.gz, OpenStack.tar.gz) into
`/home/buildout/loghub-full/<dataset>/` and record sizes + SHA-256 here.

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
