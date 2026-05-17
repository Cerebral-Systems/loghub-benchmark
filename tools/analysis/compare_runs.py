#!/usr/bin/env python3
"""Compare a single-attempt baseline run against a multi-attempt Mesh-ensemble run.

Reads two Harbor job directories. For each task, computes:
  - baseline_reward: reward.txt from the single baseline attempt
  - mesh_ensemble_reward: max(reward.txt across all 3 mesh attempts)
  - lift: mesh - baseline

Outputs a markdown summary suitable for docs/MESH_BENCHMARK_RESULTS.md.

Usage:
    python compare_runs.py BASELINE_JOB_DIR MESH_JOB_DIR > docs/MESH_BENCHMARK_RESULTS.md
"""
import json
import sys
import re
from pathlib import Path
from collections import defaultdict


def load_trial_rewards(job_dir: Path) -> dict[str, list[float]]:
    """Map task_slug -> list of rewards (one per trial attempt)."""
    rewards: dict[str, list[float]] = defaultdict(list)
    for trial_dir in job_dir.iterdir():
        if not trial_dir.is_dir():
            continue
        # Trial dir names look like: <slug>__<random>
        m = re.match(r"^(.+)__[A-Za-z0-9]+$", trial_dir.name)
        if not m:
            continue
        slug = m.group(1)
        reward_file = trial_dir / "verifier" / "reward.txt"
        if reward_file.exists():
            try:
                v = float(reward_file.read_text().strip())
                rewards[slug].append(v)
            except (ValueError, OSError):
                pass
    return dict(rewards)


def dataset_of(slug: str) -> str:
    # Slug shape: <dataset>-<root-cause>-<id>
    return slug.split("-", 1)[0]


def render_report(baseline: dict[str, list[float]], mesh: dict[str, list[float]]) -> str:
    all_slugs = sorted(set(baseline) | set(mesh))
    if not all_slugs:
        return "# No data\n"

    rows = []
    for slug in all_slugs:
        b = baseline.get(slug, [])
        m = mesh.get(slug, [])
        baseline_score = b[0] if b else None
        mesh_score = max(m) if m else None
        lift = (mesh_score - baseline_score) if (mesh_score is not None and baseline_score is not None) else None
        rows.append({
            "slug": slug,
            "dataset": dataset_of(slug),
            "baseline": baseline_score,
            "mesh_best": mesh_score,
            "mesh_attempts": len(m),
            "lift": lift,
        })

    # Headlines
    completed = [r for r in rows if r["baseline"] is not None and r["mesh_best"] is not None]
    baseline_mean = sum(r["baseline"] for r in completed) / len(completed) if completed else 0
    mesh_mean = sum(r["mesh_best"] for r in completed) / len(completed) if completed else 0
    lift_mean = mesh_mean - baseline_mean
    n_mesh_wins = sum(1 for r in completed if r["lift"] is not None and r["lift"] > 0)
    n_ties = sum(1 for r in completed if r["lift"] == 0)
    n_baseline_wins = sum(1 for r in completed if r["lift"] is not None and r["lift"] < 0)
    n_fully_solved_baseline = sum(1 for r in completed if r["baseline"] == 1.0)
    n_fully_solved_mesh = sum(1 for r in completed if r["mesh_best"] == 1.0)

    out = []
    out.append("# Mesh Ensemble vs Baseline on Loghub-SRE-v1\n")
    out.append("## Headline numbers\n")
    out.append(f"- **Tasks evaluated**: {len(completed)} of {len(all_slugs)}")
    out.append(f"- **Single-agent baseline mean reward**: {baseline_mean:.3f}")
    out.append(f"- **Mesh ensemble mean reward** (best-of-3): {mesh_mean:.3f}")
    out.append(f"- **Mesh lift**: +{lift_mean:.3f} ({100*lift_mean/baseline_mean:+.1f}% relative)" if baseline_mean else "")
    out.append(f"- **Tasks where Mesh > baseline**: {n_mesh_wins}/{len(completed)}")
    out.append(f"- **Tasks where Mesh = baseline (tie)**: {n_ties}/{len(completed)}")
    out.append(f"- **Tasks where Mesh < baseline**: {n_baseline_wins}/{len(completed)}  (sampling noise within ensemble — Mesh is best-of-N so theoretical floor = baseline)")
    out.append(f"- **Tasks fully solved (reward=1.0)**: baseline {n_fully_solved_baseline} | Mesh {n_fully_solved_mesh}\n")

    # Per-dataset breakdown
    by_ds = defaultdict(list)
    for r in completed:
        by_ds[r["dataset"]].append(r)
    out.append("## Per-dataset breakdown\n")
    out.append("| Dataset | N | Baseline mean | Mesh mean | Lift |")
    out.append("|---|---|---|---|---|")
    for ds, rs in sorted(by_ds.items()):
        b = sum(r["baseline"] for r in rs) / len(rs)
        m = sum(r["mesh_best"] for r in rs) / len(rs)
        out.append(f"| {ds} | {len(rs)} | {b:.3f} | {m:.3f} | +{m-b:.3f} |")
    out.append("")

    # Per-task table
    out.append("## Per-task scores\n")
    out.append("| Task | Dataset | Baseline | Mesh (best-of-N) | N attempts | Lift |")
    out.append("|---|---|---|---|---|---|")
    for r in sorted(rows, key=lambda r: -((r["lift"] or 0))):
        b = f"{r['baseline']:.3f}" if r["baseline"] is not None else "—"
        m = f"{r['mesh_best']:.3f}" if r["mesh_best"] is not None else "—"
        l = f"+{r['lift']:.3f}" if r["lift"] is not None else "—"
        out.append(f"| `{r['slug']}` | {r['dataset']} | {b} | {m} | {r['mesh_attempts']} | {l} |")

    return "\n".join(out) + "\n"


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    baseline_dir = Path(sys.argv[1])
    mesh_dir = Path(sys.argv[2])
    print(render_report(load_trial_rewards(baseline_dir), load_trial_rewards(mesh_dir)))
