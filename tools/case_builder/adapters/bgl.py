"""BGL adapter — Blue Gene/L supercomputer log.

Inputs:
  - `BGL.log`: one event per line; the 0th whitespace-delimited token is
    the alert tag — `-` for normal, otherwise a short code (KERNDTLB,
    APPSEV, KERNSTOR, ...).

Slice strategy: 5k-15k line windows containing at least one non-`-`
line. Each anomaly-bearing window becomes one candidate case. Root
cause maps directly from the alert tag of the dominant non-`-` line
(see `bgl_taxonomy.md`).
"""

from __future__ import annotations

import bisect
import hashlib
from pathlib import Path
from typing import Iterator

from .base import AdapterBase, CandidateCase, LabelIndex, LogSlice
from .fp_classifier import classify_fp_line, is_scary_line

# Sized for whole-corpus runs; tests monkeypatch these.
MIN_SLICE_LINES = 5_000
MAX_SLICE_LINES = 15_000

# FP windows are smaller and require all-`-` lines.
FP_SLICE_LINES = 5_000
FP_MIN_INDICATORS = 3
FP_MAX_INDICATORS = 5

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
    # Subclasses (e.g. ThunderbirdAdapter) override these four class attrs
    # plus root_cause_taxonomy to inherit BGL's inline-tag slicing logic
    # without reimplementing it.
    LOG_FILENAMES: tuple[str, ...] = ("BGL.log", "BGL_2k.log")
    TOP_TAGS: tuple[str, ...] = TOP_TAGS
    TAG_TO_SLUG: dict[str, str] = TAG_TO_SLUG
    OTHER_SLUG: str = _OTHER_SLUG
    root_cause_taxonomy = tuple([*sorted(TAG_TO_SLUG.values()), _OTHER_SLUG])

    # --- label loading -----------------------------------------------------

    def load_labels(self, input_path: Path) -> LabelIndex:
        """LabelIndex.entries[line_index_str] = alert_tag (raw, including '-').

        BGL has no separate label file; the alert tag is inline. We still
        emit a LabelIndex so the adapter contract is uniform across datasets.
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

    def _locate_log(self, input_path: Path) -> Path:
        for name in self.LOG_FILENAMES:
            candidate = input_path / name
            if candidate.is_file():
                return candidate
        if input_path.is_file():
            return input_path
        raise FileNotFoundError(
            f"{self.dataset_name} log not found under {input_path}; "
            f"tried: {', '.join(self.LOG_FILENAMES)}"
        )

    # --- case iteration ----------------------------------------------------

    def iter_candidate_cases(
        self,
        input_path: Path,
        labels: LabelIndex,
        *,
        max_cases: int | None = None,
        seed: int = 0,
    ) -> Iterator[CandidateCase]:
        """Stream the log twice to keep memory bounded.

        BGL is 743 MB and HDFS is 1.5 GB; both fit in RAM. Thunderbird is
        30 GB. Loading the full log into a Python list would OOM the VM,
        so this method:
          1. Counts total lines with a one-pass scan (cheap, sequential).
          2. Plans every slice deterministically using only line numbers.
          3. Re-streams the file once, filling per-plan buffers as line
             indices fall inside each plan's window.
          4. Yields cases in the original priority order so case_id list
             order stays stable.
        """
        log_path = self._locate_log(input_path)

        n_lines = self._count_lines(log_path)
        anomaly_indices_all = sorted(int(k) for k in labels.entries)
        if not anomaly_indices_all:
            return

        plans = self._plan_slices(
            n_lines=n_lines,
            anomaly_indices_all=anomaly_indices_all,
            seed=seed,
            max_cases=max_cases,
        )
        if not plans:
            return

        self._fill_plan_buffers(log_path, plans)

        for plan in plans:
            offset = plan["offset"]
            length = len(plan["buffer"])
            slice_ = LogSlice(lines=tuple(plan["buffer"]), offset=offset, length=length)
            # The plan was built assuming a window of plan["length"]; if
            # the file ended sooner the buffer is shorter, so re-derive
            # the in-window anomalies from what we actually captured.
            left = bisect.bisect_left(anomaly_indices_all, offset)
            right = bisect.bisect_left(anomaly_indices_all, offset + length)
            in_window = anomaly_indices_all[left:right]
            if not in_window:
                continue
            anomaly_lines = [(idx - offset) + 1 for idx in in_window]
            root_cause = self.classify_root_cause(list(slice_.lines), anomaly_lines)
            yield CandidateCase(
                case_id=self.case_id(slice_, anomaly_lines),
                dataset_name=self.dataset_name,
                adapter_version=self.adapter_version,
                slice=slice_,
                anomaly_line_ids=tuple(anomaly_lines),
                root_cause=root_cause,
                anomaly_keys=tuple(
                    labels.entries[str(idx)] for idx in in_window[:5]
                ),
                extra={"slice_seed": plan["slice_seed"], "anchor": plan["anchor"]},
            )

    @staticmethod
    def _count_lines(log_path: Path) -> int:
        with log_path.open(errors="replace") as fh:
            return sum(1 for _ in fh)

    def _plan_slices(
        self,
        *,
        n_lines: int,
        anomaly_indices_all: list[int],
        seed: int,
        max_cases: int | None,
    ) -> list[dict]:
        """Compute slice geometry and dedup overlapping windows. Returns
        the plans in priority order (i.e. the order cases will be yielded)."""
        order = self._deterministic_order(anomaly_indices_all, seed)
        plans: list[dict] = []
        covered: set[int] = set()
        # anomaly_indices_all is sorted; use bisect for O(log n) window queries
        # so per-anchor planning stays cheap even with millions of anomalies
        # (Thunderbird has ~3.2M).
        for anchor in order:
            if anchor in covered:
                continue
            slice_seed = self._mix_seed(seed, anchor)
            offset, length = self._compute_slice_geometry(
                n_lines=n_lines, anchor=anchor, seed=slice_seed
            )
            left = bisect.bisect_left(anomaly_indices_all, offset)
            right = bisect.bisect_left(anomaly_indices_all, offset + length)
            in_window = anomaly_indices_all[left:right]
            if not in_window:
                continue
            covered.update(in_window)
            plans.append({
                "anchor": anchor,
                "offset": offset,
                "length": length,
                "slice_seed": slice_seed,
                "buffer": [],
            })
            if max_cases is not None and len(plans) >= max_cases:
                break
        return plans

    @staticmethod
    def _fill_plan_buffers(log_path: Path, plans: list[dict]) -> None:
        """Single linear pass over the log; deposits each line into every
        plan whose window covers it. Plans are kept in their original
        priority order; we just iterate them in offset order during the scan."""
        sorted_by_offset = sorted(plans, key=lambda p: p["offset"])
        next_idx = 0
        active: list[dict] = []
        with log_path.open(errors="replace") as fh:
            for line_no, raw in enumerate(fh):
                while next_idx < len(sorted_by_offset) and sorted_by_offset[next_idx]["offset"] == line_no:
                    active.append(sorted_by_offset[next_idx])
                    next_idx += 1
                if not active:
                    if next_idx >= len(sorted_by_offset):
                        break
                    continue
                line = raw.rstrip("\n")
                still_active = []
                for plan in active:
                    if line_no < plan["offset"] + plan["length"]:
                        plan["buffer"].append(line)
                        still_active.append(plan)
                active = still_active

    @staticmethod
    def _deterministic_order(values: list[int], seed: int) -> list[int]:
        """Stable permutation: sort by SHA-256(seed|value)."""
        return sorted(values, key=lambda v: hashlib.sha256(f"{seed}|{v}".encode()).digest())

    @staticmethod
    def _mix_seed(seed: int, anchor: int) -> int:
        h = hashlib.sha256(f"{seed}|{anchor}".encode()).digest()
        return int.from_bytes(h[:8], "big")

    # --- false-positive window iteration (T1) ------------------------------

    def iter_false_positive_windows(
        self,
        input_path: Path,
        labels: LabelIndex,
        *,
        max_cases: int | None = None,
        seed: int = 0,
    ) -> Iterator[CandidateCase]:
        """Scan the log streaming, building windows of FP_SLICE_LINES
        consecutive `-` lines. For each candidate window, mine 3–5 scary
        lines and yield a case.

        We use a single pass with a sliding tail buffer so the multi-GB
        Thunderbird log doesn't have to be materialized in RAM.
        """
        log_path = self._locate_log(input_path)

        yielded = 0
        # We iterate, collecting consecutive normal-tagged lines until we
        # have FP_SLICE_LINES of them; then mine indicators, yield, and
        # reset. Note we don't reset to the next line of the log — we
        # reset to "start collecting a fresh window from scratch" so
        # cases don't overlap.
        with log_path.open(errors="replace") as fh:
            buffer: list[str] = []
            buffer_start: int = 0  # 0-based line index where buffer started
            line_no = -1
            for line_no, raw in enumerate(fh):
                line = raw.rstrip("\n")
                tag = self._tag_of(line)
                if tag != NORMAL_TAG:
                    # Anomalous line breaks the run; reset.
                    buffer = []
                    buffer_start = line_no + 1
                    continue
                if not buffer:
                    buffer_start = line_no
                buffer.append(line)
                if len(buffer) >= FP_SLICE_LINES:
                    indicators = self._mine_fp_indicators(buffer)
                    if len(indicators) >= FP_MIN_INDICATORS:
                        slice_seed = self._mix_seed(seed, buffer_start)
                        slice_ = LogSlice(
                            lines=tuple(buffer),
                            offset=buffer_start,
                            length=len(buffer),
                        )
                        yield CandidateCase(
                            case_id=self.case_id(slice_, []),
                            dataset_name=self.dataset_name,
                            adapter_version=self.adapter_version,
                            slice=slice_,
                            anomaly_line_ids=(),
                            root_cause="no_incident",
                            anomaly_keys=(),
                            extra={
                                "fp_indicators": indicators,
                                "slice_seed": slice_seed,
                            },
                            task_type="fp",
                        )
                        yielded += 1
                        if max_cases is not None and yielded >= max_cases:
                            return
                    # Reset and look for next disjoint window.
                    buffer = []
                    buffer_start = line_no + 1

    @staticmethod
    def _mine_fp_indicators(window: list[str]) -> list[dict]:
        out: list[dict] = []
        for i, line in enumerate(window):
            if is_scary_line(line):
                out.append({
                    "line": i + 1,
                    "why_not_anomalous": classify_fp_line(line),
                })
                if len(out) >= FP_MAX_INDICATORS:
                    break
        return out

    # --- slice selection ---------------------------------------------------

    def select_slice(
        self,
        full_log: list[str],
        anomaly_indices: list[int],
        seed: int,
    ) -> LogSlice:
        """In-memory variant kept for the public AdapterBase contract and
        unit tests. The case iteration path uses the streaming variant
        via `_compute_slice_geometry` + `_fill_plan_buffers` to avoid
        loading multi-GB logs into a Python list."""
        if not anomaly_indices:
            raise ValueError("select_slice requires at least one anomaly index")
        n = len(full_log)
        if n == 0:
            raise ValueError("full_log is empty")
        offset, length = self._compute_slice_geometry(
            n_lines=n, anchor=min(anomaly_indices), seed=seed
        )
        return LogSlice(lines=tuple(full_log[offset:offset + length]), offset=offset, length=length)

    @staticmethod
    def _compute_slice_geometry(*, n_lines: int, anchor: int, seed: int) -> tuple[int, int]:
        """Returns `(offset, length)` for a window of MIN_SLICE_LINES..MAX_SLICE_LINES
        that contains `anchor`. Pure function of (n_lines, anchor, seed)."""
        if n_lines == 0:
            raise ValueError("n_lines is zero")
        size = MIN_SLICE_LINES + (seed % (MAX_SLICE_LINES - MIN_SLICE_LINES + 1))
        size = min(size, n_lines)
        max_pad_before = size - 1
        pad_before = (seed >> 8) % (max_pad_before + 1) if max_pad_before > 0 else 0
        offset = max(0, anchor - pad_before)
        end = offset + size
        if end > n_lines:
            end = n_lines
            offset = max(0, end - size)
        return offset, end - offset

    # --- temporal parsing (T2) -------------------------------------------

    # BGL format: TAG epoch_ts YYYY.MM.DD RACK ...
    # Component is the alert tag (or "NORMAL" for `-`-tagged lines).
    # Lower precedence number = earlier in the causal chain. The actual
    # taxonomy is dataset-specific; we approximate with "kernel-level
    # events precede app-level events" since kernel events typically
    # trigger application failures, not the other way around.
    _COMPONENT_PRECEDENCE_PREFIXES: tuple[tuple[str, int], ...] = (
        ("KERN", 0),  # kernel-level: storage, term, etc.
        ("APP", 5),   # app-level: appsev, appres, etc.
    )

    def parse_event(self, line: str) -> dict | None:
        """Return {timestamp, component, level} for a BGL/Thunderbird line.

        Token 0 = TAG (or `-`), token 1 = epoch seconds.
        Component = TAG. Level = always "ALERT" for non-`-` lines.
        """
        parts = line.split(None, 3)
        if len(parts) < 2:
            return None
        tag = parts[0]
        try:
            ts = int(parts[1])
        except ValueError:
            return None
        component = tag if tag != "-" else "NORMAL"
        level = "ALERT" if tag != "-" else "INFO"
        return {"timestamp": ts, "component": component, "level": level}

    def component_precedence(self, component: str) -> int:
        for prefix, prec in self._COMPONENT_PRECEDENCE_PREFIXES:
            if component.startswith(prefix):
                return prec
        if component == "NORMAL":
            return 100
        return 10

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
            return self.OTHER_SLUG
        top_tags = self.TOP_TAGS

        # Rank by (count desc, taxonomy priority asc) — TOP_TAGS first.
        def priority(tag: str) -> int:
            try:
                return top_tags.index(tag)
            except ValueError:
                return len(top_tags) + 1

        top_tag = max(counts.items(), key=lambda kv: (kv[1], -priority(kv[0])))[0]
        return self.TAG_TO_SLUG.get(top_tag, self.OTHER_SLUG)
