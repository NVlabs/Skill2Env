"""Shared validation helper functions."""

import json
import os
import re


def load_state(workspace):
    """Load _state.json; return None when missing or invalid."""
    path = os.path.join(workspace, "_state.json")
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError, TypeError):
        return None


def get_tier(workspace):
    """Read research tier from _state.json; default to Tier 3."""
    state = load_state(workspace)
    if state:
        try:
            return int(state.get("tier", 3))
        except (ValueError, TypeError):
            return 3
    return 3


def file_exists(workspace, filename):
    return os.path.isfile(os.path.join(workspace, filename))


def file_line_count(workspace, filename):
    path = os.path.join(workspace, filename)
    if not os.path.isfile(path):
        return 0
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return sum(1 for _ in f)


def file_size_bytes(workspace, filename):
    path = os.path.join(workspace, filename)
    if not os.path.isfile(path):
        return 0
    return os.path.getsize(path)


def file_contains_keyword(workspace, filename, keyword):
    path = os.path.join(workspace, filename)
    if not os.path.isfile(path):
        return False
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    return keyword in content or keyword.lower() in content.lower()


def file_contains_pattern(workspace, filename, pattern):
    path = os.path.join(workspace, filename)
    if not os.path.isfile(path):
        return False
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    return bool(re.search(pattern, content, re.MULTILINE))


def count_pattern(workspace, filename, pattern):
    path = os.path.join(workspace, filename)
    if not os.path.isfile(path):
        return 0
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    return len(re.findall(pattern, content, re.MULTILINE))


def check_anti_patterns(workspace, filename):
    """Detect vague anti-pattern wording in reports."""
    anti_patterns = ["\u5168\u9762\u5206\u6790", "\u7efc\u5408\u8003\u8651", "\u9700\u8981\u8fdb\u4e00\u6b65\u7814\u7a76", "\u6709\u5f85\u89c2\u5bdf", "\u4e0d\u4e00\u800c\u8db3"]
    warnings = []
    for ap in anti_patterns:
        count = count_pattern(workspace, filename, re.escape(ap))
        if count > 0:
            warnings.append(f"Vague anti-pattern wording detected {count} time(s)")
    return warnings


class ValidationResult:
    """Validation result collector."""

    def __init__(self, stage):
        self.stage = stage
        self.checks = []
        self.warnings = []
        self.failed = False

    def fail(self, message):
        self.checks.append({"level": "FAIL", "message": message})
        self.failed = True

    def pass_check(self, message):
        self.checks.append({"level": "PASS", "message": message})

    def warn(self, message):
        self.warnings.append(message)

    def to_dict(self):
        return {
            "stage": self.stage,
            "gate": "BLOCKED ❌" if self.failed else "PASS ✅",
            "checks": self.checks,
            "warnings": self.warnings,
        }
