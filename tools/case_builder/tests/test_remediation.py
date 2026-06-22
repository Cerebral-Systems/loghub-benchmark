"""Unit tests for the remediation taxonomy + state-mutation helpers.

Covers:
- mitigation_for_root_cause / expected_health_for_root_cause taxonomy mapping
- build_topology + build_initial_state shape
- simulate_apply_mitigation behaviour for the four "recovery" actions and
  the mark_noop escalation path
- end-to-end rem task export via the build_rem_tasks driver against a
  fixtures-style synthetic source task
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from tools.case_builder import build_rem_tasks as brt
from tools.case_builder import remediation as rem
from tools.case_builder import export_to_harbor as ex


# --- Taxonomy ---------------------------------------------------------------


def test_mitigation_for_root_cause_covers_known_labels():
    # Every label in the per-dataset taxonomy must resolve to a known action.
    for label, action in rem.MITIGATION_FOR.items():
        assert action in rem.MITIGATION_ACTIONS, (
            f"label {label!r} maps to {action!r} which is not an allowed action"
        )


def test_mitigation_for_unknown_root_cause_defaults_to_restart():
    assert rem.mitigation_for_root_cause("never_seen_label") == "restart_component"


def test_expected_health_for_known_degraded_root_causes():
    for label in ("data_corruption", "cpu", "ecc", "nmi"):
        assert rem.expected_health_for_root_cause(label) == "degraded"


def test_expected_health_for_recoverable_root_causes():
    for label in ("datanode_unreachable", "machine_down", "vm_task_failure"):
        assert rem.expected_health_for_root_cause(label) == "healthy"


# --- Topology + state synthesis ---------------------------------------------


def test_build_topology_marks_only_root_as_independent():
    files = ["a.log", "b.log", "c.log"]
    topo = rem.build_topology(files, "b.log")
    by_name = {c["name"]: c for c in topo["components"]}
    assert by_name["b"]["depends_on"] == []
    assert by_name["a"]["depends_on"] == ["b"]
    assert by_name["c"]["depends_on"] == ["b"]
    assert topo["root_component"] == "b"


def test_build_initial_state_degrades_everyone_and_cascades_dependents():
    files = ["a.log", "b.log", "c.log"]
    state = rem.build_initial_state(files, "b.log")
    assert state["components"]["b"]["state"] == "degraded"
    assert "cascading_from" not in state["components"]["b"]
    assert state["components"]["a"]["cascading_from"] == "b"
    assert state["components"]["c"]["cascading_from"] == "b"


# --- Mitigation simulation --------------------------------------------------


def test_simulate_restart_recovers_cluster():
    state = rem.build_initial_state(["a.log", "b.log"], "a.log")
    new_state = rem.simulate_apply_mitigation(state, "restart_component", "a", root_component="a")
    states = {info["state"] for info in new_state["components"].values()}
    assert states == {"healthy"}


def test_simulate_mark_noop_keeps_degraded_but_escalates_root():
    state = rem.build_initial_state(["a.log", "b.log"], "a.log")
    new_state = rem.simulate_apply_mitigation(state, "mark_noop", "a", root_component="a")
    assert new_state["components"]["a"]["state"] == "degraded"
    assert new_state["components"]["a"]["escalated"] is True
    assert rem.health_summary(new_state) == "degraded"


def test_simulate_wrong_target_does_nothing():
    state = rem.build_initial_state(["a.log", "b.log"], "a.log")
    new_state = rem.simulate_apply_mitigation(
        state, "restart_component", "b", root_component="a"
    )
    states = {info["state"] for info in new_state["components"].values()}
    assert states == {"degraded"}
    # last_action is still recorded so the verifier can see the attempt.
    assert new_state["components"]["a"]["last_action"] == "restart_component"


def test_simulate_out_of_enum_does_nothing():
    state = rem.build_initial_state(["a.log", "b.log"], "a.log")
    new_state = rem.simulate_apply_mitigation(
        state, "force_delete_data", "a", root_component="a"
    )
    states = {info["state"] for info in new_state["components"].values()}
    assert states == {"degraded"}
    assert new_state["components"]["a"]["last_action"] == "force_delete_data"


def test_health_summary_is_healthy_only_when_all_components_healthy():
    state = rem.build_initial_state(["a.log", "b.log"], "a.log")
    assert rem.health_summary(state) == "degraded"
    healed = rem.simulate_apply_mitigation(state, "restart_component", "a", root_component="a")
    assert rem.health_summary(healed) == "healthy"


# --- End-to-end rem export --------------------------------------------------


def _make_rem_case() -> dict:
    return {
        "case_id": "abcdef1234567890" + "0" * 48,
        "dataset_name": "HDFS_v1",
        "adapter_version": "rem-1",
        "slice": {"lines": [], "offset": 0, "length": 0},
        "anomaly_line_ids": [],
        "root_cause": "datanode_unreachable",
        "anomaly_keys": [],
        "extra": {
            "rem": {
                "files": {
                    "hdfs-namenode.log": [
                        "081109 203615 35 INFO dfs.FSNamesystem: namenode degraded reason A",
                        "081109 203616 35 INFO dfs.FSNamesystem: namenode degraded reason B",
                    ],
                    "hdfs-datanode-a.log": [
                        "081109 203620 148 INFO dfs.DataNode$DataXceiver: datanode cascading",
                    ],
                },
                "root_component": "hdfs-namenode.log",
                "causal_chain": [
                    {"step": 0, "component": "hdfs-namenode.log", "role": "root", "evidence_line": 1},
                    {"step": 1, "component": "hdfs-datanode-a.log", "role": "downstream",
                     "caused_by_step": 0, "evidence_line": 1},
                ],
                "anomaly_locations": [
                    {"file": "hdfs-namenode.log", "line": 1},
                    {"file": "hdfs-datanode-a.log", "line": 1},
                ],
                "source_task": "test-source",
            },
        },
        "task_type": "rem",
    }


def test_export_rem_writes_expected_layout(tmp_path: Path) -> None:
    case = _make_rem_case()
    out = tmp_path / "tasks"
    task_dir = ex.export_case(case, out, author_name="X", author_email="x@example.com")
    for rel in (
        "task.toml",
        "instruction.md",
        "environment/Dockerfile",
        "environment/data/topology.json",
        "environment/data/service_state.json",
        "environment/data/bin/apply_mitigation",
        "environment/data/bin/check_health",
        "environment/data/logs/hdfs-namenode.log",
        "environment/data/logs/hdfs-datanode-a.log",
        "environment/data/config/hdfs-namenode.json",
        "environment/data/config/hdfs-namenode.known_good.json",
        "solution/derive_answer.py",
        "solution/oracle_hints.json",
        "solution/solve.sh",
        "tests/test.sh",
        "tests/test_state.py",
        "tests/expected.json",
    ):
        assert (task_dir / rel).exists(), f"missing {rel}"

    expected = json.loads((task_dir / "tests" / "expected.json").read_text())
    assert expected["schema_version"] == ex.ANSWER_SCHEMA_VERSION_REM
    assert expected["root_component"] == "hdfs-namenode"
    assert expected["mitigation"]["action"] == "restart_component"
    assert expected["mitigation"]["target"] == "hdfs-namenode"
    assert "restart_component" in expected["allowed_actions"]
    assert "force_delete_data" in expected["unsafe_actions"]


def test_rem_apply_mitigation_runs_in_subprocess(tmp_path: Path) -> None:
    case = _make_rem_case()
    out = tmp_path / "tasks"
    task_dir = ex.export_case(case, out, author_name="X", author_email="x@example.com")
    # Stage a /app-like working dir.
    app = tmp_path / "app"
    (app / "logs").mkdir(parents=True)
    (app / "bin").mkdir()
    for f in ("hdfs-namenode.log", "hdfs-datanode-a.log"):
        (app / "logs" / f).write_text(
            (task_dir / "environment" / "data" / "logs" / f).read_text()
        )
    (app / "topology.json").write_text(
        (task_dir / "environment" / "data" / "topology.json").read_text()
    )
    (app / "service_state.json").write_text(
        (task_dir / "environment" / "data" / "service_state.json").read_text()
    )
    (app / "bin" / "apply_mitigation").write_text(
        (task_dir / "environment" / "data" / "bin" / "apply_mitigation").read_text()
    )
    (app / "bin" / "apply_mitigation").chmod(0o755)
    rc = subprocess.run(
        [
            "python3", str(app / "bin" / "apply_mitigation"),
            "--action", "restart_component",
            "--target", "hdfs-namenode",
            "--state", str(app / "service_state.json"),
            "--topology", str(app / "topology.json"),
        ],
        capture_output=True,
        text=True,
    )
    assert rc.returncode == 0, rc.stderr
    state = json.loads((app / "service_state.json").read_text())
    states = {info["state"] for info in state["components"].values()}
    assert states == {"healthy"}


def _write_opaque_corr_source(tasks_dir: Path, slug: str) -> Path:
    task_dir = tasks_dir / slug
    (task_dir / "tests").mkdir(parents=True)
    (task_dir / "environment" / "data").mkdir(parents=True)
    (task_dir / "environment" / "data" / "hdfs-namenode.log").write_text(
        "root block allocation\n"
    )
    (task_dir / "environment" / "data" / "hdfs-datanode-a.log").write_text(
        "downstream block receive\n"
    )
    (task_dir / "tests" / "expected.json").write_text(
        json.dumps(
            {
                "schema_version": ex.ANSWER_SCHEMA_VERSION_CORR,
                "files": ["hdfs-namenode.log", "hdfs-datanode-a.log"],
                "root_component": "hdfs-namenode.log",
                "root_cause_type": "datanode_unreachable",
                "causal_chain": [
                    {
                        "step": 0,
                        "component": "hdfs-namenode.log",
                        "role": "root",
                        "evidence_line": 1,
                        "snippet": "root block allocation",
                    },
                    {
                        "step": 1,
                        "component": "hdfs-datanode-a.log",
                        "role": "downstream",
                        "caused_by_step": 0,
                        "evidence_line": 1,
                        "snippet": "downstream block receive",
                    },
                ],
            }
        )
        + "\n"
    )
    return task_dir


def test_synthesize_rem_case_supports_opaque_task_ids(tmp_path: Path) -> None:
    tasks_dir = tmp_path / "tasks"
    source = _write_opaque_corr_source(tasks_dir, "lh-12345678")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "task-id-map.json").write_text(
        json.dumps({"lh-12345678": "corr-hdfs-other-legacy123"}) + "\n"
    )

    case = brt.synthesize_rem_case(source)

    assert case is not None
    assert case["dataset_name"] == "HDFS_v1"
    assert case["extra"]["rem"]["source_task"] == "corr-hdfs-other-legacy123"
    assert case["extra"]["rem"]["files"]["hdfs-namenode.log"] == [
        "root block allocation"
    ]


def test_default_rem_selection_uses_task_id_map_for_opaque_dirs(tmp_path: Path) -> None:
    tasks_dir = tmp_path / "tasks"
    source = _write_opaque_corr_source(tasks_dir, "lh-abcdef12")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "task-id-map.json").write_text(
        json.dumps({"lh-abcdef12": "corr-hdfs-other-legacy456"}) + "\n"
    )

    assert brt.build_default_selection(tasks_dir) == [source]
