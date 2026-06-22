from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.case_builder import rebuild_curated as rc


def test_expected_dataset_from_expected_uses_files_not_slug() -> None:
    expected = {"files": ["thunderbird-tbird.log"]}

    assert rc.expected_dataset_from_expected(expected) == "Thunderbird"


def test_expected_dataset_from_expected_rejects_missing_files() -> None:
    with pytest.raises(SystemExit, match="files"):
        rc.expected_dataset_from_expected({"files": []})


def test_write_manifest_uses_legacy_slug_for_opaque_task_ids(tmp_path: Path) -> None:
    tasks_dir = tmp_path / "tasks"
    task_dir = tasks_dir / "lh-12345678"
    task_dir.mkdir(parents=True)
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "task-id-map.json").write_text(
        json.dumps({"lh-12345678": "hdfs-datanode-abcdef0"}) + "\n"
    )

    cases_dir = tmp_path / "cases" / "hdfs"
    cases_dir.mkdir(parents=True)
    case = {
        "dataset_name": "HDFS_v1",
        "adapter_version": "1",
        "case_id": "abcdef0123456789",
        "root_cause": "datanode_unreachable",
        "anomaly_keys": ["blk_1"],
    }
    (cases_dir / "case.json").write_text(json.dumps(case) + "\n")
    (cases_dir / "manifest.json").write_text(
        json.dumps({"cases": [{"file": "case.json"}]}) + "\n"
    )

    output = tmp_path / "curated_selection.json"
    rc.write_manifest(tasks_dir, [f"hdfs={cases_dir}"], output, seed=0)

    manifest = json.loads(output.read_text())
    assert manifest["selections"] == [
        {
            "slug": "hdfs-datanode-abcdef0",
            "adapter": "hdfs",
            "dataset_name": "HDFS_v1",
            "adapter_version": "1",
            "case_id": "abcdef0123456789",
            "root_cause": "datanode_unreachable",
            "anomaly_keys": ["blk_1"],
        }
    ]
