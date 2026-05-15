# Autonomous session goal — Loghub SRE Harbor benchmark

You are running unattended in a long-lived session on Mesh's `mesh-test` VM. Your job is to execute the milestones defined in [docs/PLAN.md](PLAN.md) sequentially, top to bottom, committing after each milestone.

## Read these first, in order

1. **`CLAUDE.md`** at repo root — operational rules, decisions, canary GUID, key references.
2. **`docs/PLAN.md`** — the full milestone breakdown (M1 → M11) you are executing.
3. **The Harbor benchmark template README** — `gh api repos/harbor-framework/benchmark-template/contents/README.md --jq .content | base64 -d` — your reference for the target shape.

## Standing rules

- Execute milestones in order. Do not skip M1.
- After each milestone:
  1. Run any tests/checks required by that milestone's Definition of Done.
  2. Commit with a clear message tagged `(M<n>)`.
  3. **Do NOT push.** The remote PAT lacks Contents:write scope. Commit locally; the user will pull via SSH and push from their laptop. (If/when push is later enabled, this instruction will be updated.)
  4. Move to the next milestone.
- **One milestone per work session is acceptable.** Don't rush. Quality matters more than speed for a benchmark we intend to upstream.
- **Stop and write `STATUS.md` when blocked** on any of:
  - An "Open decision" from PLAN.md that hasn't been resolved.
  - A rubric criterion failing that you've tried 3+ times to fix.
  - A test failure you can't isolate.
  - Missing data (Loghub corpus not on disk, etc.).
  Then exit cleanly. The user will respond and you'll continue from STATUS.md.

## What "good" looks like at each checkpoint

- After M1: `bash ci_checks/check-canary.sh tasks/<any>` runs; repo layout matches template; commits clean.
- After M2 (per adapter): unit tests green; case_ids stable across runs; root-cause taxonomy documented.
- After M3: 5 sample HDFS tasks pass static + oracle/nop validation locally.
- After M4: 60 tasks under `tasks/`, all passing local validation.
- After M5: all PR-level CI gates green on a no-op PR.
- After M6: anti-leak gate catches all `ci_checks/test-tasks/`.
- After M7: `harbor check` green on all 60 tasks, twice in a row.
- After M8: invariant tests committed and passing.
- After M9: docs cross-reference cleanly; README is human-readable.
- After M10: stress pack tarball generated and `harbor run`-able.
- After M11: baselines recorded; legacy code removed; ready to submit.

## What NOT to do

- Don't add `Co-Authored-By: Claude` or "Generated with Claude Code" markers to anything. The work is the user's. (See `~/.claude/CLAUDE.md` and project `CLAUDE.md`.)
- Don't `--no-verify` past failing hooks. Fix the underlying issue.
- Don't push without verifying the branch name is correct.
- Don't `rm -rf` repo subtrees or `git reset --hard` without a clear safety check.
- Don't guess past ambiguity. Write to STATUS.md and stop.
- Don't run `harbor check` in a tight loop — each invocation is $0.10-0.30. Budget your calls.

## Toolchain reminder

- `harbor` v0.7.0 (also aliases `hb`, `hr`)
- `uv` v0.11 — use for any Python tooling
- `docker` v29 — needed for task validation
- `gh`, `git`, `python3` 3.12, `pip3`
- `ripgrep`, `jq`, `tmux`

## Starting state when this session begins

- You are on branch `autonomous-buildout-YYYYMMDD` (or whatever the launcher set).
- The branch is rebased on `origin/main`.
- `CLAUDE.md`, `docs/PLAN.md`, and `docs/AUTONOMOUS_GOAL.md` are committed (this is the bootstrap commit).
- `tasks/` is empty.
- `src/loghub_benchmark/` is intact (will be removed in M11).

Begin with M1. Read PLAN.md first.
