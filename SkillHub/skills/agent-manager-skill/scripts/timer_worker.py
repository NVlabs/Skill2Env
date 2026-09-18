#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


def _read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding='utf-8'))


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding='utf-8')


def _utc_now_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def _main_script() -> Path:
    return Path(__file__).resolve().parent / 'main.py'


def _mark(path: Path, **updates: object) -> dict[str, object]:
    payload = _read_json(path)
    payload.update(updates)
    _write_json(path, payload)
    return payload


def _run_timer(timer_file: Path) -> int:
    payload = _read_json(timer_file)
    repo_root = Path(str(payload.get('repo_root') or Path.cwd())).resolve()
    run_at_epoch = int(payload.get('run_at_epoch', 0) or 0)
    timer_id = str(payload.get('timer_id') or timer_file.stem)
    kind = str(payload.get('kind') or 'unknown')
    sleep_seconds = max(0, run_at_epoch - int(time.time()))
    if sleep_seconds:
        time.sleep(sleep_seconds)

    payload = _read_json(timer_file)
    if str(payload.get('status') or 'pending') != 'pending':
        print(f"⏭️  Timer {timer_id} skipped: status={payload.get('status')}")
        return 0

    _mark(
        timer_file,
        status='running',
        started_at=_utc_now_iso(),
        worker_pid=os.getpid(),
    )

    main_script = _main_script()
    if kind == 'heartbeat':
        agent = str(payload.get('agent') or '').strip()
        timeout = str(payload.get('timeout') or '').strip()
        if not agent:
            _mark(timer_file, status='failed', finished_at=_utc_now_iso(), exit_code=1, error='missing_agent')
            return 1
        commands = [
            [sys.executable, str(main_script), 'start', agent, '--restore'],
            [sys.executable, str(main_script), 'heartbeat', 'run', agent] + (['--timeout', timeout] if timeout else []),
        ]
    elif kind == 'rescue':
        agent = str(payload.get('agent') or '').strip()
        timeout = str(payload.get('timeout') or '').strip()
        reason = str(payload.get('reason') or '').strip()
        heartbeat_id = str(payload.get('heartbeat_id') or '').strip()
        if not agent:
            _mark(timer_file, status='failed', finished_at=_utc_now_iso(), exit_code=1, error='missing_agent')
            return 1
        rescue_reason = " ".join(part for part in [reason, f"hb_id={heartbeat_id}" if heartbeat_id else ''] if part).strip()
        rescue_cmd = [sys.executable, str(main_script), 'heartbeat', 'rescue', agent]
        if timeout:
            rescue_cmd.extend(['--timeout', timeout])
        if rescue_reason:
            rescue_cmd.extend(['--reason', rescue_reason])
        if bool(payload.get('no_prime')) or not bool(payload.get('prime', True)):
            rescue_cmd.append('--no-prime')
        if bool(payload.get('fresh')):
            rescue_cmd.append('--fresh')
        commands = [rescue_cmd]
    elif kind == 'command':
        command_args = [str(item) for item in list(payload.get('command_args') or []) if str(item)]
        if not command_args:
            _mark(timer_file, status='failed', finished_at=_utc_now_iso(), exit_code=1, error='missing_command_args')
            return 1
        commands = [[sys.executable, str(main_script), *command_args]]
    else:
        _mark(timer_file, status='failed', finished_at=_utc_now_iso(), exit_code=1, error=f'unsupported_kind:{kind}')
        return 1

    exit_code = 0
    for cmd in commands:
        print(f"▶️  Running timer {timer_id}: {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd=str(repo_root))
        exit_code = int(result.returncode)
        if exit_code != 0:
            break

    final_status = 'completed' if exit_code == 0 else 'failed'
    _mark(
        timer_file,
        status=final_status,
        finished_at=_utc_now_iso(),
        exit_code=exit_code,
    )
    return exit_code


def main() -> int:
    parser = argparse.ArgumentParser(description='Run one agent-manager timer job')
    parser.add_argument('--timer-file', required=True, help='Path to the timer state file')
    args = parser.parse_args()
    return _run_timer(Path(args.timer_file).resolve())


if __name__ == '__main__':
    raise SystemExit(main())
