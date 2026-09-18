from __future__ import annotations
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import main  # noqa: E402


class HeartbeatTraceTests(unittest.TestCase):
    def setUp(self):
        self.temp_root = Path(tempfile.mkdtemp(prefix='hb-trace-tests-'))

    def tearDown(self):
        shutil.rmtree(self.temp_root, ignore_errors=True)

    def test_append_and_read_audit_events(self):
        main._append_heartbeat_audit_event(
            self.temp_root,
            agent_id='emp-0001',
            heartbeat_id='20260209-120001',
            send_status='ok',
            ack_status='ack',
            duration_ms=1200,
            context_left=62,
            failure_type='',
            session_mode='auto',
            timestamp='2026-02-09T12:00:01Z',
        )
        main._append_heartbeat_audit_event(
            self.temp_root,
            agent_id='emp-0001',
            heartbeat_id='20260209-120002',
            send_status='ok',
            ack_status='timeout',
            duration_ms=3100,
            context_left=18,
            failure_type='timeout',
            session_mode='auto',
            timestamp='2026-02-09T12:00:02Z',
        )

        events = main._read_heartbeat_audit_events(self.temp_root, agent_id='emp-0001', limit=10)
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0]['hb_id'], '20260209-120002')
        self.assertEqual(events[1]['hb_id'], '20260209-120001')

        by_hb = main._read_heartbeat_audit_events(self.temp_root, heartbeat_id='20260209-120001', limit=10)
        self.assertEqual(len(by_hb), 1)
        self.assertEqual(by_hb[0]['ack_status'], 'ack')

    def test_trace_limit_is_bounded(self):
        for index in range(12):
            main._append_heartbeat_audit_event(
                self.temp_root,
                agent_id='emp-0002',
                heartbeat_id=f'20260209-1200{index:02d}',
                send_status='ok',
                ack_status='ack',
                duration_ms=10,
                context_left=50,
                timestamp=f'2026-02-09T12:00:{index:02d}Z',
            )

        events = main._read_heartbeat_audit_events(self.temp_root, agent_id='emp-0002', limit=5)
        self.assertEqual(len(events), 5)

    def test_read_filters_since_until(self):
        main._append_heartbeat_audit_event(
            self.temp_root,
            agent_id='emp-0005',
            heartbeat_id='hb-1',
            send_status='ok',
            ack_status='ack',
            duration_ms=50,
            context_left=80,
            timestamp='2026-02-09T11:00:00Z',
        )
        main._append_heartbeat_audit_event(
            self.temp_root,
            agent_id='emp-0005',
            heartbeat_id='hb-2',
            send_status='ok',
            ack_status='ack',
            duration_ms=60,
            context_left=81,
            timestamp='2026-02-09T12:00:00Z',
        )

        since = main._parse_iso8601_utc('2026-02-09T11:30:00Z')
        until = main._parse_iso8601_utc('2026-02-09T12:00:00Z')
        events = main._read_heartbeat_audit_events(self.temp_root, agent_id='emp-0005', since=since, until=until, limit=10)

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]['hb_id'], 'hb-2')

    def test_classify_heartbeat_ack(self):
        self.assertEqual(main._classify_heartbeat_ack(last_state='idle', timed_out=False, waited_for_ack=True), ('ack', ''))
        self.assertEqual(main._classify_heartbeat_ack(last_state='blocked', timed_out=False, waited_for_ack=True), ('blocked', 'blocked'))
        self.assertEqual(main._classify_heartbeat_ack(last_state='busy', timed_out=True, waited_for_ack=True), ('timeout', 'timeout'))
        self.assertEqual(main._classify_heartbeat_ack(last_state='busy', timed_out=False, waited_for_ack=True), ('no_ack', 'no_ack'))
        self.assertEqual(main._classify_heartbeat_ack(last_state=None, timed_out=False, waited_for_ack=False), ('not_checked', ''))

    def test_read_skips_invalid_lines(self):
        audit_file = main._heartbeat_audit_file(self.temp_root, 'emp-0003')
        audit_file.parent.mkdir(parents=True, exist_ok=True)
        audit_file.write_text(
            '{"timestamp":"2026-02-09T12:00:00Z","agent_id":"emp-0003","hb_id":"h1","send_status":"ok","ack_status":"ack","duration_ms":100,"context_left":10,"failure_type":"","session_mode":"restore"}\n'
            'not-json\n'
            '[]\n',
            encoding='utf-8',
        )

        events = main._read_heartbeat_audit_events(self.temp_root, agent_id='emp-0003', limit=10)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]['hb_id'], 'h1')

    def test_json_payload_shape(self):
        main._append_heartbeat_audit_event(
            self.temp_root,
            agent_id='emp-0004',
            heartbeat_id='hb-shape',
            send_status='ok',
            ack_status='not_checked',
            duration_ms=0,
            context_left=None,
            session_mode='restore',
            timestamp='2026-02-09T12:00:00Z',
        )
        audit_file = main._heartbeat_audit_file(self.temp_root, 'emp-0004')
        row = audit_file.read_text(encoding='utf-8').strip()
        payload = json.loads(row)
        self.assertEqual(payload['agent_id'], 'emp-0004')
        self.assertEqual(payload['hb_id'], 'hb-shape')
        self.assertIn('duration_ms', payload)
        self.assertIn('reason_code', payload)
        self.assertIn('duration', payload)
        self.assertIn('stage', payload)
        self.assertIn('result', payload)
        self.assertIn('reason_code', payload)


if __name__ == '__main__':
    unittest.main()
