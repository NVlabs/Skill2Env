"""Stage 3.5: Interview Prep Validator"""

from .common import (
    ValidationResult, file_exists, file_contains_keyword,
    file_contains_pattern, count_pattern,
)


def validate(workspace):
    r = ValidationResult(3.5)
    f = "interview_guides.md"

    if not file_exists(workspace, f):
        r.fail(f"{f} missing")
        return r
    r.pass_check(f"{f} exists")

    has_profile = (
        file_contains_keyword(workspace, f, "\u8bbf\u8c08\u5bf9\u8c61")
        or file_contains_keyword(workspace, f, "\u5bf9\u8c61\u753b\u50cf")
        or file_contains_keyword(workspace, f, "interviewee")
        or file_contains_keyword(workspace, f, "target role")
    )
    if has_profile:
        r.pass_check("interviewee profile present")
    else:
        r.fail("interviewee profile not detected")

    has_goal = (
        file_contains_keyword(workspace, f, "\u8bbf\u8c08\u76ee\u6807")
        or file_contains_keyword(workspace, f, "\u9a8c\u8bc1\u5047\u8bbe")
        or file_contains_keyword(workspace, f, "objective")
        or file_contains_keyword(workspace, f, "hypothesis")
    )
    if has_goal:
        r.pass_check("interview objective/hypothesis mapping present")
    else:
        r.fail("interview objective or hypothesis mapping not detected")

    has_questions = (
        file_contains_keyword(workspace, f, "\u95ee\u9898\u63d0\u7eb2")
        or file_contains_keyword(workspace, f, "\u6838\u5fc3\u95ee\u9898")
        or file_contains_keyword(workspace, f, "questions")
    )
    if has_questions:
        r.pass_check("question guide present")
    else:
        r.fail("question guide not detected")

    question_count = count_pattern(workspace, f, r"^\s*(?:[-*]|\d+[.)]|Q\d+[:：])")
    if question_count < 5:
        r.warn(f"{question_count} question items detected; interview guide may be thin")
    else:
        r.pass_check(f"question item count: {question_count}")

    has_reminder = (
        file_contains_keyword(workspace, f, "\u8bbf\u8c08\u7eaa\u8981")
        or file_contains_keyword(workspace, f, "\u539f\u59cb\u8bb0\u5f55")
        or file_contains_keyword(workspace, f, "notes")
    )
    if has_reminder:
        r.pass_check("post-interview material collection reminder present")
    else:
        r.warn("post-interview notes/raw-record collection reminder not detected")

    return r
