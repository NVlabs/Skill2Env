"""Stage 5: Insights Validator"""

from .common import (
    ValidationResult, file_exists, file_contains_pattern,
    file_contains_keyword, count_pattern, get_tier,
)
from . import evidence_integrity


def validate(workspace):
    r = ValidationResult(5)
    f = "insights.md"
    tier = get_tier(workspace)

    if not file_exists(workspace, f):
        r.fail(f"{f} missing")
        return r
    r.pass_check(f"{f} exists")

    has_score = file_contains_pattern(workspace, f, r"[0-9]+\s*\u5206|\u8bc4\u5206|score|Score")
    if has_score:
        r.pass_check("insight score present")
    else:
        r.fail("insight score not detected")

    has_red = file_contains_pattern(workspace, f, r"\u7ea2\u961f|red.?team|Red.?Team|\u7ea2\u961f\u5ba1\u67e5")
    if has_red:
        r.pass_check("red-team review record present")
    else:
        r.fail("red-team review record not detected; required for all tiers")

    has_blue = file_contains_pattern(workspace, f, r"\u84dd\u961f|blue.?team|Blue.?Team|\u84dd\u961f\u5ba1\u67e5")
    if has_blue:
        r.pass_check("blue-team review record present")
    else:
        r.fail("blue-team review record not detected; required for all tiers")

    if has_red:
        has_substantive = file_contains_pattern(
            workspace, f, r"\u5b9e\u8d28|\u81f4\u547d|Substantive|Fatal"
        )
        if has_substantive:
            r.pass_check("red-team substantive/fatal challenge record present")
        else:
            r.warn("red-team review lacks substantive/fatal challenges; each core insight needs at least one substantive challenge")

    insight_count = count_pattern(workspace, f, r"(?:\u6d1e\u5bdf|Insight)\s*[I#]?\s*\d")
    if insight_count < 3:
        r.warn(f"only {insight_count} insights detected; recommend at least 3")

    has_confirm = file_contains_pattern(
        workspace, f, r"\u7528\u6237\u786e\u8ba4|\u5df2\u786e\u8ba4|\u5f85\u786e\u8ba4|\u5df2\u4fee\u6539"
    )
    if has_confirm:
        r.pass_check("user confirmation status present")
    else:
        r.warn("user confirmation status not detected; insights.md should record confirmation outcomes")

    has_key_var = (
        file_contains_keyword(workspace, f, "\u5173\u952e\u53d8\u91cf")
        or file_contains_keyword(workspace, f, "\u76d1\u6d4b\u6e05\u5355")
    )
    if has_key_var:
        r.pass_check("key-variable/watchlist record present")
    else:
        r.warn("key-variable watchlist not detected")

    so_what_count = count_pattern(workspace, f, r"So What|so what|So what")
    layer_markers = count_pattern(workspace, f, r"→.*→|⇒.*⇒|\u7b2c[\u4e00\u4e8c\u4e09\u56db1-4]\u5c42|Layer [1-4]|\u73b0\u8c61[\s\S]*?\u542b\u4e49[\s\S]*?\u7b56\u7565|\u542b\u4e49[\s\S]*?\u7b56\u7565[\s\S]*?\u884c\u52a8")
    depth_signal = max(so_what_count, layer_markers)
    if depth_signal >= 3:
        r.pass_check(f"So What depth signal: {depth_signal}（So What {so_what_count} matches + layer markers {layer_markers} matches)")
    else:
        r.warn(f"So What chain depth is thin (So What {so_what_count} matches + layer markers {layer_markers} matches; core insights require at least 3 reasoning layers)")

    has_premortem = (
        file_contains_keyword(workspace, f, "Pre-mortem")
        or file_contains_keyword(workspace, f, "pre-mortem")
        or file_contains_keyword(workspace, f, "\u98ce\u9669\u63d0\u793a")
        or file_contains_keyword(workspace, f, "\u5931\u8d25\u539f\u56e0")
    )
    if has_premortem:
        r.pass_check("pre-mortem risk record present")
    else:
        r.warn("pre-mortem risk record not detected")

    has_smart = (
        file_contains_keyword(workspace, f, "SMART")
        or file_contains_pattern(workspace, f, r"Specific|Measurable|Achievable|Relevant|Time.?bound")
        or file_contains_pattern(workspace, f, r"\*{2}[SMART]\*{2}\s*[:：]")
    )
    if has_smart:
        r.pass_check("SMART test record present")
    else:
        r.warn("SMART test record not detected")

    has_action = file_contains_keyword(workspace, f, "\u5efa\u8bae") or file_contains_keyword(workspace, f, "\u884c\u52a8")
    if has_action:
        r.pass_check("action recommendation present")
    else:
        r.warn("action recommendation not detected")

    evidence_integrity.validate_insight_confidence(r, workspace, f)

    return r
