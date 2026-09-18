from __future__ import annotations
import argparse


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Agent Manager - Manage employee agents via tmux",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list                          List all agents
  %(prog)s start dev                     Start dev agent (session: agent-emp-0001)
  %(prog)s start dev --tmux-layout windows  Start dev agent in a shared tmux session
  %(prog)s start dev --working-dir /path  Start with custom working dir
  %(prog)s stop dev                      Stop dev agent
  %(prog)s status dev                    Show runtime + heartbeat status
  %(prog)s monitor dev --follow          Monitor dev output (live)
  %(prog)s send dev "hello"              Send message to dev
  %(prog)s assign dev <<EOF              Assign task to dev
  Fix the bug
  EOF
        """,
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    list_parser = subparsers.add_parser('list', help='List all agents')
    list_parser.add_argument('--running', '-r', action='store_true', help='Show only running agents')

    start_parser = subparsers.add_parser('start', help='Start an agent')
    start_parser.add_argument('agent', help='Agent name (e.g., dev, qa) or file ID (e.g., EMP_0001)')
    start_parser.add_argument('--working-dir', '-w', help='Override working directory')
    start_parser.add_argument(
        '--tmux-layout',
        choices=['sessions', 'windows'],
        default='sessions',
        help=(
            "tmux layout: 'sessions' (default, one session per agent) "
            "or 'windows' (single shared session with one window per agent)"
        ),
    )
    start_restore_group = start_parser.add_mutually_exclusive_group()
    start_restore_group.add_argument(
        '--restore',
        '-r',
        action='store_true',
        default=True,
        help='Restore/reuse the existing tmux session if it already exists (default)',
    )
    start_restore_group.add_argument(
        '--no-restore',
        dest='restore',
        action='store_false',
        help='Fail if the tmux session already exists',
    )

    stop_parser = subparsers.add_parser('stop', help='Stop a running agent')
    stop_parser.add_argument('agent', help='Agent name')

    status_parser = subparsers.add_parser('status', help='Show status for one agent')
    status_parser.add_argument('agent', help='Agent name or file ID')

    monitor_parser = subparsers.add_parser('monitor', help='Monitor agent output')
    monitor_parser.add_argument('agent', help='Agent name')
    monitor_parser.add_argument('--follow', '-f', action='store_true', help='Follow output (like tail -f)')
    monitor_parser.add_argument('--lines', '-n', type=int, default=100, help='Number of lines to show (default: 100)')

    send_parser = subparsers.add_parser('send', help='Send message to agent')
    send_parser.add_argument('agent', help='Agent name')
    send_parser.add_argument(
        '--send-enter',
        dest='send_enter',
        action='store_true',
        default=True,
        help='Send Enter after message (default)',
    )
    send_parser.add_argument(
        '--no-enter',
        dest='send_enter',
        action='store_false',
        default=True,
        help='Do not send Enter after message (message will be typed but not submitted)',
    )
    send_parser.add_argument('message', help='Message to send')

    assign_parser = subparsers.add_parser('assign', help='Assign task to agent')
    assign_parser.add_argument('agent', help='Agent name')
    assign_parser.add_argument('--task-file', '-f', help='Read task from file')

    schedule_parser = subparsers.add_parser('schedule', help='Manage scheduled jobs')
    schedule_subparsers = schedule_parser.add_subparsers(dest='schedule_command', help='Schedule commands')

    doctor_parser = subparsers.add_parser('doctor', help='Check environment and configuration')
    doctor_parser.add_argument('--deep', action='store_true', help='Perform deeper checks')

    schedule_subparsers.add_parser('list', help='List all scheduled jobs')

    schedule_sync_parser = schedule_subparsers.add_parser('sync', help='Sync schedules to crontab')
    schedule_sync_parser.add_argument(
        '--dry-run',
        '-n',
        action='store_true',
        help='Show what would be synced without making changes',
    )

    schedule_run_parser = schedule_subparsers.add_parser('run', help='Run a scheduled job manually')
    schedule_run_parser.add_argument('agent', help='Agent name')
    schedule_run_parser.add_argument('--job', '-j', required=True, help='Job name to run')
    schedule_run_parser.add_argument('--timeout', '-t', help='Override max runtime (e.g., 30m, 2h)')

    heartbeat_parser = subparsers.add_parser('heartbeat', help='Manage heartbeat jobs')
    heartbeat_subparsers = heartbeat_parser.add_subparsers(dest='heartbeat_command', help='Heartbeat commands')

    heartbeat_subparsers.add_parser('list', help='List all heartbeat jobs')

    heartbeat_sync_parser = heartbeat_subparsers.add_parser('sync', help='Sync heartbeats to crontab')
    heartbeat_sync_parser.add_argument(
        '--dry-run',
        '-n',
        action='store_true',
        help='Show what would be synced without making changes',
    )

    heartbeat_run_parser = heartbeat_subparsers.add_parser('run', help='Run a heartbeat manually')
    heartbeat_run_parser.add_argument('agent', help='Agent name or file ID')
    heartbeat_run_parser.add_argument('--timeout', '-t', help='Override max runtime (e.g., 30m, 2h)')
    heartbeat_run_parser.add_argument(
        '--retry',
        type=int,
        help='Heartbeat retry count on recoverable failures (default: 1)',
    )
    heartbeat_run_parser.add_argument(
        '--backoff-seconds',
        type=int,
        help='Retry backoff seconds (default: 3)',
    )
    heartbeat_run_parser.add_argument(
        '--fallback-mode',
        choices=['none', 'fresh'],
        help='Fallback policy after retries (default: fresh)',
    )
    heartbeat_run_parser.add_argument(
        '--notify-on-failure',
        action='store_true',
        help='Send notifier alert when recovery still fails',
    )
    heartbeat_run_parser.add_argument(
        '--notifier-channel',
        help='Notifier channel when --notify-on-failure is enabled (default: all)',
    )
    heartbeat_run_parser.add_argument(
        '--force-session-mode',
        choices=['restore', 'auto', 'fresh', 'force'],
        help=argparse.SUPPRESS,
    )

    heartbeat_rescue_parser = heartbeat_subparsers.add_parser('rescue', help='Force-stop/start one agent heartbeat session')
    heartbeat_rescue_parser.add_argument('agent', help='Agent name or file ID')
    heartbeat_rescue_parser.add_argument('--timeout', '-t', help='Override heartbeat timeout for the post-rescue prime pass')
    heartbeat_rescue_parser.add_argument('--reason', help='Operator note for why the rescue is being performed')
    heartbeat_rescue_parser.add_argument(
        '--no-prime',
        action='store_true',
        help='Restart the agent session but skip the immediate heartbeat prime pass',
    )
    heartbeat_rescue_parser.add_argument(
        '--fresh',
        action='store_true',
        help='Use a fresh restart instead of restore mode',
    )

    heartbeat_trace_parser = heartbeat_subparsers.add_parser('trace', help='Query heartbeat audit trace logs')
    heartbeat_trace_parser.add_argument('--hb-id', help='Filter by heartbeat id (HB_ID)')
    heartbeat_trace_parser.add_argument('--agent', help='Filter by agent name/file ID/agent-id')
    heartbeat_trace_parser.add_argument('--since', help='Filter events at/after time (ISO-8601, UTC recommended)')
    heartbeat_trace_parser.add_argument('--until', help='Filter events at/before time (ISO-8601, UTC recommended)')
    heartbeat_trace_parser.add_argument('--limit', '-n', type=int, default=20, help='Max number of records to show (default: 20)')
    heartbeat_trace_parser.add_argument('--json', action='store_true', help='Output records as JSON')

    heartbeat_slo_parser = heartbeat_subparsers.add_parser('slo', help='Summarize heartbeat SLO metrics')
    heartbeat_slo_parser.add_argument('--agent', help='Filter by agent name/file ID/agent-id')
    heartbeat_slo_parser.add_argument(
        '--window',
        choices=['daily', 'weekly'],
        default='daily',
        help='Preset time window (default: daily)',
    )
    heartbeat_slo_parser.add_argument('--since', help='Override start time (ISO-8601, UTC recommended)')
    heartbeat_slo_parser.add_argument('--until', help='Override end time (ISO-8601, UTC recommended)')
    heartbeat_slo_parser.add_argument('--json', action='store_true', help='Output summary as JSON')

    dream_parser = subparsers.add_parser('dream', help='Run dream mode tasks')
    dream_subparsers = dream_parser.add_subparsers(dest='dream_command', help='Dream commands')

    dream_run_parser = dream_subparsers.add_parser('run', help='Run one dream task manually')
    dream_run_parser.add_argument('agent', help='Agent name or file ID')
    dream_run_parser.add_argument('--window-id', help='Expected active dream window id')
    dream_run_parser.add_argument('--trigger-hb-id', help='Heartbeat id that triggered the dream run')
    dream_run_parser.add_argument('--timeout', '-t', help='Override dream timeout (e.g., 10m, 1h)')

    timer_parser = subparsers.add_parser('timer', help='Schedule delayed agent-manager actions')
    timer_subparsers = timer_parser.add_subparsers(dest='timer_command', help='Timer commands')

    timer_list_parser = timer_subparsers.add_parser('list', help='List recent timers')
    timer_list_parser.add_argument('--limit', '-n', type=int, default=20, help='Max timers to show (default: 20)')

    timer_heartbeat_parser = timer_subparsers.add_parser('heartbeat', help='Run one heartbeat after a delay')
    timer_heartbeat_parser.add_argument('agent', help='Agent name or file ID')
    timer_heartbeat_parser.add_argument('--delay', '-d', required=True, help='Delay before running (e.g., 5s, 30s, 5m)')
    timer_heartbeat_parser.add_argument('--timeout', '-t', help='Override heartbeat timeout')

    timer_rescue_parser = timer_subparsers.add_parser('rescue', help='Run one heartbeat rescue after a delay')
    timer_rescue_parser.add_argument('agent', help='Agent name or file ID')
    timer_rescue_parser.add_argument('--delay', '-d', required=True, help='Delay before running (e.g., 5s, 30s, 5m)')
    timer_rescue_parser.add_argument('--timeout', '-t', help='Override heartbeat timeout for the prime pass')
    timer_rescue_parser.add_argument('--reason', help='Operator note for why the rescue is being scheduled')
    timer_rescue_parser.add_argument(
        '--no-prime',
        action='store_true',
        help='Restart the agent session but skip the immediate heartbeat prime pass',
    )
    timer_rescue_parser.add_argument(
        '--fresh',
        action='store_true',
        help='Use a fresh restart instead of restore mode',
    )
    timer_rescue_parser.add_argument('--heartbeat-id', help=argparse.SUPPRESS)
    timer_rescue_parser.add_argument('--dedupe-key', help=argparse.SUPPRESS)

    timer_command_parser = timer_subparsers.add_parser('command', help='Run one agent-manager command after a delay')
    timer_command_parser.add_argument('--delay', '-d', required=True, help='Delay before running (e.g., 5s, 30s, 5m)')
    timer_command_parser.add_argument('command_args', nargs=argparse.REMAINDER, help="Command to run after '--'")

    inbound_parser = subparsers.add_parser('inbound', help='Manage inbound queue recovery')
    inbound_subparsers = inbound_parser.add_subparsers(dest='inbound_command', help='Inbound commands')

    inbound_drain_parser = inbound_subparsers.add_parser('drain', help='Drain queued inbound messages')
    inbound_drain_parser.add_argument('agent', help='Agent name or file ID')
    inbound_drain_parser.add_argument(
        '--once',
        action='store_true',
        help='Run exactly one drain pass and exit',
    )

    inbound_rescue_parser = inbound_subparsers.add_parser(
        'rescue',
        help='Print a periodic rescue sweep invocation for cron/systemd timers',
    )
    inbound_rescue_parser.add_argument('agent', help='Agent name or file ID')

    return parser
