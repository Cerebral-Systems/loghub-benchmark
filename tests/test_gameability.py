"""Regression tests against reward-hacking / no-investigation answers.

For one representative task per family we assert (a) the canonical oracle
answer still scores a full 1.0 after the verifier hardening, and (b) the
degenerate/forgery answers the release audit found scoring ~0.85-1.0 now
score materially below the oracle. These lock in the WS1a-e hardening so the
exploits cannot silently return.

Known, documented limitation: BGL/Thunderbird inline-label LOCALIZATION is
inherently easy (the alert tag is in the log text), so a "smart" attacker who
greps tagged lines and pastes real snippets still scores high there. Fully
fixing that needs corpus regeneration with injected-incident ground truth
(tracked as a follow-up). We still assert the *empty-snippet* no-read path is
closed for inline.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verifier_harness as H  # noqa: E402

TASKS = Path(__file__).resolve().parent.parent / "tasks"

REP = {
    "v1_exact": "hdfs-datanode-0b694b5",
    "v1_inline": "bgl-kernstor-2baf5ac",
    "fp": "fp-hdfs-noise-85ae5a1",
    "seq": "seq-hdfs-other-1f260d4",
    "corr": "corr-hdfs-other-2015555",
    "sev": "sev-hdfs-other-72dc9df",
    "tmpl": "tmpl-hdfs-mix-3ac1e1c",
    "rem": "rem-hdfs-other-3b66455",
}


def _score_oracle(slug: str) -> float:
    td = TASKS / slug
    with tempfile.TemporaryDirectory() as t:
        app = Path(t) / "app"
        app.mkdir()
        H._setup_app(td, app)
        ans = H.oracle_answer(td, app)
    return H.score(td, ans)


@pytest.mark.parametrize("slug", REP.values(), ids=list(REP))
def test_oracle_still_scores_full(slug):
    """Hardening must not break the oracle: every family scores exactly 1.0."""
    assert _score_oracle(slug) == pytest.approx(1.0)


def _v1_degen(td: Path, app: Path, *, smart: bool) -> dict:
    exp = json.loads((td / "tests" / "expected.json").read_text())
    files = exp["files"]
    mode = exp.get("evidence_validation", {}).get("mode", "exact_location")
    n = exp["min_evidence_count"]
    rc = exp["root_cause_type"]

    def lines(f):
        return (app / f).read_text(errors="replace").splitlines()

    def snip(f, i):
        return lines(f)[i - 1][:120] if smart else ""

    ev = []
    if mode == "inline_label":
        tm = exp["evidence_validation"]["tag_to_root_cause"]
        want = next((k for k, v in tm.items() if v == rc), None)
        for f in files:
            for i, line in enumerate(lines(f), 1):
                if line.strip().split(None, 1)[:1] == [want]:
                    ev.append({"file": f, "line": i, "snippet": snip(f, i)})
                    if len(ev) >= n:
                        break
            if len(ev) >= n:
                break
    else:
        ev = [{"file": files[0], "line": i, "snippet": snip(files[0], i)} for i in range(1, n + 1)]
    return {
        "schema_version": exp["schema_version"], "is_incident": True, "evidence": ev,
        "anomaly_keys": exp.get("anomaly_keys") or ["x"], "root_cause_type": rc,
        "recommended_action": "investigate",
    }


def _sev_degen(td: Path, app: Path, *, smart: bool) -> dict:
    exp = json.loads((td / "tests" / "expected.json").read_text())
    files = exp["files"]
    n = exp["min_evidence_count"]

    def snip(i):
        return (app / files[0]).read_text(errors="replace").splitlines()[i - 1][:120] if smart else ""

    return {
        "schema_version": exp["schema_version"], "is_incident": True,
        "evidence": [{"file": files[0], "line": i, "snippet": snip(i)} for i in range(1, n + 1)],
        "anomaly_keys": exp.get("anomaly_keys") or ["x"], "root_cause_type": exp["root_cause_type"],
        "recommended_action": "investigate", "severity": exp["severity"],
        "severity_justification": exp["severity_justification"],
        "component_count": exp.get("component_count", 1),
    }


def _rem_forge(td: Path, app: Path) -> dict:
    """Old exploit: hand-write healthy /app/service_state.json + declare a
    wrong/empty mitigation."""
    exp = json.loads((td / "tests" / "expected.json").read_text())
    ss = json.loads((app / "service_state.json").read_text())
    for info in ss.get("components", {}).values():
        info["state"] = "healthy"
        info["escalated"] = False
    (app / "service_state.json").write_text(json.dumps(ss))
    return {
        "schema_version": exp["schema_version"], "is_incident": True,
        "root_component": exp["root_component"], "root_cause_type": exp["root_cause_type"],
        "causal_chain": [{"step": 0, "role": "root",
                          "component": exp["causal_chain"][0]["component"],
                          "evidence": {"file": "x", "line": 1, "snippet": ""}}],
        "mitigation": {"action": "mark_noop", "target": "NOT_THE_ROOT"},
    }


# Ceilings are set a little above measured values so the tests are stable but
# still fail loudly if a future change re-opens an exploit.
@pytest.mark.parametrize("slug,builder,ceiling", [
    ("hdfs-datanode-0b694b5", lambda td, app: _v1_degen(td, app, smart=False), 0.80),
    ("hdfs-datanode-0b694b5", lambda td, app: _v1_degen(td, app, smart=True), 0.85),
    ("bgl-kernstor-2baf5ac", lambda td, app: _v1_degen(td, app, smart=False), 0.95),
    ("sev-hdfs-other-72dc9df", lambda td, app: _sev_degen(td, app, smart=False), 0.90),
    ("sev-hdfs-other-72dc9df", lambda td, app: _sev_degen(td, app, smart=True), 0.90),
    ("rem-hdfs-other-3b66455", _rem_forge, 0.75),
])
def test_degenerate_answer_scores_below_ceiling(slug, builder, ceiling):
    td = TASKS / slug
    with tempfile.TemporaryDirectory() as t:
        app = Path(t) / "app"
        app.mkdir()
        H._setup_app(td, app)
        ans = builder(td, app)
        r = H.score(td, ans)
    assert r < ceiling, f"{slug}: degenerate answer scored {r:.3f}, expected < {ceiling}"
    assert r < 1.0, f"{slug}: degenerate answer scored a full 1.0 — exploit re-opened"


def test_empty_snippet_never_full_credit():
    """The headline exploit: empty snippets must never yield full credit."""
    td = TASKS / "hdfs-datanode-0b694b5"
    with tempfile.TemporaryDirectory() as t:
        app = Path(t) / "app"
        app.mkdir()
        H._setup_app(td, app)
        exp = json.loads((td / "tests" / "expected.json").read_text())
        # oracle locations but blank snippets:
        ev = [{"file": e["file"], "line": e["line"], "snippet": ""} for e in exp["evidence"][:exp["min_evidence_count"]]]
        ans = {"schema_version": exp["schema_version"], "is_incident": True, "evidence": ev,
               "anomaly_keys": exp.get("anomaly_keys") or ["x"],
               "root_cause_type": exp["root_cause_type"], "recommended_action": "investigate"}
        assert H.score(td, ans) < 1.0
