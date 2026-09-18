from __future__ import annotations

import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from services.inbound_queue import append_inbound_message_event  # noqa: E402
from services.inbound_queue import canonical_inbound_state  # noqa: E402
from services.inbound_queue import classify_inbound_replay_state  # noqa: E402
from services.inbound_queue import enqueue_inbound_message  # noqa: E402
from services.inbound_queue import load_pending_inbound_messages  # noqa: E402
from services.inbound_queue import load_replayable_inbound_messages  # noqa: E402


class InboundQueueStateMachineTests(unittest.TestCase):
    def test_canonical_state_maps_legacy_dispatch_failed(self):
        self.assertEqual(canonical_inbound_state('dispatch_failed'), 'failed')
        self.assertEqual(canonical_inbound_state('failed'), 'failed')

    def test_load_pending_normalizes_legacy_dispatch_failed_events(self):
        temp_root = Path(tempfile.mkdtemp(prefix='agent-manager-inbound-legacy-'))
        message_id = enqueue_inbound_message(
            temp_root,
            agent_id='main',
            source='send',
            message_kind='message',
            message='legacy failed payload',
        )
        append_inbound_message_event(
            temp_root,
            agent_id='main',
            message_id=message_id,
            event='dispatch_failed',
            state='dispatch_failed',
            detail='legacy_failure',
            attempt_count=1,
        )

        pending = load_pending_inbound_messages(temp_root, agent_id='main')
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0].get('state'), 'failed')
        self.assertEqual(pending[0].get('attempt_count'), 1)

    def test_load_replayable_filters_by_backoff_and_stale_claim(self):
        temp_root = Path(tempfile.mkdtemp(prefix='agent-manager-inbound-replayable-'))
        now = datetime(2026, 3, 18, 12, 0, 0, tzinfo=timezone.utc)

        queued_id = enqueue_inbound_message(
            temp_root,
            agent_id='main',
            source='send',
            message_kind='message',
            message='queued payload',
        )
        self.assertTrue(queued_id)

        failed_due_id = enqueue_inbound_message(
            temp_root,
            agent_id='main',
            source='send',
            message_kind='message',
            message='failed due payload',
        )
        append_inbound_message_event(
            temp_root,
            agent_id='main',
            message_id=failed_due_id,
            event='failed',
            state='failed',
            detail='retry_due',
            attempt_count=1,
            next_retry_at=(now - timedelta(seconds=5)).isoformat().replace('+00:00', 'Z'),
        )

        failed_wait_id = enqueue_inbound_message(
            temp_root,
            agent_id='main',
            source='send',
            message_kind='message',
            message='failed waiting payload',
        )
        append_inbound_message_event(
            temp_root,
            agent_id='main',
            message_id=failed_wait_id,
            event='failed',
            state='failed',
            detail='retry_waiting',
            attempt_count=1,
            next_retry_at=(now + timedelta(minutes=5)).isoformat().replace('+00:00', 'Z'),
        )

        claimed_stale_id = enqueue_inbound_message(
            temp_root,
            agent_id='main',
            source='assign',
            message_kind='task_assignment',
            message='claimed stale payload',
        )
        append_inbound_message_event(
            temp_root,
            agent_id='main',
            message_id=claimed_stale_id,
            event='claimed',
            state='claimed',
            detail='claimed_stale',
            attempt_count=1,
            claimed_at=(now - timedelta(minutes=10)).isoformat().replace('+00:00', 'Z'),
        )

        replayable = load_replayable_inbound_messages(
            temp_root,
            agent_id='main',
            now=now,
            max_attempts=3,
            dispatch_lease_seconds=300,
        )
        replayable_ids = {payload.get('message_id') for payload in replayable}
        self.assertEqual(replayable_ids, {queued_id, failed_due_id, claimed_stale_id})
        self.assertNotIn(failed_wait_id, replayable_ids)

    def test_classify_inbound_replay_state_marks_attempt_limit_dead_letter(self):
        payload = {
            'state': 'failed',
            'attempt_count': 3,
        }
        decision = classify_inbound_replay_state(payload, max_attempts=3)
        self.assertEqual(decision, 'dead_letter')


if __name__ == '__main__':
    unittest.main()
