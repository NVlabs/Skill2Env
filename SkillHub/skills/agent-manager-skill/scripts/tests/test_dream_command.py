from __future__ import annotations

import argparse
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import main  # noqa: E402
from commands.dream import cmd_dream  # noqa: E402
from services.dream_state import save_dream_state  # noqa: E402


class DreamCommandTests(unittest.TestCase):
    def test_command_dispatch_unknown_subcommand(self):
        out = io.StringIO()
        with redirect_stdout(out):
            rc = cmd_dream(argparse.Namespace(dream_command='nope'), run_handler=lambda _args: 0)
        self.assertEqual(rc, 1)
        self.assertIn('Unknown dream command', out.getvalue())

    def test_main_dream_run_skips_stale_window(self):
        temp_root = Path(tempfile.mkdtemp(prefix='agent-manager-dream-'))
        work_dir = temp_root / 'workspace'
        work_dir.mkdir(parents=True, exist_ok=True)
        (work_dir / 'DREAM.md').write_text('dream here\n', encoding='utf-8')
        save_dream_state(temp_root, 'main', {
            'window_id': 'dream-window-HB-actual',
        })
        agent_config = {
            'name': 'main',
            'file_id': 'main',
            'working_directory': str(work_dir),
            'launcher': 'codex',
            'heartbeat': {'enabled': True, 'dream': {'enabled': True}},
            'enabled': True,
        }

        out = io.StringIO()
        with redirect_stdout(out), \
                patch('main.check_tmux', return_value=True), \
                patch('main.resolve_agent', return_value=agent_config), \
                patch('main.get_agent_id', return_value='main'), \
                patch('main.session_exists', return_value=True), \
                patch('main.get_repo_root', return_value=temp_root):
            rc = main.cmd_dream_run(
                argparse.Namespace(
                    agent='main',
                    window_id='dream-window-HB-old',
                    trigger_hb_id='HB-1',
                    timeout=None,
                )
            )

        self.assertEqual(rc, 0)
        self.assertIn('stale', out.getvalue())


if __name__ == '__main__':
    unittest.main()
