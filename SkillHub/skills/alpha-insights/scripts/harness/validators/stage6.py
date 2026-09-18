"""Stage 6: Report Validator"""

from .common import (
    ValidationResult, file_exists, file_size_bytes,
    file_contains_keyword, count_pattern, check_anti_patterns,
    get_tier, load_state,
)
from . import evidence_integrity


def validate(workspace):
    r = ValidationResult(6)
    f = "report.html"
    tier = get_tier(workspace)

    if not file_exists(workspace, f):
        r.fail(f"{f} missing")
        return r
    r.pass_check(f"{f} exists")

    size = file_size_bytes(workspace, f)
    if size < 5000:
        r.fail(f"file has only {size} bytes; report is incomplete and must be >= 5KB")
    else:
        r.pass_check(f"file size: {size} bytes")

    if file_contains_keyword(workspace, f, "chapter-section"):
        r.pass_check("chapter section present")
    else:
        r.fail("chapter-section missing; report has no body content")

    for section_id, label in [
        ("cover-page", "cover page"),
        ("toc-page", "TOC page"),
        ("footer-page", "footer page"),
    ]:
        if file_contains_keyword(workspace, f, section_id):
            r.pass_check(f"{label} exists")
        else:
            r.fail(f"{label} missing ({section_id}); complete report must include cover, TOC, and footer pages")

    # ECharts
    if file_contains_keyword(workspace, f, "echarts"):
        r.pass_check("ECharts reference present")
    else:
        r.warn("ECharts reference missing")

    if file_contains_keyword(workspace, f, "echarts.init"):
        r.pass_check("ECharts initialization code present")
    else:
        r.warn("ECharts initialization code missing")

    data_count = count_pattern(workspace, f, r'(?:"data"|(?<!")\bdata)\s*[:\[]')
    if data_count > 0:
        r.pass_check(f"ECharts data keys present ({data_count} matches)")
    else:
        r.warn("ECharts data key count is 0; model output may have filtered chart data")

    chart_count = count_pattern(workspace, f, r"echarts\.init")
    if tier >= 3 and chart_count < 6:
        r.fail(f"ECharts chart count is only {chart_count} (Tier 3 requires >=6)")
    elif tier >= 2 and chart_count < 3:
        r.fail(f"ECharts chart count is only {chart_count} (Tier 2 requires >=3)")
    elif chart_count >= 3:
        r.pass_check(f"ECharts charts: {chart_count} items")
    elif chart_count > 0:
        r.warn(f"ECharts chart count is only {chart_count} items")
    else:
        r.warn("No ECharts charts detected")

    chapter_count = count_pattern(workspace, f, r"chapter-header")
    if tier >= 3 and chapter_count < 4:
        r.warn(f"chapter count is only {chapter_count} (Tier 3 recommends 4-5 core chapters)")
    elif tier >= 2 and chapter_count < 2:
        r.warn(f"chapter count is only {chapter_count} (Tier 2 recommends 2-3 core chapters)")
    elif chapter_count > 0:
        r.pass_check(f"chapter count: {chapter_count}")

    ap_warnings = check_anti_patterns(workspace, f)
    for w in ap_warnings:
        r.warn(w)

    evidence_integrity.validate_report_links(r, workspace, f)

    if tier >= 2:
        has_blind_spot = (
            file_contains_keyword(workspace, f, "\u76f2\u533a")
            or file_contains_keyword(workspace, f, "blind spot")
            or file_contains_keyword(workspace, f, "Blind Spot")
        )
        if has_blind_spot:
            r.pass_check("blind-spot review present")
        else:
            r.warn("blind-spot review section not detected; Tier 2+ requires blind-spot analysis")

    state = load_state(workspace)
    if state and state.get("iqr_results"):
        iqr_data = state["iqr_results"].get("6")
        if iqr_data:
            result = iqr_data.get("result", "unknown")
            if result == "BLOCK":
                r.fail("IQR review blocked this stage; fix and resubmit")
            elif result in ("PASS", "REVISE"):
                r.pass_check(f"IQR review completed ({result}）")
            else:
                r.warn(f"Unexpected IQR review result: {result}")
        else:
            r.warn("Stage 6 IQR review record not detected; independent quality review is recommended")
    else:
        r.warn("IQR review record not detected; independent quality review is recommended")

    return r
