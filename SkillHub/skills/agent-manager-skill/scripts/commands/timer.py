from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _timer_state_dir(repo_root: Path) -> Path:
    return repo_root / '.claude' / 'state' / 'agent-manager' / 'timers'


def _timer_log_dir(repo_root: Path) -> Path:
    return repo_root / '.crontab_logs'


def _timer_worker_script() -> Path:
    return Path(__file__).resolve().parents[1] / 'timer_worker.py'


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding='utf-8')


def _read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding='utf-8'))


def _find_existing_timer(*, repo_root: Path, kind: str, dedupe_key: str) -> dict[str, object] | None:
    if not dedupe_key:
        return None

    timer_dir = _timer_state_dir(repo_root)
    if not timer_dir.exists():
        return None

    for timer_file in sorted(timer_dir.glob('*.json')):
        try:
            payload = _read_json(timer_file)
        except Exception:
            continue
        if str(payload.get('kind') or '') != kind:
            continue
        if str(payload.get('dedupe_key') or '') != dedupe_key:
            continue
        if str(payload.get('status') or '') not in {'pending', 'running'}:
            continue
        return payload
    return None


def _schedule_worker(*, repo_root: Path, timer_file: Path, log_file: Path) -> int:
    worker_script = _timer_worker_script()
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with log_file.open('a', encoding='utf-8') as handle:
        proc = subprocess.Popen(
            [sys.executable, str(worker_script), '--timer-file', str(timer_file)],
            cwd=str(repo_root),
            stdout=handle,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            text=True,
        )
    return int(proc.pid)


def _create_timer_id(kind: str) -> str:
    safe_kind = ''.join(ch for ch in str(kind or 'timer').lower() if ch.isalnum() or ch in ('-', '_')) or 'timer'
    return f"{safe_kind}-{int(time.time() * 1000)}-{os.getpid()}"


def _format_ts(epoch_seconds: int) -> str:
    return datetime.fromtimestamp(epoch_seconds, tz=timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')


def _schedule_timer(*, args, deps: Any, kind: str, payload: dict[str, object]) -> int:
    delay_seconds = deps.parse_duration(args.delay)
    if not delay_seconds or delay_seconds <= 0:
        print("❌ Invalid delay; use values like 5s, 30s, 5m, 1h")
        return 1

    repo_root = deps.get_repo_root()
    dedupe_key = str(payload.get('dedupe_key') or '').strip()
    if dedupe_key:
        existing = _find_existing_timer(repo_root=repo_root, kind=kind, dedupe_key=dedupe_key)
        if existing is not None:
            print(f"⏱️  Timer already scheduled: {existing.get('timer_id')}")
            print(f"   Kind: {kind}")
            print(f"   Dedupe key: {dedupe_key}")
            return 0

    timer_id = _create_timer_id(kind)
    now = int(time.time())
    run_at = now + int(delay_seconds)
    timer_dir = _timer_state_dir(repo_root)
    timer_file = timer_dir / f'{timer_id}.json'
    log_file = _timer_log_dir(repo_root) / f'agent-manager-timer-{timer_id}.log'

    record = {
        'timer_id': timer_id,
        'kind': kind,
        'status': 'pending',
        'created_at_epoch': now,
        'run_at_epoch': run_at,
        'created_at': datetime.fromtimestamp(now, tz=timezone.utc).isoformat(),
        'run_at': datetime.fromtimestamp(run_at, tz=timezone.utc).isoformat(),
        'delay_seconds': int(delay_seconds),
        'repo_root': str(repo_root),
        'log_file': str(log_file),
        **payload,
    }
    _write_json(timer_file, record)
    pid = _schedule_worker(repo_root=repo_root, timer_file=timer_file, log_file=log_file)
    record['worker_pid'] = pid
    _write_json(timer_file, record)

    print(f"⏱️  Timer scheduled: {timer_id}")
    print(f"   Kind: {kind}")
    print(f"   Run at: {_format_ts(run_at)}")
    print(f"   Delay: {delay_seconds}s")
    print(f"   Worker PID: {pid}")
    print(f"   State: {timer_file}")
    print(f"   Log: {log_file}")
    return 0


def _list_timers(*, deps: Any, limit: int) -> int:
    repo_root = deps.get_repo_root()
    timer_dir = _timer_state_dir(repo_root)
    if not timer_dir.exists():
        print("No timers scheduled.")
        return 0

    records: list[dict[str, object]] = []
    for timer_file in sorted(timer_dir.glob('*.json')):
        try:
            records.append(_read_json(timer_file))
        except Exception:
            continue

    if not records:
        print("No timers scheduled.")
        return 0

    records.sort(key=lambda item: int(item.get('created_at_epoch', 0) or 0), reverse=True)
    if limit > 0:
        records = records[:limit]

    print("⏱️ Timers:")
    print()
    for record in records:
        timer_id = str(record.get('timer_id') or '')
        kind = str(record.get('kind') or 'unknown')
        status = str(record.get('status') or 'unknown')
        run_at_epoch = int(record.get('run_at_epoch', 0) or 0)
        print(f"- {timer_id}")
        print(f"  kind={kind} status={status} run_at={_format_ts(run_at_epoch) if run_at_epoch else 'unknown'}")
    return 0


def cmd_timer(args, *, deps: Any):
    """Handle timer subcommands."""
    if args.timer_command == 'list':
        return _list_timers(deps=deps, limit=int(args.limit))

    if args.timer_command == 'heartbeat':
        return _schedule_timer(
            args=args,
            deps=deps,
            kind='heartbeat',
            payload={
                'agent': args.agent,
                'timeout': str(args.timeout or '').strip(),
            },
        )

    if args.timer_command == 'rescue':
        return _schedule_timer(
            args=args,
            deps=deps,
            kind='rescue',
            payload={
                'agent': args.agent,
                'timeout': str(args.timeout or '').strip(),
                'prime': not bool(getattr(args, 'no_prime', False)),
                'fresh': bool(getattr(args, 'fresh', False)),
                'reason': str(getattr(args, 'reason', '') or '').strip(),
                'heartbeat_id': str(getattr(args, 'heartbeat_id', '') or '').strip(),
                'dedupe_key': str(getattr(args, 'dedupe_key', '') or '').strip(),
            },
        )

    if args.timer_command == 'command':
        command_args = list(args.command_args or [])
        if command_args and command_args[0] == '--':
            command_args = command_args[1:]
        if not command_args:
            print("❌ timer command requires an agent-manager command after '--'")
            return 1

        return _schedule_timer(
            args=args,
            deps=deps,
            kind='command',
            payload={
                'command_args': command_args,
            },
        )

    print(f"Unknown timer command: {args.timer_command}")
    return 1
