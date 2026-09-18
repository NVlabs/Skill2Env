from __future__ import annotations
import sys
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import runtime_state  # noqa: E402


class RuntimeStateMachineTests(unittest.TestCase):
    def test_normalize_runtime_state(self):
        self.assertEqual(runtime_state.normalize_runtime_state('idle'), 'idle')
        self.assertEqual(runtime_state.normalize_runtime_state('BUSY'), 'busy')
        self.assertEqual(runtime_state.normalize_runtime_state('weird'), 'unknown')

    def test_parse_elapsed_seconds(self):
        self.assertEqual(runtime_state.parse_elapsed_seconds('[⏱ 5m 7s]'), 307)
        self.assertEqual(runtime_state.parse_elapsed_seconds('[⏳ 42s]'), 42)
        self.assertEqual(runtime_state.parse_elapsed_seconds('elapsed 3.9s'), 3)
        self.assertIsNone(runtime_state.parse_elapsed_seconds('no timer'))

    def test_detect_error_reason(self):
        self.assertEqual(runtime_state.detect_error_reason('Error 522 Cloudflare Ray ID'), 'cloudflare_522')
        self.assertEqual(runtime_state.detect_error_reason('API Error: 400 unknown provider'), 'unknown_provider')
        self.assertEqual(runtime_state.detect_error_reason('connection refused'), 'connection_refused')
        self.assertIsNone(runtime_state.detect_error_reason('timeout/cancel/unwind 成功率与耗尽计数'))
        self.assertIsNone(runtime_state.detect_error_reason('timeout/cancel/unwind 成功率与耗尽计数\nfailure modes'))
        self.assertIsNone(runtime_state.detect_error_reason('all good'))

    def test_unknown_when_session_not_running(self):
        state = runtime_state.evaluate_runtime_state(output='', session_running=False)
        self.assertEqual(state.get('state'), 'unknown')
        self.assertEqual(state.get('reason'), 'session_not_running')

    def test_unknown_when_output_unreadable(self):
        state = runtime_state.evaluate_runtime_state(output='', output_readable=False)
        self.assertEqual(state.get('state'), 'unknown')
        self.assertEqual(state.get('reason'), 'unreadable_output')

    def test_blocked_has_priority(self):
        cfg = {
            'busy_patterns': ['Thinking...'],
            'blocked_patterns': ['requires approval'],
            'stuck_after_seconds': 180,
        }
        state = runtime_state.evaluate_runtime_state(
            output='Thinking... action requires approval',
            runtime_config=cfg,
            elapsed_seconds=999,
            error_reason='timeout',
        )
        self.assertEqual(state.get('state'), 'blocked')
        self.assertIn('blocked_pattern:', str(state.get('reason')))

    def test_busy_and_stuck_transitions(self):
        cfg = {
            'busy_patterns': ['Thinking...'],
            'blocked_patterns': ['requires approval'],
            'stuck_after_seconds': 120,
        }
        busy = runtime_state.evaluate_runtime_state(
            output='Thinking...',
            runtime_config=cfg,
            elapsed_seconds=119,
        )
        self.assertEqual(busy.get('state'), 'busy')

        stuck = runtime_state.evaluate_runtime_state(
            output='Thinking...',
            runtime_config=cfg,
            elapsed_seconds=120,
        )
        self.assertEqual(stuck.get('state'), 'stuck')
        self.assertEqual(stuck.get('reason'), 'busy_elapsed>=120')

    def test_error_when_not_busy_or_blocked(self):
        cfg = {
            'busy_patterns': ['Thinking...'],
            'blocked_patterns': ['requires approval'],
            'stuck_after_seconds': 180,
        }
        state = runtime_state.evaluate_runtime_state(
            output='Last request failed',
            runtime_config=cfg,
            error_reason='http_500',
        )
        self.assertEqual(state.get('state'), 'error')
        self.assertEqual(state.get('reason'), 'http_500')

    def test_idle_and_empty_output_boundaries(self):
        cfg = {
            'busy_patterns': ['Thinking...'],
            'blocked_patterns': ['requires approval'],
            'stuck_after_seconds': 180,
        }
        idle = runtime_state.evaluate_runtime_state(
            output='Ready for input',
            runtime_config=cfg,
        )
        self.assertEqual(idle.get('state'), 'idle')

        unknown = runtime_state.evaluate_runtime_state(
            output='   ',
            runtime_config=cfg,
        )
        self.assertEqual(unknown.get('state'), 'unknown')
        self.assertEqual(unknown.get('reason'), 'empty_output')

    def test_forced_state_path(self):
        state = runtime_state.evaluate_runtime_state(
            output='anything',
            force_state='blocked',
            force_reason='manual_override',
        )
        self.assertEqual(state.get('state'), 'blocked')
        self.assertEqual(state.get('reason'), 'manual_override')


if __name__ == '__main__':
    unittest.main()
