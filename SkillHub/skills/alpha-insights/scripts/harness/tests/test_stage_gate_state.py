import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HARNESS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HARNESS_DIR))

from hooks._workspace_finder import find_workspace  # noqa: E402
from validators.stage1 import validate as validate_stage1  # noqa: E402

STAGE_GATE = HARNESS_DIR / "stage_gate.py"
STATE_MANAGER = HARNESS_DIR / "state_manager.py"


class StageGateCliTests(unittest.TestCase):
    def test_stage1_accepts_capitalized_english_topic_and_tier(self):
        with tempfile.TemporaryDirectory() as workspace:
            Path(workspace, "user_brief.md").write_text(
                "# User Brief\n\nTopic: Evaluate a market opportunity\nTier: Tier 1\nBackground: smoke test\n",
                encoding="utf-8",
            )

            result = validate_stage1(workspace).to_dict()

            self.assertEqual(result["gate"], "PASS ✅")

    def test_validate_all_exits_nonzero_when_any_stage_is_blocked(self):
        with tempfile.TemporaryDirectory() as workspace:
            result = subprocess.run(
                [sys.executable, str(STAGE_GATE), "validate-all", workspace],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.assertNotEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            self.assertTrue(any("BLOCKED" in item.get("gate", "") for item in payload))

    def test_unknown_stage_is_blocked_and_exits_nonzero(self):
        with tempfile.TemporaryDirectory() as workspace:
            result = subprocess.run(
                [sys.executable, str(STAGE_GATE), "validate", "8", workspace],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.assertNotEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            self.assertIn("无验证器", payload["error"])


class StateManagerStageTests(unittest.TestCase):
    def test_record_validation_accepts_stage_3_5(self):
        with tempfile.TemporaryDirectory() as workspace:
            subprocess.run(
                [sys.executable, str(STATE_MANAGER), "init", workspace, "--tier", "2"],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(STATE_MANAGER),
                    "record_validation",
                    workspace,
                    "--stage",
                    "3.5",
                    "--result",
                    '{"gate":"PASS ✅"}',
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["stage"], 3.5)

    def test_advance_rejects_invalid_stage(self):
        with tempfile.TemporaryDirectory() as workspace:
            subprocess.run(
                [sys.executable, str(STATE_MANAGER), "init", workspace, "--tier", "2"],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
            )

            result = subprocess.run(
                [sys.executable, str(STATE_MANAGER), "advance", workspace, "--stage", "99"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.assertNotEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            self.assertIn("无效 Stage 编号", payload["error"])


class WorkspaceFinderTests(unittest.TestCase):
    def test_interview_guides_counts_as_workspace_deliverable(self):
        with tempfile.TemporaryDirectory() as workspace:
            Path(workspace, "interview_guides.md").write_text("# interview guide\n", encoding="utf-8")

            self.assertEqual(find_workspace(workspace), workspace)


if __name__ == "__main__":
    unittest.main()
