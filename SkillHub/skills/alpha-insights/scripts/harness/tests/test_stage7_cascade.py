import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HARNESS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HARNESS_DIR))

from validators.stage7 import validate


STAGE_GATE_HOOK = HARNESS_DIR / "hooks" / "stage_gate_hook.py"


def _write(path: Path, content: str = "ok\n", mtime: int = 1_700_000_000) -> None:
    path.write_text(content, encoding="utf-8")
    os.utime(path, (mtime, mtime))


class Stage7CascadeTests(unittest.TestCase):
    def _workspace(self) -> tempfile.TemporaryDirectory:
        return tempfile.TemporaryDirectory()

    def _write_stage7_state(self, workspace: Path) -> None:
        (workspace / "_state.json").write_text(
            json.dumps({"current_stage": 7, "disclosure_log": []}, ensure_ascii=False),
            encoding="utf-8",
        )

    def test_stage7_blocks_when_upstream_evidence_is_newer_than_insights(self) -> None:
        with self._workspace() as tmp:
            workspace = Path(tmp)
            self._write_stage7_state(workspace)
            _write(workspace / "research_definition.md", mtime=1_700_000_000)
            _write(workspace / "research_plan.md", mtime=1_700_000_100)
            _write(workspace / "evidence_base.md", mtime=1_700_000_500)
            _write(workspace / "insights.md", mtime=1_700_000_200)
            _write(workspace / "report.html", "<html>" + ("x" * 6000) + "</html>", mtime=1_700_000_300)

            result = validate(str(workspace)).to_dict()

            self.assertEqual(result["gate"], "BLOCKED ❌")
            self.assertTrue(any("级联不完整" in check["message"] for check in result["checks"]))
            self.assertTrue(any("evidence_base.md" in check["message"] for check in result["checks"]))

    def test_stage7_blocks_when_final_report_is_missing(self) -> None:
        with self._workspace() as tmp:
            workspace = Path(tmp)
            self._write_stage7_state(workspace)
            _write(workspace / "research_definition.md", mtime=1_700_000_000)
            _write(workspace / "research_plan.md", mtime=1_700_000_100)
            _write(workspace / "evidence_base.md", mtime=1_700_000_200)
            _write(workspace / "insights.md", mtime=1_700_000_300)

            result = validate(str(workspace)).to_dict()

            self.assertEqual(result["gate"], "BLOCKED ❌")
            self.assertTrue(any("report.html 不存在" in check["message"] for check in result["checks"]))

    def test_stage7_passes_when_downstream_artifacts_are_fresh(self) -> None:
        with self._workspace() as tmp:
            workspace = Path(tmp)
            self._write_stage7_state(workspace)
            _write(workspace / "research_definition.md", mtime=1_700_000_000)
            _write(workspace / "research_plan.md", mtime=1_700_000_100)
            _write(workspace / "evidence_base.md", mtime=1_700_000_200)
            _write(workspace / "insights.md", mtime=1_700_000_300)
            _write(workspace / "report.html", "<html>" + ("x" * 6000) + "</html>", mtime=1_700_000_400)

            result = validate(str(workspace)).to_dict()

            self.assertEqual(result["gate"], "PASS ✅")
            self.assertTrue(any("级联完整性通过" in check["message"] for check in result["checks"]))

    def test_stage_gate_hook_exposes_stage7_gate_metadata(self) -> None:
        with self._workspace() as tmp:
            workspace = Path(tmp)
            self._write_stage7_state(workspace)
            _write(workspace / "research_definition.md", mtime=1_700_000_000)
            _write(workspace / "research_plan.md", mtime=1_700_000_100)
            _write(workspace / "evidence_base.md", mtime=1_700_000_500)
            _write(workspace / "insights.md", mtime=1_700_000_200)
            _write(workspace / "report.html", "<html>" + ("x" * 6000) + "</html>", mtime=1_700_000_300)

            payload = {"cwd": str(workspace), "tool_input": {"file_path": str(workspace / "report.html")}}
            proc = subprocess.run(
                [sys.executable, str(STAGE_GATE_HOOK)],
                input=json.dumps(payload, ensure_ascii=False),
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(proc.returncode, 0, proc.stderr)
            decoded = json.loads(proc.stdout)
            self.assertTrue(decoded["alpha_insights_gate"]["blocked"])
            self.assertTrue(decoded["alpha_insights_gate"]["stage7_gate"]["blocked"])
            self.assertEqual(decoded["alpha_insights_gate"]["stage7_gate"]["gate"], "BLOCKED ❌")
            self.assertIn("Stage 7 级联完整性检查", decoded["message"])


if __name__ == "__main__":
    unittest.main()
