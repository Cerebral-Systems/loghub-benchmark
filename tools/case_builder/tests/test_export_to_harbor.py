"""Unit tests for the Harbor task exporter.

The exporter emits multi-file partitioned tasks. Tests cover both the
directory shape that Harbor's static checks read and the (file, line)
tuple schema that the verifier asserts against.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools.case_builder import export_to_harbor as ex


def _make_hdfs_case(**overrides) -> dict:
    """Build a synthetic HDFS case with a mix of namenode + datanode lines
    so partitioning produces multiple files."""
    case: dict = {
        "case_id": "abcdef1234567890" + "0" * 48,
        "dataset_name": "HDFS_v1",
        "adapter_version": "2",
        "slice": {
            "lines": [
                "081109 203615 148 INFO dfs.DataNode$DataXceiver: Receiving block blk_42 src: /10.0.0.1:50010 dest: /10.0.0.1:50010",
                "081109 203616 35 INFO dfs.FSNamesystem: BLOCK* NameSystem.addStoredBlock for blk_42",
                "081109 203617 148 INFO dfs.DataNode$DataXceiver: writeBlock blk_42 received exception",
                "081109 203618 35 INFO dfs.FSNamesystem: namesystem heartbeat",
            ],
            "offset": 0,
            "length": 4,
        },
        "anomaly_line_ids": [1, 3],
        "root_cause": "datanode_unreachable",
        "anomaly_keys": ["blk_42"],
        "extra": {},
    }
    case.update(overrides)
    return case


def _make_bgl_case(**overrides) -> dict:
    case: dict = {
        "case_id": "1234567890abcdef" + "1" * 48,
        "dataset_name": "BGL",
        "adapter_version": "1",
        "slice": {
            "lines": [
                "KERNDTLB 1 2005.06.03 R03-M0-N0-C:J12-U11 ts host RAS KERNEL FATAL data TLB",
                "- 1 2005.06.03 R04-M0-N0-C:J12-U11 ts host RAS KERNEL INFO normal",
                "KERNDTLB 1 2005.06.03 R05-M0-N0-C:J12-U11 ts host RAS KERNEL FATAL data TLB",
                "APPSEV 1 2005.06.03 R06-M0-N0-C:J12-U11 ts host RAS APP FATAL severe error",
            ],
            "offset": 0,
            "length": 4,
        },
        "anomaly_line_ids": [1, 3],
        "root_cause": "kerndtlb",
        "anomaly_keys": ["KERNDTLB"],
        "extra": {},
    }
    case.update(overrides)
    return case


# --- slug -------------------------------------------------------------------


def test_make_slug_is_three_token_lowercase_hyphen():
    case = _make_hdfs_case()
    slug = ex.make_slug(case)
    assert slug == "hdfs-datanode-abcdef1"
    parts = slug.split("-")
    assert len(parts) == 3
    assert all(p == p.lower() for p in parts)


def test_make_slug_handles_underscore_root_causes():
    case = _make_hdfs_case(
        dataset_name="OpenStack",
        root_cause="vm_task_failure",
        case_id="ffeeddccbbaa9988" + "1" * 48,
    )
    slug = ex.make_slug(case)
    assert slug == "openstack-vmtask-ffeeddc"
    assert "_" not in slug


def test_make_slug_is_stable_across_runs():
    case = _make_hdfs_case()
    assert ex.make_slug(case) == ex.make_slug(case)


# --- partition functions ----------------------------------------------------


@pytest.mark.parametrize(
    "line,expected",
    [
        ("081109 203615 148 INFO dfs.NameNode: foo", "hdfs-namenode.log"),
        ("081109 203615 148 INFO dfs.FSNamesystem: bar", "hdfs-namenode.log"),
        ("081109 203615 148 INFO dfs.DataNode$DataXceiver: writeBlock /10.0.0.1:50010 ...", "hdfs-datanode-a.log"),
        ("081109 203615 148 INFO dfs.OtherComponent: misc line", "hdfs-misc.log"),
    ],
)
def test_partition_hdfs(line: str, expected: str):
    """Datanode IPs hash deterministically into the -a/-b bucket; we only
    assert membership in {-a, -b, -other} for the datanode case."""
    result = ex._partition_hdfs(line)
    if expected.endswith("hdfs-datanode-a.log"):
        assert result in {"hdfs-datanode-a.log", "hdfs-datanode-b.log"}
    else:
        assert result == expected


def test_partition_hadoop_drops_synthetic_headers():
    assert ex._partition_hadoop("### normal_job=application_1_001") is None
    assert ex._partition_hadoop("### anomalous_job=application_1_002") is None


def test_partition_bgl_buckets_by_full_location_token():
    line_a = "- 1 2005.06.03 R03-M0-N0-C:J12-U11 ts host RAS KERNEL INFO foo"
    line_b = "- 1 2005.06.03 R03-M0-N1-C:J12-U11 ts host RAS KERNEL INFO bar"
    assert ex._partition_bgl(line_a).startswith("bgl-nodes-")
    assert ex._partition_bgl(line_b).startswith("bgl-nodes-")
    assert ex._partition_bgl(line_a) == ex._partition_bgl(line_a)


def test_partition_openstack_by_service():
    assert ex._partition_openstack(
        "nova-api.log.2017-05-14 2017-05-14 19:39 25746 INFO ..."
    ) == "openstack-nova-api.log"
    assert ex._partition_openstack(
        "nova-compute.log.2017-05-14 2017-05-14 19:39 2931 INFO ..."
    ) == "openstack-nova-compute.log"


# --- export_case structure (multi-file) -------------------------------------


def test_export_case_writes_partitioned_files(tmp_path: Path):
    out = tmp_path / "tasks"
    ex.export_case(
        _make_hdfs_case(), out, author_name="Author X", author_email="x@example.com"
    )
    task_dir = out / "hdfs-datanode-abcdef1"
    # Expect at least namenode + at least one datanode file.
    data_dir = task_dir / "environment" / "data"
    log_files = sorted(p.name for p in data_dir.glob("*.log"))
    assert "hdfs-namenode.log" in log_files
    assert any("hdfs-datanode" in name for name in log_files)
    assert len(log_files) >= 2, f"expected ≥2 partition files; got {log_files}"


def test_dockerfile_copies_every_log_file(tmp_path: Path):
    out = tmp_path / "tasks"
    ex.export_case(_make_hdfs_case(), out, author_name="x", author_email="x@example.com")
    task_dir = out / "hdfs-datanode-abcdef1"
    dockerfile = (task_dir / "environment" / "Dockerfile").read_text()
    for log in (task_dir / "environment" / "data").glob("*.log"):
        assert f"COPY data/{log.name} /app/{log.name}" in dockerfile


def test_expected_json_uses_v2_schema(tmp_path: Path):
    out = tmp_path / "tasks"
    ex.export_case(_make_hdfs_case(), out, author_name="x", author_email="x@example.com")
    expected = json.loads((out / "hdfs-datanode-abcdef1" / "tests" / "expected.json").read_text())
    assert expected["schema_version"] == "loghub-sre-answer-v2"
    # Evidence is now a list of {file, line}.
    assert isinstance(expected["evidence"], list)
    assert all({"file", "line"}.issubset(e) for e in expected["evidence"])
    # Plus the legacy fields the verifier still uses.
    assert expected["root_cause_type"] == "datanode_unreachable"
    assert expected["anomaly_keys"] == ["blk_42"]
    assert expected["evidence_validation"] == {"mode": "exact_location"}
    assert expected["files"]


def test_inline_label_expected_json_omits_huge_ground_truth_locations(tmp_path: Path):
    out = tmp_path / "tasks"
    ex.export_case(_make_bgl_case(), out, author_name="x", author_email="x@example.com")
    expected = json.loads((out / "bgl-kerndtlb-1234567" / "tests" / "expected.json").read_text())
    assert expected["evidence"] == []
    assert expected["evidence_validation"]["mode"] == "inline_label"
    assert expected["evidence_validation"]["tag_to_root_cause"]["KERNDTLB"] == "kerndtlb"
    hints = json.loads((out / "bgl-kerndtlb-1234567" / "solution" / "oracle_hints.json").read_text())
    assert hints["anomaly_locations"]


def test_inline_label_oracle_hints_match_expected_root_cause(tmp_path: Path):
    out = tmp_path / "tasks"
    case = _make_bgl_case(anomaly_line_ids=[1, 3, 4])
    ex.export_case(case, out, author_name="x", author_email="x@example.com")
    task_dir = out / "bgl-kerndtlb-1234567"
    hints = json.loads((task_dir / "solution" / "oracle_hints.json").read_text())
    data_dir = task_dir / "environment" / "data"
    cited_tags = []
    for loc in hints["anomaly_locations"]:
        line = (data_dir / loc["file"]).read_text().splitlines()[loc["line"] - 1]
        cited_tags.append(line.split(None, 1)[0])
    assert cited_tags == ["KERNDTLB", "KERNDTLB"]


def test_anomaly_line_ids_translated_to_file_line_tuples(tmp_path: Path):
    out = tmp_path / "tasks"
    ex.export_case(_make_hdfs_case(), out, author_name="x", author_email="x@example.com")
    task_dir = out / "hdfs-datanode-abcdef1"
    expected = json.loads((task_dir / "tests" / "expected.json").read_text())
    # The fixture has 4 lines; anomaly slice ids 1 and 3 are DataNode lines
    # that go into hdfs-datanode-*.log. Each entry must point at a real line.
    for entry in expected["evidence"]:
        log_path = task_dir / "environment" / "data" / entry["file"]
        assert log_path.is_file()
        lines = log_path.read_text().splitlines()
        assert 1 <= entry["line"] <= len(lines)


def test_task_toml_uses_new_schema(tmp_path: Path):
    out = tmp_path / "tasks"
    ex.export_case(_make_hdfs_case(), out, author_name="x", author_email="x@example.com")
    toml_text = (out / "hdfs-datanode-abcdef1" / "task.toml").read_text()
    assert 'version = "1.0"' in toml_text
    assert "schema_version" not in toml_text
    assert 'name = "loghub-sre/hdfs-datanode-abcdef1"' in toml_text
    assert 'difficulty = "medium"' in toml_text
    assert 'category = "sre-log-investigation"' in toml_text
    assert "allow_internet = true" in toml_text
    assert '"multi-file"' in toml_text
    for forbidden in ("difficulty_explanation", "solution_explanation", "expert_time_estimate_hours"):
        assert forbidden not in toml_text


def test_canary_present_in_every_emitted_text_file(tmp_path: Path):
    out = tmp_path / "tasks"
    ex.export_case(_make_hdfs_case(), out, author_name="x", author_email="x@example.com")
    task_dir = out / "hdfs-datanode-abcdef1"
    for relative in (
        "instruction.md",
        "task.toml",
        "environment/Dockerfile",
        "solution/solve.sh",
        "solution/derive_answer.py",
        "tests/test.sh",
        "tests/test_state.py",
    ):
        assert ex.CANARY_GUID in (task_dir / relative).read_text(), f"canary missing from {relative}"


def test_oracle_hints_carry_file_line_locations(tmp_path: Path):
    out = tmp_path / "tasks"
    ex.export_case(_make_hdfs_case(), out, author_name="x", author_email="x@example.com")
    hints = json.loads((out / "hdfs-datanode-abcdef1" / "solution" / "oracle_hints.json").read_text())
    assert "anomaly_locations" in hints
    for loc in hints["anomaly_locations"]:
        assert {"file", "line"}.issubset(loc)
    assert hints["root_cause_type"] == "datanode_unreachable"
    assert hints["anomaly_keys"] == ["blk_42"]


# --- single-file backward-compat --------------------------------------------


def test_single_file_flag_restores_legacy_layout(tmp_path: Path):
    out = tmp_path / "tasks"
    ex.export_case(
        _make_hdfs_case(),
        out,
        author_name="x",
        author_email="x@example.com",
        single_file=True,
    )
    task_dir = out / "hdfs-datanode-abcdef1"
    files = sorted(p.name for p in (task_dir / "environment" / "data").glob("*.log"))
    assert files == ["hdfs.log"]  # single concatenated file


# --- anti-leak guard --------------------------------------------------------


def test_anti_leak_catches_label_baked_into_log(tmp_path: Path):
    poisoned = _make_hdfs_case()
    poisoned["slice"]["lines"][1] = "081109 203616 35 INFO dfs.FSNamesystem: datanode_unreachable token leak"
    out = tmp_path / "tasks"
    with pytest.raises(RuntimeError, match="oracle leak"):
        ex.export_case(poisoned, out, author_name="x", author_email="x@example.com")


def test_anti_leak_catches_label_in_dockerfile(tmp_path: Path):
    out = tmp_path / "tasks"
    ex.export_case(_make_hdfs_case(), out, author_name="x", author_email="x@example.com")
    task_dir = out / "hdfs-datanode-abcdef1"
    dockerfile = task_dir / "environment" / "Dockerfile"
    dockerfile.write_text(dockerfile.read_text() + "\n# datanode_unreachable leaked here\n")
    with pytest.raises(RuntimeError, match="oracle leak"):
        ex._enforce_no_oracle_leak(task_dir)


def test_anti_leak_allows_filenames_in_dockerfile(tmp_path: Path):
    """Filenames legitimately appear in both the Dockerfile (COPY) and
    expected.json (files list). The guard must not flag them."""
    out = tmp_path / "tasks"
    # This should not raise.
    ex.export_case(_make_hdfs_case(), out, author_name="x", author_email="x@example.com")


# --- derive_answer.py integration -------------------------------------------


def test_derive_answer_script_runs_and_produces_valid_answer(tmp_path: Path):
    out = tmp_path / "tasks"
    ex.export_case(_make_hdfs_case(), out, author_name="x", author_email="x@example.com")
    task_dir = out / "hdfs-datanode-abcdef1"

    # Stage logs as if /app/ inside the container.
    app_dir = tmp_path / "app"
    app_dir.mkdir()
    for log in (task_dir / "environment" / "data").glob("*.log"):
        (app_dir / log.name).write_text(log.read_text())

    hints_path = task_dir / "solution" / "oracle_hints.json"
    derive = task_dir / "solution" / "derive_answer.py"
    answer_path = tmp_path / "answer.json"

    result = subprocess.run(
        [sys.executable, str(derive), "--app-dir", str(app_dir),
         "--hints", str(hints_path), "--out", str(answer_path)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr

    answer = json.loads(answer_path.read_text())
    expected = json.loads((task_dir / "tests" / "expected.json").read_text())

    assert answer["schema_version"] == expected["schema_version"]
    assert answer["is_incident"] is True
    assert answer["root_cause_type"] == expected["root_cause_type"]
    assert answer["root_cause_type"] in expected["allowed_root_causes"]
    assert answer["recommended_action"] in expected["safe_recommendations"]
    # Evidence is multi-file now.
    answer_locs = sorted((e["file"], e["line"]) for e in answer["evidence"])
    expected_locs = sorted((e["file"], e["line"]) for e in expected["evidence"])
    assert answer_locs == expected_locs
    # Snippets must come from the actual file content.
    for entry in answer["evidence"]:
        actual_line = (app_dir / entry["file"]).read_text().splitlines()[entry["line"] - 1]
        assert entry["snippet"] in actual_line
