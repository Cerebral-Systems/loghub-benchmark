"""Shared classifier for false-positive indicator lines.

FP windows contain scary-but-benign log lines. Each indicator is
tagged with one of five `why_not_anomalous` categories so the `fp`
verifier can check both *which* lines the agent flags and *why*.

Categories (must match the enum in the v2-fp answer schema):
  - rate_limit_warning
  - recoverable_retry
  - benign_info
  - expected_event
  - transient_state
"""

from __future__ import annotations

import re

WHY_NOT_ANOMALOUS = (
    "rate_limit_warning",
    "recoverable_retry",
    "benign_info",
    "expected_event",
    "transient_state",
)

# Order matters: first match wins, so more-specific patterns precede the
# generic "benign_info" catch-all. Each entry is (regex, category).
_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"throttl|rate.?limit|exceeded.*quota|too many requests|backoff", re.I), "rate_limit_warning"),
    (re.compile(r"retry.*succe|retried|retrying.*after|reconnect.*succe|recovered.*after", re.I), "recoverable_retry"),
    (re.compile(r"scheduled|periodic|cron|cleanup|gc\b|garbage[\s_-]?collect|checkpoint|heartbeat|verification|delete|deleted|expired", re.I), "expected_event"),
    (re.compile(r"warn|temporary|transient|temporarily|drain|preparing|pending|redundant|duplicate", re.I), "transient_state"),
    # Note: "error|fail" without preceding "FATAL" or "ERROR" level marker is
    # often benign text inside an INFO log line ("parity error corrected",
    # "task failed to acquire lock, will retry").
    (re.compile(r"\b(corrected|recovered|ignored|skipped|will retry|will be retried)\b", re.I), "benign_info"),
)


def classify_fp_line(line: str) -> str:
    """Return the why_not_anomalous category for a benign-noise line.

    Falls back to `benign_info` if no specific pattern matches. The
    intent is for every line passed in to *already* look scary (caller
    pre-filtered on `error|warn|fail|throttle|retry` substrings) — this
    function only refines the category.
    """
    for pattern, label in _PATTERNS:
        if pattern.search(line):
            return label
    return "benign_info"


# Regex used by adapters to spot "scary but possibly benign" lines in a
# normal-only window. The exporter and adapters both reference this so
# the criterion stays in one place. The broader set includes "verification"
# and "redundant"-style ops phrases because a hyperalert agent might flag
# those — testing that the agent correctly recognizes them as benign IS
# the point of T1 (false-positive triage).
SCARY_LINE_RE = re.compile(
    r"(?:error|warn|fail|except|retry|throttl|timeout|drop|reset|"
    r"corrupt|denied|refused|abort|terminate|"
    r"verification|redundant|duplicate|expired|deleted)",
    re.I,
)


def is_scary_line(line: str) -> bool:
    return bool(SCARY_LINE_RE.search(line))
