"""Offline harness to score an answer against a task's verifier without
Docker/Harbor. Sets up a temp /app + /tests, path-redirects the committed
tests/test_state.py, runs pytest, and computes the same fractional reward
the in-container test.sh would (passed / non-skipped).

Used by tests/test_gameability.py to assert that (a) the oracle answer still
scores 1.0 after verifier hardening and (b) degenerate / reward-hacking
answers score low. Not a test module itself (no test_* functions).
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _setup_app(task_dir: Path, app: Path) -> None:
    """Mirror the Dockerfile layout: every task copies `data/<X>` to
    `/app/<X>`, so we copy environment/data/<X> -> app/<X> (stripping the
    leading data/). bin/ scripts are made executable like the Dockerfile."""
    data = task_dir / "environment" / "data"
    for p in sorted(data.rglob("*")):
        rel = p.relative_to(data)
        dest = app / rel
        if p.is_dir():
            dest.mkdir(parents=True, exist_ok=True)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(p, dest)
            if p.parent.name == "bin":
                dest.chmod(0o755)


def oracle_answer(task_dir: Path, app: Path) -> dict:
    """Produce the canonical oracle answer by running the task's own
    derive_answer.py against the temp app dir."""
    out = app / "answer.json"
    proc = subprocess.run(
        [
            sys.executable,
            str(task_dir / "solution" / "derive_answer.py"),
            "--app-dir", str(app),
            "--hints", str(task_dir / "solution" / "oracle_hints.json"),
            "--out", str(out),
        ],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"derive_answer failed for {task_dir.name}:\n{proc.stderr}")
    return json.loads(out.read_text())


def score(task_dir: Path, answer: dict) -> float:
    """Reward in [0,1] = passed / (tests - skipped), matching test.sh."""
    task_dir = Path(task_dir)
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        app = td / "app"
        tests = td / "tests"
        app.mkdir()
        tests.mkdir()
        _setup_app(task_dir, app)
        (app / "answer.json").write_text(json.dumps(answer))
        shutil.copy(task_dir / "tests" / "expected.json", tests / "expected.json")
        init = task_dir / "tests" / "initial_state.json"
        if init.exists():
            shutil.copy(init, tests / "initial_state.json")

        ts = (task_dir / "tests" / "test_state.py").read_text()
        ts = ts.replace('Path("/app/answer.json")', f'Path(r"{app / "answer.json"}")')
        ts = ts.replace('Path("/tests/expected.json")', f'Path(r"{tests / "expected.json"}")')
        ts = ts.replace('Path("/tests/initial_state.json")', f'Path(r"{tests / "initial_state.json"}")')
        ts = ts.replace('Path("/app")', f'Path(r"{app}")')
        # rem verifier references these absolute paths directly:
        ts = ts.replace('"/app/bin/', f'"{app}/bin/')
        ts = ts.replace('Path("/app/service_state.json")', f'Path(r"{app / "service_state.json"}")')
        (tests / "test_state.py").write_text(ts)

        junit = td / "out.xml"
        subprocess.run(
            [sys.executable, "-m", "pytest", str(tests / "test_state.py"),
             "-p", "no:cacheprovider", "--junit-xml", str(junit), "-q"],
            cwd=td, capture_output=True, text=True,
        )
        root = ET.parse(junit).getroot()
        suite = root if root.tag == "testsuite" else root.find("testsuite")
        total = int(suite.get("tests", 0))
        skipped = int(suite.get("skipped", 0))
        failures = int(suite.get("failures", 0))
        errors = int(suite.get("errors", 0))
        denom = total - skipped
        passed = denom - failures - errors
        return passed / denom if denom else 0.0
