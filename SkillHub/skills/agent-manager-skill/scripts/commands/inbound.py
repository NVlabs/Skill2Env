from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
import shlex
from typing import Any, Callable, Dict, Optional

from .lifecycle import _confirm_delivery_after_send
from services.inbound_queue import (
    classify_inbound_replay_state,
    inbound_message_attempt_count,
    load_pending_inbound_messages,
)


_DISPATCH_LEASE_SECONDS = 300
_RETRY_BACKOFF_SECONDS = 60
_MAX_REPLAY_ATTEMPTS = 3
_DEFAULT_RESCUE_CRON = '*/5 * * * *'
_DEFAULT_RESCUE_ON_CALENDAR = '*:0/5'


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _reclaim_reason(payload: Dict[str, Any]) -> str:
    state = str(payload.get('state') or '').strip()
    if state == 'claimed':
        return 'stale_claimed_lease'
    if state == 'dispatching':
        return 'stale_dispatching_lease'
    return ''


def _build_replay_message(
    deps: Any,
    *,
    repo_root: Path,
    agent_id: str,
    payload: Dict[str, Any],
    is_codex: bool,
) -> str:
    message = str(payload.get('message') or '')
    source = str(payload.get('source') or '')
    message_kind = str(payload.get('message_kind') or '')

    if message_kind == 'task_assignment' or source == 'assign':
        task_message = f"# Task Assignment\n\n{message}"
        if is_codex and deps._should_use_codex_file_pointer(task_message):
            task_file = deps.write_codex_message_file(repo_root, agent_id, 'assign-replay', task_message)
            return (
                f"Task assignment replayed from inbound queue. Read and follow instructions from file: {task_file}\n"
                "Execute the task now and report progress/blocks."
            )
        return task_message

    if is_codex and deps._should_use_codex_file_pointer(message):
        message_file = deps.write_codex_message_file(repo_root, agent_id, 'send-replay', message)
        return (
            f"Inbound message replayed from queue. Read and execute the message from file: {message_file}\n"
            "After completing it, summarize key results."
        )
    return message


def build_inbound_rescue_plan(*, deps: Any, agent_id: str = 'main') -> Dict[str, str]:
    repo_root = deps.get_repo_root()
    main_script = deps.Path(deps.__file__).resolve()
    log_dir = repo_root / '.crontab_logs'
    log_file = log_dir / f'agent-{agent_id}-inbound-rescue.log'

    repo_root_q = shlex.quote(str(repo_root))
    main_script_q = shlex.quote(str(main_script))
    log_dir_q = shlex.quote(str(log_dir))
    log_file_q = shlex.quote(str(log_file))
    agent_id_q = shlex.quote(str(agent_id))

    shell_command = (
        f"cd {repo_root_q} && "
        f"mkdir -p {log_dir_q} && "
        f"python3 {main_script_q} inbound drain {agent_id_q} --once "
        f">> {log_file_q} 2>&1"
    )

    systemd_exec = shlex.quote(shell_command)
    service_unit = "\n".join([
        "[Unit]",
        "Description=Agent Manager inbound rescue sweep for main",
        "",
        "[Service]",
        "Type=oneshot",
        f"WorkingDirectory={repo_root}",
        f"ExecStart=/usr/bin/env bash -lc {systemd_exec}",
    ])
    timer_unit = "\n".join([
        "[Unit]",
        "Description=Run Agent Manager inbound rescue sweep every 5 minutes",
        "",
        "[Timer]",
        f"OnCalendar={_DEFAULT_RESCUE_ON_CALENDAR}",
        "Persistent=true",
        "",
        "[Install]",
        "WantedBy=timers.target",
    ])

    return {
        'shell': shell_command,
        'cron': f"{_DEFAULT_RESCUE_CRON} {shell_command}",
        'systemd_service': service_unit,
        'systemd_timer': timer_unit,
    }


def drain_main_inbound_once(
    *,
    deps: Any,
    agent_id: str = 'main',
    trigger: str = 'manual',
) -> Dict[str, int]:
    repo_root = deps.get_repo_root()
    pending = load_pending_inbound_messages(repo_root, agent_id=agent_id)
    if not pending:
        return {'rc': 0, 'drained': 0, 'skipped': 0, 'failed': 0, 'dead_lettered': 0}

    agent_config = deps.resolve_agent(agent_id)
    if not agent_config:
        print(f"❌ Agent not found: {agent_id}")
        return {'rc': 1, 'drained': 0, 'skipped': 0, 'failed': 0, 'dead_lettered': 0}

    if not deps.check_tmux():
        print("❌ tmux is not installed")
        return {'rc': 1, 'drained': 0, 'skipped': 0, 'failed': 0, 'dead_lettered': 0}

    if not deps.session_exists(agent_id):
        print(f"⚠️  Agent '{agent_config['name']}' is not running; inbound drain skipped")
        return {'rc': 1, 'drained': 0, 'skipped': len(pending), 'failed': 0, 'dead_lettered': 0}

    launcher = deps.resolve_launcher_command(agent_config.get('launcher', ''))
    is_codex = 'codex' in launcher.lower()
    claim_owner = f"inbound-drain:{trigger}"
    now = _utc_now()
    summary = {'rc': 0, 'drained': 0, 'skipped': 0, 'failed': 0, 'dead_lettered': 0}

    for payload in pending:
        message_id = str(payload.get('message_id') or '').strip()
        if not message_id:
            summary['skipped'] += 1
            continue

        attempts = inbound_message_attempt_count(payload)
        replay_state = classify_inbound_replay_state(
            payload,
            now=now,
            max_attempts=_MAX_REPLAY_ATTEMPTS,
            dispatch_lease_seconds=_DISPATCH_LEASE_SECONDS,
        )
        if replay_state == 'dead_letter':
            deps.mark_inbound_message_state(
                repo_root,
                agent_id=agent_id,
                message_id=message_id,
                state='dead_letter',
                detail='replay_attempt_limit_exceeded',
                attempt_count=attempts,
            )
            summary['dead_lettered'] += 1
            continue

        if replay_state != 'replayable':
            summary['skipped'] += 1
            continue

        next_attempt = attempts + 1
        reclaim_reason = _reclaim_reason(payload)
        if reclaim_reason:
            deps.append_inbound_message_event(
                repo_root,
                agent_id=agent_id,
                message_id=message_id,
                event='reclaimed',
                state=str(payload.get('state') or ''),
                detail=f"inbound_drain_reclaimed:{trigger}:{reclaim_reason}",
                attempt_count=next_attempt,
                claim_owner=claim_owner,
            )
        if deps.was_message_yielded(repo_root, agent_id=agent_id, message_id=message_id):
            deps.append_inbound_message_event(
                repo_root,
                agent_id=agent_id,
                message_id=message_id,
                event='resumed',
                state=str(payload.get('state') or 'queued'),
                detail=f"inbound_drain_resumed:{trigger}",
                attempt_count=next_attempt,
            )

        claimed_at = _utc_now().isoformat().replace('+00:00', 'Z')
        deps.mark_inbound_message_state(
            repo_root,
            agent_id=agent_id,
            message_id=message_id,
            state='claimed',
            detail=f"inbound_drain_claimed:{trigger}",
            claim_owner=claim_owner,
            claimed_at=claimed_at,
            attempt_count=next_attempt,
        )
        deps.mark_inbound_message_state(
            repo_root,
            agent_id=agent_id,
            message_id=message_id,
            state='dispatching',
            detail='inbound_drain_dispatch_start',
            claim_owner=claim_owner,
            claimed_at=claimed_at,
            dispatching_at=claimed_at,
            attempt_count=next_attempt,
        )

        replay_message = _build_replay_message(
            deps,
            repo_root=repo_root,
            agent_id=agent_id,
            payload=payload,
            is_codex=is_codex,
        )
        ok = deps.send_keys(
            agent_id,
            replay_message,
            send_enter=True,
            clear_input=is_codex,
            escape_first=is_codex,
            enter_via_key=is_codex,
        )
        if not ok:
            if next_attempt >= _MAX_REPLAY_ATTEMPTS:
                deps.mark_inbound_message_state(
                    repo_root,
                    agent_id=agent_id,
                    message_id=message_id,
                    state='dead_letter',
                    detail='inbound_drain_send_keys_failed',
                    attempt_count=next_attempt,
                    claim_owner=claim_owner,
                )
                summary['dead_lettered'] += 1
            else:
                next_retry_at = (_utc_now() + timedelta(seconds=_RETRY_BACKOFF_SECONDS)).isoformat().replace('+00:00', 'Z')
                deps.mark_inbound_message_state(
                    repo_root,
                    agent_id=agent_id,
                    message_id=message_id,
                    state='failed',
                    detail='inbound_drain_send_keys_failed',
                    attempt_count=next_attempt,
                    claim_owner=claim_owner,
                    next_retry_at=next_retry_at,
                )
                summary['failed'] += 1
            summary['rc'] = 1
            continue

        deps.mark_inbound_message_state(
            repo_root,
            agent_id=agent_id,
            message_id=message_id,
            state='dispatched',
            detail='inbound_drain_dispatch_ok',
            attempt_count=next_attempt,
            claim_owner=claim_owner,
        )
        delivery_confirmed, observed_state, observed_reason = _confirm_delivery_after_send(
            deps,
            agent_id=agent_id,
            launcher=launcher,
        )
        if delivery_confirmed:
            reply_evidence = 'repo_local'
            transport_ack_status = 'unverified'
            transport_ack_detail = ''
            if observed_reason != 'runtime_probe_unavailable':
                reply_evidence = 'transport_ack'
                transport_ack_status = 'ack'
                transport_ack_detail = f"{observed_state}:{observed_reason}"
            deps.mark_inbound_message_state(
                repo_root,
                agent_id=agent_id,
                message_id=message_id,
                state='handled',
                detail=f"inbound_drain_handled:{trigger}:{observed_state}:{observed_reason}",
                attempt_count=next_attempt,
                claim_owner=claim_owner,
            )
            append_reply_closure = getattr(deps, 'append_inbound_reply_closure', None)
            if callable(append_reply_closure):
                append_reply_closure(
                    repo_root,
                    agent_id=agent_id,
                    message_id=message_id,
                    detail=f"inbound_drain_reply_audit_closed:{trigger}",
                    reply_evidence=reply_evidence,
                    transport_ack_status=transport_ack_status,
                    transport_ack_detail=transport_ack_detail,
                    attempt_count=next_attempt,
                    claim_owner=claim_owner,
                )
            else:
                deps.append_inbound_message_event(
                    repo_root,
                    agent_id=agent_id,
                    message_id=message_id,
                    event='replied',
                    state='replied',
                    detail=f"inbound_drain_reply_audit_closed:{trigger}",
                    reply_evidence=reply_evidence,
                    transport_ack_status=transport_ack_status,
                    transport_ack_detail=transport_ack_detail,
                    attempt_count=next_attempt,
                    claim_owner=claim_owner,
                )
            summary['drained'] += 1
            continue

        next_retry_at = (_utc_now() + timedelta(seconds=_RETRY_BACKOFF_SECONDS)).isoformat().replace('+00:00', 'Z')
        deps.mark_inbound_message_state(
            repo_root,
            agent_id=agent_id,
            message_id=message_id,
            state='failed',
            detail=f"inbound_drain_delivery_unconfirmed:{observed_state}:{observed_reason}",
            attempt_count=next_attempt,
            claim_owner=claim_owner,
            next_retry_at=next_retry_at,
        )
        summary['failed'] += 1
        summary['rc'] = 1

    return summary


def cmd_inbound(args, *, deps: Any, drain_once_handler: Optional[Callable[..., Dict[str, int]]] = None):
    """Handle inbound queue recovery subcommands."""
    if drain_once_handler is None:
        drain_once_handler = drain_main_inbound_once

    if args.inbound_command not in {'drain', 'rescue'}:
        print(f"Unknown inbound command: {args.inbound_command}")
        return 1

    agent_config = deps.resolve_agent(args.agent)
    if not agent_config:
        print(f"❌ Agent not found: {args.agent}")
        return 1

    agent_id = deps.get_agent_id(agent_config)
    if agent_id != 'main':
        print("❌ inbound drain currently supports only the main agent")
        return 1

    if args.inbound_command == 'rescue':
        plan = build_inbound_rescue_plan(deps=deps, agent_id=agent_id)
        print("Inbound rescue shell command:")
        print(plan['shell'])
        print()
        print("Cron example:")
        print(plan['cron'])
        print()
        print("Systemd service example:")
        print(plan['systemd_service'])
        print()
        print("Systemd timer example:")
        print(plan['systemd_timer'])
        return 0

    if not getattr(args, 'once', False):
        print("❌ inbound drain currently requires --once")
        return 1

    summary = drain_once_handler(deps=deps, agent_id=agent_id, trigger='cli')
    if summary['rc'] != 0 and summary['drained'] == 0 and summary['dead_lettered'] == 0:
        return summary['rc']

    print(
        "Inbound drain summary: "
        f"drained={summary['drained']} "
        f"failed={summary['failed']} "
        f"dead_lettered={summary['dead_lettered']} "
        f"skipped={summary['skipped']}"
    )
    return summary['rc']
