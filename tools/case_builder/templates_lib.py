"""T5 template-extraction case builder.

Reads Loghub-2k structured CSVs and emits CandidateCase objects whose
slice carries 50-200 sampled log lines plus ground-truth EventTemplate
labels in `extra["template_ground_truth"]`.

The exporter ships these as a single-file log task; the agent must
partition the input lines by template and assign `<*>` placeholders
for the variable parts.
"""

from __future__ import annotations

import csv
import hashlib
import random
from collections import defaultdict
from pathlib import Path
from typing import Iterator

from .adapters.base import CandidateCase, LogSlice


# Loghub-2k CSV layouts vary per dataset. We auto-detect by required columns.
TEMPLATE_COL = "EventTemplate"
EVENT_ID_COL = "EventId"
CONTENT_COL = "Content"

# Sampling targets per case.
MIN_LINES_PER_CASE = 50
MAX_LINES_PER_CASE = 200
MIN_TEMPLATES_PER_CASE = 5

DATASET_2K_FILES: dict[str, str] = {
    "HDFS": "HDFS_2k.log_structured.csv",
    "Hadoop": "Hadoop_2k.log_structured.csv",
    "BGL": "BGL_2k.log_structured.csv",
    "Thunderbird": "Thunderbird_2k.log_structured.csv",
    "OpenStack": "OpenStack_2k.log_structured.csv",
}


def _load_structured(input_dir: Path, dataset: str) -> list[dict]:
    basename = DATASET_2K_FILES[dataset]
    path = input_dir / basename
    if not path.is_file():
        raise FileNotFoundError(f"{basename} not found under {input_dir}")
    with path.open() as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
    for col in (TEMPLATE_COL, EVENT_ID_COL, CONTENT_COL):
        if col not in (rows[0].keys() if rows else []):
            raise ValueError(f"{path}: expected column {col!r}, got {list(rows[0].keys())}")
    return rows


def iter_template_cases(
    input_dir: Path,
    dataset: str,
    *,
    max_cases: int = 4,
    seed: int = 0,
) -> Iterator[CandidateCase]:
    """Sample `max_cases` template-extraction windows from the dataset's
    2k structured CSV. Each window is a contiguous slice of MIN..MAX lines
    that contains ≥MIN_TEMPLATES_PER_CASE distinct EventTemplate values."""
    rows = _load_structured(input_dir, dataset)
    n = len(rows)
    if n < MIN_LINES_PER_CASE:
        return

    # Pre-compute starting offsets in a deterministic seed-derived order.
    # Window sizes are also seed-derived so cases differ.
    rnd = random.Random(seed)
    yielded = 0
    attempts = 0
    max_attempts = max_cases * 20

    while yielded < max_cases and attempts < max_attempts:
        attempts += 1
        size = rnd.randint(MIN_LINES_PER_CASE, MAX_LINES_PER_CASE)
        if size >= n:
            size = n - 1
        offset = rnd.randint(0, n - size)
        window = rows[offset:offset + size]

        # Need ≥MIN_TEMPLATES_PER_CASE distinct EventTemplates.
        templates_seen = {row[TEMPLATE_COL] for row in window}
        if len(templates_seen) < MIN_TEMPLATES_PER_CASE:
            continue

        # Build the line content (without the wrapping CSV columns).
        contents = [row[CONTENT_COL] for row in window]

        # Per-line GT mapping: line_idx_1based → EventTemplate
        gt_per_line = [row[TEMPLATE_COL] for row in window]
        # Aggregate: template → [line_idx_1based]
        template_to_lines: dict[str, list[int]] = defaultdict(list)
        for i, tmpl in enumerate(gt_per_line, start=1):
            template_to_lines[tmpl].append(i)

        # Assign stable template_ids (T1..TN) in order of first appearance.
        seen_order: list[str] = []
        for tmpl in gt_per_line:
            if tmpl not in seen_order:
                seen_order.append(tmpl)

        templates_payload = []
        for k, tmpl in enumerate(seen_order, start=1):
            lines = sorted(template_to_lines[tmpl])
            templates_payload.append({
                "template_id": f"T{k}",
                "template": tmpl,
                "matching_lines": lines,
                "example_line_number": lines[0],
            })

        slice_ = LogSlice(lines=tuple(contents), offset=offset, length=len(contents))
        case_id = hashlib.sha256(
            f"tmpl|{dataset}|{seed}|{offset}|{size}".encode("utf-8")
        ).hexdigest()
        yield CandidateCase(
            case_id=case_id,
            dataset_name=dataset,
            adapter_version="tmpl-1",
            slice=slice_,
            anomaly_line_ids=(),
            root_cause="n/a",
            anomaly_keys=(),
            extra={
                "template_ground_truth": templates_payload,
                "total_unique_templates": len(seen_order),
            },
            task_type="tmpl",
        )
        yielded += 1
