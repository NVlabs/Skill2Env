import json
import contextlib
import importlib.util
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HOOK = Path(__file__).resolve().parents[1] / "harness" / "hooks" / "stage_gate_hook.py"
CODEX_PRE_HOOK = Path(__file__).resolve().parents[1] / "codex_hooks" / "alpha_insights_pre_tool.py"
CODEX_POST_HOOK = Path(__file__).resolve().parents[1] / "codex_hooks" / "alpha_insights_post_tool.py"


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_main_with_stdin(module, payload: dict) -> str:
    original_stdin = sys.stdin
    stdout = io.StringIO()
    try:
        sys.stdin = io.StringIO(json.dumps(payload, ensure_ascii=False))
        with contextlib.redirect_stdout(stdout):
            module.main()
    finally:
        sys.stdin = original_stdin
    return stdout.getvalue().strip()


def _write_hook_script(path: Path, body: str) -> None:
    path.write_text(
        "#!/usr/bin/env python3\n"
        "import sys\n"
        f"{body}\n",
        encoding="utf-8",
    )


class StageGateHookSemanticsTests(unittest.TestCase):
    def test_blocked_gate_is_semantic_hard_stop_but_allows_repair_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            brief = workspace / "user_brief.md"
            brief.write_text("议题：测试一个行业\n", encoding="utf-8")

            payload = {
                "cwd": str(workspace),
                "tool_input": {"file_path": str(brief)},
            }
            proc = subprocess.run(
                [sys.executable, str(HOOK)],
                input=json.dumps(payload, ensure_ascii=False),
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(proc.returncode, 0, proc.stderr)
            decoded = json.loads(proc.stdout)
            self.assertEqual(decoded["decision"], "allow")
            self.assertTrue(decoded["alpha_insights_gate"]["blocked"])
            self.assertEqual(decoded["alpha_insights_gate"]["semantic"], "hard_stop")
            self.assertIn("Alpha Insights HARD STOP", decoded["message"])
            self.assertIn("不得进入下一阶段", decoded["message"])

    def test_codex_post_wrapper_preserves_blocked_gate_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            brief = workspace / "user_brief.md"
            brief.write_text("议题：测试一个行业\n", encoding="utf-8")

            payload = {
                "cwd": str(workspace),
                "toolName": "Write",
                "toolInput": {"file_path": str(brief)},
            }
            proc = subprocess.run(
                [sys.executable, str(CODEX_POST_HOOK)],
                input=json.dumps(payload, ensure_ascii=False),
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(proc.returncode, 0, proc.stderr)
            decoded = json.loads(proc.stdout)
            self.assertEqual(decoded["decision"], "allow")
            self.assertTrue(decoded["alpha_insights_blocked"])
            self.assertTrue(decoded["alpha_insights_gates"][0]["blocked"])
            self.assertEqual(decoded["alpha_insights_gates"][0]["semantic"], "hard_stop")
            self.assertIn("Alpha Insights HARD STOP", decoded["message"])

    def test_codex_pre_wrapper_blocks_if_html_guard_child_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            failing_guard = workspace / "failing_guard.py"
            _write_hook_script(
                failing_guard,
                "sys.stdin.read()\n"
                "print('guard stderr boom', file=sys.stderr)\n"
                "sys.exit(7)",
            )
            module = _load_module(CODEX_PRE_HOOK, "alpha_insights_pre_hook_under_test")
            module.HTML_GUARD = failing_guard

            output = _run_main_with_stdin(module, {
                "toolName": "Write",
                "toolInput": {"file_path": str(workspace / "report.html")},
            })

            decoded = json.loads(output)
            self.assertEqual(decoded["decision"], "block")
            self.assertTrue(decoded["alpha_insights_hook_error"])
            self.assertIn("html guard failed", decoded["message"])
            self.assertIn("guard stderr boom", decoded["message"])

    def test_codex_post_wrapper_surfaces_stage_gate_child_failure_as_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            failing_gate = workspace / "failing_gate.py"
            noop_progress = workspace / "noop_progress.py"
            _write_hook_script(
                failing_gate,
                "sys.stdin.read()\n"
                "print('stage stderr boom', file=sys.stderr)\n"
                "sys.exit(9)",
            )
            _write_hook_script(noop_progress, "sys.stdin.read()\n")
            module = _load_module(CODEX_POST_HOOK, "alpha_insights_post_hook_under_test")
            module.STAGE_GATE_HOOK = failing_gate
            module.PROGRESS_LOGGER = noop_progress

            output = _run_main_with_stdin(module, {
                "toolName": "Write",
                "toolInput": {"file_path": str(workspace / "user_brief.md")},
            })

            decoded = json.loads(output)
            self.assertEqual(decoded["decision"], "allow")
            self.assertTrue(decoded["alpha_insights_blocked"])
            self.assertTrue(decoded["alpha_insights_hook_error"])
            self.assertEqual(decoded["alpha_insights_hook_errors"][0]["returncode"], 9)
            self.assertIn("stage gate hook failed", decoded["message"])
            self.assertIn("stage stderr boom", decoded["message"])


if __name__ == "__main__":
    unittest.main()
