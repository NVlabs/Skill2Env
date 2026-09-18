#!/usr/bin/env python3
"""Verify the Cloud Code compatible Alpha Insights skill package."""

from __future__ import annotations

import argparse
import json
import py_compile
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


SOURCE_ROOT = Path(__file__).resolve().parents[1]


class CheckSuite:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.lines: list[str] = []

    def ok(self, message: str) -> None:
        self.lines.append(f"PASS {message}")

    def fail(self, message: str) -> None:
        self.lines.append(f"FAIL {message}")
        self.failures.append(message)

    def require(self, condition: bool, message: str) -> None:
        if condition:
            self.ok(message)
        else:
            self.fail(message)

    def finish(self) -> None:
        for line in self.lines:
            print(line)
        if self.failures:
            print(f"\nverify_cloudcode: {len(self.failures)} failure(s)", file=sys.stderr)
            sys.exit(1)
        print("\nverify_cloudcode: OK")


def _frontmatter(text: str) -> str:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return ""
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return "\n".join(lines[1:idx])
    return ""


def _run_python(script: Path, payload: dict[str, Any]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script)],
        input=json.dumps(payload, ensure_ascii=False),
        text=True,
        capture_output=True,
        check=False,
    )


def _json_stdout(proc: subprocess.CompletedProcess[str]) -> dict[str, Any]:
    try:
        return json.loads(proc.stdout or "{}")
    except json.JSONDecodeError:
        return {}


def _compile_python(root: Path, checks: CheckSuite) -> None:
    failed = []
    for path in sorted(root.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            failed.append(f"{path}: {exc.msg}")
    checks.require(not failed, f"Python compile for {root}")
    for item in failed:
        checks.fail(item)


def _write_stage1_workspace(ws: Path, root: Path) -> None:
    subprocess.run(
        [sys.executable, str(root / "scripts" / "harness" / "state_manager.py"), "init", str(ws), "--tier", "1"],
        check=True,
        capture_output=True,
        text=True,
    )
    (ws / "user_brief.md").write_text(
        "# User Brief\n\ntopic: Evaluate a market opportunity\ntier: Tier 1\nbackground: smoke test\n",
        encoding="utf-8",
    )


def _write_interview_guides(ws: Path) -> None:
    (ws / "interview_guides.md").write_text(
        "\n".join([
            "# Interview Guides",
            "interviewee: industry operator",
            "objective: validate the hypothesis and identify risks",
            "questions:",
            "- Q1: What changed in demand?",
            "- Q2: Which competitors matter?",
            "- Q3: What costs are underestimated?",
            "- Q4: What adoption blockers exist?",
            "- Q5: What evidence would change your mind?",
            "notes: Ask the user to provide raw notes after interviews.",
        ]),
        encoding="utf-8",
    )


def _validate_stage(root: Path, stage: str, ws: Path) -> dict[str, Any]:
    proc = subprocess.run(
        [sys.executable, str(root / "scripts" / "harness" / "stage_gate.py"), "validate", stage, str(ws)],
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        return {"gate": "ERROR", "stderr": proc.stderr}
    return json.loads(proc.stdout)


def _smoke(root: Path, checks: CheckSuite) -> None:
    html_guard = root / "scripts" / "harness" / "hooks" / "html_write_guard.py"
    stage_hook = root / "scripts" / "harness" / "hooks" / "stage_gate_hook.py"
    progress = root / "scripts" / "harness" / "hooks" / "progress_logger.py"

    with tempfile.TemporaryDirectory(prefix="alpha-insights-cloudcode-verify-") as td:
        ws = Path(td)
        _write_stage1_workspace(ws, root)
        _write_interview_guides(ws)

        stage1 = _validate_stage(root, "1", ws)
        checks.require("PASS" in stage1.get("gate", ""), "Stage 1 validator smoke PASS")

        stage35 = _validate_stage(root, "3.5", ws)
        checks.require("PASS" in stage35.get("gate", ""), "Stage 3.5 validator smoke PASS")

        html_proc = _run_python(html_guard, {"tool_input": {"file_path": str(ws / "report.html")}})
        html = _json_stdout(html_proc)
        checks.require(html.get("decision") == "block", "Cloud Code HTML guard blocks .html writes")

        hook1_proc = _run_python(stage_hook, {
            "tool_input": {"file_path": str(ws / "user_brief.md")},
            "cwd": str(ws),
        })
        hook1 = _json_stdout(hook1_proc)
        checks.require("Stage 1" in hook1.get("message", ""), "Cloud Code stage hook emits Stage 1 result")

        hook35_proc = _run_python(stage_hook, {
            "tool_input": {"file_path": str(ws / "interview_guides.md")},
            "cwd": str(ws),
        })
        hook35 = _json_stdout(hook35_proc)
        checks.require("Stage 3.5" in hook35.get("message", ""), "Cloud Code stage hook emits Stage 3.5 result")

        _run_python(progress, {
            "tool_name": "Write",
            "tool_input": {"file_path": str(ws / "user_brief.md")},
            "cwd": str(ws),
        })
        log_path = ws / "_hook_log.jsonl"
        log_text = log_path.read_text(encoding="utf-8") if log_path.exists() else ""
        checks.require('"tool": "Write"' in log_text, "Cloud Code progress logger records Write")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-root", type=Path, default=SOURCE_ROOT)
    args = parser.parse_args()
    root = args.skill_root.expanduser()
    checks = CheckSuite()

    checks.require(root.is_dir(), f"skill root exists: {root}")
    skill_md = root / "SKILL.md"
    checks.require(skill_md.exists(), "SKILL.md exists")
    skill_text = skill_md.read_text(encoding="utf-8")
    fm = _frontmatter(skill_text)
    checks.require("hooks:" in fm, "SKILL.md frontmatter hooks present")
    checks.require("${CLAUDE_PLUGIN_ROOT}/scripts/harness/hooks/html_write_guard.py" in fm, "HTML guard uses CLAUDE_PLUGIN_ROOT")
    checks.require("${CLAUDE_PLUGIN_ROOT}/scripts/harness/hooks/stage_gate_hook.py" in fm, "Stage gate hook uses CLAUDE_PLUGIN_ROOT")
    checks.require("${CLAUDE_PLUGIN_ROOT}/scripts/harness/hooks/progress_logger.py" in fm, "Progress logger uses CLAUDE_PLUGIN_ROOT")
    checks.require("${CLAUDE_SKILL_DIR}/scripts/harness/resume_check.py" in skill_text, "Resume check uses CLAUDE_SKILL_DIR")

    required = [
        root / "scripts" / "harness" / "hooks" / "html_write_guard.py",
        root / "scripts" / "harness" / "hooks" / "stage_gate_hook.py",
        root / "scripts" / "harness" / "hooks" / "progress_logger.py",
        root / "scripts" / "harness" / "validators" / "stage3_5.py",
        root / "scripts" / "codex_hooks" / "alpha_insights_pre_tool.py",
        root / "scripts" / "codex_hooks" / "alpha_insights_post_tool.py",
    ]
    for path in required:
        checks.require(path.exists(), f"required file exists: {path.relative_to(root)}")

    _compile_python(root / "scripts", checks)
    _smoke(root, checks)
    checks.finish()


if __name__ == "__main__":
    main()

