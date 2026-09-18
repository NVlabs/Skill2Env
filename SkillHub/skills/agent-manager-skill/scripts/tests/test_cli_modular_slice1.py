from __future__ import annotations
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from cli_parser import create_parser  # noqa: E402
from command_registry import get_command_handlers  # noqa: E402
import main  # noqa: E402


class CliModularSlice1Tests(unittest.TestCase):
    def test_start_defaults_preserved(self):
        args = create_parser().parse_args(['start', 'dev'])
        self.assertEqual(args.command, 'start')
        self.assertEqual(args.agent, 'dev')
        self.assertTrue(args.restore)
        self.assertEqual(args.tmux_layout, 'sessions')

    def test_send_no_enter_flag_preserved(self):
        args = create_parser().parse_args(['send', 'dev', '--no-enter', 'hello'])
        self.assertEqual(args.command, 'send')
        self.assertEqual(args.agent, 'dev')
        self.assertFalse(args.send_enter)
        self.assertEqual(args.message, 'hello')

    def test_assign_task_file_default_preserved(self):
        args = create_parser().parse_args(['assign', 'dev'])
        self.assertEqual(args.command, 'assign')
        self.assertEqual(args.agent, 'dev')
        self.assertIsNone(args.task_file)

    def test_heartbeat_trace_time_range_flags(self):
        args = create_parser().parse_args(
            ['heartbeat', 'trace', '--agent', 'EMP_0001', '--since', '2026-02-09T00:00:00Z', '--until', '2026-02-10T00:00:00Z']
        )
        self.assertEqual(args.command, 'heartbeat')
        self.assertEqual(args.heartbeat_command, 'trace')
        self.assertEqual(args.agent, 'EMP_0001')
        self.assertEqual(args.since, '2026-02-09T00:00:00Z')
        self.assertEqual(args.until, '2026-02-10T00:00:00Z')

    def test_heartbeat_slo_defaults(self):
        args = create_parser().parse_args(['heartbeat', 'slo'])
        self.assertEqual(args.command, 'heartbeat')
        self.assertEqual(args.heartbeat_command, 'slo')
        self.assertEqual(args.window, 'daily')
        self.assertIsNone(args.agent)

    def test_heartbeat_rescue_flags(self):
        args = create_parser().parse_args(['heartbeat', 'rescue', 'main', '--timeout', '8m', '--reason', 'stale pending'])
        self.assertEqual(args.command, 'heartbeat')
        self.assertEqual(args.heartbeat_command, 'rescue')
        self.assertEqual(args.agent, 'main')
        self.assertEqual(args.timeout, '8m')
        self.assertEqual(args.reason, 'stale pending')
        self.assertFalse(args.no_prime)
        self.assertFalse(args.fresh)

    def test_inbound_drain_once_flags(self):
        args = create_parser().parse_args(['inbound', 'drain', 'main', '--once'])
        self.assertEqual(args.command, 'inbound')
        self.assertEqual(args.inbound_command, 'drain')
        self.assertEqual(args.agent, 'main')
        self.assertTrue(args.once)

    def test_inbound_rescue_flags(self):
        args = create_parser().parse_args(['inbound', 'rescue', 'main'])
        self.assertEqual(args.command, 'inbound')
        self.assertEqual(args.inbound_command, 'rescue')
        self.assertEqual(args.agent, 'main')

    def test_timer_heartbeat_flags(self):
        args = create_parser().parse_args(['timer', 'heartbeat', 'main', '--delay', '5s', '--timeout', '8m'])
        self.assertEqual(args.command, 'timer')
        self.assertEqual(args.timer_command, 'heartbeat')
        self.assertEqual(args.agent, 'main')
        self.assertEqual(args.delay, '5s')
        self.assertEqual(args.timeout, '8m')

    def test_timer_rescue_flags(self):
        args = create_parser().parse_args(['timer', 'rescue', 'main', '--delay', '5s', '--timeout', '8m', '--reason', 'auto'])
        self.assertEqual(args.command, 'timer')
        self.assertEqual(args.timer_command, 'rescue')
        self.assertEqual(args.agent, 'main')
        self.assertEqual(args.delay, '5s')
        self.assertEqual(args.timeout, '8m')
        self.assertEqual(args.reason, 'auto')

    def test_timer_command_remainder_flags(self):
        args = create_parser().parse_args(['timer', 'command', '--delay', '5s', '--', 'heartbeat', 'run', 'main'])
        self.assertEqual(args.command, 'timer')
        self.assertEqual(args.timer_command, 'command')
        self.assertEqual(args.delay, '5s')
        self.assertEqual(args.command_args, ['--', 'heartbeat', 'run', 'main'])

    def test_schedule_run_still_requires_job(self):
        parser = create_parser()
        with self.assertRaises(SystemExit):
            parser.parse_args(['schedule', 'run', 'dev'])

    def test_registry_contract_points_to_main_handlers(self):
        handlers = get_command_handlers(
            cmd_list=main.cmd_list,
            cmd_doctor=main.cmd_doctor,
            cmd_start=main.cmd_start,
            cmd_stop=main.cmd_stop,
            cmd_status=main.cmd_status,
            cmd_monitor=main.cmd_monitor,
            cmd_send=main.cmd_send,
            cmd_assign=main.cmd_assign,
            cmd_schedule=main.cmd_schedule,
            cmd_heartbeat=main.cmd_heartbeat,
            cmd_dream=main.cmd_dream,
            cmd_timer=main.cmd_timer,
            cmd_inbound=main.cmd_inbound,
        )
        self.assertEqual(
            set(handlers.keys()),
            {'list', 'doctor', 'start', 'stop', 'status', 'monitor', 'send', 'assign', 'schedule', 'heartbeat', 'dream', 'timer', 'inbound'},
        )
        self.assertIs(handlers['start'], main.cmd_start)
        self.assertIs(handlers['status'], main.cmd_status)
        self.assertIs(handlers['heartbeat'], main.cmd_heartbeat)
        self.assertIs(handlers['dream'], main.cmd_dream)
        self.assertIs(handlers['timer'], main.cmd_timer)
        self.assertIs(handlers['inbound'], main.cmd_inbound)

    def test_start_wrapper_delegates_to_lifecycle_handler(self):
        args = object()
        with patch('main.lifecycle_cmd_start', return_value=17) as mock_handler:
            result = main.cmd_start(args)

        self.assertEqual(result, 17)
        mock_handler.assert_called_once()
        self.assertIs(mock_handler.call_args.kwargs['deps'], main)

    def test_assign_wrapper_delegates_with_main_start_handler(self):
        args = object()
        with patch('main.lifecycle_cmd_assign', return_value=23) as mock_handler:
            result = main.cmd_assign(args)

        self.assertEqual(result, 23)
        mock_handler.assert_called_once()
        self.assertIs(mock_handler.call_args.kwargs['deps'], main)
        self.assertIs(mock_handler.call_args.kwargs['start_handler'], main.cmd_start)

    def test_status_wrapper_delegates_to_status_handler(self):
        args = object()
        with patch('main.status_cmd_status', return_value=29) as mock_handler:
            result = main.cmd_status(args)

        self.assertEqual(result, 29)
        mock_handler.assert_called_once()
        self.assertIs(mock_handler.call_args.kwargs['deps'], main)

    def test_list_wrapper_delegates_to_listing_handler(self):
        args = object()
        with patch('main.listing_cmd_list', return_value=37) as mock_handler:
            result = main.cmd_list(args)

        self.assertEqual(result, 37)
        mock_handler.assert_called_once()
        self.assertIs(mock_handler.call_args.kwargs['deps'], main)

    def test_doctor_wrapper_delegates_to_doctor_handler(self):
        args = object()
        with patch('main.doctor_cmd_doctor', return_value=41) as mock_handler:
            result = main.cmd_doctor(args)

        self.assertEqual(result, 41)
        mock_handler.assert_called_once()
        self.assertIs(mock_handler.call_args.kwargs['deps'], main)

    def test_heartbeat_wrapper_delegates_to_heartbeat_handler(self):
        args = object()
        with patch('main.heartbeat_cmd_heartbeat', return_value=43) as mock_handler:
            result = main.cmd_heartbeat(args)

        self.assertEqual(result, 43)
        mock_handler.assert_called_once()
        self.assertIs(mock_handler.call_args.kwargs['run_handler'], main.cmd_heartbeat_run)
        self.assertIs(mock_handler.call_args.kwargs['rescue_handler'], main.cmd_heartbeat_rescue)
        self.assertIs(mock_handler.call_args.kwargs['trace_handler'], main.cmd_heartbeat_trace)
        self.assertIs(mock_handler.call_args.kwargs['slo_handler'], main.cmd_heartbeat_slo)

    def test_schedule_run_wrapper_delegates_to_schedule_run_handler(self):
        args = object()
        with patch('main.schedule_run_cmd_schedule_run', return_value=47) as mock_handler:
            result = main.cmd_schedule_run(args)

        self.assertEqual(result, 47)
        mock_handler.assert_called_once()
        self.assertIs(mock_handler.call_args.kwargs['deps'], main)
        self.assertIs(mock_handler.call_args.kwargs['start_handler'], main.cmd_start)

    def test_schedule_wrapper_delegates_to_schedule_handler(self):
        args = object()
        with patch('main.schedule_cmd_schedule', return_value=31) as mock_handler:
            result = main.cmd_schedule(args)

        self.assertEqual(result, 31)
        mock_handler.assert_called_once()
        self.assertIs(mock_handler.call_args.kwargs['deps'], main)
        self.assertIs(mock_handler.call_args.kwargs['schedule_run_handler'], main.cmd_schedule_run)

    def test_timer_wrapper_delegates_to_timer_handler(self):
        args = object()
        with patch('main.timer_cmd_timer', return_value=59) as mock_handler:
            result = main.cmd_timer(args)

        self.assertEqual(result, 59)
        mock_handler.assert_called_once()
        self.assertIs(mock_handler.call_args.kwargs['deps'], main)

    def test_inbound_wrapper_delegates_to_inbound_handler(self):
        args = object()
        with patch('main.inbound_cmd_inbound', return_value=53) as mock_handler:
            result = main.cmd_inbound(args)

        self.assertEqual(result, 53)
        mock_handler.assert_called_once()
        self.assertIs(mock_handler.call_args.kwargs['deps'], main)
        self.assertIs(mock_handler.call_args.kwargs['drain_once_handler'], main.drain_main_inbound_once)


if __name__ == '__main__':
    unittest.main()
