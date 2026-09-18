from __future__ import annotations
from typing import Any, Callable, Optional, Tuple


def _script_name(deps: Any) -> str:
    try:
        return deps.Path(deps.__file__).name
    except Exception:
        return "main.py"


def _session_label(agent_id: str) -> str:
    return "main" if str(agent_id).strip().lower() == "main" else f"agent-{agent_id}"


def _queue_main_inbound_message(
    deps: Any,
    *,
    agent_id: str,
    source: str,
    message_kind: str,
    message: str,
) -> Tuple[Optional[Any], str]:
    if str(agent_id).strip().lower() != 'main':
        return None, ""

    get_repo_root = getattr(deps, 'get_repo_root', None)
    enqueue_inbound_message = getattr(deps, 'enqueue_inbound_message', None)
    if not callable(get_repo_root) or not callable(enqueue_inbound_message):
        raise RuntimeError("inbound queue helpers are unavailable")

    repo_root = get_repo_root()
    message_id = enqueue_inbound_message(
        repo_root,
        agent_id=agent_id,
        source=source,
        message_kind=message_kind,
        message=message,
    )
    return repo_root, message_id


def _mark_main_inbound_state(
    deps: Any,
    repo_root: Any,
    *,
    agent_id: str,
    message_id: str,
    state: str,
    detail: str = "",
) -> None:
    if str(agent_id).strip().lower() != 'main' or not repo_root or not message_id:
        return
    mark_inbound_message_state = getattr(deps, 'mark_inbound_message_state', None)
    if not callable(mark_inbound_message_state):
        raise RuntimeError("inbound queue state helper is unavailable")
    mark_inbound_message_state(
        repo_root,
        agent_id=agent_id,
        message_id=message_id,
        state=state,
        detail=detail,
    )


def _mark_main_inbound_resumed_if_needed(
    deps: Any,
    repo_root: Any,
    *,
    agent_id: str,
    message_id: str,
    detail: str,
) -> None:
    if str(agent_id).strip().lower() != 'main' or not repo_root or not message_id:
        return
    was_message_yielded = getattr(deps, 'was_message_yielded', None)
    append_inbound_message_event = getattr(deps, 'append_inbound_message_event', None)
    if not callable(was_message_yielded) or not callable(append_inbound_message_event):
        raise RuntimeError("inbound queue resume helpers are unavailable")
    if not was_message_yielded(repo_root, agent_id=agent_id, message_id=message_id):
        return
    append_inbound_message_event(
        repo_root,
        agent_id=agent_id,
        message_id=message_id,
        event='resumed',
        state='dispatching',
        detail=detail,
    )


def _mark_main_inbound_replied(
    deps: Any,
    repo_root: Any,
    *,
    agent_id: str,
    message_id: str,
    detail: str,
    reply_evidence: str = 'repo_local',
    transport_ack_status: str = 'unverified',
    transport_ack_detail: str = '',
) -> None:
    if str(agent_id).strip().lower() != 'main' or not repo_root or not message_id:
        return
    append_inbound_reply_closure = getattr(deps, 'append_inbound_reply_closure', None)
    append_inbound_message_event = getattr(deps, 'append_inbound_message_event', None)
    if callable(append_inbound_reply_closure):
        append_inbound_reply_closure(
            repo_root,
            agent_id=agent_id,
            message_id=message_id,
            detail=detail,
            reply_evidence=reply_evidence,
            transport_ack_status=transport_ack_status,
            transport_ack_detail=transport_ack_detail,
        )
        return
    if not callable(append_inbound_message_event):
        raise RuntimeError("inbound queue reply helpers are unavailable")
    append_inbound_message_event(
        repo_root,
        agent_id=agent_id,
        message_id=message_id,
        event='replied',
        state='replied',
        detail=detail,
        reply_evidence=reply_evidence,
        transport_ack_status=transport_ack_status,
        transport_ack_detail=transport_ack_detail,
    )


def _probe_runtime_state(deps: Any, *, agent_id: str, launcher: str) -> Optional[Tuple[str, str]]:
    get_agent_runtime_state = getattr(deps, 'get_agent_runtime_state', None)
    if not callable(get_agent_runtime_state):
        return None

    try:
        runtime = get_agent_runtime_state(agent_id, launcher=launcher)
    except TypeError:
        runtime = get_agent_runtime_state(agent_id)
    except Exception:
        return None

    if not isinstance(runtime, dict):
        return None

    state = str(runtime.get('state', 'unknown'))
    reason = str(runtime.get('reason', 'unknown'))
    return state, reason


def _confirm_delivery_after_send(
    deps: Any,
    *,
    agent_id: str,
    launcher: str,
    timeout_seconds: int = 8,
    poll_seconds: float = 1.0,
) -> Tuple[bool, str, str]:
    first = _probe_runtime_state(deps, agent_id=agent_id, launcher=launcher)
    if first is None:
        return True, 'unknown', 'runtime_probe_unavailable'

    state, reason = first
    if state != 'idle':
        return True, state, reason

    import time as py_time

    deps_time = getattr(deps, 'time', None)
    now_fn = getattr(deps_time, 'time', None) or py_time.time
    sleep_fn = getattr(deps_time, 'sleep', None) or py_time.sleep

    deadline = now_fn() + max(1, int(timeout_seconds))
    last_state, last_reason = state, reason
    while now_fn() < deadline:
        sleep_fn(poll_seconds)
        snapshot = _probe_runtime_state(deps, agent_id=agent_id, launcher=launcher)
        if snapshot is None:
            continue
        last_state, last_reason = snapshot
        if last_state != 'idle':
            return True, last_state, last_reason

    return False, last_state, last_reason


def _maybe_drain_main_inbound_after_restore(deps: Any, *, agent_id: str) -> None:
    if str(agent_id).strip().lower() != 'main':
        return

    drain_once = getattr(deps, 'drain_main_inbound_once', None)
    if not callable(drain_once):
        return

    try:
        summary = drain_once(agent_id='main', trigger='start_restore')
    except Exception as exc:
        print(f"⚠️  Inbound drain skipped after restore: {exc}")
        return

    if not isinstance(summary, dict):
        return

    drained = int(summary.get('drained', 0) or 0)
    dead_lettered = int(summary.get('dead_lettered', 0) or 0)
    failed = int(summary.get('failed', 0) or 0)
    if drained or dead_lettered or failed:
        print(
            "ℹ️  Inbound drain after restore: "
            f"drained={drained} failed={failed} dead_lettered={dead_lettered}"
        )


def cmd_start(args, *, deps: Any):
    """Start an agent in tmux session."""
    check_tmux = deps.check_tmux
    resolve_agent = deps.resolve_agent
    list_all_agents = deps.list_all_agents
    get_agent_id = deps.get_agent_id
    session_exists = deps.session_exists
    get_session_info = deps.get_session_info
    normalize_path = deps._normalize_path
    get_repo_root = deps.get_repo_root
    resolve_launcher_command = deps.resolve_launcher_command
    get_provider_key = deps.get_provider_key
    snapshot_provider_sessions = deps._snapshot_provider_sessions
    get_session_restore_mode = deps.get_session_restore_mode
    get_session_restore_flag = deps.get_session_restore_flag
    load_provider_session_id = deps._load_provider_session_id
    provider_session_exists = deps._provider_session_exists
    apply_session_restore_args = deps._apply_session_restore_args
    build_system_prompt = deps.build_system_prompt
    build_launcher_config_overrides = deps.build_launcher_config_overrides
    to_toml_literal = deps._to_toml_literal
    get_system_prompt_mode = deps.get_system_prompt_mode
    get_system_prompt_flag = deps.get_system_prompt_flag
    get_system_prompt_key = deps.get_system_prompt_key
    get_system_prompt_value_mode = deps.get_system_prompt_value_mode
    get_launcher_config_mode = deps.get_launcher_config_mode
    get_launcher_config_flag = deps.get_launcher_config_flag
    get_agents_md_mode = deps.get_agents_md_mode
    get_mcp_config_mode = deps.get_mcp_config_mode
    get_mcp_config_flag = deps.get_mcp_config_flag
    build_mcp_config_json = deps.build_mcp_config_json
    build_start_command = deps.build_start_command
    write_system_prompt_file = deps.write_system_prompt_file
    write_start_command_script = deps.write_start_command_script
    start_session_with_layout = deps.start_session_with_layout
    start_session = deps.start_session
    wait_for_prompt = deps.wait_for_prompt
    inject_system_prompt = deps.inject_system_prompt
    wait_for_agent_ready = deps.wait_for_agent_ready
    save_provider_session_id = deps._save_provider_session_id
    find_new_provider_session_id_with_retry = deps._find_new_provider_session_id_with_retry
    Path = deps.Path
    shlex = deps.shlex
    json = deps.json

    if not check_tmux():
        print("❌ tmux is not installed. Install with: apt install tmux")
        return 1

    agent_config = resolve_agent(args.agent)
    if not agent_config:
        print(f"❌ Agent not found: {args.agent}")
        print("   Available agents:")
        all_agents = list_all_agents()
        for file_id, config in sorted(all_agents.items(), key=lambda item: item[0]):
            name = config.get('name') or file_id
            agent_id = get_agent_id(config)
            print(f"   - {file_id} ({name}) ({_session_label(agent_id)})")
        return 1

    agent_name = agent_config['name']
    agent_id = get_agent_id(agent_config)
    agent_file_id = agent_config.get('file_id', args.agent)

    if not agent_config.get('enabled', True):
        agent_file_path = agent_config.get('_file_path', f'agents/{agent_file_id}.md')
        print(f"⚠️  Agent '{agent_name}' is disabled")
        print(f"   Config: {agent_file_path}")
        print(f"   To enable: Set 'enabled: true' in the agent config")
        return 1

    working_dir = args.working_dir or agent_config.get('working_directory')
    normalized_working_dir = normalize_path(working_dir) if working_dir else ""
    repo_root = get_repo_root()
    sync_fullspeed_hook = getattr(deps, '_sync_codex_fullspeed_stop_hook', None)
    hook_sync = None
    if normalized_working_dir and callable(sync_fullspeed_hook):
        try:
            hook_sync = sync_fullspeed_hook(
                agent_config,
                working_dir=normalized_working_dir,
                repo_root=repo_root,
            )
        except ValueError as exc:
            print(f"❌ {exc}")
            return 1
        if hook_sync.get('reason') == 'unsupported_provider':
            print("⚠️  heartbeat.mode=full_speed currently only supports launcher: codex")
        elif hook_sync.get('reason') == 'cleaned' and hook_sync.get('updated'):
            print(f"ℹ️  Removed deprecated Codex full-speed Stop hook: {hook_sync.get('hooks_path', '')}")

    if session_exists(agent_id):
        session_info = get_session_info(agent_id) or {}
        session_name = session_info.get('session', _session_label(agent_id))
        if getattr(args, 'restore', True):
            print(f"✅ Restored existing session for '{agent_name}'")
            print(f"   Session: {session_name}({agent_name})")
            if getattr(args, 'working_dir', None):
                print(f"   Note: --working-dir is ignored when restoring")
            print()
            if session_info.get('mode') == 'windows':
                group = session_name.split(':', 1)[0]
                print(f"Attach with: tmux attach -t {group}")
            else:
                print(f"Attach with: tmux attach -t {session_name}")
            print(f"Monitor with: python3 {_script_name(deps)} monitor {agent_file_id}")
            _maybe_drain_main_inbound_after_restore(deps, agent_id=agent_id)
            return 0

        print(f"⚠️  Agent '{agent_name}' is already running")
        print(f"   Session: {session_name}({agent_name})")
        print()
        print(f"   To stop first: python3 {_script_name(deps)} stop {agent_file_id}")
        if session_info.get('mode') == 'windows':
            group = session_name.split(':', 1)[0]
            print(f"   Or attach directly: tmux attach -t {group}")
        else:
            print(f"   Or attach directly: tmux attach -t {session_name}")
        print(f"   Or restore (reuse existing): python3 {_script_name(deps)} start {agent_file_id} --restore")
        return 1

    if not normalized_working_dir:
        print("❌ No working directory specified")
        return 1

    working_dir = normalized_working_dir
    skills_dir = repo_root / '.agent' / 'skills'

    launcher = resolve_launcher_command(agent_config.get('launcher', ''))
    launcher_args = list(agent_config.get('launcher_args', []) or [])

    provider_key = get_provider_key(launcher)
    did_provider_restore = False
    provider_before_sessions: set[str] = set()

    track_provider_session = provider_key in {'droid', 'claude', 'claude-code', 'codex', 'opencode'}
    if provider_key == 'droid' and 'exec' in launcher_args:
        track_provider_session = False

    if track_provider_session:
        provider_before_sessions = snapshot_provider_sessions(provider_key, working_dir)

    if getattr(args, 'restore', True) and track_provider_session:
        restore_mode = get_session_restore_mode(launcher)
        restore_flag = get_session_restore_flag(launcher)
        if restore_mode == 'cli_optional_arg' and restore_flag:
            stored_session_id = load_provider_session_id(repo_root, provider_key, agent_id)
            if stored_session_id and provider_session_exists(
                provider_key,
                working_dir,
                stored_session_id,
                agent_id=agent_id,
            ):
                launcher_args = apply_session_restore_args(
                    provider_key,
                    launcher,
                    launcher_args,
                    restore_flag,
                    stored_session_id,
                )
                did_provider_restore = True
            elif stored_session_id:
                print(f"⚠️  Stored {provider_key} sessionId not found for cwd; starting fresh")

    system_prompt = build_system_prompt(agent_config, repo_root=repo_root, skills_dir=skills_dir)
    if provider_key == 'codex' and not did_provider_restore and deps._should_enforce_codex_session_owner(agent_id):
        system_prompt = deps._inject_codex_session_owner_marker(system_prompt, agent_id)
    system_prompt_mode = get_system_prompt_mode(launcher)
    system_prompt_flag = get_system_prompt_flag(launcher)
    system_prompt_key = get_system_prompt_key(launcher)
    system_prompt_value_mode = get_system_prompt_value_mode(launcher)
    launcher_config_mode = get_launcher_config_mode(launcher)
    launcher_config_flag = get_launcher_config_flag(launcher)
    if (
        system_prompt
        and not did_provider_restore
        and get_agents_md_mode(launcher) == 'cwd'
        and get_provider_key(launcher) != 'codex'
    ):
        if (Path(working_dir) / 'AGENTS.md').exists():
            print("ℹ️  AGENTS.md found in working directory; skipping system prompt injection")
            system_prompt = ""

    try:
        launcher_config_overrides = build_launcher_config_overrides(agent_config, working_dir=working_dir)
    except ValueError as e:
        print(f"❌ {e}")
        return 1

    mcp_config_mode = get_mcp_config_mode(launcher)
    mcp_config_flag = get_mcp_config_flag(launcher)
    try:
        mcp_config_json = build_mcp_config_json(agent_config)
    except ValueError as e:
        print(f"❌ {e}")
        return 1

    use_cli_system_prompt = bool(
        system_prompt
        and not did_provider_restore
        and system_prompt_mode in {'cli_append', 'cli_config_kv'}
        and system_prompt_flag
        and (system_prompt_mode != 'cli_config_kv' or system_prompt_key)
    )
    use_launcher_config = bool(
        launcher_config_overrides
        and not did_provider_restore
        and launcher_config_mode == 'cli_config_kv'
        and launcher_config_flag
    )
    command = build_start_command(working_dir, launcher, launcher_args)

    if use_launcher_config:
        for key, value in launcher_config_overrides.items():
            kv = f"{key}={to_toml_literal(value)}"
            command = f"{command} {shlex.quote(launcher_config_flag)} {shlex.quote(kv)}"
    elif launcher_config_overrides and did_provider_restore:
        print("ℹ️  Provider session restored; skipping launcher_config injection")
    elif launcher_config_overrides and launcher_config_mode != 'cli_config_kv':
        print(f"⚠️  launcher_config present but not supported for launcher '{launcher}' - ignoring")

    if use_cli_system_prompt:
        if system_prompt_mode == 'cli_append':
            prompt_file = write_system_prompt_file(repo_root, agent_id, system_prompt)
            command = f"{command} {shlex.quote(system_prompt_flag)} \"$(cat {shlex.quote(str(prompt_file))})\""
        elif system_prompt_mode == 'cli_config_kv':
            if system_prompt_value_mode == 'inline_text':
                toml_value = json.dumps(system_prompt)
            else:
                prompt_file = write_system_prompt_file(repo_root, agent_id, system_prompt)
                toml_value = json.dumps(str(prompt_file))
            kv = f"{system_prompt_key}={toml_value}"
            command = f"{command} {shlex.quote(system_prompt_flag)} {shlex.quote(kv)}"

    if len(command) > 6000:
        command_script = write_start_command_script(repo_root, agent_id, command)
        command = shlex.quote(str(command_script))

    if mcp_config_json and not did_provider_restore:
        if mcp_config_mode == 'cli_json' and mcp_config_flag:
            command = f"{command} {shlex.quote(mcp_config_flag)} {shlex.quote(mcp_config_json)}"
        else:
            print(f"⚠️  MCP config present but not supported for launcher '{launcher}' - ignoring")
    elif mcp_config_json and did_provider_restore:
        print(f"ℹ️  Provider session restored; skipping MCP config injection")

    tmux_config = agent_config.get('tmux') or {}
    if tmux_config and not isinstance(tmux_config, dict):
        print("❌ Invalid 'tmux' in agent config (expected a mapping)")
        return 1

    tmux_layout_spec = tmux_config.get('layout') if tmux_config else None
    tmux_target_path = tmux_config.get('target_pane') if tmux_config else None

    if tmux_layout_spec is None and tmux_target_path is not None:
        print("❌ tmux.target_pane requires tmux.layout")
        return 1

    if tmux_layout_spec is not None:
        try:
            start_session_with_layout(
                agent_id,
                command,
                layout_spec=tmux_layout_spec,
                target_path=tmux_target_path,
                session_layout=getattr(args, 'tmux_layout', 'sessions'),
            )
        except ValueError as e:
            print(f"❌ {e}")
            return 1
    else:
        if not start_session(agent_id, command, layout=getattr(args, 'tmux_layout', 'sessions')):
            print(f"❌ Failed to start agent '{agent_name}'")
            return 1

    session_info = get_session_info(agent_id) or {}
    session_name = session_info.get('session', _session_label(agent_id))
    print(f"✅ Agent '{agent_name}' started")
    print(f"   Session: {session_name}({agent_name})")
    print(f"   Working Dir: {working_dir}")
    print()

    launcher = resolve_launcher_command(agent_config.get('launcher', ''))

    print(f"⏳ Waiting for CLI to be ready...")
    if not wait_for_prompt(agent_id, launcher, timeout=30):
        print(f"⚠️  Timeout waiting for CLI prompt")
        if not session_exists(agent_id):
            print(f"❌ Agent session exited during startup")
            return 1
        if use_cli_system_prompt:
            print(f"   Continuing: system prompt injected via {system_prompt_flag}; CLI may still be starting...")
        else:
            if system_prompt:
                print(f"   System prompt not injected. Agent may still be starting...")
            return 1

    if system_prompt and not did_provider_restore:
        if use_cli_system_prompt:
            print(f"✅ CLI ready (system prompt injected via {system_prompt_flag})")
        else:
            if get_provider_key(launcher) == 'codex':
                print("❌ Codex system prompt injection is configured as CLI-only (no tmux_paste fallback)")
                return 1

            print(f"✅ CLI ready, injecting system prompt via tmux...")

            if not inject_system_prompt(agent_id, system_prompt):
                print(f"❌ Failed to inject system prompt")
                return 1

            skills = agent_config.get('skills', [])
            if skills:
                print(f"   System prompt injected ({len(system_prompt)} chars, {len(skills)} skills)")
            else:
                print(f"   System prompt injected ({len(system_prompt)} chars)")
    elif system_prompt and did_provider_restore:
        print(f"ℹ️  Provider session restored; skipping system prompt injection")
    else:
        print(f"ℹ️  No system prompt configured for this agent")

    if track_provider_session:
        if did_provider_restore:
            session_id = load_provider_session_id(repo_root, provider_key, agent_id)
            if session_id:
                save_provider_session_id(repo_root, provider_key, agent_id, session_id=session_id, cwd=working_dir)
        else:
            new_session_id = find_new_provider_session_id_with_retry(
                provider_key,
                working_dir,
                before_paths=provider_before_sessions,
                agent_id=agent_id,
                timeout_s=2.0,
            )
            if new_session_id:
                save_provider_session_id(repo_root, provider_key, agent_id, session_id=new_session_id, cwd=working_dir)

    print(f"⏳ Waiting for agent to be ready...")
    agent_ready = wait_for_agent_ready(agent_id, launcher, timeout=45)
    if agent_ready:
        print(f"✅ Agent is ready!")
    else:
        print(f"⚠️  Agent readiness timeout, but may still be processing...")

    if not session_exists(agent_id):
        print(f"❌ Agent session exited during startup")
        return 1

    if agent_ready and getattr(args, 'restore', True):
        _maybe_drain_main_inbound_after_restore(deps, agent_id=agent_id)

    print()
    print(f"Attach with: tmux attach -t {session_name}")
    print(f"Monitor with: python3 {_script_name(deps)} monitor {agent_file_id}")

    return 0


def cmd_stop(args, *, deps: Any):
    """Stop a running agent."""
    check_tmux = deps.check_tmux
    resolve_agent = deps.resolve_agent
    get_agent_id = deps.get_agent_id
    session_exists = deps.session_exists
    stop_session = deps.stop_session

    if not check_tmux():
        print("❌ tmux is not installed")
        return 1

    agent_config = resolve_agent(args.agent)
    if not agent_config:
        print(f"❌ Agent not found: {args.agent}")
        return 1

    agent_name = agent_config['name']
    agent_id = get_agent_id(agent_config)

    if not session_exists(agent_id):
        print(f"⚠️  Agent '{agent_name}' is not running")
        return 1

    if not stop_session(agent_id):
        print(f"❌ Failed to stop agent '{agent_name}'")
        return 1

    session_name = _session_label(agent_id)
    print(f"✅ Agent '{agent_name}' stopped")
    print(f"   Session {session_name}({agent_name}) terminated")
    return 0


def cmd_monitor(args, *, deps: Any):
    """Monitor agent output."""
    check_tmux = deps.check_tmux
    resolve_agent = deps.resolve_agent
    get_agent_id = deps.get_agent_id
    capture_output = deps.capture_output
    time = deps.time

    if not check_tmux():
        print("❌ tmux is not installed")
        return 1

    agent_config = resolve_agent(args.agent)
    if not agent_config:
        print(f"❌ Agent not found: {args.agent}")
        return 1

    agent_name = agent_config['name']
    agent_id = get_agent_id(agent_config)

    if args.follow:
        session_name = _session_label(agent_id)
        print(f"📺 Following output for {session_name}({agent_name}) (Ctrl+C to stop)...")
        print()

        last_output = ""
        try:
            while True:
                output = capture_output(agent_id, args.lines)
                if output is None:
                    print(f"⚠️  Agent '{agent_name}' is not running")
                    return 1

                if output != last_output:
                    if last_output:
                        new_lines = output[len(last_output):]
                        print(new_lines, end='')
                    else:
                        print(output, end='')
                    last_output = output

                time.sleep(2)
        except KeyboardInterrupt:
            print("\n\n⏹  Monitoring stopped")
    else:
        output = capture_output(agent_id, args.lines)
        if output is None:
            print(f"⚠️  Agent '{agent_name}' is not running")
            return 1

        session_name = _session_label(agent_id)
        print(f"📺 Last {args.lines} lines from {session_name}({agent_name}):")
        print("=" * 60)
        print(output)
        print("=" * 60)

    return 0


def cmd_send(args, *, deps: Any):
    """Send message to agent."""
    resolve_agent = deps.resolve_agent
    get_agent_id = deps.get_agent_id
    check_tmux = deps.check_tmux
    session_exists = deps.session_exists
    Path = deps.Path
    resolve_launcher_command = deps.resolve_launcher_command
    should_use_codex_file_pointer = deps._should_use_codex_file_pointer
    get_repo_root = deps.get_repo_root
    write_codex_message_file = deps.write_codex_message_file
    send_keys = deps.send_keys

    agent_config = resolve_agent(args.agent)
    if not agent_config:
        print(f"❌ Agent not found: {args.agent}")
        return 1

    agent_name = agent_config['name']
    agent_id = get_agent_id(agent_config)
    queue_repo_root, queue_message_id = _queue_main_inbound_message(
        deps,
        agent_id=agent_id,
        source='send',
        message_kind='message',
        message=args.message,
    )

    if not check_tmux():
        print("❌ tmux is not installed")
        return 1

    if not session_exists(agent_id):
        print(f"⚠️  Agent '{agent_name}' is not running")
        print(f"   Start with: python3 {Path(deps.__file__).name} start {agent_config.get('file_id', agent_name)}")
        return 1

    launcher = resolve_launcher_command(agent_config.get('launcher', ''))
    is_codex = 'codex' in launcher.lower()
    runtime_snapshot = _probe_runtime_state(deps, agent_id=agent_id, launcher=launcher)
    if runtime_snapshot is not None:
        runtime_state, runtime_reason = runtime_snapshot
        if runtime_state != 'idle':
            print(
                f"⚠️  Agent '{agent_name}' runtime is {runtime_state} ({runtime_reason}); "
                "message may be delayed or ignored"
            )

    outgoing_message = args.message
    if is_codex and should_use_codex_file_pointer(outgoing_message):
        repo_root = get_repo_root()
        message_file = write_codex_message_file(repo_root, agent_id, 'send', outgoing_message)
        outgoing_message = (
            f"Read and execute the message from file: {message_file}\n"
            "After completing it, summarize key results."
        )
        print(f"ℹ️  Codex long message detected; using file pointer: {message_file}")

    _mark_main_inbound_resumed_if_needed(
        deps,
        queue_repo_root,
        agent_id=agent_id,
        message_id=queue_message_id,
        detail='message_dispatch_resumed',
    )
    _mark_main_inbound_state(
        deps,
        queue_repo_root,
        agent_id=agent_id,
        message_id=queue_message_id,
        state='dispatching',
        detail='tmux_send_start',
    )
    if not send_keys(
        agent_id,
        outgoing_message,
        send_enter=args.send_enter,
        clear_input=is_codex,
        escape_first=is_codex,
        enter_via_key=is_codex,
    ):
        _mark_main_inbound_state(
            deps,
            queue_repo_root,
            agent_id=agent_id,
            message_id=queue_message_id,
            state='failed',
            detail='send_keys_failed',
        )
        print(f"❌ Failed to send message to {agent_name}")
        return 1

    _mark_main_inbound_state(
        deps,
        queue_repo_root,
        agent_id=agent_id,
        message_id=queue_message_id,
        state='dispatched',
        detail='tmux_send_ok',
    )
    print(f"✅ Message sent to {agent_name}")
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
        _mark_main_inbound_state(
            deps,
            queue_repo_root,
            agent_id=agent_id,
            message_id=queue_message_id,
            state='handled',
            detail=f"delivery_confirmed:{observed_state}:{observed_reason}",
        )
        _mark_main_inbound_replied(
            deps,
            queue_repo_root,
            agent_id=agent_id,
            message_id=queue_message_id,
            detail='reply_audit_closed:send',
            reply_evidence=reply_evidence,
            transport_ack_status=transport_ack_status,
            transport_ack_detail=transport_ack_detail,
        )
    if not delivery_confirmed:
        print(
            f"⚠️  Delivery unconfirmed: agent remained idle after send "
            f"(state={observed_state}, reason={observed_reason})"
        )

    if outgoing_message == args.message:
        print(f"   Message: {args.message}")
    else:
        print(f"   Original message length: {len(args.message)} chars")
    print()
    print(f"Monitor response: python3 {Path(deps.__file__).name} monitor {agent_name}")
    return 0


def cmd_assign(args, *, deps: Any, start_handler: Optional[Callable] = None):
    """Assign task to agent."""
    resolve_agent = deps.resolve_agent
    get_agent_id = deps.get_agent_id
    check_tmux = deps.check_tmux
    session_exists = deps.session_exists
    argparse = deps.argparse
    time = deps.time
    resolve_launcher_command = deps.resolve_launcher_command
    should_use_codex_file_pointer = deps._should_use_codex_file_pointer
    get_repo_root = deps.get_repo_root
    write_codex_message_file = deps.write_codex_message_file
    send_keys = deps.send_keys
    Path = deps.Path
    sys = deps.sys

    if start_handler is None:
        start_handler = deps.cmd_start

    agent_config = resolve_agent(args.agent)
    if not agent_config:
        print(f"❌ Agent not found: {args.agent}")
        return 1

    agent_name = agent_config['name']
    agent_id = get_agent_id(agent_config)

    if args.task_file:
        try:
            with open(args.task_file, 'r') as f:
                task = f.read()
        except FileNotFoundError:
            print(f"❌ Task file not found: {args.task_file}")
            return 1
    else:
        task = sys.stdin.read()

    if not task.strip():
        print("❌ Task cannot be empty")
        print("   Provide task via stdin or --task-file")
        return 1

    queue_repo_root, queue_message_id = _queue_main_inbound_message(
        deps,
        agent_id=agent_id,
        source='assign',
        message_kind='task_assignment',
        message=task,
    )

    if not check_tmux():
        print("❌ tmux is not installed")
        return 1

    if not session_exists(agent_id):
        print(f"⚠️  Agent {agent_name} is not running. Starting...")

        start_args = argparse.Namespace(
            agent=args.agent,
            working_dir=None,
        )

        if start_handler(start_args) != 0:
            return 1

        print()
        time.sleep(3)

    launcher = resolve_launcher_command(agent_config.get('launcher', ''))
    is_codex = 'codex' in launcher.lower()
    runtime_snapshot = _probe_runtime_state(deps, agent_id=agent_id, launcher=launcher)
    if runtime_snapshot is not None:
        runtime_state, runtime_reason = runtime_snapshot
        if runtime_state != 'idle':
            print(
                f"⚠️  Agent '{agent_name}' runtime is {runtime_state} ({runtime_reason}); "
                "assignment may be delayed or ignored"
            )

    task_message = f"# Task Assignment\n\n{task}"
    if is_codex and should_use_codex_file_pointer(task_message):
        repo_root = get_repo_root()
        task_file = write_codex_message_file(repo_root, agent_id, 'assign', task_message)
        task_message = (
            f"Task assignment received. Read and follow instructions from file: {task_file}\n"
            "Execute the task now and report progress/blocks."
        )
        print(f"ℹ️  Codex long assignment detected; using file pointer: {task_file}")

    _mark_main_inbound_resumed_if_needed(
        deps,
        queue_repo_root,
        agent_id=agent_id,
        message_id=queue_message_id,
        detail='assignment_dispatch_resumed',
    )
    _mark_main_inbound_state(
        deps,
        queue_repo_root,
        agent_id=agent_id,
        message_id=queue_message_id,
        state='dispatching',
        detail='tmux_assign_start',
    )
    if not send_keys(
        agent_id,
        task_message,
        send_enter=True,
        clear_input=is_codex,
        escape_first=is_codex,
        enter_via_key=is_codex,
    ):
        _mark_main_inbound_state(
            deps,
            queue_repo_root,
            agent_id=agent_id,
            message_id=queue_message_id,
            state='failed',
            detail='assign_send_keys_failed',
        )
        print(f"❌ Failed to assign task to {agent_name}")
        return 1

    _mark_main_inbound_state(
        deps,
        queue_repo_root,
        agent_id=agent_id,
        message_id=queue_message_id,
        state='dispatched',
        detail='tmux_assign_ok',
    )
    print(f"✅ Task assigned to {agent_name}")
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
        _mark_main_inbound_state(
            deps,
            queue_repo_root,
            agent_id=agent_id,
            message_id=queue_message_id,
            state='handled',
            detail=f"delivery_confirmed:{observed_state}:{observed_reason}",
        )
        _mark_main_inbound_replied(
            deps,
            queue_repo_root,
            agent_id=agent_id,
            message_id=queue_message_id,
            detail='reply_audit_closed:assign',
            reply_evidence=reply_evidence,
            transport_ack_status=transport_ack_status,
            transport_ack_detail=transport_ack_detail,
        )
    if not delivery_confirmed:
        print(
            f"⚠️  Delivery unconfirmed: agent remained idle after assign "
            f"(state={observed_state}, reason={observed_reason})"
        )

    print()
    print(f"Monitor progress: python3 {Path(deps.__file__).name} monitor {agent_name} --follow")
    return 0
