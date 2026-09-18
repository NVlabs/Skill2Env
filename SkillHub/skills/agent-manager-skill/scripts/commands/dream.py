from __future__ import annotations
from typing import Callable


def cmd_dream(
    args,
    *,
    run_handler: Callable,
):
    """Handle dream subcommands."""
    if args.dream_command == 'run':
        return run_handler(args)

    print(f"Unknown dream command: {args.dream_command}")
    return 1
