"""Rebuild or describe the committed curated Loghub-SRE task set.

The adapters can emit many more cases than the 60 tasks committed under
`tasks/`. This tool keeps that curated set reproducible by recording the
full case IDs behind those slugs, then rebuilding exactly those cases
from the raw corpus.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from . import export_to_harbor
from .adapters import AdapterBase
from .build_cases import ADAPTERS

DEFAULT_MANIFEST = Path("tools/case_builder/curated_selection.json")
DEFAULT_CORPUS_ROOT = Path("/home/buildout/loghub-full")

DATASET_TO_ADAPTER = {
    "HDFS_v1": "hdfs",
    "Hadoop": "hadoop",
    "BGL": "bgl",
    "Thunderbird": "thunderbird",
    "OpenStack": "openstack",
}

ADAPTER_INPUT_SUBDIR = {
    "hdfs": "HDFS",
    "hadoop": "Hadoop",
    "bgl": "BGL",
    "thunderbird": "Thunderbird",
    "openstack": "OpenStack",
}


def _load_case(path: Path) -> dict:
    return json.loads(path.read_text())


def write_manifest(tasks_dir: Path, cases_dirs: list[str], output: Path, seed: int) -> None:
    cases_by_slug: dict[str, dict] = {}
    for spec in cases_dirs:
        if "=" not in spec:
            raise SystemExit(f"bad --cases-dir {spec!r}; expected adapter=/path")
        adapter_name, path_s = spec.split("=", 1)
        path = Path(path_s)
        manifest_path = path / "manifest.json"
        if not manifest_path.is_file():
            raise SystemExit(f"{manifest_path} not found")
        manifest = _load_case(manifest_path)
        for meta in manifest["cases"]:
            case = _load_case(path / meta["file"])
            slug = export_to_harbor.make_slug(case)
            cases_by_slug[slug] = {
                "adapter": adapter_name,
                "case": case,
            }

    selections = []
    missing = []
    for task_dir in sorted(d for d in tasks_dir.iterdir() if d.is_dir()):
        record = cases_by_slug.get(task_dir.name)
        if record is None:
            missing.append(task_dir.name)
            continue
        case = record["case"]
        selections.append(
            {
                "slug": task_dir.name,
                "adapter": record["adapter"],
                "dataset_name": case["dataset_name"],
                "adapter_version": case["adapter_version"],
                "case_id": case["case_id"],
                "root_cause": case["root_cause"],
                "anomaly_keys": list(case.get("anomaly_keys", [])),
            }
        )

    if missing:
        raise SystemExit(f"no case JSON found for task slugs: {missing}")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(
            {
                "schema_version": "loghub-curated-selection-v1",
                "seed": seed,
                "task_count": len(selections),
                "selections": selections,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    print(f"wrote {len(selections)} selections to {output}")


def refresh_from_existing(
    tasks_dir: Path,
    cases_dirs: list[str],
    output_dir: Path,
    manifest_output: Path,
    *,
    seed: int,
    clear_output: bool,
    author_name: str,
    author_email: str,
) -> None:
    existing_slugs = sorted(d.name for d in tasks_dir.iterdir() if d.is_dir())
    desired_counts: dict[tuple[str, str], int] = {}
    for task_dir in sorted(d for d in tasks_dir.iterdir() if d.is_dir()):
        expected = json.loads((task_dir / "tests" / "expected.json").read_text())
        dataset = expected_dataset_from_slug(task_dir.name)
        key = (dataset, expected["root_cause_type"])
        desired_counts[key] = desired_counts.get(key, 0) + 1

    cases: list[tuple[str, dict]] = []
    for spec in cases_dirs:
        if "=" not in spec:
            raise SystemExit(f"bad --cases-dir {spec!r}; expected adapter=/path")
        adapter_name, path_s = spec.split("=", 1)
        path = Path(path_s)
        manifest = _load_case(path / "manifest.json")
        for meta in manifest["cases"]:
            cases.append((adapter_name, _load_case(path / meta["file"])))

    selected: list[tuple[str, dict]] = []
    selected_case_ids: set[str] = set()
    remaining = dict(desired_counts)

    # Preserve old slugs first when the refreshed exporter still gives a
    # suitably agentic file layout.
    existing = set(existing_slugs)
    for adapter_name, case in cases:
        slug = export_to_harbor.make_slug(case)
        if slug not in existing:
            continue
        if not _case_has_enough_files(case):
            continue
        key = (case["dataset_name"], case["root_cause"])
        if remaining.get(key, 0) <= 0:
            continue
        selected.append((adapter_name, case))
        selected_case_ids.add(case["case_id"])
        remaining[key] -= 1

    # Fill gaps, including Hadoop v2 whose case IDs and slugs intentionally
    # change after compact evidence selection.
    for adapter_name, case in cases:
        if case["case_id"] in selected_case_ids:
            continue
        if not _case_has_enough_files(case):
            continue
        key = (case["dataset_name"], case["root_cause"])
        if remaining.get(key, 0) <= 0:
            continue
        selected.append((adapter_name, case))
        selected_case_ids.add(case["case_id"])
        remaining[key] -= 1

    missing = {key: count for key, count in remaining.items() if count}
    if missing:
        raise SystemExit(f"could not refresh desired task distribution; missing {missing}")

    if clear_output and output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    selections = []
    for adapter_name, case in sorted(selected, key=lambda item: export_to_harbor.make_slug(item[1])):
        task_dir = export_to_harbor.export_case(
            case,
            output_dir,
            author_name=author_name,
            author_email=author_email,
        )
        selections.append(
            {
                "slug": task_dir.name,
                "adapter": adapter_name,
                "dataset_name": case["dataset_name"],
                "adapter_version": case["adapter_version"],
                "case_id": case["case_id"],
                "root_cause": case["root_cause"],
                "anomaly_keys": list(case.get("anomaly_keys", [])),
            }
        )

    manifest_output.parent.mkdir(parents=True, exist_ok=True)
    manifest_output.write_text(
        json.dumps(
            {
                "schema_version": "loghub-curated-selection-v1",
                "seed": seed,
                "task_count": len(selections),
                "selections": selections,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    print(f"refreshed {len(selections)} tasks in {output_dir}")
    print(f"wrote curated manifest to {manifest_output}")


def expected_dataset_from_slug(slug: str) -> str:
    prefix = slug.split("-", 1)[0]
    by_prefix = {
        "hdfs": "HDFS_v1",
        "hadoop": "Hadoop",
        "bgl": "BGL",
        "thunderbird": "Thunderbird",
        "openstack": "OpenStack",
    }
    return by_prefix[prefix]


def _case_has_enough_files(case: dict) -> bool:
    if case["dataset_name"] not in {"BGL", "Thunderbird"}:
        return True
    files, _ = export_to_harbor._partition_slice(case)
    return len(files) >= 2


def rebuild(
    manifest_path: Path,
    corpus_root: Path,
    output_dir: Path,
    *,
    clear_output: bool,
    author_name: str,
    author_email: str,
) -> None:
    manifest = _load_case(manifest_path)
    wanted = manifest["selections"]
    by_adapter: dict[str, set[str]] = {}
    for selection in wanted:
        by_adapter.setdefault(selection["adapter"], set()).add(selection["case_id"])

    found: dict[str, dict] = {}
    for adapter_name, wanted_ids in by_adapter.items():
        adapter_cls: type[AdapterBase] = ADAPTERS[adapter_name]
        adapter = adapter_cls()
        input_path = corpus_root / ADAPTER_INPUT_SUBDIR[adapter_name]
        labels = adapter.load_labels(input_path)
        for case in adapter.iter_candidate_cases(input_path, labels, max_cases=None, seed=manifest["seed"]):
            if case.case_id in wanted_ids:
                found[case.case_id] = _case_to_dict(case)
                if wanted_ids <= found.keys():
                    break

    missing = sorted(selection["case_id"] for selection in wanted if selection["case_id"] not in found)
    if missing:
        raise SystemExit(f"curated case IDs not found in regenerated candidates: {missing}")

    if clear_output and output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for selection in wanted:
        case = found[selection["case_id"]]
        slug = export_to_harbor.make_slug(case)
        if slug != selection["slug"]:
            raise SystemExit(f"slug drift for {selection['case_id']}: manifest={selection['slug']} generated={slug}")
        export_to_harbor.export_case(
            case,
            output_dir,
            author_name=author_name,
            author_email=author_email,
        )
    print(f"rebuilt {len(wanted)} curated tasks in {output_dir}")


def _case_to_dict(case) -> dict:
    return {
        "case_id": case.case_id,
        "dataset_name": case.dataset_name,
        "adapter_version": case.adapter_version,
        "slice": {
            "lines": list(case.slice.lines),
            "offset": case.slice.offset,
            "length": case.slice.length,
        },
        "anomaly_line_ids": list(case.anomaly_line_ids),
        "root_cause": case.root_cause,
        "anomaly_keys": list(case.anomaly_keys),
        "extra": dict(case.extra),
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    w = sub.add_parser("write-manifest", help="write manifest from task slugs and case-builder outputs")
    w.add_argument("--tasks-dir", type=Path, default=Path("tasks"))
    w.add_argument("--cases-dir", action="append", required=True, help="adapter=/path/to/cases; repeat per adapter")
    w.add_argument("--output", type=Path, default=DEFAULT_MANIFEST)
    w.add_argument("--seed", type=int, default=0)

    r = sub.add_parser("rebuild", help="rebuild exactly the manifest-selected tasks")
    r.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    r.add_argument("--corpus-root", type=Path, default=DEFAULT_CORPUS_ROOT)
    r.add_argument("--output-dir", type=Path, default=Path("tasks"))
    r.add_argument("--clear-output", action="store_true")
    r.add_argument("--author-name", default="madhav")
    r.add_argument("--author-email", default="madhavgoyal007@pm.me")

    f = sub.add_parser("refresh-from-existing", help="refresh current curation from case-builder outputs")
    f.add_argument("--tasks-dir", type=Path, default=Path("tasks"))
    f.add_argument("--cases-dir", action="append", required=True, help="adapter=/path/to/cases; repeat per adapter")
    f.add_argument("--output-dir", type=Path, default=Path("tasks"))
    f.add_argument("--manifest-output", type=Path, default=DEFAULT_MANIFEST)
    f.add_argument("--seed", type=int, default=0)
    f.add_argument("--clear-output", action="store_true")
    f.add_argument("--author-name", default="madhav")
    f.add_argument("--author-email", default="madhavgoyal007@pm.me")

    args = parser.parse_args(argv)
    if args.command == "write-manifest":
        write_manifest(args.tasks_dir, args.cases_dir, args.output, args.seed)
    elif args.command == "rebuild":
        rebuild(
            args.manifest,
            args.corpus_root,
            args.output_dir,
            clear_output=args.clear_output,
            author_name=args.author_name,
            author_email=args.author_email,
        )
    else:
        refresh_from_existing(
            args.tasks_dir,
            args.cases_dir,
            args.output_dir,
            args.manifest_output,
            seed=args.seed,
            clear_output=args.clear_output,
            author_name=args.author_name,
            author_email=args.author_email,
        )


if __name__ == "__main__":
    main()
