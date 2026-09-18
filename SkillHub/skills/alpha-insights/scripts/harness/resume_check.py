#!/usr/bin/env python3
"""
Alpha Insights — Resume Check (\u7528\u4e8e SKILL.md !`shell` \u5185\u8054\u8c03\u7528)

\u81ea\u52a8\u626b\u63cf workspace \u76ee\u5f55，\u8f93\u51fa\u65ad\u70b9\u7eed\u505a\u6458\u8981。
\u65e0\u53c2\u6570\u8fd0\u884c：\u4ece cwd \u5411\u4e0a\u626b\u63cf；\u5e26\u53c2\u6570\u8fd0\u884c：\u626b\u63cf\u6307\u5b9a\u76ee\u5f55。

\u8f93\u51fa\u8bbe\u8ba1\u4e3a\u4eba\u53ef\u8bfb，\u76f4\u63a5\u5d4c\u5165 SKILL prompt。
"""

import json
import os
import sys

STAGE_NAMES = {
    0: "Initialized", 1: "Briefing", 2: "Framing", 3: "Planning",
    4: "Research", 5: "Insights", 6: "Report", 7: "Iteration",
}

DELIVERABLES = {
    1: "user_brief.md", 2: "research_definition.md", 3: "research_plan.md",
    3.5: "interview_guides.md",
    4: "evidence_base.md", 5: "insights.md", 6: "report.html",
}

KNOWN_FILES = list(DELIVERABLES.values())


def find_workspaces(base_dir):
    """scan candidate workspace directories under base_dir"""
    found = []

    # Strategy 1: base_dir/workspace/*/
    ws_root = os.path.join(base_dir, "workspace")
    if os.path.isdir(ws_root):
        for entry in os.listdir(ws_root):
            candidate = os.path.join(ws_root, entry)
            if os.path.isdir(candidate):
                found.append(candidate)

    # Strategy 2: base_dir itself has deliverables
    for f in KNOWN_FILES:
        if os.path.isfile(os.path.join(base_dir, f)):
            found.append(base_dir)
            break

    return found


def workspace_summary(ws_path):
    """generate one workspace summary"""
    name = os.path.basename(ws_path)

    # Try _state.json first
    state_file = os.path.join(ws_path, "_state.json")
    if os.path.isfile(state_file):
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                state = json.load(f)
            stage = state.get("current_stage", 0)
            tier = state.get("tier", "?")
            completed = state.get("completed_stages", [])
            return {
                "name": name,
                "tier": tier,
                "current_stage": stage,
                "stage_name": STAGE_NAMES.get(stage, f"Stage {stage}"),
                "completed_stages": completed,
                "source": "_state.json",
            }
        except (json.JSONDecodeError, OSError):
            pass  # corrupted → fall through to deliverable inference

    # Fallback: infer from existing deliverable files
    existing = []
    for stage_num, filename in sorted(DELIVERABLES.items()):
        if os.path.isfile(os.path.join(ws_path, filename)):
            existing.append(stage_num)

    if not existing:
        return None

    max_stage = max(existing)
    return {
        "name": name,
        "tier": "?",
        "current_stage": max_stage,
        "stage_name": STAGE_NAMES.get(max_stage, f"Stage {max_stage}"),
        "completed_stages": existing,
        "source": "inferred",
    }


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

    if not os.path.isdir(base):
        print("No active research workspace found.")
        return

    workspaces = find_workspaces(base)
    if not workspaces:
        print("No active research workspace found.")
        return

    summaries = []
    for ws in workspaces:
        s = workspace_summary(ws)
        if s:
            summaries.append(s)

    if not summaries:
        print("No active research workspace found.")
        return

    # Sort by most advanced stage (descending)
    summaries.sort(key=lambda x: x["current_stage"], reverse=True)

    print(f"Found {len(summaries)} workspace(s):")
    for s in summaries:
        completed_str = ", ".join(str(c) for c in s["completed_stages"]) if s["completed_stages"] else "none"
        tier_str = f"Tier {s['tier']}" if s['tier'] != '?' else "Tier unknown"
        print(f"  - [{s['name']}] {tier_str} | Stage {s['current_stage']} ({s['stage_name']}) | Completed: [{completed_str}]")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("No active research workspace found.")
