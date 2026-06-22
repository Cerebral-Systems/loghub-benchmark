from __future__ import annotations

import json
import os
import re
import shlex
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Any

from harbor.agents.base import BaseAgent
from harbor.environments.base import BaseEnvironment
from harbor.models.agent.context import AgentContext


API_ROOT = os.environ.get("DEVIN_API_ROOT", "https://api.devin.ai").rstrip("/")
LEGACY_API_BASE = os.environ.get("DEVIN_API_BASE", f"{API_ROOT}/v1").rstrip("/")
DEFAULT_MAX_ACU = int(os.environ.get("DEVIN_MAX_ACU_LIMIT", "5"))
DEFAULT_POLL_SECONDS = float(os.environ.get("DEVIN_POLL_INTERVAL_SEC", "20"))
DEFAULT_WALL_TIMEOUT_SECONDS = float(os.environ.get("DEVIN_WALL_TIMEOUT_SEC", "1200"))
TERMINAL_STATUSES = {"finished", "blocked", "expired", "error", "exit", "suspended"}


class DevinHarborAgent(BaseAgent):
    """Harbor adapter that runs each task as one isolated Devin API session."""

    SUPPORTS_ATIF = False

    @staticmethod
    def name() -> str:
        return "devin-api-single-session"

    def version(self) -> str | None:
        return "devin-api-v1-v3"

    async def setup(self, environment: BaseEnvironment) -> None:
        if not os.environ.get("DEVIN_API_KEY"):
            raise RuntimeError("DEVIN_API_KEY is required for DevinHarborAgent")
        await environment.exec(command="mkdir -p /logs/agent", user="root")

    async def run(
        self,
        instruction: str,
        environment: BaseEnvironment,
        context: AgentContext,
    ) -> None:
        started = time.time()
        task_kind = _task_kind(instruction)
        schema_version = _schema_version(instruction)
        task_name = _task_name(instruction, schema_version)
        api_key = os.environ["DEVIN_API_KEY"]

        bundle = await _build_task_bundle(environment, instruction)
        with tempfile.TemporaryDirectory(prefix="devin-harbor-") as tmp:
            bundle_path = Path(tmp) / "loghub_task_bundle.txt"
            answer_path = Path(tmp) / "answer.json"
            bundle_path.write_text(bundle, encoding="utf-8")

            api = _api_context(api_key)
            attachment_url = _upload_attachment(api, bundle_path)
            session = _create_session(
                api=api,
                prompt=_prompt(instruction, attachment_url, schema_version, task_kind),
                schema=_structured_output_schema(schema_version),
                task_name=task_name,
            )
            session_id = session["session_id"]

            detail = _poll_session(api, session_id, started)
            structured_output = _coerce_structured_output(detail.get("structured_output"))
            if not structured_output:
                _request_final_structured_output(api, session_id, schema_version)
                detail = _poll_session(api, session_id, started, extra_seconds=180)
                structured_output = _coerce_structured_output(detail.get("structured_output"))

            answer = _extract_answer(structured_output, schema_version)
            if not answer:
                answer = _minimal_answer(schema_version)

            mitigation_result: dict[str, Any] | None = None
            if schema_version == "loghub-sre-answer-v3-remediation":
                mitigation_result = await _apply_selected_mitigation(environment, answer)
                _merge_postcheck(answer, mitigation_result)

            answer_path.write_text(json.dumps(answer, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            await environment.upload_file(answer_path, "/app/answer.json")

            termination_error: str | None = None
            terminated_session = False
            termination_detail = _terminate_session_best_effort(api, session_id)
            if isinstance(termination_detail, dict) and termination_detail.get("_termination_error"):
                termination_error = str(termination_detail["_termination_error"])
            elif termination_detail:
                detail = termination_detail
                terminated_session = True

        final_answer = await environment.exec(command="cat /app/answer.json 2>/dev/null || true", user="root")
        (self.logs_dir / "answer.json").write_text((final_answer.stdout or "").strip() + "\n")

        summary = {
            "agent": self.name(),
            "api_version": api["version"],
            "api_base": api["base"],
            "org_id": api.get("org_id"),
            "session_id": session.get("session_id"),
            "session_url": session.get("url"),
            "status": detail.get("status"),
            "status_enum": detail.get("status_enum"),
            "schema_version": schema_version,
            "task_kind": task_kind,
            "task_name": task_name,
            "elapsed_seconds": round(time.time() - started, 3),
            "structured_output_present": bool(structured_output),
            "mitigation_result": mitigation_result,
            "terminated_session": terminated_session,
            "termination_error": termination_error,
            "acus_consumed": detail.get("acus_consumed"),
        }
        (self.logs_dir / "devin-session-summary.json").write_text(
            json.dumps(summary, indent=2, sort_keys=True, default=str) + "\n"
        )
        (self.logs_dir / "devin-session-detail.json").write_text(
            json.dumps(_redact_session_detail(detail), indent=2, sort_keys=True, default=str) + "\n"
        )
        context.metadata = {"devin": summary}


async def _build_task_bundle(environment: BaseEnvironment, instruction: str) -> str:
    proc = await environment.exec(
        command=r"""python3 - <<'PY'
from __future__ import annotations

import json
from pathlib import Path

root = Path("/app")
files = []
for path in sorted(root.rglob("*")):
    if not path.is_file():
        continue
    rel = path.relative_to(root).as_posix()
    if rel == "answer.json":
        continue
    try:
        data = path.read_bytes()
    except OSError as exc:
        files.append({"path": rel, "error": str(exc)})
        continue
    text = data.decode("utf-8", errors="replace")
    files.append({
        "path": rel,
        "size_bytes": len(data),
        "line_count": len(text.splitlines()),
        "content": text,
    })

print(json.dumps({"files": files}, ensure_ascii=False))
PY""",
        user="root",
    )
    if _exit_code(proc) != 0:
        raise RuntimeError(f"failed to collect /app files: {proc.stderr}")
    payload = json.loads(proc.stdout)

    parts = [
        "LOGHUB SRE HARBOR TASK BUNDLE",
        "",
        "The original task instruction is below.",
        "",
        instruction.strip(),
        "",
        "Visible /app files follow. Lines are numbered 1-based; cite these line numbers exactly.",
        "",
    ]
    for item in payload["files"]:
        parts.append(f"===== FILE {item['path']} ({item.get('size_bytes', 0)} bytes) =====")
        if "error" in item:
            parts.append(f"[unreadable: {item['error']}]")
            parts.append("")
            continue
        for line_no, line in enumerate(item["content"].splitlines(), start=1):
            parts.append(f"{line_no:06d}: {line}")
        if item["content"].endswith("\n"):
            parts.append("")
        parts.append("")
    return "\n".join(parts)


def _api_context(api_key: str) -> dict[str, str]:
    requested = os.environ.get("DEVIN_API_VERSION", "").strip().lower()
    if requested == "v3" or api_key.startswith("cog_"):
        org_id = os.environ.get("DEVIN_ORG_ID", "").strip()
        if not org_id:
            principal = _request_json("GET", f"{API_ROOT}/v3/self", api_key, None, timeout=60)
            org_id = str(principal.get("org_id") or "")
        if not org_id:
            raise RuntimeError("DEVIN_ORG_ID is required for Devin API v3 service-user keys")
        return {
            "version": "v3",
            "base": f"{API_ROOT}/v3/organizations/{urllib.parse.quote(org_id)}",
            "org_id": org_id,
            "api_key": api_key,
        }
    return {"version": "v1", "base": LEGACY_API_BASE, "api_key": api_key}


def _upload_attachment(api: dict[str, str], path: Path) -> str:
    boundary = f"----devin-harbor-{uuid.uuid4().hex}"
    data = path.read_bytes()
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{path.name}"\r\n'
        "Content-Type: text/plain; charset=utf-8\r\n\r\n"
    ).encode("utf-8") + data + f"\r\n--{boundary}--\r\n".encode("utf-8")
    endpoint = f"{api['base']}/attachments"
    response = _request(
        "POST",
        endpoint,
        api["api_key"],
        body=body,
        content_type=f"multipart/form-data; boundary={boundary}",
        timeout=180,
    )
    text = response.decode("utf-8", errors="replace").strip()
    try:
        parsed = json.loads(text)
        if isinstance(parsed, str):
            return parsed
        if isinstance(parsed, dict) and parsed.get("url"):
            return str(parsed["url"])
    except json.JSONDecodeError:
        pass
    return text.strip('"')


def _create_session(
    api: dict[str, str],
    prompt: str,
    schema: dict[str, Any],
    task_name: str,
) -> dict[str, Any]:
    payload: dict[str, Any]
    if api["version"] == "v3":
        attachment_urls = _attachment_urls_from_prompt(prompt)
        payload = {
            "prompt": prompt,
            "attachment_urls": attachment_urls,
            "structured_output_required": True,
            "structured_output_schema": schema,
            "max_acu_limit": DEFAULT_MAX_ACU,
            "tags": ["loghub-sre", "harbor", "single-session", task_name[:80]],
            "title": f"Loghub SRE benchmark: {task_name[:80]}",
        }
        devin_mode = os.environ.get("DEVIN_MODE", "").strip()
        if devin_mode:
            payload["devin_mode"] = devin_mode
    else:
        payload = {
            "prompt": prompt,
            "structured_output_schema": schema,
            "max_acu_limit": DEFAULT_MAX_ACU,
            "idempotent": os.environ.get("DEVIN_IDEMPOTENT", "false").lower() == "true",
            "unlisted": True,
            "tags": ["loghub-sre", "harbor", "single-session", task_name[:80]],
            "title": f"Loghub SRE benchmark: {task_name[:80]}",
        }
    raw = _request_json("POST", f"{api['base']}/sessions", api["api_key"], payload, timeout=120)
    if "session_id" not in raw:
        raise RuntimeError(f"Devin create session response missing session_id: {raw}")
    return raw


def _poll_session(
    api: dict[str, str],
    session_id: str,
    started: float,
    extra_seconds: float = 0,
) -> dict[str, Any]:
    deadline = started + DEFAULT_WALL_TIMEOUT_SECONDS + extra_seconds
    last: dict[str, Any] = {}
    while time.time() < deadline:
        try:
            last = _request_json("GET", _session_url(api, session_id), api["api_key"], None)
        except (RuntimeError, json.JSONDecodeError) as exc:
            if _is_transient_api_error(exc):
                time.sleep(DEFAULT_POLL_SECONDS)
                continue
            raise
        status = str(last.get("status_enum") or last.get("status") or "").lower()
        status_detail = str(last.get("status_detail") or "").lower()
        if _coerce_structured_output(last.get("structured_output")):
            return last
        if status == "running" and status_detail in {"finished", "waiting_for_user"}:
            return last
        if status in TERMINAL_STATUSES:
            return last
        time.sleep(DEFAULT_POLL_SECONDS)
    return last


def _request_final_structured_output(api: dict[str, str], session_id: str, schema_version: str) -> None:
    message = (
        "Please update structured_output now with the final benchmark answer object only. "
        f"It must match schema_version {schema_version} and contain no markdown."
    )
    try:
        url = f"{_session_url(api, session_id)}/messages" if api["version"] == "v3" else (
            f"{api['base']}/sessions/{urllib.parse.quote(session_id)}/message"
        )
        _request_json(
            "POST",
            url,
            api["api_key"],
            {"message": message},
            timeout=60,
        )
    except Exception:
        return


def _terminate_session_best_effort(api: dict[str, str], session_id: str) -> dict[str, Any]:
    urls = [_session_url(api, session_id)]
    if api["version"] == "v3" and not session_id.startswith("devin-"):
        urls.append(f"{api['base']}/sessions/{urllib.parse.quote('devin-' + session_id)}")

    last_error: Exception | None = None
    for url in urls:
        try:
            return _request_json("DELETE", url, api["api_key"], None, timeout=60)
        except Exception as exc:
            last_error = exc
    return {"_termination_error": str(last_error)}


def _session_url(api: dict[str, str], session_id: str) -> str:
    return f"{api['base']}/sessions/{urllib.parse.quote(session_id)}"


def _attachment_urls_from_prompt(prompt: str) -> list[str]:
    return re.findall(r'ATTACHMENT:"([^"]+)"', prompt)


def _request_json(
    method: str,
    url: str,
    api_key: str,
    payload: dict[str, Any] | None,
    timeout: float = 90,
) -> dict[str, Any]:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    raw = _request(method, url, api_key, body=body, content_type="application/json", timeout=timeout)
    if not raw:
        return {}
    return json.loads(raw.decode("utf-8"))


def _request(
    method: str,
    url: str,
    api_key: str,
    body: bytes | None,
    content_type: str,
    timeout: float,
) -> bytes:
    headers = {"Authorization": f"Bearer {api_key}"}
    if body is not None:
        headers["Content-Type"] = content_type
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Devin API {method} {url} failed: HTTP {exc.code}: {detail}") from exc


def _is_transient_api_error(exc: Exception) -> bool:
    if isinstance(exc, json.JSONDecodeError):
        return True
    text = str(exc)
    return "HTTP 502" in text or "HTTP 503" in text or "HTTP 504" in text


def _prompt(instruction: str, attachment_url: str, schema_version: str, task_kind: str) -> str:
    remediation_note = ""
    if schema_version == "loghub-sre-answer-v3-remediation":
        remediation_note = (
            "\nYou are running remotely and cannot execute /app/bin/apply_mitigation yourself. "
            "Choose the mitigation.action and mitigation.target in the structured output; "
            "the Harbor adapter will execute exactly that command in the task container and fill the postcheck from the real result.\n"
        )
    return f"""You are being evaluated on the Loghub SRE Harbor benchmark.

Solve exactly one task from the attached line-numbered /app snapshot. Use the original instruction in the bundle as the source of truth. Return the final /app/answer.json content in structured_output only; do not include markdown, commentary, or an outer wrapper.

Required schema_version: {schema_version}
Task kind: {task_kind}
{remediation_note}
Important benchmark constraints:
- Evidence file names must be basenames or relative paths exactly as requested by the task.
- Evidence line numbers must match the 1-based line numbers in the bundle.
- Evidence snippets must be verbatim substrings from the cited line.
- Do not use any files or ground truth that are not present in the attachment.
- Once structured_output contains the final answer, stop immediately and wait; do not keep investigating.

ATTACHMENT:"{attachment_url}"
"""


def _structured_output_schema(schema_version: str) -> dict[str, Any]:
    evidence = {
        "type": "object",
        "additionalProperties": True,
        "required": ["file", "line", "snippet"],
        "properties": {
            "file": {"type": "string"},
            "line": {"type": "integer", "minimum": 1},
            "snippet": {"type": "string"},
        },
    }
    if schema_version == "loghub-sre-answer-v2-fp":
        return {
            "type": "object",
            "required": ["schema_version", "is_incident", "false_positive_indicators", "confidence"],
            "additionalProperties": False,
            "properties": {
                "schema_version": {"const": schema_version},
                "is_incident": {"type": "boolean"},
                "false_positive_indicators": {
                    "type": "array",
                    "items": {
                        "allOf": [
                            evidence,
                            {
                                "type": "object",
                                "required": ["why_not_anomalous"],
                                "properties": {
                                    "why_not_anomalous": {
                                        "enum": [
                                            "rate_limit_warning",
                                            "recoverable_retry",
                                            "benign_info",
                                            "expected_event",
                                            "transient_state",
                                        ]
                                    }
                                },
                            },
                        ]
                    },
                },
                "confidence": {"type": "number", "minimum": 0, "maximum": 1},
            },
        }
    if schema_version == "loghub-sre-answer-v2-seq":
        return {
            "type": "object",
            "required": ["schema_version", "is_incident", "timeline", "root_cause_type"],
            "additionalProperties": False,
            "properties": {
                "schema_version": {"const": schema_version},
                "is_incident": {"type": "boolean"},
                "timeline": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["sequence", "file", "line", "snippet", "role"],
                        "additionalProperties": True,
                        "properties": {
                            "sequence": {"type": "integer", "minimum": 0},
                            "file": {"type": "string"},
                            "line": {"type": "integer", "minimum": 1},
                            "snippet": {"type": "string"},
                            "role": {"enum": ["trigger", "propagation", "consequence", "noise"]},
                        },
                    },
                },
                "root_cause_type": {"type": "string"},
            },
        }
    if schema_version == "loghub-sre-answer-v2-corr":
        return {
            "type": "object",
            "required": ["schema_version", "is_incident", "root_component", "causal_chain", "root_cause_type"],
            "additionalProperties": False,
            "properties": {
                "schema_version": {"const": schema_version},
                "is_incident": {"type": "boolean"},
                "root_component": {"type": "string"},
                "causal_chain": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["step", "component", "role", "evidence_line", "snippet"],
                        "additionalProperties": True,
                        "properties": {
                            "step": {"type": "integer", "minimum": 0},
                            "component": {"type": "string"},
                            "role": {"enum": ["root", "downstream"]},
                            "evidence_line": {"type": "integer", "minimum": 1},
                            "snippet": {"type": "string"},
                            "caused_by_step": {"type": "integer", "minimum": 0},
                        },
                    },
                },
                "root_cause_type": {"type": "string"},
            },
        }
    if schema_version == "loghub-sre-answer-v2-sev":
        return {
            "type": "object",
            "required": [
                "schema_version",
                "is_incident",
                "evidence",
                "anomaly_keys",
                "root_cause_type",
                "severity",
                "severity_justification",
            ],
            "additionalProperties": False,
            "properties": {
                "schema_version": {"const": schema_version},
                "is_incident": {"type": "boolean"},
                "evidence": {"type": "array", "items": evidence},
                "anomaly_keys": {"type": "array", "items": {"type": "string"}},
                "root_cause_type": {"type": "string"},
                "severity": {"enum": ["P0", "P1", "P2", "P3"]},
                "severity_justification": {
                    "enum": ["multi_component", "single_critical", "recoverable", "transient_warning"]
                },
            },
        }
    if schema_version == "loghub-sre-answer-v2-tmpl":
        return {
            "type": "object",
            "required": ["schema_version", "templates", "total_unique_templates"],
            "additionalProperties": False,
            "properties": {
                "schema_version": {"const": schema_version},
                "templates": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["template_id", "template", "matching_lines", "example_line_number"],
                        "additionalProperties": False,
                        "properties": {
                            "template_id": {"type": "string"},
                            "template": {"type": "string"},
                            "matching_lines": {"type": "array", "items": {"type": "integer", "minimum": 1}},
                            "example_line_number": {"type": "integer", "minimum": 1},
                        },
                    },
                },
                "total_unique_templates": {"type": "integer", "minimum": 0},
            },
        }
    if schema_version == "loghub-sre-answer-v3-remediation":
        return {
            "type": "object",
            "required": [
                "schema_version",
                "is_incident",
                "root_component",
                "root_cause_type",
                "causal_chain",
                "mitigation",
                "postcheck",
            ],
            "additionalProperties": False,
            "properties": {
                "schema_version": {"const": schema_version},
                "is_incident": {"type": "boolean"},
                "root_component": {"type": "string"},
                "root_cause_type": {"type": "string"},
                "causal_chain": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["step", "component", "role", "evidence"],
                        "additionalProperties": True,
                        "properties": {
                            "step": {"type": "integer", "minimum": 0},
                            "component": {"type": "string"},
                            "role": {"enum": ["root", "downstream"]},
                            "caused_by_step": {"type": "integer", "minimum": 0},
                            "evidence": evidence,
                        },
                    },
                },
                "mitigation": {
                    "type": "object",
                    "required": ["action", "target", "rationale"],
                    "additionalProperties": False,
                    "properties": {
                        "action": {
                            "enum": [
                                "restart_component",
                                "rollback_config",
                                "increase_quota",
                                "disable_route",
                                "mark_noop",
                            ]
                        },
                        "target": {"type": "string"},
                        "rationale": {"type": "string"},
                    },
                },
                "postcheck": {
                    "type": "object",
                    "required": ["health_status", "command"],
                    "additionalProperties": False,
                    "properties": {
                        "health_status": {"enum": ["healthy", "degraded", "unhealthy"]},
                        "command": {"type": "string"},
                    },
                },
            },
        }
    return {
        "type": "object",
        "required": ["schema_version", "is_incident", "evidence", "anomaly_keys", "root_cause_type", "recommended_action"],
        "additionalProperties": False,
        "properties": {
            "schema_version": {"const": "loghub-sre-answer-v2"},
            "is_incident": {"type": "boolean"},
            "evidence": {"type": "array", "items": evidence},
            "anomaly_keys": {"type": "array", "items": {"type": "string"}},
            "root_cause_type": {"type": "string"},
            "recommended_action": {
                "enum": ["escalate", "investigate", "no_action", "open_incident", "page_owner"]
            },
        },
    }


async def _apply_selected_mitigation(environment: BaseEnvironment, answer: dict[str, Any]) -> dict[str, Any]:
    mitigation = answer.get("mitigation") if isinstance(answer.get("mitigation"), dict) else {}
    action = str(mitigation.get("action") or "mark_noop")
    target = str(mitigation.get("target") or answer.get("root_component") or "")
    apply_cmd = (
        "/app/bin/apply_mitigation --action "
        f"{shlex.quote(action)} --target {shlex.quote(target)}"
    )
    apply_proc = await environment.exec(command=apply_cmd, user="root")
    health_proc = await environment.exec(command="/app/bin/check_health", user="root")
    health_status = "unhealthy"
    first_line = (health_proc.stdout or "").splitlines()[0] if health_proc.stdout else ""
    if first_line.startswith("status="):
        health_status = first_line.split("=", 1)[1].strip()
    return {
        "command": apply_cmd,
        "action": action,
        "target": target,
        "apply_exit_code": _exit_code(apply_proc),
        "apply_stdout": apply_proc.stdout,
        "apply_stderr": apply_proc.stderr,
        "postcheck_exit_code": _exit_code(health_proc),
        "postcheck_stdout": health_proc.stdout,
        "postcheck_stderr": health_proc.stderr,
        "health_status": health_status,
    }


def _merge_postcheck(answer: dict[str, Any], mitigation_result: dict[str, Any]) -> None:
    answer["postcheck"] = {
        "health_status": mitigation_result.get("health_status") or "unhealthy",
        "command": "/app/bin/check_health",
    }


def _exit_code(proc: Any) -> int:
    value = getattr(proc, "exit_code", None)
    if value is None:
        value = getattr(proc, "returncode", None)
    return int(value or 0)


def _coerce_structured_output(value: Any) -> dict[str, Any] | None:
    if isinstance(value, dict):
        return value
    if isinstance(value, str) and value.strip():
        text = value.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text)
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            return None
        return parsed if isinstance(parsed, dict) else None
    return None


def _extract_answer(output: dict[str, Any] | None, schema_version: str) -> dict[str, Any] | None:
    if not output:
        return None
    if output.get("schema_version") == schema_version:
        return output
    for key in ("answer", "answer_json", "structured_output", "result"):
        value = output.get(key)
        if isinstance(value, dict) and value.get("schema_version") == schema_version:
            return value
        if isinstance(value, str):
            parsed = _coerce_structured_output(value)
            if parsed and parsed.get("schema_version") == schema_version:
                return parsed
    return output


def _minimal_answer(schema_version: str) -> dict[str, Any]:
    if schema_version == "loghub-sre-answer-v2-fp":
        return {"schema_version": schema_version, "is_incident": False, "false_positive_indicators": [], "confidence": 0}
    if schema_version == "loghub-sre-answer-v2-seq":
        return {"schema_version": schema_version, "is_incident": True, "timeline": [], "root_cause_type": "unknown"}
    if schema_version == "loghub-sre-answer-v2-corr":
        return {
            "schema_version": schema_version,
            "is_incident": True,
            "root_component": "",
            "causal_chain": [],
            "root_cause_type": "unknown",
        }
    if schema_version == "loghub-sre-answer-v2-sev":
        return {
            "schema_version": schema_version,
            "is_incident": True,
            "evidence": [],
            "anomaly_keys": [],
            "root_cause_type": "unknown",
            "severity": "P3",
            "severity_justification": "transient_warning",
        }
    if schema_version == "loghub-sre-answer-v2-tmpl":
        return {"schema_version": schema_version, "templates": [], "total_unique_templates": 0}
    if schema_version == "loghub-sre-answer-v3-remediation":
        return {
            "schema_version": schema_version,
            "is_incident": True,
            "root_component": "",
            "root_cause_type": "other",
            "causal_chain": [],
            "mitigation": {"action": "mark_noop", "target": "", "rationale": "No structured output returned."},
            "postcheck": {"health_status": "unhealthy", "command": "/app/bin/check_health"},
        }
    return {
        "schema_version": "loghub-sre-answer-v2",
        "is_incident": True,
        "evidence": [],
        "anomaly_keys": [],
        "root_cause_type": "unknown",
        "recommended_action": "investigate",
    }


def _schema_version(instruction: str) -> str:
    match = re.search(r'"schema_version"\s*:\s*"([^"]+)"', instruction)
    if match:
        return match.group(1)
    return "loghub-sre-answer-v2"


def _task_kind(instruction: str) -> str:
    schema = _schema_version(instruction)
    if schema.endswith("-fp"):
        return "false-positive"
    if schema.endswith("-seq"):
        return "temporal-sequence"
    if schema.endswith("-corr"):
        return "cross-component-correlation"
    if schema.endswith("-sev"):
        return "severity"
    if schema.endswith("-tmpl"):
        return "template-extraction"
    if schema.endswith("-remediation"):
        return "remediation"
    return "anomaly-localization"


def _task_name(instruction: str, schema_version: str) -> str:
    first = next((line.strip("# ").strip() for line in instruction.splitlines() if line.strip()), "")
    safe = re.sub(r"[^a-zA-Z0-9_.-]+", "-", first.lower()).strip("-")
    return safe[:64] or schema_version


def _redact_session_detail(detail: dict[str, Any]) -> dict[str, Any]:
    redacted = dict(detail)
    messages = redacted.get("messages")
    if isinstance(messages, list) and len(messages) > 20:
        redacted["messages"] = messages[-20:]
        redacted["messages_truncated"] = len(messages) - 20
    return redacted
