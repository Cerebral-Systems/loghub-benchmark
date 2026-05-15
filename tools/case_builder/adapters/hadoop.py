"""Hadoop adapter — turns Loghub's Hadoop corpus into Harbor task candidates.

Inputs:
  - One directory per Hadoop application, named `application_<ts>_<id>/`,
    each containing multiple `container_*.log` files.
  - `abnormal_label.txt`: a human-readable text grouping job IDs by fault
    type ('Normal' / 'Machine down' / 'Network disconnection' / 'Disk full').

Per-job logs are small (~50-500 KiB), so we follow PLAN.md M2b's "concatenate
one normal job + one anomalous job into a single window" strategy. The
case_id pins the chosen (normal, anomalous) pair via the slice line layout.

Hadoop has the strongest gold signal in Loghub — root cause comes directly
from the label file, no pattern heuristics.
"""

from __future__ import annotations

import hashlib
import re
from collections import defaultdict
from pathlib import Path
from typing import Iterator

from .base import AdapterBase, CandidateCase, LabelIndex, LogSlice


# Map abnormal_label.txt headings → our taxonomy slug.
LABEL_HEADING_TO_SLUG = {
    "Normal": "normal",
    "Machine down": "machine_down",
    "Network disconnection": "network_disconnect",
    "Disk full": "disk_full",
}

POSITIVE_TAXONOMY = ("machine_down", "network_disconnect", "disk_full")

JOB_LINE_RE = re.compile(r"^\+?\s*(application_\d+_\d+)\s*$")


class HadoopAdapter(AdapterBase):
    dataset_name = "Hadoop"
    adapter_version = "1"
    # Cases only emit anomalous root causes; 'normal' is preserved for the
    # label vocabulary but never returned by classify_root_cause.
    root_cause_taxonomy = POSITIVE_TAXONOMY

    # --- label loading -----------------------------------------------------

    def load_labels(self, input_path: Path) -> LabelIndex:
        label_file = self._locate_label_file(input_path)
        entries: dict[str, str] = {}
        current_label: str | None = None
        with label_file.open() as fh:
            for raw in fh:
                stripped = raw.strip()
                if not stripped:
                    continue
                heading = self._heading_for(stripped)
                if heading is not None:
                    current_label = heading
                    continue
                m = JOB_LINE_RE.match(stripped)
                if m and current_label is not None:
                    entries[m.group(1)] = current_label
        return LabelIndex(entries=entries, positive_labels=frozenset(POSITIVE_TAXONOMY))

    @staticmethod
    def _heading_for(line: str) -> str | None:
        """Return the taxonomy slug for a heading line, or None if not a heading.

        abnormal_label.txt headings are bare words ending in ':' such as
        'Normal:', 'Machine down:', 'Network disconnection:', 'Disk full:'.
        Application-stanza markers ('### WordCount', '### PageRank') are ignored.
        """
        if not line.endswith(":"):
            return None
        body = line[:-1].strip()
        return LABEL_HEADING_TO_SLUG.get(body)

    @staticmethod
    def _locate_label_file(input_path: Path) -> Path:
        for c in (input_path / "abnormal_label.txt", input_path / "labels.txt"):
            if c.is_file():
                return c
        raise FileNotFoundError(f"abnormal_label.txt not found under {input_path}")

    # --- case iteration ----------------------------------------------------

    def iter_candidate_cases(
        self,
        input_path: Path,
        labels: LabelIndex,
        *,
        max_cases: int | None = None,
        seed: int = 0,
    ) -> Iterator[CandidateCase]:
        normal_jobs = sorted(k for k, v in labels.entries.items() if v == "normal")
        anomalous_jobs = sorted(k for k in labels.anomalous_keys())
        if not normal_jobs:
            raise ValueError("Hadoop adapter requires at least one normal job for slice pairing")
        if not anomalous_jobs:
            return

        yielded = 0
        for anomalous_job in anomalous_jobs:
            normal_job = self._pick_normal(anomalous_job, normal_jobs, seed)
            normal_lines = self._read_job_lines(input_path, normal_job)
            anomalous_lines = self._read_job_lines(input_path, anomalous_job)
            if not normal_lines or not anomalous_lines:
                continue

            # Concatenated stream: [header for normal] + normal_lines +
            # [header for anomalous] + anomalous_lines.
            header_n = f"### normal_job={normal_job}"
            header_a = f"### anomalous_job={anomalous_job}"
            combined = [header_n, *normal_lines, header_a, *anomalous_lines]

            # 1-based line numbers within the slice that belong to the
            # anomalous job (i.e. the lines the agent must cite).
            start_of_anomalous = 1 + 1 + len(normal_lines) + 1  # header_n + normal_lines + header_a + first anomalous line
            anomaly_line_ids = list(range(start_of_anomalous, start_of_anomalous + len(anomalous_lines)))

            slice_ = LogSlice(lines=tuple(combined), offset=0, length=len(combined))
            root_cause = labels.entries[anomalous_job]
            self.validate_root_cause(root_cause)
            yield CandidateCase(
                case_id=self.case_id(slice_, anomaly_line_ids),
                dataset_name=self.dataset_name,
                adapter_version=self.adapter_version,
                slice=slice_,
                anomaly_line_ids=tuple(anomaly_line_ids),
                root_cause=root_cause,
                anomaly_keys=(anomalous_job,),
                extra={"normal_job": normal_job},
            )
            yielded += 1
            if max_cases is not None and yielded >= max_cases:
                return

    @staticmethod
    def _pick_normal(anomalous_job: str, normal_jobs: list[str], seed: int) -> str:
        h = hashlib.sha256(f"{seed}|{anomalous_job}".encode("utf-8")).digest()
        return normal_jobs[int.from_bytes(h[:8], "big") % len(normal_jobs)]

    @staticmethod
    def _read_job_lines(input_path: Path, job_id: str) -> list[str]:
        job_dir = input_path / job_id
        if not job_dir.is_dir():
            return []
        # Stable container ordering: container_*.log sorted lexicographically.
        out: list[str] = []
        for container_log in sorted(job_dir.glob("container_*.log")):
            with container_log.open(errors="replace") as fh:
                for line in fh:
                    out.append(line.rstrip("\n"))
        return out

    # --- slice / classification overrides ---------------------------------

    def select_slice(self, full_log, anomaly_indices, seed):  # pragma: no cover
        raise NotImplementedError("Hadoop slices are built inside iter_candidate_cases")

    def classify_root_cause(self, log_slice, anomaly_lines):  # pragma: no cover
        raise NotImplementedError("Hadoop uses gold labels; classification is done in iter_candidate_cases")
