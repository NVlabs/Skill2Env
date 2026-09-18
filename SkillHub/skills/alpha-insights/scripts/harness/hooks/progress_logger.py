#!/usr/bin/env python3
"""Hook 4: PostToolUse on all tools (async) — append tool usage to _hook_log.jsonl.

Runs asynchronously, never injects messages into conversation.
Writes append-only JSONL for debugging and progress tracking.
"""

import json
import os
import sys
from datetime import datetime, timezone

# Add harness parent dir to path
_HARNESS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _HARNESS_DIR not in sys.path:
    sys.path.insert(0, _HARNESS_DIR)

from hooks._workspace_finder import find_workspace  # noqa: E402


def _truncate(s, maxlen=100):
    if not s:
        return s
    s = str(s)
    return s[:maxlen] + "…" if len(s) > maxlen else s


def main():
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        return

    cwd = data.get("cwd") or ""
    workspace = find_workspace(cwd)
    if not workspace:
        return  # nowhere to log

    tool_name = data.get("tool_name") or "unknown"
    tool_input = data.get("tool_input") or {}

    # Extract key params based on tool type
    key_param = ""
    if tool_name == "Write":
        key_param = tool_input.get("file_path") or tool_input.get("path") or ""
    elif tool_name == "Read":
        key_param = tool_input.get("file_path") or ""
    elif tool_name == "Bash":
        key_param = _truncate(tool_input.get("command") or "")
    elif tool_name in ("Grep", "Glob"):
        key_param = tool_input.get("pattern") or ""
    elif tool_name == "Edit":
        key_param = tool_input.get("file_path") or ""
    else:
        # Generic: try file_path, then first string value
        key_param = tool_input.get("file_path") or ""
        if not key_param:
            for v in tool_input.values():
                if isinstance(v, str) and v:
                    key_param = _truncate(v)
                    break

    log_entry = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tool": tool_name,
        "param": key_param,
    }

    log_path = os.path.join(workspace, "_hook_log.jsonl")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    # async hook → no stdout output


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)  # fail open
