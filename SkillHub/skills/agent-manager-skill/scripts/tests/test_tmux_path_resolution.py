from __future__ import annotations
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import tmux_helper  # noqa: E402


class TmuxPathResolutionTests(unittest.TestCase):
    @patch("tmux_helper.shutil.which", return_value="/usr/bin/tmux")
    def test_ensure_tmux_in_path_when_already_resolvable(self, _mock_which):
        original_path = os.environ.get("PATH", "")
        with patch.dict(os.environ, {"PATH": original_path}, clear=False):
            self.assertTrue(tmux_helper._ensure_tmux_in_path())
            self.assertEqual(os.environ.get("PATH", ""), original_path)

    @patch("tmux_helper.os.access", return_value=True)
    @patch("tmux_helper.os.path.isfile", side_effect=lambda p: p == "/opt/homebrew/bin/tmux")
    @patch("tmux_helper.shutil.which", return_value=None)
    def test_ensure_tmux_in_path_adds_homebrew_path_when_missing(self, _mock_which, _mock_isfile, _mock_access):
        with patch.dict(os.environ, {"PATH": "/usr/bin:/bin"}, clear=False):
            self.assertTrue(tmux_helper._ensure_tmux_in_path())
            self.assertTrue(os.environ.get("PATH", "").startswith("/opt/homebrew/bin:"))

    @patch("tmux_helper.os.access", return_value=False)
    @patch("tmux_helper.os.path.isfile", return_value=False)
    @patch("tmux_helper.shutil.which", return_value=None)
    def test_ensure_tmux_in_path_returns_false_when_no_candidate(self, _mock_which, _mock_isfile, _mock_access):
        with patch.dict(os.environ, {"PATH": "/usr/bin:/bin"}, clear=False):
            self.assertFalse(tmux_helper._ensure_tmux_in_path())


if __name__ == "__main__":
    unittest.main()
