"""Build an exact-field failure report for Loghub-SRE Harbor runs.

The older ``failure_modes`` helper classifies failures from assertion text.
That is useful for a quick histogram, but many Loghub assertions include
overlapping words, so broad regex buckets can be misleading. This report uses
stable verifier test names first, then augments them with answer-vs-expected
diffs and optional baseline deltas.
"""

from __future__ import annotations

import argparse
import json
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


FAMILY_PREFIXES = ("rem-", "seq-", "corr-", "sev-", "tmpl-", "fp-")

TEST_CATEGORY_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("schema_or_missing_answer", ("answer_is_valid_json", "schema_version", "answer_schema", "required_field")),
    ("incident_discrimination", ("is_incident", "no_incident", "incident_true")),
    ("root_cause_enum", ("root_cause", "inline_label_evidence_matches_root_cause")),
    ("evidence_file_or_line", ("evidence_within_ground_truth", "no_cross_file_line_confusion", "evidence_lines_in_range", "evidence_real", "evidence_present", "minimum_evidence_count")),
    ("evidence_snippet", ("snippet", "snippets_match")),
    ("sequence_trigger_or_order", ("trigger_role", "timeline", "kendall", "precedes")),
    ("causal_chain", ("causal_chain", "chain_edge")),
    ("root_component", ("root_component",)),
    ("severity", ("severity", "justification")),
    ("template_grouping", ("template", "grouping", "unique_templates")),
    ("false_positive_indicators", ("indicator", "classification")),
    ("mitigation", ("mitigation",)),
    ("post_state", ("post_mitigation", "postcheck", "check_health")),
)


@dataclass(frozen=True)
class TrialReport:
    task_slug: str
    family: str
    dataset: str
    trial_dir: str
    reward: float
    failed_tests: list[str]
    failure_categories: list[str]
    field_diff: dict[str, Any]
    baseline_reward: float | None = None
    reward_delta: float | None = None


def family_for_slug(slug: str) -> str:
    for prefix in FAMILY_PREFIXES:
        if slug.startswith(prefix):
            return prefix[:-1]
    return "v1"


def dataset_for_slug(slug: str) -> str:
    trimmed = slug
    for prefix in FAMILY_PREFIXES:
        if trimmed.startswith(prefix):
            trimmed = trimmed[len(prefix):]
            break
    return trimmed.split("-", 1)[0]


def collect_reports(
    run_dir: Path,
    *,
    tasks_dir: Path = Path("tasks"),
    baseline_run_dir: Path | None = None,
) -> list[TrialReport]:
    baseline = _collect_rewards(baseline_run_dir) if baseline_run_dir else {}
    rows: list[TrialReport] = []
    for trial_dir in sorted(run_dir.iterdir()):
        if not trial_dir.is_dir() or "__" not in trial_dir.name:
            continue
        slug = trial_dir.name.rsplit("__", 1)[0]
        reward = _read_reward(trial_dir)
        if reward is None:
            continue
        failed_tests = _failed_test_names(trial_dir)
        expected = _load_json(tasks_dir / slug / "tests" / "expected.json")
        answer = _load_json(_answer_path(trial_dir)) if _answer_path(trial_dir) else {}
        base_reward = baseline.get(slug)
        rows.append(
            TrialReport(
                task_slug=slug,
                family=family_for_slug(slug),
                dataset=dataset_for_slug(slug),
                trial_dir=str(trial_dir),
                reward=reward,
                failed_tests=failed_tests,
                failure_categories=sorted({_category_for_test(name) for name in failed_tests}),
                field_diff=diff_answer(answer, expected),
                baseline_reward=base_reward,
                reward_delta=round(reward - base_reward, 6) if base_reward is not None else None,
            )
        )
    return rows


def summarize(rows: list[TrialReport]) -> dict[str, Any]:
    rewards = [row.reward for row in rows]
    summary: dict[str, Any] = {
        "n_trials": len(rows),
        "mean_reward": round(statistics.mean(rewards), 6) if rewards else 0.0,
        "median_reward": round(statistics.median(rewards), 6) if rewards else 0.0,
        "full_solves": sum(1 for row in rows if row.reward >= 0.999),
        "zero_scores": sum(1 for row in rows if row.reward == 0.0),
        "by_family": _group_summary(rows, "family"),
        "by_dataset": _group_summary(rows, "dataset"),
        "failed_tests": dict(Counter(test for row in rows for test in row.failed_tests).most_common()),
        "failure_categories": dict(Counter(cat for row in rows for cat in row.failure_categories).most_common()),
        "field_mismatches": _field_mismatch_summary(rows),
    }
    comparable = [row for row in rows if row.reward_delta is not None]
    if comparable:
        deltas = [row.reward_delta for row in comparable if row.reward_delta is not None]
        summary["baseline_comparison"] = {
            "n_overlap": len(comparable),
            "mean_delta": round(statistics.mean(deltas), 6),
            "improved": sum(1 for delta in deltas if delta > 0),
            "regressed": sum(1 for delta in deltas if delta < 0),
            "same": sum(1 for delta in deltas if delta == 0),
            "top_regressions": [
                _row_brief(row)
                for row in sorted(comparable, key=lambda item: item.reward_delta or 0)[:12]
                if (row.reward_delta or 0) < 0
            ],
            "top_improvements": [
                _row_brief(row)
                for row in sorted(comparable, key=lambda item: item.reward_delta or 0, reverse=True)[:12]
                if (row.reward_delta or 0) > 0
            ],
        }
    return summary


def diff_answer(answer: dict[str, Any], expected: dict[str, Any]) -> dict[str, Any]:
    fields: dict[str, Any] = {}

    def scalar(key: str) -> None:
        if key in expected:
            fields[key] = _cmp(answer.get(key), expected.get(key))

    for key in ("schema_version", "is_incident", "root_cause_type", "root_component", "severity", "severity_justification"):
        scalar(key)

    if isinstance(expected.get("mitigation"), dict):
        mitigation = answer.get("mitigation") if isinstance(answer.get("mitigation"), dict) else {}
        for subkey in ("action", "target"):
            fields[f"mitigation.{subkey}"] = _cmp(mitigation.get(subkey), expected["mitigation"].get(subkey))

    if "expected_health" in expected:
        postcheck = answer.get("postcheck") if isinstance(answer.get("postcheck"), dict) else {}
        fields["postcheck.health_status"] = _cmp(postcheck.get("health_status"), expected["expected_health"])

    if isinstance(expected.get("evidence"), list):
        fields["evidence_exact"] = _set_overlap(_evidence_pairs(answer.get("evidence")), _expected_pairs(expected.get("evidence")))
    if isinstance(expected.get("false_positive_indicators"), list):
        fields["false_positive_indicators"] = _set_overlap(
            _evidence_pairs(answer.get("false_positive_indicators")),
            _expected_pairs(expected.get("false_positive_indicators")),
        )
    if isinstance(expected.get("causal_chain"), list):
        fields["causal_chain_components"] = _set_overlap(
            {(item.get("component"), None) for item in answer.get("causal_chain", []) if isinstance(item, dict)},
            {(item.get("component"), None) for item in expected.get("causal_chain", []) if isinstance(item, dict)},
        )
    if isinstance(expected.get("timeline"), list):
        actual = [
            (item.get("file"), item.get("line"))
            for item in sorted(answer.get("timeline", []) or [], key=lambda item: item.get("sequence", 0))
            if isinstance(item, dict)
        ]
        expected_order = [(item.get("file"), item.get("line")) for item in expected.get("timeline", []) if isinstance(item, dict)]
        fields["timeline_order"] = {
            "match": actual == expected_order,
            "actual_len": len(actual),
            "expected_len": len(expected_order),
            "prefix_match_len": _prefix_match_len(actual, expected_order),
        }
    if isinstance(expected.get("templates"), list) or "total_unique_templates" in expected:
        fields["total_unique_templates"] = _cmp(answer.get("total_unique_templates"), expected.get("total_unique_templates"))

    return {"fields": fields, "mismatches": sorted(name for name, result in fields.items() if result.get("match") is False)}


def _group_summary(rows: list[TrialReport], attr: str) -> dict[str, Any]:
    groups: dict[str, list[TrialReport]] = defaultdict(list)
    for row in rows:
        groups[getattr(row, attr)].append(row)
    out: dict[str, Any] = {}
    for key, group in sorted(groups.items()):
        rewards = [row.reward for row in group]
        out[key] = {
            "n": len(group),
            "mean_reward": round(statistics.mean(rewards), 6),
            "full_solves": sum(1 for row in group if row.reward >= 0.999),
            "top_failed_tests": dict(Counter(test for row in group for test in row.failed_tests).most_common(8)),
            "top_categories": dict(Counter(cat for row in group for cat in row.failure_categories).most_common(8)),
        }
    return out


def _field_mismatch_summary(rows: list[TrialReport]) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for row in rows:
        counter.update(row.field_diff.get("mismatches", []))
    return dict(counter.most_common())


def _row_brief(row: TrialReport) -> dict[str, Any]:
    return {
        "task": row.task_slug,
        "family": row.family,
        "dataset": row.dataset,
        "reward": row.reward,
        "baseline_reward": row.baseline_reward,
        "delta": row.reward_delta,
        "failed_tests": row.failed_tests[:8],
        "mismatches": row.field_diff.get("mismatches", [])[:8],
    }


def _collect_rewards(run_dir: Path | None) -> dict[str, float]:
    if run_dir is None:
        return {}
    rewards: dict[str, float] = {}
    for trial_dir in run_dir.iterdir():
        if not trial_dir.is_dir() or "__" not in trial_dir.name:
            continue
        reward = _read_reward(trial_dir)
        if reward is not None:
            rewards[trial_dir.name.rsplit("__", 1)[0]] = reward
    return rewards


def _read_reward(trial_dir: Path) -> float | None:
    reward_path = trial_dir / "verifier" / "reward.txt"
    if reward_path.is_file():
        try:
            return float(reward_path.read_text().strip())
        except ValueError:
            return None
    result_path = trial_dir / "result.json"
    if result_path.is_file():
        try:
            result = json.loads(result_path.read_text())
        except json.JSONDecodeError:
            return None
        reward = ((result.get("verifier_result") or {}).get("rewards") or {}).get("reward")
        return float(reward) if isinstance(reward, (int, float)) else None
    return None


def _failed_test_names(trial_dir: Path) -> list[str]:
    ctrf_path = trial_dir / "verifier" / "ctrf.json"
    if not ctrf_path.is_file():
        return []
    try:
        data = json.loads(ctrf_path.read_text())
    except json.JSONDecodeError:
        return []
    out: list[str] = []
    for test in data.get("results", {}).get("tests", []):
        if test.get("status") == "failed":
            out.append(str(test.get("name") or "?").split("::")[-1])
    return out


def _category_for_test(test_name: str) -> str:
    lowered = test_name.lower()
    for category, needles in TEST_CATEGORY_RULES:
        if any(needle in lowered for needle in needles):
            return category
    return "other"


def _load_json(path: Path | None) -> dict[str, Any]:
    if path is None or not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text())
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def _answer_path(trial_dir: Path) -> Path | None:
    for candidate in (
        trial_dir / "artifacts" / "answer.json",
        trial_dir / "agent" / "answer.json",
        trial_dir / "answer.json",
    ):
        if candidate.is_file():
            return candidate
    return None


def _cmp(actual: Any, expected: Any) -> dict[str, Any]:
    return {"actual": actual, "expected": expected, "match": actual == expected}


def _expected_pairs(entries: Any) -> set[tuple[str, int]]:
    out: set[tuple[str, int]] = set()
    for item in entries or []:
        if isinstance(item, dict) and isinstance(item.get("file"), str) and isinstance(item.get("line"), int):
            out.add((item["file"], item["line"]))
    return out


def _evidence_pairs(entries: Any) -> set[tuple[str, int]]:
    out: set[tuple[str, int]] = set()
    for item in entries or []:
        if not isinstance(item, dict):
            continue
        line = item.get("line", item.get("evidence_line"))
        if isinstance(item.get("file"), str) and isinstance(line, int):
            out.add((item["file"], line))
    return out


def _set_overlap(actual: set[tuple[Any, Any]], expected: set[tuple[Any, Any]]) -> dict[str, Any]:
    overlap = actual & expected
    return {
        "match": bool(expected) and expected.issubset(actual),
        "actual_count": len(actual),
        "expected_count": len(expected),
        "overlap_count": len(overlap),
        "recall": round(len(overlap) / len(expected), 4) if expected else 1.0,
        "precision": round(len(overlap) / len(actual), 4) if actual else 1.0,
    }


def _prefix_match_len(actual: list[tuple[Any, Any]], expected: list[tuple[Any, Any]]) -> int:
    count = 0
    for left, right in zip(actual, expected, strict=False):
        if left != right:
            break
        count += 1
    return count


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--tasks-dir", type=Path, default=Path("tasks"))
    parser.add_argument("--baseline-run-dir", type=Path, default=None)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--rows-out", type=Path, default=None)
    args = parser.parse_args(argv)
    if not args.run_dir.is_dir():
        parser.error(f"--run-dir does not exist or is not a directory: {args.run_dir}")
    if not args.tasks_dir.is_dir():
        parser.error(f"--tasks-dir does not exist or is not a directory: {args.tasks_dir}")
    if args.baseline_run_dir is not None and not args.baseline_run_dir.is_dir():
        parser.error(f"--baseline-run-dir does not exist or is not a directory: {args.baseline_run_dir}")

    rows = collect_reports(args.run_dir, tasks_dir=args.tasks_dir, baseline_run_dir=args.baseline_run_dir)
    payload = {"summary": summarize(rows), "rows": [_row_brief(row) for row in rows]}
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.write_text(text)
    else:
        print(text)
    if args.rows_out:
        args.rows_out.write_text(json.dumps([row.__dict__ for row in rows], indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
