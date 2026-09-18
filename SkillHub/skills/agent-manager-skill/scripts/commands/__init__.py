"""Command handler modules for Agent Manager CLI."""

from __future__ import annotations

from .dream import cmd_dream
from .doctor import cmd_doctor
from .heartbeat import cmd_heartbeat
from .inbound import cmd_inbound
from .lifecycle import cmd_assign, cmd_monitor, cmd_send, cmd_start, cmd_stop
from .listing import cmd_list
from .schedule import cmd_schedule
from .schedule_run import cmd_schedule_run
from .status import cmd_status
from .timer import cmd_timer

__all__ = [
    'cmd_start',
    'cmd_stop',
    'cmd_monitor',
    'cmd_send',
    'cmd_assign',
    'cmd_doctor',
    'cmd_dream',
    'cmd_list',
    'cmd_status',
    'cmd_schedule',
    'cmd_schedule_run',
    'cmd_heartbeat',
    'cmd_timer',
    'cmd_inbound',
]
