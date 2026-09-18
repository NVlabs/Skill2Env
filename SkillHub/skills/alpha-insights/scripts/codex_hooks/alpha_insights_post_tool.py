#!/usr/bin/env python3
"""Codex PostToolUse adapter for Alpha Insights."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[2]
HOOK_DIR = SKILL_ROOT / "scripts" / "harness" / "hooks"
STAGE_GATE_HOOK = HOOK_DIR / "stage_gate_hook.py"
PROGRESS_LOGGER = HOOK_DIR / "progress_logger.py"


def _tool_input(data: dict[str, Any]) -> Any:
    return data.get("tool_input") or data.get("toolInput") or data.get("input") or {}


def _tool_name(data: dict[str, Any]) -> str:
    return str(data.get("tool_name") or data.get("toolName") or data.get("tool") or "")


def _string_payload(value: Any) -> str:
    if isinstance(value, str):
        return value
    try:
        return json.dumps(value, ensure_ascii=False)
    except Exception:
        return str(value)


def _extract_paths(data: dict[str, Any]) -> list[str]:
    tool_input = _tool_input(data)
    paths: list[str] = []

    if isinstance(tool_input, dict):
        for key in ("file_path", "path", "target_file", "targetPath"):
            value = tool_input.get(key)
            if isinstance(value, str) and value:
                paths.append(value)
        patch_text = "\n".join(
            _string_payload(tool_input.get(key, ""))
            for key in ("patch", "input", "cmd", "command")
        )
    else:
        patch_text = _string_payload(tool_input)

    for match in re.finditer(r"^\*\*\* (?:Add|Update|Delete) File: (.+)$", patch_text, re.MULTILINE):
        paths.append(match.group(1).strip())

    seen: set[str] = set()
    deduped: list[str] = []
    for path in paths:
        if path not in seen:
            seen.add(path)
            deduped.append(path)
    return deduped


def _normalized_payload(data: dict[str, Any]) -> dict[str, Any]:
    payload = dict(data)
    payload["tool_name"] = _tool_name(data)
    payload["tool_input"] = _tool_input(data)
    return payload


def _snippet(value: str, limit: int = 600) -> str:
    value = value.strip()
    if len(value) <= limit:
        return value
    return value[:limit].rstrip() + "..."


def _hook_error(script: Path, hook_name: str, proc: subprocess.CompletedProcess[str], *, blocked: bool) -> dict[str, Any]:
    return {
        "hook": hook_name,
        "script": str(script),
        "returncode": proc.returncode,
        "stderr": _snippet(proc.stderr),
        "stdout": _snippet(proc.stdout),
        "blocked": blocked,
    }


def _hook_error_message(hook_name: str, proc: subprocess.CompletedProcess[str], *, blocked: bool) -> str:
    detail_parts = []
    if proc.stderr.strip():
        detail_parts.append(f"stderr: {_snippet(proc.stderr)}")
    if proc.stdout.strip():
        detail_parts.append(f"stdout: {_snippet(proc.stdout)}")
    details = "\n".join(detail_parts) or "no child hook output"
    if blocked:
        return (
            f"Alpha Insights {hook_name} hook failed (returncode={proc.returncode}). "
            "Treat the current gate as BLOCKED until manual validation passes.\n"
            f"{details}"
        )
    return (
        f"Alpha Insights {hook_name} hook failed (returncode={proc.returncode}). "
        "Continue the tool operation, but inspect the hook before relying on automation logs.\n"
        f"{details}"
    )


def _run_hook(script: Path, payload: dict[str, Any]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(script)],
        input=json.dumps(payload, ensure_ascii=False),
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> None:
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except Exception:
        return

    hook_errors: list[dict[str, Any]] = []
    progress_proc = _run_hook(PROGRESS_LOGGER, _normalized_payload(data))
    if progress_proc.returncode != 0:
        hook_errors.append(_hook_error(PROGRESS_LOGGER, "progress_logger", progress_proc, blocked=False))

    messages: list[str] = []
    gates: list[dict[str, Any]] = []
    for path in _extract_paths(data):
        payload = dict(data)
        payload["tool_name"] = _tool_name(data) or "ApplyPatch"
        payload["tool_input"] = {"file_path": path}
        proc = _run_hook(STAGE_GATE_HOOK, payload)
        if proc.returncode != 0:
            hook_errors.append(_hook_error(STAGE_GATE_HOOK, "stage_gate", proc, blocked=True))
            messages.append(_hook_error_message("stage gate", proc, blocked=True))
            gates.append(
                {
                    "blocked": True,
                    "semantic": "hard_stop",
                    "hook_error": True,
                    "hook": "stage_gate",
                    "script": str(STAGE_GATE_HOOK),
                    "returncode": proc.returncode,
                }
            )
            continue
        output = proc.stdout.strip()
        if not output:
            continue
        try:
            decoded = json.loads(output)
        except Exception:
            messages.append(output)
        else:
            message = decoded.get("message")
            if message:
                messages.append(str(message))
            gate = decoded.get("alpha_insights_gate")
            if isinstance(gate, dict):
                gates.append(gate)

    if hook_errors and not messages:
        messages.extend(
            _hook_error_message(str(error["hook"]).replace("_", " "), progress_proc, blocked=False)
            for error in hook_errors
            if error.get("hook") == "progress_logger"
        )

    if messages:
        blocked = any(bool(gate.get("blocked")) for gate in gates)
        print(json.dumps({
            "decision": "allow",
            "message": "\n\n".join(messages),
            "alpha_insights_blocked": blocked,
            "alpha_insights_gates": gates,
            "alpha_insights_hook_error": bool(hook_errors),
            "alpha_insights_hook_errors": hook_errors,
        }, ensure_ascii=False))


if __name__ == "__main__":
    main()
