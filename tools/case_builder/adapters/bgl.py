"""BGL adapter — Blue Gene/L supercomputer log.

Inputs:
  - `BGL.log`: one event per line; the 0th whitespace-delimited token is
    the alert tag — `-` for normal, otherwise a short code (KERNDTLB,
    APPSEV, KERNSTOR, ...).

PLAN.md M2c slice strategy: 5k-15k line windows containing ≥1 non-`-`
line. Each anomaly-bearing window becomes one candidate case. Root cause
maps directly from the alert tag of the dominant non-`-` line (see
`bgl_taxonomy.md`).
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Iterator

from .base import AdapterBase, CandidateCase, LabelIndex, LogSlice

# Sized for whole-corpus runs; tests monkeypatch these.
MIN_SLICE_LINES = 5_000
MAX_SLICE_LINES = 15_000

NORMAL_TAG = "-"

# Top-10 BGL alert tags by frequency (see bgl_taxonomy.md). Order matters
# for documentation but not for correctness — _tag_to_slug uses a dict.
TOP_TAGS: tuple[str, ...] = (
    "KERNDTLB",
    "KERNSTOR",
    "APPSEV",
    "KERNMNTF",
    "KERNTERM",
    "KERNREC",
    "APPREAD",
    "KERNRTSP",
    "APPRES",
    "APPUNAV",
)
_OTHER_SLUG = "other_alert"
TAG_TO_SLUG: dict[str, str] = {tag: tag.lower() for tag in TOP_TAGS}


class BGLAdapter(AdapterBase):
    dataset_name = "BGL"
    adapter_version = "1"
    root_cause_taxonomy = tuple([*sorted(TAG_TO_SLUG.values()), _OTHER_SLUG])

    # --- label loading -----------------------------------------------------

    def load_labels(self, input_path: Path) -> LabelIndex:
        """LabelIndex.entries[line_index_str] = alert_tag (raw, including '-').

        BGL has no separate label file; the alert tag is inline. We still
        emit a LabelIndex so the M2 contract is uniform across datasets.
        Keys are stringified 0-based line indices. positive_labels is
        every observed non-'-' tag, so AdapterBase.anomalous_keys() yields
        the lines that need slicing.
        """
        log_path = self._locate_log(input_path)
        entries: dict[str, str] = {}
        positive: set[str] = set()
        with log_path.open(errors="replace") as fh:
            for i, raw in enumerate(fh):
                tag = self._tag_of(raw)
                if tag and tag != NORMAL_TAG:
                    entries[str(i)] = tag
                    positive.add(tag)
        return LabelIndex(entries=entries, positive_labels=frozenset(positive))

    @staticmethod
    def _tag_of(line: str) -> str:
        line = line.strip()
        if not line:
            return ""
        return line.split(None, 1)[0]

    @staticmethod
    def _locate_log(input_path: Path) -> Path:
        for c in (input_path / "BGL.log", input_path / "BGL_2k.log", input_path):
            if c.is_file():
                return c
        raise FileNotFoundError(f"BGL log not found under {input_path}")

    # --- case iteration ----------------------------------------------------

    def iter_candidate_cases(
        self,
        input_path: Path,
        labels: LabelIndex,
        *,
        max_cases: int | None = None,
        seed: int = 0,
    ) -> Iterator[CandidateCase]:
        log_path = self._locate_log(input_path)
        with log_path.open(errors="replace") as fh:
            full_log = fh.read().splitlines()

        # Anomaly indices, sorted; we'll seed-shuffle deterministically
        # before slicing so cases aren't all clustered at the file start.
        anomaly_indices_all = sorted(int(k) for k in labels.entries)
        if not anomaly_indices_all:
            return

        order = self._deterministic_order(anomaly_indices_all, seed)
        yielded = 0
        covered: set[int] = set()
        for anchor in order:
            if anchor in covered:
                continue  # an earlier slice already swept this anomaly
            slice_seed = self._mix_seed(seed, anchor)
            slice_ = self.select_slice(full_log, [anchor], slice_seed)
            # Anomaly lines inside the slice (1-based).
            slice_anomalies_zero_based = [
                idx for idx in anomaly_indices_all
                if slice_.offset <= idx < slice_.offset + slice_.length
            ]
            if not slice_anomalies_zero_based:
                continue
            covered.update(slice_anomalies_zero_based)
            anomaly_lines = [(idx - slice_.offset) + 1 for idx in slice_anomalies_zero_based]
            root_cause = self.classify_root_cause(list(slice_.lines), anomaly_lines)
            yield CandidateCase(
                case_id=self.case_id(slice_, anomaly_lines),
                dataset_name=self.dataset_name,
                adapter_version=self.adapter_version,
                slice=slice_,
                anomaly_line_ids=tuple(anomaly_lines),
                root_cause=root_cause,
                anomaly_keys=tuple(labels.entries[str(idx)] for idx in slice_anomalies_zero_based[:5]),
                extra={"slice_seed": slice_seed, "anchor": anchor},
            )
            yielded += 1
            if max_cases is not None and yielded >= max_cases:
                return

    @staticmethod
    def _deterministic_order(values: list[int], seed: int) -> list[int]:
        """Stable permutation: sort by SHA-256(seed|value)."""
        return sorted(values, key=lambda v: hashlib.sha256(f"{seed}|{v}".encode()).digest())

    @staticmethod
    def _mix_seed(seed: int, anchor: int) -> int:
        h = hashlib.sha256(f"{seed}|{anchor}".encode()).digest()
        return int.from_bytes(h[:8], "big")

    # --- slice selection ---------------------------------------------------

    def select_slice(
        self,
        full_log: list[str],
        anomaly_indices: list[int],
        seed: int,
    ) -> LogSlice:
        if not anomaly_indices:
            raise ValueError("select_slice requires at least one anomaly index")
        n = len(full_log)
        if n == 0:
            raise ValueError("full_log is empty")

        size = MIN_SLICE_LINES + (seed % (MAX_SLICE_LINES - MIN_SLICE_LINES + 1))
        size = min(size, n)

        anchor = min(anomaly_indices)
        max_pad_before = size - 1
        pad_before = (seed >> 8) % (max_pad_before + 1) if max_pad_before > 0 else 0
        offset = max(0, anchor - pad_before)
        end = offset + size
        if end > n:
            end = n
            offset = max(0, end - size)
        actual_size = end - offset
        lines = tuple(full_log[offset:end])
        return LogSlice(lines=lines, offset=offset, length=actual_size)

    # --- root-cause classification ----------------------------------------

    def classify_root_cause(
        self,
        log_slice: list[str],
        anomaly_lines: list[int],
    ) -> str:
        """Pick the slug for the most-frequent non-'-' tag among anomaly_lines.

        Ties broken by the taxonomy order (top tags win over rarer ones).
        """
        counts: dict[str, int] = {}
        for line_no in anomaly_lines:
            idx = line_no - 1
            if 0 <= idx < len(log_slice):
                tag = self._tag_of(log_slice[idx])
                if tag and tag != NORMAL_TAG:
                    counts[tag] = counts.get(tag, 0) + 1
        if not counts:
            return _OTHER_SLUG
        # Rank by (count desc, taxonomy priority asc) — TOP_TAGS first.
        def priority(tag: str) -> int:
            try:
                return TOP_TAGS.index(tag)
            except ValueError:
                return len(TOP_TAGS) + 1
        top_tag = max(counts.items(), key=lambda kv: (kv[1], -priority(kv[0])))[0]
        return TAG_TO_SLUG.get(top_tag, _OTHER_SLUG)
