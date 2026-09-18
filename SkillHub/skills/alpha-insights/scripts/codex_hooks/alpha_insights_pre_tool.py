#!/usr/bin/env python3
"""Codex PreToolUse adapter for Alpha Insights."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[2]
HTML_GUARD = SKILL_ROOT / "scripts" / "harness" / "hooks" / "html_write_guard.py"


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

    for match in re.finditer(r'"(?:file_path|path|targetPath)"\s*:\s*"([^"]+)"', patch_text):
        paths.append(match.group(1))

    seen: set[str] = set()
    deduped: list[str] = []
    for path in paths:
        if path not in seen:
            seen.add(path)
            deduped.append(path)
    return deduped


def _snippet(value: str, limit: int = 600) -> str:
    value = value.strip()
    if len(value) <= limit:
        return value
    return value[:limit].rstrip() + "..."


def _hook_failure_payload(script: Path, proc: subprocess.CompletedProcess[str]) -> str:
    details = []
    if proc.stderr.strip():
        details.append(f"stderr: {_snippet(proc.stderr)}")
    if proc.stdout.strip():
        details.append(f"stdout: {_snippet(proc.stdout)}")
    detail_text = "\n".join(details) or "no child hook output"
    return json.dumps(
        {
            "decision": "block",
            "message": (
                "Alpha Insights html guard failed "
                f"(returncode={proc.returncode}). Direct HTML writes are blocked "
                "until the guard is fixed.\n"
                f"{detail_text}"
            ),
            "reason": "alpha_insights_html_guard_failed",
            "alpha_insights_hook_error": True,
            "alpha_insights_hook_errors": [
                {
                    "hook": "html_write_guard",
                    "script": str(script),
                    "returncode": proc.returncode,
                    "stderr": _snippet(proc.stderr),
                    "stdout": _snippet(proc.stdout),
                }
            ],
        },
        ensure_ascii=False,
    )


def _run_html_guard(original: dict[str, Any], file_path: str) -> str:
    payload = dict(original)
    payload["tool_name"] = _tool_name(original) or "ApplyPatch"
    payload["tool_input"] = {"file_path": file_path}
    proc = subprocess.run(
        ["python3", str(HTML_GUARD)],
        input=json.dumps(payload, ensure_ascii=False),
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        return _hook_failure_payload(HTML_GUARD, proc)
    return proc.stdout.strip()


def main() -> None:
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except Exception:
        return

    for path in _extract_paths(data):
        if path.lower().endswith((".html", ".htm")):
            output = _run_html_guard(data, path)
            if output:
                print(output)
            return


if __name__ == "__main__":
    main()
