"""Severity scoring for T4 (severity classification).

The rule table is the one in docs/PLAN_V2.md T4. Severity is computed
from two inputs:

  - `tag`: the dataset-specific alert tag (or root_cause for datasets
    without inline tags, like Hadoop / HDFS / OpenStack).
  - `component_count`: how many distinct partition files contain anomaly
    lines (computed at export time from the line_map).

The classification rule (precedence: lowest P-number wins):

  P0 — component_count ≥ 3 OR tag in P0_TAGS
  P1 — component_count == 2 OR tag in P1_TAGS
  P2 — single component AND tag in P2_TAGS (recoverable)
  P3 — single component AND tag in P3_TAGS (transient warning)
  Default → P3 if no rule matches.

Justification labels follow the verifier's consistency rule:

  P0/P1 ⇒ "multi_component" (if multi-component triggered the rule)
        or "single_critical" (if a critical tag triggered the rule)
  P2    ⇒ "recoverable"
  P3    ⇒ "transient_warning"
"""

from __future__ import annotations

P0 = "P0"
P1 = "P1"
P2 = "P2"
P3 = "P3"

ALL_SEVERITIES = (P0, P1, P2, P3)

# Justification enum — must match the v2-sev verifier.
JUSTIFICATION_MULTI_COMPONENT = "multi_component"
JUSTIFICATION_SINGLE_CRITICAL = "single_critical"
JUSTIFICATION_RECOVERABLE = "recoverable"
JUSTIFICATION_TRANSIENT_WARNING = "transient_warning"

ALL_JUSTIFICATIONS = (
    JUSTIFICATION_MULTI_COMPONENT,
    JUSTIFICATION_SINGLE_CRITICAL,
    JUSTIFICATION_RECOVERABLE,
    JUSTIFICATION_TRANSIENT_WARNING,
)

# Per-dataset tag → severity-class mappings. Keys are case-normalized
# (matching what each adapter emits as root_cause / alert tag).
_DATASET_TAGS: dict[str, dict[str, tuple[str, ...]]] = {
    "HDFS_v1": {
        P0: ("namenode_error", "datanode_unreachable"),
        P1: ("replication_failure", "data_corruption"),
        P2: ("timeout",),
        P3: ("other",),
    },
    "Hadoop": {
        P0: ("machine_down",),
        P1: ("network_disconnect",),
        P2: ("disk_full",),
        P3: ("normal",),
    },
    "BGL": {
        # KERNSTOR/KERNTERM → P0 (critical kernel failures)
        # KERNDTLB/APPSEV → P1 (severe but recoverable kernel/app errors)
        # KERNMNTF/KERNRTSP/KERNREC/APPREAD → P2
        # APPRES/APPUNAV/other_alert → P3 (transient/info-level)
        P0: ("kernstor", "kernterm"),
        P1: ("kerndtlb", "appsev"),
        P2: ("kernmntf", "kernrtsp", "kernrec", "appread"),
        P3: ("appres", "appunav", "other_alert"),
    },
    "Thunderbird": {
        # Hardware faults at the bottom of the stack → P0
        # Storage layer → P1
        # Subsystem failures → P2
        # Application-level → P3
        P0: ("cpu", "ecc", "nmi"),
        P1: ("scsi", "chk_dsk", "ext_fs"),
        P2: ("mpt",),
        P3: ("vapi", "pbs_con", "pbs_bfd", "other_alert"),
    },
    "OpenStack": {
        P0: (),
        P1: ("vm_task_failure", "network_error"),
        P2: ("image_pull_failure",),
        P3: ("other",),
    },
}


def _tag_severity_class(dataset: str, tag: str) -> str | None:
    """Returns the severity P-class the tag maps to, or None if unknown."""
    by_class = _DATASET_TAGS.get(dataset)
    if not by_class:
        return None
    for severity, tags in by_class.items():
        if tag in tags:
            return severity
    return None


def compute_severity(dataset: str, tag: str, component_count: int) -> tuple[str, str]:
    """Return (severity, justification) for a case.

    Rules cascade by priority — the *highest severity* wins, so a
    P0 tag in a single-component window is still P0.
    """
    tag_class = _tag_severity_class(dataset, tag)

    # P0: component_count >= 3 OR P0 tag
    if component_count >= 3 or tag_class == P0:
        if tag_class == P0:
            return (P0, JUSTIFICATION_SINGLE_CRITICAL)
        return (P0, JUSTIFICATION_MULTI_COMPONENT)

    # P1: component_count == 2 OR P1 tag
    if component_count == 2 or tag_class == P1:
        if tag_class == P1:
            return (P1, JUSTIFICATION_SINGLE_CRITICAL)
        return (P1, JUSTIFICATION_MULTI_COMPONENT)

    # Single component below: tag class wins.
    if tag_class == P2:
        return (P2, JUSTIFICATION_RECOVERABLE)
    if tag_class == P3:
        return (P3, JUSTIFICATION_TRANSIENT_WARNING)

    # Unknown tag, single component → conservative default.
    return (P3, JUSTIFICATION_TRANSIENT_WARNING)


def justification_consistent(severity: str, justification: str) -> bool:
    """Mirrors the verifier's `test_justification_consistent_with_severity`."""
    if severity in (P0, P1):
        return justification in (JUSTIFICATION_MULTI_COMPONENT, JUSTIFICATION_SINGLE_CRITICAL)
    if severity in (P2, P3):
        return justification in (JUSTIFICATION_RECOVERABLE, JUSTIFICATION_TRANSIENT_WARNING)
    return False
