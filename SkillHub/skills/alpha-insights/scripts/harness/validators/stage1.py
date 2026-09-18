"""Stage 1: Briefing Validator"""

from .common import ValidationResult, file_exists, file_contains_keyword, file_line_count


def validate(workspace):
    r = ValidationResult(1)
    f = "user_brief.md"

    if not file_exists(workspace, f):
        r.fail(f"{f} missing")
        return r
    r.pass_check(f"{f} exists")

    has_topic = (
        file_contains_keyword(workspace, f, "\u8bae\u9898")
        or file_contains_keyword(workspace, f, "\u7814\u7a76\u95ee\u9898")
        or file_contains_keyword(workspace, f, "topic")
        or file_contains_keyword(workspace, f, "question")
    )
    if has_topic:
        r.pass_check("topic keyword present")
    else:
        r.fail("topic/research question not detected")

    has_tier = (
        file_contains_keyword(workspace, f, "Tier")
        or file_contains_keyword(workspace, f, "\u6863\u4f4d")
        or file_contains_keyword(workspace, f, "tier")
    )
    if has_tier:
        r.pass_check("tier information present")
    else:
        r.fail("Tier information not detected")

    lines = file_line_count(workspace, f)
    if lines < 3:
        r.warn(f"file has only {lines} lines; background may be too thin")

    return r
