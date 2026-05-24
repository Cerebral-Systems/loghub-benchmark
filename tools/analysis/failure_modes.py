"""Classify pytest assertion failures from Harbor trial dirs.

The verifier emits ctrf.json with per-test status + trace text. This
module reads those, groups failed assertions into stable "failure mode"
buckets, and emits a histogram. Buckets are matched in priority order;
the first match wins.

Bucket taxonomy (covers fp/sev/seq/corr/tmpl/v3-remediation answers):

  - missing_answer:        /app/answer.json wasn't written
  - schema_mismatch:       wrong schema_version or missing top-level field
  - wrong_is_incident:     test_is_incident_* failed
  - hallucinated_evidence: cited file or line doesn't exist in /app
  - snippet_not_verbatim:  evidence snippet doesn't match the cited line
  - wrong_root_cause:      root_cause_type mismatch
  - wrong_severity:        severity or justification mismatch
  - wrong_root_component:  root_component mismatch
  - wrong_trigger:         seq trigger location mismatch
  - bad_chain_topology:    causal_chain structural / acyclicity failure
  - missing_chain_edge:    causal_chain_edge_correctness failed
  - wrong_mitigation:      mitigation.action or .target mismatch
  - unsafe_mitigation:     mitigation in unsafe_actions enum
  - bad_post_state:        post-mitigation health doesn't match expected
  - low_grouping_score:    tmpl Rand index below threshold
  - other:                 fallback for unmatched traces

Each bucket carries the first 2 trial+test_name samples for context.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


# Each tuple: (bucket_name, regex_pattern_against_trace)
# Order matters — first hit wins.
RULES: list[tuple[str, re.Pattern[str]]] = [
    ("missing_answer", re.compile(r"missing /app/answer\.json|agent did not write")),
    ("schema_mismatch", re.compile(r"schema_version mismatch|answer missing required field")),
    ("wrong_is_incident", re.compile(r"is_incident|discrimination test")),
    ("hallucinated_evidence", re.compile(r"references unknown file|out of range")),
    ("snippet_not_verbatim", re.compile(r"snippet .* not (?:present|verbatim)")),
    ("wrong_root_component", re.compile(r"root_component (?:mismatch|.* !=)")),
    ("wrong_root_cause", re.compile(r"root_cause_type mismatch|root_cause_type .* != ")),
    ("wrong_severity", re.compile(r"severity mismatch|justification")),
    ("wrong_trigger", re.compile(r"trigger mismatch|non-trigger event.*precedes")),
    ("missing_chain_edge", re.compile(r"causal chain missing edges|chain missing ground-truth")),
    ("bad_chain_topology", re.compile(r"caused_by_step|first step must|cycle detected|chain must")),
    ("wrong_mitigation", re.compile(r"mitigation\.(action|target) mismatch")),
    ("unsafe_mitigation", re.compile(r"unsafe enum|unsafe_actions")),
    ("bad_post_state", re.compile(r"check_health reports|expected (?:healthy|degraded)|not escalated")),
    ("low_grouping_score", re.compile(r"Rand index|Kendall tau")),
]


@dataclass(frozen=True)
class FailureRow:
    trial_id: str
    task_slug: str
    test_name: str
    bucket: str
    trace_excerpt: str


def _classify(trace: str) -> str:
    for bucket, pattern in RULES:
        if pattern.search(trace):
            return bucket
    return "other"


def _trial_slug_from_dir(trial_dir: Path) -> tuple[str, str]:
    name = trial_dir.name
    if "__" in name:
        slug, tid = name.rsplit("__", 1)
        return slug, tid
    return name, "0"


def _scan_trial(trial_dir: Path) -> list[FailureRow]:
    ctrf = trial_dir / "verifier" / "ctrf.json"
    if not ctrf.is_file():
        return []
    try:
        data = json.loads(ctrf.read_text())
    except json.JSONDecodeError:
        return []
    slug, tid = _trial_slug_from_dir(trial_dir)
    out: list[FailureRow] = []
    for test in data.get("results", {}).get("tests", []):
        if test.get("status") != "failed":
            continue
        trace = test.get("trace") or test.get("message") or ""
        out.append(
            FailureRow(
                trial_id=tid,
                task_slug=slug,
                test_name=test.get("name", "?"),
                bucket=_classify(trace),
                trace_excerpt=trace[:400],
            )
        )
    return out


def scan(run_dir: Path) -> list[FailureRow]:
    rows: list[FailureRow] = []
    for child in sorted(run_dir.iterdir()):
        if child.is_dir() and (child / "verifier").is_dir():
            rows.extend(_scan_trial(child))
    return rows


def histogram(rows: list[FailureRow]) -> dict[str, dict]:
    bucket_to_rows: dict[str, list[FailureRow]] = defaultdict(list)
    for r in rows:
        bucket_to_rows[r.bucket].append(r)
    out: dict[str, dict] = {}
    for bucket, rs in sorted(bucket_to_rows.items(), key=lambda kv: -len(kv[1])):
        out[bucket] = {
            "count": len(rs),
            "fraction": round(len(rs) / len(rows), 4) if rows else 0.0,
            "samples": [
                {"trial": r.trial_id, "task": r.task_slug, "test": r.test_name}
                for r in rs[:2]
            ],
        }
    return out


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--run-dir", type=Path, required=True,
                   help="Harbor run directory with trial subdirs.")
    p.add_argument("--out", type=Path, default=None, help="Write JSON histogram here.")
    args = p.parse_args(argv)

    rows = scan(args.run_dir)
    hist = histogram(rows)
    print(json.dumps({"n_failures": len(rows), "by_bucket": hist}, indent=2))
    if args.out:
        args.out.write_text(
            json.dumps({"n_failures": len(rows), "by_bucket": hist}, indent=2, sort_keys=True) + "\n"
        )


if __name__ == "__main__":
    main()
