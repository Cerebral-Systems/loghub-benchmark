# Rubric-Pass Report

> Refresh note (2026-05-17): this report is the last completed two-pass
> Moonshot rubric run. A rerun after the network-enabled task refresh was
> attempted on Hetzner, but the configured Moonshot account returned an
> insufficient-balance/quota error before the first task completed. Do not
> treat the tables below as refreshed verdicts for the regenerated task set.

**Date:** 2026-05-16
**Grader:** `moonshot-v1-128k` via Moonshot's OpenAI-compat endpoint
**Checker:** `tools/rubric_check/moonshot_check.py` (custom because `harbor check`
is hardwired to Anthropic's Claude Agent SDK and Moonshot doesn't satisfy
Claude Code's streaming/tool-use shape).
**Tasks evaluated:** 60 — every task under `tasks/`.

## Headline

**0 failures across all 60 tasks on both runs.** Every committed task
passes every applicable rubric criterion.

| Run | Pass | Fail | N/A | Unknown | Tasks with ≥1 FAIL |
|---|---|---|---|---|---|
| 1 | 1545 | **0** | 135 | 0 | **0/60** |
| 2 | 1377 | **0** | 303 | 0 | **0/60** |

The run-2 N/A count is higher because the grader's interpretation of
the adapter-spec-retired criteria varies between runs (sometimes PASS
based on the `[metadata].difficulty` enum, sometimes N/A because the
literal field is gone). Both outcomes are acceptable for our schema.

## Why `harbor check` was replaced

`harbor check` requires `ANTHROPIC_API_KEY` and routes through Claude
Code's tool-use streaming. Moonshot's Anthropic-compat endpoint at
`api.moonshot.ai/anthropic` exposes `/v1/messages` but doesn't satisfy
Claude Code's expectations (tested at runtime — returns
`Exception: Claude Code returned an error result: success`). To stay
within the moonshot/kimi API budget the user wired up, we wrote a
parallel rubric checker that:

1. Loads the same `rubrics/task-implementation.toml`.
2. Builds the same prompt as `harbor check` would (using the upstream
   `check_prompt.txt` template, with task file contents inlined instead
   of letting the grader issue Read/Glob/Grep tool calls).
3. Calls Moonshot's OpenAI-compatible API with structured-JSON output.
4. Writes per-task JSON in the same shape `harbor check -o ...` does.

Apart from the transport, the rubric prompt and the per-criterion
verdicts are equivalent to what `harbor check` would have produced.

## Adapter-spec retired criteria

Five criteria in the vendored rubric protect task.toml fields that this
benchmark deliberately retired:

- `difficulty_explanation_quality` → replaced by `[metadata].difficulty` enum
- `solution_explanation_quality` → no longer required
- `verification_explanation_quality` → no longer required
- `expert_time_estimate` → no longer required
- `task_readme` → optional, intentionally omitted

The grader is given an explicit note in the prompt to mark these
`not_applicable` rather than `fail`. To insulate against grader
variance, `moonshot_check.py` post-processes verdicts: if one of these
five criteria is rated `fail` with an explanation that boils down to
"the field is missing/empty/retired", the verdict is coerced to
`not_applicable` (with a `[coerced] Adapter-spec retired ...` prefix on
the explanation so the substitution is auditable).

Without coercion, run 1 had 6 fails on 3 tasks (all six were
`solution_explanation_quality` or `verification_explanation_quality`
flagged for empty fields). After coercion: 0 fails.

## Run 1 — per-criterion outcomes (60 tasks × 28 criteria = 1680 verdicts)

| Criterion | PASS | FAIL | N/A |
|---|---|---|---|
| agentic | 60 | 0 | 0 |
| anti_cheat_robustness | 60 | 0 | 0 |
| category_and_tags | 60 | 0 | 0 |
| deterministic_reproducible | 60 | 0 | 0 |
| difficult | 60 | 0 | 0 |
| difficulty_explanation_quality | 53 | 0 | 7 |
| environment_hygiene | 60 | 0 | 0 |
| essential_difficulty | 60 | 0 | 0 |
| expert_time_estimate | 35 | 0 | 25 |
| functional_verification | 60 | 0 | 0 |
| instruction_concision | 60 | 0 | 0 |
| interesting | 60 | 0 | 0 |
| novel | 60 | 0 | 0 |
| outcome_verified | 60 | 0 | 0 |
| resource_configuration | 60 | 0 | 0 |
| reviewable | 60 | 0 | 0 |
| solution_explanation_quality | 29 | 0 | 31 |
| solution_quality | 60 | 0 | 0 |
| solvable | 60 | 0 | 0 |
| structured_data_schema | 60 | 0 | 0 |
| task_name | 60 | 0 | 0 |
| task_readme | 0 | 0 | 60 |
| task_security | 60 | 0 | 0 |
| task_toml_schema | 60 | 0 | 0 |
| test_instruction_alignment | 60 | 0 | 0 |
| typos | 60 | 0 | 0 |
| verifiable | 60 | 0 | 0 |
| verification_explanation_quality | 48 | 0 | 12 |

## Run 1 — per-dataset breakdown

| Dataset | Tasks | PASS verdicts | FAIL | N/A |
|---|---|---|---|---|
| HDFS | 18 | 456 | 0 | 48 |
| Hadoop | 12 | 318 | 0 | 18 |
| BGL | 15 | 376 | 0 | 44 |
| Thunderbird | 10 | 261 | 0 | 19 |
| OpenStack | 5 | 134 | 0 | 6 |

## Cost

- Run 1: 1,341,174 input tokens × 60 tasks → estimated ~$2 at Moonshot's
  list pricing.
- Run 2: similar order of magnitude.
- Total spend: roughly **$3–5**.

## Reproducing this report

```bash
set -a; . .env; set +a   # MOONSHOT_API_KEY, OPENAI_API_KEY
.venv-tools/bin/python -m tools.rubric_check.moonshot_check tasks/<slug> \
    --model moonshot-v1-128k \
    --output-dir /tmp/m7-checks
```

The per-task JSON files in `/tmp/m7-checks-run1/` and
`/tmp/m7-checks-run2/` are the raw evidence for this report. Re-running
on the full 60-task set takes ~10 minutes at 5-way parallelism.

## What didn't happen

- No iteration loop was needed beyond the one-shot retirement coercion.
  The multi-file rework and adapter-spec migration left the substrate
  already rubric-clean.
- No per-task BlockId / hostname remapping for the `novel` criterion was
  needed. The grader rated `novel = pass` 60/60 on the multi-file
  partitioned layout.
- No `difficulty` bumps. The HDFS/BGL/Thunderbird/OpenStack tasks all
  passed `difficult = pass` 60/60 with the default `medium`/`hard`
  values from `DATASET_DIFFICULTY` in `export_to_harbor.py`.
