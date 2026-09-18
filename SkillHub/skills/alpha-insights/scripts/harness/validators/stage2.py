"""Stage 2: Framing Validator"""

from .common import ValidationResult, file_exists, file_contains_keyword, count_pattern, load_state


def validate(workspace):
    r = ValidationResult(2)
    f = "research_definition.md"

    if not file_exists(workspace, f):
        r.fail(f"{f} missing")
        return r
    r.pass_check(f"{f} exists")

    has_subq = (
        file_contains_keyword(workspace, f, "\u5b50\u95ee\u9898")
        or file_contains_keyword(workspace, f, "sub-question")
        or file_contains_keyword(workspace, f, "Q1")
    )
    if has_subq:
        r.pass_check("sub-questions present")
    else:
        r.fail("sub-questions not detected")

    has_lens = (
        file_contains_keyword(workspace, f, "\u900f\u955c")
        or file_contains_keyword(workspace, f, "lens")
        or file_contains_keyword(workspace, f, "\u5206\u6790\u900f\u955c")
    )
    if has_lens:
        r.pass_check("lens assignment present")
    else:
        r.fail("lens assignment not detected")

    framework_count = count_pattern(workspace, f, r"(?:\u6846\u67b6|framework|\u6a21\u578b|model)")
    if framework_count < 2:
        r.warn(f"framework/model mentions: {framework_count}; recommend at least 2 frameworks")

    state = load_state(workspace)
    if state and state.get("iqr_results"):
        iqr_data = state["iqr_results"].get("2")
        if iqr_data:
            result = iqr_data.get("result", "unknown")
            if result == "BLOCK":
                r.fail("IQR review blocked this stage; fix and resubmit")
            elif result in ("PASS", "REVISE"):
                r.pass_check(f"IQR review completed ({result}）")
            else:
                r.warn(f"Unexpected IQR review result: {result}")
        else:
            r.warn("Stage 2 IQR review record not detected; independent quality review is recommended")
    else:
        r.warn("IQR review record not detected; independent quality review is recommended")

    return r
