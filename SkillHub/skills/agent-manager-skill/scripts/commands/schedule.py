from __future__ import annotations
from typing import Any, Callable


def cmd_schedule(args, *, deps: Any, schedule_run_handler: Callable):
    """Handle schedule subcommands."""
    from schedule_helper import list_schedules_formatted, sync_crontab

    if args.schedule_command == 'list':
        print(list_schedules_formatted())
        return 0

    if args.schedule_command == 'sync':
        result = sync_crontab(dry_run=args.dry_run)

        if args.dry_run:
            print("🔍 Dry run - would sync the following to crontab:")
            print()
            if result['content']:
                print(result['content'])
            else:
                print("(no schedules configured)")
            return 0

        if result['success']:
            print("✅ Crontab synced successfully")
            entries = result.get('entries', 0)
            added = result.get('added', 0)
            removed = result.get('removed', 0)
            print(f"   {entries} schedule entries configured")
            if added or removed:
                print(f"   Changes: +{added} -{removed}")
        else:
            print("❌ Failed to sync crontab")
            return 1

        return 0

    if args.schedule_command == 'run':
        return schedule_run_handler(args)

    print(f"Unknown schedule command: {args.schedule_command}")
    return 1
