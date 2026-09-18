from __future__ import annotations
import argparse
import sys
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from services.heartbeat_service import parse_heartbeat_recovery_policy  # noqa: E402
from services.heartbeat_state_machine import (  # noqa: E402
    classify_heartbeat_ack,
    failure_reason_code,
    should_retry_heartbeat_attempt,
)


class HeartbeatServiceizationTests(unittest.TestCase):
    def test_parse_recovery_policy_service_defaults(self):
        policy = parse_heartbeat_recovery_policy({'enabled': True}, fallback_modes={'none', 'fresh'})
        self.assertEqual(policy['max_retries'], 1)
        self.assertEqual(policy['retry_backoff_seconds'], 3)
        self.assertEqual(policy['fallback_mode'], 'fresh')

    def test_parse_recovery_policy_normalizes_restart_and_blank_channel(self):
        heartbeat = {
            'enabled': True,
            'recovery': {
                'max_retries': -1,
                'retry_backoff_seconds': -2,
                'fallback_mode': 'restart',
                'notify_on_failure': 'yes',
                'notifier_channel': '   ',
            },
        }
        policy = parse_heartbeat_recovery_policy(heartbeat, fallback_modes={'none', 'fresh'})
        self.assertEqual(policy['max_retries'], 0)
        self.assertEqual(policy['retry_backoff_seconds'], 0)
        self.assertEqual(policy['fallback_mode'], 'fresh')
        self.assertTrue(policy['notify_on_failure'])
        self.assertEqual(policy['notifier_channel'], 'all')

    def test_parse_recovery_policy_accepts_cli_overrides(self):
        args = argparse.Namespace(
            retry=2,
            backoff_seconds=1,
            fallback_mode='none',
            notify_on_failure='true',
            notifier_channel='ops',
        )
        policy = parse_heartbeat_recovery_policy({'enabled': True}, args=args, fallback_modes={'none', 'fresh'})
        self.assertEqual(policy['max_retries'], 2)
        self.assertEqual(policy['retry_backoff_seconds'], 1)
        self.assertEqual(policy['fallback_mode'], 'none')
        self.assertTrue(policy['notify_on_failure'])
        self.assertEqual(policy['notifier_channel'], 'ops')

    def test_state_machine_ack_reason_code(self):
        ack, failure, reason = classify_heartbeat_ack(waited_for_ack=True, last_state='busy', timed_out=True)
        self.assertEqual((ack, failure, reason), ('timeout', 'timeout', 'HB_ACK_TIMEOUT'))

    def test_state_machine_no_ack_reason_code(self):
        ack, failure, reason = classify_heartbeat_ack(waited_for_ack=True, last_state='busy', timed_out=False)
        self.assertEqual((ack, failure, reason), ('no_ack', 'no_ack', 'HB_NO_ACK'))

    def test_failure_reason_code_mapping(self):
        self.assertEqual(failure_reason_code(failure_type='send_fail'), 'HB_SEND_FAIL')
        self.assertEqual(failure_reason_code(failure_type='blocked'), 'HB_AGENT_BLOCKED')
        self.assertEqual(failure_reason_code(failure_type='timeout'), 'HB_ACK_TIMEOUT')
        self.assertEqual(failure_reason_code(failure_type='no_ack'), 'HB_NO_ACK')
        self.assertEqual(failure_reason_code(failure_type='unknown'), 'HB_UNKNOWN')

    def test_should_retry_uses_state_machine_rules(self):
        self.assertTrue(should_retry_heartbeat_attempt(failure_type='no_ack', attempt_index=0, max_retries=1))
        self.assertFalse(should_retry_heartbeat_attempt(failure_type='unknown', attempt_index=0, max_retries=1))


if __name__ == '__main__':
    unittest.main()
