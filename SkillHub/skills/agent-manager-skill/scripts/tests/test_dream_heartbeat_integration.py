from __future__ import annotations

import argparse
import io
import json
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


class DreamHeartbeatIntegrationTests(unittest.TestCase):
    def test_heartbeat_schedules_dream_when_interval_exceeds_idle_after(self):
        temp_root = Path(tempfile.mkdtemp(prefix='agent-manager-dream-heartbeat-'))
        work_dir = temp_root / 'workspace'
        work_dir.mkdir(parents=True, exist_ok=True)
        (work_dir / 'DREAM.md').write_text('follow dream\n', encoding='utf-8')
        agent_config = {
            'name': 'main',
            'file_id': 'main',
            'working_directory': str(work_dir),
            'launcher': 'codex',
            'heartbeat': {
                'enabled': True,
                'cron': '0 */4 * * *',
                'max_runtime': '8m',
                'session_mode': 'auto',
                'dream': {
                    'enabled': True,
                    'idle_after': '1h',
                    'max_runtime': '15m',
                },
            },
            'enabled': True,
        }

        out = io.StringIO()
        with redirect_stdout(out), \
                patch('main.check_tmux', return_value=True), \
                patch('main.resolve_agent', return_value=agent_config), \
                patch('main.get_agent_id', return_value='main'), \
                patch('main.session_exists', return_value=True), \
                patch('main.resolve_launcher_command', return_value='codex'), \
                patch('main.get_repo_root', return_value=temp_root), \
                patch('main._detect_agent_context_left_percent', return_value=None), \
                patch('main._maybe_rollover_heartbeat_session', return_value=None), \
                patch('main._maybe_run_main_inbound_heartbeat_sweep', return_value=False), \
                patch('main.has_pending_inbound_messages', return_value=False), \
                patch('main._heartbeat_preflight_runtime_state', return_value=('idle', 'ready')), \
                patch('main._run_heartbeat_attempt', return_value={
                    'send_status': 'ok',
                    'ack_status': 'ack',
                    'ack_evidence': 'direct_heartbeat_ok',
                    'failure_type': '',
                    'reason_code': 'HB_ACK_OK',
                    'duration_ms': 1000,
                }), \
                patch('main.cmd_timer', return_value=0) as mock_cmd_timer:
            rc = main.cmd_heartbeat_run(
                argparse.Namespace(
                    agent='main',
                    timeout=None,
                    retry=None,
                    backoff_seconds=None,
                    fallback_mode=None,
                    notify_on_failure=False,
                    notifier_channel=None,
                )
            )

        self.assertEqual(rc, 0)
        mock_cmd_timer.assert_called_once()
        timer_args = mock_cmd_timer.call_args.args[0]
        self.assertEqual(timer_args.timer_command, 'command')
        self.assertIn('dream', timer_args.command_args)
        state_file = temp_root / '.claude' / 'state' / 'agent-manager' / 'dream-state' / 'main.json'
        payload = json.loads(state_file.read_text(encoding='utf-8'))
        self.assertTrue(payload['triggered_for_window'])

    def test_fixed_dream_window_replaces_heartbeat_dispatch(self):
        temp_root = Path(tempfile.mkdtemp(prefix='agent-manager-fixed-dream-heartbeat-'))
        work_dir = temp_root / 'workspace'
        work_dir.mkdir(parents=True, exist_ok=True)
        (work_dir / 'DREAM.md').write_text('follow dream\n', encoding='utf-8')
        agent_config = {
            'name': 'main',
            'file_id': 'main',
            'working_directory': str(work_dir),
            'launcher': 'codex',
            'heartbeat': {
                'enabled': True,
                'cron': '*/10 * * * *',
                'max_runtime': '8m',
                'session_mode': 'auto',
                'schedule': {
                    'timezone': 'Asia/Shanghai',
                    'work_days': [1],
                    'work_hours': {'start': '09:00', 'end': '10:00'},
                },
                'dream': {
                    'enabled': True,
                    'idle_after': '1h',
                    'max_runtime': '30m',
                    'fixed_windows': [
                        {'timezone': 'Asia/Shanghai', 'start': '23:00', 'end': '08:00'},
                    ],
                },
            },
            'enabled': True,
        }

        out = io.StringIO()
        with redirect_stdout(out), \
                patch('main.check_tmux', return_value=True), \
                patch('main.resolve_agent', return_value=agent_config), \
                patch('main.get_agent_id', return_value='main'), \
                patch('main.session_exists', return_value=True), \
                patch('main.resolve_launcher_command', return_value='codex'), \
                patch('main.get_repo_root', return_value=temp_root), \
                patch('main._detect_agent_context_left_percent', return_value=None), \
                patch('main._maybe_rollover_heartbeat_session', return_value=None), \
                patch('main._maybe_run_main_inbound_heartbeat_sweep', return_value=False), \
                patch('main.has_pending_inbound_messages', return_value=False), \
                patch('main._heartbeat_preflight_runtime_state', return_value=('idle', 'ready')), \
                patch('main.resolve_active_dream_window', return_value={
                    'active': True,
                    'window_id': 'fixed-window-1',
                    'summary': 'Asia/Shanghai 23:00-08:00 Mon-Sun',
                }), \
                patch('main._run_heartbeat_attempt') as mock_heartbeat_attempt, \
                patch('main._run_dream_attempt', return_value={
                    'send_status': 'ok',
                    'ack_status': 'ack',
                    'ack_evidence': 'direct_dream_ok',
                    'completion_evidence': 'direct_dream_ok:tail_sha1=abc123',
                    'failure_type': '',
                    'reason_code': 'DREAM_ACK_OK',
                    'duration_ms': 1000,
                }) as mock_dream_attempt, \
                patch('main.cmd_timer') as mock_cmd_timer:
            rc = main.cmd_heartbeat_run(
                argparse.Namespace(
                    agent='main',
                    timeout=None,
                    retry=None,
                    backoff_seconds=None,
                    fallback_mode=None,
                    notify_on_failure=False,
                    notifier_channel=None,
                )
            )

        self.assertEqual(rc, 0)
        mock_heartbeat_attempt.assert_not_called()
        mock_cmd_timer.assert_not_called()
        mock_dream_attempt.assert_called_once()
        self.assertEqual(mock_dream_attempt.call_args.kwargs['timeout_seconds'], 30 * 60)
        sent_message = mock_dream_attempt.call_args.kwargs['dream_message']
        self.assertIn('Read DREAM.md', sent_message)
        self.assertIn('[TRIGGER_HB_ID:', sent_message)
        self.assertIn('Heartbeat completed via fixed Dream window', out.getvalue())
        audit_file = temp_root / '.claude' / 'state' / 'agent-manager' / 'dream-audit' / 'main.jsonl'
        audit_events = [
            json.loads(line)
            for line in audit_file.read_text(encoding='utf-8').splitlines()
        ]
        completed = [event for event in audit_events if event.get('event') == 'run_completed']
        self.assertEqual(len(completed), 1)
        self.assertIn('completion=direct_dream_ok:tail_sha1=abc123', completed[0]['detail'])

    def test_direct_dream_ack_ignores_prompt_echo(self):
        dream_id = 'DREAM-123'
        prompt_echo = (
            "› Read DREAM.md if it exists. "
            "If nothing worth doing emerges, reply DREAM_OK. "
            f"[DREAM_ID:{dream_id}]"
        )
        final_reply = f"• DREAM_OK [DREAM_ID:{dream_id}]"

        self.assertFalse(main._has_direct_dream_ack(prompt_echo, dream_id))
        self.assertTrue(main._has_direct_dream_ack(final_reply, dream_id))

    def test_dream_attempt_hashes_tail_and_detects_direct_ack(self):
        temp_root = Path(tempfile.mkdtemp(prefix='agent-manager-dream-attempt-'))
        dream_id = 'DREAM-123'

        with patch('main.capture_output', side_effect=[
            'baseline output',
            f'baseline output\n• DREAM_OK [DREAM_ID:{dream_id}]',
        ]), \
                patch('main.send_keys', return_value=True) as mock_send_keys, \
                patch('main.has_pending_inbound_messages', return_value=False), \
                patch('main.get_agent_runtime_state', return_value={'state': 'idle'}), \
                patch('main.time.sleep', return_value=None):
            result = main._run_dream_attempt(
                repo_root=temp_root,
                agent_id='main',
                agent_name='main',
                launcher='codex',
                dream_message='Read DREAM.md',
                timeout_seconds=5,
                is_codex=True,
                dream_id=dream_id,
            )

        self.assertEqual(result['send_status'], 'ok')
        self.assertEqual(result['ack_status'], 'ack')
        self.assertEqual(result['ack_evidence'], 'direct_dream_ok')
        self.assertTrue(result['completion_evidence'].startswith('direct_dream_ok:tail_sha1='))
        mock_send_keys.assert_called_once()


if __name__ == '__main__':
    unittest.main()
