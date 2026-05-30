#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API_ROOT = os.environ.get("DEVIN_API_ROOT", "https://api.devin.ai").rstrip("/")


def main() -> int:
    if not os.environ.get("DEVIN_API_KEY"):
        print("DEVIN_API_KEY is required", file=sys.stderr)
        return 2

    if len(sys.argv) < 2:
        print("usage: terminate-devin-sessions-from-run.py RUN_DIR [RUN_DIR ...]", file=sys.stderr)
        return 2

    api = _api_context(os.environ["DEVIN_API_KEY"])
    session_ids: list[str] = []
    for arg in sys.argv[1:]:
        run_dir = Path(arg)
        for path in sorted(run_dir.glob("*/agent/devin-session-summary.json")):
            try:
                summary = json.loads(path.read_text())
            except Exception as exc:
                print(f"skip unreadable {path}: {exc}", file=sys.stderr)
                continue
            session_id = str(summary.get("session_id") or "").strip()
            if session_id:
                session_ids.append(session_id)

    seen: set[str] = set()
    for session_id in session_ids:
        if session_id in seen:
            continue
        seen.add(session_id)
        result = _terminate_session_best_effort(api, session_id)
        if result.get("_termination_error"):
            print(f"{session_id}\tERROR\t{result['_termination_error']}")
        else:
            status = result.get("status")
            status_detail = result.get("status_detail")
            acus = result.get("acus_consumed")
            print(f"{session_id}\tOK\tstatus={status}\tdetail={status_detail}\tacus={acus}")

    print(f"processed={len(seen)}")
    return 0


def _api_context(api_key: str) -> dict[str, str]:
    org_id = os.environ.get("DEVIN_ORG_ID", "").strip()
    if not org_id:
        principal = _request_json("GET", f"{API_ROOT}/v3/self", api_key, None, timeout=60)
        org_id = str(principal.get("org_id") or "")
    if not org_id:
        raise RuntimeError("DEVIN_ORG_ID is required for Devin API v3 service-user keys")
    return {
        "base": f"{API_ROOT}/v3/organizations/{urllib.parse.quote(org_id)}",
        "api_key": api_key,
    }


def _terminate_session_best_effort(api: dict[str, str], session_id: str) -> dict:
    urls = [f"{api['base']}/sessions/{urllib.parse.quote(session_id)}"]
    if not session_id.startswith("devin-"):
        urls.append(f"{api['base']}/sessions/{urllib.parse.quote('devin-' + session_id)}")

    last_error: Exception | None = None
    for url in urls:
        try:
            return _request_json("DELETE", url, api["api_key"], None, timeout=60)
        except Exception as exc:
            last_error = exc
    return {"_termination_error": str(last_error)}


def _request_json(
    method: str,
    url: str,
    api_key: str,
    payload: dict | None,
    timeout: float = 90,
) -> dict:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Authorization": f"Bearer {api_key}"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Devin API {method} {url} failed: HTTP {exc.code}: {detail}") from exc
    if not raw:
        return {}
    return json.loads(raw.decode("utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
