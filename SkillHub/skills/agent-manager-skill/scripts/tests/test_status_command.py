from __future__ import annotations
import argparse
import io
import json
import shutil
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


class StatusCommandTests(unittest.TestCase):
    def setUp(self):
        self.temp_root = Path(tempfile.mkdtemp(prefix='agent-manager-status-'))

    def tearDown(self):
        shutil.rmtree(self.temp_root, ignore_errors=True)

    def _run_status(self, agent='dev'):
        output = io.StringIO()
        with redirect_stdout(output):
            code = main.cmd_status(argparse.Namespace(agent=agent))
        return code, output.getvalue()

    def test_status_running_uses_recent_audit_event(self):
        agent_config = {'name': 'dev', 'file_id': 'EMP_0001', 'enabled': True, 'launcher': 'codex'}
        audit_file = self.temp_root / '.claude' / 'state' / 'agent-manager' / 'heartbeat-audit' / 'emp-0001.jsonl'
        dream_audit = self.temp_root / '.claude' / 'state' / 'agent-manager' / 'dream-audit' / 'emp-0001.jsonl'
        dream_state = self.temp_root / '.claude' / 'state' / 'agent-manager' / 'dream-state' / 'emp-0001.json'
        audit_file.parent.mkdir(parents=True, exist_ok=True)
        dream_audit.parent.mkdir(parents=True, exist_ok=True)
        dream_state.parent.mkdir(parents=True, exist_ok=True)
        with audit_file.open('w', encoding='utf-8') as f:
            f.write('not-json\n')
            f.write(json.dumps({'hb_id': 'HB-1', 'timestamp': '2026-02-09T09:00:00Z', 'send_status': 'ok', 'ack_status': 'ack'}) + '\n')
            f.write(json.dumps({'hb_id': 'HB-2', 'timestamp': '2026-02-09T09:10:00Z', 'send_status': 'ok', 'ack_status': 'timeout'}) + '\n')
        with dream_audit.open('w', encoding='utf-8') as f:
            f.write(json.dumps({'event': 'run_completed', 'dream_id': 'DREAM-1'}) + '\n')
        dream_state.write_text(json.dumps({'window_id': 'dream-window-HB-2', 'triggered_for_window': True}), encoding='utf-8')

        with patch('main.check_tmux', return_value=True), \
                patch('main.resolve_agent', return_value=agent_config), \
                patch('main.session_exists', return_value=True), \
                patch('main.get_session_info', return_value={'session': 'agent-emp-0001'}), \
                patch('main.resolve_launcher_command', return_value='codex'), \
                patch('main.get_agent_runtime_state', return_value={'state': 'busy', 'elapsed_seconds': 14}), \
                patch('main.get_repo_root', return_value=self.temp_root), \
                patch('main.capture_output', return_value=''):
            code, text = self._run_status('dev')

        self.assertEqual(code, 0)
        self.assertIn('Running: yes', text)
        self.assertIn('Runtime state: busy', text)
        self.assertIn('Runtime elapsed: 14s', text)
        self.assertIn('Recent heartbeat: HB-2 (2026-02-09T09:10:00Z)', text)
        self.assertIn('Heartbeat detail: send=ok ack=timeout', text)
        self.assertIn('Recent dream: run_completed (DREAM-1)', text)
        self.assertIn('Dream window: dream-window-HB-2 (triggered)', text)

    def test_status_running_falls_back_to_tmux_output_hb_id(self):
        agent_config = {'name': 'qa', 'file_id': 'EMP_0002', 'enabled': True, 'launcher': 'codex'}

        with patch('main.check_tmux', return_value=True), \
                patch('main.resolve_agent', return_value=agent_config), \
                patch('main.session_exists', return_value=True), \
                patch('main.get_session_info', return_value={'session': 'agent-emp-0002'}), \
                patch('main.resolve_launcher_command', return_value='codex'), \
                patch('main.get_agent_runtime_state', return_value={'state': 'idle'}), \
                patch('main.get_repo_root', return_value=self.temp_root), \
                patch('main.capture_output', return_value='... [HB_ID:HB-FROM-TAIL] ...'):
            code, text = self._run_status('qa')

        self.assertEqual(code, 0)
        self.assertIn('Runtime state: idle', text)
        self.assertIn('Recent heartbeat: HB-FROM-TAIL (from tmux output)', text)

    def test_status_stopped_agent(self):
        agent_config = {'name': 'ops', 'file_id': 'EMP_0003', 'enabled': False, 'launcher': 'codex'}

        with patch('main.check_tmux', return_value=True), \
                patch('main.resolve_agent', return_value=agent_config), \
                patch('main.session_exists', return_value=False), \
                patch('main.resolve_launcher_command', return_value='codex'), \
                patch('main.get_repo_root', return_value=self.temp_root):
            code, text = self._run_status('ops')

        self.assertEqual(code, 0)
        self.assertIn('Enabled: no', text)
        self.assertIn('Running: no', text)
        self.assertIn('Runtime state: stopped', text)
        self.assertIn('Recent heartbeat: none', text)


    def test_status_main_agent_uses_main_session_label(self):
        agent_config = {'name': 'main', 'file_id': 'main', 'enabled': True, 'launcher': 'codex'}

        with patch('main.check_tmux', return_value=True), \
                patch('main.resolve_agent', return_value=agent_config), \
                patch('main.session_exists', return_value=True), \
                patch('main.get_session_info', return_value=None), \
                patch('main.resolve_launcher_command', return_value='codex'), \
                patch('main.get_agent_runtime_state', return_value={'state': 'idle'}), \
                patch('main.get_repo_root', return_value=self.temp_root), \
                patch('main.capture_output', return_value=''):
            code, text = self._run_status('main')

        self.assertEqual(code, 0)
        self.assertIn('Session: main(main)', text)
        self.assertNotIn('agent-main', text)


if __name__ == '__main__':
    unittest.main()
