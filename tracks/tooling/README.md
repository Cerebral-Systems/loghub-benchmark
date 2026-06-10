# Tooling track (unscored)

The 20 log-template-extraction (`tmpl-*`) tasks live here, **outside the
scored leaderboard set**, for two reasons documented in
[docs/data-provenance.md](../../docs/data-provenance.md):

1. **Contamination** — their ground truth derives from the published
   Loghub-2k structured CSVs (public since 2023, plausibly in LLM
   training data).
2. **Mechanizable** — the task is solvable by a ~30-line deterministic
   Drain-style templater (validated: 17/20 full pass with no model),
   so it measures tooling presence rather than investigation skill.

They remain useful as an agentic "can the agent write and run a
clustering script" exercise and keep their oracle=1.0 invariant, which
the test suite still enforces. Run them directly:

```bash
harbor run -p tracks/tooling/tmpl-hdfs-mix-3ac1e1c --agent oracle
```
