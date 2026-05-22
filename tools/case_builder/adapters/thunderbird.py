"""Thunderbird adapter — subclasses BGL's inline-tagged log adapter.

Format is identical to BGL (0th whitespace token is `-` or an alert
code), but the alert vocabulary differs. This adapter subclasses BGL
and overrides only the taxonomy mapping.

The taxonomy here is the top alert codes by frequency across the full
Thunderbird.log; see `tools/case_builder/adapters/thunderbird_taxonomy.md`
for the count basis and slug mapping. Bumping the taxonomy requires
bumping `ThunderbirdAdapter.adapter_version` so prior case_ids invalidate.
"""

from __future__ import annotations

from .bgl import BGLAdapter

# Thunderbird's full alert vocabulary across the 211M-line corpus is
# exactly these 10 tags (see thunderbird_taxonomy.md). Order = priority
# for tie-breaking. No "other" tags appear in the published corpus, but
# OTHER_SLUG remains the fallback in case future data introduces new ones.
TOP_TAGS: tuple[str, ...] = (
    "VAPI",
    "PBS_CON",
    "MPT",
    "EXT_FS",
    "CPU",
    "SCSI",
    "ECC",
    "PBS_BFD",
    "CHK_DSK",
    "NMI",
)
_OTHER_SLUG = "other_alert"
TAG_TO_SLUG: dict[str, str] = {tag: tag.lower() for tag in TOP_TAGS}


class ThunderbirdAdapter(BGLAdapter):
    dataset_name = "Thunderbird"
    adapter_version = "1"
    LOG_FILENAMES = ("Thunderbird.log", "Thunderbird_2k.log")
    TOP_TAGS = TOP_TAGS
    TAG_TO_SLUG = TAG_TO_SLUG
    OTHER_SLUG = _OTHER_SLUG
    root_cause_taxonomy = tuple([*sorted(TAG_TO_SLUG.values()), _OTHER_SLUG])

    # T2 component-precedence: hardware-layer alerts (CPU, ECC, NMI) precede
    # storage-layer alerts (SCSI, CHK_DSK, EXT_FS) which precede application
    # alerts (VAPI, PBS_*, MPT).
    _TB_COMPONENT_PRECEDENCE: dict[str, int] = {
        "CPU": 0,
        "ECC": 0,
        "NMI": 0,
        "SCSI": 2,
        "CHK_DSK": 2,
        "EXT_FS": 2,
        "MPT": 4,
        "VAPI": 5,
        "PBS_BFD": 5,
        "PBS_CON": 5,
    }

    def component_precedence(self, component: str) -> int:  # type: ignore[override]
        if component == "NORMAL":
            return 100
        return self._TB_COMPONENT_PRECEDENCE.get(component, 10)
