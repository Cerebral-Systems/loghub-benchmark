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


def test_seq_trigger_only_not_full_credit():
    """A timeline containing only the (correct) trigger must NOT score full
    credit — sequence reconstruction requires covering the event chain, and
    Kendall tau must not be vacuously 1.0 on <2 common events. Regression for
    the one-event seq bypass."""
    td = TASKS / "seq-hdfs-other-1f260d4"
    exp = json.loads((td / "tests" / "expected.json").read_text())
    trig = next(e for e in exp["timeline"] if e["role"] == "trigger")
    with tempfile.TemporaryDirectory() as t:
        app = Path(t) / "app"
        app.mkdir()
        H._setup_app(td, app)
        line = (app / trig["file"]).read_text(errors="replace").splitlines()[trig["line"] - 1][:120]
        ans = {"schema_version": exp["schema_version"], "is_incident": True,
               "root_cause_type": exp["root_cause_type"],
               "timeline": [{"file": trig["file"], "line": trig["line"],
                             "snippet": line, "role": "trigger", "sequence": 0}]}
        assert H.score(td, ans) < 1.0, "seq one-event scored full credit — recall gap re-opened"


def test_fp_indicators_require_snippets():
    """FP indicators with correct (file, line, why_not_anomalous) but NO
    snippet must NOT score full credit — snippets are required so the
    predictable benign locations can't be cited without reading. Regression
    for the optional-snippet bypass."""
    td = TASKS / "fp-hdfs-noise-85ae5a1"
    exp = json.loads((td / "tests" / "expected.json").read_text())
    gt = exp["false_positive_indicators"]
    ans = {"schema_version": exp["schema_version"], "is_incident": False, "confidence": 0.9,
           "false_positive_indicators": [
               {"file": i["file"], "line": i["line"], "why_not_anomalous": i["why_not_anomalous"]}
               for i in gt[:exp["min_indicator_count"]]],
           "root_cause_type": exp.get("root_cause_type", "no_incident")}
    with tempfile.TemporaryDirectory() as t:
        app = Path(t) / "app"
        app.mkdir()
        H._setup_app(td, app)
        assert H.score(td, ans) < 1.0, "fp no-snippet scored full credit — optional-snippet bypass re-opened"


# One representative task per family for the blind-floor regression.
_FLOOR_SLUGS = [
    "hdfs-datanode-0b694b5", "hadoop-machine-e087882", "bgl-kernstor-2baf5ac",
    "thunderbird-vapi-01593fb", "openstack-vmtask-2024031", "fp-hdfs-noise-85ae5a1",
    "seq-hadoop-machine-227f3f0", "corr-hadoop-machine-29cd40d",
    "sev-hdfs-other-72dc9df", "tmpl-hdfs-mix-3ac1e1c", "rem-hdfs-other-3b66455",
]


def _format_only_answer(td: Path) -> dict:
    """Zero-investigation answer: the schema skeleton from instruction.md with
    family-prior constants and EMPTY evidence/indicators/timeline/chain/templates.
    This is what a leaderboard-gaming script can produce without reading logs."""
    import re as _re
    text = (td / "instruction.md").read_text()
    m = _re.search(r"```json\s*\n(.*?)```", text, _re.DOTALL)
    raw = m.group(1)
    raw = _re.sub(r'"<[^>]*>"', '"placeholder"', raw)
    raw = _re.sub(r"<float[^>]*>", "0.5", raw)
    raw = _re.sub(r"<int[^>]*>", "0", raw)
    raw = _re.sub(r"<[^>\n\"]*>", "0", raw)
    ans = json.loads(raw)
    for k in ("evidence", "false_positive_indicators", "timeline", "causal_chain",
              "templates", "anomaly_keys"):
        if k in ans:
            ans[k] = []
    if "is_incident" in ans:
        ans["is_incident"] = not td.name.startswith("fp-")
    if "total_unique_templates" in ans:
        ans["total_unique_templates"] = 0
    return ans


@pytest.mark.parametrize("slug", _FLOOR_SLUGS)
def test_blind_floor_is_zero(slug):
    """The zero-investigation floor must stay at 0: schema compliance plus
    family priors with no evidence earns NOTHING under gate-aware scoring.
    If this regresses, structural tests have leaked back into the reward
    denominator (the pre-v1.0 floor was 0.62)."""
    td = TASKS / slug
    ans = _format_only_answer(td)
    assert H.score(td, ans) <= 0.05, (
        f"{slug}: blind format-only answer scored above the floor — "
        "gate/substantive split has regressed"
    )
