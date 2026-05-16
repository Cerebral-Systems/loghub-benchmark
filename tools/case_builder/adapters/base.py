"""Adapter contract shared by every Loghub dataset.

Every adapter is a pure function of `(dataset_version, adapter_version,
slice_parameters, anomaly_lines)` so case_ids stay stable across runs and
across machines. The exporter in `tools/case-builder/export_to_harbor.py`
(landing in M3) reads the JSON case specs these adapters emit and writes
the Harbor-shaped `tasks/<slug>/` directories.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, Mapping


@dataclass(frozen=True)
class LabelIndex:
    """Maps entity keys (block id, job id, host, ...) to a label string.

    `positive_labels` is the subset of values in `entries.values()` that
    indicate an anomaly. Adapters define this per-dataset because Loghub's
    label vocabulary varies (e.g. HDFS uses 'Anomaly', Hadoop uses fault names).
    """

    entries: Mapping[str, str]
    positive_labels: frozenset[str]

    def is_anomalous(self, key: str) -> bool:
        return self.entries.get(key) in self.positive_labels

    def anomalous_keys(self) -> list[str]:
        return [k for k, v in self.entries.items() if v in self.positive_labels]


@dataclass(frozen=True)
class LogSlice:
    """A window into the full log, suitable for baking into a task image.

    `offset` is the 0-based line index of `lines[0]` within the full log;
    `length` is `len(lines)`. Together they pin the slice deterministically
    so `case_id` stays stable.
    """

    lines: tuple[str, ...]
    offset: int
    length: int

    def __post_init__(self) -> None:
        if self.length != len(self.lines):
            raise ValueError(f"LogSlice length {self.length} != len(lines) {len(self.lines)}")


@dataclass(frozen=True)
class CandidateCase:
    """A task candidate before Harbor-shaping.

    Carries everything the M3 exporter needs to write `tasks/<slug>/`:
    the log slice, the anomaly lines (1-based to match Loghub's LineId
    convention), the root-cause label, and the entity keys involved.
    """

    case_id: str
    dataset_name: str
    adapter_version: str
    slice: LogSlice
    anomaly_line_ids: tuple[int, ...]  # 1-based line numbers within `slice.lines`
    root_cause: str
    anomaly_keys: tuple[str, ...]  # block IDs / job IDs / etc. that triggered this case
    extra: Mapping[str, object] = field(default_factory=dict)


class AdapterBase:
    """Subclass per dataset; override the four data-shaped methods.

    `adapter_version` is bumped whenever the slice or classification logic
    changes in a way that should invalidate prior case_ids.
    """

    dataset_name: str = ""
    adapter_version: str = "0"
    root_cause_taxonomy: tuple[str, ...] = ()

    # --- API surface -------------------------------------------------------

    def load_labels(self, input_path: Path) -> LabelIndex:
        raise NotImplementedError

    def iter_candidate_cases(
        self,
        input_path: Path,
        labels: LabelIndex,
        *,
        max_cases: int | None = None,
        seed: int = 0,
    ) -> Iterator[CandidateCase]:
        raise NotImplementedError

    def classify_root_cause(
        self,
        log_slice: list[str],
        anomaly_lines: list[int],
    ) -> str:
        raise NotImplementedError

    def select_slice(
        self,
        full_log: list[str],
        anomaly_indices: list[int],
        seed: int,
    ) -> LogSlice:
        raise NotImplementedError

    # --- shared helpers ----------------------------------------------------

    def case_id(self, slice_: LogSlice, anomaly_lines: list[int]) -> str:
        """Deterministic SHA-256 over the dataset + adapter version + slice +
        anomaly lines. Pure function — same inputs => same id, forever."""
        canonical = "|".join(
            [
                self.dataset_name,
                self.adapter_version,
                str(slice_.offset),
                str(slice_.length),
                ",".join(str(n) for n in sorted(anomaly_lines)),
            ]
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def validate_root_cause(self, value: str) -> str:
        if value not in self.root_cause_taxonomy:
            raise ValueError(
                f"root_cause {value!r} not in {self.dataset_name} taxonomy "
                f"{self.root_cause_taxonomy!r}"
            )
        return value
