# Contributing to Loghub SRE benchmark

Tasks in this benchmark are **generated**, not hand-authored. The 60
tasks committed to `tasks/` come out of the case-builder
(`tools/case_builder/`) running over the Loghub corpus. The supported
contribution paths reflect that:

1. **A new dataset adapter** — to extend the benchmark with a Loghub
   dataset that isn't covered today.
2. **Improvements to an existing adapter** — tighter slicing, a new
   root-cause heuristic, expanded fixtures.
3. **Tooling around the exporter** — partitioning strategies, anti-leak
   rules, new ci_checks gates.
4. **Bug fixes / docs / tests.**

We do not accept hand-authored single tasks. Every committed task must
be reproducible by running the case-builder + exporter on a known
corpus version with a known seed — that's how
`tests/test_case_ids_stable_from_fixture` stays meaningful.

## Local setup

```bash
git clone https://github.com/<owner>/loghub-benchmark
cd loghub-benchmark
uv venv .venv-tools && source .venv-tools/bin/activate
pip install harbor pytest pytest-json-ctrf openai  # openai for the rubric grader
make unit             # adapter + exporter tests in ~5s
```

To run the harbor oracle/nop validation you also need Docker. To run
the rubric grader you need a Moonshot or Anthropic API key (see
[`docs/rubric-pass-report.md`](docs/rubric-pass-report.md) for how M7
is set up).

## Adding a new dataset adapter

The full spec lives in [`docs/dataset-adapters.md`](docs/dataset-adapters.md).
Short version:

1. Download the corpus into `/home/buildout/loghub-full/<DatasetName>/`
   and record sizes + SHA-256 in `docs/data-setup.md`.
2. Write the adapter (`tools/case_builder/adapters/<dataset>.py`)
   inheriting from `AdapterBase`. Aim for ≤200 lines.
3. Commit a tiny synthetic fixture (10–30 lines + label file) under
   `tools/case_builder/tests/fixtures/<dataset>/` and write 3+ unit
   tests in `tools/case_builder/tests/test_<dataset>_adapter.py`.
4. Register the adapter in `tools/case_builder/build_cases.py` and the
   four exporter tables in `tools/case_builder/export_to_harbor.py`
   (`DATASET_SLUG`, `DATASET_LOG_BASENAME`, `DATASET_DIFFICULTY`,
   `_PARTITIONERS`).
5. Document the root-cause taxonomy in a sibling
   `<dataset>_taxonomy.md` if the dataset has a non-trivial mapping.
6. Run `make rebuild-curated` when you need to reproduce the committed
   task set, or use `tools.case_builder.rebuild_curated refresh-from-existing`
   when intentionally refreshing the curated manifest from new case-builder
   outputs.
7. Refresh `tests/snapshots/case_ids.json` to cover the new adapter's
   fixture-derived ids.

## What "good" looks like

Every PR must pass `make validate-all`. Concretely:

- `make unit`: pytest across `tools/case_builder/tests/` and
  `tests/test_repo_invariants.py`. Currently 265 tests; new adapters
  should add 3+ unit tests and not regress any existing one.
- `make static`: 12 ci_checks/*.sh scripts × every task in `tasks/`.
  All must pass. The negative test-tasks under
  `ci_checks/test-tasks/fail-loghub-*/` must continue to fail their
  respective check (they're regression tests for the checks
  themselves).
- `make oracle-nop`: every task in `tasks/` yields
  `harbor run --agent oracle` reward=1 and `--agent nop` reward=0.
  Slow (~10–15 min at 6-way parallelism for 60 tasks).
- The Moonshot rubric grader (`tools/rubric_check/moonshot_check.py`)
  yields 0 fails on the same two-run criterion documented in
  `docs/rubric-pass-report.md`.

## What we DON'T accept

- **Hand-authored tasks** — generate via the case-builder, period.
- **Tasks without a stable case_id** — every slug under `tasks/` must
  reproduce from `(corpus, adapter_version, seed)` so the snapshot
  test stays meaningful.
- **`solve.sh` shortcuts** — solve.sh must derive the answer through
  computation on the visible logs. `cp /tests/expected.json
  /app/answer.json` is caught by `ci_checks/check-oracle-derives.sh`
  and the corresponding negative test under
  `ci_checks/test-tasks/fail-loghub-hardcoded-answer/`.
- **Disabling internet in `[environment]`** — Loghub SRE intentionally
  sets `allow_internet = true` so Harbor-compatible CLI agents can
  install runtime dependencies during the agent phase. Ground truth is
  still protected by verifier-only `expected.json`, canary checks, and
  oracle-leak checks. The `ci_checks/check-allow-internet.sh` script
  enforces explicit `true` across generated tasks.

## Adapter-version bumps

Bump `<Adapter>.adapter_version` any time you change the slice
geometry, the root-cause classification logic, or the label-loading
logic. Bumping invalidates prior `case_id`s, which means every
existing slug derived from that adapter changes — and the M8 snapshot
test will fail unless `tests/snapshots/case_ids.json` is regenerated
in the same commit. Both changes go in one commit so reviewers can
see the cause and effect together.

## Commit hygiene

- One milestone per commit when working through the long-running
  buildout branch (see `docs/PLAN.md` for the milestone list).
- Commit messages explain the *why*, not the *what* — the diff
  already shows what changed.
- Never amend a published commit; create a follow-up commit.
- No AI co-author trailers (`Co-Authored-By: Claude` etc.). The work
  is the user's.

## Reviewing

See [REVIEWING.md](REVIEWING.md). The CI gates do most of the
mechanical checking; reviewers focus on slice quality, taxonomy
soundness, and whether the adapter's fixture covers its edge cases.
