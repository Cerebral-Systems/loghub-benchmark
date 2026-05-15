# BGL alert taxonomy

BGL marks each log line with a 0th-column alert tag — `-` for normal and a
short code (e.g. `KERNDTLB`, `APPSEV`) for anomalies. The full corpus
contains ~30 distinct alert codes with a heavy long tail. PLAN.md M2c
specifies "top ~10 alert categories by frequency (collapse rare ones into
`other_alert`)".

This file is the source of truth for the taxonomy. Bumping it requires
bumping `BGLAdapter.adapter_version` so prior case_ids stay invalidated.

## Frequency basis

Tallied across the full `BGL.log` (4,747,963 lines, 348,460 non-`-` lines)
at corpus SHA-256 captured in `docs/data-setup.md`.

| Rank | Tag | Count | Family | Description |
|---|---|---|---|---|
| 1 | `KERNDTLB`  | 152,734 | kernel | Data TLB miss / address translation error |
| 2 | `KERNSTOR`  |  63,491 | kernel | Storage controller error |
| 3 | `APPSEV`    |  49,651 | application | Severe application error |
| 4 | `KERNMNTF`  |  31,531 | kernel | Mount failure |
| 5 | `KERNTERM`  |  23,338 | kernel | Termination event |
| 6 | `KERNREC`   |   6,145 | kernel | Recoverable kernel error |
| 7 | `APPREAD`   |   5,983 | application | Read failure |
| 8 | `KERNRTSP`  |   3,983 | kernel | Runtime support fault |
| 9 | `APPRES`    |   2,370 | application | Application restart event |
| 10 | `APPUNAV`  |   2,048 | application | Application unavailable |

Anything outside this list collapses to **`other_alert`**.

## Adapter mapping

`BGLAdapter.root_cause_taxonomy` mirrors this list in the same order
(plus `other_alert`). The 0th-column tag becomes the root cause directly:

```text
KERNDTLB  → kerndtlb
KERNSTOR  → kernstor
APPSEV    → appsev
KERNMNTF  → kernmntf
KERNTERM  → kernterm
KERNREC   → kernrec
APPREAD   → appread
KERNRTSP  → kernrtsp
APPRES    → appres
APPUNAV   → appunav
anything else (non-`-`) → other_alert
```

Lowercase slugs are used to fit the `[a-z][a-z0-9-]+` slug convention
expected by Harbor's task naming rules; they round-trip via
`BGLAdapter._tag_to_slug`.
