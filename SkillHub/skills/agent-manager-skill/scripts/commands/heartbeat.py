from __future__ import annotations
from typing import Callable


def cmd_heartbeat(
    args,
    *,
    run_handler: Callable,
    rescue_handler: Callable,
    trace_handler: Callable,
    slo_handler: Callable,
):
    """Handle heartbeat subcommands."""
    from schedule_helper import list_heartbeats_formatted, sync_crontab

    if args.heartbeat_command == 'list':
        print(list_heartbeats_formatted())
        return 0

    if args.heartbeat_command == 'sync':
        result = sync_crontab(dry_run=args.dry_run)

        if args.dry_run:
            print("🔍 Dry run - would sync the following to crontab:")
            print()
            if result['content']:
                print(result['content'])
            else:
                print("(no heartbeats configured)")
            return 0

        if result['success']:
            print("✅ Crontab synced successfully")
            entries = result.get('entries', 0)
            added = result.get('added', 0)
            removed = result.get('removed', 0)
            print(f"   {entries} entries configured (schedules + heartbeats)")
            if added or removed:
                print(f"   Changes: +{added} -{removed}")
        else:
            print("❌ Failed to sync crontab")
            return 1

        return 0

    if args.heartbeat_command == 'run':
        return run_handler(args)

    if args.heartbeat_command == 'rescue':
        return rescue_handler(args)

    if args.heartbeat_command == 'trace':
        return trace_handler(args)

    if args.heartbeat_command == 'slo':
        return slo_handler(args)

    print(f"Unknown heartbeat command: {args.heartbeat_command}")
    return 1
