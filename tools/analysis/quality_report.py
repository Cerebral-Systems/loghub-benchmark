"""Render a Markdown quality report from Harbor run directories.

Combines summarize_runs (per-task / per-eval reward stats) with
failure_modes (assertion-bucket histogram) into one report. Also slices
by task family prefix (anomaly / fp / sev / seq / corr / tmpl / rem)
and per-dataset (hdfs / hadoop / bgl / thunderbird / openstack) so it's
easy to see where the agent under-performs.

Usage:
    python -m tools.analysis.quality_report \\
        --run-dir /path/to/harbor/run \\
        --out docs/quality-report.md
"""

from __future__ import annotations

import argparse
import statistics
from collections import defaultdict
from pathlib import Path

from . import failure_modes as fm
from . import summarize_runs as sr


FAMILY_PREFIXES = ("anomaly", "fp", "sev", "seq", "corr", "tmpl", "rem")
DATASET_PREFIXES = ("hdfs", "hadoop", "bgl", "thunderbird", "openstack")


def _family(slug: str) -> str:
    head = slug.split("-", 1)[0]
    if head in {"fp", "sev", "seq", "corr", "tmpl", "rem"}:
        return head
    return "anomaly"


def _dataset(slug: str) -> str:
    parts = slug.split("-")
    head = parts[1] if parts[0] in {"fp", "sev", "seq", "corr", "tmpl", "rem"} else parts[0]
    return head if head in DATASET_PREFIXES else "other"


def _format_table(rows: list[dict], headers: list[str]) -> str:
    if not rows:
        return "_(no rows)_\n"
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(h, "")) for h in headers) + " |")
    return "\n".join(lines) + "\n"


def _aggregate_slice(trials: list[sr.Trial], key_fn) -> list[dict]:
    groups: dict[str, list[float]] = defaultdict(list)
    for t in trials:
        groups[key_fn(t.task_slug)].append(t.reward)
    rows: list[dict] = []
    for key, rewards in sorted(groups.items()):
        rows.append(
            {
                "key": key,
                "n_trials": len(rewards),
                "mean_reward": round(statistics.mean(rewards), 4),
                "median_reward": round(statistics.median(rewards), 4),
                "pass_at_1": round(sum(1 for r in rewards if r > 0) / len(rewards), 4),
                "full_solve_rate": round(
                    sum(1 for r in rewards if r >= 0.999) / len(rewards), 4
                ),
            }
        )
    return rows


def build_report(run_dirs: list[Path], title: str = "Loghub-SRE Quality Report") -> str:
    all_trials: list[sr.Trial] = []
    for rd in run_dirs:
        all_trials.extend(sr._collect_run_dir(rd))

    if not all_trials:
        return f"# {title}\n\nNo trials found under: {', '.join(str(r) for r in run_dirs)}\n"

    rewards = [t.reward for t in all_trials]
    overall = {
        "n_trials": len(all_trials),
        "mean": round(statistics.mean(rewards), 4),
        "median": round(statistics.median(rewards), 4),
        "pass_at_1": round(sum(1 for r in rewards if r > 0) / len(rewards), 4),
        "full_solve_rate": round(
            sum(1 for r in rewards if r >= 0.999) / len(rewards), 4
        ),
        "min": round(min(rewards), 4),
        "max": round(max(rewards), 4),
    }

    by_family = _aggregate_slice(all_trials, _family)
    by_dataset = _aggregate_slice(all_trials, _dataset)
    per_task = sr.aggregate(all_trials)

    # Failure modes across all run dirs.
    failure_rows: list[fm.FailureRow] = []
    for rd in run_dirs:
        failure_rows.extend(fm.scan(rd))
    fhist = fm.histogram(failure_rows)
    fhist_rows = [
        {"bucket": k, "count": v["count"], "fraction": v["fraction"]}
        for k, v in fhist.items()
    ]

    out = [f"# {title}", ""]
    out.append("## Overall")
    out.append("")
    out.append(_format_table([overall], list(overall.keys())))
    out.append("")
    out.append("## Per family")
    out.append("")
    out.append(_format_table(by_family, ["key", "n_trials", "mean_reward", "median_reward", "pass_at_1", "full_solve_rate"]))
    out.append("")
    out.append("## Per dataset")
    out.append("")
    out.append(_format_table(by_dataset, ["key", "n_trials", "mean_reward", "median_reward", "pass_at_1", "full_solve_rate"]))
    out.append("")
    out.append("## Failure modes")
    out.append("")
    out.append(f"Total failed assertions: **{len(failure_rows)}**")
    out.append("")
    out.append(_format_table(fhist_rows, ["bucket", "count", "fraction"]))
    out.append("")
    out.append("## Per task (top 20 by mean reward, ascending)")
    out.append("")
    sorted_tasks = sorted(per_task, key=lambda r: r["mean_reward"])[:20]
    out.append(
        _format_table(
            sorted_tasks,
            ["task_slug", "eval_name", "n_trials", "mean_reward", "pass_at_1", "full_solve_rate"],
        )
    )
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--run-dir", action="append", type=Path, required=True)
    p.add_argument("--out", type=Path, default=Path("quality-report.md"))
    p.add_argument("--title", default="Loghub-SRE Quality Report")
    args = p.parse_args(argv)
    text = build_report(args.run_dir, title=args.title)
    args.out.write_text(text)
    print(f"wrote {args.out} ({len(text):,} bytes)")


if __name__ == "__main__":
    main()
