#!/usr/bin/env python3
"""
Alpha Insights — Review Dashboard

Summarize the full research quality picture before Stage 5 -> Stage 6.
Read _state.json plus stage deliverables and extract quality indicators.

Usage:
    python3 scripts/harness/dashboard.py <workspace_path>

Output:
    Human-readable quality dashboard text, not JSON, suitable for direct display.
"""

import json
import os
import re
import sys


def _load_state(workspace):
    path = os.path.join(workspace, "_state.json")
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def _read_file(workspace, filename):
    path = os.path.join(workspace, filename)
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _file_exists(workspace, filename):
    return os.path.isfile(os.path.join(workspace, filename))


def _file_size(workspace, filename):
    path = os.path.join(workspace, filename)
    if not os.path.isfile(path):
        return 0
    return os.path.getsize(path)


# ── Stage 1: Briefing ──

def assess_stage1(workspace):
    content = _read_file(workspace, "user_brief.md")
    if content is None:
        return "missing", []

    details = []
    line_count = len(content.strip().split("\n"))
    details.append(f"{line_count} lines")

    has_topic = bool(re.search(r"\u8bae\u9898|\u7814\u7a76\u95ee\u9898|topic|question", content, re.IGNORECASE))
    has_tier = bool(re.search(r"Tier|\u6863\u4f4d|tier", content, re.IGNORECASE))
    if has_topic:
        details.append("topic present")
    else:
        details.append("topic not detected")
    if has_tier:
        details.append("tier present")
    else:
        details.append("tier not detected")

    status = "✅" if has_topic and has_tier else "⚠️"
    return status, details


# ── Stage 2: Research Definition ──

def assess_stage2(workspace):
    content = _read_file(workspace, "research_definition.md")
    if content is None:
        return "missing", []

    details = []
    q_count = len(re.findall(r"(?:^|\n)\s*(?:Q\d|\u5b50\u95ee\u9898|Sub-question)", content, re.IGNORECASE))
    if q_count == 0:
        q_count = len(re.findall(r"(?:^|\n)\s*\d+\.\s", content))
    details.append(f"sub-questions {q_count} items")

    if "MECE" in content or "mece" in content.lower():
        details.append("MECE ✓")

    fw_matches = re.findall(r"(?:\u6846\u67b6|framework|\u6a21\u578b|model)[：:]\s*(\S+)", content, re.IGNORECASE)
    fw_count = len(fw_matches)
    if fw_count > 0:
        details.append(f"Frameworks: {' + '.join(fw_matches[:3])}")
    else:
        state = _load_state(workspace)
        if state and state.get("frameworks_loaded"):
            fw_names = state["frameworks_loaded"]
            details.append(f"Frameworks: {' + '.join(fw_names[:3])}")

    return "✅ produced", details


# ── Stage 3: Research Plan ──

def assess_stage3(workspace):
    content = _read_file(workspace, "research_plan.md")
    if content is None:
        return "missing", []

    details = []
    h_count = len(re.findall(r"(?:^|\n)\s*H\d", content))
    if h_count == 0:
        h_count = len(re.findall(r"\u5047\u8bbe", content))
    details.append(f"hypotheses {h_count} items")

    qh_map = re.findall(r"→\s*Q\d|Q\d.*→|\u5bf9\u5e94.*Q\d", content)
    if qh_map:
        details.append("Q->H->Lens mapping present")

    ds_count = len(re.findall(r"Track\s+[A-G]", content))
    if ds_count > 0:
        details.append(f"data tracks {ds_count} categories")

    return "✅ produced", details


# ── Stage 4: Evidence Base ──

def assess_stage4(workspace):
    content = _read_file(workspace, "evidence_base.md")
    if content is None:
        return "missing", []

    details = []
    lines = content.strip().split("\n")
    details.append(f"evidence {len(lines)} lines")

    a_count = len(re.findall(r"\bA\s*\u7ea7|\u7f6e\u4fe1\u5ea6.*A|confidence.*A", content, re.IGNORECASE))
    b_count = len(re.findall(r"\bB\s*\u7ea7|\u7f6e\u4fe1\u5ea6.*B|confidence.*B", content, re.IGNORECASE))
    c_count = len(re.findall(r"\bC\s*\u7ea7|\u7f6e\u4fe1\u5ea6.*C|confidence.*C", content, re.IGNORECASE))
    total = a_count + b_count + c_count
    if total > 0:
        a_pct = round(a_count / total * 100)
        b_pct = round(b_count / total * 100)
        c_pct = round(c_count / total * 100)
        details.append(f"Grade A {a_pct}% · Grade B {b_pct}% · Grade C {c_pct}%")
        if (a_count + b_count) / total < 0.5:
            details.append("B-or-better share below 50%")

    has_map = bool(re.search(r"\u6846\u67b6\u8bc1\u636e\u5730\u56fe|Framework Evidence Map", content, re.IGNORECASE))
    if has_map:
        done = len(re.findall(r"✅", content))
        pending = len(re.findall(r"⏳", content))
        na = len(re.findall(r"➖", content))
        gap = len(re.findall(r"⚠️", content))
        details.append(f"framework map ✅{done} ⏳{pending} ⚠️{gap} ➖{na}")
    else:
        details.append("framework evidence map not detected")

    return "✅ produced", details


# ── Stage 5: Insights ──

def assess_stage5(workspace):
    content = _read_file(workspace, "insights.md")
    if content is None:
        return "missing", []

    details = []
    content_for_scores = content.replace("**", "")
    scores = re.findall(r"(\d{1,2})\s*[/／]\s*20|\u8bc4\u5206[：:]\s*(\d{1,2})|=\s*(\d{1,2})\s*\u5206", content_for_scores)
    score_values = [int(s[0] or s[1] or s[2]) for s in scores if (s[0] or s[1] or s[2])]

    if score_values:
        core = [s for s in score_values if s >= 18]
        secondary = [s for s in score_values if 16 <= s < 18]
        details.append(f"insights {len(score_values)} items")
        if core:
            details.append(f"Core A insights {len(core)} (18-20 points)")
        if secondary:
            details.append(f"Core B insights {len(secondary)} (16-17 points)")
    else:
        details.append("score not detected")

    has_red = bool(re.search(r"\u7ea2\u961f|red.?team", content, re.IGNORECASE))
    has_blue = bool(re.search(r"\u84dd\u961f|blue.?team", content, re.IGNORECASE))
    if has_red and has_blue:
        fatal = re.findall(r"\u81f4\u547d", content)
        if fatal:
            details.append(f"red team: {len(fatal)} fatal challenges handled")
        else:
            details.append("red/blue-team review present")
    elif has_red:
        details.append("red-team review present | blue-team missing")
    elif has_blue:
        details.append("red-team missing | blue-team review present")

    return "✅ produced", details


# ── Overall Assessment ──

def overall_assessment(stages):
    """Generate the overall assessment from stage statuses."""
    failed = [name for name, (status, _) in stages.items() if "❌" in status]
    warnings = []
    for name, (_, details) in stages.items():
        for d in details:
            if "⚠️" in d:
                warnings.append(f"{name}: {d}")

    if failed:
        return f"❌ {len(failed)} stage deliverables missing ({', '.join(failed)}); fix before entering Stage 6"
    elif warnings:
        return f"⚠️ overall passed with {len(warnings)} warnings to review"
    else:
        return "✅ all checks passed; ready for Stage 6 report generation"


def generate_dashboard(workspace):
    """Generate the research quality dashboard."""
    stages = {
        "User Brief (S1)": assess_stage1(workspace),
        "Research Definition (S2)": assess_stage2(workspace),
        "Research Plan (S3)": assess_stage3(workspace),
        "Evidence Base (S4)": assess_stage4(workspace),
        "Insights (S5)": assess_stage5(workspace),
    }

    state = _load_state(workspace)
    tier_str = f"Tier {state['tier']}" if state and "tier" in state else "unknown"

    lines = []
    lines.append("=== Research Quality Dashboard ===")
    lines.append(f"Research tier: {tier_str}")
    lines.append("")

    for name, (status, details) in stages.items():
        detail_str = " | ".join(details) if details else "no details"
        lines.append(f"📋 {name}   {status} | {detail_str}")

    lines.append("")
    lines.append(f"Overall assessment: {overall_assessment(stages)}")
    lines.append("━━━━━━━━━━━━━━━━━━━")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 dashboard.py <workspace_path>")
        sys.exit(1)

    workspace = sys.argv[1]
    if not os.path.isdir(workspace):
        print(f"error: workspace directory does not exist: {workspace}")
        sys.exit(1)

    print(generate_dashboard(workspace))


if __name__ == "__main__":
    main()
