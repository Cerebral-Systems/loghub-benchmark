# Reviewing PRs

Most quality gates are automated — by the time a PR is open, you can
trust that `make validate-all` passed on the author's machine and the
`.github/workflows/` will run the same gates in CI. Reviewing focuses
on the judgment calls the gates can't make.

## What CI already enforces

Every PR runs:

| Gate | Where | Catches |
|---|---|---|
| 12 static-check scripts × every task | `.github/workflows/static-checks.yml` → `ci_checks/check-*.sh` | canary presence, Dockerfile sanity, absolute paths, test-file references, task.toml field set, slug length, GPU types, explicit network-enabled policy |
| Anti-leak + canary-everywhere + oracle-derives | `ci_checks/check-oracle-leak.sh`, `check-canary-everywhere.sh`, `check-oracle-derives.sh` | ground-truth leaking into the agent-visible environment, forgotten canaries in author-added files, `solve.sh` short-circuits |
| Harbor oracle/nop validation | `.github/workflows/validate-task.yml` | `harbor run --agent oracle` reward=1, `--agent nop` reward=0 per task |
| Adapter + exporter unit tests | `make unit` → `tools/case_builder/tests/test_*` | adapter contract regressions, exporter schema drift, slug stability |
| Repo invariants | `tests/test_repo_invariants.py` | `case_ids` match the snapshot, `task.toml` parses with harbor's TaskConfig, oracle's derive_answer.py produces a valid answer per dataset |
| Rubric grader (manual) | `.github/workflows/review.yml` → `harbor check` (or `tools/rubric_check/moonshot_check.py` for the Moonshot path) | 28-criterion Harbor implementation rubric |

If any gate fails, the PR is not ready — you can request changes
without opening any file.

## What you focus on

### For a new dataset adapter PR

1. **Slice quality.** Read a few of the generated `tasks/<slug>/`
   directories. Is the slice agentic — does it force the agent to grep
   across files instead of one-shotting? Does the anomalous evidence
   actually concentrate in one or two files? Are the partitions
   semantically meaningful for a real SRE (datanode-1 vs datanode-2,
   nova-api vs nova-compute) rather than random buckets?
2. **Taxonomy soundness.** Open the `<dataset>_taxonomy.md` doc. Does
   the mapping reflect the dataset's actual fault families, or is it
   forcing the data into someone else's schema? Are the slug forms
   reasonable for the rest of the pipeline (no underscores, no
   hyphens that break the three-token slug rule)?
3. **Fixture coverage.** Check
   `tools/case_builder/tests/fixtures/<dataset>/` — does the fixture
   include at least one example of every taxonomy label, plus a few
   normal lines? If the unit tests pass on the fixture, does the
   adapter actually work on the real corpus? Spot-check one
   real-corpus run.
4. **Diversity in the curated set.** If the dataset's natural
   anomaly distribution is heavily skewed (Thunderbird is 99.6% VAPI),
   does the curated 60-task set still include rare categories? Or has
   the author called that out as a known limitation in their
   `<dataset>_taxonomy.md`?

### For an adapter-improvement PR

1. **Adapter version bump?** Any change to slice geometry, root-cause
   classification, or label loading must bump `adapter_version` AND
   regenerate `tests/snapshots/case_ids.json` in the same commit. If
   the snapshot drifted but the version didn't bump, request a fix.
2. **Determinism still holds.** Pull the branch and run
   `python -m tools.case_builder.build_cases --adapter <name>
   --seed 0 ...` twice into different output dirs; the manifest's
   `case_id` field must be byte-identical across runs. For the
   committed 60-task set, `make rebuild-curated` must reproduce the
   slugs recorded in `tools/case_builder/curated_selection.json`.
3. **Migration plan.** If `case_id`s shifted, every task under
   `tasks/<dataset>-*/` will need re-export. Did the PR include the
   regeneration? If not, the task set is stale relative to the
   adapter.

### For a tooling / exporter PR

1. **Backward compat.** The `--single-file` flag on the exporter
   exists for backward compat with the M3 layout. If your change
   removes or breaks that, call it out — there may be downstream tools
   that still expect the single-file shape.
2. **Anti-leak still tight.** The anti-leak guard in
   `_enforce_no_oracle_leak` has been refined twice for false
   positives (single English words, filenames). If you add a new
   check, make sure it doesn't reintroduce the patterns the existing
   negative test-tasks were designed to surface.
3. **Negative tests cover the new check.** Any new `ci_checks/check-*.sh`
   needs a corresponding `ci_checks/test-tasks/fail-loghub-*/`
   directory that the check rejects.

### For a docs PR

Skim for accuracy. The most common drift is between `README.md` and
the actual codebase as the schema evolves (e.g., the
`anomaly_line_ids` → `evidence: [{file, line, snippet}]` change in
M3.5 invalidated a paragraph in the README that had to be rewritten).
Cross-references between docs (`README.md` ↔
`docs/dataset-adapters.md` ↔ `docs/scoring.md`) should resolve.

## Approving / requesting changes

This benchmark is small enough that a single reviewer can usually
clear a PR in one pass. For changes that affect the case_id snapshot,
the rubric pass, or more than 10 tasks, request a second pair of
eyes — the blast radius is too large for a solo merge.

## What we don't review for

- **Per-task instruction grammar.** The instruction.md is templated;
  fixing the wording for one task means fixing it everywhere via the
  template. Don't paper over template bugs in individual tasks.
- **Rubric score on individual criteria.** The rubric grader is
  variance-prone (M7 showed the same field rated PASS in one run, N/A
  in another). What matters is the aggregate two-run pass; treat a
  one-run N/A as noise unless it correlates with a real defect.
- **Disk size of the task slices.** The Dockerfile's `COPY data/...`
  layers are unique per task and won't dedupe. Whole-repo size is
  bounded by the 60-task curation; don't try to shrink individual
  slices below the adapter's MIN_SLICE_LINES.
