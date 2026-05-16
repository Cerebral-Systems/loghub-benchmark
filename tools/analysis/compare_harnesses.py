#!/usr/bin/env python3
"""Compare multiple Harbor agent harnesses on the same task set.

Reads N Harbor job directories. For each task, captures the reward from each
harness, plus the best-of-N as the "Mesh ensemble" score (faithful to
agent_mesh.py:_collect_attempts which selects the best successful attempt).

Emits a Mesh-branded markdown report with:
  - Headline: mean reward per harness + Mesh ensemble lift
  - Per-dataset breakdown
  - Per-task table (each harness as a column)

Usage:
    python compare_harnesses.py NAME1=DIR1 NAME2=DIR2 ... > docs/MESH_BENCHMARK.md

Example:
    python compare_harnesses.py \\
        mini-swe-agent=baselines/baseline-kimi-k2_6 \\
        hermes=baselines/hermes-kimi \\
        opencode=baselines/opencode-kimi \\
        > docs/MESH_BENCHMARK.md
"""
import re
import sys
from pathlib import Path
from collections import defaultdict


def load_rewards(job_dir: Path) -> dict[str, float]:
    """task_slug -> best reward across this harness's trial attempts."""
    rewards: dict[str, list[float]] = defaultdict(list)
    if not job_dir.is_dir():
        return {}
    for trial_dir in job_dir.iterdir():
        if not trial_dir.is_dir():
            continue
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
    return {slug: max(vs) for slug, vs in rewards.items() if vs}


def dataset_of(slug: str) -> str:
    return slug.split("-", 1)[0]


def render(harness_data: dict[str, dict[str, float]]) -> str:
    all_slugs = sorted(set().union(*(d.keys() for d in harness_data.values())))
    harness_names = list(harness_data.keys())

    # Per-task best-of-N (Mesh ensemble)
    mesh_scores = {}
    for slug in all_slugs:
        scores = [harness_data[h].get(slug) for h in harness_names if slug in harness_data[h]]
        if scores:
            mesh_scores[slug] = max(scores)

    # Headline stats per harness
    def mean(d: dict[str, float], slugs):
        vals = [d[s] for s in slugs if s in d]
        return sum(vals) / len(vals) if vals else 0.0

    fully_solved = {h: sum(1 for v in harness_data[h].values() if v == 1.0) for h in harness_names}
    completed_per_harness = {h: len(harness_data[h]) for h in harness_names}
    mesh_mean = sum(mesh_scores.values()) / len(mesh_scores) if mesh_scores else 0
    mesh_solved = sum(1 for v in mesh_scores.values() if v == 1.0)

    out = []
    out.append("# Mesh on Loghub-SRE-v1: Multi-Harness Comparison\n")
    out.append("Comparison of Harbor agent harnesses against the 60-task Loghub-SRE-v1 benchmark, with **Mesh** modeled as the best-of-N selector over the heterogeneous agent pool — faithful to `services/orchestrator/agent_mesh.py:_collect_attempts`.\n")

    out.append("## Headline numbers\n")
    out.append("| Harness | Tasks completed | Mean reward | Fully solved (=1.0) |")
    out.append("|---|---|---|---|")
    for h in harness_names:
        m = mean(harness_data[h], all_slugs)
        out.append(f"| {h} | {completed_per_harness[h]} | {m:.3f} | {fully_solved[h]} |")
    out.append(f"| **Mesh (best-of-{len(harness_names)})** | {len(mesh_scores)} | **{mesh_mean:.3f}** | **{mesh_solved}** |")
    out.append("")

    best_single = max((mean(harness_data[h], all_slugs) for h in harness_names), default=0)
    lift_abs = mesh_mean - best_single
    lift_pct = 100 * lift_abs / best_single if best_single else 0
    out.append(f"**Mesh ensemble lift over best single harness**: +{lift_abs:.3f} ({lift_pct:+.1f}%)\n")

    # Per-dataset breakdown
    by_ds = defaultdict(lambda: defaultdict(list))
    for slug in all_slugs:
        ds = dataset_of(slug)
        for h in harness_names:
            if slug in harness_data[h]:
                by_ds[ds][h].append(harness_data[h][slug])
        if slug in mesh_scores:
            by_ds[ds]["__mesh"].append(mesh_scores[slug])

    out.append("## Per-dataset breakdown\n")
    cols = harness_names + ["__mesh"]
    header = "| Dataset | N | " + " | ".join(f"{h}" if h != "__mesh" else "**Mesh**" for h in cols) + " |"
    sep = "|---|---|" + "|".join(["---"] * len(cols)) + "|"
    out.append(header)
    out.append(sep)
    for ds in sorted(by_ds.keys()):
        row_vals = [f"{sum(by_ds[ds][h])/len(by_ds[ds][h]):.3f}" if by_ds[ds][h] else "—" for h in cols]
        n_tasks = max((len(by_ds[ds][h]) for h in cols if by_ds[ds][h]), default=0)
        out.append(f"| {ds} | {n_tasks} | " + " | ".join(row_vals) + " |")
    out.append("")

    # Per-task scores
    out.append("## Per-task scores\n")
    header = "| Task | Dataset | " + " | ".join(harness_names) + " | **Mesh best-of-N** |"
    sep = "|---|---|" + "|".join(["---"] * (len(harness_names) + 1)) + "|"
    out.append(header)
    out.append(sep)
    for slug in all_slugs:
        ds = dataset_of(slug)
        cells = [f"{harness_data[h][slug]:.3f}" if slug in harness_data[h] else "—" for h in harness_names]
        mesh = f"{mesh_scores[slug]:.3f}" if slug in mesh_scores else "—"
        out.append(f"| `{slug}` | {ds} | " + " | ".join(cells) + f" | **{mesh}** |")
    out.append("")

    out.append("## Reproducing this experiment\n")
    out.append("```bash")
    out.append("export MOONSHOT_API_KEY=sk-...; export KIMI_API_KEY=$MOONSHOT_API_KEY")
    for h in harness_names:
        out.append(f"harbor run -p tasks/ --agent {h} -m moonshot/kimi-k2.6 --agent-timeout-multiplier 3.0 --job-name {h}-kimi -o baselines")
    out.append("")
    out.append("python3 tools/analysis/compare_harnesses.py \\")
    pieces = [f"  {h}=baselines/{h}-kimi" for h in harness_names]
    out.append(" \\\n".join(pieces))
    out.append("```")

    return "\n".join(out) + "\n"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    data = {}
    for arg in sys.argv[1:]:
        if "=" not in arg:
            print(f"bad arg: {arg!r} (expected NAME=DIR)", file=sys.stderr)
            sys.exit(2)
        name, path = arg.split("=", 1)
        data[name] = load_rewards(Path(path))
    print(render(data))
