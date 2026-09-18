from __future__ import annotations
import argparse
import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from commands.heartbeat import cmd_heartbeat  # noqa: E402


class HeartbeatCommandTests(unittest.TestCase):
    def _run(self, args, **kwargs):
        out = io.StringIO()
        with redirect_stdout(out):
            code = cmd_heartbeat(args, **kwargs)
        return code, out.getvalue()

    def test_list_command_prints_formatted_output(self):
        args = argparse.Namespace(heartbeat_command='list')
        with patch('schedule_helper.list_heartbeats_formatted', return_value='heartbeats-list'):
            code, text = self._run(
                args,
                run_handler=lambda _args: 99,
                rescue_handler=lambda _args: 98,
                trace_handler=lambda _args: 99,
                slo_handler=lambda _args: 99,
            )

        self.assertEqual(code, 0)
        self.assertIn('heartbeats-list', text)

    def test_sync_dry_run_prints_preview(self):
        args = argparse.Namespace(heartbeat_command='sync', dry_run=True)
        with patch('schedule_helper.sync_crontab', return_value={'content': 'cron-content'}):
            code, text = self._run(
                args,
                run_handler=lambda _args: 99,
                rescue_handler=lambda _args: 98,
                trace_handler=lambda _args: 99,
                slo_handler=lambda _args: 99,
            )

        self.assertEqual(code, 0)
        self.assertIn('Dry run', text)
        self.assertIn('cron-content', text)

    def test_sync_apply_success(self):
        args = argparse.Namespace(heartbeat_command='sync', dry_run=False)
        with patch(
            'schedule_helper.sync_crontab',
            return_value={'success': True, 'entries': 4, 'added': 1, 'removed': 0},
        ):
            code, text = self._run(
                args,
                run_handler=lambda _args: 99,
                rescue_handler=lambda _args: 98,
                trace_handler=lambda _args: 99,
                slo_handler=lambda _args: 99,
            )

        self.assertEqual(code, 0)
        self.assertIn('Crontab synced successfully', text)
        self.assertIn('4 entries configured', text)

    def test_run_trace_and_slo_delegate_handlers(self):
        run_args = argparse.Namespace(heartbeat_command='run')
        rescue_args = argparse.Namespace(heartbeat_command='rescue')
        trace_args = argparse.Namespace(heartbeat_command='trace')
        slo_args = argparse.Namespace(heartbeat_command='slo')

        code_run, _ = self._run(
            run_args,
            run_handler=lambda _args: 11,
            rescue_handler=lambda _args: 44,
            trace_handler=lambda _args: 22,
            slo_handler=lambda _args: 33,
        )
        code_rescue, _ = self._run(
            rescue_args,
            run_handler=lambda _args: 11,
            rescue_handler=lambda _args: 44,
            trace_handler=lambda _args: 22,
            slo_handler=lambda _args: 33,
        )
        code_trace, _ = self._run(
            trace_args,
            run_handler=lambda _args: 11,
            rescue_handler=lambda _args: 44,
            trace_handler=lambda _args: 22,
            slo_handler=lambda _args: 33,
        )
        code_slo, _ = self._run(
            slo_args,
            run_handler=lambda _args: 11,
            rescue_handler=lambda _args: 44,
            trace_handler=lambda _args: 22,
            slo_handler=lambda _args: 33,
        )

        self.assertEqual(code_run, 11)
        self.assertEqual(code_rescue, 44)
        self.assertEqual(code_trace, 22)
        self.assertEqual(code_slo, 33)

    def test_unknown_subcommand_returns_error(self):
        args = argparse.Namespace(heartbeat_command='nope')
        code, text = self._run(
            args,
            run_handler=lambda _args: 11,
            rescue_handler=lambda _args: 44,
            trace_handler=lambda _args: 22,
            slo_handler=lambda _args: 33,
        )

        self.assertEqual(code, 1)
        self.assertIn('Unknown heartbeat command', text)


if __name__ == '__main__':
    unittest.main()
