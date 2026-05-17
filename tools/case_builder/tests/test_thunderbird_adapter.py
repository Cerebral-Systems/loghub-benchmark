"""Unit tests for the Thunderbird adapter.

Thunderbird inherits BGL's inline-tag slicing logic verbatim — these
tests focus on the filename override (`Thunderbird.log` instead of
`BGL.log`) and the distinct alert vocabulary.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.case_builder.adapters import bgl as bgl_mod
from tools.case_builder.adapters.bgl import BGLAdapter
from tools.case_builder.adapters.thunderbird import ThunderbirdAdapter

FIXTURES = Path(__file__).parent / "fixtures"


def test_thunderbird_is_a_bgl_subclass():
    """Inheritance is structural — if this breaks, the rest of the
    adapter contract is at risk of diverging silently."""
    assert issubclass(ThunderbirdAdapter, BGLAdapter)
    assert ThunderbirdAdapter.dataset_name == "Thunderbird"
    assert ThunderbirdAdapter().LOG_FILENAMES[0] == "Thunderbird.log"


def test_locate_log_finds_thunderbird_log():
    log = ThunderbirdAdapter()._locate_log(FIXTURES)
    assert log.name == "Thunderbird.log"


def test_taxonomy_differs_from_bgl():
    """Confirm we didn't accidentally inherit BGL's alert vocabulary."""
    t = set(ThunderbirdAdapter.root_cause_taxonomy)
    b = set(BGLAdapter.root_cause_taxonomy)
    overlap = t & b
    # Only the catch-all should overlap.
    assert overlap == {"other_alert"}


def test_load_labels_picks_up_thunderbird_tags():
    labels = ThunderbirdAdapter().load_labels(FIXTURES)
    # Fixture indices (0-based): VAPI at 2, 4; ECC at 6; CPU at 8;
    # NETWORK at 10; SOMETHING_RARE at 12.
    assert set(labels.entries) == {"2", "4", "6", "8", "10", "12"}
    assert labels.entries["2"] == "VAPI"
    assert labels.entries["12"] == "SOMETHING_RARE"
    assert labels.positive_labels == frozenset(
        {"VAPI", "ECC", "CPU", "NETWORK", "SOMETHING_RARE"}
    )


@pytest.mark.parametrize(
    "tag_line,expected",
    [
        ("VAPI 1 2 3 hw vapi: link down", "vapi"),
        ("ECC 1 2 3 hw ecc: single-bit error", "ecc"),
        ("CPU 1 2 3 hw cpu: thermal", "cpu"),
        ("PBS_CON 1 2 3 sched pbs: connect failed", "pbs_con"),
        ("MPT 1 2 3 hw mpt: fusion event", "mpt"),
        ("EXT_FS 1 2 3 fs ext: filesystem error", "ext_fs"),
        ("NMI 1 2 3 hw nmi: non-maskable", "nmi"),
        ("SOMETHING_RARE 1 2 3 misc rare: weird", "other_alert"),
        ("- 1 2 3 src routine event", "other_alert"),
    ],
)
def test_classify_root_cause_uses_thunderbird_taxonomy(tag_line: str, expected: str):
    result = ThunderbirdAdapter().classify_root_cause([tag_line], [1])
    assert result == expected
    assert result in ThunderbirdAdapter.root_cause_taxonomy


def test_iter_candidate_cases_yields_thunderbird_cases(monkeypatch):
    # Fixture is 15 lines; shrink the slice window so we get more than
    # one case.
    monkeypatch.setattr(bgl_mod, "MIN_SLICE_LINES", 4, raising=True)
    monkeypatch.setattr(bgl_mod, "MAX_SLICE_LINES", 6, raising=True)
    adapter = ThunderbirdAdapter()
    labels = adapter.load_labels(FIXTURES)
    cases = list(adapter.iter_candidate_cases(FIXTURES, labels, seed=0))
    assert cases
    # Every anomaly index in the fixture must be covered by exactly one case.
    swept = set()
    for c in cases:
        for line_no in c.anomaly_line_ids:
            swept.add(c.slice.offset + line_no - 1)
    assert swept == {int(k) for k in labels.entries}
    for c in cases:
        assert c.root_cause in ThunderbirdAdapter.root_cause_taxonomy
        assert c.dataset_name == "Thunderbird"


def test_case_id_stable_across_runs(monkeypatch):
    monkeypatch.setattr(bgl_mod, "MIN_SLICE_LINES", 4, raising=True)
    monkeypatch.setattr(bgl_mod, "MAX_SLICE_LINES", 6, raising=True)
    adapter = ThunderbirdAdapter()
    labels = adapter.load_labels(FIXTURES)
    run1 = [c.case_id for c in adapter.iter_candidate_cases(FIXTURES, labels, seed=0)]
    run2 = [c.case_id for c in adapter.iter_candidate_cases(FIXTURES, labels, seed=0)]
    assert run1 == run2
    run3 = [c.case_id for c in adapter.iter_candidate_cases(FIXTURES, labels, seed=99)]
    assert run3 != run1 or len(run1) <= 1
