#!/usr/bin/env python3
"""
Alpha Insights — Stage Gate Validator

\u7edf\u4e00\u5165\u53e3，\u8c03\u7528\u5404 Stage Validator。

Usage:
    python3 stage_gate.py validate <stage_num> <workspace_path>
    python3 stage_gate.py validate-all <workspace_path>
"""

import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from validators import stage1, stage2, stage3, stage3_5, stage4, stage5, stage6, stage7


VALIDATORS = {
    1: stage1.validate,
    2: stage2.validate,
    3: stage3.validate,
    3.5: stage3_5.validate,
    4: stage4.validate,
    5: stage5.validate,
    6: stage6.validate,
    7: stage7.validate,
}


def parse_stage_num(raw):
    try:
        value = float(raw)
    except ValueError:
        raise ValueError(f"invalid stage number: {raw}")
    if value.is_integer():
        return int(value)
    return value


def is_blocked(result):
    return "BLOCKED" in str(result.get("gate", ""))


def validate_stage(stage_num, workspace):
    validator = VALIDATORS.get(stage_num)
    if validator is None:
        raise ValueError(f"Stage {stage_num}  has no validator")
    result = validator(workspace)
    return result.to_dict()


def validate_all(workspace):
    results = []
    for stage_num in sorted(VALIDATORS.keys()):
        results.append(validate_stage(stage_num, workspace))
    return results


def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python3 stage_gate.py validate <stage_num> <workspace_path>")
        print("  python3 stage_gate.py validate-all <workspace_path>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "validate":
        if len(sys.argv) < 4:
            print("error: validate requires <stage_num> <workspace_path>")
            sys.exit(1)
        stage_num = parse_stage_num(sys.argv[2])
        workspace = sys.argv[3]
        try:
            result = validate_stage(stage_num, workspace)
        except ValueError as exc:
            print(json.dumps({"stage": stage_num, "gate": "BLOCKED ❌", "error": str(exc)}, ensure_ascii=False, indent=2))
            sys.exit(1)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if is_blocked(result):
            sys.exit(1)

    elif command == "validate-all":
        workspace = sys.argv[2]
        results = validate_all(workspace)
        print(json.dumps(results, ensure_ascii=False, indent=2))
        if any(is_blocked(result) for result in results):
            sys.exit(1)

    else:
        print(f"unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
