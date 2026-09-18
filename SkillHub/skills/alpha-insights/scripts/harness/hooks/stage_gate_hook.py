#!/usr/bin/env python3
"""Hook 2: PostToolUse on Write — auto-run stage gate after deliverable writes.

When a deliverable file (user_brief.md, research_definition.md, etc.) is written,
automatically run the corresponding stage validator and inject results into the
conversation.
"""

import json
import os
import sys

# Add harness parent dir to path
_HARNESS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _HARNESS_DIR not in sys.path:
    sys.path.insert(0, _HARNESS_DIR)

from hooks._workspace_finder import find_workspace  # noqa: E402

# Deliverable filename → stage number
DELIVERABLE_MAP = {
    "user_brief.md": 1,
    "research_definition.md": 2,
    "research_plan.md": 3,
    "interview_guides.md": 3.5,
    "evidence_base.md": 4,
    "insights.md": 5,
    "report.html": 6,
}


HARD_STOP_MESSAGE = (
    "⛔ Alpha Insights HARD STOP: the current Stage Gate is BLOCKED. "
    "This write may remain for repair, but do not advance, create or update "
    "downstream deliverables, or claim stage completion. Fix the FAIL items above "
    "and rerun the same Stage Gate until PASS."
)


def main():
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        return  # malformed input → fail open

    tool_input = data.get("tool_input") or {}
    file_path = tool_input.get("file_path") or tool_input.get("path") or ""
    basename = os.path.basename(file_path)

    stage_num = DELIVERABLE_MAP.get(basename)
    if stage_num is None:
        return  # not a deliverable → silent pass

    cwd = data.get("cwd") or ""
    workspace = find_workspace(cwd)

    # Also try: the directory containing the written file
    if not workspace:
        parent = os.path.dirname(file_path)
        if parent and os.path.isdir(parent):
            # Accept if it has _state.json OR the deliverable we just wrote
            if (os.path.isfile(os.path.join(parent, "_state.json"))
                    or os.path.isfile(os.path.join(parent, basename))):
                workspace = parent

    if not workspace:
        return  # can't locate workspace → fail open

    # Import and run stage gate validator
    from stage_gate import validate_stage  # noqa: E402

    result = validate_stage(stage_num, workspace)
    gate = result.get("gate", "UNKNOWN")
    blocked = "BLOCKED" in str(gate)
    checks = result.get("checks", [])
    warnings = result.get("warnings", [])

    stage7_result = None
    stage7_gate = None
    state = None
    try:
        state_path = os.path.join(workspace, "_state.json")
        if os.path.isfile(state_path):
            with open(state_path, "r", encoding="utf-8") as f:
                state = json.load(f)
    except Exception:
        pass

    if state and state.get("current_stage") == 7:
        stage7_result = validate_stage(7, workspace)
        stage7_gate = stage7_result.get("gate", "UNKNOWN")
        blocked = blocked or "BLOCKED" in str(stage7_gate)

    # Format human-readable output
    lines = []

    if "PASS" in gate:
        lines.append(f"✅ Stage {stage_num} gate passed")
    elif "BLOCKED" in gate:
        lines.append(f"❌ Stage {stage_num} gate blocked")
    else:
        lines.append(f"ℹ️ Stage {stage_num} gate: {gate}")

    if checks:
        for chk in checks:
            status = "✓" if chk.get("level") == "PASS" else "✗"
            lines.append(f"  {status} {chk.get('message', '')}")

    if warnings:
        for w in warnings:
            lines.append(f"  ⚠️ {w}")

    if stage7_result:
        lines.append(f"")
        lines.append(f"Stage 7 cascade integrity check")
        if "PASS" in stage7_gate:
            lines.append(f"  cascade intact")
        elif "BLOCKED" in stage7_gate:
            lines.append(f"  cascade may be incomplete; review below")
        for chk in stage7_result.get("checks", []):
            status = "✓" if chk.get("level") == "PASS" else "✗"
            lines.append(f"    {status} {chk.get('message', '')}")
        for w in stage7_result.get("warnings", []):
            lines.append(f"    ⚠️ {w}")

    if blocked:
        lines.append("")
        lines.append(HARD_STOP_MESSAGE)

    json.dump({
        "decision": "allow",
        "message": "\n".join(lines),
        "alpha_insights_gate": {
            "stage": stage_num,
            "gate": gate,
            "blocked": blocked,
            "semantic": "hard_stop" if blocked else "pass_or_warn",
            "stage7_gate": {
                "gate": stage7_gate,
                "blocked": "BLOCKED" in str(stage7_gate),
            } if stage7_result else None,
        },
    }, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Fail open + transparent: don't block, but warn that gate didn't run
        try:
            json.dump({
                "decision": "allow",
                "message": f"Stage gate hook error ({type(e).__name__}: {e}); this gate did not run. Manually inspect the gate checklist."
            }, sys.stdout, ensure_ascii=False)
        except Exception:
            sys.exit(0)  # last resort: silent fail open
