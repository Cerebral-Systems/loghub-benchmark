"""OpenStack adapter — turns Loghub's OpenStack corpus into Harbor task candidates.

Inputs (Zenodo OpenStack.tar.gz layout):
  - `openstack_normal1.log` (52k lines, no anomalies)
  - `openstack_abnormal.log` (18k lines, contains injected anomalies)
  - `openstack_normal2.log` (137k lines, no anomalies)
  - `anomaly_labels.txt` (4 VM instance UUIDs with injected faults)

Slice strategy: concatenate normal1 + abnormal + normal2 into a virtual
full log so the agent must locate the anomalous instance amongst real
benign nova/neutron traffic. Each anomalous VM UUID anchors K case
variants (different seed-derived window offsets) so we can produce >=10
candidate cases from the 4 instances the corpus ships with.

Root-cause taxonomy:
  - vm_task_failure
  - network_error
  - image_pull_failure
  - other
"""

from __future__ import annotations

import bisect
import hashlib
import re
from pathlib import Path
from typing import Iterator

from .base import AdapterBase, CandidateCase, LabelIndex, LogSlice
from .fp_classifier import classify_fp_line, is_scary_line

MIN_SLICE_LINES = 2_000
MAX_SLICE_LINES = 8_000

FP_SLICE_LINES = 3_000
FP_MIN_INDICATORS = 3
FP_MAX_INDICATORS = 5

INSTANCE_RE = re.compile(r"\[instance:\s*([0-9a-f-]{36})\]")

ROOT_CAUSE_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    # Order matters: more-specific patterns first.
    (re.compile(r"glance|Unknown base file|imagecache|image fetch|image .* not found", re.IGNORECASE), "image_pull_failure"),
    (re.compile(r"neutron|port .* not found|Connection refused|network unreachable|deallocate network", re.IGNORECASE), "network_error"),
    (re.compile(r"destroy the instance|Deleting instance files|VM Stopped|task .* failed|Lifecycle Event", re.IGNORECASE), "vm_task_failure"),
)


class OpenStackAdapter(AdapterBase):
    # Coarse (app/VM-level) labels: windows carry many anomaly lines;
    # the fp-true 'subtle' ceiling must be wider or no window qualifies.
    FP_TRUE_MAX_ANOMALY_LINES = 40

    dataset_name = "OpenStack"
    adapter_version = "1"
    root_cause_taxonomy = (
        "vm_task_failure",
        "network_error",
        "image_pull_failure",
        "other",
    )
    VARIANTS_PER_INSTANCE = 3  # 4 instances * 3 variants = 12 candidate cases by default

    # --- label loading -----------------------------------------------------

    def load_labels(self, input_path: Path) -> LabelIndex:
        """Reads anomaly_labels.txt and returns an index of anomalous VM UUIDs.

        positive_labels is {"Anomaly"} for vocabulary parity with HDFS;
        the actual semantic check is `is_anomalous(uuid)` against the
        UUID set parsed from the label file.
        """
        label_file = self._locate_label_file(input_path)
        anomalous_uuids: set[str] = set()
        with label_file.open() as fh:
            for raw in fh:
                line = raw.strip()
                # Match anything that looks like a UUID v4.
                if re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", line):
                    anomalous_uuids.add(line)
        entries = {uuid: "Anomaly" for uuid in anomalous_uuids}
        return LabelIndex(entries=entries, positive_labels=frozenset({"Anomaly"}))

    @staticmethod
    def _locate_label_file(input_path: Path) -> Path:
        for c in (input_path / "anomaly_labels.txt", input_path / "anomaly_label.txt"):
            if c.is_file():
                return c
        raise FileNotFoundError(f"anomaly_labels.txt not found under {input_path}")

    # --- case iteration ----------------------------------------------------

    def iter_candidate_cases(
        self,
        input_path: Path,
        labels: LabelIndex,
        *,
        max_cases: int | None = None,
        seed: int = 0,
    ) -> Iterator[CandidateCase]:
        anomalous_uuids = sorted(labels.anomalous_keys())
        if not anomalous_uuids:
            return

        full_log = self._concatenated_log(input_path)

        # Map UUID -> sorted line indices where it appears.
        uuid_to_lines: dict[str, list[int]] = {u: [] for u in anomalous_uuids}
        for i, line in enumerate(full_log):
            for m in INSTANCE_RE.findall(line):
                if m in uuid_to_lines:
                    uuid_to_lines[m].append(i)

        # Drop UUIDs with no mentions (shouldn't happen with the published
        # corpus but stay defensive).
        uuid_to_lines = {u: lines for u, lines in uuid_to_lines.items() if lines}
        if not uuid_to_lines:
            return

        n_lines = len(full_log)
        variants = self.VARIANTS_PER_INSTANCE
        if max_cases is not None:
            # If the caller asked for fewer than n_instances cases, drop variants;
            # if more, scale variants up so we cover the request.
            n_instances = len(uuid_to_lines)
            variants = max(1, -(-max_cases // n_instances))  # ceil

        yielded = 0
        for uuid in sorted(uuid_to_lines):
            anomaly_indices = uuid_to_lines[uuid]
            for variant_idx in range(variants):
                slice_seed = self._mix_seed(seed, uuid, variant_idx)
                anchor = anomaly_indices[0]
                offset, length = self._compute_slice_geometry(
                    n_lines=n_lines, anchor=anchor, seed=slice_seed
                )
                left = bisect.bisect_left(anomaly_indices, offset)
                right = bisect.bisect_left(anomaly_indices, offset + length)
                in_window = anomaly_indices[left:right]
                if not in_window:
                    continue
                anomaly_lines = [(idx - offset) + 1 for idx in in_window]
                slice_ = LogSlice(
                    lines=tuple(full_log[offset:offset + length]),
                    offset=offset,
                    length=length,
                )
                root_cause = self.classify_root_cause(list(slice_.lines), anomaly_lines)
                yield CandidateCase(
                    case_id=self.case_id(slice_, anomaly_lines),
                    dataset_name=self.dataset_name,
                    adapter_version=self.adapter_version,
                    slice=slice_,
                    anomaly_line_ids=tuple(anomaly_lines),
                    root_cause=root_cause,
                    anomaly_keys=(uuid,),
                    extra={"slice_seed": slice_seed, "variant": variant_idx},
                )
                yielded += 1
                if max_cases is not None and yielded >= max_cases:
                    return

    # --- false-positive window iteration (T1) ------------------------------

    def iter_false_positive_windows(
        self,
        input_path: Path,
        labels: LabelIndex,
        *,
        max_cases: int | None = None,
        seed: int = 0,
    ) -> Iterator[CandidateCase]:
        """Use only `openstack_normal*.log` (excluding abnormal). Cut
        FP_SLICE_LINES-sized windows; mine scary-but-benign indicators.

        We pre-build the normal-only stream and verify no anomalous VM
        UUID appears in any candidate window.
        """
        anomalous_uuids = set(labels.anomalous_keys())
        normal_log = self._concatenated_normal_log(input_path)
        n = len(normal_log)
        if n < FP_SLICE_LINES:
            return

        yielded = 0
        candidate_offsets = list(range(0, n - FP_SLICE_LINES, FP_SLICE_LINES // 2))
        order = sorted(
            candidate_offsets,
            key=lambda o: hashlib.sha256(f"{seed}|{o}".encode()).digest(),
        )
        for offset in order:
            window = normal_log[offset:offset + FP_SLICE_LINES]
            # Defensive: skip windows that mention any anomalous UUID
            # (shouldn't happen since we only loaded normal_log, but the
            # check is cheap and catches dataset typos).
            uuids_in_window = set()
            for line in window:
                uuids_in_window.update(INSTANCE_RE.findall(line))
            if uuids_in_window & anomalous_uuids:
                continue

            indicators: list[dict] = []
            for i, line in enumerate(window):
                if is_scary_line(line):
                    indicators.append({
                        "line": i + 1,
                        "why_not_anomalous": classify_fp_line(line),
                    })
                    if len(indicators) >= FP_MAX_INDICATORS:
                        break
            if len(indicators) < FP_MIN_INDICATORS:
                continue

            slice_ = LogSlice(lines=tuple(window), offset=offset, length=FP_SLICE_LINES)
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

    @staticmethod
    def _concatenated_normal_log(input_path: Path) -> list[str]:
        """Stream openstack_normal1.log + openstack_normal2.log only
        (no abnormal). FP windows draw exclusively from these files so the
        ground truth `is_incident: false` is sound."""
        parts: list[str] = []
        for name in ("openstack_normal1.log", "openstack_normal2.log"):
            path = input_path / name
            if path.is_file():
                with path.open(errors="replace") as fh:
                    parts.extend(line.rstrip("\n") for line in fh)
        if not parts:
            raise FileNotFoundError(
                f"OpenStack normal log files not found under {input_path}"
            )
        return parts

    # --- helpers -----------------------------------------------------------

    @staticmethod
    def _concatenated_log(input_path: Path) -> list[str]:
        """Stitch the three published files into one stream in the
        canonical normal1 + abnormal + normal2 order. The OpenStack
        corpus is only ~207k lines / 60 MB so loading it whole is fine."""
        parts = []
        for name in ("openstack_normal1.log", "openstack_abnormal.log", "openstack_normal2.log"):
            path = input_path / name
            if path.is_file():
                with path.open(errors="replace") as fh:
                    parts.extend(line.rstrip("\n") for line in fh)
        if not parts:
            raise FileNotFoundError(
                f"OpenStack log parts (openstack_normal*.log, openstack_abnormal.log) "
                f"not found under {input_path}"
            )
        return parts

    @staticmethod
    def _mix_seed(seed: int, uuid: str, variant_idx: int) -> int:
        h = hashlib.sha256(f"{seed}|{uuid}|{variant_idx}".encode()).digest()
        return int.from_bytes(h[:8], "big")

    @staticmethod
    def _compute_slice_geometry(*, n_lines: int, anchor: int, seed: int) -> tuple[int, int]:
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

    _OS_EVENT_RE = re.compile(
        r"^([\w-]+)\.log\S*\s+"  # service.log prefix
        r"(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2}):(\d{2})\.(\d{3})"
    )

    _COMPONENT_PRECEDENCE: dict[str, int] = {
        "nova-api": 0,
        "nova-scheduler": 1,
        "nova-conductor": 2,
        "nova-compute": 3,
        "neutron-server": 4,
        "neutron-agent": 5,
    }

    def parse_event(self, line: str) -> dict | None:
        m = self._OS_EVENT_RE.match(line)
        if not m:
            return None
        component = m.group(1)
        year, mon, day, hh, mm, ss, ms = (int(m.group(i)) for i in range(2, 9))
        ts = (
            year * 10**13
            + mon * 10**11
            + day * 10**9
            + hh * 10**7
            + mm * 10**5
            + ss * 10**3
            + ms
        )
        return {"timestamp": ts, "component": component, "level": "INFO"}

    def component_precedence(self, component: str) -> int:
        return self._COMPONENT_PRECEDENCE.get(component, 100)

    # --- AdapterBase methods we don't use in the streaming path -----------

    def select_slice(self, full_log, anomaly_indices, seed):  # pragma: no cover
        """Kept for the AdapterBase contract; iter_candidate_cases inlines
        equivalent logic to avoid building a separate LogSlice per anomaly."""
        if not anomaly_indices:
            raise ValueError("select_slice requires at least one anomaly index")
        offset, length = self._compute_slice_geometry(
            n_lines=len(full_log), anchor=min(anomaly_indices), seed=seed
        )
        return LogSlice(lines=tuple(full_log[offset:offset + length]), offset=offset, length=length)

    def classify_root_cause(
        self,
        log_slice: list[str],
        anomaly_lines: list[int],
    ) -> str:
        """First-match wins over the configured ROOT_CAUSE_PATTERNS.

        Only inspects the anomaly lines (which are the lines mentioning
        an anomalous VM UUID), so classification stays explainable: every
        returned root cause is justified by at least one cited line.
        """
        for line_no in anomaly_lines:
            idx = line_no - 1
            if 0 <= idx < len(log_slice):
                line = log_slice[idx]
                for pattern, label in ROOT_CAUSE_PATTERNS:
                    if pattern.search(line):
                        return label
        return "other"
