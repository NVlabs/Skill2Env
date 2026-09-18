from __future__ import annotations

import argparse
import io
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from commands.timer import cmd_timer  # noqa: E402


class TimerCommandTests(unittest.TestCase):
    def setUp(self):
        self.temp_root = Path(tempfile.mkdtemp(prefix='agent-manager-timer-'))

    def tearDown(self):
        shutil.rmtree(self.temp_root, ignore_errors=True)

    def _deps(self):
        return SimpleNamespace(
            get_repo_root=lambda: self.temp_root,
            parse_duration=lambda value: {'5s': 5, '10s': 10}.get(value),
        )

    def _run(self, args, *, deps=None):
        out = io.StringIO()
        with redirect_stdout(out):
            code = cmd_timer(args, deps=deps or self._deps())
        return code, out.getvalue()

    def test_timer_heartbeat_schedules_state_and_worker(self):
        args = argparse.Namespace(timer_command='heartbeat', agent='main', delay='5s', timeout='8m')
        with patch('commands.timer._schedule_worker', return_value=12345):
            code, text = self._run(args)

        self.assertEqual(code, 0)
        self.assertIn('Timer scheduled', text)
        timer_files = list((self.temp_root / '.claude' / 'state' / 'agent-manager' / 'timers').glob('*.json'))
        self.assertEqual(len(timer_files), 1)
        payload = json.loads(timer_files[0].read_text(encoding='utf-8'))
        self.assertEqual(payload['kind'], 'heartbeat')
        self.assertEqual(payload['agent'], 'main')
        self.assertEqual(payload['timeout'], '8m')
        self.assertEqual(payload['worker_pid'], 12345)

    def test_timer_rescue_schedules_state_and_worker(self):
        args = argparse.Namespace(
            timer_command='rescue',
            agent='main',
            delay='5s',
            timeout='8m',
            reason='stale pending',
            no_prime=False,
            fresh=False,
            heartbeat_id='20260326-010101',
            dedupe_key='pending-rescue:main:20260326-010101',
        )
        with patch('commands.timer._schedule_worker', return_value=12347):
            code, _text = self._run(args)

        self.assertEqual(code, 0)
        timer_files = list((self.temp_root / '.claude' / 'state' / 'agent-manager' / 'timers').glob('*.json'))
        payload = json.loads(timer_files[0].read_text(encoding='utf-8'))
        self.assertEqual(payload['kind'], 'rescue')
        self.assertEqual(payload['agent'], 'main')
        self.assertEqual(payload['timeout'], '8m')
        self.assertTrue(payload['prime'])
        self.assertEqual(payload['heartbeat_id'], '20260326-010101')
        self.assertEqual(payload['dedupe_key'], 'pending-rescue:main:20260326-010101')
        self.assertEqual(payload['worker_pid'], 12347)

    def test_timer_command_requires_command_args(self):
        args = argparse.Namespace(timer_command='command', delay='5s', command_args=['--'])
        code, text = self._run(args)
        self.assertEqual(code, 1)
        self.assertIn('requires an agent-manager command', text)

    def test_timer_command_schedules_remainder_args(self):
        args = argparse.Namespace(timer_command='command', delay='5s', command_args=['--', 'heartbeat', 'run', 'main', '--timeout', '8m'])
        with patch('commands.timer._schedule_worker', return_value=12346):
            code, _text = self._run(args)

        self.assertEqual(code, 0)
        timer_files = list((self.temp_root / '.claude' / 'state' / 'agent-manager' / 'timers').glob('*.json'))
        payload = json.loads(timer_files[0].read_text(encoding='utf-8'))
        self.assertEqual(payload['kind'], 'command')
        self.assertEqual(payload['command_args'], ['heartbeat', 'run', 'main', '--timeout', '8m'])

    def test_timer_rescue_dedupes_existing_pending_timer(self):
        timer_dir = self.temp_root / '.claude' / 'state' / 'agent-manager' / 'timers'
        timer_dir.mkdir(parents=True, exist_ok=True)
        (timer_dir / 'existing.json').write_text(json.dumps({
            'timer_id': 'timer-existing',
            'kind': 'rescue',
            'status': 'pending',
            'dedupe_key': 'pending-rescue:main:20260326-010101',
            'created_at_epoch': 1,
            'run_at_epoch': 2,
        }), encoding='utf-8')

        args = argparse.Namespace(
            timer_command='rescue',
            agent='main',
            delay='5s',
            timeout='8m',
            reason='stale pending',
            no_prime=False,
            fresh=False,
            heartbeat_id='20260326-010101',
            dedupe_key='pending-rescue:main:20260326-010101',
        )
        with patch('commands.timer._schedule_worker') as worker_mock:
            code, text = self._run(args)

        self.assertEqual(code, 0)
        self.assertIn('Timer already scheduled', text)
        worker_mock.assert_not_called()

    def test_timer_list_prints_recent_records(self):
        timer_dir = self.temp_root / '.claude' / 'state' / 'agent-manager' / 'timers'
        timer_dir.mkdir(parents=True, exist_ok=True)
        (timer_dir / 'a.json').write_text(json.dumps({
            'timer_id': 'timer-a',
            'kind': 'heartbeat',
            'status': 'pending',
            'created_at_epoch': 1,
            'run_at_epoch': 2,
        }), encoding='utf-8')
        (timer_dir / 'b.json').write_text(json.dumps({
            'timer_id': 'timer-b',
            'kind': 'command',
            'status': 'completed',
            'created_at_epoch': 3,
            'run_at_epoch': 4,
        }), encoding='utf-8')

        args = argparse.Namespace(timer_command='list', limit=10)
        code, text = self._run(args)
        self.assertEqual(code, 0)
        self.assertIn('timer-b', text)
        self.assertIn('timer-a', text)


if __name__ == '__main__':
    unittest.main()
