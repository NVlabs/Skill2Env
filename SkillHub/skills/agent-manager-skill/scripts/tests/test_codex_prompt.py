from __future__ import annotations
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import tmux_helper  # noqa: E402


class CodexPromptDetectionTests(unittest.TestCase):
    def test_detects_upgrade_model_choice_prompt(self):
        output = """
Codex just got an upgrade. Introducing gpt-5.2-codex.

Choose how you'd like Codex to proceed.

› 1. Try new model
  2. Use existing model
"""
        self.assertTrue(tmux_helper._is_codex_model_choice_prompt(output))

    def test_detects_generic_model_choice_prompt(self):
        output = """
Choose how you'd like Codex to proceed.
› 1. Try new model
  2. Use existing model
"""
        self.assertTrue(tmux_helper._is_codex_model_choice_prompt(output))

    def test_does_not_flag_regular_prompt_or_suggestions(self):
        output = """
› Summarize the changes
❯
"""
        self.assertFalse(tmux_helper._is_codex_model_choice_prompt(output))

    def test_menu_option_regex_matches_numbered_options_only(self):
        self.assertIsNotNone(tmux_helper._CODEX_MENU_OPTION_RE.match("› 1. Try new model"))
        self.assertIsNotNone(tmux_helper._CODEX_MENU_OPTION_RE.match("❯ 2. Use existing model"))
        self.assertIsNone(tmux_helper._CODEX_MENU_OPTION_RE.match("› Summarize the changes"))
        self.assertIsNone(tmux_helper._CODEX_MENU_OPTION_RE.match("❯"))

    @patch('tmux_helper.time.sleep', return_value=None)
    @patch('tmux_helper.recover_codex_interrupted', return_value=True)
    @patch('tmux_helper.get_agent_runtime_state')
    @patch('tmux_helper._agent_pane_target', return_value='%1')
    @patch('tmux_helper.session_exists', return_value=True)
    @patch('tmux_helper.subprocess.run')
    def test_stabilize_codex_session_clears_interrupted_before_ready(
        self,
        mock_run,
        _mock_exists,
        _mock_target,
        mock_runtime,
        mock_recover,
        _mock_sleep,
    ):
        mock_run.side_effect = [
            type('P', (), {'returncode': 0, 'stdout': '■ Conversation interrupted\n› Use /skills to list available skills\n'})(),
            type('P', (), {'returncode': 0, 'stdout': '╭─╮\n│ model: gpt-5.4 high │\n╰─╯\n›\n'})(),
            type('P', (), {'returncode': 0, 'stdout': '╭─╮\n│ model: gpt-5.4 high │\n╰─╯\n›\n'})(),
        ]
        mock_runtime.side_effect = [
            {'state': 'interrupted', 'reason': 'interrupted:Conversation interrupted'},
            {'state': 'idle', 'reason': 'ready'},
            {'state': 'idle', 'reason': 'ready'},
        ]

        ok = tmux_helper.stabilize_codex_session('main', timeout=5, stable_samples=2, poll_interval=0.1)
        self.assertTrue(ok)
        mock_recover.assert_called_once_with('main')

    @patch('tmux_helper.time.sleep', return_value=None)
    @patch('tmux_helper.stabilize_codex_session', return_value=True)
    @patch('tmux_helper._agent_pane_target', return_value='%1')
    def test_wait_for_agent_ready_codex_uses_stabilize_session(
        self,
        _mock_target,
        mock_stabilize,
        _mock_sleep,
    ):
        ok = tmux_helper.wait_for_agent_ready('main', 'codex', timeout=12)
        self.assertTrue(ok)
        mock_stabilize.assert_called_once()


if __name__ == "__main__":
    unittest.main()
