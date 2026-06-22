"""Regression tests against reward-hacking / no-investigation answers.

For one representative task per family we assert (a) the canonical oracle
answer still scores a full 1.0 after the verifier hardening, and (b) the
degenerate/forgery answers the release audit found scoring ~0.85-1.0 now
score materially below the oracle. These lock in the WS1a-e hardening so the
exploits cannot silently return.

BGL/Thunderbird labels are stripped from agent-visible logs and scored via
exact locations, so a "smart" attacker still has to cite the committed
ground-truth coordinates with real snippets rather than grep visible tags.
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
    "v1_exact": "lh-f53d4948",
    "v1_bgl_exact": "lh-84158338",
    "fp": "lh-a67368b6",
    "seq": "lh-95c71c89",
    "corr": "lh-c3d5deec",
    "sev": "lh-72340082",
    "tmpl": "tmpl-hdfs-mix-3ac1e1c",
    "rem": "lh-26152f56",
}


def _resolve_task(slug: str) -> Path:
    """Scored tasks live in tasks/; the unscored tooling track (tmpl) keeps
    its oracle invariant from tracks/tooling/."""
    td = TASKS / slug
    if not td.exists():
        td = TASKS.parent / "tracks" / "tooling" / slug
    return td


def _score_oracle(slug: str) -> float:
    td = _resolve_task(slug)
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


def _corr_coordinate_only(td: Path, *, blank_snippets: bool) -> dict:
    exp = json.loads((td / "tests" / "expected.json").read_text())
    chain = []
    for step in exp["causal_chain"]:
        out = {
            "step": step["step"],
            "component": step["component"],
            "role": step["role"],
            "evidence_line": step["evidence_line"],
        }
        if blank_snippets:
            out["snippet"] = ""
        if "caused_by_step" in step:
            out["caused_by_step"] = step["caused_by_step"]
        chain.append(out)
    return {
        "schema_version": exp["schema_version"],
        "is_incident": True,
        "root_component": exp["root_component"],
        "causal_chain": chain,
        "root_cause_type": exp["root_cause_type"],
    }


# Ceilings are set a little above measured values so the tests are stable but
# still fail loudly if a future change re-opens an exploit.
@pytest.mark.parametrize("slug,builder,ceiling", [
    ("lh-f53d4948", lambda td, app: _v1_degen(td, app, smart=False), 0.80),
    ("lh-f53d4948", lambda td, app: _v1_degen(td, app, smart=True), 0.85),
    ("lh-84158338", lambda td, app: _v1_degen(td, app, smart=False), 0.95),
    ("lh-72340082", lambda td, app: _sev_degen(td, app, smart=False), 0.90),
    ("lh-72340082", lambda td, app: _sev_degen(td, app, smart=True), 0.90),
    ("lh-26152f56", _rem_forge, 0.75),
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
    td = TASKS / "lh-f53d4948"
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


@pytest.mark.parametrize("blank_snippets", [False, True])
def test_corr_chain_requires_verbatim_snippets(blank_snippets):
    """Correct corr coordinates alone must not score full credit."""
    td = TASKS / "lh-c3d5deec"
    with tempfile.TemporaryDirectory() as t:
        app = Path(t) / "app"
        app.mkdir()
        H._setup_app(td, app)
        ans = _corr_coordinate_only(td, blank_snippets=blank_snippets)
        assert H.score(td, ans) < 1.0


def test_seq_trigger_only_not_full_credit():
    """A timeline containing only the (correct) trigger must NOT score full
    credit — sequence reconstruction requires covering the event chain, and
    Kendall tau must not be vacuously 1.0 on <2 common events. Regression for
    the one-event seq bypass."""
    td = TASKS / "lh-95c71c89"
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
    td = TASKS / "lh-a67368b6"
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
    "lh-f53d4948", "lh-ca997bb8", "lh-84158338",
    "lh-2c60e732", "lh-ea0de35d", "lh-a67368b6",
    "lh-a9a7e3b9", "lh-99f4466c",
    "lh-72340082", "lh-26152f56",
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


def test_wrong_remedy_does_not_heal():
    """Fault-specific replay: on a disk_full task the canonical remedy is
    increase_quota. An agent declaring restart_component (wrong-but-active)
    must lose both the action-match and the post-mitigation replay — the
    cluster stays broken when you restart a process to fix a full disk."""
    td = TASKS / "lh-57e73974"
    exp = json.loads((td / "tests" / "expected.json").read_text())
    assert exp["mitigation"]["action"] == "increase_quota", "fixture drifted"
    with tempfile.TemporaryDirectory() as t:
        app = Path(t) / "app"
        app.mkdir()
        H._setup_app(td, app)
        right = H.oracle_answer(td, app)
        assert H.score(td, right) == 1.0, "oracle no longer scores 1.0 on diverse-action rem"
        wrong = json.loads(json.dumps(right))
        wrong["mitigation"]["action"] = "restart_component"
        r = H.score(td, wrong)
        # Wrong remedy must lose BOTH the action-match AND the recovery
        # replay (3/5 substantive = 0.6). A score of 0.8 here means the
        # replay healed on the wrong action — exactly the fallback hole a
        # re-render once re-opened by stripping required_action.
        assert r <= 0.61, (
            f"wrong-but-active remedy scored {r:.2f} (> 0.6) — the replay "
            "is not fault-specific; check required_action in tests/initial_state.json"
        )


def test_all_rem_initial_states_carry_required_action():
    """Every committed rem task's verifier-only initial_state.json must name
    the canonical action, matching expected.json. Guards against any future
    re-render path dropping the field (which silently re-permits any active
    action in the replay)."""
    # Opaque task ids: find rem tasks by schema, not by slug.
    rem_dirs = sorted(
        d for d in TASKS.iterdir()
        if (d / "tests" / "initial_state.json").exists()
    )
    assert rem_dirs, "no rem tasks found"
    for td in rem_dirs:
        state = json.loads((td / "tests" / "initial_state.json").read_text())
        exp = json.loads((td / "tests" / "expected.json").read_text())
        assert state.get("required_action") == exp["mitigation"]["action"], (
            f"{td.name}: tests/initial_state.json required_action="
            f"{state.get('required_action')!r} != expected mitigation "
            f"{exp['mitigation']['action']!r}"
        )
