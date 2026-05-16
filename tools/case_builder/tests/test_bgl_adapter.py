"""Unit tests for the BGL adapter.

BGL has inline labels (the 0th column is `-` or a short alert tag), so
the adapter has no separate label file to parse. The tests cover:
  1. LabelIndex captures every non-`-` line.
  2. Slice selection produces a window containing the anchor anomaly.
  3. Root cause maps the dominant alert tag through the taxonomy.
  4. case_id stable across runs at the same seed.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.case_builder.adapters import bgl as bgl_mod
from tools.case_builder.adapters.bgl import BGLAdapter

FIXTURES = Path(__file__).parent / "fixtures"


def test_load_labels_captures_non_normal_lines():
    labels = BGLAdapter().load_labels(FIXTURES)
    # Fixture has 15 lines total; non-`-` rows are at 0-based indices 2,5,7,8,11,13.
    assert set(labels.entries) == {"2", "5", "7", "8", "11", "13"}
    assert labels.entries["2"] == "KERNDTLB"
    assert labels.entries["7"] == "APPSEV"
    assert labels.entries["11"] == "KERNSTOR"
    assert labels.entries["13"] == "LINKIAP"
    # positive_labels is whatever non-`-` tags actually appear in the log.
    assert labels.positive_labels == frozenset({"KERNDTLB", "APPSEV", "KERNSTOR", "LINKIAP"})


@pytest.mark.parametrize(
    "tag_line,expected",
    [
        ("KERNDTLB 1 2 3 RAS KERNEL FATAL data TLB", "kerndtlb"),
        ("APPSEV 1 2 3 RAS APP FATAL severe error", "appsev"),
        ("KERNSTOR 1 2 3 RAS KERNEL FATAL storage", "kernstor"),
        ("LINKIAP 1 2 3 RAS LINK WARN link issue", "other_alert"),
        ("- 1 2 3 RAS KERNEL INFO normal", "other_alert"),
    ],
)
def test_classify_root_cause_maps_tag(tag_line: str, expected: str):
    result = BGLAdapter().classify_root_cause([tag_line], [1])
    assert result == expected
    assert result in BGLAdapter.root_cause_taxonomy


def test_classify_root_cause_breaks_ties_by_taxonomy_priority():
    # APPSEV (rank 3) beats LINKIAP (other_alert) when tied on count.
    lines = [
        "APPSEV 1 2 3 RAS APP FATAL ...",
        "LINKIAP 1 2 3 RAS LINK WARN ...",
    ]
    assert BGLAdapter().classify_root_cause(lines, [1, 2]) == "appsev"


def test_select_slice_pads_window_around_anchor(monkeypatch):
    monkeypatch.setattr(bgl_mod, "MIN_SLICE_LINES", 5, raising=True)
    monkeypatch.setattr(bgl_mod, "MAX_SLICE_LINES", 8, raising=True)
    adapter = BGLAdapter()
    log = (FIXTURES / "BGL.log").read_text().splitlines()

    a = adapter.select_slice(log, [7], seed=123)
    b = adapter.select_slice(log, [7], seed=123)
    assert a == b
    assert a.offset <= 7 < a.offset + a.length
    assert 5 <= a.length <= 8


def test_iter_candidate_cases_dedupes_overlapping_anomalies(monkeypatch):
    monkeypatch.setattr(bgl_mod, "MIN_SLICE_LINES", 8, raising=True)
    monkeypatch.setattr(bgl_mod, "MAX_SLICE_LINES", 12, raising=True)
    adapter = BGLAdapter()
    labels = adapter.load_labels(FIXTURES)
    cases = list(adapter.iter_candidate_cases(FIXTURES, labels, seed=0))
    assert cases, "expected at least one case from the fixture"
    # A 12-line window on a 15-line log will sweep up most anomalies in one case.
    swept = set()
    for c in cases:
        for line_no in c.anomaly_line_ids:
            swept.add(c.slice.offset + line_no - 1)
    # Every fixture anomaly should be covered by exactly one case.
    expected_anomalies = {int(k) for k in labels.entries}
    assert swept == expected_anomalies
    for c in cases:
        assert c.root_cause in BGLAdapter.root_cause_taxonomy


def test_case_id_stable_across_runs(monkeypatch):
    monkeypatch.setattr(bgl_mod, "MIN_SLICE_LINES", 8, raising=True)
    monkeypatch.setattr(bgl_mod, "MAX_SLICE_LINES", 12, raising=True)
    adapter = BGLAdapter()
    labels = adapter.load_labels(FIXTURES)
    run1 = [c.case_id for c in adapter.iter_candidate_cases(FIXTURES, labels, seed=0)]
    run2 = [c.case_id for c in adapter.iter_candidate_cases(FIXTURES, labels, seed=0)]
    assert run1 == run2
    run3 = [c.case_id for c in adapter.iter_candidate_cases(FIXTURES, labels, seed=99)]
    # Different seed → different order/slice → different ids (at least partially).
    assert run3 != run1 or len(run1) <= 1
