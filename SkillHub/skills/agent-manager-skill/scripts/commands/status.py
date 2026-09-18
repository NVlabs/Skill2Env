from __future__ import annotations
import json
import re
from typing import Any, Optional


def _session_label(agent_id: str) -> str:
    return 'main' if str(agent_id).strip().lower() == 'main' else f"agent-{agent_id}"


def _heartbeat_audit_path(repo_root, agent_id: str):
    return repo_root / '.claude' / 'state' / 'agent-manager' / 'heartbeat-audit' / f"{agent_id}.jsonl"


def _dream_audit_path(repo_root, agent_id: str):
    return repo_root / '.claude' / 'state' / 'agent-manager' / 'dream-audit' / f"{agent_id}.jsonl"


def _dream_state_path(repo_root, agent_id: str):
    return repo_root / '.claude' / 'state' / 'agent-manager' / 'dream-state' / f"{agent_id}.json"


def _load_recent_heartbeat_event(repo_root, agent_id: str) -> Optional[dict]:
    audit_file = _heartbeat_audit_path(repo_root, agent_id)
    if not audit_file.exists():
        return None

    try:
        lines = audit_file.read_text(encoding='utf-8').splitlines()
    except Exception:
        return None

    for raw in reversed(lines):
        line = raw.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except Exception:
            continue
        if isinstance(payload, dict):
            return payload

    return None


def _load_recent_dream_event(repo_root, agent_id: str) -> Optional[dict]:
    audit_file = _dream_audit_path(repo_root, agent_id)
    if not audit_file.exists():
        return None

    try:
        lines = audit_file.read_text(encoding='utf-8').splitlines()
    except Exception:
        return None

    for raw in reversed(lines):
        line = raw.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except Exception:
            continue
        if isinstance(payload, dict):
            return payload

    return None


def _load_dream_state(repo_root, agent_id: str) -> Optional[dict]:
    path = _dream_state_path(repo_root, agent_id)
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return None
    return payload if isinstance(payload, dict) else None


def _extract_recent_hb_id_from_output(output: str) -> str:
    if not output:
        return ""

    inline_matches = re.findall(r"\[HB_ID:([A-Za-z0-9_-]+)\]", output)
    if inline_matches:
        return str(inline_matches[-1])

    plain_matches = re.findall(r"HB_ID:\s*([A-Za-z0-9_-]+)", output)
    if plain_matches:
        return str(plain_matches[-1])

    return ""


def cmd_status(args, *, deps: Any):
    check_tmux = deps.check_tmux
    resolve_agent = deps.resolve_agent
    get_agent_id = deps.get_agent_id
    session_exists = deps.session_exists
    resolve_launcher_command = deps.resolve_launcher_command
    get_session_info = deps.get_session_info
    get_agent_runtime_state = deps.get_agent_runtime_state
    get_repo_root = deps.get_repo_root
    capture_output = deps.capture_output

    if not check_tmux():
        print("❌ tmux is not installed")
        return 1

    agent_config = resolve_agent(args.agent)
    if not agent_config:
        print(f"❌ Agent not found: {args.agent}")
        return 1

    agent_name = agent_config['name']
    agent_id = get_agent_id(agent_config)
    enabled = bool(agent_config.get('enabled', True))
    running = session_exists(agent_id)
    launcher = resolve_launcher_command(agent_config.get('launcher', ''))

    default_session_name = _session_label(agent_id)
    session_info = get_session_info(agent_id) if running else None
    session_name = session_info.get('session', default_session_name) if session_info else default_session_name

    if running:
        runtime = get_agent_runtime_state(agent_id, launcher=launcher)
    else:
        runtime = {'state': 'stopped'}

    runtime_state = str(runtime.get('state', 'unknown'))
    runtime_reason = str(runtime.get('reason', '')).strip()
    elapsed_seconds = runtime.get('elapsed_seconds')

    recent_heartbeat = "none"
    recent_heartbeat_detail = ""
    recent_dream = "none"
    dream_window = "none"

    repo_root = get_repo_root()
    event = _load_recent_heartbeat_event(repo_root, agent_id)
    if event:
        hb_id = str(event.get('hb_id') or '').strip()
        timestamp = str(event.get('timestamp') or '').strip()
        send_status = str(event.get('send_status') or 'unknown').strip()
        ack_status = str(event.get('ack_status') or 'unknown').strip()
        if hb_id and timestamp:
            recent_heartbeat = f"{hb_id} ({timestamp})"
        elif hb_id:
            recent_heartbeat = hb_id
        else:
            recent_heartbeat = "recorded (missing hb_id)"
        recent_heartbeat_detail = f"send={send_status} ack={ack_status}"
    elif running:
        tail = capture_output(agent_id, lines=220) or ""
        hb_id = _extract_recent_hb_id_from_output(tail)
        if hb_id:
            recent_heartbeat = f"{hb_id} (from tmux output)"

    dream_event = _load_recent_dream_event(repo_root, agent_id)
    dream_state = _load_dream_state(repo_root, agent_id)
    if dream_event:
        recent_dream = str(dream_event.get('event') or 'recorded')
        if dream_event.get('dream_id'):
            recent_dream += f" ({dream_event.get('dream_id')})"
    if dream_state and dream_state.get('window_id'):
        status = 'triggered' if dream_state.get('triggered_for_window') else 'active'
        dream_window = f"{dream_state.get('window_id')} ({status})"

    print(f"📌 Status: {agent_name}")
    print(f"   Agent ID: {agent_id}")
    print(f"   Enabled: {'yes' if enabled else 'no'}")
    print(f"   Running: {'yes' if running else 'no'}")
    print(f"   Session: {session_name}({agent_name})" if running else f"   Session: {session_name} (not running)")
    print(f"   Runtime state: {runtime_state}")
    if runtime_reason:
        print(f"   Runtime reason: {runtime_reason}")
    if elapsed_seconds is not None:
        print(f"   Runtime elapsed: {elapsed_seconds}s")
    print(f"   Recent heartbeat: {recent_heartbeat}")
    if recent_heartbeat_detail:
        print(f"   Heartbeat detail: {recent_heartbeat_detail}")
    print(f"   Recent dream: {recent_dream}")
    print(f"   Dream window: {dream_window}")

    return 0
