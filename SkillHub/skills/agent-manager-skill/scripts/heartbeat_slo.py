#!/usr/bin/env python3
"""Heartbeat SLO summary utilities and CLI."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

from agent_config import resolve_agent
from repo_root import get_repo_root

SUCCESS_RATE_MIN = 0.99
TIMEOUT_RATE_MAX = 0.02
RECOVERY_P95_MAX_MS = 120000


def _parse_iso8601_utc(value: object) -> Optional[datetime]:
    text = str(value or '').strip()
    if not text:
        return None

    normalized = text
    if normalized.endswith('Z'):
        normalized = normalized[:-1] + '+00:00'

    try:
        parsed = datetime.fromisoformat(normalized)
    except Exception:
        return None

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    else:
        parsed = parsed.astimezone(timezone.utc)
    return parsed


def _safe_agent_id(agent_value: str) -> str:
    safe = str(agent_value or 'unknown').strip().lower() or 'unknown'
    return ''.join(ch if ch.isalnum() or ch in {'_', '-'} else '-' for ch in safe)


def resolve_agent_id(agent_value: Optional[str]) -> Optional[str]:
    if not agent_value:
        return None

    raw = str(agent_value).strip()
    if not raw:
        return None

    resolved = resolve_agent(raw)
    if resolved:
        file_id = str(resolved.get('file_id', raw)).strip().lower()
        return file_id.replace('_', '-')

    normalized = raw.lower()
    if normalized.startswith('agent-'):
        normalized = normalized[len('agent-'):]
    return normalized.replace('_', '-')


def _audit_dir(repo_root: Path) -> Path:
    return repo_root / '.claude' / 'state' / 'agent-manager' / 'heartbeat-audit'


def load_heartbeat_events(
    *,
    repo_root: Path,
    agent_id: Optional[str] = None,
    since: Optional[datetime] = None,
    until: Optional[datetime] = None,
) -> list[dict]:
    audit_dir = _audit_dir(repo_root)
    if not audit_dir.exists() or not audit_dir.is_dir():
        return []

    files: list[Path]
    if agent_id:
        files = [audit_dir / f"{_safe_agent_id(agent_id)}.jsonl"]
    else:
        files = sorted(audit_dir.glob('*.jsonl'))

    events: list[dict] = []
    for file_path in files:
        if not file_path.exists() or not file_path.is_file():
            continue
        try:
            with file_path.open('r', encoding='utf-8') as file_obj:
                for line in file_obj:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        payload = json.loads(line)
                    except Exception:
                        continue
                    if not isinstance(payload, dict):
                        continue
                    if agent_id and str(payload.get('agent_id', '')).lower() != str(agent_id).lower():
                        continue

                    event_time = _parse_iso8601_utc(payload.get('timestamp'))
                    if since and (event_time is None or event_time < since):
                        continue
                    if until and (event_time is None or event_time > until):
                        continue
                    events.append(payload)
        except Exception:
            continue

    events.sort(key=lambda event: str(event.get('timestamp', '')))
    return events


def _failure_bucket(event: dict) -> str:
    failure_type = str(event.get('failure_type', '') or '').strip().lower()
    if failure_type:
        return failure_type

    send_status = str(event.get('send_status', '')).strip().lower()
    ack_status = str(event.get('ack_status', '')).strip().lower()

    if send_status != 'ok':
        return 'send_fail'
    if ack_status in {'timeout', 'blocked', 'no_ack'}:
        return ack_status
    if ack_status in {'ack', 'not_checked', ''}:
        return ''
    return 'unknown'


def _run_result(final_event: dict) -> str:
    result = str(final_event.get('result', '') or '').strip().lower()
    if result in {'success', 'failure', 'pending'}:
        return result

    bucket = _failure_bucket(final_event)
    if bucket:
        return 'failure'

    send_status = str(final_event.get('send_status', '')).strip().lower()
    ack_status = str(final_event.get('ack_status', '')).strip().lower()
    if send_status == 'ok' and ack_status == 'ack':
        return 'success'
    return 'pending'


def _percentile(values: list[int], percentile: float) -> int:
    if not values:
        return 0
    if percentile <= 0:
        return int(min(values))
    if percentile >= 100:
        return int(max(values))

    ordered = sorted(int(max(0, value)) for value in values)
    rank = (len(ordered) - 1) * (percentile / 100.0)
    lower = int(rank)
    upper = min(lower + 1, len(ordered) - 1)
    if lower == upper:
        return ordered[lower]

    lower_weight = upper - rank
    upper_weight = rank - lower
    return int(round(ordered[lower] * lower_weight + ordered[upper] * upper_weight))


def _default_window(window: str) -> tuple[datetime, datetime]:
    now = datetime.now(timezone.utc)
    normalized = str(window or 'daily').strip().lower()
    if normalized == 'weekly':
        return now - timedelta(days=7), now
    return now - timedelta(days=1), now


def _normalize_window(
    *,
    window: str,
    since: Optional[datetime],
    until: Optional[datetime],
) -> tuple[datetime, datetime, str]:
    normalized = str(window or 'daily').strip().lower()
    if normalized not in {'daily', 'weekly'}:
        raise ValueError(f"Unsupported window: {window}")

    default_since, default_until = _default_window(normalized)
    effective_since = since or default_since
    effective_until = until or default_until

    if effective_since > effective_until:
        raise ValueError('Invalid time range: since cannot be later than until')

    return effective_since, effective_until, normalized


def build_slo_summary(
    *,
    repo_root: Path,
    agent_id: Optional[str],
    window: str,
    since: Optional[datetime],
    until: Optional[datetime],
) -> dict:
    effective_since, effective_until, normalized_window = _normalize_window(
        window=window,
        since=since,
        until=until,
    )

    events = load_heartbeat_events(
        repo_root=repo_root,
        agent_id=agent_id,
        since=effective_since,
        until=effective_until,
    )

    runs: dict[tuple[str, str], list[dict]] = {}
    for event in events:
        hb_id = str(event.get('hb_id', '')).strip()
        event_agent = str(event.get('agent_id', '')).strip().lower()
        if not hb_id or not event_agent:
            continue
        key = (event_agent, hb_id)
        bucket = runs.setdefault(key, [])
        bucket.append(event)

    for group in runs.values():
        group.sort(key=lambda event: str(event.get('timestamp', '')))

    run_count = len(runs)
    success_runs = 0
    timeout_runs = 0
    recovery_spans: list[int] = []
    failure_buckets: dict[str, int] = {}

    for group in runs.values():
        final_event = group[-1]
        result = _run_result(final_event)
        if result == 'success':
            success_runs += 1

        bucket = _failure_bucket(final_event)
        if bucket:
            failure_buckets[bucket] = failure_buckets.get(bucket, 0) + 1
            if bucket == 'timeout':
                timeout_runs += 1

        if len(group) > 1 or any(str(event.get('recovery_action', '')).strip() for event in group):
            started = _parse_iso8601_utc(group[0].get('timestamp'))
            ended = _parse_iso8601_utc(group[-1].get('timestamp'))
            if started and ended and ended >= started:
                recovery_spans.append(int((ended - started).total_seconds() * 1000))
            else:
                summed_duration = sum(
                    int(max(0, int(event.get('duration_ms', 0) or 0)))
                    for event in group
                    if isinstance(event.get('duration_ms'), int)
                )
                if summed_duration > 0:
                    recovery_spans.append(summed_duration)

    success_rate = (success_runs / run_count) if run_count else 1.0
    timeout_rate = (timeout_runs / run_count) if run_count else 0.0

    recovery_p95 = _percentile(recovery_spans, 95)
    recovery_avg = int(sum(recovery_spans) / len(recovery_spans)) if recovery_spans else 0

    alerts = {
        'success_rate': {
            'status': 'ALERT' if success_rate < SUCCESS_RATE_MIN else 'OK',
            'threshold': f'>= {SUCCESS_RATE_MIN:.2%}',
            'value': f'{success_rate:.2%}',
        },
        'timeout_rate': {
            'status': 'ALERT' if timeout_rate > TIMEOUT_RATE_MAX else 'OK',
            'threshold': f'<= {TIMEOUT_RATE_MAX:.2%}',
            'value': f'{timeout_rate:.2%}',
        },
        'recovery_p95_ms': {
            'status': 'ALERT' if recovery_spans and recovery_p95 > RECOVERY_P95_MAX_MS else 'OK',
            'threshold': f'<= {RECOVERY_P95_MAX_MS}ms',
            'value': f'{recovery_p95}ms',
        },
    }

    return {
        'window': normalized_window,
        'since': effective_since.isoformat().replace('+00:00', 'Z'),
        'until': effective_until.isoformat().replace('+00:00', 'Z'),
        'agent_id': agent_id,
        'events': len(events),
        'runs': run_count,
        'success_runs': success_runs,
        'timeout_runs': timeout_runs,
        'success_rate': success_rate,
        'timeout_rate': timeout_rate,
        'recovery_samples': len(recovery_spans),
        'recovery_avg_ms': recovery_avg,
        'recovery_p95_ms': recovery_p95,
        'failure_buckets': dict(sorted(failure_buckets.items())),
        'alerts': alerts,
    }


def format_slo_summary(summary: dict) -> str:
    lines = [
        '📈 Heartbeat SLO Summary',
        f"Window: {summary.get('window')} ({summary.get('since')} -> {summary.get('until')})",
    ]

    agent_id = summary.get('agent_id')
    if agent_id:
        lines.append(f"Agent: {agent_id}")

    lines.extend(
        [
            f"Runs: {summary.get('runs', 0)} (events={summary.get('events', 0)})",
            f"Success: {summary.get('success_runs', 0)} ({summary.get('success_rate', 0.0):.2%})",
            f"Timeout: {summary.get('timeout_runs', 0)} ({summary.get('timeout_rate', 0.0):.2%})",
            (
                f"Recovery: samples={summary.get('recovery_samples', 0)} "
                f"avg={summary.get('recovery_avg_ms', 0)}ms "
                f"p95={summary.get('recovery_p95_ms', 0)}ms"
            ),
            '',
            'Failure buckets:',
        ]
    )

    buckets = summary.get('failure_buckets') or {}
    if buckets:
        for key, value in buckets.items():
            lines.append(f"- {key}: {value}")
    else:
        lines.append('- (none)')

    lines.append('')
    lines.append('Alerts:')
    alerts = summary.get('alerts') or {}
    for key in ['success_rate', 'timeout_rate', 'recovery_p95_ms']:
        alert = alerts.get(key, {})
        lines.append(
            f"- {key}: {alert.get('status', 'OK')} "
            f"(value={alert.get('value', 'n/a')}, threshold={alert.get('threshold', 'n/a')})"
        )

    return '\n'.join(lines)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Heartbeat SLO summary')
    parser.add_argument('--agent', help='Filter by agent name/file ID/agent-id')
    parser.add_argument('--window', choices=['daily', 'weekly'], default='daily', help='Preset time window')
    parser.add_argument('--since', help='Override start time (ISO-8601)')
    parser.add_argument('--until', help='Override end time (ISO-8601)')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = create_parser().parse_args(argv)

    since = _parse_iso8601_utc(getattr(args, 'since', None))
    until = _parse_iso8601_utc(getattr(args, 'until', None))
    if args.since and since is None:
        print(f"❌ Invalid --since timestamp: {args.since}")
        return 1
    if args.until and until is None:
        print(f"❌ Invalid --until timestamp: {args.until}")
        return 1

    try:
        summary = build_slo_summary(
            repo_root=get_repo_root(),
            agent_id=resolve_agent_id(getattr(args, 'agent', None)),
            window=getattr(args, 'window', 'daily'),
            since=since,
            until=until,
        )
    except ValueError as exc:
        print(f"❌ {exc}")
        return 1

    if getattr(args, 'json', False):
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(format_slo_summary(summary))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
