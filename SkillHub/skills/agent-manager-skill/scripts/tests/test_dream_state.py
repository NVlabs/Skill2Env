from __future__ import annotations

import sys
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from services.dream_state import process_heartbeat_for_dream  # noqa: E402


class DreamStateTests(unittest.TestCase):
    def test_direct_ok_starts_window(self):
        result = process_heartbeat_for_dream(
            state={},
            agent_id='main',
            heartbeat_id='HB-1',
            heartbeat_timestamp='2026-04-05T12:00:00Z',
            ack_status='ack',
            ack_evidence='direct_heartbeat_ok',
            failure_type='',
            idle_after_seconds=3600,
            configured_heartbeat_interval_seconds=600,
        )

        self.assertEqual(result['event'], 'window_started')
        self.assertFalse(result['should_trigger'])
        self.assertEqual(result['state']['window_id'], 'dream-window-HB-1')
        self.assertEqual(result['state']['last_direct_ok_hb_id'], 'HB-1')

    def test_large_heartbeat_interval_can_trigger_on_first_direct_ok(self):
        result = process_heartbeat_for_dream(
            state={},
            agent_id='main',
            heartbeat_id='HB-1',
            heartbeat_timestamp='2026-04-05T12:00:00Z',
            ack_status='ack',
            ack_evidence='direct_heartbeat_ok',
            failure_type='',
            idle_after_seconds=3600,
            configured_heartbeat_interval_seconds=4 * 3600,
        )

        self.assertTrue(result['should_trigger'])
        self.assertEqual(result['effective_idle_elapsed'], 4 * 3600)

    def test_non_direct_ok_resets_window(self):
        result = process_heartbeat_for_dream(
            state={
                'window_id': 'dream-window-HB-1',
                'window_started_at': '2026-04-05T11:00:00Z',
                'triggered_for_window': True,
            },
            agent_id='main',
            heartbeat_id='HB-2',
            heartbeat_timestamp='2026-04-05T12:00:00Z',
            ack_status='not_checked',
            ack_evidence='none',
            failure_type='busy_skip',
            idle_after_seconds=3600,
        )

        self.assertEqual(result['event'], 'window_reset')
        self.assertFalse(result['should_trigger'])
        self.assertEqual(result['state']['window_id'], '')
        self.assertFalse(result['state']['triggered_for_window'])
        self.assertEqual(result['state']['last_reset_reason'], 'busy_skip')

    def test_triggered_window_does_not_retrigger(self):
        result = process_heartbeat_for_dream(
            state={
                'window_id': 'dream-window-HB-1',
                'window_started_at': '2026-04-05T11:00:00Z',
                'last_heartbeat_at': '2026-04-05T11:30:00Z',
                'triggered_for_window': True,
            },
            agent_id='main',
            heartbeat_id='HB-2',
            heartbeat_timestamp='2026-04-05T12:00:00Z',
            ack_status='ack',
            ack_evidence='direct_heartbeat_ok',
            failure_type='',
            idle_after_seconds=1800,
            configured_heartbeat_interval_seconds=600,
        )

        self.assertEqual(result['event'], 'window_extended')
        self.assertFalse(result['should_trigger'])


if __name__ == '__main__':
    unittest.main()
