# Benchmark structure & grading

How a Loghub-SRE task is laid out, what the agent sees, and how the verifier
scores it. (For the exhaustive per-assertion list and the anti-gaming rationale,
see [scoring.md](scoring.md); for how tasks are generated, see
[dataset-adapters.md](dataset-adapters.md).)

## Task anatomy

Every task is a self-contained [Harbor](https://www.harborframework.com/docs/tasks)
task directory:

```
tasks/<slug>/
├── instruction.md         # the prompt the agent sees
├── task.toml              # Harbor metadata ([task]/[metadata]/[environment]/[agent]/[verifier])
├── environment/
│   ├── Dockerfile         # ubuntu:24.04 + python3-pytest; COPY data/* /app/
│   └── data/              # partitioned log files (+ topology/state/config/bin for rem)
│       └── <component>.log
├── solution/              # ORACLE-ONLY (never mounted in the agent phase)
│   ├── solve.sh           # oracle entrypoint
│   ├── derive_answer.py   # derives answer.json from the visible logs (no copy-the-answer)
│   └── oracle_hints.json  # (file, line) coords + root cause
└── tests/                 # VERIFIER-ONLY (never mounted in the agent phase)
    ├── test.sh            # pytest entry; writes the reward
    ├── test_state.py      # assertions against /app/answer.json
    ├── expected.json      # ground truth + evidence-validation mode
    └── initial_state.json # (rem only) pre-mitigation state for verifier-side replay
```

**Runtime visibility (Harbor contract):** the agent sees `instruction.md` and
`/app/*` (the `data/` files). It does **not** see `solution/` or `tests/`. The
verifier mounts `tests/` only during the verification phase. Every text file
carries a canary GUID; `ci_checks/check-oracle-leak.sh` enforces that no
ground-truth string leaks into `environment/`.

## Answer schema

The agent writes `/app/answer.json`. v1 localization example:

```json
{
  "schema_version": "loghub-sre-answer-v2",
  "is_incident": true,
  "evidence": [{ "file": "hdfs-datanode-a.log", "line": 47, "snippet": "Got exception while serving blk_-..." }],
  "anomaly_keys": ["blk_-..."],
  "root_cause_type": "datanode_unreachable",
  "recommended_action": "investigate"
}
```

Each of the 7 skill families has its own `schema_version` and answer shape:

| Family | schema_version | Answer shape |
|---|---|---|
| v1 localization | `…-v2` | `evidence[]` + `anomaly_keys` + `root_cause_type` + `recommended_action` |
| false-positive | `…-v2-fp` | `false_positive_indicators[]` + `why_not_anomalous` |
| temporal sequence | `…-v2-seq` | `timeline[]` (ordered) + trigger + roles |
| correlation | `…-v2-corr` | `root_component` + `causal_chain[]` (role, caused_by_step) |
| severity | `…-v2-sev` | `severity` (P0–P3) + `severity_justification` + `evidence[]` |
| template extraction | `…-v2-tmpl` | `templates[]` partitioning all lines |
| remediation (v3) | `…-v3-remediation` | causal chain + `mitigation` (action, target) + recovered health |

## Grading

**Fractional reward.** The verifier runs `tests/test_state.py` (pytest) against
`/app/answer.json` and writes `passed / non_skipped` to
`/logs/verifier/reward.txt` — a continuous 0–1 score (partial credit), uniform
across all 180 tasks.

**What's asserted** (per family; full list in [scoring.md](scoring.md)): valid
JSON, schema match, referenced files exist, line numbers in range, snippets
appear **verbatim** (non-empty, ≥12 chars), evidence is **within the
ground-truth set**, `root_cause_type` is in the dataset taxonomy and matches the
gold label, and `recommended_action` is in the safe set. Evidence-validation
modes:
- **exact-location** (HDFS / Hadoop / OpenStack): cited `(file, line)` must be in the GT set.
- **inline-label** (BGL / Thunderbird): each cited line's visible alert tag must map to the expected root cause, over ≥ `min_evidence_count` distinct lines.

**Anti-gaming.** Credit is bound to evidence (a slug-guessable category earns
nothing without grounded citations), empty/trivial snippets are rejected, and
`rem` recovery is graded by **replaying the declared mitigation** against a
verifier-only initial state (the agent-writable `/app/service_state.json` is not
trusted). Regressions are locked by `tests/test_gameability.py`. See
[scoring.md → Anti-gaming hardening](scoring.md).

## Oracle / nop contract

- `harbor run --agent oracle` → reward **1.0** on every task (the oracle derives
  the answer from the visible logs via `solution/derive_answer.py`; it never
  copies `tests/expected.json`).
- `harbor run --agent nop` → reward **0.0** on every task.

`make oracle-nop` checks both endpoints across all 180 tasks.

## Determinism, canary & CI gates

- **Deterministic** task generation: case IDs are `sha256(dataset + adapter_version + slice + anomaly lines)`; splits are salted hashes. Locked by `tests/snapshots/`.
- **Canary** GUID on every text surface (training-contamination tripwire), enforced in CI.
- **CI gates** (`.github/workflows/`): adapter/exporter/repo-invariant tests, `make static` (12 checks × 180 tasks via `ci_checks/` with negative fixtures), `make oracle-nop`, and the committed-vs-template drift gate.

## Generation

Tasks are **generated**, not hand-authored — adapters over the Loghub corpus
(`tools/case_builder/`). New tasks come from adapter additions, never one-off
hand authoring. See [dataset-adapters.md](dataset-adapters.md) and
[CONTRIBUTING.md](../CONTRIBUTING.md).
