"""CLI: build JSON case specs from a Loghub dataset.

    python -m tools.case-builder.build_cases \\
        --adapter hdfs \\
        --input  /home/buildout/loghub-full/HDFS \\
        --output .benchmark/cases-hdfs \\
        --max-cases 20

Writes one JSON per candidate case plus a manifest.json. Each case's
`case_id` is a pure function of dataset + adapter version + slice
parameters + anomaly lines, so re-running on the same inputs produces
the same files. The Harbor exporter consumes these JSON specs.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from .adapters import AdapterBase
from .adapters.bgl import BGLAdapter
from .adapters.hadoop import HadoopAdapter
from .adapters.hdfs import HDFSAdapter
from .adapters.openstack import OpenStackAdapter
from .adapters.thunderbird import ThunderbirdAdapter

ADAPTERS: dict[str, type[AdapterBase]] = {
    "hdfs": HDFSAdapter,
    "hadoop": HadoopAdapter,
    "bgl": BGLAdapter,
    "thunderbird": ThunderbirdAdapter,
    "openstack": OpenStackAdapter,
}


def _case_to_dict(case) -> dict:
    d = asdict(case)
    # LogSlice's lines is a tuple — keep it as a list for JSON.
    d["slice"]["lines"] = list(case.slice.lines)
    d["anomaly_line_ids"] = list(case.anomaly_line_ids)
    d["anomaly_keys"] = list(case.anomaly_keys)
    return d


def build(
    adapter_name: str,
    input_path: Path,
    output_dir: Path,
    max_cases: int,
    seed: int,
    *,
    task_type: str = "anomaly",
) -> int:
    if adapter_name not in ADAPTERS:
        raise SystemExit(f"unknown adapter {adapter_name!r}; choices: {sorted(ADAPTERS)}")
    adapter = ADAPTERS[adapter_name]()
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"loading labels from {input_path} ...", file=sys.stderr)
    labels = adapter.load_labels(input_path)
    print(f"  {len(labels.entries):,} labels; {len(labels.anomalous_keys()):,} anomalous", file=sys.stderr)

    if task_type == "anomaly":
        case_iter = adapter.iter_candidate_cases(input_path, labels, max_cases=max_cases, seed=seed)
    elif task_type == "fp":
        case_iter = adapter.iter_false_positive_windows(input_path, labels, max_cases=max_cases, seed=seed)
    elif task_type in ("seq", "corr"):
        # T2/T3: reuse v1 anomaly cases; the timeline / causal-chain is
        # derived at export time. We mark the task_type here so the exporter
        # dispatches to the right path.
        def _retag_iter():
            from .adapters.base import CandidateCase
            for c in adapter.iter_candidate_cases(input_path, labels, max_cases=max_cases, seed=seed):
                yield CandidateCase(
                    case_id=c.case_id,
                    dataset_name=c.dataset_name,
                    adapter_version=c.adapter_version,
                    slice=c.slice,
                    anomaly_line_ids=c.anomaly_line_ids,
                    root_cause=c.root_cause,
                    anomaly_keys=c.anomaly_keys,
                    extra=c.extra,
                    task_type=task_type,
                )
        case_iter = _retag_iter()
    else:
        raise SystemExit(f"unknown task_type {task_type!r}")

    manifest: list[dict] = []
    count = 0
    for case in case_iter:
        case_dict = _case_to_dict(case)
        out_path = output_dir / f"{case.case_id}.json"
        with out_path.open("w") as fh:
            json.dump(case_dict, fh, indent=2, sort_keys=True)
        manifest.append(
            {
                "case_id": case.case_id,
                "dataset_name": case.dataset_name,
                "adapter_version": case.adapter_version,
                "root_cause": case.root_cause,
                "anomaly_keys": list(case.anomaly_keys),
                "anomaly_line_ids": list(case.anomaly_line_ids),
                "slice_offset": case.slice.offset,
                "slice_length": case.slice.length,
                "file": out_path.name,
                "task_type": case.task_type,
            }
        )
        count += 1
        if count % 5 == 0:
            print(f"  built {count} cases ...", file=sys.stderr)

    manifest_path = output_dir / "manifest.json"
    with manifest_path.open("w") as fh:
        json.dump(
            {
                "adapter": adapter_name,
                "adapter_version": adapter.adapter_version,
                "dataset_name": adapter.dataset_name,
                "seed": seed,
                "max_cases": max_cases,
                "input_path": str(input_path),
                "count": count,
                "cases": manifest,
            },
            fh,
            indent=2,
            sort_keys=True,
        )

    print(f"wrote {count} cases + manifest.json to {output_dir}", file=sys.stderr)
    return count


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--adapter", required=True, choices=sorted(ADAPTERS))
    p.add_argument("--input", required=True, type=Path, help="dataset directory (e.g. HDFS/)")
    p.add_argument("--output", required=True, type=Path, help="output directory for case JSON")
    p.add_argument("--max-cases", type=int, default=20, help="upper bound on cases to emit")
    p.add_argument("--seed", type=int, default=0, help="seed mixed into per-case slice selection")
    p.add_argument(
        "--task-type",
        default="anomaly",
        choices=("anomaly", "fp", "seq", "corr"),
        help="Which adapter generator to invoke. 'anomaly' (v1, default) calls "
        "iter_candidate_cases. 'fp' (v2/T1) calls iter_false_positive_windows. "
        "'seq' (v2/T2) and 'corr' (v2/T3) reuse v1 anomaly cases and tag them "
        "for the respective exporter.",
    )
    args = p.parse_args(argv)
    build(args.adapter, args.input, args.output, args.max_cases, args.seed, task_type=args.task_type)


if __name__ == "__main__":
    main()
