from __future__ import annotations
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import tmux_helper  # noqa: E402


class SendKeysTests(unittest.TestCase):
    @patch('tmux_helper._agent_pane_target', return_value='%1')
    @patch('tmux_helper.session_exists', return_value=True)
    @patch('tmux_helper.time.sleep', return_value=None)
    @patch('tmux_helper.subprocess.run')
    def test_enter_via_key_uses_native_enter_first(self, mock_run, _mock_sleep, _mock_session_exists, _mock_target):
        commands = []
        capture_index = {'count': 0}

        def fake_run(args, *pargs, **kwargs):
            commands.append(args)
            if args[:5] == ['tmux', 'capture-pane', '-p', '-t', '%1']:
                capture_index['count'] += 1
                stdout = 'before\n' if capture_index['count'] == 1 else 'after\n'
                return subprocess.CompletedProcess(args=args, returncode=0, stdout=stdout)
            return subprocess.CompletedProcess(args=args, returncode=0, stdout='')

        mock_run.side_effect = fake_run

        ok = tmux_helper.send_keys(
            'emp-0001',
            'hello from test',
            send_enter=True,
            enter_via_key=True,
        )

        self.assertTrue(ok)
        self.assertTrue(any(cmd[:4] == ['tmux', 'send-keys', '-t', '%1'] and cmd[-1] == 'C-m' for cmd in commands))
        self.assertFalse(any(cmd[:4] == ['tmux', 'load-buffer', '-b', 'enter-key'] for cmd in commands))

    @patch('tmux_helper._agent_pane_target', return_value='%1')
    @patch('tmux_helper.session_exists', return_value=True)
    @patch('tmux_helper.time.sleep', return_value=None)
    @patch('tmux_helper.subprocess.run')
    def test_enter_via_key_returns_false_when_native_and_fallback_do_not_change_pane(
        self,
        mock_run,
        _mock_sleep,
        _mock_session_exists,
        _mock_target,
    ):
        commands = []

        def fake_run(args, *pargs, **kwargs):
            commands.append(args)
            if args[:5] == ['tmux', 'capture-pane', '-p', '-t', '%1']:
                return subprocess.CompletedProcess(args=args, returncode=0, stdout='unchanged\n')
            return subprocess.CompletedProcess(args=args, returncode=0, stdout='')

        mock_run.side_effect = fake_run

        ok = tmux_helper.send_keys(
            'emp-0001',
            'hello from test',
            send_enter=True,
            enter_via_key=True,
        )

        self.assertFalse(ok)
        self.assertTrue(any(cmd[:4] == ['tmux', 'send-keys', '-t', '%1'] and cmd[-1] == 'C-m' for cmd in commands))
        self.assertTrue(any(cmd[:4] == ['tmux', 'load-buffer', '-b', 'enter-key'] for cmd in commands))
        self.assertTrue(any(cmd[:5] == ['tmux', 'paste-buffer', '-d', '-b', 'enter-key'] for cmd in commands))

    @patch('tmux_helper._agent_pane_target', return_value='%1')
    @patch('tmux_helper.session_exists', return_value=True)
    @patch('tmux_helper.time.sleep', return_value=None)
    @patch('tmux_helper.subprocess.run')
    def test_enter_via_key_fallback_succeeds_when_pane_changes_after_newline(
        self,
        mock_run,
        _mock_sleep,
        _mock_session_exists,
        _mock_target,
    ):
        commands = []
        capture_outputs = iter([
            'unchanged\n',  # native before
            'unchanged\n',  # native probe-1
            'unchanged\n',  # native probe-2
            'unchanged\n',  # native probe-3
            'unchanged\n',  # fallback before
            'changed\n',    # fallback probe-1
        ])

        def fake_run(args, *pargs, **kwargs):
            commands.append(args)
            if args[:5] == ['tmux', 'capture-pane', '-p', '-t', '%1']:
                return subprocess.CompletedProcess(args=args, returncode=0, stdout=next(capture_outputs))
            return subprocess.CompletedProcess(args=args, returncode=0, stdout='')

        mock_run.side_effect = fake_run

        ok = tmux_helper.send_keys(
            'emp-0001',
            'hello from test',
            send_enter=True,
            enter_via_key=True,
        )

        self.assertTrue(ok)
        self.assertTrue(any(cmd[:4] == ['tmux', 'load-buffer', '-b', 'enter-key'] for cmd in commands))
        self.assertTrue(any(cmd[:5] == ['tmux', 'paste-buffer', '-d', '-b', 'enter-key'] for cmd in commands))


if __name__ == '__main__':
    unittest.main()
