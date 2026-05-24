"""Aggregate one or more Harbor result directories into a per-task / per-eval table.

A "Harbor result directory" is anything produced by `harbor run`: typically
a top-level result.json plus one trial dir per task with its own
result.json + verifier/ subtree. This tool walks one or more such roots,
groups trials by (task_slug, eval_name), and emits a CSV/Markdown table
with mean reward, median reward, pass@1, full-solve rate, SEM, and trial
count.

Usage:
    python -m tools.analysis.summarize_runs \\
        --run-dir /path/to/harbor/results/2026-05-24__... \\
        --out summary.csv

Multiple --run-dir flags combine into one table (per-task aggregation
across runs); pass --by-run to keep them separated.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Trial:
    run_dir: str
    task_slug: str
    eval_name: str
    trial_id: str
    reward: float
    passed_tests: int | None
    total_tests: int | None


def _read_reward_from_verifier(verifier_dir: Path) -> float | None:
    reward_path = verifier_dir / "reward.txt"
    if reward_path.is_file():
        try:
            return float(reward_path.read_text().strip())
        except ValueError:
            return None
    return None


def _read_pass_counts(verifier_dir: Path) -> tuple[int | None, int | None]:
    ctrf_path = verifier_dir / "ctrf.json"
    if not ctrf_path.is_file():
        return None, None
    try:
        data = json.loads(ctrf_path.read_text())
    except json.JSONDecodeError:
        return None, None
    summary = data.get("results", {}).get("summary", {})
    return summary.get("passed"), summary.get("tests")


def _trial_slug_from_dir(trial_dir: Path) -> tuple[str, str]:
    """`<task_slug>__<trial_id>` => (task_slug, trial_id)."""
    name = trial_dir.name
    if "__" in name:
        slug, tid = name.rsplit("__", 1)
        return slug, tid
    return name, "0"


def _collect_run_dir(run_dir: Path) -> list[Trial]:
    """Walk a single Harbor run dir and yield Trial rows."""
    trials: list[Trial] = []
    top_result = run_dir / "result.json"
    eval_for_task: dict[str, str] = {}
    if top_result.is_file():
        try:
            top = json.loads(top_result.read_text())
        except json.JSONDecodeError:
            top = {}
        for eval_name, eval_block in top.get("stats", {}).get("evals", {}).items():
            for _reward, trial_ids in eval_block.get("reward_stats", {}).get("reward", {}).items():
                for tid in trial_ids:
                    eval_for_task[tid] = eval_name
    for trial_dir in sorted(run_dir.iterdir()):
        if not trial_dir.is_dir():
            continue
        if not (trial_dir / "result.json").is_file() and not (trial_dir / "verifier").is_dir():
            continue
        slug, tid = _trial_slug_from_dir(trial_dir)
        verifier_dir = trial_dir / "verifier"
        reward = _read_reward_from_verifier(verifier_dir) if verifier_dir.is_dir() else None
        passed, total = _read_pass_counts(verifier_dir) if verifier_dir.is_dir() else (None, None)
        if reward is None:
            # Fall back to per-trial result.json mean if reward.txt missing.
            res_path = trial_dir / "result.json"
            if res_path.is_file():
                try:
                    res = json.loads(res_path.read_text())
                except json.JSONDecodeError:
                    res = {}
                evals = res.get("stats", {}).get("evals", {})
                metrics = next(iter(evals.values()), {}).get("metrics", [])
                if metrics:
                    reward = metrics[0].get("mean")
        eval_name = eval_for_task.get(trial_dir.name) or eval_for_task.get(slug, "unknown")
        if reward is None:
            continue
        trials.append(
            Trial(
                run_dir=str(run_dir),
                task_slug=slug,
                eval_name=eval_name,
                trial_id=tid,
                reward=float(reward),
                passed_tests=passed,
                total_tests=total,
            )
        )
    return trials


def _sem(values: Iterable[float]) -> float:
    vals = list(values)
    if len(vals) < 2:
        return 0.0
    return statistics.stdev(vals) / math.sqrt(len(vals))


def aggregate(trials: list[Trial], *, by_run: bool = False) -> list[dict]:
    groups: dict[tuple, list[Trial]] = defaultdict(list)
    for t in trials:
        key = (t.run_dir, t.task_slug, t.eval_name) if by_run else (t.task_slug, t.eval_name)
        groups[key].append(t)
    rows: list[dict] = []
    for key, group in sorted(groups.items()):
        rewards = [t.reward for t in group]
        row: dict = {
            "task_slug": group[0].task_slug,
            "eval_name": group[0].eval_name,
            "n_trials": len(group),
            "mean_reward": round(statistics.mean(rewards), 4),
            "median_reward": round(statistics.median(rewards), 4),
            "pass_at_1": round(sum(1 for r in rewards if r > 0) / len(rewards), 4),
            "full_solve_rate": round(sum(1 for r in rewards if r >= 0.999) / len(rewards), 4),
            "sem": round(_sem(rewards), 4),
            "min_reward": round(min(rewards), 4),
            "max_reward": round(max(rewards), 4),
        }
        if by_run:
            row["run_dir"] = group[0].run_dir
        rows.append(row)
    return rows


def write_csv(rows: list[dict], out_path: Path) -> None:
    if not rows:
        out_path.write_text("")
        return
    field_order = list(rows[0].keys())
    with out_path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=field_order)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_markdown(rows: list[dict], out_path: Path) -> None:
    if not rows:
        out_path.write_text("(no rows)\n")
        return
    headers = list(rows[0].keys())
    md = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for row in rows:
        md.append("| " + " | ".join(str(row[h]) for h in headers) + " |")
    out_path.write_text("\n".join(md) + "\n")


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--run-dir", action="append", type=Path, required=True,
                   help="Harbor run directory; repeat for multiple runs.")
    p.add_argument("--out", type=Path, default=Path("summary.csv"))
    p.add_argument("--format", choices=("csv", "markdown"), default="csv")
    p.add_argument("--by-run", action="store_true",
                   help="Keep runs separate; otherwise pool trials across runs.")
    args = p.parse_args(argv)

    all_trials: list[Trial] = []
    for rd in args.run_dir:
        all_trials.extend(_collect_run_dir(rd))

    rows = aggregate(all_trials, by_run=args.by_run)
    if args.format == "csv":
        write_csv(rows, args.out)
    else:
        write_markdown(rows, args.out)
    print(f"summarized {len(all_trials)} trials -> {len(rows)} rows -> {args.out}")


if __name__ == "__main__":
    main()
