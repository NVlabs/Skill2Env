from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Optional


def _utc_now_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat().replace('+00:00', 'Z')


def parse_iso8601_utc(value: object) -> Optional[datetime]:
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


def dream_state_file(repo_root: Path, agent_id: str) -> Path:
    safe_agent_id = str(agent_id or 'unknown').strip().lower() or 'unknown'
    return repo_root / '.claude' / 'state' / 'agent-manager' / 'dream-state' / f'{safe_agent_id}.json'


def dream_audit_file(repo_root: Path, agent_id: str) -> Path:
    safe_agent_id = str(agent_id or 'unknown').strip().lower() or 'unknown'
    return repo_root / '.claude' / 'state' / 'agent-manager' / 'dream-audit' / f'{safe_agent_id}.jsonl'


def _default_state(agent_id: str) -> dict[str, Any]:
    return {
        'agent_id': str(agent_id),
        'window_id': '',
        'window_started_at': '',
        'window_started_by_hb_id': '',
        'last_heartbeat_at': '',
        'last_heartbeat_hb_id': '',
        'last_direct_ok_at': '',
        'last_direct_ok_hb_id': '',
        'triggered_for_window': False,
        'triggered_at': '',
        'triggered_by_hb_id': '',
        'last_reset_reason': '',
        'last_dream_id': '',
        'last_dream_timer_id': '',
    }


def load_dream_state(repo_root: Path, agent_id: str) -> dict[str, Any]:
    path = dream_state_file(repo_root, agent_id)
    state = _default_state(agent_id)
    if not path.exists():
        return state
    try:
        payload = json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return state
    if not isinstance(payload, dict):
        return state
    state.update(payload)
    state['agent_id'] = str(agent_id)
    return state


def save_dream_state(repo_root: Path, agent_id: str, state: dict[str, Any]) -> Path:
    path = dream_state_file(repo_root, agent_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = _default_state(agent_id)
    payload.update(state or {})
    payload['agent_id'] = str(agent_id)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return path


def append_dream_audit_event(
    repo_root: Path,
    *,
    agent_id: str,
    event: str,
    window_id: str = '',
    hb_id: str = '',
    dream_id: str = '',
    reason_code: str = '',
    detail: str = '',
    timer_id: str = '',
    effective_idle_elapsed: Optional[int] = None,
) -> Path:
    path = dream_audit_file(repo_root, agent_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        'timestamp': _utc_now_iso(),
        'agent_id': str(agent_id),
        'event': str(event or ''),
        'window_id': str(window_id or ''),
        'hb_id': str(hb_id or ''),
        'dream_id': str(dream_id or ''),
        'reason_code': str(reason_code or ''),
        'detail': str(detail or ''),
        'timer_id': str(timer_id or ''),
    }
    if isinstance(effective_idle_elapsed, int):
        payload['effective_idle_elapsed'] = max(0, int(effective_idle_elapsed))
    with path.open('a', encoding='utf-8') as fp:
        fp.write(json.dumps(payload, ensure_ascii=False) + '\n')
    return path


def process_heartbeat_for_dream(
    *,
    state: dict[str, Any],
    agent_id: str,
    heartbeat_id: str,
    heartbeat_timestamp: str,
    ack_status: str,
    ack_evidence: str,
    failure_type: str,
    idle_after_seconds: int,
    configured_heartbeat_interval_seconds: Optional[int] = None,
) -> dict[str, Any]:
    direct_ok = str(ack_status or '') == 'ack' and str(ack_evidence or '') == 'direct_heartbeat_ok'
    next_state = _default_state(agent_id)
    next_state.update(state or {})
    next_state['agent_id'] = str(agent_id)

    current_time = parse_iso8601_utc(heartbeat_timestamp)
    previous_hb_time = parse_iso8601_utc(next_state.get('last_heartbeat_at'))
    window_started_at = parse_iso8601_utc(next_state.get('window_started_at'))
    had_window = bool(next_state.get('window_id'))

    if direct_ok:
        if not had_window:
            next_state['window_id'] = f'dream-window-{heartbeat_id}'
            next_state['window_started_at'] = heartbeat_timestamp
            next_state['window_started_by_hb_id'] = heartbeat_id
            window_started_at = current_time
            window_event = 'window_started'
            window_reason = 'DREAM_WINDOW_STARTED'
        else:
            window_event = 'window_extended'
            window_reason = 'DREAM_WINDOW_EXTENDED'

        next_state['last_direct_ok_at'] = heartbeat_timestamp
        next_state['last_direct_ok_hb_id'] = heartbeat_id
        next_state['last_heartbeat_at'] = heartbeat_timestamp
        next_state['last_heartbeat_hb_id'] = heartbeat_id
        next_state['last_reset_reason'] = ''

        window_elapsed = 0
        interval_elapsed = 0
        if current_time and window_started_at:
            window_elapsed = max(0, int((current_time - window_started_at).total_seconds()))
        if current_time and previous_hb_time:
            interval_elapsed = max(0, int((current_time - previous_hb_time).total_seconds()))

        effective_idle_elapsed = max(
            window_elapsed,
            interval_elapsed,
            max(0, int(configured_heartbeat_interval_seconds or 0)),
        )
        should_trigger = effective_idle_elapsed >= max(1, int(idle_after_seconds)) and not bool(next_state.get('triggered_for_window'))
        return {
            'state': next_state,
            'event': window_event,
            'reason_code': window_reason,
            'should_trigger': should_trigger,
            'effective_idle_elapsed': effective_idle_elapsed,
        }

    next_state['window_id'] = ''
    next_state['window_started_at'] = ''
    next_state['window_started_by_hb_id'] = ''
    next_state['last_direct_ok_at'] = ''
    next_state['last_direct_ok_hb_id'] = ''
    next_state['triggered_for_window'] = False
    next_state['triggered_at'] = ''
    next_state['triggered_by_hb_id'] = ''
    next_state['last_heartbeat_at'] = heartbeat_timestamp
    next_state['last_heartbeat_hb_id'] = heartbeat_id
    next_state['last_reset_reason'] = str(failure_type or ack_status or ack_evidence or 'heartbeat_non_direct')

    return {
        'state': next_state,
        'event': 'window_reset' if had_window else '',
        'reason_code': 'DREAM_WINDOW_RESET' if had_window else '',
        'should_trigger': False,
        'effective_idle_elapsed': 0,
    }
