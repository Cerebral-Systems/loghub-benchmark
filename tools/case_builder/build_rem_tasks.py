"""Seed rem-* (T6 outcome remediation) tasks from existing corr-* / seq-* tasks.

The remediation exporter (export_to_harbor._export_rem_case) needs a case
dict whose `extra["rem"]` slot is already populated with:

  - files: {filename: [lines]}            (the partitioned log content)
  - root_component: <log filename>        (causal root)
  - causal_chain: [{step, component, role, evidence_line, caused_by_step?}]
  - anomaly_locations: [{file, line}]     (evidence the agent should cite)

That metadata is exactly what the existing corr-* (and to a lesser extent
seq-*) task directories already encode in their tests/expected.json. This
driver reads those task dirs and re-exports them as rem-* tasks, so we get
20+ remediation tasks deterministically without re-walking the loghub corpus.

Usage:
    python -m tools.case_builder.build_rem_tasks \\
        --tasks-dir tasks \\
        --selection tools/case_builder/remediation_selection.json \\
        --output-dir tasks
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from . import export_to_harbor as ex


DATASET_BY_PREFIX = {
    "hdfs": "HDFS_v1",
    "hadoop": "Hadoop",
    "bgl": "BGL",
    "thunderbird": "Thunderbird",
    "openstack": "OpenStack",
}


def _dataset_from_slug(slug: str) -> str:
    parts = slug.split("-")
    # corr-hdfs-other-2015555 -> hdfs ; seq-openstack-vmtask-0965b62 -> openstack
    prefix = parts[1] if parts[0] in {"corr", "seq", "fp", "sev", "tmpl", "rem"} else parts[0]
    return DATASET_BY_PREFIX[prefix]


def _stable_short_id(source_slug: str) -> str:
    """Deterministic 7-char id derived from the seed slug, used for rem-* slug."""
    return hashlib.sha256(source_slug.encode("utf-8")).hexdigest()[:7]


def _read_logs(task_dir: Path) -> dict[str, list[str]]:
    files: dict[str, list[str]] = {}
    data_dir = task_dir / "environment" / "data"
    for path in sorted(data_dir.glob("*.log")):
        files[path.name] = path.read_text(errors="replace").splitlines()
    return files


def _causal_chain_from_corr(expected: dict) -> tuple[list[dict], str, list[dict]]:
    """Pull (chain, root_filename, anomaly_locations) from a corr-* expected.json."""
    chain_in = expected["causal_chain"]
    chain_out: list[dict] = []
    for step in chain_in:
        out_step = {
            "step": step["step"],
            "component": step["component"],
            "role": step["role"],
            "evidence_line": step["evidence_line"],
        }
        if "caused_by_step" in step:
            out_step["caused_by_step"] = step["caused_by_step"]
        chain_out.append(out_step)
    root_file = expected["root_component"]
    anomaly_locations = [
        {"file": s["component"], "line": s["evidence_line"]} for s in chain_in
    ]
    return chain_out, root_file, anomaly_locations


def _causal_chain_from_seq(expected: dict) -> tuple[list[dict], str, list[dict]]:
    """Project a seq-* timeline into a corr-style causal chain.

    The trigger event becomes step 0 (root). Subsequent events in the same
    component as the trigger collapse with it (don't add a new chain step);
    events in distinct components become a single linear downstream chain
    in trigger-then-other-files order.
    """
    timeline = expected["timeline"]
    trigger = next(e for e in timeline if e["role"] == "trigger")
    root_file = trigger["file"]
    chain_out: list[dict] = []
    seen_components: set[str] = set()
    parent_step: int | None = None
    anomaly_locations: list[dict] = []
    for entry in timeline:
        if entry["file"] in seen_components:
            anomaly_locations.append({"file": entry["file"], "line": entry["line"]})
            continue
        if entry["file"] == root_file and parent_step is not None:
            anomaly_locations.append({"file": entry["file"], "line": entry["line"]})
            continue
        seen_components.add(entry["file"])
        step_idx = len(chain_out)
        out_step: dict = {
            "step": step_idx,
            "component": entry["file"],
            "role": "root" if step_idx == 0 else "downstream",
            "evidence_line": entry["line"],
        }
        if step_idx > 0:
            assert parent_step is not None
            out_step["caused_by_step"] = parent_step
        chain_out.append(out_step)
        parent_step = step_idx
        anomaly_locations.append({"file": entry["file"], "line": entry["line"]})
    return chain_out, root_file, anomaly_locations


def _causal_chain_from_v1(expected: dict) -> tuple[list[dict], str, list[dict]]:
    """Project a v1 localization expected.json into a corr-style causal chain.

    The file holding the most ground-truth evidence becomes the root
    component (step 0, first evidence line as the root event); every other
    file with evidence becomes one downstream step. This lets v1 sources —
    which carry the only action-diverse root causes in the committed set
    (hadoop disk_full -> increase_quota, network_disconnect ->
    disable_route) — seed remediation tasks."""
    evidence = expected["evidence"]
    by_file: dict[str, list[int]] = {}
    for e in evidence:
        by_file.setdefault(e["file"], []).append(e["line"])
    if not by_file:
        return [], "", []
    root_file = max(by_file, key=lambda f: (len(by_file[f]), -min(by_file[f])))
    chain_out: list[dict] = [{
        "step": 0,
        "component": root_file,
        "role": "root",
        "evidence_line": min(by_file[root_file]),
    }]
    for fname in sorted(f for f in by_file if f != root_file):
        chain_out.append({
            "step": len(chain_out),
            "component": fname,
            "role": "downstream",
            "evidence_line": min(by_file[fname]),
            "caused_by_step": 0,
        })
    anomaly_locations = [{"file": e["file"], "line": e["line"]} for e in evidence]
    return chain_out, root_file, anomaly_locations


def synthesize_rem_case(source_task_dir: Path) -> dict | None:
    """Build a case dict suitable for ex._export_rem_case() from a source task.

    Returns None if the source task does not have enough structure to seed
    a useful remediation task (e.g. a single-file seq with no trigger).
    """
    expected = json.loads((source_task_dir / "tests" / "expected.json").read_text())
    schema = expected.get("schema_version", "")
    files = _read_logs(source_task_dir)
    if not files:
        return None

    if schema.endswith("-v2-corr"):
        chain, root_file, anomaly_locations = _causal_chain_from_corr(expected)
    elif schema.endswith("-v2-seq"):
        chain, root_file, anomaly_locations = _causal_chain_from_seq(expected)
    elif schema.endswith("-v2"):
        # v1 localization source (exact-location evidence only).
        if expected.get("evidence_validation", {}).get("mode") not in (None, "exact_location"):
            return None
        chain, root_file, anomaly_locations = _causal_chain_from_v1(expected)
        if not chain:
            return None
    else:
        return None

    dataset = _dataset_from_slug(source_task_dir.name)
    root_cause = expected["root_cause_type"]
    short_id = _stable_short_id(source_task_dir.name)
    case_id = hashlib.sha256(
        f"rem|{source_task_dir.name}|{root_cause}".encode("utf-8")
    ).hexdigest()
    # Pad to 64 hex chars (sha256 already 64, but keep the format explicit).
    case_id = (case_id + "0" * 64)[:64]

    case: dict = {
        "case_id": case_id,
        "dataset_name": dataset,
        "adapter_version": "rem-1",
        "slice": {"lines": [], "offset": 0, "length": 0},
        "anomaly_line_ids": [],
        "root_cause": root_cause,
        "anomaly_keys": [],
        "extra": {
            "rem": {
                "files": files,
                "root_component": root_file,
                "causal_chain": chain,
                "anomaly_locations": anomaly_locations,
                "source_task": source_task_dir.name,
            },
        },
        "task_type": "rem",
    }
    # Force the short_id by overwriting case_id's leading 7 chars deterministically:
    # ex.make_slug_v2 picks case_id[:7]. Hash above already gives 7 stable hex chars.
    case["case_id"] = short_id + case_id[7:]
    return case


def build_default_selection(tasks_dir: Path) -> list[Path]:
    """Pick the default 20 source tasks (5 hdfs, 5 hadoop, 5 openstack, 3 bgl, 2 tb).

    The OpenStack count is filled from seq-openstack-* (corr-openstack-* does
    not currently exist in the curated set); the rest pull from corr-*.
    """
    selection: list[Path] = []

    def take(prefix_pattern: str, count: int) -> None:
        for path in sorted(tasks_dir.iterdir()):
            if len(selection) - prev >= count:
                break
            if not path.is_dir():
                continue
            if not path.name.startswith(prefix_pattern):
                continue
            selection.append(path)

    prev = 0
    take("corr-hdfs-", 4)
    prev = len(selection)
    take("corr-hadoop-", 3)
    # v1 hadoop sources carry the only action-diverse root causes in the
    # committed set: disk_full -> increase_quota, network_disconnect ->
    # disable_route. Without them every rem task's correct mitigation is
    # restart_component and the action decision is a constant.
    prev = len(selection)
    take("hadoop-disk-", 3)
    prev = len(selection)
    take("hadoop-network-", 3)
    prev = len(selection)
    take("seq-openstack-", 4)
    prev = len(selection)
    take("corr-bgl-", 2)
    prev = len(selection)
    take("corr-thunderbird-", 1)
    return selection


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--tasks-dir", type=Path, default=Path("tasks"))
    p.add_argument("--output-dir", type=Path, default=Path("tasks"))
    p.add_argument("--selection", type=Path, default=None,
                   help="JSON file with a 'sources' list of slug strings (under --tasks-dir).")
    p.add_argument("--author-name", default="Madhav Goyal")
    p.add_argument("--author-email", default="madhav@campnetwork.xyz")
    p.add_argument("--print-only", action="store_true", help="List source tasks and exit.")
    args = p.parse_args(argv)

    if args.selection:
        manifest = json.loads(args.selection.read_text())
        sources = [args.tasks_dir / slug for slug in manifest["sources"]]
    else:
        sources = build_default_selection(args.tasks_dir)

    print(f"selected {len(sources)} source tasks:", file=sys.stderr)
    for s in sources:
        print(f"  {s.name}", file=sys.stderr)
    if args.print_only:
        return

    args.output_dir.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    skipped: list[str] = []
    for src in sources:
        case = synthesize_rem_case(src)
        if case is None:
            skipped.append(src.name)
            print(f"skip {src.name}: no usable structure", file=sys.stderr)
            continue
        try:
            out_dir = ex.export_case(
                case,
                args.output_dir,
                author_name=args.author_name,
                author_email=args.author_email,
            )
        except ex._SkipRemCase as exc:
            skipped.append(src.name)
            print(f"skip {src.name}: {exc}", file=sys.stderr)
            continue
        written.append(out_dir.name)
        print(f"wrote {out_dir.name}", file=sys.stderr)

    print(f"\nexported {len(written)} rem-* tasks (skipped {len(skipped)})", file=sys.stderr)


if __name__ == "__main__":
    main()
