from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
import os
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional


_LEGACY_STATE_ALIASES = {'dispatch_failed': 'failed'}
_PENDING_STATES = {'queued', 'claimed', 'dispatching', 'failed'}
_RETRYABLE_STATES = {'queued', 'failed'}
_LEASED_STATES = {'claimed', 'dispatching'}


def canonical_inbound_state(state: object) -> str:
    text = str(state or '').strip()
    if not text:
        return ''
    return _LEGACY_STATE_ALIASES.get(text, text)


def _parse_utc_timestamp(value: object) -> Optional[datetime]:
    text = str(value or '').strip()
    if not text:
        return None

    normalized = text[:-1] + '+00:00' if text.endswith('Z') else text
    try:
        parsed = datetime.fromisoformat(normalized)
    except Exception:
        return None

    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def inbound_message_attempt_count(payload: Dict[str, Any]) -> int:
    try:
        return max(0, int(payload.get('attempt_count') or 0))
    except Exception:
        return 0


def _next_retry_due(payload: Dict[str, Any], *, now: datetime) -> bool:
    next_retry_at = _parse_utc_timestamp(payload.get('next_retry_at'))
    return next_retry_at is None or next_retry_at <= now


def _lease_expired(payload: Dict[str, Any], *, now: datetime, dispatch_lease_seconds: int) -> bool:
    lease_anchor = (
        _parse_utc_timestamp(payload.get('claimed_at'))
        or _parse_utc_timestamp(payload.get('dispatching_at'))
        or _parse_utc_timestamp(payload.get('timestamp'))
    )
    if lease_anchor is None:
        return True
    return now >= lease_anchor + timedelta(seconds=max(1, int(dispatch_lease_seconds)))


def classify_inbound_replay_state(
    payload: Dict[str, Any],
    *,
    now: Optional[datetime] = None,
    max_attempts: int = 3,
    dispatch_lease_seconds: int = 300,
) -> str:
    current_time = now or datetime.now(timezone.utc)
    attempts = inbound_message_attempt_count(payload)
    if attempts >= max(1, int(max_attempts)):
        return 'dead_letter'

    state = canonical_inbound_state(payload.get('state'))
    if state in _RETRYABLE_STATES and _next_retry_due(payload, now=current_time):
        return 'replayable'
    if state in _LEASED_STATES and _lease_expired(payload, now=current_time, dispatch_lease_seconds=dispatch_lease_seconds):
        return 'replayable'
    if state in _PENDING_STATES:
        return 'pending'
    return 'terminal'


def _queue_file(repo_root: Path, agent_id: str) -> Path:
    return repo_root / '.claude' / 'state' / 'agent-manager' / 'inbound-queue' / f'{agent_id}.jsonl'


def _append_event(repo_root: Path, agent_id: str, payload: Dict[str, Any]) -> None:
    queue_file = _queue_file(repo_root, agent_id)
    queue_file.parent.mkdir(parents=True, exist_ok=True)
    with queue_file.open('a', encoding='utf-8') as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + "\n")
        fh.flush()
        os.fsync(fh.fileno())


def append_inbound_message_event(
    repo_root: Path,
    *,
    agent_id: str,
    message_id: str,
    event: str,
    state: Optional[str] = None,
    detail: str = "",
    **extra: Any,
) -> None:
    payload: Dict[str, Any] = {
        'message_id': str(message_id),
        'agent_id': str(agent_id),
        'event': str(event),
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
    }
    if state is not None:
        payload['state'] = str(state)
    if detail:
        payload['detail'] = str(detail)
    for key, value in extra.items():
        payload[str(key)] = value
    _append_event(repo_root, agent_id, payload)


def append_inbound_reply_closure(
    repo_root: Path,
    *,
    agent_id: str,
    message_id: str,
    detail: str,
    reply_evidence: str = 'repo_local',
    transport_ack_status: str = 'unverified',
    transport_ack_detail: str = '',
    **extra: Any,
) -> None:
    payload_extra: Dict[str, Any] = dict(extra)
    payload_extra['reply_evidence'] = str(reply_evidence or 'repo_local')
    payload_extra['transport_ack_status'] = str(transport_ack_status or 'unverified')
    if transport_ack_detail:
        payload_extra['transport_ack_detail'] = str(transport_ack_detail)

    append_inbound_message_event(
        repo_root,
        agent_id=agent_id,
        message_id=message_id,
        event='replied',
        state='replied',
        detail=detail,
        **payload_extra,
    )


def enqueue_inbound_message(
    repo_root: Path,
    *,
    agent_id: str,
    source: str,
    message_kind: str,
    message: str,
) -> str:
    message_id = f"msg-{int(time.time() * 1000)}-{uuid.uuid4().hex[:8]}"
    timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    base = {
        'message_id': message_id,
        'agent_id': str(agent_id),
        'source': str(source),
        'message_kind': str(message_kind),
        'message': str(message),
    }
    append_inbound_message_event(
        repo_root,
        agent_id=agent_id,
        message_id=message_id,
        event='received',
        state='received',
        source=source,
        message_kind=message_kind,
        message=message,
        received_at=timestamp,
    )
    append_inbound_message_event(
        repo_root,
        agent_id=agent_id,
        message_id=message_id,
        event='queued',
        state='queued',
        source=source,
        message_kind=message_kind,
        message=message,
    )
    return message_id


def mark_inbound_message_state(
    repo_root: Path,
    *,
    agent_id: str,
    message_id: str,
    state: str,
    detail: str = "",
    **extra: Any,
) -> None:
    append_inbound_message_event(
        repo_root,
        agent_id=agent_id,
        message_id=message_id,
        event=str(state),
        state=str(state),
        detail=detail,
        **extra,
    )


def read_inbound_events(
    repo_root: Path,
    *,
    agent_id: str,
    message_id: Optional[str] = None,
    limit: Optional[int] = None,
) -> List[Dict[str, Any]]:
    queue_file = _queue_file(repo_root, agent_id)
    if not queue_file.exists():
        return []

    events: List[Dict[str, Any]] = []
    with queue_file.open('r', encoding='utf-8') as fh:
        for raw_line in fh:
            line = raw_line.strip()
            if not line:
                continue
            try:
                payload = json.loads(line)
            except Exception:
                continue
            if not isinstance(payload, dict):
                continue
            if message_id and str(payload.get('message_id') or '') != str(message_id):
                continue
            events.append(payload)

    events.sort(key=lambda item: str(item.get('timestamp') or ''))
    if limit is not None:
        return events[-max(0, int(limit)) :]
    return events


def was_message_yielded(repo_root: Path, *, agent_id: str, message_id: str) -> bool:
    return any(
        str(event.get('event') or '') == 'yielded'
        for event in read_inbound_events(repo_root, agent_id=agent_id, message_id=message_id)
    )


def note_pending_messages_yielded(
    repo_root: Path,
    *,
    agent_id: str,
    heartbeat_id: str,
    reason_code: str,
    detail: str = "",
) -> List[str]:
    pending = load_pending_inbound_messages(repo_root, agent_id=agent_id)
    yielded_ids: List[str] = []
    for payload in pending:
        message_id = str(payload.get('message_id') or '').strip()
        if not message_id:
            continue
        append_inbound_message_event(
            repo_root,
            agent_id=agent_id,
            message_id=message_id,
            event='yielded',
            state=str(payload.get('state') or 'queued'),
            detail=detail,
            heartbeat_id=heartbeat_id,
            reason_code=reason_code,
        )
        yielded_ids.append(message_id)
    return yielded_ids


def load_pending_inbound_messages(repo_root: Path, *, agent_id: str) -> List[Dict[str, Any]]:
    latest: Dict[str, Dict[str, Any]] = {}
    for payload in read_inbound_events(repo_root, agent_id=agent_id):
        message_id = str(payload.get('message_id') or '').strip()
        if not message_id:
            continue
        current = latest.get(message_id, {})
        merged = dict(current)
        merged.update(payload)
        merged['state'] = canonical_inbound_state(merged.get('state'))
        latest[message_id] = merged

    pending = [payload for payload in latest.values() if str(payload.get('state') or '') in _PENDING_STATES]
    pending.sort(key=lambda item: str(item.get('timestamp') or ''))
    return pending


def load_replayable_inbound_messages(
    repo_root: Path,
    *,
    agent_id: str,
    now: Optional[datetime] = None,
    max_attempts: int = 3,
    dispatch_lease_seconds: int = 300,
) -> List[Dict[str, Any]]:
    current_time = now or datetime.now(timezone.utc)
    replayable = [
        payload
        for payload in load_pending_inbound_messages(repo_root, agent_id=agent_id)
        if classify_inbound_replay_state(
            payload,
            now=current_time,
            max_attempts=max_attempts,
            dispatch_lease_seconds=dispatch_lease_seconds,
        ) == 'replayable'
    ]
    replayable.sort(key=lambda item: str(item.get('timestamp') or ''))
    return replayable


def has_pending_inbound_messages(repo_root: Path, *, agent_id: str) -> bool:
    return bool(load_pending_inbound_messages(repo_root, agent_id=agent_id))
