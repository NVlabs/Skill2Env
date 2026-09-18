#!/usr/bin/env python3
"""Hook 3: PreToolUse on Write — block direct .html/.htm file writes.

Stage 6 requires HTML generation via Bash+Python because:
- Model output layer randomly filters ECharts 'data' keywords
- Write tool truncates large HTML files in tight context
"""

import json
import sys


def main():
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        # malformed input → allow but warn (transparent failure)
        json.dump({
            "decision": "allow",
            "message": "⚠️ html_write_guard: failed to parse input, allowing by default",
        }, sys.stdout, ensure_ascii=False)
        return

    tool_input = data.get("tool_input") or {}
    file_path = tool_input.get("file_path") or tool_input.get("path") or ""

    if file_path.lower().endswith((".html", ".htm")):
        json.dump({
            "decision": "block",
            "reason": (
                "HTML files must be generated through Bash + Python scripts "
                "(report_helper.py or manual string assembly). Write is blocked for .html "
                "because model output can filter ECharts data keys and truncate large files "
                "when context is tight. Follow Stage 6 instructions."
            ),
        }, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
