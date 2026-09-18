from __future__ import annotations
import shutil
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import heartbeat_slo  # noqa: E402
import main  # noqa: E402


class HeartbeatSloTests(unittest.TestCase):
    def setUp(self):
        self.temp_root = Path(tempfile.mkdtemp(prefix='hb-slo-tests-'))

    def tearDown(self):
        shutil.rmtree(self.temp_root, ignore_errors=True)

    def test_build_slo_summary_counts_success_and_timeout(self):
        main._append_heartbeat_audit_event(
            self.temp_root,
            agent_id='emp-0001',
            heartbeat_id='hb-a',
            send_status='ok',
            ack_status='ack',
            duration_ms=120,
            context_left=80,
            timestamp='2026-02-09T11:00:00Z',
        )
        main._append_heartbeat_audit_event(
            self.temp_root,
            agent_id='emp-0001',
            heartbeat_id='hb-b',
            send_status='ok',
            ack_status='timeout',
            duration_ms=300,
            context_left=22,
            failure_type='timeout',
            timestamp='2026-02-09T12:00:00Z',
        )

        summary = heartbeat_slo.build_slo_summary(
            repo_root=self.temp_root,
            agent_id='emp-0001',
            window='daily',
            since=datetime(2026, 2, 9, 0, 0, 0, tzinfo=timezone.utc),
            until=datetime(2026, 2, 10, 0, 0, 0, tzinfo=timezone.utc),
        )

        self.assertEqual(summary['runs'], 2)
        self.assertEqual(summary['success_runs'], 1)
        self.assertEqual(summary['timeout_runs'], 1)
        self.assertAlmostEqual(summary['success_rate'], 0.5)
        self.assertAlmostEqual(summary['timeout_rate'], 0.5)
        self.assertEqual(summary['failure_buckets'].get('timeout'), 1)
        self.assertEqual(summary['alerts']['success_rate']['status'], 'ALERT')
        self.assertEqual(summary['alerts']['timeout_rate']['status'], 'ALERT')

    def test_recovery_p95_uses_multi_attempt_runs(self):
        main._append_heartbeat_audit_event(
            self.temp_root,
            agent_id='emp-0002',
            heartbeat_id='hb-retry',
            send_status='ok',
            ack_status='timeout',
            duration_ms=15000,
            context_left=40,
            failure_type='timeout',
            attempt=1,
            timestamp='2026-02-09T12:00:00Z',
        )
        main._append_heartbeat_audit_event(
            self.temp_root,
            agent_id='emp-0002',
            heartbeat_id='hb-retry',
            send_status='ok',
            ack_status='ack',
            duration_ms=1000,
            context_left=39,
            attempt=2,
            recovery_action='retry',
            timestamp='2026-02-09T12:00:40Z',
        )

        summary = heartbeat_slo.build_slo_summary(
            repo_root=self.temp_root,
            agent_id='emp-0002',
            window='daily',
            since=datetime(2026, 2, 9, 0, 0, 0, tzinfo=timezone.utc),
            until=datetime(2026, 2, 10, 0, 0, 0, tzinfo=timezone.utc),
        )

        self.assertEqual(summary['runs'], 1)
        self.assertEqual(summary['success_runs'], 1)
        self.assertEqual(summary['recovery_samples'], 1)
        self.assertEqual(summary['recovery_p95_ms'], 40000)
        self.assertEqual(summary['alerts']['recovery_p95_ms']['status'], 'OK')

    def test_invalid_window_raises(self):
        with self.assertRaises(ValueError):
            heartbeat_slo.build_slo_summary(
                repo_root=self.temp_root,
                agent_id=None,
                window='monthly',
                since=None,
                until=None,
            )


if __name__ == '__main__':
    unittest.main()
