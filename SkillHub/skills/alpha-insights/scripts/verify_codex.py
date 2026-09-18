#!/usr/bin/env python3
"""Verify a Codex Desktop installation of Alpha Insights."""

from __future__ import annotations

import argparse
import json
import os
import py_compile
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


SKILL_NAME = "alpha-insights"


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
            print(f"\nverify_codex: {len(self.failures)} failure(s)", file=sys.stderr)
            sys.exit(1)
        print("\nverify_codex: OK")


def _codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex").expanduser()


def _has_frontmatter_hooks(skill_md: Path) -> bool:
    lines = skill_md.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return False
    for line in lines[1:]:
        if line.strip() == "---":
            return False
        if line.startswith("hooks:"):
            return True
    return False


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


def _check_hooks_json(hooks_json: Path, root: Path, checks: CheckSuite) -> None:
    try:
        data = json.loads(hooks_json.read_text(encoding="utf-8"))
    except Exception as exc:
        checks.fail(f"hooks.json readable JSON: {exc}")
        return
    checks.ok(f"hooks.json readable: {hooks_json}")

    expected = {
        "PreToolUse": root / "scripts" / "codex_hooks" / "alpha_insights_pre_tool.py",
        "PostToolUse": root / "scripts" / "codex_hooks" / "alpha_insights_post_tool.py",
    }
    hooks = data.get("hooks", {})
    for event, script in expected.items():
        command = f"python3 {script}"
        found = False
        for entry in hooks.get(event, []):
            for hook in entry.get("hooks", []):
                if hook.get("command") == command:
                    found = True
        checks.require(found, f"{event} wrapper registered: {command}")


def _write_stage1_workspace(ws: Path, root: Path) -> None:
    subprocess.run(
        [sys.executable, str(root / "scripts" / "harness" / "state_manager.py"), "init", str(ws), "--tier", "1"],
        check=True,
        capture_output=True,
        text=True,
    )
    (ws / "user_brief.md").write_text(
        "# User Brief\n\nTopic: Evaluate a market opportunity\nTier: Tier 1\nBackground: smoke test\n",
        encoding="utf-8",
    )


def _write_interview_guides(ws: Path) -> None:
    (ws / "interview_guides.md").write_text(
        "\n".join([
            "# Interview Guide",
            "Interviewee: industry operator",
            "Interview objective: validate hypotheses and identify risks",
            "Question guide:",
            "- Q1: What changed in demand?",
            "- Q2: Which competitors matter?",
            "- Q3: What costs are underestimated?",
            "- Q4: What adoption blockers exist?",
            "- Q5: What evidence would change your mind?",
            "Interview notes: Ask the user to provide raw notes after interviews.",
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
    pre = root / "scripts" / "codex_hooks" / "alpha_insights_pre_tool.py"
    post = root / "scripts" / "codex_hooks" / "alpha_insights_post_tool.py"
    with tempfile.TemporaryDirectory(prefix="alpha-insights-codex-verify-") as td:
        ws = Path(td)
        _write_stage1_workspace(ws, root)
        _write_interview_guides(ws)

        stage1 = _validate_stage(root, "1", ws)
        checks.require("PASS" in stage1.get("gate", ""), "Stage 1 validator smoke PASS")

        stage35 = _validate_stage(root, "3.5", ws)
        checks.require("PASS" in stage35.get("gate", ""), "Stage 3.5 validator smoke PASS")

        html_proc = _run_python(pre, {
            "toolName": "Write",
            "toolInput": {"file_path": str(ws / "report.html")},
            "cwd": str(ws),
        })
        html = _json_stdout(html_proc)
        checks.require(html.get("decision") == "block", "Codex PreToolUse HTML guard blocks .html writes")

        post1_proc = _run_python(post, {
            "toolName": "Write",
            "toolInput": {"file_path": str(ws / "user_brief.md")},
            "cwd": str(ws),
        })
        post1 = _json_stdout(post1_proc)
        checks.require("Stage 1" in post1.get("message", ""), "Codex PostToolUse Stage 1 hook emits gate result")

        post35_proc = _run_python(post, {
            "toolName": "Write",
            "toolInput": {"file_path": str(ws / "interview_guides.md")},
            "cwd": str(ws),
        })
        post35 = _json_stdout(post35_proc)
        checks.require("Stage 3.5" in post35.get("message", ""), "Codex PostToolUse Stage 3.5 hook emits gate result")

        log_path = ws / "_hook_log.jsonl"
        log_text = log_path.read_text(encoding="utf-8") if log_path.exists() else ""
        checks.require('"tool": "Write"' in log_text, "Codex progress logger records camelCase payload as Write")


def main() -> None:
    codex_home = _codex_home()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-root", type=Path, default=codex_home / "skills" / SKILL_NAME)
    parser.add_argument("--hooks-json", type=Path, default=codex_home / "hooks.json")
    args = parser.parse_args()

    root = args.skill_root.expanduser()
    checks = CheckSuite()

    checks.require(root.is_dir(), f"skill root exists: {root}")
    checks.require(not (root / ".git").exists(), "installed Codex skill root is not a git repository")
    required = [
        root / "SKILL.md",
        root / "scripts" / "codex_hooks" / "alpha_insights_pre_tool.py",
        root / "scripts" / "codex_hooks" / "alpha_insights_post_tool.py",
        root / "scripts" / "harness" / "hooks" / "html_write_guard.py",
        root / "scripts" / "harness" / "hooks" / "stage_gate_hook.py",
        root / "scripts" / "harness" / "hooks" / "progress_logger.py",
        root / "scripts" / "harness" / "validators" / "stage3_5.py",
    ]
    for path in required:
        checks.require(path.exists(), f"required file exists: {path.relative_to(root)}")

    skill_text = (root / "SKILL.md").read_text(encoding="utf-8")
    checks.require(not _has_frontmatter_hooks(root / "SKILL.md"), "Codex installed SKILL.md has no Cloud Code frontmatter hooks")
    checks.require("${CLAUDE_" not in skill_text, "Codex installed SKILL.md has no CLAUDE_* placeholders")
    checks.require(str(root / "scripts" / "harness" / "resume_check.py") in skill_text, "Codex resume check uses installed absolute path")

    _check_hooks_json(args.hooks_json.expanduser(), root, checks)
    _compile_python(root / "scripts", checks)
    _smoke(root, checks)
    checks.finish()


if __name__ == "__main__":
    main()

