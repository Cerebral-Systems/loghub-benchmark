"""Unit tests for tools.analysis modules.

Builds a minimal Harbor-shaped run dir under tmp_path, runs each tool,
and asserts the aggregation + classification logic.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.analysis import diff_oracle_agent as doa
from tools.analysis import failure_modes as fm
from tools.analysis import summarize_runs as sr


def _write_trial(
    run_dir: Path,
    slug: str,
    tid: str,
    reward: float,
    *,
    passed: int = 0,
    total: int = 1,
    failures: list[tuple[str, str]] | None = None,
) -> Path:
    """Materialize a Harbor trial dir; `failures` is list of (test_name, trace)."""
    trial = run_dir / f"{slug}__{tid}"
    (trial / "verifier").mkdir(parents=True)
    (trial / "verifier" / "reward.txt").write_text(f"{reward}\n")
    ctrf_tests = []
    for name, trace in failures or []:
        ctrf_tests.append(
            {
                "name": f"test_state.py::{name}",
                "status": "failed",
                "trace": trace,
            }
        )
    for _ in range(passed):
        ctrf_tests.append({"name": "test_state.py::ok", "status": "passed"})
    ctrf = {"results": {"summary": {"passed": passed, "tests": total}, "tests": ctrf_tests}}
    (trial / "verifier" / "ctrf.json").write_text(json.dumps(ctrf))
    return trial


# --- summarize_runs ---------------------------------------------------------


def test_summarize_runs_aggregates_by_task_and_eval(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    _write_trial(run_dir, "hdfs-datanode-aaaa111", "t1", 1.0)
    _write_trial(run_dir, "hdfs-datanode-aaaa111", "t2", 0.5)
    _write_trial(run_dir, "rem-hdfs-other-bbbb222", "t1", 0.0)
    # Top-level result.json links trial_id -> eval_name.
    (run_dir / "result.json").write_text(
        json.dumps(
            {
                "stats": {
                    "evals": {
                        "oracle__adhoc": {
                            "reward_stats": {
                                "reward": {
                                    "1.0": ["hdfs-datanode-aaaa111__t1"],
                                    "0.5": ["hdfs-datanode-aaaa111__t2"],
                                    "0.0": ["rem-hdfs-other-bbbb222__t1"],
                                }
                            }
                        }
                    }
                }
            }
        )
    )

    trials = sr._collect_run_dir(run_dir)
    assert len(trials) == 3
    rows = sr.aggregate(trials)
    by_slug = {r["task_slug"]: r for r in rows}
    assert by_slug["hdfs-datanode-aaaa111"]["mean_reward"] == 0.75
    assert by_slug["hdfs-datanode-aaaa111"]["pass_at_1"] == 1.0
    assert by_slug["rem-hdfs-other-bbbb222"]["pass_at_1"] == 0.0


def test_summarize_runs_handles_missing_top_result(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    _write_trial(run_dir, "fp-hadoop-noise-xx", "0", 0.25)
    trials = sr._collect_run_dir(run_dir)
    assert len(trials) == 1
    assert trials[0].eval_name == "unknown"


# --- failure_modes ----------------------------------------------------------


def test_failure_modes_classifies_known_traces(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    _write_trial(
        run_dir, "rem-hdfs-other-xx", "0", 0.0,
        failures=[
            ("test_post_mitigation_state", "check_health reports degraded, expected healthy"),
            ("test_mitigation_target_matches", "mitigation.action mismatch: got 'mark_noop'"),
            ("test_causal_chain_recall", "causal chain missing edges: [('a','b')]"),
            ("test_evidence_real", "references unknown file 'fake.log'"),
            ("test_random_other", "well that was unexpected"),
        ],
    )
    rows = fm.scan(run_dir)
    by_bucket = {r.bucket for r in rows}
    assert "bad_post_state" in by_bucket
    assert "wrong_mitigation" in by_bucket
    assert "missing_chain_edge" in by_bucket
    assert "hallucinated_evidence" in by_bucket
    assert "other" in by_bucket
    hist = fm.histogram(rows)
    assert hist["bad_post_state"]["count"] == 1


# --- diff_oracle_agent ------------------------------------------------------


def test_diff_oracle_agent_matches_remediation_fields() -> None:
    expected = {
        "schema_version": "loghub-sre-answer-v3-remediation",
        "root_component": "hdfs-namenode",
        "root_cause_type": "datanode_unreachable",
        "mitigation": {"action": "restart_component", "target": "hdfs-namenode"},
        "expected_health": "healthy",
        "causal_chain": [
            {"step": 0, "component": "hdfs-namenode.log", "evidence_line": 1, "role": "root"},
            {"step": 1, "component": "hdfs-datanode-a.log", "evidence_line": 1,
             "role": "downstream", "caused_by_step": 0},
        ],
    }
    answer = {
        "schema_version": "loghub-sre-answer-v3-remediation",
        "root_component": "hdfs-namenode",
        "root_cause_type": "datanode_unreachable",
        "mitigation": {"action": "restart_component", "target": "hdfs-namenode"},
        "postcheck": {"health_status": "healthy"},
        "causal_chain": [
            {"step": 0, "component": "hdfs-namenode.log", "evidence": {"file": "x", "line": 1, "snippet": ""}},
            {"step": 1, "component": "hdfs-datanode-a.log", "evidence": {"file": "x", "line": 1, "snippet": ""}},
        ],
    }
    diff = doa.diff_answer_to_expected(answer, expected)
    summary = diff["summary"]
    assert summary["mismatches"] == 0
    assert diff["fields"]["mitigation.action"]["match"] is True
    assert diff["fields"]["postcheck.health_status"]["match"] is True
    assert diff["fields"]["causal_chain_components"]["recall"] == 1.0


def test_diff_oracle_agent_flags_mismatch_in_mitigation() -> None:
    expected = {
        "schema_version": "loghub-sre-answer-v3-remediation",
        "root_component": "x",
        "mitigation": {"action": "restart_component", "target": "x"},
        "expected_health": "healthy",
    }
    answer = {
        "schema_version": "loghub-sre-answer-v3-remediation",
        "root_component": "x",
        "mitigation": {"action": "mark_noop", "target": "x"},
        "postcheck": {"health_status": "degraded"},
    }
    diff = doa.diff_answer_to_expected(answer, expected)
    assert diff["fields"]["mitigation.action"]["match"] is False
    assert diff["fields"]["postcheck.health_status"]["match"] is False
