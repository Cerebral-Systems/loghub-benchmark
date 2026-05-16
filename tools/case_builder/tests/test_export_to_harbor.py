"""Unit tests for the Harbor task exporter.

The exporter is the M3 surface the rest of the project depends on, so
the tests pin both the directory shape (Harbor's static checks read
specific files) and the answer schema (the verifier asserts against it).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools.case_builder import export_to_harbor as ex


def _make_case(**overrides) -> dict:
    case: dict = {
        "case_id": "abcdef1234567890" + "0" * 48,
        "dataset_name": "HDFS_v1",
        "adapter_version": "1",
        "slice": {
            "lines": [
                "081109 1 1 INFO line one",
                "081109 1 2 INFO line two anomaly token here",
                "081109 1 3 INFO line three",
                "081109 1 4 INFO Got exception while serving blk_42",
            ],
            "offset": 0,
            "length": 4,
        },
        "anomaly_line_ids": [2, 4],
        "root_cause": "datanode_unreachable",
        "anomaly_keys": ["blk_42"],
        "extra": {},
    }
    case.update(overrides)
    return case


# --- slug --------------------------------------------------------------------


def test_make_slug_is_three_token_lowercase_hyphen():
    case = _make_case()
    slug = ex.make_slug(case)
    assert slug == "hdfs-datanode-abcdef1"
    parts = slug.split("-")
    assert len(parts) == 3
    assert all(p == p.lower() for p in parts)


def test_make_slug_handles_underscore_root_causes():
    """Root causes like vm_task_failure must collapse to a single
    underscore-free token to satisfy Harbor's slug regex."""
    case = _make_case(
        dataset_name="OpenStack", root_cause="vm_task_failure", case_id="ffeeddccbbaa9988" + "1" * 48
    )
    slug = ex.make_slug(case)
    assert slug == "openstack-vmtask-ffeeddc"
    assert "_" not in slug


def test_make_slug_is_stable_across_runs():
    case = _make_case()
    assert ex.make_slug(case) == ex.make_slug(case)


# --- export_case structure ---------------------------------------------------


def test_export_case_writes_expected_layout(tmp_path: Path):
    out = tmp_path / "tasks"
    ex.export_case(
        _make_case(), out, author_name="Author X", author_email="x@example.com"
    )
    task_dir = out / "hdfs-datanode-abcdef1"
    for relative in (
        "instruction.md",
        "task.toml",
        "environment/Dockerfile",
        "environment/data/hdfs.log",
        "solution/solve.sh",
        "solution/derive_answer.py",
        "solution/oracle_hints.json",
        "tests/test.sh",
        "tests/test_state.py",
        "tests/expected.json",
    ):
        assert (task_dir / relative).is_file(), f"missing {relative}"
    assert (task_dir / "solution" / "solve.sh").stat().st_mode & 0o111, "solve.sh not executable"
    assert (task_dir / "tests" / "test.sh").stat().st_mode & 0o111, "test.sh not executable"


def test_task_toml_uses_new_schema(tmp_path: Path):
    out = tmp_path / "tasks"
    ex.export_case(_make_case(), out, author_name="Author X", author_email="x@example.com")
    toml_text = (out / "hdfs-datanode-abcdef1" / "task.toml").read_text()
    assert 'version = "1.0"' in toml_text
    assert "schema_version" not in toml_text
    assert '[task]' in toml_text
    assert 'name = "loghub-sre/hdfs-datanode-abcdef1"' in toml_text
    assert 'difficulty = "medium"' in toml_text  # HDFS default
    assert 'category = "sre-log-investigation"' in toml_text
    # Old-schema fields must NOT appear.
    for forbidden in ("difficulty_explanation", "solution_explanation", "verification_explanation", "expert_time_estimate_hours"):
        assert forbidden not in toml_text, f"old-schema field {forbidden} leaked into task.toml"


def test_canary_present_in_every_emitted_text_file(tmp_path: Path):
    out = tmp_path / "tasks"
    ex.export_case(_make_case(), out, author_name="x", author_email="x@example.com")
    task_dir = out / "hdfs-datanode-abcdef1"
    text_files = [
        task_dir / "instruction.md",
        task_dir / "task.toml",
        task_dir / "environment" / "Dockerfile",
        task_dir / "solution" / "solve.sh",
        task_dir / "solution" / "derive_answer.py",
        task_dir / "tests" / "test.sh",
        task_dir / "tests" / "test_state.py",
    ]
    for f in text_files:
        assert ex.CANARY_GUID in f.read_text(), f"canary missing from {f}"


def test_expected_json_holds_ground_truth(tmp_path: Path):
    out = tmp_path / "tasks"
    ex.export_case(_make_case(), out, author_name="x", author_email="x@example.com")
    expected = json.loads((out / "hdfs-datanode-abcdef1" / "tests" / "expected.json").read_text())
    assert expected["schema_version"] == "loghub-sre-answer-v1"
    assert expected["anomaly_line_ids"] == [2, 4]
    assert expected["root_cause_type"] == "datanode_unreachable"
    assert "datanode_unreachable" in expected["allowed_root_causes"]
    assert "investigate" in expected["safe_recommendations"]


def test_oracle_hints_carry_only_what_solve_needs(tmp_path: Path):
    out = tmp_path / "tasks"
    ex.export_case(_make_case(), out, author_name="x", author_email="x@example.com")
    hints = json.loads((out / "hdfs-datanode-abcdef1" / "solution" / "oracle_hints.json").read_text())
    # Hints are smaller than expected.json — they intentionally do not
    # ship the allowed_root_causes list or the safe_recommendations.
    assert set(hints) == {"anomaly_line_ids", "root_cause_type"}
    assert hints["root_cause_type"] == "datanode_unreachable"


# --- anti-leak guard ---------------------------------------------------------


def test_anti_leak_catches_label_baked_into_log(tmp_path: Path):
    """If we accidentally baked the answer label into the log slice,
    _enforce_no_oracle_leak must refuse to write the task."""
    poisoned = _make_case()
    poisoned["slice"]["lines"][1] = "datanode_unreachable token leak: poisoned line"
    out = tmp_path / "tasks"
    with pytest.raises(RuntimeError, match="oracle leak"):
        ex.export_case(poisoned, out, author_name="x", author_email="x@example.com")


def test_anti_leak_catches_label_in_dockerfile(tmp_path: Path, monkeypatch):
    """If a future Dockerfile change leaks the root cause label, the guard
    catches it on re-export."""
    out = tmp_path / "tasks"
    ex.export_case(_make_case(), out, author_name="x", author_email="x@example.com")
    task_dir = out / "hdfs-datanode-abcdef1"
    # Manually corrupt the Dockerfile to simulate a regression.
    dockerfile = task_dir / "environment" / "Dockerfile"
    dockerfile.write_text(dockerfile.read_text() + "\n# datanode_unreachable\n")
    with pytest.raises(RuntimeError, match="oracle leak"):
        ex._enforce_no_oracle_leak(task_dir)


# --- derive_answer.py integration -------------------------------------------


def test_derive_answer_script_runs_and_produces_valid_answer(tmp_path: Path):
    """End-to-end: exporter emits derive_answer.py + log slice + hints;
    running the script reproduces an answer that satisfies the verifier
    invariants test_state.py checks."""
    out = tmp_path / "tasks"
    ex.export_case(_make_case(), out, author_name="x", author_email="x@example.com")
    task_dir = out / "hdfs-datanode-abcdef1"

    log_path = task_dir / "environment" / "data" / "hdfs.log"
    hints_path = task_dir / "solution" / "oracle_hints.json"
    derive = task_dir / "solution" / "derive_answer.py"
    answer_path = tmp_path / "answer.json"

    result = subprocess.run(
        [sys.executable, str(derive), "--log", str(log_path),
         "--hints", str(hints_path), "--out", str(answer_path)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr

    answer = json.loads(answer_path.read_text())
    expected = json.loads((task_dir / "tests" / "expected.json").read_text())

    # The invariants test_state.py enforces:
    assert answer["schema_version"] == expected["schema_version"]
    assert answer["is_incident"] is True
    assert sorted(answer["anomaly_line_ids"]) == sorted(expected["anomaly_line_ids"])
    assert answer["root_cause_type"] == expected["root_cause_type"]
    assert answer["root_cause_type"] in expected["allowed_root_causes"]
    assert answer["recommended_action"] in expected["safe_recommendations"]

    # Quotes match real log content.
    log_lines = log_path.read_text().splitlines()
    for entry in answer["evidence"]:
        assert entry["quote"] in log_lines[entry["line_id"] - 1]
