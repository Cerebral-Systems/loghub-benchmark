"""Shared timeline-building for T2 (temporal sequence reconstruction).

Per docs/PLAN_V2.md T2, each adapter exposes a `parse_event(line)` that
extracts (timestamp_int, component, level) from a log line. This module
takes the adapter + a CandidateCase and returns a canonical ordered
timeline of the anomaly lines tagged with `trigger` / `propagation` /
`consequence` roles.

Tiebreak rule: when two events share both timestamp and component
precedence, the lower slice-relative line index wins (mirrors the
chronological order in the file).
"""

from __future__ import annotations

from dataclasses import dataclass


TRIGGER_ROLE = "trigger"
PROPAGATION_ROLE = "propagation"
CONSEQUENCE_ROLE = "consequence"
NOISE_ROLE = "noise"

ALLOWED_ROLES = (TRIGGER_ROLE, PROPAGATION_ROLE, CONSEQUENCE_ROLE, NOISE_ROLE)


@dataclass(frozen=True)
class TimelineEvent:
    sequence: int
    slice_line_id: int  # 1-based within the case slice
    timestamp: int  # adapter-defined integer (epoch or composed yymmdd*1e6 + hhmmss)
    component: str
    component_precedence: int
    role: str


def build_timeline(adapter, case_slice_lines: list[str], anomaly_line_ids: list[int]) -> list[TimelineEvent]:
    """Order the anomaly lines and tag roles.

    `adapter` must implement `parse_event(line: str) -> dict` returning
    {timestamp: int, component: str, level: str}. The adapter also
    provides `component_precedence(component: str) -> int` (lower = earlier
    in causal chain).
    """
    events: list[tuple[int, str, int, int]] = []  # (timestamp, component, precedence, slice_line_id)
    for line_id in anomaly_line_ids:
        idx = line_id - 1
        if not (0 <= idx < len(case_slice_lines)):
            continue
        parsed = adapter.parse_event(case_slice_lines[idx])
        if parsed is None:
            continue
        ts = parsed.get("timestamp", 0)
        comp = parsed.get("component", "unknown")
        prec = adapter.component_precedence(comp)
        events.append((ts, comp, prec, line_id))

    # Sort by (timestamp asc, precedence asc, line_id asc — natural file order tiebreak)
    events.sort(key=lambda e: (e[0], e[2], e[3]))

    if not events:
        return []

    # Role assignment:
    #   sequence 0 = trigger
    #   same component as trigger = propagation
    #   different component = consequence
    trigger_component = events[0][1]
    timeline: list[TimelineEvent] = []
    for seq, (ts, comp, prec, line_id) in enumerate(events):
        if seq == 0:
            role = TRIGGER_ROLE
        elif comp == trigger_component:
            role = PROPAGATION_ROLE
        else:
            role = CONSEQUENCE_ROLE
        timeline.append(TimelineEvent(
            sequence=seq,
            slice_line_id=line_id,
            timestamp=ts,
            component=comp,
            component_precedence=prec,
            role=role,
        ))
    return timeline


def kendall_tau(ground_truth_order: list[int], predicted_order: list[int]) -> float:
    """Kendall tau over the items present in BOTH lists.

    Both lists are sequences of slice-line ids in their respective orderings.
    Items only in one list are ignored (we measure on the overlap). Returns
    a value in [-1, 1]; 1 = perfect agreement, -1 = perfect reversal.
    """
    common = set(ground_truth_order) & set(predicted_order)
    if len(common) < 2:
        return 1.0  # degenerate — no comparable pairs
    gt_filtered = [x for x in ground_truth_order if x in common]
    pr_filtered = [x for x in predicted_order if x in common]
    gt_rank = {x: i for i, x in enumerate(gt_filtered)}
    pr_rank = {x: i for i, x in enumerate(pr_filtered)}

    items = list(common)
    n = len(items)
    concordant = 0
    discordant = 0
    for i in range(n):
        for j in range(i + 1, n):
            a, b = items[i], items[j]
            d_gt = gt_rank[a] - gt_rank[b]
            d_pr = pr_rank[a] - pr_rank[b]
            if d_gt * d_pr > 0:
                concordant += 1
            elif d_gt * d_pr < 0:
                discordant += 1
    total = concordant + discordant
    if total == 0:
        return 1.0
    return (concordant - discordant) / total
