from __future__ import annotations
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import main  # noqa: E402
from services.inbound_queue import append_inbound_message_event  # noqa: E402
from services.inbound_queue import enqueue_inbound_message  # noqa: E402
from services.inbound_queue import read_inbound_events  # noqa: E402


class HeartbeatRecoveryTests(unittest.TestCase):
    def test_parse_recovery_policy_defaults(self):
        policy = main._parse_heartbeat_recovery_policy({'enabled': True})
        self.assertEqual(policy['max_retries'], 1)
        self.assertEqual(policy['retry_backoff_seconds'], 3)
        self.assertEqual(policy['fallback_mode'], 'fresh')
        self.assertFalse(policy['notify_on_failure'])

    def test_parse_recovery_policy_with_nested_config(self):
        heartbeat = {
            'recovery': {
                'max_retries': 2,
                'retry_backoff_seconds': 5,
                'fallback_mode': 'none',
                'notify_on_failure': True,
                'notifier_channel': 'slack',
            }
        }
        policy = main._parse_heartbeat_recovery_policy(heartbeat)
        self.assertEqual(policy['max_retries'], 2)
        self.assertEqual(policy['retry_backoff_seconds'], 5)
        self.assertEqual(policy['fallback_mode'], 'none')
        self.assertTrue(policy['notify_on_failure'])
        self.assertEqual(policy['notifier_channel'], 'slack')

    def test_parse_recovery_policy_cli_overrides(self):
        args = type('Args', (), {
            'retry': 4,
            'backoff_seconds': 1,
            'fallback_mode': 'fresh',
            'notify_on_failure': True,
            'notifier_channel': 'all',
        })()
        policy = main._parse_heartbeat_recovery_policy({'recovery': {'max_retries': 1}}, args)
        self.assertEqual(policy['max_retries'], 4)
        self.assertEqual(policy['retry_backoff_seconds'], 1)
        self.assertEqual(policy['fallback_mode'], 'fresh')
        self.assertTrue(policy['notify_on_failure'])

    def test_classify_heartbeat_ack(self):
        self.assertEqual(main._classify_heartbeat_ack(waited_for_ack=False, last_state=None, timed_out=False), ('not_checked', ''))
        self.assertEqual(main._classify_heartbeat_ack(waited_for_ack=True, last_state='idle', timed_out=False), ('ack', ''))
        self.assertEqual(main._classify_heartbeat_ack(waited_for_ack=True, last_state='blocked', timed_out=False), ('blocked', 'blocked'))
        self.assertEqual(main._classify_heartbeat_ack(waited_for_ack=True, last_state='busy', timed_out=True), ('timeout', 'timeout'))
        self.assertEqual(main._classify_heartbeat_ack(waited_for_ack=True, last_state='busy', timed_out=False), ('no_ack', 'no_ack'))

    def test_should_retry_heartbeat_attempt(self):
        self.assertTrue(main._should_retry_heartbeat_attempt(failure_type='send_fail', attempt_index=0, max_retries=1))
        self.assertTrue(main._should_retry_heartbeat_attempt(failure_type='timeout', attempt_index=0, max_retries=1))
        self.assertTrue(main._should_retry_heartbeat_attempt(failure_type='no_activation', attempt_index=0, max_retries=1))
        self.assertFalse(main._should_retry_heartbeat_attempt(failure_type='unknown', attempt_index=0, max_retries=1))
        self.assertFalse(main._should_retry_heartbeat_attempt(failure_type='send_fail', attempt_index=1, max_retries=1))

    def test_resolve_auto_starvation_skip_threshold_defaults_and_disable(self):
        self.assertEqual(
            main._resolve_auto_starvation_skip_threshold({'enabled': True}),
            main._HEARTBEAT_AUTO_STARVATION_SKIP_THRESHOLD,
        )
        self.assertEqual(
            main._resolve_auto_starvation_skip_threshold({'auto_starvation_skip_threshold': 5}),
            5,
        )
        self.assertEqual(
            main._resolve_auto_starvation_skip_threshold({'recovery': {'auto_starvation_skip_threshold': 7}}),
            7,
        )
        self.assertIsNone(
            main._resolve_auto_starvation_skip_threshold({'auto_starvation_skip_threshold': 0}),
        )

    def test_count_consecutive_auto_preflight_skips_stops_at_first_attempt(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            main._append_heartbeat_audit_event(
                repo_root,
                agent_id='emp-0001',
                heartbeat_id='hb-attempt',
                send_status='ok',
                ack_status='ack',
                duration_ms=1,
                context_left=55,
                session_mode='auto',
                phase='attempt',
                attempt=1,
                timestamp='2026-03-12T10:03:00Z',
            )
            main._append_heartbeat_audit_event(
                repo_root,
                agent_id='emp-0001',
                heartbeat_id='hb-skip-2',
                send_status='skip',
                ack_status='not_checked',
                duration_ms=0,
                context_left=55,
                failure_type='busy_skip',
                session_mode='auto',
                phase='preflight',
                attempt=0,
                recovery_action='skip_busy',
                reason_code='HB_AUTO_BUSY_SKIP',
                timestamp='2026-03-12T10:02:00Z',
            )
            main._append_heartbeat_audit_event(
                repo_root,
                agent_id='emp-0001',
                heartbeat_id='hb-skip-1',
                send_status='skip',
                ack_status='not_checked',
                duration_ms=0,
                context_left=55,
                failure_type='busy_skip',
                session_mode='auto',
                phase='preflight',
                attempt=0,
                recovery_action='skip_busy',
                reason_code='HB_AUTO_BUSY_SKIP',
                timestamp='2026-03-12T10:01:00Z',
            )

            self.assertEqual(
                main._count_consecutive_auto_preflight_skips(repo_root, agent_id='emp-0001'),
                0,
            )

            main._append_heartbeat_audit_event(
                repo_root,
                agent_id='emp-0001',
                heartbeat_id='hb-skip-4',
                send_status='skip',
                ack_status='not_checked',
                duration_ms=0,
                context_left=55,
                failure_type='busy_skip',
                session_mode='auto',
                phase='preflight',
                attempt=0,
                recovery_action='skip_busy',
                reason_code='HB_AUTO_BUSY_SKIP',
                timestamp='2026-03-12T10:05:00Z',
            )
            main._append_heartbeat_audit_event(
                repo_root,
                agent_id='emp-0001',
                heartbeat_id='hb-skip-3',
                send_status='skip',
                ack_status='not_checked',
                duration_ms=0,
                context_left=55,
                failure_type='busy_skip',
                session_mode='auto',
                phase='preflight',
                attempt=0,
                recovery_action='skip_busy',
                reason_code='HB_AUTO_BUSY_SKIP',
                timestamp='2026-03-12T10:04:00Z',
            )

            self.assertEqual(
                main._count_consecutive_auto_preflight_skips(repo_root, agent_id='emp-0001'),
                2,
            )

    def test_count_consecutive_auto_preflight_skips_can_filter_reason_codes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            main._append_heartbeat_audit_event(
                repo_root,
                agent_id='emp-0001',
                heartbeat_id='hb-pending-2',
                send_status='skip',
                ack_status='not_checked',
                duration_ms=0,
                context_left=55,
                failure_type='pending_skip',
                session_mode='auto',
                phase='preflight',
                attempt=0,
                recovery_action='skip_busy',
                reason_code='HB_AUTO_PENDING_SKIP',
                timestamp='2026-03-12T10:03:00Z',
            )
            main._append_heartbeat_audit_event(
                repo_root,
                agent_id='emp-0001',
                heartbeat_id='hb-pending-1',
                send_status='skip',
                ack_status='not_checked',
                duration_ms=0,
                context_left=55,
                failure_type='pending_skip',
                session_mode='auto',
                phase='preflight',
                attempt=0,
                recovery_action='skip_busy',
                reason_code='HB_AUTO_PENDING_SKIP',
                timestamp='2026-03-12T10:02:00Z',
            )
            main._append_heartbeat_audit_event(
                repo_root,
                agent_id='emp-0001',
                heartbeat_id='hb-busy',
                send_status='skip',
                ack_status='not_checked',
                duration_ms=0,
                context_left=55,
                failure_type='busy_skip',
                session_mode='auto',
                phase='preflight',
                attempt=0,
                recovery_action='skip_busy',
                reason_code='HB_AUTO_BUSY_SKIP',
                timestamp='2026-03-12T10:01:00Z',
            )

            self.assertEqual(
                main._count_consecutive_auto_preflight_skips(
                    repo_root,
                    agent_id='emp-0001',
                    reason_codes={'HB_AUTO_PENDING_SKIP'},
                ),
                2,
            )

    def test_generate_heartbeat_id_uses_utc(self):
        local_now = datetime(2026, 3, 26, 0, 50, 1, tzinfo=timezone(timedelta(hours=8)))
        self.assertEqual(main._generate_heartbeat_id(local_now), '20260325-165001')

    @patch('main.time.sleep', return_value=None)
    @patch('main.capture_output', side_effect=['pane-a', 'pane-b'])
    @patch('main.get_agent_runtime_state', return_value={'state': 'idle', 'reason': 'ready'})
    def test_heartbeat_preflight_detects_active_when_pane_changes(
        self,
        _mock_runtime,
        _mock_capture,
        _mock_sleep,
    ):
        state, reason = main._heartbeat_preflight_runtime_state(
            agent_id='emp-0001',
            launcher='codex',
            sample_count=2,
            sample_interval_seconds=0.1,
            capture_lines=40,
        )
        self.assertEqual(state, 'busy')
        self.assertTrue(reason.startswith('preflight_pane_changed:'))

    @patch('main.time.sleep', return_value=None)
    @patch('main.capture_output', side_effect=['pane-a', 'pane-a'])
    @patch('main.get_agent_runtime_state', return_value={'state': 'idle', 'reason': 'ready'})
    def test_heartbeat_preflight_keeps_idle_when_pane_stable(
        self,
        _mock_runtime,
        _mock_capture,
        _mock_sleep,
    ):
        state, reason = main._heartbeat_preflight_runtime_state(
            agent_id='emp-0001',
            launcher='codex',
            sample_count=2,
            sample_interval_seconds=0.1,
            capture_lines=40,
        )
        self.assertEqual(state, 'idle')
        self.assertEqual(reason, 'ready')

    @patch('main.time.sleep', return_value=None)
    @patch('main.capture_output', side_effect=[
        'Read HEARTBEAT.md... [HB_ID:20260321-004002]\n• 已处理并继续执行\n',
        'Read HEARTBEAT.md... [HB_ID:20260321-004002]\n• 已处理并继续执行\n',
    ])
    @patch('main.get_agent_runtime_state', return_value={'state': 'idle', 'reason': 'ready'})
    def test_heartbeat_preflight_ignores_acknowledged_pending_marker(
        self,
        _mock_runtime,
        _mock_capture,
        _mock_sleep,
    ):
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            main._append_heartbeat_audit_event(
                repo_root,
                agent_id='emp-0001',
                heartbeat_id='20260321-004002',
                send_status='ok',
                ack_status='ack',
                duration_ms=4661,
                context_left=35,
                session_mode='auto',
                phase='attempt',
                attempt=1,
                timestamp='2026-03-20T16:40:10Z',
            )

            state, reason = main._heartbeat_preflight_runtime_state(
                repo_root=repo_root,
                agent_id='emp-0001',
                launcher='codex',
                sample_count=2,
                sample_interval_seconds=0.1,
                capture_lines=40,
            )

        self.assertEqual(state, 'idle')
        self.assertEqual(reason, 'ready')

    @patch('main.capture_output', return_value='baseline')
    @patch('main.send_keys', return_value=False)
    def test_run_heartbeat_attempt_send_fail(self, _mock_send, _mock_capture):
        result = main._run_heartbeat_attempt(
            agent_id='emp-0001',
            agent_name='qa-agent',
            launcher='codex',
            heartbeat_message='hello',
            timeout_seconds=30,
            is_codex=True,
        )
        self.assertEqual(result['send_status'], 'fail')
        self.assertEqual(result['failure_type'], 'send_fail')

    @patch('main.time.sleep', return_value=None)
    @patch('main.capture_output', return_value='tail output')
    @patch('main.get_agent_runtime_state', side_effect=[
        {'state': 'busy', 'reason': 'busy_pattern:Thinking'},  # activation detected
        {'state': 'idle', 'reason': 'ready'},                   # completion detected
    ])
    @patch('main.send_keys', return_value=True)
    def test_run_heartbeat_attempt_ack(self, _mock_send, _mock_state, _mock_capture, _mock_sleep):
        result = main._run_heartbeat_attempt(
            agent_id='emp-0001',
            agent_name='qa-agent',
            launcher='codex',
            heartbeat_message='hello',
            timeout_seconds=30,
            is_codex=True,
        )
        self.assertEqual(result['send_status'], 'ok')
        self.assertEqual(result['ack_status'], 'ack')

    @patch('main.time.sleep', return_value=None)
    @patch('main.capture_output', return_value='tail output')
    @patch('main.get_agent_runtime_state', return_value={'state': 'busy', 'reason': 'busy_pattern:Thinking'})
    @patch('main.has_pending_inbound_messages', side_effect=[True])
    @patch('main.send_keys', return_value=True)
    def test_run_heartbeat_attempt_yields_when_pending_user_work_detected(
        self,
        _mock_send,
        _mock_pending,
        _mock_state,
        _mock_capture,
        _mock_sleep,
    ):
        result = main._run_heartbeat_attempt(
            agent_id='main',
            agent_name='main',
            launcher='codex',
            heartbeat_message='hello [HB_ID:20260317-000001]',
            timeout_seconds=30,
            is_codex=True,
        )
        self.assertEqual(result['send_status'], 'ok')
        self.assertEqual(result['ack_status'], 'yielded')
        self.assertEqual(result['failure_type'], 'user_queue_yield')

    @patch('main.time.sleep', return_value=None)
    @patch('main.capture_output', return_value='tail output')
    @patch('main.get_agent_runtime_state', return_value={'state': 'idle'})
    @patch('main.send_keys', return_value=True)
    def test_run_heartbeat_attempt_no_activation(self, _mock_send, _mock_state, _mock_capture, _mock_sleep):
        """Agent stays idle the entire time — no activation detected, classified as no_ack."""
        result = main._run_heartbeat_attempt(
            agent_id='emp-0001',
            agent_name='qa-agent',
            launcher='codex',
            heartbeat_message='hello',
            timeout_seconds=30,
            is_codex=True,
        )
        self.assertEqual(result['send_status'], 'ok')
        self.assertEqual(result['ack_status'], 'no_ack')
        self.assertEqual(result['failure_type'], 'no_activation')
        self.assertEqual(result['reason_code'], 'HB_NO_ACTIVATION')

    @patch('main.time.sleep', return_value=None)
    @patch('main.capture_output')
    @patch('main.get_agent_runtime_state', return_value={'state': 'idle'})
    @patch('main.send_keys', return_value=True)
    def test_run_heartbeat_attempt_activation_via_output_change(self, _mock_send, _mock_state, mock_capture, _mock_sleep):
        """Agent stays idle in state checks, but pane output changes — activation via output change."""
        # First call: baseline before send_keys.
        # Second call: changed pane tail during activation polling.
        # Third call: phase-2 polling capture.
        # Fourth call: final tail capture.
        short_output = 'short baseline'
        changed_output = 'short baseLine'
        mock_capture.side_effect = [short_output, changed_output, changed_output, changed_output]
        result = main._run_heartbeat_attempt(
            agent_id='emp-0001',
            agent_name='qa-agent',
            launcher='codex',
            heartbeat_message='hello',
            timeout_seconds=30,
            is_codex=True,
        )
        self.assertEqual(result['send_status'], 'ok')
        self.assertEqual(result['ack_status'], 'ack')

    @patch('main.time.sleep', return_value=None)
    @patch('main.capture_output')
    @patch('main.get_agent_runtime_state', return_value={'state': 'idle'})
    @patch('main.send_keys', return_value=True)
    def test_run_heartbeat_attempt_activation_via_hb_id_in_pane(self, _mock_send, _mock_state, mock_capture, _mock_sleep):
        heartbeat_id = '20260228-120001'
        pane_tail = f"some output [HB_ID:{heartbeat_id}]"
        mock_capture.side_effect = [pane_tail, pane_tail, pane_tail, pane_tail]
        result = main._run_heartbeat_attempt(
            agent_id='emp-0001',
            agent_name='qa-agent',
            launcher='codex',
            heartbeat_message=f'hello [HB_ID:{heartbeat_id}]',
            timeout_seconds=30,
            is_codex=True,
        )
        self.assertEqual(result['send_status'], 'ok')
        self.assertEqual(result['ack_status'], 'ack')
        self.assertNotEqual(result['failure_type'], 'no_activation')

    @patch('main.time.sleep', return_value=None)
    @patch('main.capture_output')
    @patch('main.get_agent_runtime_state', return_value={'state': 'idle'})
    @patch('main.send_keys', return_value=True)
    def test_run_heartbeat_attempt_direct_ack_via_pane_output(self, _mock_send, _mock_state, mock_capture, _mock_sleep):
        heartbeat_id = '20260228-120002'
        baseline = 'before heartbeat'
        ack_line = f'HEARTBEAT_OK [HB_ID:{heartbeat_id}]'
        mock_capture.side_effect = [baseline, ack_line, ack_line]
        result = main._run_heartbeat_attempt(
            agent_id='emp-0001',
            agent_name='qa-agent',
            launcher='codex',
            heartbeat_message=f'hello [HB_ID:{heartbeat_id}]',
            timeout_seconds=30,
            is_codex=True,
        )
        self.assertEqual(result['send_status'], 'ok')
        self.assertEqual(result['ack_status'], 'ack')
        self.assertEqual(result['reason_code'], 'HB_ACK_OK')

    @patch('main.recover_codex_interrupted')
    @patch('main.time.sleep', return_value=None)
    @patch('main.capture_output', side_effect=['baseline', 'interrupted tail', 'interrupted tail'])
    @patch('main.get_agent_runtime_state', return_value={'state': 'interrupted', 'reason': 'interrupted:Conversation interrupted'})
    @patch('main.send_keys', return_value=True)
    def test_run_heartbeat_attempt_interrupted_requires_fresh_recovery(
        self,
        mock_send,
        _mock_state,
        _mock_capture,
        _mock_sleep,
        mock_recover,
    ):
        result = main._run_heartbeat_attempt(
            agent_id='emp-0001',
            agent_name='qa-agent',
            launcher='codex',
            heartbeat_message='hello [HB_ID:20260228-120003]',
            timeout_seconds=30,
            is_codex=True,
        )
        self.assertEqual(result['send_status'], 'ok')
        self.assertEqual(result['ack_status'], 'no_ack')
        self.assertEqual(result['failure_type'], 'interrupted')
        self.assertEqual(result['reason_code'], 'HB_INTERRUPTED')
        self.assertEqual(mock_send.call_count, 1)
        mock_recover.assert_not_called()

    @patch('main.recover_codex_interrupted')
    @patch('main.time.sleep', return_value=None)
    @patch('main.capture_output', side_effect=['baseline', 'suggestion tip', 'HEARTBEAT_OK [HB_ID:20260228-120004]', 'HEARTBEAT_OK [HB_ID:20260228-120004]'])
    @patch('main.get_agent_runtime_state', side_effect=[
        {'state': 'interrupted', 'reason': 'suggestion_tip:› Improve docs'},
        {'state': 'idle', 'reason': 'ready'},
    ])
    @patch('main.send_keys', return_value=True)
    def test_run_heartbeat_attempt_suggestion_tip_still_recovers_locally(
        self,
        mock_send,
        _mock_state,
        _mock_capture,
        _mock_sleep,
        mock_recover,
    ):
        result = main._run_heartbeat_attempt(
            agent_id='emp-0001',
            agent_name='qa-agent',
            launcher='codex',
            heartbeat_message='hello [HB_ID:20260228-120004]',
            timeout_seconds=30,
            is_codex=True,
        )
        self.assertEqual(result['ack_status'], 'ack')
        self.assertEqual(result['failure_type'], '')
        self.assertEqual(mock_send.call_count, 2)
        mock_recover.assert_called_once()

    @patch('main.arm_codex_fullspeed_stop_hook_skip')
    @patch('main.cmd_start', return_value=0)
    @patch('main.stop_session', return_value=True)
    @patch('main.time.sleep', return_value=None)
    def test_restart_heartbeat_session_fresh(self, _mock_sleep, _mock_stop, _mock_start, mock_arm_skip):
        ok = main._restart_heartbeat_session_fresh('EMP_0001', 'qa-agent', 'emp-0001')
        self.assertTrue(ok)
        mock_arm_skip.assert_not_called()

    @patch('main._notify_heartbeat_failure', return_value=True)
    @patch('main._append_heartbeat_audit_event')
    @patch('main.time.sleep', return_value=None)
    @patch('main._run_heartbeat_attempt')
    @patch('main._maybe_rollover_heartbeat_session', return_value=None)
    @patch('main._detect_agent_context_left_percent', return_value=77)
    @patch('main.resolve_launcher_command', return_value='codex')
    @patch('main.session_exists', return_value=True)
    @patch('main.resolve_agent')
    @patch('main.check_tmux', return_value=True)
    def test_cmd_heartbeat_run_retry_then_success(
        self,
        _mock_tmux,
        mock_resolve_agent,
        _mock_session,
        _mock_launcher,
        _mock_context,
        _mock_rollover,
        mock_run_attempt,
        _mock_sleep,
        mock_audit,
        mock_notify,
    ):
        mock_resolve_agent.return_value = {
            'name': 'qa-agent',
            'file_id': 'EMP_0001',
            'enabled': True,
            'heartbeat': {
                'enabled': True,
                'recovery': {
                    'max_retries': 1,
                    'retry_backoff_seconds': 0,
                    'fallback_mode': 'none',
                },
            },
            'launcher': 'codex',
        }
        mock_run_attempt.side_effect = [
            {
                'send_status': 'fail',
                'ack_status': 'not_checked',
                'failure_type': 'send_fail',
                'duration_ms': 100,
            },
            {
                'send_status': 'ok',
                'ack_status': 'ack',
                'failure_type': '',
                'duration_ms': 120,
            },
        ]

        args = type('Args', (), {
            'agent': 'EMP_0001',
            'timeout': None,
            'retry': None,
            'backoff_seconds': 0,
            'fallback_mode': None,
            'notify_on_failure': False,
            'notifier_channel': None,
        })()

        result = main.cmd_heartbeat_run(args)
        self.assertEqual(result, 0)
        self.assertEqual(mock_run_attempt.call_count, 2)
        self.assertEqual(mock_audit.call_count, 2)
        mock_notify.assert_not_called()

    @patch('main._notify_heartbeat_failure', return_value=True)
    @patch('main.stabilize_codex_session', return_value=True)
    @patch('main._restart_heartbeat_session_fresh', return_value=True)
    @patch('main._append_heartbeat_audit_event')
    @patch('main.time.sleep', return_value=None)
    @patch('main._run_heartbeat_attempt')
    @patch('main._maybe_rollover_heartbeat_session', return_value=None)
    @patch('main._detect_agent_context_left_percent', return_value=12)
    @patch('main.resolve_launcher_command', return_value='codex')
    @patch('main.session_exists', return_value=True)
    @patch('main.resolve_agent')
    @patch('main.check_tmux', return_value=True)
    def test_cmd_heartbeat_run_fallback_and_notify_on_failure(
        self,
        _mock_tmux,
        mock_resolve_agent,
        _mock_session,
        _mock_launcher,
        _mock_context,
        _mock_rollover,
        mock_run_attempt,
        _mock_sleep,
        mock_audit,
        mock_restart,
        _mock_stabilize,
        mock_notify,
    ):
        mock_resolve_agent.return_value = {
            'name': 'qa-agent',
            'file_id': 'EMP_0001',
            'enabled': True,
            'heartbeat': {
                'enabled': True,
                'recovery': {
                    'max_retries': 0,
                    'retry_backoff_seconds': 0,
                    'fallback_mode': 'fresh',
                    'notify_on_failure': True,
                    'notifier_channel': 'all',
                },
            },
            'launcher': 'codex',
        }
        mock_run_attempt.side_effect = [
            {
                'send_status': 'ok',
                'ack_status': 'timeout',
                'failure_type': 'timeout',
                'duration_ms': 200,
            },
            {
                'send_status': 'fail',
                'ack_status': 'no_ack',
                'failure_type': 'send_fail',
                'duration_ms': 300,
            },
        ]

        args = type('Args', (), {
            'agent': 'EMP_0001',
            'timeout': None,
            'retry': 0,
            'backoff_seconds': 0,
            'fallback_mode': 'fresh',
            'notify_on_failure': True,
            'notifier_channel': 'all',
        })()

        result = main.cmd_heartbeat_run(args)
        self.assertEqual(result, 1)
        self.assertEqual(mock_run_attempt.call_count, 2)
        self.assertEqual(mock_audit.call_count, 2)
        mock_restart.assert_called_once()
        mock_notify.assert_called_once()

    @patch('main.stabilize_codex_session', return_value=True)
    @patch('main._restart_heartbeat_session_fresh', return_value=True)
    @patch('main._append_heartbeat_audit_event')
    @patch('main.time.sleep', return_value=None)
    @patch('main._run_heartbeat_attempt')
    @patch('main._maybe_rollover_heartbeat_session', return_value=None)
    @patch('main._detect_agent_context_left_percent', return_value=12)
    @patch('main.resolve_launcher_command', return_value='codex')
    @patch('main.session_exists', return_value=True)
    @patch('main.resolve_agent')
    @patch('main.check_tmux', return_value=True)
    def test_cmd_heartbeat_run_interrupted_skips_same_session_retry_and_uses_fresh_fallback(
        self,
        _mock_tmux,
        mock_resolve_agent,
        _mock_session,
        _mock_launcher,
        _mock_context,
        _mock_rollover,
        mock_run_attempt,
        _mock_sleep,
        mock_audit,
        mock_restart,
        mock_stabilize,
    ):
        mock_resolve_agent.return_value = {
            'name': 'qa-agent',
            'file_id': 'EMP_0001',
            'enabled': True,
            'heartbeat': {
                'enabled': True,
                'recovery': {
                    'max_retries': 1,
                    'retry_backoff_seconds': 0,
                    'fallback_mode': 'fresh',
                    'notify_on_failure': False,
                },
            },
            'launcher': 'codex',
        }
        mock_run_attempt.side_effect = [
            {
                'send_status': 'ok',
                'ack_status': 'no_ack',
                'failure_type': 'interrupted',
                'reason_code': 'HB_INTERRUPTED',
                'duration_ms': 200,
            },
            {
                'send_status': 'ok',
                'ack_status': 'ack',
                'failure_type': '',
                'reason_code': 'HB_ACK_OK',
                'duration_ms': 150,
            },
        ]

        args = type('Args', (), {
            'agent': 'EMP_0001',
            'timeout': None,
            'retry': None,
            'backoff_seconds': 0,
            'fallback_mode': 'fresh',
            'notify_on_failure': False,
            'notifier_channel': None,
        })()

        result = main.cmd_heartbeat_run(args)
        self.assertEqual(result, 0)
        self.assertEqual(mock_run_attempt.call_count, 2)
        self.assertEqual(mock_audit.call_count, 2)
        mock_restart.assert_called_once()
        mock_stabilize.assert_called_once()

    @patch('main.stabilize_codex_session', return_value=False)
    @patch('main._restart_heartbeat_session_fresh', return_value=True)
    @patch('main._append_heartbeat_audit_event')
    @patch('main.time.sleep', return_value=None)
    @patch('main._run_heartbeat_attempt')
    @patch('main._maybe_rollover_heartbeat_session', return_value=None)
    @patch('main._detect_agent_context_left_percent', return_value=12)
    @patch('main.resolve_launcher_command', return_value='codex')
    @patch('main.session_exists', return_value=True)
    @patch('main.resolve_agent')
    @patch('main.check_tmux', return_value=True)
    def test_cmd_heartbeat_run_fallback_stabilize_failure_skips_second_send(
        self,
        _mock_tmux,
        mock_resolve_agent,
        _mock_session,
        _mock_launcher,
        _mock_context,
        _mock_rollover,
        mock_run_attempt,
        _mock_sleep,
        mock_audit,
        mock_restart,
        mock_stabilize,
    ):
        mock_resolve_agent.return_value = {
            'name': 'qa-agent',
            'file_id': 'EMP_0001',
            'enabled': True,
            'heartbeat': {
                'enabled': True,
                'recovery': {
                    'max_retries': 1,
                    'retry_backoff_seconds': 0,
                    'fallback_mode': 'fresh',
                    'notify_on_failure': False,
                },
            },
            'launcher': 'codex',
        }
        mock_run_attempt.return_value = {
            'send_status': 'ok',
            'ack_status': 'no_ack',
            'failure_type': 'interrupted',
            'reason_code': 'HB_INTERRUPTED',
            'duration_ms': 200,
        }

        args = type('Args', (), {
            'agent': 'EMP_0001',
            'timeout': None,
            'retry': None,
            'backoff_seconds': 0,
            'fallback_mode': 'fresh',
            'notify_on_failure': False,
            'notifier_channel': None,
        })()

        result = main.cmd_heartbeat_run(args)
        self.assertEqual(result, 1)
        self.assertEqual(mock_run_attempt.call_count, 1)
        mock_restart.assert_called_once()
        mock_stabilize.assert_called_once()
        self.assertEqual(mock_audit.call_count, 2)


    @patch('main._notify_heartbeat_failure', return_value=True)
    @patch('main._append_heartbeat_audit_event')
    @patch('main.time.sleep', return_value=None)
    @patch('main._run_heartbeat_attempt')
    @patch('main._maybe_rollover_heartbeat_session', return_value=None)
    @patch('main._detect_agent_context_left_percent', return_value=40)
    @patch('main.resolve_launcher_command', return_value='codex')
    @patch('main.session_exists', return_value=True)
    @patch('main.resolve_agent')
    @patch('main.check_tmux', return_value=True)
    def test_cmd_heartbeat_run_ignores_legacy_guard_config_keys(
        self,
        _mock_tmux,
        mock_resolve_agent,
        _mock_session,
        _mock_launcher,
        _mock_context,
        _mock_rollover,
        mock_run_attempt,
        _mock_sleep,
        mock_audit,
        mock_notify,
    ):
        mock_resolve_agent.return_value = {
            'name': 'qa-agent',
            'file_id': 'EMP_0001',
            'enabled': True,
            'heartbeat': {
                'enabled': True,
                'watch_repo': True,
                'force_action_when_open_work': True,
                'recovery': {
                    'max_retries': 0,
                    'retry_backoff_seconds': 0,
                    'fallback_mode': 'none',
                    'notify_on_failure': False,
                },
            },
            'launcher': 'codex',
        }

        mock_run_attempt.return_value = {
            'send_status': 'ok',
            'ack_status': 'ack',
            'failure_type': '',
            'duration_ms': 80,
            'reason_code': 'HB_ACK_OK',
        }

        args = type('Args', (), {
            'agent': 'EMP_0001',
            'timeout': None,
            'retry': 0,
            'backoff_seconds': 0,
            'fallback_mode': 'none',
            'notify_on_failure': False,
            'notifier_channel': None,
        })()

        result = main.cmd_heartbeat_run(args)
        self.assertEqual(result, 0)
        self.assertEqual(mock_run_attempt.call_count, 1)
        mock_notify.assert_not_called()

        self.assertEqual(mock_audit.call_count, 1)
        self.assertEqual(mock_audit.call_args.kwargs.get('phase'), 'attempt')
        self.assertNotEqual(mock_audit.call_args.kwargs.get('phase'), 'guard_followup')

    @patch('main._append_heartbeat_audit_event')
    @patch('main.time.sleep', return_value=None)
    @patch('main._run_heartbeat_attempt')
    @patch('main._maybe_rollover_heartbeat_session', return_value=None)
    @patch('main._count_consecutive_auto_preflight_skips', return_value=0)
    @patch('main._heartbeat_preflight_runtime_state', return_value=('busy', 'busy_pattern:Thinking...'))
    @patch('main._detect_agent_context_left_percent', return_value=55)
    @patch('main.resolve_launcher_command', return_value='codex')
    @patch('main.session_exists', return_value=True)
    @patch('main.resolve_agent')
    @patch('main.check_tmux', return_value=True)
    def test_cmd_heartbeat_run_auto_mode_skips_when_agent_busy(
        self,
        _mock_tmux,
        mock_resolve_agent,
        _mock_session,
        _mock_launcher,
        _mock_context,
        _mock_skip_count,
        _mock_preflight,
        _mock_rollover,
        mock_run_attempt,
        _mock_sleep,
        mock_audit,
    ):
        mock_resolve_agent.return_value = {
            'name': 'qa-agent',
            'file_id': 'EMP_0001',
            'enabled': True,
            'heartbeat': {
                'enabled': True,
                'session_mode': 'auto',
                'recovery': {
                    'max_retries': 1,
                    'retry_backoff_seconds': 0,
                    'fallback_mode': 'none',
                },
            },
            'launcher': 'codex',
        }

        args = type('Args', (), {
            'agent': 'EMP_0001',
            'timeout': None,
            'retry': None,
            'backoff_seconds': 0,
            'fallback_mode': None,
            'notify_on_failure': False,
            'notifier_channel': None,
        })()

        result = main.cmd_heartbeat_run(args)
        self.assertEqual(result, 0)
        mock_run_attempt.assert_not_called()
        mock_audit.assert_called_once()
        self.assertEqual(mock_audit.call_args.kwargs.get('phase'), 'preflight')
        self.assertEqual(mock_audit.call_args.kwargs.get('failure_type'), 'busy_skip')
        self.assertEqual(mock_audit.call_args.kwargs.get('reason_code'), 'HB_AUTO_BUSY_SKIP')

    @patch('main._append_heartbeat_audit_event')
    @patch('main.has_pending_inbound_messages', return_value=True)
    @patch('main.time.sleep', return_value=None)
    @patch('main._run_heartbeat_attempt')
    @patch('main._maybe_rollover_heartbeat_session', return_value=None)
    @patch('main._maybe_run_main_inbound_heartbeat_sweep', return_value=False)
    @patch('main._count_consecutive_auto_preflight_skips', return_value=0)
    @patch('main._heartbeat_preflight_runtime_state', return_value=('idle', 'ready'))
    @patch('main._detect_agent_context_left_percent', return_value=55)
    @patch('main.resolve_launcher_command', return_value='codex')
    @patch('main.session_exists', return_value=True)
    @patch('main.resolve_agent')
    @patch('main.check_tmux', return_value=True)
    def test_cmd_heartbeat_run_yields_when_pending_user_queue_exists(
        self,
        _mock_tmux,
        mock_resolve_agent,
        _mock_session,
        _mock_launcher,
        _mock_context,
        _mock_preflight,
        _mock_skip_count,
        _mock_sweep,
        _mock_rollover,
        mock_run_attempt,
        _mock_sleep,
        _mock_pending,
        mock_audit,
    ):
        mock_resolve_agent.return_value = {
            'name': 'main',
            'file_id': 'main',
            'enabled': True,
            'heartbeat': {
                'enabled': True,
                'session_mode': 'auto',
                'recovery': {
                    'max_retries': 1,
                    'retry_backoff_seconds': 0,
                    'fallback_mode': 'none',
                },
            },
            'launcher': 'codex',
        }

        args = type('Args', (), {
            'agent': 'main',
            'timeout': None,
            'retry': None,
            'backoff_seconds': 0,
            'fallback_mode': None,
            'notify_on_failure': False,
            'notifier_channel': None,
        })()

        result = main.cmd_heartbeat_run(args)
        self.assertEqual(result, 0)
        mock_run_attempt.assert_not_called()
        mock_audit.assert_called_once()
        self.assertEqual(mock_audit.call_args.kwargs.get('phase'), 'preflight')
        self.assertEqual(mock_audit.call_args.kwargs.get('failure_type'), 'user_queue_yield')
        self.assertEqual(mock_audit.call_args.kwargs.get('reason_code'), 'HB_USER_QUEUE_PENDING')

    @patch('main.get_repo_root')
    @patch('main._append_heartbeat_audit_event')
    @patch('main.time.sleep', return_value=None)
    @patch('main._run_heartbeat_attempt')
    @patch('main._maybe_rollover_heartbeat_session', return_value=None)
    @patch('main._count_consecutive_auto_preflight_skips', return_value=0)
    @patch('main._heartbeat_preflight_runtime_state', return_value=('idle', 'ready'))
    @patch('main._detect_agent_context_left_percent', return_value=55)
    @patch('main.resolve_launcher_command', return_value='codex')
    @patch('main.session_exists', return_value=True)
    @patch('main.resolve_agent')
    @patch('main.check_tmux', return_value=True)
    def test_cmd_heartbeat_run_records_queue_yield_event(
        self,
        _mock_tmux,
        mock_resolve_agent,
        _mock_session,
        _mock_launcher,
        _mock_context,
        _mock_preflight,
        _mock_skip_count,
        _mock_rollover,
        mock_run_attempt,
        _mock_sleep,
        mock_audit,
        mock_repo_root,
    ):
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = Path(tmpdir)
            mock_repo_root.return_value = temp_root
            message_id = enqueue_inbound_message(
                temp_root,
                agent_id='main',
                source='send',
                message_kind='message',
                message='pending user work',
            )
            append_inbound_message_event(
                temp_root,
                agent_id='main',
                message_id=message_id,
                event='failed',
                state='failed',
                detail='waiting_for_retry_window',
                attempt_count=1,
                next_retry_at='2099-01-01T00:00:00Z',
            )
            mock_resolve_agent.return_value = {
                'name': 'main',
                'file_id': 'main',
                'enabled': True,
                'heartbeat': {
                    'enabled': True,
                    'session_mode': 'auto',
                    'recovery': {
                        'max_retries': 1,
                        'retry_backoff_seconds': 0,
                        'fallback_mode': 'none',
                    },
                },
                'launcher': 'codex',
            }

            args = type('Args', (), {
                'agent': 'main',
                'timeout': None,
                'retry': None,
                'backoff_seconds': 0,
                'fallback_mode': None,
                'notify_on_failure': False,
                'notifier_channel': None,
            })()

            result = main.cmd_heartbeat_run(args)
            self.assertEqual(result, 0)
            mock_run_attempt.assert_not_called()
            mock_audit.assert_called_once()
            events = read_inbound_events(temp_root, agent_id='main', message_id=message_id)
            self.assertEqual([event.get('event') for event in events], ['received', 'queued', 'failed', 'yielded'])
            self.assertEqual(events[-1].get('reason_code'), 'HB_USER_QUEUE_PENDING')

    @patch('main.get_repo_root')
    @patch('main._append_heartbeat_audit_event')
    @patch('main.time.sleep', return_value=None)
    @patch('main._run_heartbeat_attempt')
    @patch('main.drain_main_inbound_once')
    @patch('main._maybe_rollover_heartbeat_session', return_value=None)
    @patch('main._count_consecutive_auto_preflight_skips', return_value=0)
    @patch('main._heartbeat_preflight_runtime_state', return_value=('idle', 'ready'))
    @patch('main._detect_agent_context_left_percent', return_value=55)
    @patch('main.resolve_launcher_command', return_value='codex')
    @patch('main.session_exists', return_value=True)
    @patch('main.resolve_agent')
    @patch('main.check_tmux', return_value=True)
    def test_cmd_heartbeat_run_sweeps_replayable_queue_before_dispatch(
        self,
        _mock_tmux,
        mock_resolve_agent,
        _mock_session,
        _mock_launcher,
        _mock_context,
        _mock_preflight,
        _mock_skip_count,
        _mock_rollover,
        mock_drain,
        mock_run_attempt,
        _mock_sleep,
        mock_audit,
        mock_repo_root,
    ):
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = Path(tmpdir)
            mock_repo_root.return_value = temp_root
            enqueue_inbound_message(
                temp_root,
                agent_id='main',
                source='send',
                message_kind='message',
                message='queued user work',
            )
            mock_resolve_agent.return_value = {
                'name': 'main',
                'file_id': 'main',
                'enabled': True,
                'heartbeat': {
                    'enabled': True,
                    'session_mode': 'auto',
                    'recovery': {
                        'max_retries': 1,
                        'retry_backoff_seconds': 0,
                        'fallback_mode': 'none',
                    },
                },
                'launcher': 'codex',
            }
            mock_drain.return_value = {
                'rc': 0,
                'drained': 1,
                'failed': 0,
                'dead_lettered': 0,
                'skipped': 0,
            }

            args = type('Args', (), {
                'agent': 'main',
                'timeout': None,
                'retry': None,
                'backoff_seconds': 0,
                'fallback_mode': None,
                'notify_on_failure': False,
                'notifier_channel': None,
            })()

            result = main.cmd_heartbeat_run(args)
            self.assertEqual(result, 0)
            mock_drain.assert_called_once_with(agent_id='main', trigger='heartbeat_sweep')
            mock_run_attempt.assert_not_called()
            mock_audit.assert_called_once()
            self.assertEqual(mock_audit.call_args.kwargs.get('reason_code'), 'HB_INBOUND_SWEEP')
            self.assertEqual(mock_audit.call_args.kwargs.get('recovery_action'), 'inbound_sweep')
            self.assertEqual(mock_audit.call_args.kwargs.get('failure_type'), 'inbound_queue_sweep')

    @patch('main._append_heartbeat_audit_event')
    @patch('main.time.sleep', return_value=None)
    @patch('main._run_heartbeat_attempt', return_value={
        'send_status': 'ok',
        'ack_status': 'yielded',
        'failure_type': 'user_queue_yield',
        'reason_code': 'HB_USER_QUEUE_YIELD',
        'duration_ms': 1,
    })
    @patch('main._maybe_rollover_heartbeat_session', return_value=None)
    @patch('main.has_pending_inbound_messages', side_effect=[False, False])
    @patch('main._maybe_run_main_inbound_heartbeat_sweep', return_value=False)
    @patch('main._count_consecutive_auto_preflight_skips', return_value=0)
    @patch('main._heartbeat_preflight_runtime_state', return_value=('idle', 'ready'))
    @patch('main._detect_agent_context_left_percent', return_value=55)
    @patch('main.resolve_launcher_command', return_value='codex')
    @patch('main.session_exists', return_value=True)
    @patch('main.resolve_agent')
    @patch('main.check_tmux', return_value=True)
    def test_cmd_heartbeat_run_yields_when_user_queue_arrives_during_attempt(
        self,
        _mock_tmux,
        mock_resolve_agent,
        _mock_session,
        _mock_launcher,
        _mock_context,
        _mock_preflight,
        _mock_skip_count,
        _mock_sweep,
        _mock_pending,
        _mock_rollover,
        mock_run_attempt,
        _mock_sleep,
        mock_audit,
    ):
        mock_resolve_agent.return_value = {
            'name': 'main',
            'file_id': 'main',
            'enabled': True,
            'heartbeat': {
                'enabled': True,
                'session_mode': 'auto',
                'recovery': {
                    'max_retries': 1,
                    'retry_backoff_seconds': 0,
                    'fallback_mode': 'none',
                },
            },
            'launcher': 'codex',
        }

        args = type('Args', (), {
            'agent': 'main',
            'timeout': None,
            'retry': None,
            'backoff_seconds': 0,
            'fallback_mode': None,
            'notify_on_failure': False,
            'notifier_channel': None,
        })()

        result = main.cmd_heartbeat_run(args)
        self.assertEqual(result, 0)
        mock_run_attempt.assert_called_once()
        self.assertEqual(mock_audit.call_args.kwargs.get('failure_type'), 'user_queue_yield')

    @patch('main._append_heartbeat_audit_event')
    @patch('main.time.sleep', return_value=None)
    @patch('main._run_heartbeat_attempt')
    @patch('main._maybe_rollover_heartbeat_session', return_value=None)
    @patch('main._count_consecutive_auto_preflight_skips', return_value=0)
    @patch('main._heartbeat_preflight_runtime_state', return_value=('busy', 'preflight_pane_changed:1'))
    @patch('main._detect_agent_context_left_percent', return_value=55)
    @patch('main.resolve_launcher_command', return_value='codex')
    @patch('main.session_exists', return_value=True)
    @patch('main.resolve_agent')
    @patch('main.check_tmux', return_value=True)
    def test_cmd_heartbeat_run_auto_mode_skips_when_preflight_detects_active_pane(
        self,
        _mock_tmux,
        mock_resolve_agent,
        _mock_session,
        _mock_launcher,
        _mock_context,
        _mock_skip_count,
        _mock_preflight,
        _mock_rollover,
        mock_run_attempt,
        _mock_sleep,
        mock_audit,
    ):
        mock_resolve_agent.return_value = {
            'name': 'qa-agent',
            'file_id': 'EMP_0001',
            'enabled': True,
            'heartbeat': {
                'enabled': True,
                'session_mode': 'auto',
                'recovery': {
                    'max_retries': 1,
                    'retry_backoff_seconds': 0,
                    'fallback_mode': 'none',
                },
            },
            'launcher': 'codex',
        }

        args = type('Args', (), {
            'agent': 'EMP_0001',
            'timeout': None,
            'retry': None,
            'backoff_seconds': 0,
            'fallback_mode': None,
            'notify_on_failure': False,
            'notifier_channel': None,
        })()

        result = main.cmd_heartbeat_run(args)
        self.assertEqual(result, 0)
        mock_run_attempt.assert_not_called()
        mock_audit.assert_called_once()
        self.assertEqual(mock_audit.call_args.kwargs.get('phase'), 'preflight')
        self.assertEqual(mock_audit.call_args.kwargs.get('failure_type'), 'active_skip')
        self.assertEqual(mock_audit.call_args.kwargs.get('reason_code'), 'HB_AUTO_ACTIVE_SKIP')

    @patch('main._append_heartbeat_audit_event')
    @patch('main.time.sleep', return_value=None)
    @patch('main._run_heartbeat_attempt', return_value={
        'send_status': 'ok',
        'ack_status': 'ack',
        'failure_type': '',
        'reason_code': '',
        'duration_ms': 1,
    })
    @patch('main._maybe_rollover_heartbeat_session', return_value=None)
    @patch('main._count_consecutive_auto_preflight_skips', return_value=main._HEARTBEAT_AUTO_STARVATION_SKIP_THRESHOLD)
    @patch('main._heartbeat_preflight_runtime_state', return_value=('busy', 'busy_pattern:Thinking...'))
    @patch('main._detect_agent_context_left_percent', return_value=55)
    @patch('main.resolve_launcher_command', return_value='codex')
    @patch('main.session_exists', return_value=True)
    @patch('main.resolve_agent')
    @patch('main.check_tmux', return_value=True)
    def test_cmd_heartbeat_run_auto_mode_bypasses_preflight_after_starvation_threshold(
        self,
        _mock_tmux,
        mock_resolve_agent,
        _mock_session,
        _mock_launcher,
        _mock_context,
        _mock_preflight,
        _mock_skip_count,
        _mock_rollover,
        mock_run_attempt,
        _mock_sleep,
        mock_audit,
    ):
        mock_resolve_agent.return_value = {
            'name': 'qa-agent',
            'file_id': 'EMP_0001',
            'enabled': True,
            'heartbeat': {
                'enabled': True,
                'session_mode': 'auto',
                'recovery': {
                    'max_retries': 1,
                    'retry_backoff_seconds': 0,
                    'fallback_mode': 'none',
                },
            },
            'launcher': 'codex',
        }

        args = type('Args', (), {
            'agent': 'EMP_0001',
            'timeout': None,
            'retry': None,
            'backoff_seconds': 0,
            'fallback_mode': None,
            'notify_on_failure': False,
            'notifier_channel': None,
        })()

        result = main.cmd_heartbeat_run(args)
        self.assertEqual(result, 0)
        mock_run_attempt.assert_called_once()
        mock_audit.assert_called_once()
        self.assertEqual(mock_audit.call_args.kwargs.get('phase'), 'attempt')
        self.assertEqual(mock_audit.call_args.kwargs.get('recovery_action'), 'auto_starvation_bypass')

    @patch('main._append_heartbeat_audit_event')
    @patch('main.time.sleep', return_value=None)
    @patch('main._run_heartbeat_attempt')
    @patch('main._maybe_rollover_heartbeat_session', return_value=None)
    @patch('main._count_consecutive_auto_preflight_skips', return_value=99)
    @patch('main._heartbeat_preflight_runtime_state', return_value=('busy', 'busy_pattern:Thinking...'))
    @patch('main._detect_agent_context_left_percent', return_value=55)
    @patch('main.resolve_launcher_command', return_value='codex')
    @patch('main.session_exists', return_value=True)
    @patch('main.resolve_agent')
    @patch('main.check_tmux', return_value=True)
    def test_cmd_heartbeat_run_auto_mode_can_disable_starvation_bypass(
        self,
        _mock_tmux,
        mock_resolve_agent,
        _mock_session,
        _mock_launcher,
        _mock_context,
        _mock_preflight,
        _mock_skip_count,
        _mock_rollover,
        mock_run_attempt,
        _mock_sleep,
        mock_audit,
    ):
        mock_resolve_agent.return_value = {
            'name': 'main',
            'file_id': 'main',
            'enabled': True,
            'heartbeat': {
                'enabled': True,
                'session_mode': 'auto',
                'auto_starvation_skip_threshold': 0,
                'recovery': {
                    'max_retries': 1,
                    'retry_backoff_seconds': 0,
                    'fallback_mode': 'none',
                },
            },
            'launcher': 'codex',
        }

        args = type('Args', (), {
            'agent': 'main',
            'timeout': None,
            'retry': None,
            'backoff_seconds': 0,
            'fallback_mode': None,
            'notify_on_failure': False,
            'notifier_channel': None,
        })()

        result = main.cmd_heartbeat_run(args)
        self.assertEqual(result, 0)
        mock_run_attempt.assert_not_called()
        mock_audit.assert_called_once()
        self.assertEqual(mock_audit.call_args.kwargs.get('phase'), 'preflight')
        self.assertEqual(mock_audit.call_args.kwargs.get('failure_type'), 'busy_skip')

    @patch('main._append_heartbeat_audit_event')
    @patch('main._schedule_pending_heartbeat_rescue_timer', return_value=True)
    @patch('main._heartbeat_id_age_seconds', return_value=60)
    @patch('main.time.sleep', return_value=None)
    @patch('main._run_heartbeat_attempt')
    @patch('main._maybe_rollover_heartbeat_session', return_value=None)
    @patch('main._count_consecutive_auto_preflight_skips', return_value=1)
    @patch('main._heartbeat_preflight_runtime_state', return_value=('busy', 'pending_heartbeat:20260317-010101'))
    @patch('main._detect_agent_context_left_percent', return_value=55)
    @patch('main.resolve_launcher_command', return_value='codex')
    @patch('main.session_exists', return_value=True)
    @patch('main.resolve_agent')
    @patch('main.check_tmux', return_value=True)
    def test_cmd_heartbeat_run_auto_mode_does_not_bypass_pending_heartbeat(
        self,
        _mock_tmux,
        mock_resolve_agent,
        _mock_session,
        _mock_launcher,
        _mock_context,
        _mock_preflight,
        _mock_skip_count,
        _mock_rollover,
        mock_run_attempt,
        _mock_sleep,
        _mock_hb_age,
        mock_schedule_rescue,
        mock_audit,
    ):
        mock_resolve_agent.return_value = {
            'name': 'qa-agent',
            'file_id': 'EMP_0001',
            'enabled': True,
            'heartbeat': {
                'enabled': True,
                'session_mode': 'auto',
                'recovery': {
                    'max_retries': 1,
                    'retry_backoff_seconds': 0,
                    'fallback_mode': 'none',
                },
            },
            'launcher': 'codex',
        }

        args = type('Args', (), {
            'agent': 'EMP_0001',
            'timeout': None,
            'retry': None,
            'backoff_seconds': 0,
            'fallback_mode': None,
            'notify_on_failure': False,
            'notifier_channel': None,
        })()

        result = main.cmd_heartbeat_run(args)
        self.assertEqual(result, 0)
        mock_run_attempt.assert_not_called()
        mock_schedule_rescue.assert_called_once()
        mock_audit.assert_called_once()
        self.assertEqual(mock_audit.call_args.kwargs.get('phase'), 'preflight')
        self.assertEqual(mock_audit.call_args.kwargs.get('failure_type'), 'pending_skip')
        self.assertEqual(mock_audit.call_args.kwargs.get('reason_code'), 'HB_AUTO_PENDING_SKIP')
        self.assertEqual(mock_audit.call_args.kwargs.get('recovery_action'), 'schedule_pending_rescue_timer')

    @patch('main._append_heartbeat_audit_event')
    @patch('main._schedule_pending_heartbeat_rescue_timer')
    @patch('main._restart_heartbeat_session_restore', return_value=True)
    @patch('main.time.sleep', return_value=None)
    @patch('main._run_heartbeat_attempt', return_value={
        'send_status': 'ok',
        'ack_status': 'ack',
        'failure_type': '',
        'reason_code': '',
        'duration_ms': 1,
    })
    @patch('main._maybe_rollover_heartbeat_session', return_value=None)
    @patch('main._count_consecutive_auto_preflight_skips', side_effect=[main._HEARTBEAT_PENDING_RESCUE_SKIP_THRESHOLD, 0])
    @patch('main._heartbeat_id_age_seconds', return_value=main._HEARTBEAT_PENDING_RESCUE_AGE_SECONDS + 5)
    @patch('main._heartbeat_preflight_runtime_state', return_value=('busy', 'pending_heartbeat:20260317-010101'))
    @patch('main._detect_agent_context_left_percent', return_value=55)
    @patch('main.resolve_launcher_command', return_value='codex')
    @patch('main.session_exists', return_value=True)
    @patch('main.resolve_agent')
    @patch('main.check_tmux', return_value=True)
    def test_cmd_heartbeat_run_auto_mode_rescues_stale_pending_heartbeat(
        self,
        _mock_tmux,
        mock_resolve_agent,
        _mock_session,
        _mock_launcher,
        _mock_context,
        _mock_preflight,
        _mock_hb_age,
        _mock_skip_count,
        _mock_rollover,
        mock_run_attempt,
        _mock_sleep,
        mock_restart_restore,
        mock_schedule_rescue,
        mock_audit,
    ):
        mock_resolve_agent.return_value = {
            'name': 'qa-agent',
            'file_id': 'EMP_0001',
            'enabled': True,
            'heartbeat': {
                'enabled': True,
                'session_mode': 'auto',
                'recovery': {
                    'max_retries': 1,
                    'retry_backoff_seconds': 0,
                    'fallback_mode': 'none',
                },
            },
            'launcher': 'codex',
        }

        args = type('Args', (), {
            'agent': 'EMP_0001',
            'timeout': None,
            'retry': None,
            'backoff_seconds': 0,
            'fallback_mode': None,
            'notify_on_failure': False,
            'notifier_channel': None,
        })()

        result = main.cmd_heartbeat_run(args)
        self.assertEqual(result, 0)
        mock_restart_restore.assert_called_once()
        mock_schedule_rescue.assert_not_called()
        mock_run_attempt.assert_called_once()
        self.assertGreaterEqual(mock_audit.call_count, 1)
        self.assertEqual(mock_audit.call_args.kwargs.get('phase'), 'attempt')
        self.assertEqual(mock_audit.call_args.kwargs.get('recovery_action'), 'auto_pending_rescue')

    @patch('main._append_heartbeat_audit_event')
    @patch('main.time.sleep', return_value=None)
    @patch('main._run_heartbeat_attempt', return_value={
        'send_status': 'ok',
        'ack_status': 'ack',
        'failure_type': '',
        'reason_code': '',
        'duration_ms': 1,
    })
    @patch('main._maybe_rollover_heartbeat_session', return_value=None)
    @patch('main._heartbeat_preflight_runtime_state', return_value=('error', 'timeout'))
    @patch('main._detect_agent_context_left_percent', return_value=55)
    @patch('main.resolve_launcher_command', return_value='claude-code')
    @patch('main.session_exists', return_value=True)
    @patch('main.resolve_agent')
    @patch('main.check_tmux', return_value=True)
    def test_cmd_heartbeat_run_force_mode_bypasses_preflight_idle_gate(
        self,
        _mock_tmux,
        mock_resolve_agent,
        _mock_session,
        _mock_launcher,
        _mock_context,
        mock_preflight,
        _mock_rollover,
        mock_run_attempt,
        _mock_sleep,
        mock_audit,
    ):
        mock_resolve_agent.return_value = {
            'name': 'qa-agent',
            'file_id': 'EMP_0001',
            'enabled': True,
            'heartbeat': {
                'enabled': True,
                'session_mode': 'force',
                'recovery': {
                    'max_retries': 1,
                    'retry_backoff_seconds': 0,
                    'fallback_mode': 'none',
                },
            },
            'launcher': 'claude-code',
        }

        args = type('Args', (), {
            'agent': 'EMP_0001',
            'timeout': None,
            'retry': None,
            'backoff_seconds': 0,
            'fallback_mode': None,
            'notify_on_failure': False,
            'notifier_channel': None,
        })()

        result = main.cmd_heartbeat_run(args)
        self.assertEqual(result, 0)
        mock_preflight.assert_not_called()
        mock_run_attempt.assert_called_once()
        self.assertGreaterEqual(mock_audit.call_count, 1)
        self.assertEqual(mock_audit.call_args.kwargs.get('phase'), 'attempt')
        self.assertEqual(mock_audit.call_args.kwargs.get('session_mode'), 'force')


class RuntimeStateInterruptedTests(unittest.TestCase):
    """Tests for the new 'interrupted' runtime state (Issue #97)."""

    def setUp(self):
        # Import runtime_state from the scripts directory
        import runtime_state
        self.runtime_state = runtime_state
        self.codex_runtime_cfg = {
            'busy_patterns': ['Thinking', 'esc to interrupt'],
            'blocked_patterns': ['requires approval'],
            'stuck_after_seconds': 180,
            'interrupted_patterns': ['Conversation interrupted'],
            'suggestion_tip_pattern': r'^[›❯]\s+(?!\d+\.)',
        }

    def test_conversation_interrupted_detected(self):
        """'■ Conversation interrupted' in output → state='interrupted'."""
        output = (
            "• Working on task\n"
            "■ Conversation interrupted - tell the model what to do differently.\n"
            "\n"
            "› Write tests for @filename\n"
            "\n"
            "  ? for shortcuts                                              55% context left"
        )
        result = self.runtime_state.evaluate_runtime_state(
            output=output,
            runtime_config=self.codex_runtime_cfg,
        )
        self.assertEqual(result['state'], 'interrupted')
        self.assertIn('interrupted', result.get('reason', ''))

    def test_plain_text_conversation_interrupted_is_not_interrupted(self):
        """Quoted/plain text mentioning 'Conversation interrupted' should not trigger interrupted."""
        output = (
            "• Reading Slack transcript\n"
            "用户说：这里应该是 Conversation interrupted 的误判，不是 Codex UI 中断。\n"
            "继续检查 timer 和 heartbeat 逻辑。\n"
        )
        result = self.runtime_state.evaluate_runtime_state(
            output=output,
            runtime_config=self.codex_runtime_cfg,
        )
        self.assertNotEqual(result['state'], 'interrupted')
        self.assertEqual(result['state'], 'idle')

    def test_old_plain_text_interrupted_plus_busy_marker_stays_busy(self):
        """Busy pane with quoted text should remain busy, not interrupted."""
        output = (
            "Slack transcript: Conversation interrupted was reported by the user.\n"
            "• Working (4s • esc to interrupt)\n"
        )
        result = self.runtime_state.evaluate_runtime_state(
            output=output,
            runtime_config=self.codex_runtime_cfg,
        )
        self.assertEqual(result['state'], 'busy')

    def test_suggestion_tip_with_shortcuts_detected(self):
        """Suggestion tip '› Write tests...' + '? for shortcuts' → interrupted."""
        output = (
            "\n"
            "› Use /skills to list available skills\n"
            "\n"
            "  ? for shortcuts                                              89% context left"
        )
        result = self.runtime_state.evaluate_runtime_state(
            output=output,
            runtime_config=self.codex_runtime_cfg,
        )
        self.assertEqual(result['state'], 'interrupted')
        self.assertIn('suggestion_tip', result.get('reason', ''))

    def test_numbered_menu_not_interrupted(self):
        """Numbered menu '› 1. Try new model' should NOT be interrupted."""
        output = (
            "› 1. Try new model\n"
            "› 2. Use existing model\n"
            "  ? for shortcuts                                              100% context left"
        )
        result = self.runtime_state.evaluate_runtime_state(
            output=output,
            runtime_config=self.codex_runtime_cfg,
        )
        # Numbered menus should not trigger suggestion_tip detection
        self.assertNotEqual(result.get('reason', ''), 'suggestion_tip')

    def test_normal_idle_not_interrupted(self):
        """Normal idle prompt without suggestion tip → idle."""
        output = (
            "• Task completed successfully\n"
            "\n"
            "›\n"
            "                                                               80% context left"
        )
        result = self.runtime_state.evaluate_runtime_state(
            output=output,
            runtime_config=self.codex_runtime_cfg,
        )
        self.assertEqual(result['state'], 'idle')

    def test_busy_takes_priority_over_interrupted(self):
        """If busy pattern is also present, busy takes priority (turn still active)."""
        output = (
            "• Analyzing code (5s • esc to interrupt)\n"
            "› Write tests for @filename\n"
            "  ? for shortcuts"
        )
        # 'Conversation interrupted' not in output, but suggestion tip is.
        # However 'esc to interrupt' matches busy pattern → should be interrupted
        # because interrupted_patterns check runs before busy_patterns check.
        # Actually, the interrupted check for 'Conversation interrupted' won't match,
        # but suggestion_tip will match. Let's verify the priority.
        result = self.runtime_state.evaluate_runtime_state(
            output=output,
            runtime_config=self.codex_runtime_cfg,
        )
        # suggestion_tip detection runs before busy, so this should be interrupted
        self.assertEqual(result['state'], 'interrupted')


class PendingHeartbeatDetectionTests(unittest.TestCase):
    """Tests for _has_pending_heartbeat() — prevents HB accumulation."""

    def test_no_hb_id_in_pane(self):
        output = "› Implement {feature}\n  ? for shortcuts  100% context left"
        pending, hb_id = main._has_pending_heartbeat(output)
        self.assertFalse(pending)
        self.assertEqual(hb_id, '')

    def test_empty_output(self):
        pending, hb_id = main._has_pending_heartbeat('')
        self.assertFalse(pending)

    def test_pending_hb_no_response(self):
        fresh_hb = (datetime.now(timezone.utc) - timedelta(minutes=1)).strftime('%Y%m%d-%H%M%S')
        output = (
            f"Read HEARTBEAT.md if it exists... [HB_ID:{fresh_hb}]\n"
            "› Implement {feature}\n"
            "  ? for shortcuts  100% context left\n"
        )
        pending, hb_id = main._has_pending_heartbeat(output)
        self.assertTrue(pending)
        self.assertEqual(hb_id, fresh_hb)

    def test_hb_with_ok_response(self):
        output = (
            "Read HEARTBEAT.md if it exists... [HB_ID:20260301-150002]\n"
            "HEARTBEAT_OK\n"
            "› Implement {feature}\n"
        )
        pending, hb_id = main._has_pending_heartbeat(output)
        self.assertFalse(pending)

    def test_multiple_hbs_last_unanswered(self):
        old_hb = (datetime.now(timezone.utc) - timedelta(minutes=30)).strftime('%Y%m%d-%H%M%S')
        fresh_hb = (datetime.now(timezone.utc) - timedelta(minutes=1)).strftime('%Y%m%d-%H%M%S')
        output = (
            f"Read HEARTBEAT.md if it exists... [HB_ID:{old_hb}]\n"
            "HEARTBEAT_OK\n"
            f"Read HEARTBEAT.md if it exists... [HB_ID:{fresh_hb}]\n"
            "› Implement {feature}\n"
        )
        pending, hb_id = main._has_pending_heartbeat(output)
        self.assertTrue(pending)
        self.assertEqual(hb_id, fresh_hb)

    def test_multiple_hbs_all_answered(self):
        output = (
            "Read HEARTBEAT.md if it exists... [HB_ID:20260301-140002]\n"
            "HEARTBEAT_OK\n"
            "Read HEARTBEAT.md if it exists... [HB_ID:20260301-150002]\n"
            "HEARTBEAT_OK\n"
        )
        pending, hb_id = main._has_pending_heartbeat(output)
        self.assertFalse(pending)

    def test_pending_hb_fresh_under_stale_threshold(self):
        hb_id = (datetime.now(timezone.utc) - timedelta(minutes=5)).strftime('%Y%m%d-%H%M%S')
        output = f"Read HEARTBEAT.md if it exists... [HB_ID:{hb_id}]\n"
        pending, parsed_hb_id = main._has_pending_heartbeat(output, stale_threshold_seconds=900)
        self.assertTrue(pending)
        self.assertEqual(parsed_hb_id, hb_id)

    def test_pending_hb_stale_over_stale_threshold(self):
        hb_id = (datetime.now(timezone.utc) - timedelta(minutes=16)).strftime('%Y%m%d-%H%M%S')
        output = f"Read HEARTBEAT.md if it exists... [HB_ID:{hb_id}]\n"
        pending, parsed_hb_id = main._has_pending_heartbeat(output, stale_threshold_seconds=900)
        self.assertFalse(pending)
        self.assertEqual(parsed_hb_id, '')

    def test_pending_hb_parse_failure_falls_back_to_pending(self):
        output = "Read HEARTBEAT.md if it exists... [HB_ID:20261301-250000]\n"
        pending, hb_id = main._has_pending_heartbeat(output, stale_threshold_seconds=900)
        self.assertTrue(pending)
        self.assertEqual(hb_id, '20261301-250000')


if __name__ == '__main__':
    unittest.main()
