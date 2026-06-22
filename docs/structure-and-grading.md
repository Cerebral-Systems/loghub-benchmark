# Benchmark structure & grading

How a Loghub-SRE task is laid out, what the agent sees, and how the verifier
scores it. (For the exhaustive per-assertion list and the anti-gaming rationale,
see [scoring.md](scoring.md); for how tasks are generated, see
[dataset-adapters.md](dataset-adapters.md).)

## Task anatomy

Every task is a self-contained [Harbor](https://www.harborframework.com/docs/tasks)
task directory:

Task ids are **opaque** (`tasks/lh-<hash>/`) so the directory name leaks no
dataset or root-cause hint; `docs/task-id-map.json` maps each back to its
descriptive build slug. The 20 unscored log-template-extraction tasks live under
`tracks/tooling/` (same layout), not in `tasks/`.

```
tasks/lh-<hash>/
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

Each skill family has its own `schema_version` and answer shape. Six are
**scored** (180 tasks); template extraction ships as an **unscored tooling
track** under `tracks/tooling/`:

| Family | Count | schema_version | Answer shape |
|---|---:|---|---|
| v1 localization | 60 | `…-v2` | `evidence[]` + `anomaly_keys` + `root_cause_type` + `recommended_action` |
| false-positive (mixed) | 25 | `…-v2-fp` | verdict `is_incident` + `false_positive_indicators[]` **or** `incident_evidence[]` |
| temporal sequence | 28 | `…-v2-seq` | `timeline[]` (ordered) + trigger + roles |
| correlation | 32 | `…-v2-corr` | `root_component` + `causal_chain[]` (role, caused_by_step) |
| severity | 15 | `…-v2-sev` | `severity` (P0–P3) + `severity_justification` + `evidence[]` |
| remediation (v3) | 20 | `…-v3-remediation` | causal chain + `mitigation` (action, target) + recovered health |
| *template extraction (unscored)* | *20* | `…-v2-tmpl` | `templates[]` partitioning all lines — `tracks/tooling/` |

The false-positive family is **mixed**: ~60% benign-noise windows
(`is_incident=false`, cite `false_positive_indicators[]`) and ~40% subtle true
incidents (`is_incident=true`, cite `incident_evidence[]`), so the verdict is a
real decision, not a family constant.

## Grading

**Gate-aware fractional reward.** The verifier runs `tests/test_state.py`
(pytest) against `/app/answer.json`. Assertions are split into two classes:

- **Gates** (`test_gate_*`) — format, schema, enum-membership, citation
  integrity, and safety checks. Any gate failure zeroes the reward; passing
  gates earns **no credit**.
- **Substantive tests** — evidence-vs-ground-truth, root-cause match,
  ordering/recall floors, recovery replay. The reward written to
  `/logs/verifier/reward.txt` is `passed / non_skipped` over the substantive
  tests only — a continuous 0–1 score, uniform across all 180 tasks.

A schema-compliant answer with no real investigation scores **0.000** (the
measured zero-effort floor across all 180 tasks); the oracle scores 1.0 and
`nop` 0.0. `tests/test_gameability.py` regression-locks the floor.

**What's asserted** (per family; full list in [scoring.md](scoring.md)): valid
JSON, schema match, referenced files exist, line numbers in range, snippets
appear **verbatim** (non-empty, ≥12 chars), evidence is **within the
ground-truth set**, `root_cause_type` is in the dataset taxonomy and matches the
gold label, and `recommended_action` is in the safe set. Evidence-validation
modes:
- **exact-location** (committed scored tasks): cited `(file, line)` must be in the GT set.
- **inline-label** (legacy/future-only): each cited line's visible alert tag must map to the expected root cause, over ≥ `min_evidence_count` distinct lines.

**Anti-gaming.** Credit is bound to evidence (a slug-guessable category earns
nothing without grounded citations), empty/trivial snippets are rejected, and
`rem` recovery is graded by **replaying the declared mitigation** against a
verifier-only initial state (the agent-writable `/app/service_state.json` is not
trusted). The replay is **fault-specific**: `tests/initial_state.json` carries
the one remedy that actually fixes the fault class, so a wrong-but-active
action (restarting a process to fix a full disk) leaves the replayed cluster
broken. Regressions are locked by `tests/test_gameability.py`. See
[scoring.md → Anti-gaming hardening](scoring.md).

## Agent integration

Any agent that Harbor can run works unmodified: the contract is "read `/app`,
write `/app/answer.json`". Built-in CLI agents (`claude-code`,
`mini-swe-agent`, `codex`, …) are selected with `--agent <name>`; a custom
agent subclasses `harbor.agents.base.BaseAgent` (`name()`, `version()`,
`setup()`, `run(instruction, environment, context)` → write
`/app/answer.json` via `environment.exec`) and is selected with
`--agent-import-path module.path:ClassName`. There is intentionally **no
MCP/tool surface**: the tasks are plain files in the container, so any agent
that can run shell commands can investigate. Pin the harness to
`harbor==0.13.1` for comparable runs (`pip install '.[bench]'`).

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
