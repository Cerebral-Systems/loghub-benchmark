# Baselines

This page records substrate-correctness baselines for the committed
60-task Harbor benchmark. Real-agent baselines are intentionally
deferred because they require API keys and explicit spend approval. The
oracle/nop and rubric numbers below validate that the benchmark itself
is runnable and correctly guarded; real-agent pass rates belong in a
future leaderboard.

## Oracle vs nop on the curated 60-task set

Latest refresh: **2026-05-17**, run on Hetzner at
`/home/buildout/loghub-benchmark` after the network-enabled task refresh,
BGL/Thunderbird inline-label verifier change, and Hadoop adapter v2
evidence compaction.

| Agent | Reward 1.0 | Reward 0.0 | Pass rate |
|---|---|---|---|
| `oracle` | 60 | 0 | **100.0%** |
| `nop` | 0 | 60 | **0.0%** |

The 2026-05-17 run completed 6-way in parallel with `oracle/nop:
60/60 green`.

The oracle's path:

1. `solution/solve.sh` is invoked by Harbor in the agent phase.
2. `solve.sh` calls `solution/derive_answer.py` with the visible
   `/app/*.log` files and the oracle-only `solution/oracle_hints.json`
   side-channel that carries the ground-truth `(file, line)` coords.
3. `derive_answer.py` reads each cited line out of the actual log,
   extracts a verbatim snippet, and writes the answer to `/app/answer.json`.
4. The verifier mounts `/tests/` and runs `test_state.py` against
   `/app/answer.json`. Mode-specific evidence tests skip when they do
   not apply, and reward is computed as passed / non-skipped tests.

`nop` simply doesn't run anything, so `/app/answer.json` is never
created — `test_answer_is_valid_json` fails first, reward goes to 0.

## Rubric grader (28-criterion Harbor implementation rubric)

| Run | PASS | FAIL | N/A | Unknown | Tasks with ≥1 FAIL |
|---|---|---|---|---|---|
| 1 | 1545 | **0** | 135 | 0 | **0/60** |
| 2 | 1377 | **0** | 303 | 0 | **0/60** |

Captured in `docs/rubric-pass-report.md` via the Moonshot-backed
checker (`tools/rubric_check/moonshot_check.py`). 5 adapter-spec-
retired criteria (`difficulty_explanation_quality`,
`solution_explanation_quality`, `verification_explanation_quality`,
`expert_time_estimate`, `task_readme`) get coerced from grader-FAIL
to `not_applicable` when the explanation cites a missing/empty field
— those fields were deliberately retired by the adapter-spec schema,
and penalising their absence would be wrong.

Rubric refresh note: a 2026-05-17 rerun was attempted after the task
refresh because `MOONSHOT_API_KEY` was present on Hetzner, but the
Moonshot account returned an insufficient-balance/quota error before
the first task completed. No refreshed rubric verdicts are claimed here.

## Static-check + invariant pass

Across the full 60-task set:

| Layer | Count | Status |
|---|---|---|
| Static checks per task (canary, dockerfile sanity, Dockerfile references, absolute paths, test refs, test.sh sanity, task fields, slug, timeout, instruction timeout, gpu types, allow-internet) | 12 × 60 = 720 | all green |
| Unit tests and repo invariants (`tools/case_builder/tests/` + `tests/test_repo_invariants.py`, including oracle-leak and oracle-derivation samples) | 266 | all green |
| Negative test-tasks under `ci_checks/test-tasks/fail-loghub-*/` | 4 | each fails the right check |

## Real-agent baselines — not in this report

To run a real LLM-agent trial across the 60 tasks, the canonical
command is:

```bash
harbor run -p tasks/<slug> \
    --agent claude-code -m anthropic/claude-opus-4-7
```

That requires:

- `ANTHROPIC_API_KEY` set in the calling shell (harbor's `quality_checker`
  module hardcodes the check, so the Moonshot/Kimi route doesn't help
  here).
- model/API budget approval. A single 60-task sweep can be non-trivial
  depending on the agent, model, retries, and reasoning settings.

No paid real-agent sweep is included in this report. When an Anthropic
key or another supported agent setup is authorised, the baselines can
be regenerated and this doc replaced with real pass-rates per agent,
model, and reasoning setting.

`.github/workflows/run-trials.yml` is the manual-dispatch path for
running this from CI.

## How to update this doc

1. Run the baseline workflow: `harbor run -p tasks/* --agent <agent>
   -m <model> -k 3 --jobs-dir <jobs>`.
2. Compute pass@1 / pass@3 / per-dataset / per-root-cause aggregates
   from the resulting Harbor `result.json` files.
3. Drop the table here and link the raw `result.json` files for
   reproducibility.

Until then this file documents the substrate-correctness baselines
only.
