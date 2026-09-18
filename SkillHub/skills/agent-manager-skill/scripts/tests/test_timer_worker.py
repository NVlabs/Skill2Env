from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import timer_worker  # noqa: E402


class TimerWorkerTests(unittest.TestCase):
    def setUp(self):
        self.temp_root = Path(tempfile.mkdtemp(prefix='timer-worker-'))
        self.timer_file = self.temp_root / 'timer.json'

    def tearDown(self):
        shutil.rmtree(self.temp_root, ignore_errors=True)

    def _write_payload(self, payload: dict[str, object]) -> None:
        self.timer_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding='utf-8')

    def test_command_timer_runs_command_and_completes(self):
        self._write_payload({
            'timer_id': 'command-1',
            'kind': 'command',
            'status': 'pending',
            'repo_root': str(self.temp_root),
            'run_at_epoch': 0,
            'command_args': ['timer', 'list'],
        })

        run_mock = Mock(return_value=Mock(returncode=0))
        with patch.object(timer_worker.subprocess, 'run', run_mock):
            rc = timer_worker._run_timer(self.timer_file)

        self.assertEqual(rc, 0)
        payload = json.loads(self.timer_file.read_text(encoding='utf-8'))
        self.assertEqual(payload['status'], 'completed')
        self.assertEqual(payload['exit_code'], 0)
        cmd = run_mock.call_args.args[0]
        self.assertEqual(cmd[-2:], ['timer', 'list'])

    def test_heartbeat_timer_runs_restore_then_heartbeat(self):
        self._write_payload({
            'timer_id': 'heartbeat-1',
            'kind': 'heartbeat',
            'status': 'pending',
            'repo_root': str(self.temp_root),
            'run_at_epoch': 0,
            'agent': 'main',
            'timeout': '8m',
        })

        run_mock = Mock(side_effect=[Mock(returncode=0), Mock(returncode=0)])
        with patch.object(timer_worker.subprocess, 'run', run_mock):
            rc = timer_worker._run_timer(self.timer_file)

        self.assertEqual(rc, 0)
        self.assertEqual(run_mock.call_count, 2)
        start_cmd = run_mock.call_args_list[0].args[0]
        heartbeat_cmd = run_mock.call_args_list[1].args[0]
        self.assertEqual(start_cmd[-3:], ['start', 'main', '--restore'])
        self.assertEqual(heartbeat_cmd[-5:], ['heartbeat', 'run', 'main', '--timeout', '8m'])

    def test_timer_marks_failure_when_command_missing(self):
        self._write_payload({
            'timer_id': 'command-2',
            'kind': 'command',
            'status': 'pending',
            'repo_root': str(self.temp_root),
            'run_at_epoch': 0,
            'command_args': [],
        })

        rc = timer_worker._run_timer(self.timer_file)
        self.assertEqual(rc, 1)
        payload = json.loads(self.timer_file.read_text(encoding='utf-8'))
        self.assertEqual(payload['status'], 'failed')
        self.assertEqual(payload['error'], 'missing_command_args')

    def test_completed_timer_is_skipped(self):
        self._write_payload({
            'timer_id': 'command-3',
            'kind': 'command',
            'status': 'completed',
            'repo_root': str(self.temp_root),
            'run_at_epoch': 0,
            'command_args': ['timer', 'list'],
        })

        with patch.object(timer_worker.subprocess, 'run') as run_mock:
            rc = timer_worker._run_timer(self.timer_file)

        self.assertEqual(rc, 0)
        run_mock.assert_not_called()


if __name__ == '__main__':
    unittest.main()
