"""Remediation task helpers for Loghub-SRE.

The rem-* task family asks the agent to do more than diagnose: it must
choose an SRE mitigation, apply it via local container tooling, and leave
`/app/service_state.json` in the expected recovered state. The verifier
checks both the diagnosis fields and the observable post-mitigation
state.

This module is the single source of truth for:

- the allowed mitigation actions (`MITIGATION_ACTIONS`),
- the root-cause → recommended-action map per dataset (`MITIGATION_FOR`),
- expected post-mitigation health (`EXPECTED_HEALTH`),
- the deterministic topology and `service_state.json` shapes used by the
  agent-visible bin scripts.

The exporter (`export_to_harbor.py`) imports these tables and bakes them
into each task; the unit tests in `tests/` cover the table contents and
the synthesizer helpers below.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

# ---------------------------------------------------------------------------
# Action taxonomy
# ---------------------------------------------------------------------------

MITIGATION_ACTIONS: tuple[str, ...] = (
    "restart_component",
    "rollback_config",
    "increase_quota",
    "disable_route",
    "mark_noop",
)

# Actions an SRE may choose for an incident but that this task never
# expects as the correct answer — used to seed distractor lists and the
# `unsafe_actions` verifier check.
UNSAFE_ACTIONS: tuple[str, ...] = (
    "force_delete_data",
    "disable_monitoring",
    "ignore_alert",
)


@dataclass(frozen=True)
class RemediationDecision:
    """The canonical decision row for a single rem-* task."""

    action: str
    target_component: str  # bare component name (no .log suffix)
    expected_health: str  # "healthy" | "degraded" | "unhealthy"
    rationale: str  # short, evidence-grounded prose used by the oracle


# ---------------------------------------------------------------------------
# Root-cause → mitigation map
# ---------------------------------------------------------------------------
#
# The mapping below is intentionally narrow: each dataset's root_cause
# taxonomy is small (5-12 labels), and for each we pick exactly one
# canonical mitigation. The agent must derive the action from log evidence,
# not from a wider menu.

MITIGATION_FOR: dict[str, str] = {
    # HDFS_v1
    "replication_failure": "restart_component",
    "data_corruption": "mark_noop",
    "datanode_unreachable": "restart_component",
    "namenode_error": "restart_component",
    "timeout": "restart_component",
    "other": "restart_component",
    # Hadoop
    "machine_down": "restart_component",
    "network_disconnect": "disable_route",
    "disk_full": "increase_quota",
    "normal": "mark_noop",
    # BGL
    "kerndtlb": "restart_component",
    "kernstor": "restart_component",
    "appsev": "restart_component",
    "kernmntf": "restart_component",
    "kernterm": "restart_component",
    "kernrec": "restart_component",
    "appread": "restart_component",
    "kernrtsp": "restart_component",
    "appres": "restart_component",
    "appunav": "restart_component",
    "other_alert": "restart_component",
    # Thunderbird
    "vapi": "restart_component",
    "pbs_con": "restart_component",
    "mpt": "restart_component",
    "ext_fs": "increase_quota",
    "cpu": "mark_noop",
    "scsi": "rollback_config",
    "ecc": "mark_noop",
    "pbs_bfd": "restart_component",
    "chk_dsk": "increase_quota",
    "nmi": "mark_noop",
    # OpenStack
    "vm_task_failure": "restart_component",
    "network_error": "disable_route",
    "image_pull_failure": "rollback_config",
}

# Some root causes are intrinsically not auto-recoverable through restart;
# they expect "degraded" with `escalated=true` after `mark_noop`.
DEGRADED_EXPECTED: frozenset[str] = frozenset(
    {"data_corruption", "cpu", "ecc", "nmi", "normal"}
)

# ---------------------------------------------------------------------------
# Observable fault symptoms
# ---------------------------------------------------------------------------
#
# Each canonical action corresponds to an observable symptom on the ROOT
# component in service_state.json. The symptom is legitimate diagnostic
# state (an SRE inspecting the cluster would see it), and it is what makes
# the agent-visible tooling honest: /app/bin/apply_mitigation only clears
# the symptom its action actually addresses, so running the wrong remedy
# leaves the cluster visibly broken instead of "confirming" a bad fix.
# The symptom names deliberately do NOT reuse root_cause_type labels.

SYMPTOM_FOR_ACTION: dict[str, tuple[str, object, object]] = {
    # action -> (symptom_field, broken_value, recovered_value)
    "restart_component": ("process_state", "not_responding", "running"),
    "increase_quota": ("storage_usage_pct", 100, 35),
    "disable_route": ("peer_link", "flapping", "isolated"),
    "rollback_config": ("config_status", "drifted", "known_good"),
    "mark_noop": ("hardware_status", "failing_unrecoverable", "failing_unrecoverable"),
}


def symptom_for_action(action: str) -> tuple[str, object, object]:
    return SYMPTOM_FOR_ACTION.get(action, SYMPTOM_FOR_ACTION["restart_component"])


def mitigation_for_root_cause(root_cause: str) -> str:
    """Return the canonical mitigation action for a dataset root_cause.

    Falls back to `restart_component` for unknown labels — defensible
    default for any taxonomy entry that wasn't explicitly mapped.
    """
    return MITIGATION_FOR.get(root_cause, "restart_component")


def expected_health_for_root_cause(root_cause: str) -> str:
    """`healthy` after a successful mitigation, except for root causes
    where the canonical mitigation is `mark_noop` (escalation only)."""
    return "degraded" if root_cause in DEGRADED_EXPECTED else "healthy"


# ---------------------------------------------------------------------------
# Component-name helpers
# ---------------------------------------------------------------------------


def component_name_from_filename(filename: str) -> str:
    """`hdfs-namenode.log` -> `hdfs-namenode`."""
    if filename.endswith(".log"):
        return filename[: -len(".log")]
    return filename


# ---------------------------------------------------------------------------
# Topology + service_state synthesizers
# ---------------------------------------------------------------------------


def build_topology(file_basenames: Iterable[str], root_filename: str) -> dict:
    """Synthesize a simple dependency topology from the file list.

    The root component has no upstream deps; every other component depends
    on the root. That matches the canonical "namenode-down cascades to
    datanodes" shape and keeps the topology deterministic without needing
    to encode per-dataset wiring rules.
    """
    files = sorted(file_basenames)
    root = component_name_from_filename(root_filename)
    components = []
    for name in files:
        comp = component_name_from_filename(name)
        components.append(
            {
                "name": comp,
                "log_file": name,
                "depends_on": [] if comp == root else [root],
            }
        )
    return {
        "root_component": root,
        "components": components,
    }


def build_initial_state(
    file_basenames: Iterable[str], root_filename: str, required_action: str = "restart_component"
) -> dict:
    """Encode 'pre-mitigation' state: root degraded with an observable fault
    symptom (determined by the canonical action that fixes it), deps cascading."""
    root = component_name_from_filename(root_filename)
    field, broken, _recovered = symptom_for_action(required_action)
    state: dict = {"components": {}}
    for name in sorted(file_basenames):
        comp = component_name_from_filename(name)
        if comp == root:
            state["components"][comp] = {
                "state": "degraded",
                "escalated": False,
                "last_action": None,
                field: broken,
            }
        else:
            state["components"][comp] = {
                "state": "degraded",
                "escalated": False,
                "last_action": None,
                "cascading_from": root,
            }
    return state


# ---------------------------------------------------------------------------
# apply_mitigation deterministic semantics
# ---------------------------------------------------------------------------
#
# The apply_mitigation script (rendered into /app/bin/) takes
# `--action ACT --target TGT` and mutates /app/service_state.json. The
# semantics encoded below are also used by the unit tests to assert
# behaviour without invoking the shipped Python script.


def simulate_apply_mitigation(
    state: dict, action: str, target: str, *, root_component: str
) -> dict:
    """Pure function: return the new state after applying (action, target).

    Fault-specific semantics: the root component carries an observable
    symptom field (see ``SYMPTOM_FOR_ACTION``), and an active action heals
    the cluster ONLY if it is the action that clears that symptom.
    Restarting a process does not fix a full disk — the symptom (and the
    degraded state) persists, exactly as in production.

      - the matching active action applied to the root: clear the symptom,
        flip root to healthy and recover its dependents.
      - mark_noop applied to the root: leave state degraded but set
        escalated=true. This is the right answer for unrecoverable causes.
      - a non-matching action, an out-of-enum action, or a wrong target:
        leave health untouched and record `last_action` so the attempt is
        visible.
    """
    new_state = {
        "components": {
            comp: dict(info) for comp, info in state.get("components", {}).items()
        }
    }
    for info in new_state["components"].values():
        info["last_action"] = action

    if action not in MITIGATION_ACTIONS or target != root_component:
        return new_state

    if action == "mark_noop":
        new_state["components"][root_component]["escalated"] = True
        return new_state

    field, broken, recovered = symptom_for_action(action)
    root_info = new_state["components"].get(root_component, {})
    if root_info.get(field) != broken:
        # Wrong remedy for the observed fault: nothing recovers.
        return new_state

    for comp, info in new_state["components"].items():
        info["state"] = "healthy"
        info["cascading_from"] = None
        if comp == root_component:
            info["escalated"] = False
            info[field] = recovered
    return new_state


def health_summary(state: dict) -> str:
    """Reduce service_state to a single overall health label."""
    components = state.get("components", {})
    if not components:
        return "unknown"
    states = {info.get("state", "unknown") for info in components.values()}
    if states == {"healthy"}:
        return "healthy"
    if "unhealthy" in states:
        return "unhealthy"
    return "degraded"


# ---------------------------------------------------------------------------
# Config-file pair synthesis
# ---------------------------------------------------------------------------
#
# Some mitigations target config rather than process state. We bake a
# "current" config plus a "known_good" backup so `rollback_config` is a
# real local file operation, not a stub. For non-config root causes the
# config files are still emitted but the rollback verifier only fires
# when action == rollback_config.


def build_component_configs(file_basenames: Iterable[str], root_filename: str, action: str) -> dict[str, dict]:
    """`{filename: {"current": ..., "known_good": ...}}` for each component."""
    root = component_name_from_filename(root_filename)
    out: dict[str, dict] = {}
    for name in sorted(file_basenames):
        comp = component_name_from_filename(name)
        if comp == root and action == "rollback_config":
            current = {
                "version": "2",
                "feature_flags": {"new_routing": True},
                "thresholds": {"max_concurrent": 0},  # known-broken
                "endpoint": "https://broken.invalid",
            }
            known_good = {
                "version": "1",
                "feature_flags": {"new_routing": False},
                "thresholds": {"max_concurrent": 64},
                "endpoint": "https://default.invalid",
            }
        else:
            current = {
                "version": "1",
                "feature_flags": {"new_routing": False},
                "thresholds": {"max_concurrent": 64},
                "endpoint": "https://default.invalid",
            }
            known_good = current
        out[comp] = {"current": current, "known_good": known_good}
    return out
