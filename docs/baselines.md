# Baselines

This page records substrate-correctness baselines for the committed
180-task scored Harbor benchmark (60 v1 anomaly localization + 100 v2
across 4 skill axes — false-positive 25, sequence 28, correlation 32,
severity 15 — + 20 v3 outcome remediation). A 20-task log-template
extraction tooling track ships unscored under `tracks/tooling/`.
Real-agent leaderboard numbers live in the top-level `README.md`; this
doc covers only the oracle/nop and rubric gates that validate the
benchmark substrate itself.

## Oracle vs nop on the curated 180-task set

`make oracle-nop` is run as part of `make validate-all`. After the v3
remediation hardening (2026-05-24), the full set passes:

| Agent | Reward 1.0 | Reward 0.0 | Pass rate |
|---|---|---|---|
| `oracle` | 180 | 0 | **100.0%** |
| `nop` | 0 | 180 | **0.0%** |

The oracle's path:

1. `solution/solve.sh` is invoked by Harbor in the agent phase.
2. `solve.sh` calls `solution/derive_answer.py` with the visible
   `/app/*.log` files and the oracle-only `solution/oracle_hints.json`
   side-channel that carries the ground-truth `(file, line)` coords.
3. `derive_answer.py` reads each cited line out of the actual log,
   extracts a verbatim snippet, and writes the answer to `/app/answer.json`.
4. The verifier mounts `/tests/` and runs `test_state.py` against
   `/app/answer.json`. Mode-specific evidence tests skip when they do
   not apply. Reward is gate-aware: any `test_gate_*` failure zeroes the
   reward, and the score is passed / non-skipped over the substantive
   (non-gate) tests only.

`nop` simply doesn't run anything, so `/app/answer.json` is never
created — the `test_gate_answer_is_valid_json` gate fails first, reward goes to 0.

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

The two-pass rubric run captured here covers the v1 60-task set only.
The 100 v2 tasks and 20 v3 remediation tasks have not been rubric-graded
yet; they're validated via oracle/nop gates and the per-task pytest
verifier assertions.

## Static-check + invariant pass

Across the full 180-task set:

| Layer | Count | Status |
|---|---|---|
| Static checks per task (canary, dockerfile sanity, Dockerfile references, absolute paths, test refs, test.sh sanity, task fields, slug, timeout, instruction timeout, gpu types, allow-internet) | 12 × 180 = 2,160 | all green |
| Unit tests and repo invariants (`tools/case_builder/tests/` + `tests/test_repo_invariants.py` — oracle-leak, oracle-derivation, the committed-vs-template drift gate, and the ground-truth hash snapshot) + `tests/test_gameability.py` anti-reward-hacking regressions | all green |
| Negative test-tasks under `ci_checks/test-tasks/fail-loghub-*/` | each fails the right check |

## Real-agent baselines

Real-agent leaderboard runs (DeepSeek, Claude Code, Mesh) live in the
top-level `README.md`. To reproduce one of them, the canonical command
is:

```bash
harbor run -p tasks/ \
    --agent mini-swe-agent -m deepseek/deepseek-v4-flash \
    --agent-timeout-multiplier 3.0
```

Other agent/model combinations require `ANTHROPIC_API_KEY` or the
relevant provider key. `.github/workflows/run-trials.yml` is the
manual-dispatch path for running this from CI.
