# Codex Run Summary

## Run: 2026-05-17 19:38 (+08)

### Scope
- Refreshed the committed Loghub-SRE Harbor benchmark so the 60-task set is network-enabled, reproducible from a curated manifest, lighter to review, and validated end to end on the Hetzner machine at `/home/buildout/loghub-benchmark`.

### Changes
- Switched generated tasks and `ci_checks/check-allow-internet.sh` to require explicit `allow_internet = true` while keeping canary, oracle-leak, and verifier-only ground-truth protections.
- Added `evidence_validation` to generated `expected.json`: exact `(file, line)` validation for HDFS/Hadoop/OpenStack, inline alert-tag validation for BGL/Thunderbird.
- Reworked BGL partitioning from rack modulo buckets to full node/location-token buckets, removing one-file BGL tasks from the curated set.
- Bumped Hadoop adapter to v2 with deterministic, root-cause-specific evidence selection capped at 50 lines.
- Added `tools/case_builder/curated_selection.json`, `tools/case_builder/rebuild_curated.py`, `make rebuild-curated`, and `just rebuild-curated` for exact curated-set regeneration.
- Replaced the uncommitted `/tmp/validate-task.sh` dependency with committed `tools/validate_task.sh`.

### How It Works Now
- Case builders emit candidate JSON from full Loghub corpora; `rebuild_curated refresh-from-existing` preserves the published distribution and writes the curated manifest.
- The exporter writes multi-file Harbor tasks with network-enabled task metadata, compact expected files, root-cause-filtered oracle hints, and fractional reward based on passed / non-skipped verifier tests.
- `make oracle-nop` calls `tools/validate_task.sh`, which prefers `.venv-tools/bin/harbor` when present and validates each task with oracle and nop agents.

### Files Touched
- `tools/case_builder/export_to_harbor.py` for network policy, evidence validation modes, BGL partitioning, verifier template, and oracle hints.
- `tools/case_builder/adapters/hadoop.py` for v2 compact evidence selection.
- `tools/case_builder/rebuild_curated.py` and `tools/case_builder/curated_selection.json` for reproducible curation.
- `ci_checks/check-allow-internet.sh` and `ci_checks/check-oracle-leak.sh` for static policy alignment.
- `tools/validate_task.sh`, `Makefile`, and `justfile` for local and remote validation entry points.
- `tasks/` regenerated to preserve 18 HDFS, 12 Hadoop, 15 BGL, 10 Thunderbird, and 5 OpenStack tasks.
- `README.md`, `CONTRIBUTING.md`, `REVIEWING.md`, `TASK_REVIEW_AUTOMATION.md`, and `docs/*.md` for policy, scoring, baselines, and handoff updates.

### Validation
- Hetzner: `.venv-tools/bin/python -m pytest tools/case_builder/tests tests/test_repo_invariants.py -q` -> `266 passed`.
- Hetzner: `make static` -> `static checks: 60 tasks x 12 checks all green`.
- Hetzner: `make oracle-nop` -> `oracle/nop: 60/60 green`.
- Local audit: 60 tasks with distribution `18/12/15/10/5`, no bad inline-label tasks, and max `expected.json` size 4028 bytes.

### Risks / Follow-ups
- Moonshot rubric refresh was attempted because a key existed, but the account returned an insufficient-balance/quota error before completing the first task. `docs/rubric-pass-report.md` remains a historical report until billing is restored.
- No paid real-agent baseline sweep was run; `docs/baselines.md` keeps Mesh/OpenSRE context separate from Harbor task validity.
