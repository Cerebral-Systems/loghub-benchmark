# Thunderbird alert taxonomy

Thunderbird's `Thunderbird.log` uses the same inline-tag format as BGL —
0th whitespace-delimited token is `-` for normal or a short alert code.
PLAN.md M2d specifies Thunderbird "differs from BGL's" taxonomy and
should be a subclass that overrides only the mapping.

This file is the source of truth for the taxonomy. Bumping it requires
bumping `ThunderbirdAdapter.adapter_version` so prior case_ids stay
invalidated.

## Frequency basis

Tallied across the full `Thunderbird.log` (211,212,192 lines, of which
3,248,239 are non-`-`) at corpus SHA-256 captured in
[`docs/data-setup.md`](../../../docs/data-setup.md). The corpus contains
**exactly these 10 alert codes** end-to-end — unlike BGL's long tail,
Thunderbird's vocabulary is closed.

| Rank | Tag | Count | Family | Description |
|---|---|---|---|---|
| 1 | `VAPI`     | 3,229,194 | InfiniBand | Verbs API / InfiniBand fabric event |
| 2 | `PBS_CON`  |     5,318 | scheduler  | PBS scheduler connection failure |
| 3 | `MPT`      |     4,583 | storage    | LSI Logic MPT Fusion SCSI driver event |
| 4 | `EXT_FS`   |     4,022 | filesystem | ext{2,3,4} filesystem error |
| 5 | `CPU`      |     2,741 | hardware   | CPU error (thermal / cache / parity) |
| 6 | `SCSI`     |     2,186 | storage    | SCSI subsystem error |
| 7 | `ECC`      |       146 | memory     | ECC single/multi-bit memory error |
| 8 | `PBS_BFD`  |        28 | scheduler  | PBS Bidirectional Forwarding Detection event |
| 9 | `CHK_DSK`  |        13 | storage    | Disk-check error |
| 10 | `NMI`     |         8 | hardware   | Non-maskable interrupt |

Anything outside this list collapses to **`other_alert`** — kept as a
safety net even though no such lines exist in the published corpus.

## Adapter mapping

`ThunderbirdAdapter.TAG_TO_SLUG` lower-cases each tag:

```text
VAPI     → vapi
PBS_CON  → pbs_con
MPT      → mpt
EXT_FS   → ext_fs
CPU      → cpu
SCSI     → scsi
ECC      → ecc
PBS_BFD  → pbs_bfd
CHK_DSK  → chk_dsk
NMI      → nmi
anything else (non-`-`) → other_alert
```

The slugs deliberately keep underscores (rather than collapsing to
hyphens) so the family is readable in `tasks/<slug>` directory names —
e.g. `thunderbird-vapi-001`, `thunderbird-pbs_con-002`. Harbor's slug
validator accepts underscores within tokens.

## Notes for slice strategy

VAPI dominates by three orders of magnitude. A naive frequency-weighted
sample would yield ~99% VAPI cases. The case-builder's deterministic
permutation in `BGLAdapter.iter_candidate_cases` (SHA-256 over
`seed|anomaly_index`) breaks that monotone bias, but M4's curation pass
should still hand-balance the committed task set so the rarer
categories (ECC, PBS_BFD, CHK_DSK, NMI) are represented.
