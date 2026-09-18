#!/usr/bin/env python3
"""
Alpha Insights — Workspace State Manager

\u5916\u90e8\u72b6\u6001\u8ffd\u8e2a，\u8ba9 AI \u7684\u6267\u884c\u8def\u5f84\u53ef\u5ba1\u8ba1。
\u7ba1\u7406 workspace/_state.json \u6587\u4ef6。

Usage:
    python3 state_manager.py init <workspace> --tier 2
    python3 state_manager.py advance <workspace> --stage 2
    python3 state_manager.py log <workspace> --type file_load --detail "📚 \u52a0\u8f7d X"
    python3 state_manager.py status <workspace>
"""

import json
import sys
import os
from datetime import datetime, timezone

STATE_FILE = "_state.json"
VERSION = "2.0"

STAGE_NAMES = {
    0: "Initialized",
    1: "Briefing",
    2: "Framing",
    3: "Planning",
    3.5: "Interview",
    4: "Research",
    5: "Insights",
    6: "Report",
    7: "Iteration",
}

STAGE_DELIVERABLES = {
    1: "user_brief.md",
    2: "research_definition.md",
    3: "research_plan.md",
    3.5: "interview_guides.md",
    4: "evidence_base.md",
    5: "insights.md",
    6: "report.html",
}

VALID_STAGES = set(STAGE_NAMES)


def _now():
    return datetime.now(timezone.utc).isoformat()


def _state_path(workspace):
    return os.path.join(workspace, STATE_FILE)


def parse_stage(raw):
    """Parse and validate a stage number."""
    try:
        stage = float(raw)
    except (TypeError, ValueError):
        raise ValueError(f"invalid stage number: {raw}") from None
    if stage.is_integer():
        stage = int(stage)
    if stage not in VALID_STAGES:
        valid = ", ".join(str(s) for s in sorted(VALID_STAGES))
        raise ValueError(f"invalid stage number: {raw}. Valid values: {valid}")
    return stage


def _load_state(workspace):
    path = _state_path(workspace)
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(json.dumps({"warning": f"_state.json read failed: {e}; treating as missing"}, ensure_ascii=False), file=sys.stderr)
        return None


def _save_state(workspace, state):
    state["updated_at"] = _now()
    path = _state_path(workspace)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def cmd_init(workspace, tier=3):
    """initialize workspace state"""
    os.makedirs(workspace, exist_ok=True)
    state = {
        "version": VERSION,
        "workspace": os.path.abspath(workspace),
        "created_at": _now(),
        "updated_at": _now(),
        "tier": tier,
        "current_stage": 0,
        "completed_stages": [],
        "stage_history": [],
        "frameworks_loaded": [],
        "methodologies_loaded": [],
        "files_loaded": [],
        "disclosure_log": [],
        "validation_results": [],
        "interview_activated": False,
        "interview_checkpoint_done": False,
        "interview_checkpoint_result": None,
    }
    _save_state(workspace, state)
    print(json.dumps({"action": "init", "workspace": workspace, "tier": tier, "status": "OK ✅"}, ensure_ascii=False))


def cmd_advance(workspace, stage):
    """advance to target stage"""
    if stage not in VALID_STAGES:
        valid = ", ".join(str(s) for s in sorted(VALID_STAGES))
        print(json.dumps({"error": f"invalid stage number: {stage}. Valid values: {valid}"}, ensure_ascii=False))
        sys.exit(1)

    state = _load_state(workspace)
    if state is None:
        print(json.dumps({"error": f"No _state.json in {workspace}. Run 'init' first."}, ensure_ascii=False))
        sys.exit(1)

    prev_stage = state["current_stage"]

    if stage <= prev_stage and prev_stage > 0:
        print(json.dumps({
            "error": f"cannot move backward from Stage {prev_stage} to Stage {stage}. Use the Stage 7 iteration flow for rollback.",
            "action": "advance",
            "status": "BLOCKED ❌",
        }, ensure_ascii=False))
        sys.exit(1)

    if prev_stage > 0 and prev_stage not in state["completed_stages"]:
        state["completed_stages"].append(prev_stage)
        for entry in reversed(state["stage_history"]):
            if entry["stage"] == prev_stage and entry.get("completed") is None:
                entry["completed"] = _now()
                break

    state["current_stage"] = stage
    state["stage_history"].append({
        "stage": stage,
        "name": STAGE_NAMES.get(stage, f"Stage {stage}"),
        "started": _now(),
        "completed": None,
        "deliverable": STAGE_DELIVERABLES.get(stage),
    })

    _save_state(workspace, state)
    print(json.dumps({
        "action": "advance",
        "from_stage": prev_stage,
        "to_stage": stage,
        "stage_name": STAGE_NAMES.get(stage, f"Stage {stage}"),
        "status": "OK ✅",
    }, ensure_ascii=False))


def cmd_log(workspace, log_type, detail):
    """record disclosure log"""
    state = _load_state(workspace)
    if state is None:
        print(json.dumps({"error": f"No _state.json in {workspace}. Run 'init' first."}, ensure_ascii=False))
        sys.exit(1)

    entry = {
        "timestamp": _now(),
        "stage": state["current_stage"],
        "type": log_type,
        "detail": detail,
    }
    state["disclosure_log"].append(entry)

    if log_type == "file_load":
        filename = detail.replace("📚 \u52a0\u8f7d ", "").replace("📚 \u52a0\u8f7d", "").strip()
        if filename and filename not in state["files_loaded"]:
            state["files_loaded"].append(filename)
    elif log_type == "framework":
        if detail not in state["frameworks_loaded"]:
            state["frameworks_loaded"].append(detail)
    elif log_type == "methodology":
        if detail not in state["methodologies_loaded"]:
            state["methodologies_loaded"].append(detail)
    elif log_type == "interview_activated":
        state["interview_activated"] = True
    elif log_type == "interview_declined":
        state["interview_activated"] = False
    elif log_type == "interview_checkpoint_done":
        state["interview_checkpoint_done"] = True
        state["interview_checkpoint_result"] = detail  # "completed" / "deferred" / "cancelled"
    elif log_type == "iqr_result":
        if "iqr_results" not in state:
            state["iqr_results"] = {}
        state["iqr_results"][str(state["current_stage"])] = {
            "result": detail,  # "PASS" / "REVISE" / "BLOCK"
            "timestamp": _now(),
        }

    _save_state(workspace, state)
    print(json.dumps({"action": "log", "entry": entry, "status": "OK ✅"}, ensure_ascii=False))


def cmd_status(workspace):
    """print current state summary"""
    state = _load_state(workspace)
    if state is None:
        print(json.dumps({"error": f"No _state.json in {workspace}."}, ensure_ascii=False))
        sys.exit(1)

    summary = {
        "tier": state["tier"],
        "current_stage": state["current_stage"],
        "current_stage_name": STAGE_NAMES.get(state["current_stage"], "Unknown"),
        "completed_stages": state["completed_stages"],
        "frameworks_loaded": len(state["frameworks_loaded"]),
        "methodologies_loaded": len(state["methodologies_loaded"]),
        "files_loaded": len(state["files_loaded"]),
        "disclosure_count": len(state["disclosure_log"]),
        "validation_results": state["validation_results"][-3:] if state["validation_results"] else [],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def cmd_record_validation(workspace, stage, result_json):
    """record validation result"""
    state = _load_state(workspace)
    if state is None:
        print(json.dumps({"error": f"No _state.json in {workspace}."}, ensure_ascii=False))
        sys.exit(1)

    result = json.loads(result_json) if isinstance(result_json, str) else result_json
    result["recorded_at"] = _now()
    state["validation_results"].append(result)
    _save_state(workspace, state)
    print(json.dumps({"action": "record_validation", "stage": stage, "status": "OK ✅"}, ensure_ascii=False))


def main():
    if len(sys.argv) < 3:
        print("Usage: state_manager.py <command> <workspace> [options]")
        print("Commands: init, advance, log, status, record_validation")
        sys.exit(1)

    command = sys.argv[1]
    workspace = sys.argv[2]

    if command == "init":
        tier = 3
        for i, arg in enumerate(sys.argv):
            if arg == "--tier" and i + 1 < len(sys.argv):
                tier = int(sys.argv[i + 1])
        cmd_init(workspace, tier)

    elif command == "advance":
        stage = None
        for i, arg in enumerate(sys.argv):
            if arg == "--stage" and i + 1 < len(sys.argv):
                try:
                    stage = parse_stage(sys.argv[i + 1])
                except ValueError as exc:
                    print(json.dumps({"error": str(exc)}, ensure_ascii=False))
                    sys.exit(1)
        if stage is None:
            print("error: advance requires --stage N")
            sys.exit(1)
        cmd_advance(workspace, stage)

    elif command == "log":
        log_type = None
        detail = None
        for i, arg in enumerate(sys.argv):
            if arg == "--type" and i + 1 < len(sys.argv):
                log_type = sys.argv[i + 1]
            if arg == "--detail" and i + 1 < len(sys.argv):
                detail = sys.argv[i + 1]
        if not log_type or not detail:
            print("error: log requires --type and --detail")
            sys.exit(1)
        cmd_log(workspace, log_type, detail)

    elif command == "status":
        cmd_status(workspace)

    elif command == "record_validation":
        stage = None
        result_json = None
        for i, arg in enumerate(sys.argv):
            if arg == "--stage" and i + 1 < len(sys.argv):
                try:
                    stage = parse_stage(sys.argv[i + 1])
                except ValueError as exc:
                    print(json.dumps({"error": str(exc)}, ensure_ascii=False))
                    sys.exit(1)
            if arg == "--result" and i + 1 < len(sys.argv):
                result_json = sys.argv[i + 1]
        if stage is None or result_json is None:
            print("error: record_validation requires --stage and --result")
            sys.exit(1)
        cmd_record_validation(workspace, stage, result_json)

    else:
        print(f"unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
