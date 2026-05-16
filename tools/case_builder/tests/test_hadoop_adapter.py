"""Unit tests for the Hadoop adapter.

Hadoop's strongest gold signal is the per-job fault label in
abnormal_label.txt, so the tests focus on:
  1. Label parsing across the four heading formats Loghub uses.
  2. Slice concatenation pairs one normal + one anomalous job.
  3. Root cause flows straight from the label (no heuristics).
  4. case_id stability across runs.
"""

from __future__ import annotations

from pathlib import Path

from tools.case_builder.adapters.hadoop import (
    POSITIVE_TAXONOMY,
    HadoopAdapter,
)

FIXTURE = Path(__file__).parent / "fixtures" / "hadoop"


def test_load_labels_parses_all_four_categories():
    labels = HadoopAdapter().load_labels(FIXTURE)
    assert labels.entries == {
        "application_1_0001": "normal",
        "application_1_0002": "normal",
        "application_1_0003": "machine_down",
        "application_1_0004": "network_disconnect",
        "application_1_0005": "disk_full",
    }
    assert labels.positive_labels == frozenset(POSITIVE_TAXONOMY)
    assert set(labels.anomalous_keys()) == {
        "application_1_0003",
        "application_1_0004",
        "application_1_0005",
    }


def test_iter_candidate_cases_pairs_normal_and_anomalous_jobs():
    adapter = HadoopAdapter()
    labels = adapter.load_labels(FIXTURE)
    cases = list(adapter.iter_candidate_cases(FIXTURE, labels, seed=0))
    # One case per anomalous job.
    assert len(cases) == 3
    by_job = {c.anomaly_keys[0]: c for c in cases}
    assert set(by_job) == {"application_1_0003", "application_1_0004", "application_1_0005"}

    for case in cases:
        # The slice contains both the chosen normal and the anomalous job.
        joined = "\n".join(case.slice.lines)
        normal_job = case.extra["normal_job"]
        assert normal_job in joined
        assert case.anomaly_keys[0] in joined
        # Headers separate the two job streams.
        assert any(line.startswith("### normal_job=") for line in case.slice.lines)
        assert any(line.startswith("### anomalous_job=") for line in case.slice.lines)
        # Anomaly line numbers point only at the anomalous half.
        anomalous_lines = [case.slice.lines[ln - 1] for ln in case.anomaly_line_ids]
        assert all(case.anomaly_keys[0] in line or "ERROR" in line or "Job complete" not in line for line in anomalous_lines)
        # All anomaly line indices fall after the anomalous-job header.
        anom_header_idx = next(
            i for i, line in enumerate(case.slice.lines, start=1) if line.startswith("### anomalous_job=")
        )
        assert all(ln > anom_header_idx for ln in case.anomaly_line_ids)


def test_root_cause_flows_from_gold_label():
    adapter = HadoopAdapter()
    labels = adapter.load_labels(FIXTURE)
    by_job = {
        c.anomaly_keys[0]: c.root_cause
        for c in adapter.iter_candidate_cases(FIXTURE, labels, seed=0)
    }
    assert by_job["application_1_0003"] == "machine_down"
    assert by_job["application_1_0004"] == "network_disconnect"
    assert by_job["application_1_0005"] == "disk_full"


def test_case_id_stable_across_runs():
    adapter = HadoopAdapter()
    labels = adapter.load_labels(FIXTURE)
    run1 = {c.anomaly_keys[0]: c.case_id for c in adapter.iter_candidate_cases(FIXTURE, labels, seed=0)}
    run2 = {c.anomaly_keys[0]: c.case_id for c in adapter.iter_candidate_cases(FIXTURE, labels, seed=0)}
    assert run1 == run2
    # Different seed → different normal-job pairing → different slice → different ids.
    run3 = {c.anomaly_keys[0]: c.case_id for c in adapter.iter_candidate_cases(FIXTURE, labels, seed=7)}
    assert run3 != run1 or len(set(run1.values())) < len(run1)
