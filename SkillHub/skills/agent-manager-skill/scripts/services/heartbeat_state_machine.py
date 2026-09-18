from __future__ import annotations
from typing import Optional


RECOVERABLE_FAILURE_TYPES = {'send_fail', 'no_ack', 'no_activation', 'timeout', 'blocked'}


def failure_reason_code(*, failure_type: str, ack_status: str = '', send_status: str = '') -> str:
    failure = str(failure_type or '').strip().lower()
    if failure == 'interrupted':
        return 'HB_INTERRUPTED'
    if failure == 'send_fail':
        return 'HB_SEND_FAIL'
    if failure == 'blocked':
        return 'HB_AGENT_BLOCKED'
    if failure == 'timeout':
        return 'HB_ACK_TIMEOUT'
    if failure == 'no_ack':
        return 'HB_NO_ACK'
    if failure == 'no_activation':
        return 'HB_NO_ACTIVATION'

    ack = str(ack_status or '').strip().lower()
    if ack == 'blocked':
        return 'HB_AGENT_BLOCKED'
    if ack == 'timeout':
        return 'HB_ACK_TIMEOUT'
    if ack == 'no_ack':
        return 'HB_NO_ACK'

    send = str(send_status or '').strip().lower()
    if send == 'fail':
        return 'HB_SEND_FAIL'

    return 'HB_UNKNOWN'


def classify_heartbeat_ack(*, waited_for_ack: bool, last_state: Optional[str], timed_out: bool) -> tuple[str, str, str]:
    if not waited_for_ack:
        return 'not_checked', '', 'HB_NOT_CHECKED'

    state = str(last_state or '').strip().lower()
    if state == 'idle':
        return 'ack', '', 'HB_ACK_OK'
    if state == 'blocked':
        return 'blocked', 'blocked', 'HB_AGENT_BLOCKED'
    if timed_out:
        return 'timeout', 'timeout', 'HB_ACK_TIMEOUT'
    return 'no_ack', 'no_ack', 'HB_NO_ACK'


def should_retry_heartbeat_attempt(*, failure_type: str, attempt_index: int, max_retries: int) -> bool:
    if attempt_index >= max_retries:
        return False
    return str(failure_type or '').strip().lower() in RECOVERABLE_FAILURE_TYPES
