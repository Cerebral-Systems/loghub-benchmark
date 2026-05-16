"""CLI: tar up 1000s of non-curated tasks for at-scale regression eval.

The curated `tasks/` directory ships 60 hand-balanced tasks that all
pass `harbor check` — that's the publishable benchmark. The stress pack
is the engineering tool: same adapters, same exporter, no curation, no
rubric pass. Use it to track agent regression across the full
case-builder population without paying per-task review cost.

The output is a tarball: extracting it gives `<target>-extracted/`
with the same `tasks/<slug>/` layout the curated set uses, plus a
`STRESS_PACK_MANIFEST.json` describing the generation parameters so
the bundle is reproducible.

Use:

    python -m tools.stress_pack_generator \\
        --target-count 1000 \\
        --output stress-pack-v1.tar.gz \\
        --seed 0
"""

from __future__ import annotations

import argparse
import datetime
import json
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
from pathlib import Path

from tools.case_builder import build_cases, export_to_harbor

# Per-dataset corpus directories on this VM. Override via --corpus-root
# if you move the data.
DEFAULT_CORPUS_ROOT = Path("/home/buildout/loghub-full")
DATASETS: tuple[tuple[str, str, int], ...] = (
    # (adapter_name, corpus_subdir, default_share_weight)
    ("hdfs", "HDFS", 4),
    ("hadoop", "Hadoop", 1),
    ("bgl", "BGL", 3),
    ("thunderbird", "Thunderbird", 2),
    ("openstack", "OpenStack", 1),
)


def _allocate(target: int) -> dict[str, int]:
    """Divide `target` across adapters by their default share weight.

    For Hadoop and OpenStack the corpus has a hard upper bound (44 and
    12 candidate cases respectively); the allocator caps at those even
    if the share would be higher."""
    total_weight = sum(w for _, _, w in DATASETS)
    hard_caps = {"hadoop": 44, "openstack": 12}
    out: dict[str, int] = {}
    remainder = target
    for name, _, weight in DATASETS:
        share = (target * weight) // total_weight
        share = min(share, hard_caps.get(name, target))
        out[name] = share
        remainder -= share
    # Spill any leftover into hdfs/bgl/thunderbird in that order — those
    # have effectively unbounded case populations.
    for name in ("hdfs", "bgl", "thunderbird"):
        if remainder <= 0:
            break
        bump = min(remainder, target)
        out[name] += bump
        remainder -= bump
    return out


def _run_adapter(
    adapter: str,
    corpus_dir: Path,
    cases_dir: Path,
    target: int,
    seed: int,
) -> int:
    build_cases.build(
        adapter_name=adapter,
        input_path=corpus_dir,
        output_dir=cases_dir,
        max_cases=target,
        seed=seed,
    )
    manifest = json.loads((cases_dir / "manifest.json").read_text())
    return manifest["count"]


def _export_cases(cases_dir: Path, output_dir: Path) -> int:
    written = 0
    manifest = json.loads((cases_dir / "manifest.json").read_text())
    for case_meta in manifest["cases"]:
        case = json.loads((cases_dir / case_meta["file"]).read_text())
        export_to_harbor.export_case(
            case,
            output_dir,
            author_name="Madhav Goyal",
            author_email="madhav@campnetwork.xyz",
        )
        written += 1
    return written


def _write_bundle_manifest(
    bundle_root: Path,
    *,
    target: int,
    actual: int,
    allocation: dict[str, int],
    per_adapter_actual: dict[str, int],
    seed: int,
) -> None:
    """Drop a metadata file so consumers can tell what the bundle was
    generated from without re-deriving from filenames."""
    manifest = {
        "schema_version": "stress-pack-v1",
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "target_count": target,
        "actual_count": actual,
        "seed": seed,
        "allocation_requested": allocation,
        "allocation_actual": per_adapter_actual,
        "exporter_canary": export_to_harbor.CANARY_GUID,
        "answer_schema_version": export_to_harbor.ANSWER_SCHEMA_VERSION,
        "datasets": [
            {"adapter": name, "corpus_dir": str(DEFAULT_CORPUS_ROOT / subdir)}
            for name, subdir, _ in DATASETS
        ],
    }
    (bundle_root / "STRESS_PACK_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--target-count", type=int, default=1000)
    p.add_argument("--output", type=Path, required=True, help="path for the .tar.gz bundle")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--corpus-root", type=Path, default=DEFAULT_CORPUS_ROOT)
    p.add_argument(
        "--keep-extracted",
        action="store_true",
        help="leave the extracted bundle alongside the tarball (useful for `harbor run -p`)",
    )
    args = p.parse_args(argv)

    args.output = args.output.resolve()
    args.output.parent.mkdir(parents=True, exist_ok=True)

    allocation = _allocate(args.target_count)
    print(f"target={args.target_count} → allocation {allocation}", file=sys.stderr)

    with tempfile.TemporaryDirectory(prefix="stress-pack-") as tmpdir:
        tmp = Path(tmpdir)
        tasks_dir = tmp / "tasks"
        tasks_dir.mkdir()

        per_adapter_actual: dict[str, int] = {}
        for adapter, subdir, _ in DATASETS:
            share = allocation[adapter]
            if share == 0:
                per_adapter_actual[adapter] = 0
                continue
            corpus_dir = args.corpus_root / subdir
            if not corpus_dir.is_dir():
                print(f"!! skipping {adapter}: {corpus_dir} missing", file=sys.stderr)
                per_adapter_actual[adapter] = 0
                continue

            cases_dir = tmp / f"cases-{adapter}"
            print(f"[{adapter}] building up to {share} cases ...", file=sys.stderr)
            t0 = time.time()
            built = _run_adapter(adapter, corpus_dir, cases_dir, share, args.seed)
            print(f"[{adapter}]   built {built} cases in {time.time() - t0:.1f}s", file=sys.stderr)
            t0 = time.time()
            written = _export_cases(cases_dir, tasks_dir)
            print(f"[{adapter}]   exported {written} tasks in {time.time() - t0:.1f}s", file=sys.stderr)
            per_adapter_actual[adapter] = written

        total = sum(per_adapter_actual.values())
        _write_bundle_manifest(
            tmp,
            target=args.target_count,
            actual=total,
            allocation=allocation,
            per_adapter_actual=per_adapter_actual,
            seed=args.seed,
        )

        # Move tasks/ + manifest into a named bundle root for legibility.
        bundle_name = args.output.stem.replace(".tar", "") + "-extracted"
        staged = tmp / bundle_name
        shutil.move(str(tasks_dir), str(staged / "tasks"))
        shutil.move(str(tmp / "STRESS_PACK_MANIFEST.json"), str(staged / "STRESS_PACK_MANIFEST.json"))

        print(f"packing → {args.output} ...", file=sys.stderr)
        with tarfile.open(args.output, "w:gz", compresslevel=6) as tar:
            tar.add(staged, arcname=bundle_name)
        size_mb = args.output.stat().st_size / (1024 * 1024)
        print(f"wrote {args.output} ({size_mb:.1f} MiB, {total} tasks)", file=sys.stderr)

        if args.keep_extracted:
            extracted_dest = args.output.parent / bundle_name
            if extracted_dest.exists():
                shutil.rmtree(extracted_dest)
            shutil.move(str(staged), str(extracted_dest))
            print(f"kept extracted bundle at {extracted_dest}", file=sys.stderr)


if __name__ == "__main__":
    main()
