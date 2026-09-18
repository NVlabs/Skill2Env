from __future__ import annotations
import argparse
import io
import random
import sys
import tempfile
import unittest
from contextlib import ExitStack, redirect_stdout
from pathlib import Path
from unittest.mock import patch


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import main  # noqa: E402


DETERMINISTIC_SEED = 20260210


class _FakeRuntime:
    def __init__(self):
        self.running = True
        self.sent_messages: list[dict] = []

    def session_exists(self, _agent_id: str) -> bool:
        return self.running

    def send_keys(self, agent_id: str, message: str, **kwargs) -> bool:
        self.sent_messages.append({'agent_id': agent_id, 'message': message, 'kwargs': kwargs})
        return True


class IntegrationMatrixSlice1Tests(unittest.TestCase):
    def setUp(self):
        random.seed(DETERMINISTIC_SEED)
        self.temp_root = Path(tempfile.mkdtemp(prefix='agent-manager-integration-matrix-'))
        self.work_dir = self.temp_root / 'workspace'
        self.work_dir.mkdir(parents=True, exist_ok=True)

    def _agent_config(self, *, launcher: str, recovery: dict | None = None) -> dict:
        heartbeat = {'enabled': True, 'session_mode': 'restore'}
        if recovery is not None:
            heartbeat['recovery'] = recovery

        return {
            'name': 'dev',
            'file_id': 'EMP_0001',
            'working_directory': str(self.work_dir),
            'launcher': launcher,
            'launcher_args': [],
            'heartbeat': heartbeat,
            'enabled': True,
        }

    def _patch_common(self, stack: ExitStack, runtime: _FakeRuntime, config: dict):
        stack.enter_context(patch('main.time.sleep', return_value=None))
        stack.enter_context(patch('main.check_tmux', return_value=True))
        stack.enter_context(patch('main.resolve_agent', side_effect=lambda _agent: config))
        stack.enter_context(patch('main.get_agent_id', return_value='emp-0001'))
        stack.enter_context(patch('main.resolve_launcher_command', side_effect=lambda launcher: launcher))
        stack.enter_context(patch('main._should_use_codex_file_pointer', return_value=True))
        stack.enter_context(patch('main.get_repo_root', return_value=self.temp_root))
        stack.enter_context(patch('main.write_codex_message_file', side_effect=main.write_codex_message_file))
        stack.enter_context(patch('main.session_exists', side_effect=runtime.session_exists))
        stack.enter_context(patch('main.send_keys', side_effect=runtime.send_keys))
        stack.enter_context(patch('main._detect_agent_context_left_percent', return_value=77))
        stack.enter_context(patch('main._maybe_rollover_heartbeat_session', return_value=None))
        stack.enter_context(patch('main._append_heartbeat_audit_event', return_value=None))
        stack.enter_context(patch('main._notify_heartbeat_failure', return_value=True))
        stack.enter_context(patch('main._restart_heartbeat_session_fresh', return_value=True))

    def _run_cmd(self, func, args, *, stdin_text: str | None = None):
        output = io.StringIO()
        with redirect_stdout(output):
            if stdin_text is None:
                rc = func(args)
            else:
                with patch('sys.stdin', io.StringIO(stdin_text)):
                    rc = func(args)
        return rc, output.getvalue()

    def test_provider_transport_matrix_send_and_assign(self):
        cases = [
            {'launcher': 'codex', 'expect_pointer': True},
            {'launcher': 'claude-code', 'expect_pointer': False},
            {'launcher': 'generic-cli', 'expect_pointer': False},
        ]

        long_message = '\n'.join([f'line-{index}' for index in range(24)])
        long_task = '\n'.join([f'task-{index}' for index in range(24)])

        for case in cases:
            with self.subTest(case=case):
                runtime = _FakeRuntime()
                config = self._agent_config(launcher=case['launcher'])
                with ExitStack() as stack:
                    self._patch_common(stack, runtime, config)

                    send_rc, send_out = self._run_cmd(
                        main.cmd_send,
                        argparse.Namespace(agent='dev', message=long_message, send_enter=True),
                    )
                    self.assertEqual(send_rc, 0, msg=f"send failed: {send_out}")
                    send_payload = runtime.sent_messages[-1]['message']

                    if case['expect_pointer']:
                        self.assertIn('Read and execute the message from file:', send_payload)
                        send_file = Path(send_payload.split('file:', 1)[1].splitlines()[0].strip())
                        self.assertTrue(send_file.exists())
                    else:
                        self.assertEqual(send_payload, long_message)

                    assign_rc, assign_out = self._run_cmd(
                        main.cmd_assign,
                        argparse.Namespace(agent='dev', task_file=None),
                        stdin_text=long_task,
                    )
                    self.assertEqual(assign_rc, 0, msg=f"assign failed: {assign_out}")
                    assign_payload = runtime.sent_messages[-1]['message']

                    if case['expect_pointer']:
                        self.assertIn('Read and follow instructions from file:', assign_payload)
                        assign_file = Path(assign_payload.split('file:', 1)[1].splitlines()[0].strip())
                        self.assertTrue(assign_file.exists())
                    else:
                        self.assertIn('# Task Assignment', assign_payload)

    def test_heartbeat_recovery_matrix_retry_and_fallback(self):
        cases = [
            {
                'name': 'retry-then-success',
                'recovery': {
                    'max_retries': 1,
                    'retry_backoff_seconds': 0,
                    'fallback_mode': 'none',
                    'notify_on_failure': False,
                },
                'attempts': [
                    {'send_status': 'fail', 'ack_status': 'not_checked', 'failure_type': 'send_fail', 'duration_ms': 10},
                    {'send_status': 'ok', 'ack_status': 'ack', 'failure_type': '', 'duration_ms': 20},
                ],
                'expected_rc': 0,
                'expect_restart_calls': 0,
                'expect_notify_calls': 0,
            },
            {
                'name': 'fallback-fresh-then-fail',
                'recovery': {
                    'max_retries': 0,
                    'retry_backoff_seconds': 0,
                    'fallback_mode': 'fresh',
                    'notify_on_failure': True,
                    'notifier_channel': 'all',
                },
                'attempts': [
                    {'send_status': 'ok', 'ack_status': 'timeout', 'failure_type': 'timeout', 'duration_ms': 30},
                ],
                'stabilize_ok': False,
                'expected_rc': 1,
                'expect_restart_calls': 1,
                'expect_notify_calls': 1,
            },
        ]

        for case in cases:
            with self.subTest(case=case['name']):
                runtime = _FakeRuntime()
                config = self._agent_config(launcher='codex', recovery=case['recovery'])

                with ExitStack() as stack:
                    self._patch_common(stack, runtime, config)
                    run_attempt_mock = stack.enter_context(
                        patch('main._run_heartbeat_attempt', side_effect=case['attempts'])
                    )
                    restart_mock = stack.enter_context(
                        patch('main._restart_heartbeat_session_fresh', return_value=True)
                    )
                    stack.enter_context(
                        patch('main.stabilize_codex_session', return_value=case.get('stabilize_ok', True))
                    )
                    notify_mock = stack.enter_context(
                        patch('main._notify_heartbeat_failure', return_value=True)
                    )

                    rc, output = self._run_cmd(
                        main.cmd_heartbeat_run,
                        argparse.Namespace(
                            agent='dev',
                            timeout=None,
                            retry=None,
                            backoff_seconds=0,
                            fallback_mode=None,
                            notify_on_failure=None,
                            notifier_channel=None,
                        ),
                    )

                self.assertEqual(rc, case['expected_rc'], msg=output)
                self.assertEqual(run_attempt_mock.call_count, len(case['attempts']))
                self.assertEqual(restart_mock.call_count, case['expect_restart_calls'])
                self.assertEqual(notify_mock.call_count, case['expect_notify_calls'])


if __name__ == '__main__':
    unittest.main()
