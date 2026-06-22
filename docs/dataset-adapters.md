# Dataset adapters

Every adapter is a class in `tools/case_builder/adapters/` that turns a
Loghub corpus into JSON case specs. The same JSON spec then flows
through `tools/case_builder/export_to_harbor.py` to produce a Harbor-
shaped `tasks/<slug>/` directory. **Adapters never write task files —
only case JSON.** The exporter is the only thing that knows about
`task.toml`, partitioning, or the answer schema, so future schema
changes touch one file.

## Contract

Every adapter subclasses `AdapterBase` (`tools/case_builder/adapters/base.py`)
and defines:

```python
class FooAdapter(AdapterBase):
    dataset_name: str           # e.g. "HDFS_v1"
    adapter_version: str        # bump when the slice/classification
                                # logic changes in a way that should
                                # invalidate prior case_ids
    root_cause_taxonomy: tuple[str, ...]

    def load_labels(self, input_path: Path) -> LabelIndex: ...
    def iter_candidate_cases(
        self,
        input_path: Path,
        labels: LabelIndex,
        *,
        max_cases: int | None = None,
        seed: int = 0,
    ) -> Iterator[CandidateCase]: ...
    def select_slice(self, full_log: list[str],
                     anomaly_indices: list[int], seed: int) -> LogSlice: ...
    def classify_root_cause(self, log_slice: list[str],
                            anomaly_lines: list[int]) -> str: ...
```

`case_id` is computed by `AdapterBase` from a canonical join of
`(dataset_name, adapter_version, slice.offset, slice.length,
sorted(anomaly_lines))` — see `AdapterBase.case_id`. Don't override it.

## Determinism

`case_id` is a pure SHA-256 over its inputs. The substrate guarantees:

- Same corpus + same adapter code + same seed → same case_ids forever.
- `tests/test_case_ids_stable_from_fixture` locks this against
  `tests/snapshots/case_ids.json`.
- Bumping `adapter_version` is the documented way to invalidate prior
  case_ids. Do it any time you change the slice geometry, the
  root-cause classifier, or the label-loading logic in a way that
  shifts the inputs to `case_id()`. A version bump must be accompanied
  by regenerating the snapshot in the same commit.

## Slice strategy per dataset

| Dataset | Strategy | Window size |
|---|---|---|
| HDFS_v1 | Anchor on first mention of an anomalous block; bounded MIN..MAX window. v2 of the adapter caps the window — earlier versions expanded to cover a block's full lifetime, which exploded to 2M+ lines for long-lived blocks. | 10k–30k |
| Hadoop | Pair an anomalous job's container logs with a deterministically-chosen normal job's, separated by a `### normal_job=...` / `### anomalous_job=...` marker. The exporter drops those markers when partitioning (otherwise the file boundaries leak which half is anomalous). | concatenated per-job |
| BGL | Deterministic permutation of all non-`-` lines; sweep slices in order, dedup overlaps. Streamed in two passes (count → fill) so the 30 GB Thunderbird corpus stays under ~3 GB RSS. Exported files are bucketed by full node/location token to avoid one-file rack-only tasks. | 5k–15k |
| Thunderbird | Subclass of BGL — only `LOG_FILENAMES` + taxonomy are overridden. | 5k–15k |
| OpenStack | Per-instance variant scheme: each of the 4 anomalous VM UUIDs anchors K slice variants (default 3), so we yield ≥10 cases despite only 4 instances in the corpus. | 2k–8k |

## Taxonomy

Each adapter declares a `root_cause_taxonomy`. Document the mapping
explicitly in a sibling `<adapter>_taxonomy.md` file when the dataset
has a non-trivial code → slug mapping (see
[`tools/case_builder/adapters/bgl_taxonomy.md`](../tools/case_builder/adapters/bgl_taxonomy.md)
and
[`tools/case_builder/adapters/thunderbird_taxonomy.md`](../tools/case_builder/adapters/thunderbird_taxonomy.md)).

The exporter maps full-taxonomy slugs (with underscores) to short
single-token slug forms in `ROOT_CAUSE_SLUG` so the directory name
satisfies Harbor's three-hyphen-token slug constraint. The canonical
underscored form survives unchanged in `task.toml` `[metadata].tags`
and in `tests/expected.json` `root_cause_type`.

## Evidence validation

`expected.json` includes an `evidence_validation` mode. The committed
scored tasks use `exact_location`, where every cited `(file, line)` must
be present in the generated evidence set. BGL and Thunderbird still load
their raw upstream labels from the first log column, but the exporter
strips that visible tag from agent-visible logs before scoring, so
localization is based on the generated ground-truth coordinates rather
than label-grep.

## Adding a new dataset

1. Drop the corpus under the conventional `<host>/loghub-full/<DatasetName>/`
   layout (or anywhere — the case-builder accepts `--input`). Document
   checksums + source URL in `docs/data-setup.md`.
2. Add `tools/case_builder/adapters/<dataset>.py` implementing
   `AdapterBase`. Aim for ≤200 lines — most adapters are bookkeeping
   around 2–3 regexes and a label-file parser.
3. Add fixtures under `tools/case_builder/tests/fixtures/<dataset>/`
   and 3+ unit tests in `tools/case_builder/tests/test_<dataset>_adapter.py`.
   The fixture should be 10–30 lines + a tiny label file.
4. Register the adapter in `tools/case_builder/build_cases.py`'s
   `ADAPTERS` dict and the exporter's `DATASET_SLUG` /
   `DATASET_LOG_BASENAME` / `DATASET_DIFFICULTY` tables.
5. Add a per-dataset partition function to `_PARTITIONERS` in
   `tools/case_builder/export_to_harbor.py`. The function takes a log
   line and returns a basename for the file that line belongs in (or
   `None` to drop the line).
6. Run `make rebuild-curated` to reproduce the legacy v1 localization
   manifest into `.benchmark/rebuilt-curated-v1`. The committed public
   benchmark uses opaque `lh-<hash>` IDs, so `refresh-from-existing` reads
   `docs/task-id-map.json` when deriving the old descriptive slugs from
   current task directories.
7. Refresh `tests/snapshots/case_ids.json` to include the new
   adapter's fixture-derived ids.

The 5 existing adapters are the reference implementations. Hadoop is
the simplest (gold labels, no heuristics). Thunderbird is the smallest
(45 lines — a thin subclass of BGL). HDFS is the most pattern-heavy.
