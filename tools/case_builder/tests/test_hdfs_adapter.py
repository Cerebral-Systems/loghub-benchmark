"""Unit tests for the HDFS_v1 adapter.

Covers the four guarantees the adapter contract makes about every adapter:
  1. Labels load with the right vocabulary.
  2. Root-cause classification maps known patterns to the documented taxonomy.
  3. Slice selection produces a deterministic window around the anomaly.
  4. case_id is a pure function of (dataset, adapter version, slice, anomaly lines).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.case_builder.adapters import hdfs as hdfs_mod
from tools.case_builder.adapters.hdfs import HDFSAdapter

FIXTURES = Path(__file__).parent / "fixtures"


# --- 1. label loading --------------------------------------------------------


def test_load_labels_parses_csv_and_marks_anomalies():
    adapter = HDFSAdapter()
    labels = adapter.load_labels(FIXTURES)
    assert labels.entries["blk_1"] == "Normal"
    assert labels.entries["blk_2"] == "Anomaly"
    assert labels.positive_labels == frozenset({"Anomaly"})
    assert set(labels.anomalous_keys()) == {"blk_2", "blk_3", "blk_4", "blk_6"}


def test_load_labels_rejects_wrong_columns(tmp_path: Path):
    bad = tmp_path / "anomaly_label.csv"
    bad.write_text("foo,bar\nblk_1,X\n")
    with pytest.raises(ValueError, match="BlockId,Label"):
        HDFSAdapter().load_labels(tmp_path)


# --- 2. root-cause classification -------------------------------------------


@pytest.mark.parametrize(
    "line,expected",
    [
        ("081109 1 1 INFO x: Failed to add block blk_99 to datanode", "replication_failure"),
        ("081109 1 1 INFO x: Adding lost block blk_99 to under replication queue", "replication_failure"),
        ("081109 1 1 ERROR x: BLOCK_NOT_FOUND blk_99", "data_corruption"),
        ("081109 1 1 WARN x: writeBlock blk_99 received exception", "datanode_unreachable"),
        ("081109 1 1 WARN x: Got exception while serving blk_99 to /1.2.3.4", "datanode_unreachable"),
        ("081109 1 1 WARN x: SocketTimeoutException reading blk_99", "timeout"),
        ("081109 1 1 INFO x: nothing interesting here", "other"),
    ],
)
def test_classify_root_cause_taxonomy(line: str, expected: str):
    adapter = HDFSAdapter()
    result = adapter.classify_root_cause([line], [1])
    assert result == expected
    assert result in adapter.root_cause_taxonomy


# --- 3. slice selection ------------------------------------------------------


def test_select_slice_is_deterministic_for_fixed_inputs(monkeypatch):
    # With min slice 10k-30k the tiny fixture log triggers the "all anomalies
    # must fit" path. Shrink the window for the test so we exercise normal
    # padding logic on a 25-line log.
    monkeypatch.setattr(hdfs_mod, "MIN_SLICE_LINES", 5, raising=True)
    monkeypatch.setattr(hdfs_mod, "MAX_SLICE_LINES", 10, raising=True)
    adapter = HDFSAdapter()
    log = (FIXTURES / "HDFS.log").read_text().splitlines()

    a = adapter.select_slice(log, [6, 7], seed=42)
    b = adapter.select_slice(log, [6, 7], seed=42)
    assert a == b
    assert 5 <= a.length <= 10
    # Anomaly indices must lie inside the slice.
    assert a.offset <= 6 < a.offset + a.length
    assert a.offset <= 7 < a.offset + a.length

    # Different seed → likely different offset/length, but still valid.
    c = adapter.select_slice(log, [6, 7], seed=99)
    assert c.offset <= 6 < c.offset + c.length


def test_iter_candidate_cases_yields_one_per_anomalous_block(monkeypatch):
    monkeypatch.setattr(hdfs_mod, "MIN_SLICE_LINES", 5, raising=True)
    monkeypatch.setattr(hdfs_mod, "MAX_SLICE_LINES", 10, raising=True)
    adapter = HDFSAdapter()
    labels = adapter.load_labels(FIXTURES)
    cases = list(adapter.iter_candidate_cases(FIXTURES, labels, max_cases=10, seed=0))
    # Four anomalous blocks in the fixture (blk_2, blk_3, blk_4, blk_6).
    assert len(cases) == 4
    by_block = {c.anomaly_keys[0]: c for c in cases}
    assert set(by_block) == {"blk_2", "blk_3", "blk_4", "blk_6"}
    # Each case has at least one anomaly line within its slice.
    for c in cases:
        assert c.anomaly_line_ids
        assert all(1 <= ln <= c.slice.length for ln in c.anomaly_line_ids)
    # Root cause should be from the documented taxonomy.
    for c in cases:
        assert c.root_cause in adapter.root_cause_taxonomy
    # Spot-check: blk_3 has 'Failed to add block' + 'Adding lost block' → replication_failure.
    assert by_block["blk_3"].root_cause == "replication_failure"
    # blk_4 has 'BLOCK_NOT_FOUND' → data_corruption.
    assert by_block["blk_4"].root_cause == "data_corruption"


# --- 4. case_id stability ----------------------------------------------------


def test_case_id_stable_across_runs(monkeypatch):
    monkeypatch.setattr(hdfs_mod, "MIN_SLICE_LINES", 5, raising=True)
    monkeypatch.setattr(hdfs_mod, "MAX_SLICE_LINES", 10, raising=True)
    adapter = HDFSAdapter()
    labels = adapter.load_labels(FIXTURES)
    run1 = {c.anomaly_keys[0]: c.case_id for c in adapter.iter_candidate_cases(FIXTURES, labels, seed=0)}
    run2 = {c.anomaly_keys[0]: c.case_id for c in adapter.iter_candidate_cases(FIXTURES, labels, seed=0)}
    assert run1 == run2

    # Same data, different seed → different ids (because slice offsets shift).
    run3 = {c.anomaly_keys[0]: c.case_id for c in adapter.iter_candidate_cases(FIXTURES, labels, seed=99)}
    # At least one block's case_id must change — otherwise the seed is dead.
    assert run3 != run1
