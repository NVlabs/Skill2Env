"""Stage 4: Research Validator"""

import os
import re

from .common import (
    ValidationResult, file_exists, file_line_count,
    file_contains_keyword, file_contains_pattern, count_pattern,
    get_tier, load_state,
)
from . import evidence_integrity


def _read(workspace, filename):
    path = os.path.join(workspace, filename)
    if not os.path.isfile(path):
        return ""
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def _validate_chapter_blueprint(r, workspace, tier):
    if tier < 2:
        return

    text = _read(workspace, "research_definition.md")
    if not text:
        r.fail("Tier 2/3 missing research_definition.md; cannot validate chapter blueprint")
        return

    has_blueprint = "\u7ae0\u8282\u84dd\u56fe" in text or "Chapter Blueprint" in text
    if not has_blueprint:
        r.fail("Tier 2/3 research_definition.md missing chapter blueprint")
        return

    blueprint_start = re.search(r"\u7ae0\u8282\u84dd\u56fe|Chapter Blueprint", text, re.IGNORECASE)
    blueprint_text = text[blueprint_start.start():] if blueprint_start else text
    if "❌" in blueprint_text:
        r.fail("Tier 2/3 chapter blueprint still has blocking gaps; research further or mark as unavailable with rationale")
    else:
        r.pass_check("Tier 2/3 chapter blueprint has no blocking gap marks")


def validate(workspace):
    r = ValidationResult(4)
    f = "evidence_base.md"
    tier = get_tier(workspace)

    if not file_exists(workspace, f):
        r.fail(f"{f} missing")
        return r
    r.pass_check(f"{f} exists")

    min_lines = {1: 10, 2: 20, 3: 40}.get(tier, 10)
    lines = file_line_count(workspace, f)
    if lines < min_lines:
        r.fail(f"only {lines} lines (Tier {tier} requires >= {min_lines}）")
    else:
        r.pass_check(f"line count: {lines}（Tier {tier} requires >= {min_lines}）")

    has_confidence = file_contains_pattern(workspace, f, r"[A-D]\s*\u7ea7|\u7f6e\u4fe1\u5ea6|confidence")
    if has_confidence:
        r.pass_check("confidence grading present")
    else:
        r.warn("confidence grading not detected")

    evidence_count = count_pattern(workspace, f, r"^\| [A-Z][0-9]+-[0-9]+")
    if evidence_count > 0:
        r.pass_check(f"standard evidence rows: {evidence_count} entries")
    else:
        r.warn("standard evidence rows not found (A1-01 format)")

    has_track = file_contains_pattern(workspace, f, r"Track [A-G]")
    if has_track:
        r.pass_check("Track labels present")
    else:
        r.warn("Track labels not detected")

    high_quality = count_pattern(workspace, f, r"[AB]\s*\u7ea7")
    if high_quality == 0:
        r.fail("A/B-grade evidence not detected; gate requires at least one >=B core evidence item")
    else:
        r.pass_check(f"A/B-grade evidence: {high_quality} entries")

    evidence_integrity.validate_evidence_base(r, workspace, f)
    _validate_chapter_blueprint(r, workspace, tier)

    total_evidence = count_pattern(workspace, f, r"[A-D]\s*\u7ea7")
    if total_evidence > 0:
        ratio = high_quality / total_evidence
        if ratio < 0.5:
            r.warn(f"share of B-or-better evidence: {ratio:.0%} (recommend >= 50%)")

    state = load_state(workspace)

    if state and state.get("interview_activated"):
        if state.get("interview_checkpoint_done"):
            result = state.get("interview_checkpoint_result", "unknown")
            r.pass_check(f"interview follow-up checkpoint completed (result: {result}）")
        else:
            r.warn("Stage 3.5 interviews are active, but the follow-up checkpoint has not run; ask the user for interview progress before generating evidence_base")

    has_framework = (
        file_contains_keyword(workspace, f, "\u6846\u67b6")
        or file_contains_keyword(workspace, f, "PESTEL")
        or file_contains_keyword(workspace, f, "Porter")
        or file_contains_keyword(workspace, f, "SWOT")
        or file_contains_pattern(workspace, f, r"\u6846\u67b6[\s\S]*?\u7ed3\u8bba|\u6846\u67b6[\s\S]*?\u5206\u6790")
    )
    if has_framework:
        r.pass_check("framework analysis record present")
    else:
        r.warn("framework analysis conclusion not detected; Stage 4 requires an explicit framework analysis output")

    if state and state.get("iqr_results"):
        iqr_data = state["iqr_results"].get("4")
        if iqr_data:
            result = iqr_data.get("result", "unknown")
            if result == "BLOCK":
                r.fail("IQR review blocked this stage; fix and resubmit")
            elif result in ("PASS", "REVISE"):
                r.pass_check(f"IQR review completed ({result}）")
            else:
                r.warn(f"Unexpected IQR review result: {result}")
        else:
            r.warn("Stage 4 IQR review record not detected; independent quality review is recommended")
    else:
        r.warn("IQR review record not detected; independent quality review is recommended")

    return r
