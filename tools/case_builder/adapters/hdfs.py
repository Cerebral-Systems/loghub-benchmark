"""HDFS_v1 adapter — turns Loghub's HDFS corpus into Harbor task candidates.

Inputs:
  - HDFS.log: raw log, one event per line, format `YYMMDD HHMMSS PID LEVEL Component: Content`.
  - preprocessed/anomaly_label.csv: BlockId,Label rows; Label is 'Normal' or 'Anomaly'.

Each anomalous block becomes one candidate case. The slice is a 10k-30k
line window around the block's log lines, padded by surrounding normal
blocks so the agent must actually search rather than scan a tiny excerpt.
"""

from __future__ import annotations

import csv
import hashlib
import re
from collections import defaultdict
from pathlib import Path
from typing import Iterator

from .base import AdapterBase, CandidateCase, LabelIndex, LogSlice
from .fp_classifier import classify_fp_line, is_scary_line

# Allowed window sizes for the agent-facing log slice.
MIN_SLICE_LINES = 10_000
MAX_SLICE_LINES = 30_000

# FP windows are smaller than v1 — they don't bracket a block's lifetime,
# just sample a normal slice with benign-noise lines. HDFS in particular
# has high anomaly density (1 mention per ~39 lines on average), so the
# longest fully-normal contiguous run is ~8K lines. Stay well under that
# to get ≥5 disjoint candidates.
FP_SLICE_LINES = 1_500
FP_MIN_INDICATORS = 3
FP_MAX_INDICATORS = 5

BLOCK_ID_RE = re.compile(r"(blk_-?\d+)")

# Root-cause classification patterns. Order matters: first match wins, so
# more-specific patterns must come first. Each entry is (regex, label).
ROOT_CAUSE_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"BLOCK\* NameSystem\.addStoredBlock: Redundant addStoredBlock"), "replication_failure"),
    (re.compile(r"Failed to add block|Adding lost block|under replication"), "replication_failure"),
    (re.compile(r"BLOCK_NOT_FOUND|block .* could not be obtained|Corrupted block"), "data_corruption"),
    (re.compile(r"Got exception while serving|writeBlock .* received exception"), "datanode_unreachable"),
    (re.compile(r"BLOCK\* NameSystem\.allocateBlock.*failed|NameNode.*shutting down"), "namenode_error"),
    (re.compile(r"SocketTimeoutException|java\.net\.SocketTimeout|timed out"), "timeout"),
)


class HDFSAdapter(AdapterBase):
    dataset_name = "HDFS_v1"
    adapter_version = "2"  # v2 caps slice span to MIN..MAX (no auto-expand for block lifetime); invalidates v1 case_ids
    root_cause_taxonomy = (
        "replication_failure",
        "data_corruption",
        "datanode_unreachable",
        "namenode_error",
        "timeout",
        "other",
    )

    # --- label loading -----------------------------------------------------

    def load_labels(self, input_path: Path) -> LabelIndex:
        label_csv = self._locate_label_csv(input_path)
        entries: dict[str, str] = {}
        with label_csv.open(newline="") as fh:
            reader = csv.DictReader(fh)
            if "BlockId" not in (reader.fieldnames or []) or "Label" not in (reader.fieldnames or []):
                raise ValueError(
                    f"{label_csv}: expected columns 'BlockId,Label', got {reader.fieldnames!r}"
                )
            for row in reader:
                block_id = row["BlockId"].strip()
                label = row["Label"].strip()
                if block_id:
                    entries[block_id] = label
        return LabelIndex(entries=entries, positive_labels=frozenset({"Anomaly"}))

    @staticmethod
    def _locate_label_csv(input_path: Path) -> Path:
        """anomaly_label.csv lives next to HDFS.log in the loghub zip layout."""
        candidates = [
            input_path / "anomaly_label.csv",
            input_path / "preprocessed" / "anomaly_label.csv",
            input_path.parent / "anomaly_label.csv",
        ]
        for c in candidates:
            if c.is_file():
                return c
        raise FileNotFoundError(
            f"anomaly_label.csv not found under {input_path}; checked: "
            + ", ".join(str(c) for c in candidates)
        )

    @staticmethod
    def _locate_log(input_path: Path) -> Path:
        candidates = [input_path / "HDFS.log", input_path / "HDFS_2k.log", input_path]
        for c in candidates:
            if c.is_file():
                return c
        raise FileNotFoundError(f"HDFS log not found under {input_path}")

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
        with log_path.open() as fh:
            full_log = fh.read().splitlines()

        block_to_lines = self._index_blocks(full_log)
        anomalous_blocks = [b for b in labels.anomalous_keys() if b in block_to_lines]
        # Stable ordering: sort by block id so the iteration is reproducible.
        anomalous_blocks.sort()

        yielded = 0
        for block_id in anomalous_blocks:
            anomaly_indices = block_to_lines[block_id]  # 0-based indices into full_log
            block_seed = self._mix_seed(seed, block_id)
            slice_ = self.select_slice(full_log, anomaly_indices, block_seed)
            anomaly_lines = self._to_slice_relative_lines(slice_, anomaly_indices)
            if not anomaly_lines:
                continue  # slice didn't contain any anomaly line; skip
            root_cause = self.classify_root_cause(list(slice_.lines), anomaly_lines)
            yield CandidateCase(
                case_id=self.case_id(slice_, anomaly_lines),
                dataset_name=self.dataset_name,
                adapter_version=self.adapter_version,
                slice=slice_,
                anomaly_line_ids=tuple(anomaly_lines),
                root_cause=root_cause,
                anomaly_keys=(block_id,),
                extra={"slice_seed": block_seed},
            )
            yielded += 1
            if max_cases is not None and yielded >= max_cases:
                return

    @staticmethod
    def _index_blocks(full_log: list[str]) -> dict[str, list[int]]:
        index: dict[str, list[int]] = defaultdict(list)
        for i, line in enumerate(full_log):
            for blk in BLOCK_ID_RE.findall(line):
                index[blk].append(i)
        return index

    @staticmethod
    def _mix_seed(seed: int, key: str) -> int:
        """Mix the global seed with a per-case key so each case picks a
        reproducible window without all cases landing on the same offset."""
        h = hashlib.sha256(f"{seed}|{key}".encode("utf-8")).digest()
        return int.from_bytes(h[:8], "big")

    @staticmethod
    def _to_slice_relative_lines(slice_: LogSlice, anomaly_indices: list[int]) -> list[int]:
        """Convert 0-based full-log indices to 1-based slice-relative line numbers."""
        return sorted(
            (idx - slice_.offset) + 1
            for idx in anomaly_indices
            if slice_.offset <= idx < slice_.offset + slice_.length
        )

    # --- false-positive window iteration (T1) ------------------------------

    def iter_false_positive_windows(
        self,
        input_path: Path,
        labels: LabelIndex,
        *,
        max_cases: int | None = None,
        seed: int = 0,
    ) -> Iterator[CandidateCase]:
        """Find the longest contiguous runs of lines whose referenced block
        IDs are ALL labeled Normal, then carve FP_SLICE_LINES windows from
        those runs. HDFS has ~17K anomalous blocks scattered through 11M
        lines (~1 anomalous mention per 65 lines on average), so contiguous
        normal-only windows are rare and must be found by gap-mining
        rather than random sampling.
        """
        log_path = self._locate_log(input_path)
        with log_path.open() as fh:
            full_log = fh.read().splitlines()

        anomalous_set = frozenset(labels.anomalous_keys())

        # For each line, decide "is_anomalous_line" = mentions any anomalous block.
        # Lines with NO block IDs are treated as anomaly-neutral (don't break a run).
        is_anomalous_line: list[bool] = []
        for line in full_log:
            mentions = BLOCK_ID_RE.findall(line)
            is_anomalous_line.append(any(b in anomalous_set for b in mentions))

        # Find maximal runs of non-anomalous lines (length ≥ FP_SLICE_LINES).
        runs: list[tuple[int, int]] = []  # (start, length)
        run_start: int | None = None
        for i, anom in enumerate(is_anomalous_line):
            if anom:
                if run_start is not None and i - run_start >= FP_SLICE_LINES:
                    runs.append((run_start, i - run_start))
                run_start = None
            else:
                if run_start is None:
                    run_start = i
        if run_start is not None and len(full_log) - run_start >= FP_SLICE_LINES:
            runs.append((run_start, len(full_log) - run_start))

        if not runs:
            return

        # Deterministically pick offsets within each long run. To avoid bunching
        # all cases into the same run, order runs by SHA-256(seed|run_start).
        ordered_runs = sorted(
            runs, key=lambda r: hashlib.sha256(f"{seed}|{r[0]}".encode()).digest()
        )

        yielded = 0
        for run_start_i, run_len in ordered_runs:
            # Each run yields up to ceil(run_len / FP_SLICE_LINES) disjoint windows.
            n_windows = run_len // FP_SLICE_LINES
            for w in range(n_windows):
                offset = run_start_i + w * FP_SLICE_LINES
                window_lines = full_log[offset:offset + FP_SLICE_LINES]

                indicators: list[dict] = []
                for i, line in enumerate(window_lines):
                    if is_scary_line(line):
                        indicators.append({
                            "line": i + 1,
                            "why_not_anomalous": classify_fp_line(line),
                        })
                        if len(indicators) >= FP_MAX_INDICATORS:
                            break
                if len(indicators) < FP_MIN_INDICATORS:
                    continue

                slice_ = LogSlice(
                    lines=tuple(window_lines), offset=offset, length=FP_SLICE_LINES
                )
                yield CandidateCase(
                    case_id=self.case_id(slice_, []),
                    dataset_name=self.dataset_name,
                    adapter_version=self.adapter_version,
                    slice=slice_,
                    anomaly_line_ids=(),
                    root_cause="no_incident",
                    anomaly_keys=(),
                    extra={"fp_indicators": indicators, "slice_seed": seed},
                    task_type="fp",
                )
                yielded += 1
                if max_cases is not None and yielded >= max_cases:
                    return

    # --- slice selection ---------------------------------------------------

    def select_slice(
        self,
        full_log: list[str],
        anomaly_indices: list[int],
        seed: int,
    ) -> LogSlice:
        """Pick a MIN..MAX-sized window anchored on the first anomaly mention.

        Earlier versions expanded the window to cover the full span of
        a block's mentions, which exploded for blocks that recur over
        millions of log lines. The current rule keeps the window size
        bounded; mentions of the same block that fall outside the
        window are simply not part of this case's anomaly set (the
        instance whose first mention anchored the window is still
        anomalous, and the agent only has to cite anomalies inside
        the slice it actually sees).
        """
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
        # Inspect only the lines flagged as anomalous; this is what the
        # agent's evidence-citation answer is checked against by the verifier.
        for line_no in anomaly_lines:
            idx = line_no - 1  # convert 1-based to 0-based
            if 0 <= idx < len(log_slice):
                line = log_slice[idx]
                for pattern, label in ROOT_CAUSE_PATTERNS:
                    if pattern.search(line):
                        return label
        return "other"
