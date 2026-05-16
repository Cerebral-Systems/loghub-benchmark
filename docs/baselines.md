# Baselines

Numbers captured by the autonomous buildout during M3.5 / M4 / M11.
Real-agent (claude-code, codex, gemini) baselines are intentionally
deferred — those require API keys the autonomous session doesn't have
authorisation to spend, and the cost shape is non-trivial (~$30–80
for one trial across 60 tasks per CLAUDE.md M11 estimate). The
oracle/nop and rubric baselines are the substrate-correctness numbers;
real-agent numbers belong in the eventual leaderboard.

## Oracle vs nop on the curated 60-task set

| Agent | Reward 1.0 | Reward 0.0 | Pass rate |
|---|---|---|---|
| `oracle` | 60 | 0 | **100.0%** |
| `nop` | 0 | 60 | **0.0%** |

Both rows are documented in `commit c7a2abf` (M4 wave 3) and re-verified
after the M3.5 multi-file rework in commit `35d8699`. Validated 6-way
in parallel; raw timing was ~12 minutes for the 60-task sweep with
docker layer caching.

The oracle's path:

1. `solution/solve.sh` is invoked by Harbor in the agent phase.
2. `solve.sh` calls `solution/derive_answer.py` with the visible
   `/app/*.log` files and the oracle-only `solution/oracle_hints.json`
   side-channel that carries the ground-truth `(file, line)` coords.
3. `derive_answer.py` reads each cited line out of the actual log,
   extracts a verbatim snippet, and writes the answer to `/app/answer.json`.
4. The verifier mounts `/tests/` and runs `test_state.py` against
   `/app/answer.json`. All 12 assertions pass.

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
— those fields were deliberately retired per CLAUDE.md's adapter-
spec corrections, and penalising their absence would be wrong.

## Static-check + invariant pass

Across the full 60-task set:

| Layer | Count | Status |
|---|---|---|
| Static checks per task (canary, dockerfile sanity, absolute paths, test refs, test.sh sanity, task fields, slug, timeout, instruction timeout, gpu types, allow-internet, plus M6's oracle-leak/canary-everywhere/oracle-derives) | 15 × 60 = 900 | all green |
| Unit tests (`tools/case_builder/tests/` + `tests/test_repo_invariants.py`) | 263 | all green |
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
- `MODEL_*` budget approval; PLAN.md M11 estimates $20–50 per single
  trial × 60-task sweep with Opus, scaling roughly linearly with
  reasoning_effort.

The autonomous buildout session deliberately stopped short of
spending unspecified API budget. When the user wires up the Anthropic
key (or authorises a different per-agent setup), the M11 baselines
can be regenerated and this doc replaced with real pass-rates per
agent × model × reasoning_effort cell.

`.github/workflows/run-trials.yml` is the manual-dispatch path for
running this from CI.

## How to update this doc

1. Run the baseline workflow: `harbor run -p tasks/* --agent <agent>
   -m <model> -k 3 --jobs-dir <jobs>` (PLAN.md M11 specifies 3
   attempts per task).
2. Run `tools/leaderboard/` (the M11 follow-up tool) over `<jobs>` to
   compute pass@1 / pass@3 / per-dataset / per-root-cause aggregates.
3. Drop the table here, link the raw `result.json` files for
   reproducibility.

Until then this file documents the substrate-correctness baselines
only.
