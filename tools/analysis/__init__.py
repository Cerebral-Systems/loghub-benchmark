"""Phase 5 analysis tools for Loghub-SRE benchmark runs.

Modules:

- summarize_runs:   aggregate Harbor run/jobs directories into a single
                    table of per-task / per-eval reward stats.
- diff_oracle_agent: compare an agent's /app/answer.json (or per-trial
                    extraction) against the task's tests/expected.json
                    and emit a per-field diff summary.
- failure_modes:    classify pytest assertion failures from ctrf.json
                    into stable failure-mode buckets (snippet mismatch,
                    wrong root_cause, wrong mitigation, etc.).
- quality_report:   render a human-readable Markdown report from the
                    other three modules' outputs.
"""
