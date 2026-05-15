"""Unit tests for the OpenStack adapter.

OpenStack ships exactly 4 anomalous VM UUIDs in `anomaly_labels.txt` —
so M2e produces ≥10 cases by generating K variant slices per instance,
each anchored to the same instance but with a different seed-derived
window offset. The tests pin the variant scheme and the heuristic
root-cause taxonomy.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.case_builder.adapters import openstack as os_mod
from tools.case_builder.adapters.openstack import OpenStackAdapter

FIXTURE = Path(__file__).parent / "fixtures" / "openstack"


def test_load_labels_parses_uuid_list():
    labels = OpenStackAdapter().load_labels(FIXTURE)
    assert set(labels.entries) == {
        "11111111-1111-1111-1111-111111111111",
        "22222222-2222-2222-2222-222222222222",
    }
    assert labels.positive_labels == frozenset({"Anomaly"})


def test_load_labels_ignores_non_uuid_lines():
    """The published anomaly_labels.txt has a header sentence — make sure
    we don't misread it as a UUID."""
    labels = OpenStackAdapter().load_labels(FIXTURE)
    assert all(len(k) == 36 for k in labels.entries)


@pytest.mark.parametrize(
    "line,expected",
    [
        ("... [instance: a] destroy the instance on the hypervisor", "vm_task_failure"),
        ("... [instance: a] VM Stopped (Lifecycle Event)", "vm_task_failure"),
        ("... [instance: a] Deleting instance files /var/lib/nova/x", "vm_task_failure"),
        ("... [instance: a] WARNING imagecache: Unknown base file: /var/lib/nova/_base/x", "image_pull_failure"),
        ("... [instance: a] glance image fetch failed", "image_pull_failure"),
        ("... [instance: a] neutron port allocation failed", "network_error"),
        ("... [instance: a] Connection refused to 10.0.0.1", "network_error"),
        ("... [instance: a] Attempting claim: memory 2048 MB", "other"),
    ],
)
def test_classify_root_cause_matches_taxonomy(line: str, expected: str):
    result = OpenStackAdapter().classify_root_cause([line], [1])
    assert result == expected
    assert result in OpenStackAdapter.root_cause_taxonomy


def test_iter_candidate_cases_produces_variants_per_instance(monkeypatch):
    # Shrink slice bounds so 12-line abnormal log can host multiple windows.
    monkeypatch.setattr(os_mod, "MIN_SLICE_LINES", 4, raising=True)
    monkeypatch.setattr(os_mod, "MAX_SLICE_LINES", 8, raising=True)
    adapter = OpenStackAdapter()
    labels = adapter.load_labels(FIXTURE)
    cases = list(adapter.iter_candidate_cases(FIXTURE, labels, seed=0))
    # 2 instances * 3 variants = 6 cases (default VARIANTS_PER_INSTANCE).
    assert len(cases) == 2 * OpenStackAdapter.VARIANTS_PER_INSTANCE
    by_instance: dict[str, list] = {}
    for c in cases:
        by_instance.setdefault(c.anomaly_keys[0], []).append(c)
    assert set(by_instance) == set(labels.entries)
    for uuid, variants in by_instance.items():
        # variant ids 0..N-1
        assert sorted(v.extra["variant"] for v in variants) == list(
            range(OpenStackAdapter.VARIANTS_PER_INSTANCE)
        )
        # variant slice offsets/lengths should differ (different seeds).
        geometries = {(v.slice.offset, v.slice.length) for v in variants}
        assert len(geometries) > 1, f"all variants for {uuid} produced the same slice"


def test_classification_picks_up_real_anomalies(monkeypatch):
    monkeypatch.setattr(os_mod, "MIN_SLICE_LINES", 4, raising=True)
    monkeypatch.setattr(os_mod, "MAX_SLICE_LINES", 8, raising=True)
    adapter = OpenStackAdapter()
    labels = adapter.load_labels(FIXTURE)
    cases = list(adapter.iter_candidate_cases(FIXTURE, labels, seed=0))
    # Group cases by instance and check root-cause assignment.
    rc_by_instance: dict[str, set[str]] = {}
    for c in cases:
        rc_by_instance.setdefault(c.anomaly_keys[0], set()).add(c.root_cause)
    # Instance 1 has destroy + VM Stopped → vm_task_failure.
    assert "vm_task_failure" in rc_by_instance["11111111-1111-1111-1111-111111111111"]
    # Instance 2 has 'Unknown base file' (image_pull_failure) and 'VM Stopped'
    # (vm_task_failure); first-match wins per ROOT_CAUSE_PATTERNS order.
    inst2 = rc_by_instance["22222222-2222-2222-2222-222222222222"]
    assert inst2 & {"image_pull_failure", "vm_task_failure"}


def test_max_cases_bound_is_respected(monkeypatch):
    monkeypatch.setattr(os_mod, "MIN_SLICE_LINES", 4, raising=True)
    monkeypatch.setattr(os_mod, "MAX_SLICE_LINES", 8, raising=True)
    adapter = OpenStackAdapter()
    labels = adapter.load_labels(FIXTURE)
    cases = list(adapter.iter_candidate_cases(FIXTURE, labels, max_cases=3, seed=0))
    assert len(cases) == 3


def test_case_id_stable_across_runs(monkeypatch):
    monkeypatch.setattr(os_mod, "MIN_SLICE_LINES", 4, raising=True)
    monkeypatch.setattr(os_mod, "MAX_SLICE_LINES", 8, raising=True)
    adapter = OpenStackAdapter()
    labels = adapter.load_labels(FIXTURE)
    run1 = [c.case_id for c in adapter.iter_candidate_cases(FIXTURE, labels, seed=0)]
    run2 = [c.case_id for c in adapter.iter_candidate_cases(FIXTURE, labels, seed=0)]
    assert run1 == run2
    run3 = [c.case_id for c in adapter.iter_candidate_cases(FIXTURE, labels, seed=99)]
    assert run3 != run1
