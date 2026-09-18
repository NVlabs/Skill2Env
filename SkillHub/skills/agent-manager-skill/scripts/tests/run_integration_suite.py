#!/usr/bin/env python3

from __future__ import annotations
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def run_unittest_attempt(pattern: str, output_file: Path) -> int:
    command = [
        sys.executable,
        '-m',
        'unittest',
        'discover',
        '-s',
        'agent-manager/scripts/tests',
        '-p',
        pattern,
        '-v',
    ]

    completed = subprocess.run(command, capture_output=True, text=True)
    command_text = ' '.join(command)
    output_file.write_text(
        (
            f"$ {command_text}\n\n"
            f"exit_code: {completed.returncode}\n\n"
            f"--- stdout ---\n{completed.stdout}\n"
            f"--- stderr ---\n{completed.stderr}\n"
        ),
        encoding='utf-8',
    )
    return completed.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description='Run integration tests with flaky-control retries.')
    parser.add_argument('--pattern', default='test_integration_*.py', help='unittest file pattern')
    parser.add_argument('--attempts', type=int, default=2, help='max attempts before failing')
    parser.add_argument('--artifact-dir', default='.artifacts/integration', help='artifact output directory')
    args = parser.parse_args()

    attempts = max(1, int(args.attempts))
    artifact_dir = Path(args.artifact_dir)
    artifact_dir.mkdir(parents=True, exist_ok=True)

    summary = {
        'pattern': args.pattern,
        'attempts': attempts,
        'started_at': datetime.now(timezone.utc).isoformat(),
        'results': [],
    }

    for attempt in range(1, attempts + 1):
        log_file = artifact_dir / f'attempt-{attempt}.log'
        print(f"[integration] attempt {attempt}/{attempts} -> {log_file}")
        rc = run_unittest_attempt(args.pattern, log_file)
        summary['results'].append({'attempt': attempt, 'return_code': rc, 'log_file': str(log_file)})

        if rc == 0:
            summary['status'] = 'pass'
            summary['finished_at'] = datetime.now(timezone.utc).isoformat()
            (artifact_dir / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
            print('[integration] PASS')
            return 0

        print(f"[integration] attempt {attempt} failed")

    summary['status'] = 'fail'
    summary['finished_at'] = datetime.now(timezone.utc).isoformat()
    (artifact_dir / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print('[integration] FAIL')
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
