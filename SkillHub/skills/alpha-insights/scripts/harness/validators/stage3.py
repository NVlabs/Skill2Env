"""Stage 3: Planning Validator"""

from .common import (
    ValidationResult, file_exists, count_pattern,
    file_contains_keyword, file_contains_pattern,
)
from . import evidence_integrity


def validate(workspace):
    r = ValidationResult(3)
    f = "research_plan.md"

    if not file_exists(workspace, f):
        r.fail(f"{f} missing")
        return r
    r.pass_check(f"{f} exists")

    track_count = count_pattern(workspace, f, r"Track [A-G]")
    if track_count < 3:
        r.warn(f"only {track_count} Track entries detected; recommend at least 3")
    else:
        r.pass_check(f"Track count: {track_count}")

    has_hypothesis = (
        file_contains_pattern(workspace, f, r"H[0-9]")
        or file_contains_keyword(workspace, f, "\u5047\u8bbe")
    )
    if has_hypothesis:
        r.pass_check("hypothesis record present")
    else:
        r.warn("hypothesis record not detected (H1/H2 or hypothesis keyword)")

    has_interview_decision = (
        file_contains_keyword(workspace, f, "\u8bbf\u8c08")
        or file_contains_keyword(workspace, f, "interview")
    )
    if has_interview_decision:
        r.pass_check("interview decision record present")
    else:
        r.fail("interview decision record missing; propose interviews to the user and record the decision, even if declined")

    evidence_integrity.validate_stage3_plan(r, workspace, f)

    return r
