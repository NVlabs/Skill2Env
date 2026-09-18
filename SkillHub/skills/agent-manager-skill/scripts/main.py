#!/usr/bin/env python3
"""
Agent Manager - CLI for managing employee agents in tmux sessions.

A simple alternative to CAO using only tmux + Python.
Sessions are named: agent-{agent_id} where agent_id is file_id in lowercase (e.g., emp-0001)
"""

from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from agent_config import (
    resolve_agent,
    list_all_agents,
    load_skills,
    build_system_prompt,
    expand_env_vars,
    get_launcher_command,
    get_agent_schedule,
    get_schedule_task,
    parse_duration,
)

from repo_root import get_repo_root
from tmux_helper import (
    check_tmux,
    list_sessions,
    session_exists,
    start_session,
    start_session_with_layout,
    stop_session,
    capture_output,
    send_keys,
    get_session_info,
    wait_for_prompt,
    inject_system_prompt,
    wait_for_agent_ready,
    get_agent_runtime_state,
    recover_codex_interrupted,
    stabilize_codex_session,
)

# Import provider system (lives at .agent/skills/agent-manager/providers)
sys.path.insert(0, str(Path(__file__).parent.parent))
from providers import (
    get_system_prompt_mode,
    get_system_prompt_flag,
    get_system_prompt_key,
    get_system_prompt_value_mode,
    get_launcher_config_mode,
    get_launcher_config_flag,
    get_agents_md_mode,
    get_mcp_config_mode,
    get_mcp_config_flag,
    resolve_launcher_command,
    get_provider_key,
    get_session_restore_mode,
    get_session_restore_flag,
    get_context_left_patterns,
)

from cli_parser import create_parser
from command_registry import get_command_handlers
from commands.lifecycle import (
    cmd_start as lifecycle_cmd_start,
    cmd_stop as lifecycle_cmd_stop,
    cmd_monitor as lifecycle_cmd_monitor,
    cmd_send as lifecycle_cmd_send,
    cmd_assign as lifecycle_cmd_assign,
)
from commands.inbound import (
    cmd_inbound as inbound_cmd_inbound,
    drain_main_inbound_once as inbound_drain_main_inbound_once,
)
from commands.dream import cmd_dream as dream_cmd_dream
from services.dream_state import (
    append_dream_audit_event,
    load_dream_state,
    parse_iso8601_utc as dream_parse_iso8601_utc,
    process_heartbeat_for_dream,
    save_dream_state,
)
from services.dream_window import normalize_dream_fixed_windows, resolve_active_dream_window
from services.heartbeat_service import (
    notify_heartbeat_failure as service_notify_heartbeat_failure,
    parse_heartbeat_recovery_policy as service_parse_heartbeat_recovery_policy,
    restart_heartbeat_session_fresh as service_restart_heartbeat_session_fresh,
    run_heartbeat_attempt as service_run_heartbeat_attempt,
)
from services.inbound_queue import (
    append_inbound_reply_closure,
    append_inbound_message_event,
    enqueue_inbound_message,
    has_pending_inbound_messages,
    load_pending_inbound_messages,
    load_replayable_inbound_messages,
    mark_inbound_message_state,
    note_pending_messages_yielded,
    read_inbound_events,
    was_message_yielded,
)
from services.heartbeat_state_machine import (
    RECOVERABLE_FAILURE_TYPES as SERVICE_RECOVERABLE_FAILURE_TYPES,
    classify_heartbeat_ack as service_classify_heartbeat_ack,
    failure_reason_code as service_failure_reason_code,
    should_retry_heartbeat_attempt as service_should_retry_heartbeat_attempt,
)
from commands.status import cmd_status as status_cmd_status
from commands.listing import cmd_list as listing_cmd_list
from commands.doctor import cmd_doctor as doctor_cmd_doctor
from commands.schedule import cmd_schedule as schedule_cmd_schedule
from commands.schedule_run import cmd_schedule_run as schedule_run_cmd_schedule_run
from commands.heartbeat import cmd_heartbeat as heartbeat_cmd_heartbeat
from commands.timer import cmd_timer as timer_cmd_timer


def _normalize_path(path: str) -> str:
    try:
        return str(Path(path).resolve())
    except Exception:
        return os.path.abspath(path)


def _provider_sessions_state_dir(repo_root: Path) -> Path:
    return repo_root / '.claude' / 'state' / 'agent-manager' / 'provider-sessions'


def _load_provider_session_id(repo_root: Path, provider: str, agent_id: str) -> str:
    path = _provider_sessions_state_dir(repo_root) / provider / f"{agent_id}.json"
    try:
        payload = json.loads(path.read_text(encoding='utf-8'))
        session_id = str(payload.get('session_id') or '').strip()
        return session_id
    except Exception:
        return ""


def _save_provider_session_id(repo_root: Path, provider: str, agent_id: str, *, session_id: str, cwd: str) -> None:
    provider_dir = _provider_sessions_state_dir(repo_root) / provider
    provider_dir.mkdir(parents=True, exist_ok=True)
    path = provider_dir / f"{agent_id}.json"
    payload = {
        'provider': provider,
        'agent_id': agent_id,
        'session_id': session_id,
        'cwd': cwd,
        'updated_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding='utf-8')


def _codex_session_owner_marker(agent_id: str) -> str:
    return f"AGENT_MANAGER_OWNER:{str(agent_id or '').strip().lower()}"


def _inject_codex_session_owner_marker(system_prompt: str, agent_id: str) -> str:
    marker = _codex_session_owner_marker(agent_id)
    text = str(system_prompt or '')
    if marker in text:
        return text
    if text:
        return f"{marker}\n\n{text}"
    return marker


def _should_enforce_codex_session_owner(agent_id: str) -> bool:
    return str(agent_id or '').strip().lower() == 'main'


def _droid_sessions_dir_for_cwd(cwd: str) -> Path:
    normalized = _normalize_path(cwd)
    folder_name = "-" + normalized.lstrip('/').replace('/', '-')
    return Path.home() / '.factory' / 'sessions' / folder_name


def _droid_session_jsonl_path(cwd: str, session_id: str) -> Path:
    return _droid_sessions_dir_for_cwd(cwd) / f"{session_id}.jsonl"


def _droid_session_exists(cwd: str, session_id: str) -> bool:
    if not session_id:
        return False
    try:
        return _droid_session_jsonl_path(cwd, session_id).exists()
    except Exception:
        return False


def _snapshot_droid_sessions(cwd: str) -> set[str]:
    sessions_dir = _droid_sessions_dir_for_cwd(cwd)
    if not sessions_dir.exists() or not sessions_dir.is_dir():
        return set()
    return {str(p) for p in sessions_dir.glob('*.jsonl')}


def _extract_droid_session_id_from_jsonl(jsonl_path: Path) -> str:
    try:
        with jsonl_path.open('r', encoding='utf-8') as f:
            for _ in range(10):
                line = f.readline()
                if not line:
                    break
                line = line.strip()
                if not line:
                    continue
                payload = json.loads(line)
                if payload.get('type') == 'session_start':
                    return str(payload.get('id') or '').strip()
        return ""
    except Exception:
        return ""


def _find_new_droid_session_id(cwd: str, *, before_jsonl_paths: set[str]) -> str:
    sessions_dir = _droid_sessions_dir_for_cwd(cwd)
    if not sessions_dir.exists() or not sessions_dir.is_dir():
        return ""

    candidates = [p for p in sessions_dir.glob('*.jsonl') if str(p) not in before_jsonl_paths]
    if not candidates:
        return ""

    newest = max(candidates, key=lambda p: p.stat().st_mtime)
    return _extract_droid_session_id_from_jsonl(newest)


def _find_new_droid_session_id_with_retry(cwd: str, *, before_jsonl_paths: set[str], timeout_s: float = 2.0) -> str:
    deadline = time.time() + max(0.0, float(timeout_s))
    while True:
        session_id = _find_new_droid_session_id(cwd, before_jsonl_paths=before_jsonl_paths)
        if session_id:
            return session_id
        if time.time() >= deadline:
            return ""
        time.sleep(0.2)


_UUID_RE = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")


def _looks_like_uuid(value: str) -> bool:
    return bool(value and _UUID_RE.match(value))


def _claude_projects_dir_for_cwd(cwd: str) -> Path:
    normalized = _normalize_path(cwd)
    folder_name = "-" + normalized.lstrip('/').replace('/', '-')
    return Path.home() / '.claude' / 'projects' / folder_name


def _claude_session_jsonl_path(cwd: str, session_id: str) -> Path:
    return _claude_projects_dir_for_cwd(cwd) / f"{session_id}.jsonl"


def _claude_session_exists(cwd: str, session_id: str) -> bool:
    if not _looks_like_uuid(session_id):
        return False
    try:
        return _claude_session_jsonl_path(cwd, session_id).exists()
    except Exception:
        return False


def _snapshot_claude_sessions(cwd: str) -> set[str]:
    sessions_dir = _claude_projects_dir_for_cwd(cwd)
    if not sessions_dir.exists() or not sessions_dir.is_dir():
        return set()
    return {str(p) for p in sessions_dir.glob('*.jsonl')}


def _extract_claude_session_id_from_jsonl(jsonl_path: Path) -> str:
    try:
        with jsonl_path.open('r', encoding='utf-8') as f:
            for _ in range(10):
                line = f.readline()
                if not line:
                    break
                line = line.strip()
                if not line:
                    continue
                payload = json.loads(line)
                session_id = str(payload.get('sessionId') or payload.get('session_id') or '').strip()
                if _looks_like_uuid(session_id):
                    return session_id
        return ""
    except Exception:
        return ""


def _find_new_claude_session_id(cwd: str, *, before_jsonl_paths: set[str]) -> str:
    sessions_dir = _claude_projects_dir_for_cwd(cwd)
    if not sessions_dir.exists() or not sessions_dir.is_dir():
        return ""

    candidates = [p for p in sessions_dir.glob('*.jsonl') if str(p) not in before_jsonl_paths]
    if not candidates:
        # Best-effort fallback: pick newest session file we can parse.
        candidates = list(sessions_dir.glob('*.jsonl'))
    if not candidates:
        return ""

    for candidate in sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True):
        session_id = _extract_claude_session_id_from_jsonl(candidate)
        if session_id:
            return session_id

    return ""


def _find_new_claude_session_id_with_retry(cwd: str, *, before_jsonl_paths: set[str], timeout_s: float = 2.0) -> str:
    deadline = time.time() + max(0.0, float(timeout_s))
    while True:
        session_id = _find_new_claude_session_id(cwd, before_jsonl_paths=before_jsonl_paths)
        if session_id:
            return session_id
        if time.time() >= deadline:
            return ""
        time.sleep(0.2)


def _codex_sessions_dir() -> Path:
    return Path.home() / '.codex' / 'sessions'


def _read_codex_session_meta(jsonl_path: Path) -> dict[str, str]:
    try:
        with jsonl_path.open('r', encoding='utf-8') as f:
            for _ in range(20):
                line = f.readline()
                if not line:
                    break
                line = line.strip()
                if not line:
                    continue
                payload = json.loads(line)
                if payload.get('type') != 'session_meta':
                    continue
                meta = payload.get('payload') or {}
                base_instructions = meta.get('base_instructions') or {}
                return {
                    'session_id': str(meta.get('id') or '').strip(),
                    'cwd': _normalize_path(str(meta.get('cwd') or '').strip()) if meta.get('cwd') else '',
                    'base_instructions': str(base_instructions.get('text') or ''),
                }
    except Exception:
        pass
    return {}


def _codex_session_file_for_id(session_id: str) -> Optional[Path]:
    if not _looks_like_uuid(session_id):
        return None
    sessions_dir = _codex_sessions_dir()
    if not sessions_dir.exists() or not sessions_dir.is_dir():
        return None
    try:
        for p in sessions_dir.rglob('*.jsonl'):
            if session_id in p.name:
                return p
    except Exception:
        return None
    return None


def _codex_session_matches_owner(jsonl_path: Path, *, cwd: str, agent_id: str) -> bool:
    meta = _read_codex_session_meta(jsonl_path)
    if not meta:
        return False
    expected_cwd = _normalize_path(cwd)
    if meta.get('cwd') != expected_cwd:
        return False
    if not _should_enforce_codex_session_owner(agent_id):
        return True
    marker = _codex_session_owner_marker(agent_id)
    return marker in str(meta.get('base_instructions') or '')


def _codex_session_exists(cwd: str, session_id: str, *, agent_id: str = '') -> bool:
    if not _looks_like_uuid(session_id):
        return False
    session_file = _codex_session_file_for_id(session_id)
    if session_file is None:
        return False
    if agent_id:
        return _codex_session_matches_owner(session_file, cwd=cwd, agent_id=agent_id)
    return True


def _snapshot_codex_sessions(cwd: str) -> set[str]:
    sessions_dir = _codex_sessions_dir()
    if not sessions_dir.exists() or not sessions_dir.is_dir():
        return set()
    return {str(p) for p in sessions_dir.rglob('*.jsonl')}


def _extract_codex_session_id_from_jsonl(jsonl_path: Path) -> str:
    meta = _read_codex_session_meta(jsonl_path)
    session_id = str(meta.get('session_id') or '').strip()
    return session_id if _looks_like_uuid(session_id) else ""


def _find_new_codex_session_id(cwd: str, *, before_jsonl_paths: set[str], agent_id: str) -> str:
    sessions_dir = _codex_sessions_dir()
    if not sessions_dir.exists() or not sessions_dir.is_dir():
        return ""

    candidates = [p for p in sessions_dir.rglob('*.jsonl') if str(p) not in before_jsonl_paths]
    if not candidates:
        candidates = list(sessions_dir.rglob('*.jsonl'))
    if not candidates:
        return ""

    for candidate in sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True):
        if not _codex_session_matches_owner(candidate, cwd=cwd, agent_id=agent_id):
            continue
        session_id = _extract_codex_session_id_from_jsonl(candidate)
        if session_id:
            return session_id

    return ""


def _find_new_codex_session_id_with_retry(
    cwd: str,
    *,
    before_jsonl_paths: set[str],
    agent_id: str,
    timeout_s: float = 2.0,
) -> str:
    deadline = time.time() + max(0.0, float(timeout_s))
    while True:
        session_id = _find_new_codex_session_id(cwd, before_jsonl_paths=before_jsonl_paths, agent_id=agent_id)
        if session_id:
            return session_id
        if time.time() >= deadline:
            return ""
        time.sleep(0.2)


def _opencode_storage_dir() -> Path:
    return Path.home() / '.local' / 'share' / 'opencode' / 'storage'


def _opencode_project_id_for_cwd(cwd: str) -> str:
    normalized = _normalize_path(cwd)
    project_dir = _opencode_storage_dir() / 'project'
    if not project_dir.exists() or not project_dir.is_dir():
        return ""

    for p in project_dir.glob('*.json'):
        try:
            payload = json.loads(p.read_text(encoding='utf-8'))
            worktree = str(payload.get('worktree') or '').strip()
            if worktree and _normalize_path(worktree) == normalized:
                return str(payload.get('id') or p.stem).strip()
        except Exception:
            continue

    return ""


def _opencode_sessions_dir_for_project(project_id: str) -> Path:
    return _opencode_storage_dir() / 'session' / project_id


def _opencode_session_json_path(cwd: str, session_id: str) -> Path:
    project_id = _opencode_project_id_for_cwd(cwd)
    return _opencode_sessions_dir_for_project(project_id) / f"{session_id}.json"


def _opencode_session_exists(cwd: str, session_id: str) -> bool:
    if not session_id or not session_id.startswith('ses_'):
        return False
    project_id = _opencode_project_id_for_cwd(cwd)
    if not project_id:
        return False
    try:
        return (_opencode_sessions_dir_for_project(project_id) / f"{session_id}.json").exists()
    except Exception:
        return False


def _snapshot_opencode_sessions(cwd: str) -> set[str]:
    project_id = _opencode_project_id_for_cwd(cwd)
    if not project_id:
        return set()
    sessions_dir = _opencode_sessions_dir_for_project(project_id)
    if not sessions_dir.exists() or not sessions_dir.is_dir():
        return set()
    return {str(p) for p in sessions_dir.glob('*.json')}


def _extract_opencode_session_id_from_json(json_path: Path) -> str:
    try:
        payload = json.loads(json_path.read_text(encoding='utf-8'))
        session_id = str(payload.get('id') or '').strip()
        if session_id.startswith('ses_'):
            return session_id
        return ""
    except Exception:
        return ""


def _find_new_opencode_session_id(cwd: str, *, before_json_paths: set[str]) -> str:
    project_id = _opencode_project_id_for_cwd(cwd)
    if not project_id:
        return ""
    sessions_dir = _opencode_sessions_dir_for_project(project_id)
    if not sessions_dir.exists() or not sessions_dir.is_dir():
        return ""

    candidates = [p for p in sessions_dir.glob('*.json') if str(p) not in before_json_paths]
    if not candidates:
        candidates = list(sessions_dir.glob('*.json'))
    if not candidates:
        return ""

    for candidate in sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True):
        session_id = _extract_opencode_session_id_from_json(candidate)
        if session_id:
            return session_id

    return ""


def _find_new_opencode_session_id_with_retry(cwd: str, *, before_json_paths: set[str], timeout_s: float = 2.0) -> str:
    deadline = time.time() + max(0.0, float(timeout_s))
    while True:
        session_id = _find_new_opencode_session_id(cwd, before_json_paths=before_json_paths)
        if session_id:
            return session_id
        if time.time() >= deadline:
            return ""
        time.sleep(0.2)


def _provider_session_exists(provider_key: str, cwd: str, session_id: str, *, agent_id: str = '') -> bool:
    if provider_key == 'droid':
        return _droid_session_exists(cwd, session_id)
    if provider_key in {'claude', 'claude-code'}:
        return _claude_session_exists(cwd, session_id)
    if provider_key == 'codex':
        return _codex_session_exists(cwd, session_id, agent_id=agent_id)
    if provider_key == 'opencode':
        return _opencode_session_exists(cwd, session_id)
    return False


def _snapshot_provider_sessions(provider_key: str, cwd: str) -> set[str]:
    if provider_key == 'droid':
        return _snapshot_droid_sessions(cwd)
    if provider_key in {'claude', 'claude-code'}:
        return _snapshot_claude_sessions(cwd)
    if provider_key == 'codex':
        return _snapshot_codex_sessions(cwd)
    if provider_key == 'opencode':
        return _snapshot_opencode_sessions(cwd)
    return set()


def _find_new_provider_session_id_with_retry(
    provider_key: str,
    cwd: str,
    *,
    before_paths: set[str],
    agent_id: str = '',
    timeout_s: float = 2.0,
) -> str:
    if provider_key == 'droid':
        return _find_new_droid_session_id_with_retry(cwd, before_jsonl_paths=before_paths, timeout_s=timeout_s)
    if provider_key in {'claude', 'claude-code'}:
        return _find_new_claude_session_id_with_retry(cwd, before_jsonl_paths=before_paths, timeout_s=timeout_s)
    if provider_key == 'codex':
        return _find_new_codex_session_id_with_retry(
            cwd,
            before_jsonl_paths=before_paths,
            agent_id=agent_id,
            timeout_s=timeout_s,
        )
    if provider_key == 'opencode':
        return _find_new_opencode_session_id_with_retry(cwd, before_json_paths=before_paths, timeout_s=timeout_s)
    return ""


def _apply_session_restore_args(
    provider_key: str,
    launcher: str,
    launcher_args: list[str],
    restore_flag: str,
    session_id: str,
) -> list[str]:
    """Insert provider resume args without breaking wrapper launchers.

    For the repo-local `ccc` wrapper, the first arg is a model/account selector and
    must stay first; claude options follow after.
    """
    launcher_lower = (launcher or "").lower()
    if provider_key == 'codex' and restore_flag == 'resume':
        return ['resume', session_id] + list(launcher_args or [])
    if provider_key == 'claude-code' and 'ccc' in launcher_lower:
        if launcher_args and not str(launcher_args[0]).startswith('-'):
            return [launcher_args[0], restore_flag, session_id] + launcher_args[1:]
    return [restore_flag, session_id] + list(launcher_args or [])


def write_system_prompt_file(repo_root: Path, agent_id: str, system_prompt: str) -> Path:
    state_dir = repo_root / '.claude' / 'state' / 'system-prompts'
    state_dir.mkdir(parents=True, exist_ok=True)
    prompt_file = state_dir / f"{agent_id}.txt"
    prompt_file.write_text(system_prompt + "\n", encoding='utf-8')
    return prompt_file


def write_start_command_script(repo_root: Path, agent_id: str, command: str) -> Path:
    state_dir = repo_root / '.claude' / 'state' / 'agent-manager' / 'start-commands'
    state_dir.mkdir(parents=True, exist_ok=True)
    script_path = state_dir / f"{agent_id}.sh"
    script_path.write_text(
        "#!/usr/bin/env bash\n"
        "set -e\n"
        f"{command}\n",
        encoding='utf-8',
    )
    script_path.chmod(0o755)
    return script_path


def _to_toml_literal(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, str):
        return json.dumps(value)
    if isinstance(value, list):
        return "[" + ", ".join(_to_toml_literal(item) for item in value) + "]"
    if isinstance(value, dict):
        parts = []
        for key, item in value.items():
            parts.append(f"{json.dumps(str(key))} = {_to_toml_literal(item)}")
        return "{ " + ", ".join(parts) + " }"
    raise ValueError(f"Unsupported CLI config value type: {type(value).__name__}")


def _normalize_cli_config_value(*, key: str, value: Any, working_dir: str) -> Any:
    if isinstance(value, str):
        expanded = expand_env_vars(value)
        if key.endswith(('_file', '_path')) and expanded and not Path(expanded).is_absolute():
            return str((Path(working_dir) / expanded).resolve())
        return expanded
    if isinstance(value, list):
        return [_normalize_cli_config_value(key=key, value=item, working_dir=working_dir) for item in value]
    if isinstance(value, dict):
        return {
            str(subkey): _normalize_cli_config_value(key=str(subkey), value=item, working_dir=working_dir)
            for subkey, item in value.items()
        }
    return value


def build_launcher_config_overrides(config: dict, *, working_dir: str) -> dict[str, Any]:
    launcher_config = config.get('launcher_config') or {}
    if launcher_config and not isinstance(launcher_config, dict):
        raise ValueError("Invalid 'launcher_config' in agent config (expected a mapping)")

    return {
        str(key): _normalize_cli_config_value(key=str(key), value=value, working_dir=working_dir)
        for key, value in dict(launcher_config).items()
    }


def write_scheduled_task_file(repo_root: Path, agent_id: str, job: str, task: str) -> Path:
    state_dir = repo_root / '.claude' / 'state' / 'agent-manager' / 'scheduled-tasks' / agent_id
    state_dir.mkdir(parents=True, exist_ok=True)
    safe_job = "".join(ch if (ch.isalnum() or ch in ('-', '_')) else '-' for ch in (job or 'job'))
    task_file = state_dir / f"{safe_job}.md"
    task_file.write_text(task + "\n", encoding='utf-8')
    return task_file


def _should_use_codex_file_pointer(message: str) -> bool:
    if not message:
        return False
    line_count = message.count("\n") + 1
    return line_count >= 12 or len(message) >= 1800


def write_codex_message_file(repo_root: Path, agent_id: str, purpose: str, message: str) -> Path:
    state_dir = repo_root / '.claude' / 'state' / 'agent-manager' / 'codex-messages' / agent_id
    state_dir.mkdir(parents=True, exist_ok=True)
    safe_purpose = "".join(ch if (ch.isalnum() or ch in ('-', '_')) else '-' for ch in (purpose or 'message'))
    ts = int(time.time())
    msg_file = state_dir / f"{safe_purpose}-{ts}.md"
    msg_file.write_text(message + "\n", encoding='utf-8')
    return msg_file



_HEARTBEAT_SESSION_MODES = {"restore", "auto", "fresh", "force"}
_HEARTBEAT_AUTO_CONTEXT_THRESHOLD = 25
_HEARTBEAT_FALLBACK_MODES = {"none", "fresh"}
_HEARTBEAT_RECOVERY_FAILURE_TYPES = set(SERVICE_RECOVERABLE_FAILURE_TYPES)
_CONTEXT_LEFT_PATTERN_CACHE: dict[str, list[re.Pattern]] = {}
_HEARTBEAT_TRACE_MAX_LIMIT = 5000
_DREAM_ID_PATTERN = re.compile(r"\[DREAM_ID:([^\]\s]+)\]")
_HEARTBEAT_AUTO_STARVATION_SKIP_THRESHOLD = 3
_HEARTBEAT_AUTO_STARVATION_LOOKBACK_LIMIT = 32
_HEARTBEAT_MODES = {"normal", "full_speed"}
_HEARTBEAT_PENDING_RESCUE_AGE_SECONDS = 20 * 60
_HEARTBEAT_PENDING_RESCUE_SKIP_THRESHOLD = 3
_HEARTBEAT_PENDING_RESCUE_MIN_DELAY_SECONDS = 5
_FULL_SPEED_HEARTBEAT_DELAY_SECONDS = 5
_FULL_SPEED_STOP_HOOK_STATUS_MESSAGE = "agent-manager full-speed heartbeat hook"
_FULL_SPEED_STOP_HOOK_SKIP_TTL_SECONDS = 180


def _normalize_heartbeat_session_mode(value: object) -> str:
    mode = str(value or "restore").strip().lower()
    if mode in _HEARTBEAT_SESSION_MODES:
        return mode
    return "restore"


def _normalize_heartbeat_mode(value: object) -> str:
    mode = str(value or "normal").strip().lower()
    if mode in _HEARTBEAT_MODES:
        return mode
    return "normal"


def _resolve_auto_starvation_skip_threshold(heartbeat: object) -> Optional[int]:
    if not isinstance(heartbeat, dict):
        return _HEARTBEAT_AUTO_STARVATION_SKIP_THRESHOLD

    raw_value = heartbeat.get('auto_starvation_skip_threshold')
    if raw_value is None:
        recovery = heartbeat.get('recovery')
        if isinstance(recovery, dict):
            raw_value = recovery.get('auto_starvation_skip_threshold')

    if raw_value is None:
        return _HEARTBEAT_AUTO_STARVATION_SKIP_THRESHOLD

    try:
        threshold = int(raw_value)
    except Exception:
        return _HEARTBEAT_AUTO_STARVATION_SKIP_THRESHOLD

    if threshold <= 0:
        return None
    return threshold


def _resolve_codex_config_dir(working_dir: str) -> Path:
    current = Path(working_dir).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / '.git').exists():
            return candidate / '.codex'
    return current / '.codex'


def _heartbeat_stop_hook_skip_file(repo_root: Path, agent_id: str) -> Path:
    safe_agent_id = str(agent_id or 'unknown').strip().lower().replace('_', '-')
    safe_agent_id = re.sub(r'[^a-z0-9_-]+', '-', safe_agent_id)
    return (
        repo_root
        / '.claude'
        / 'state'
        / 'agent-manager'
        / 'stop-hook-skips'
        / f'{safe_agent_id}.json'
    )


def arm_codex_fullspeed_stop_hook_skip(
    agent_ref: object,
    *,
    reason: str,
    ttl_seconds: int = _FULL_SPEED_STOP_HOOK_SKIP_TTL_SECONDS,
) -> bool:
    agent_config = agent_ref if isinstance(agent_ref, dict) else resolve_agent(str(agent_ref or ''))
    if not isinstance(agent_config, dict):
        return False

    heartbeat = agent_config.get('heartbeat')
    if not isinstance(heartbeat, dict):
        return False
    if _normalize_heartbeat_mode(heartbeat.get('mode')) != 'full_speed':
        return False

    launcher = resolve_launcher_command(agent_config.get('launcher', ''))
    if get_provider_key(launcher) != 'codex':
        return False

    agent_id = get_agent_id(agent_config)
    repo_root = get_repo_root()
    skip_file = _heartbeat_stop_hook_skip_file(repo_root, agent_id)
    skip_file.parent.mkdir(parents=True, exist_ok=True)
    expires_at = time.time() + max(1, int(ttl_seconds))
    payload = {
        'agent_id': agent_id,
        'reason': str(reason or ''),
        'expires_at': int(expires_at),
        'created_at': int(time.time()),
    }
    skip_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding='utf-8')
    return True


def _build_fullspeed_stop_hook_command(
    *,
    repo_root: Path,
    agent_file_id: str,
    agent_id: str,
    delay_seconds: int,
) -> str:
    hook_script = Path(__file__).resolve().parent / 'fullspeed_stop_hook.py'
    parts = [
        shlex.quote(sys.executable),
        shlex.quote(str(hook_script)),
        '--agent',
        shlex.quote(str(agent_file_id)),
        '--agent-id',
        shlex.quote(str(agent_id)),
        '--repo-root',
        shlex.quote(str(repo_root)),
        '--delay',
        shlex.quote(str(max(0, int(delay_seconds)))),
    ]
    return " ".join(parts)


def _is_managed_fullspeed_stop_hook(hook: dict[str, Any]) -> bool:
    if str(hook.get('type') or '').strip() != 'command':
        return False
    if str(hook.get('statusMessage') or '').strip() == _FULL_SPEED_STOP_HOOK_STATUS_MESSAGE:
        return True
    command = str(hook.get('command') or '').strip()
    return 'fullspeed_stop_hook.py' in command


def _sync_codex_fullspeed_stop_hook(
    agent_config: dict,
    *,
    working_dir: str,
    repo_root: Optional[Path] = None,
    delay_seconds: int = _FULL_SPEED_HEARTBEAT_DELAY_SECONDS,
) -> dict[str, object]:
    heartbeat = agent_config.get('heartbeat')
    if not isinstance(heartbeat, dict):
        return {'enabled': False, 'reason': 'no_heartbeat'}

    heartbeat_mode = _normalize_heartbeat_mode(heartbeat.get('mode'))
    launcher = resolve_launcher_command(agent_config.get('launcher', ''))
    if get_provider_key(launcher) != 'codex':
        if heartbeat_mode == 'full_speed':
            return {'enabled': False, 'reason': 'unsupported_provider', 'mode': heartbeat_mode}
        return {'enabled': False, 'reason': 'not_codex', 'mode': heartbeat_mode}

    config_dir = _resolve_codex_config_dir(working_dir)
    hooks_path = config_dir / 'hooks.json'
    config_toml_path = config_dir / 'config.toml'
    data: dict[str, Any] = {}
    if hooks_path.exists():
        try:
            loaded = json.loads(hooks_path.read_text(encoding='utf-8'))
        except Exception as exc:
            raise ValueError(f"Invalid Codex hooks file: {hooks_path} ({exc})") from exc
        if not isinstance(loaded, dict):
            raise ValueError(f"Invalid Codex hooks file: {hooks_path} (expected top-level object)")
        data = dict(loaded)

    hooks_section = data.setdefault('hooks', {})
    if not isinstance(hooks_section, dict):
        raise ValueError(f"Invalid Codex hooks file: {hooks_path} (expected 'hooks' object)")

    stop_groups_raw = hooks_section.get('Stop', [])
    if stop_groups_raw is None:
        stop_groups_raw = []
    if not isinstance(stop_groups_raw, list):
        raise ValueError(f"Invalid Codex hooks file: {hooks_path} (expected 'hooks.Stop' array)")

    stop_groups: list[dict[str, Any]] = []
    for group in stop_groups_raw:
        if not isinstance(group, dict):
            raise ValueError(f"Invalid Codex hooks file: {hooks_path} (expected Stop hook group object)")
        group_hooks = group.get('hooks', [])
        if not isinstance(group_hooks, list):
            raise ValueError(f"Invalid Codex hooks file: {hooks_path} (expected Stop group 'hooks' array)")
        filtered_hooks = []
        for hook in group_hooks:
            if not isinstance(hook, dict):
                raise ValueError(f"Invalid Codex hooks file: {hooks_path} (expected hook object)")
            is_managed = _is_managed_fullspeed_stop_hook(hook)
            if not is_managed:
                filtered_hooks.append(hook)
        if filtered_hooks:
            updated_group = dict(group)
            updated_group['hooks'] = filtered_hooks
            stop_groups.append(updated_group)

    updated = False
    previous_stop_groups = hooks_section.get('Stop')
    if stop_groups:
        hooks_section['Stop'] = stop_groups
    else:
        hooks_section.pop('Stop', None)

    if hooks_section:
        data['hooks'] = hooks_section
    else:
        data.pop('hooks', None)
    if previous_stop_groups != hooks_section.get('Stop', None):
        updated = True

    if data:
        config_dir.mkdir(parents=True, exist_ok=True)
        serialized = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        current_text = hooks_path.read_text(encoding='utf-8') if hooks_path.exists() else None
        if current_text != serialized:
            hooks_path.write_text(serialized, encoding='utf-8')
            updated = True
    elif hooks_path.exists():
        hooks_path.unlink()
        updated = True

    return {
        'enabled': True,
        'active': False,
        'reason': 'cleaned',
        'mode': heartbeat_mode,
        'updated': updated,
        'hooks_path': str(hooks_path),
    }


def _get_compiled_context_left_patterns(launcher: str) -> list[re.Pattern]:
    provider_key = get_provider_key(launcher)
    cached = _CONTEXT_LEFT_PATTERN_CACHE.get(provider_key)
    if cached is not None:
        return cached

    compiled: list[re.Pattern] = []
    for raw in get_context_left_patterns(launcher):
        try:
            compiled.append(re.compile(str(raw), re.IGNORECASE))
        except Exception:
            continue

    _CONTEXT_LEFT_PATTERN_CACHE[provider_key] = compiled
    return compiled


def _extract_context_left_percent(output: str, *, launcher: str) -> Optional[int]:
    if not output:
        return None

    patterns = _get_compiled_context_left_patterns(launcher)
    if not patterns:
        return None

    for line in reversed(output.splitlines()):
        for pattern in patterns:
            match = pattern.search(line)
            if not match:
                continue
            captures = list(match.groups()) or [match.group(0)]
            for value in captures:
                try:
                    percent = int(str(value))
                except Exception:
                    continue
                if 0 <= percent <= 100:
                    return percent

    return None


def _detect_agent_context_left_percent(agent_id: str, *, launcher: str) -> Optional[int]:
    output = capture_output(agent_id, lines=220)
    if not output:
        return None
    return _extract_context_left_percent(output, launcher=launcher)


def _should_rollover_heartbeat_session(
    session_mode: str,
    context_left_percent: Optional[int],
    *,
    threshold: int = _HEARTBEAT_AUTO_CONTEXT_THRESHOLD,
) -> bool:
    if session_mode == "fresh":
        return True
    if session_mode != "auto":
        return False
    if context_left_percent is None:
        return False
    return context_left_percent < int(threshold)


def _write_heartbeat_handoff_template(repo_root: Path, agent_id: str, heartbeat_id: str) -> Path:
    state_dir = repo_root / '.claude' / 'state' / 'agent-manager' / 'heartbeat-handoffs' / agent_id
    state_dir.mkdir(parents=True, exist_ok=True)
    handoff_file = state_dir / f"{heartbeat_id}.md"
    template = (
        "# Heartbeat Session Handoff\n\n"
        f"- HB_ID: {heartbeat_id}\n"
        "- Status: pending\n\n"
        "## Current Objective\n- \n\n"
        "## Completed\n- \n\n"
        "## Pending / Blockers\n- \n\n"
        "## Next Action\n- \n\n"
        "## References\n- \n"
    )
    handoff_file.write_text(template, encoding='utf-8')
    return handoff_file


def _heartbeat_handoff_saved(handoff_file: Path) -> bool:
    try:
        content = handoff_file.read_text(encoding='utf-8')
    except Exception:
        return False
    stripped = content.strip()
    if not stripped:
        return False
    if 'Status: saved' in content:
        return True
    if 'Status: pending' not in content and len(stripped) >= 80:
        return True
    return False


def _build_heartbeat_handoff_prompt(handoff_file: Path, heartbeat_id: str) -> str:
    return (
        "Context is low. Before session rollover, persist a concise handoff.\n"
        f"Update file: {handoff_file}\n"
        "Requirements:\n"
        "1) Replace `Status: pending` with `Status: saved`.\n"
        "2) Fill sections: Current Objective, Completed, Pending / Blockers, Next Action, References.\n"
        "3) Keep it concise and actionable.\n"
        f"4) Then reply exactly: HEARTBEAT_HANDOFF_SAVED [HB_ID:{heartbeat_id}]"
    )


def _wait_for_idle_after_handoff(agent_id: str, launcher: str, timeout_seconds: int) -> str:
    deadline = time.time() + max(10, int(timeout_seconds))
    last_state = 'unknown'
    while time.time() < deadline:
        runtime = get_agent_runtime_state(agent_id, launcher=launcher)
        last_state = str(runtime.get('state', 'unknown'))
        if last_state == 'idle':
            return last_state
        if last_state in {'blocked', 'error', 'stuck'}:
            return last_state
        time.sleep(2)
    return last_state


_HEARTBEAT_PREFLIGHT_SAMPLE_COUNT = 3
_HEARTBEAT_PREFLIGHT_SAMPLE_INTERVAL_SECONDS = 2.0
_HEARTBEAT_PREFLIGHT_CAPTURE_LINES = 120

# Pattern to detect an unprocessed heartbeat message still visible in the pane.
# If the pane shows [HB_ID:...] but no subsequent HEARTBEAT_OK for that same id,
# it means a previous heartbeat was injected but not yet consumed by the agent.
_HB_ID_PATTERN = re.compile(r'\[HB_ID:(\d{8}-\d{6})\]')


def _has_pending_heartbeat(pane_output: str, stale_threshold_seconds: int = 900) -> tuple[bool, str]:
    """Check if there is an unprocessed heartbeat message in the pane.

    Returns (True, hb_id) if a HB_ID marker exists without a matching
    HEARTBEAT_OK response after it.  Returns (False, '') otherwise.
    """
    if not pane_output:
        return False, ''

    # Find all HB_ID markers and HEARTBEAT_OK responses in order.
    lines = pane_output.splitlines()
    last_hb_id = ''
    last_hb_line = -1
    last_ok_line = -1

    for i, line in enumerate(lines):
        m = _HB_ID_PATTERN.search(line)
        if m:
            last_hb_id = m.group(1)
            last_hb_line = i
        if 'HEARTBEAT_OK' in line and i > last_hb_line >= 0:
            last_ok_line = i

    if last_hb_line < 0:
        return False, ''

    # Pending if the last HB_ID has no HEARTBEAT_OK after it.
    if last_ok_line <= last_hb_line:
        # HB_ID format: YYYYMMDD-HHMMSS (UTC). If it's stale, allow a new heartbeat.
        # Parsing failures are treated as pending to preserve conservative behavior.
        threshold = max(0, int(stale_threshold_seconds))
        try:
            hb_time = datetime.strptime(last_hb_id, '%Y%m%d-%H%M%S').replace(tzinfo=timezone.utc)
            age_seconds = (datetime.now(timezone.utc) - hb_time).total_seconds()
            if age_seconds >= threshold:
                return False, ''
        except Exception:
            return True, last_hb_id
        return True, last_hb_id

    return False, ''


def _generate_heartbeat_id(now: Optional[datetime] = None) -> str:
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None:
        current = current.replace(tzinfo=timezone.utc)
    current = current.astimezone(timezone.utc)
    return current.strftime('%Y%m%d-%H%M%S')


def _heartbeat_id_age_seconds(heartbeat_id: object, *, now: Optional[datetime] = None) -> Optional[int]:
    text = str(heartbeat_id or '').strip()
    if not text:
        return None
    try:
        hb_time = datetime.strptime(text, '%Y%m%d-%H%M%S').replace(tzinfo=timezone.utc)
    except Exception:
        return None
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None:
        current = current.replace(tzinfo=timezone.utc)
    current = current.astimezone(timezone.utc)
    return max(0, int((current - hb_time).total_seconds()))


def _heartbeat_already_acknowledged(repo_root: Path, *, agent_id: str, heartbeat_id: str) -> bool:
    if not heartbeat_id:
        return False
    events = _read_heartbeat_audit_events(repo_root, agent_id=agent_id, heartbeat_id=heartbeat_id, limit=20)
    for event in events:
        if str(event.get('send_status', '')) != 'ok':
            continue
        if str(event.get('ack_status', '')) in {'ack', 'yielded'}:
            return True
    return False


def _heartbeat_preflight_runtime_state(
    *,
    repo_root: Optional[Path] = None,
    agent_id: str,
    launcher: str,
    sample_count: int = _HEARTBEAT_PREFLIGHT_SAMPLE_COUNT,
    sample_interval_seconds: float = _HEARTBEAT_PREFLIGHT_SAMPLE_INTERVAL_SECONDS,
    capture_lines: int = _HEARTBEAT_PREFLIGHT_CAPTURE_LINES,
) -> tuple[str, str]:
    """Best-effort heartbeat preflight state.

    For auto-mode heartbeat gating we avoid relying on one snapshot only.
    If pane output changes across idle samples, treat the agent as active (busy)
    to prevent heartbeat injection from interrupting an in-progress conversation.

    Also checks for pending (unprocessed) heartbeat messages already in the
    pane buffer to prevent accumulation when the agent hasn't consumed the
    previous heartbeat yet.
    """
    runtime = get_agent_runtime_state(agent_id, launcher=launcher)
    state = str(runtime.get('state', 'unknown'))
    reason = str(runtime.get('reason', 'unknown'))
    if state != 'idle':
        return state, reason

    samples = max(1, int(sample_count))
    interval = max(0.1, float(sample_interval_seconds))
    lines = max(20, int(capture_lines))

    previous_output = capture_output(agent_id, lines=lines)
    if previous_output is None:
        previous_output = ""

    # Check for pending heartbeat in pane before sampling.
    pending, pending_hb_id = _has_pending_heartbeat(previous_output)
    if pending:
        if repo_root is None or not _heartbeat_already_acknowledged(repo_root, agent_id=agent_id, heartbeat_id=pending_hb_id):
            return 'busy', f'pending_heartbeat:{pending_hb_id}'

    for sample_index in range(1, samples):
        time.sleep(interval)

        runtime = get_agent_runtime_state(agent_id, launcher=launcher)
        state = str(runtime.get('state', 'unknown'))
        reason = str(runtime.get('reason', 'unknown'))
        if state != 'idle':
            return state, reason

        current_output = capture_output(agent_id, lines=lines)
        if current_output is None:
            current_output = ""

        if current_output != previous_output:
            return 'busy', f'preflight_pane_changed:{sample_index}'

        previous_output = current_output

    return 'idle', reason




def _heartbeat_audit_dir(repo_root: Path) -> Path:
    return repo_root / '.claude' / 'state' / 'agent-manager' / 'heartbeat-audit'


def _heartbeat_audit_file(repo_root: Path, agent_id: str) -> Path:
    safe_agent_id = str(agent_id or 'unknown').strip().lower() or 'unknown'
    safe_agent_id = re.sub(r'[^a-z0-9_-]+', '-', safe_agent_id)
    return _heartbeat_audit_dir(repo_root) / f"{safe_agent_id}.jsonl"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def _parse_iso8601_utc(value: object) -> Optional[datetime]:
    return dream_parse_iso8601_utc(value)


def _heartbeat_result(*, send_status: str, ack_status: str, failure_type: str) -> str:
    failure = str(failure_type or '').strip().lower()
    if failure:
        return 'failure'

    send = str(send_status or '').strip().lower()
    ack = str(ack_status or '').strip().lower()

    if send == 'ok' and ack == 'ack':
        return 'success'
    if send != 'ok':
        return 'failure'
    if ack in {'timeout', 'blocked', 'no_ack'}:
        return 'failure'
    if ack in {'not_checked', ''}:
        return 'pending'
    return 'unknown'


def _resolve_trace_agent_id(agent_value: Optional[str]) -> Optional[str]:
    if not agent_value:
        return None

    value = str(agent_value).strip()
    if not value:
        return None

    resolved = resolve_agent(value)
    if resolved:
        return get_agent_id(resolved)

    normalized = value.lower()
    if normalized.startswith('agent-'):
        normalized = normalized[len('agent-'):]
    return normalized.replace('_', '-')


def _resolve_trace_time_range(*, since_text: Optional[str], until_text: Optional[str]) -> tuple[Optional[datetime], Optional[datetime]]:
    since = _parse_iso8601_utc(since_text)
    until = _parse_iso8601_utc(until_text)

    if since_text and since is None:
        raise ValueError(f"Invalid --since timestamp: {since_text}")
    if until_text and until is None:
        raise ValueError(f"Invalid --until timestamp: {until_text}")
    if since and until and since > until:
        raise ValueError("Invalid time range: --since cannot be later than --until")

    return since, until


def _append_heartbeat_audit_event(
    repo_root: Path,
    *,
    agent_id: str,
    heartbeat_id: str,
    send_status: str,
    ack_status: str,
    duration_ms: int,
    context_left: Optional[int],
    failure_type: str = "",
    session_mode: str = "",
    phase: str = "",
    attempt: int = 0,
    recovery_action: str = "",
    reason_code: str = "",
    ack_evidence: str = "",
    timestamp: Optional[str] = None,
) -> Path:
    audit_file = _heartbeat_audit_file(repo_root, agent_id)
    audit_file.parent.mkdir(parents=True, exist_ok=True)

    duration_value = int(max(0, duration_ms))
    event = {
        'timestamp': timestamp or _utc_now_iso(),
        'agent_id': str(agent_id),
        'hb_id': str(heartbeat_id),
        'send_status': str(send_status),
        'ack_status': str(ack_status),
        'duration_ms': duration_value,
        'duration': duration_value,
        'context_left': context_left if isinstance(context_left, int) else None,
        'failure_type': str(failure_type or ''),
        'session_mode': str(session_mode or ''),
        'phase': str(phase or ''),
        'stage': str(phase or 'heartbeat_attempt'),
        'result': _heartbeat_result(send_status=send_status, ack_status=ack_status, failure_type=failure_type),
        'attempt': int(max(0, attempt)),
        'recovery_action': str(recovery_action or ''),
        'reason_code': str(reason_code or ''),
        'ack_evidence': str(ack_evidence or ''),
    }

    with audit_file.open('a', encoding='utf-8') as fp:
        fp.write(json.dumps(event, ensure_ascii=False) + "\n")
    return audit_file


def _read_heartbeat_audit_events(
    repo_root: Path,
    *,
    heartbeat_id: Optional[str] = None,
    agent_id: Optional[str] = None,
    since: Optional[datetime] = None,
    until: Optional[datetime] = None,
    limit: int = 20,
) -> list[dict]:
    trace_limit = max(1, min(_HEARTBEAT_TRACE_MAX_LIMIT, int(limit or 20)))
    audit_dir = _heartbeat_audit_dir(repo_root)
    if not audit_dir.exists() or not audit_dir.is_dir():
        return []

    hb_filter = str(heartbeat_id or '').strip()
    agent_filter = str(agent_id or '').strip().lower()

    files: list[Path]
    if agent_filter:
        files = [_heartbeat_audit_file(repo_root, agent_filter)]
    else:
        files = sorted(audit_dir.glob('*.jsonl'))

    events: list[dict] = []
    for path in files:
        if not path.exists() or not path.is_file():
            continue
        try:
            with path.open('r', encoding='utf-8') as fp:
                for line in fp:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        payload = json.loads(line)
                    except Exception:
                        continue
                    if not isinstance(payload, dict):
                        continue
                    if hb_filter and str(payload.get('hb_id', '')) != hb_filter:
                        continue
                    if agent_filter and str(payload.get('agent_id', '')).lower() != agent_filter:
                        continue

                    event_ts = _parse_iso8601_utc(payload.get('timestamp'))
                    if since and (event_ts is None or event_ts < since):
                        continue
                    if until and (event_ts is None or event_ts > until):
                        continue

                    events.append(payload)
        except Exception:
            continue

    events.sort(key=lambda item: str(item.get('timestamp', '')), reverse=True)
    return events[:trace_limit]


def _parse_dream_policy(heartbeat: dict) -> dict:
    defaults = {
        'enabled': False,
        'idle_after': '1h',
        'idle_after_seconds': 3600,
        'max_runtime': '',
        'max_runtime_seconds': None,
        'fixed_windows': [],
    }
    raw = heartbeat.get('dream') if isinstance(heartbeat, dict) else {}
    if not isinstance(raw, dict):
        return dict(defaults)

    idle_after_text = str(raw.get('idle_after', defaults['idle_after']) or defaults['idle_after']).strip()
    idle_after_seconds = parse_duration(idle_after_text) or defaults['idle_after_seconds']
    max_runtime_text = str(raw.get('max_runtime', defaults['max_runtime']) or '').strip()
    max_runtime_seconds = parse_duration(max_runtime_text) if max_runtime_text else None
    fixed_windows = normalize_dream_fixed_windows(raw)
    return {
        'enabled': bool(raw.get('enabled', defaults['enabled'])),
        'idle_after': idle_after_text,
        'idle_after_seconds': int(idle_after_seconds),
        'max_runtime': max_runtime_text,
        'max_runtime_seconds': max_runtime_seconds,
        'fixed_windows': fixed_windows,
    }


def _parse_simple_cron_interval_seconds(cron_expr: str) -> Optional[int]:
    text = str(cron_expr or '').strip()
    if not text:
        return None
    parts = text.split()
    if len(parts) != 5:
        return None
    minute, hour, day, month, weekday = parts
    if minute.startswith('*/') and hour == '*' and day == '*' and month == '*' and weekday == '*':
        try:
            return int(minute[2:]) * 60
        except Exception:
            return None
    if minute.isdigit() and hour.startswith('*/') and day == '*' and month == '*' and weekday == '*':
        try:
            return int(hour[2:]) * 3600
        except Exception:
            return None
    if minute.isdigit() and hour.isdigit() and day.startswith('*/') and month == '*' and weekday == '*':
        try:
            return int(day[2:]) * 86400
        except Exception:
            return None
    return None


def _has_direct_dream_ack(output: str, dream_id: str) -> bool:
    if not dream_id:
        return False
    marker = f"[DREAM_ID:{dream_id}]"
    for line in str(output or '').splitlines():
        normalized = line.strip()
        if 'DREAM_OK' not in normalized or marker not in normalized:
            continue
        lower = normalized.lower()
        if 'reply dream_ok' in lower or 'read dream.md' in lower or 'if nothing worth doing' in lower:
            continue
        if re.search(r'(?:^|[\s•\-])DREAM_OK(?:[\s.!?]+|\s*)' + re.escape(marker), normalized):
            return True
    return False


def _tail_hash(output: str) -> str:
    return hashlib.sha1(str(output or '').encode('utf-8')).hexdigest()


def _dream_completion_evidence(output: str, *, dream_id: str, baseline_hash: str) -> str:
    tail_hash = _tail_hash(output)
    tail_short = tail_hash[:12]
    if _has_direct_dream_ack(output, dream_id):
        return f'direct_dream_ok:tail_sha1={tail_short}'
    if tail_hash != baseline_hash:
        return f'pane_tail_changed:tail_sha1={tail_short}'
    return f'pane_tail_unchanged:tail_sha1={tail_short}'


def _build_dream_prompt(*, dream_id: str, trigger_hb_id: str) -> str:
    prompt = (
        "Read DREAM.md if it exists (workspace context). Follow it strictly. "
        "Do not infer or repeat old tasks from prior chats. "
        "If nothing worth doing emerges, reply DREAM_OK. "
        f"[DREAM_ID:{dream_id}]"
    )
    if trigger_hb_id:
        prompt += f" [TRIGGER_HB_ID:{trigger_hb_id}]"
    return prompt


def _dream_reason_code(*, send_status: str, ack_status: str, failure_type: str) -> str:
    if str(send_status or '') != 'ok':
        return 'DREAM_SEND_FAILED'
    if str(ack_status or '') == 'ack':
        return 'DREAM_ACK_OK'
    if str(ack_status or '') == 'not_checked':
        return 'DREAM_NOT_CHECKED'
    failure = str(failure_type or '').strip()
    if failure == 'timeout':
        return 'DREAM_TIMEOUT'
    if failure == 'user_queue_yield':
        return 'DREAM_USER_QUEUE_YIELD'
    if failure:
        return f"DREAM_{failure.upper()}"
    return 'DREAM_NO_ACK'


def _schedule_dream_run(
    *,
    agent_file_id: str,
    window_id: str,
    trigger_hb_id: str,
    timeout_text: str,
) -> int:
    command_args = ['--', 'dream', 'run', agent_file_id, '--window-id', window_id, '--trigger-hb-id', trigger_hb_id]
    if timeout_text:
        command_args.extend(['--timeout', timeout_text])
    timer_args = argparse.Namespace(
        timer_command='command',
        delay='1s',
        command_args=command_args,
    )
    return cmd_timer(timer_args)


def _maybe_trigger_dream_from_heartbeat(
    *,
    repo_root: Path,
    agent_config: dict,
    agent_id: str,
    agent_file_id: str,
    heartbeat: dict,
    heartbeat_id: str,
    heartbeat_timestamp: str,
    ack_status: str,
    ack_evidence: str,
    failure_type: str,
) -> None:
    policy = _parse_dream_policy(heartbeat)
    if not policy['enabled']:
        return
    fixed_window = resolve_active_dream_window(policy)
    if fixed_window.get('active'):
        return

    state = load_dream_state(repo_root, agent_id)
    processed = process_heartbeat_for_dream(
        state=state,
        agent_id=agent_id,
        heartbeat_id=heartbeat_id,
        heartbeat_timestamp=heartbeat_timestamp,
        ack_status=ack_status,
        ack_evidence=ack_evidence,
        failure_type=failure_type,
        idle_after_seconds=int(policy['idle_after_seconds']),
        configured_heartbeat_interval_seconds=_parse_simple_cron_interval_seconds(heartbeat.get('cron', '')),
    )
    next_state = dict(processed['state'])
    event = str(processed.get('event') or '')
    reason_code = str(processed.get('reason_code') or '')
    effective_idle_elapsed = int(processed.get('effective_idle_elapsed') or 0)
    if event:
        append_dream_audit_event(
            repo_root,
            agent_id=agent_id,
            event=event,
            window_id=str(next_state.get('window_id') or ''),
            hb_id=heartbeat_id,
            reason_code=reason_code,
            detail=f'ack={ack_status}:{ack_evidence}',
            effective_idle_elapsed=effective_idle_elapsed,
        )

    if processed.get('should_trigger'):
        working_dir = _normalize_path(agent_config.get('working_directory') or '')
        dream_file = Path(working_dir) / 'DREAM.md' if working_dir else None
        next_state['triggered_for_window'] = True
        next_state['triggered_at'] = heartbeat_timestamp
        next_state['triggered_by_hb_id'] = heartbeat_id
        if not dream_file or not dream_file.exists():
            append_dream_audit_event(
                repo_root,
                agent_id=agent_id,
                event='trigger_skipped_no_dream_file',
                window_id=str(next_state.get('window_id') or ''),
                hb_id=heartbeat_id,
                reason_code='DREAM_NO_FILE',
                detail=str(dream_file or ''),
                effective_idle_elapsed=effective_idle_elapsed,
            )
        else:
            timer_rc = _schedule_dream_run(
                agent_file_id=agent_file_id,
                window_id=str(next_state.get('window_id') or ''),
                trigger_hb_id=heartbeat_id,
                timeout_text=str(policy.get('max_runtime') or ''),
            )
            if timer_rc == 0:
                append_dream_audit_event(
                    repo_root,
                    agent_id=agent_id,
                    event='trigger_scheduled',
                    window_id=str(next_state.get('window_id') or ''),
                    hb_id=heartbeat_id,
                    reason_code='DREAM_TRIGGER_SCHEDULED',
                    detail=f"idle_after={policy['idle_after']}",
                    effective_idle_elapsed=effective_idle_elapsed,
                )
            else:
                next_state['triggered_for_window'] = False
                next_state['triggered_at'] = ''
                next_state['triggered_by_hb_id'] = ''
                append_dream_audit_event(
                    repo_root,
                    agent_id=agent_id,
                    event='run_failed',
                    window_id=str(next_state.get('window_id') or ''),
                    hb_id=heartbeat_id,
                    reason_code='DREAM_TRIGGER_SCHEDULE_FAILED',
                    detail='timer_command_failed',
                    effective_idle_elapsed=effective_idle_elapsed,
                )

    save_dream_state(repo_root, agent_id, next_state)


def _run_dream_attempt(
    *,
    repo_root: Path,
    agent_id: str,
    agent_name: str,
    launcher: str,
    dream_message: str,
    timeout_seconds: Optional[int],
    is_codex: bool,
    dream_id: str,
) -> dict:
    started = time.time()
    baseline_output = capture_output(agent_id, lines=60) or ''
    baseline_hash = _tail_hash(baseline_output)
    final_output = baseline_output

    if not send_keys(
        agent_id,
        dream_message,
        send_enter=True,
        clear_input=is_codex,
        escape_first=is_codex,
        enter_via_key=is_codex,
    ):
        failure_type = 'send_fail'
        return {
            'send_status': 'fail',
            'ack_status': 'not_checked',
            'ack_evidence': 'none',
            'failure_type': 'send_fail',
            'reason_code': _dream_reason_code(
                send_status='fail',
                ack_status='not_checked',
                failure_type=failure_type,
            ),
            'duration_ms': int((time.time() - started) * 1000),
        }

    waited_for_ack = bool(timeout_seconds and timeout_seconds > 0)
    last_state: Optional[str] = None
    activated = False
    direct_ack = False
    timed_out = False
    if waited_for_ack:
        start_time = time.time()
        activation_timeout = min(60, int(timeout_seconds))
        time.sleep(2)
        while (time.time() - start_time) < activation_timeout:
            if has_pending_inbound_messages(repo_root, agent_id=agent_id):
                return {
                    'send_status': 'ok',
                    'ack_status': 'yielded',
                    'ack_evidence': 'yielded',
                    'failure_type': 'user_queue_yield',
                    'reason_code': _dream_reason_code(
                        send_status='ok',
                        ack_status='yielded',
                        failure_type='user_queue_yield',
                    ),
                    'duration_ms': int((time.time() - started) * 1000),
                }
            runtime = get_agent_runtime_state(agent_id, launcher=launcher)
            last_state = str(runtime.get('state', 'unknown'))
            current_output = capture_output(agent_id, lines=60) or ''
            final_output = current_output
            if _has_direct_dream_ack(current_output, dream_id):
                direct_ack = True
                activated = True
                last_state = 'idle'
                break
            if last_state != 'idle' or _tail_hash(current_output) != baseline_hash:
                activated = True
                break
            time.sleep(2)

        if activated and not direct_ack:
            while (time.time() - start_time) < int(timeout_seconds):
                runtime = get_agent_runtime_state(agent_id, launcher=launcher)
                last_state = str(runtime.get('state', 'unknown'))
                current_output = capture_output(agent_id, lines=60) or ''
                final_output = current_output
                if _has_direct_dream_ack(current_output, dream_id):
                    direct_ack = True
                    last_state = 'idle'
                    break
                if last_state == 'idle':
                    break
                if last_state in {'blocked', 'error', 'stuck', 'interrupted'}:
                    break
                time.sleep(2)
        if last_state != 'idle' and (time.time() - start_time) >= int(timeout_seconds):
            timed_out = True

    if direct_ack:
        ack_status = 'ack'
        ack_evidence = 'direct_dream_ok'
        failure_type = ''
    elif waited_for_ack and timed_out:
        ack_status = 'timeout'
        ack_evidence = 'none'
        failure_type = 'timeout'
    elif waited_for_ack and last_state == 'idle':
        ack_status = 'ack'
        ack_evidence = 'idle_only'
        failure_type = ''
    elif waited_for_ack:
        ack_status = 'no_ack'
        ack_evidence = 'none'
        failure_type = 'no_ack'
    else:
        ack_status = 'not_checked'
        ack_evidence = 'none'
        failure_type = ''

    completion_evidence = _dream_completion_evidence(
        final_output,
        dream_id=dream_id,
        baseline_hash=baseline_hash,
    )
    if ack_status == 'ack' and ack_evidence == 'idle_only' and completion_evidence.startswith('pane_tail_changed:'):
        ack_evidence = 'idle_after_output_change'

    return {
        'send_status': 'ok',
        'ack_status': ack_status,
        'ack_evidence': ack_evidence,
        'completion_evidence': completion_evidence,
        'failure_type': failure_type,
        'reason_code': _dream_reason_code(
            send_status='ok',
            ack_status=ack_status,
            failure_type=failure_type,
        ),
        'duration_ms': int((time.time() - started) * 1000),
    }


def _run_fixed_dream_heartbeat(
    *,
    repo_root: Path,
    agent_config: dict,
    agent_id: str,
    agent_name: str,
    dream_policy: dict,
    heartbeat_id: str,
    rollover_handoff_file: Optional[Path],
    fixed_window: dict,
    fallback_timeout_seconds: Optional[int] = None,
) -> dict:
    """Dispatch a Dream task from a heartbeat fixed window."""
    fixed_window_id = str(fixed_window.get('window_id') or f'fixed-window-{heartbeat_id}')
    fixed_window_summary = str(fixed_window.get('summary') or '')

    working_dir = _normalize_path(agent_config.get('working_directory') or '')
    dream_file = Path(working_dir) / 'DREAM.md' if working_dir else None
    if not dream_file or not dream_file.exists():
        append_dream_audit_event(
            repo_root,
            agent_id=agent_id,
            event='run_stale',
            window_id=fixed_window_id,
            hb_id=heartbeat_id,
            reason_code='DREAM_NO_FILE',
            detail=str(dream_file or ''),
        )
        print("⏭️  DREAM.md not found - skipping fixed Dream window")
        return {
            'send_status': 'skip',
            'ack_status': 'skipped',
            'ack_evidence': 'none',
            'failure_type': 'dream_no_file',
            'reason_code': 'DREAM_NO_FILE',
            'duration_ms': 0,
            'dream_id': '',
            'window_id': fixed_window_id,
            'ran': False,
        }

    if has_pending_inbound_messages(repo_root, agent_id=agent_id):
        append_dream_audit_event(
            repo_root,
            agent_id=agent_id,
            event='run_stale',
            window_id=fixed_window_id,
            hb_id=heartbeat_id,
            reason_code='DREAM_USER_QUEUE_PENDING',
            detail='pending_inbound_messages',
        )
        print("⏭️  Pending inbound user work detected - skipping fixed Dream window")
        return {
            'send_status': 'ok',
            'ack_status': 'yielded',
            'ack_evidence': 'yielded',
            'failure_type': 'user_queue_yield',
            'reason_code': 'DREAM_USER_QUEUE_PENDING',
            'duration_ms': 0,
            'dream_id': '',
            'window_id': fixed_window_id,
            'ran': False,
        }

    launcher = resolve_launcher_command(agent_config.get('launcher', ''))
    timeout_text = str(dream_policy.get('max_runtime') or '').strip()
    timeout_seconds = (
        parse_duration(timeout_text)
        if timeout_text
        else int(dream_policy.get('max_runtime_seconds') or fallback_timeout_seconds or 900)
    )
    if timeout_seconds is None:
        timeout_seconds = 900

    dream_id = time.strftime('%Y%m%d-%H%M%S')
    dream_message = _build_dream_prompt(dream_id=dream_id, trigger_hb_id=heartbeat_id)
    if rollover_handoff_file is not None:
        dream_message = f"First read rollover handoff file: {rollover_handoff_file}.\n" + dream_message

    append_dream_audit_event(
        repo_root,
        agent_id=agent_id,
        event='run_started',
        window_id=fixed_window_id,
        hb_id=heartbeat_id,
        dream_id=dream_id,
        reason_code='DREAM_FIXED_WINDOW_STARTED',
        detail=fixed_window_summary,
    )

    result = _run_dream_attempt(
        repo_root=repo_root,
        agent_id=agent_id,
        agent_name=agent_name,
        launcher=launcher,
        dream_message=dream_message,
        timeout_seconds=timeout_seconds,
        is_codex='codex' in launcher.lower(),
        dream_id=dream_id,
    )

    send_status = str(result.get('send_status', 'fail'))
    ack_status = str(result.get('ack_status', 'not_checked'))
    ack_evidence = str(result.get('ack_evidence', 'none'))
    completion_evidence = str(result.get('completion_evidence', 'none'))
    failure_type = str(result.get('failure_type', ''))
    reason_code = str(result.get('reason_code') or _dream_reason_code(
        send_status=send_status,
        ack_status=ack_status,
        failure_type=failure_type,
    ))
    duration_ms = int(result.get('duration_ms', 0) or 0)

    if send_status == 'ok' and ack_status in {'ack', 'not_checked'} and not failure_type:
        state = load_dream_state(repo_root, agent_id)
        state['last_dream_id'] = dream_id
        save_dream_state(repo_root, agent_id, state)
        append_dream_audit_event(
            repo_root,
            agent_id=agent_id,
            event='run_completed',
            window_id=fixed_window_id,
            hb_id=heartbeat_id,
            dream_id=dream_id,
            reason_code='DREAM_FIXED_WINDOW_OK',
            detail=f'ack={ack_status}:{ack_evidence}; completion={completion_evidence}',
        )
        print("✅ Dream completed successfully (fixed heartbeat window)")
        result['completed'] = True
    else:
        append_dream_audit_event(
            repo_root,
            agent_id=agent_id,
            event='run_failed',
            window_id=fixed_window_id,
            hb_id=heartbeat_id,
            dream_id=dream_id,
            reason_code='DREAM_FIXED_WINDOW_FAILED',
            detail=f'{send_status}:{ack_status}:{failure_type}',
        )
        print(f"❌ Dream failed (send={send_status}, ack={ack_status}, failure={failure_type or 'unknown'})")
        result['completed'] = False

    result.update({
        'ack_evidence': ack_evidence,
        'completion_evidence': completion_evidence,
        'reason_code': reason_code,
        'duration_ms': duration_ms,
        'dream_id': dream_id,
        'window_id': fixed_window_id,
        'ran': True,
    })
    return result


def _is_auto_preflight_skip_event(event: dict) -> bool:
    if not isinstance(event, dict):
        return False
    return (
        str(event.get('session_mode', '')) == 'auto'
        and str(event.get('phase', '')) == 'preflight'
        and str(event.get('send_status', '')) == 'skip'
    )


def _count_consecutive_auto_preflight_skips(
    repo_root: Path,
    *,
    agent_id: str,
    reason_codes: Optional[set[str]] = None,
    limit: int = _HEARTBEAT_AUTO_STARVATION_LOOKBACK_LIMIT,
) -> int:
    events = _read_heartbeat_audit_events(
        repo_root,
        agent_id=agent_id,
        limit=max(1, int(limit or _HEARTBEAT_AUTO_STARVATION_LOOKBACK_LIMIT)),
    )
    count = 0
    for event in events:
        if not _is_auto_preflight_skip_event(event):
            break
        if reason_codes is not None and str(event.get('reason_code', '')) not in reason_codes:
            break
        count += 1
    return count


def _parse_pending_heartbeat_reason(reason: object) -> str:
    text = str(reason or '').strip()
    prefix = 'pending_heartbeat:'
    if not text.startswith(prefix):
        return ''
    return text[len(prefix):].strip()


def cmd_heartbeat_trace(args) -> int:
    """Query heartbeat audit logs by HB_ID and/or agent."""
    repo_root = get_repo_root()

    try:
        since, until = _resolve_trace_time_range(
            since_text=getattr(args, 'since', None),
            until_text=getattr(args, 'until', None),
        )
    except ValueError as e:
        print(f"❌ {e}")
        return 1

    agent_id = _resolve_trace_agent_id(getattr(args, 'agent', None))

    events = _read_heartbeat_audit_events(
        repo_root,
        heartbeat_id=getattr(args, 'hb_id', None),
        agent_id=agent_id,
        since=since,
        until=until,
        limit=getattr(args, 'limit', 20),
    )

    if getattr(args, 'json', False):
        print(json.dumps(events, ensure_ascii=False, indent=2))
        return 0

    if not events:
        print("No heartbeat trace events found.")
        return 0

    print("🔎 Heartbeat Trace Events:")
    for event in events:
        timestamp = str(event.get('timestamp', 'unknown'))
        hb_id = str(event.get('hb_id', 'unknown'))
        event_agent = str(event.get('agent_id', 'unknown'))
        send_status = str(event.get('send_status', 'unknown'))
        ack_status = str(event.get('ack_status', 'unknown'))
        duration_ms = event.get('duration_ms')
        context_left = event.get('context_left')
        failure_type = str(event.get('failure_type', '') or '')
        stage = str(event.get('stage', event.get('phase', 'heartbeat_attempt')))
        result = str(event.get('result', _heartbeat_result(send_status=send_status, ack_status=ack_status, failure_type=failure_type)))

        duration_text = f"{duration_ms}ms" if isinstance(duration_ms, int) else 'n/a'
        context_text = f"{context_left}%" if isinstance(context_left, int) else 'unknown'
        failure_text = failure_type if failure_type else '-'
        print(
            f"- {timestamp} agent={event_agent} hb_id={hb_id} stage={stage} result={result} "
            f"send={send_status} ack={ack_status} duration={duration_text} "
            f"context_left={context_text} failure={failure_text}"
        )
    return 0


def cmd_heartbeat_slo(args) -> int:
    """Summarize heartbeat SLO metrics for daily/weekly windows."""
    from heartbeat_slo import build_slo_summary, format_slo_summary

    try:
        since, until = _resolve_trace_time_range(
            since_text=getattr(args, 'since', None),
            until_text=getattr(args, 'until', None),
        )
    except ValueError as e:
        print(f"❌ {e}")
        return 1

    agent_id = _resolve_trace_agent_id(getattr(args, 'agent', None))

    try:
        summary = build_slo_summary(
            repo_root=get_repo_root(),
            agent_id=agent_id,
            window=str(getattr(args, 'window', 'daily') or 'daily'),
            since=since,
            until=until,
        )
    except ValueError as e:
        print(f"❌ {e}")
        return 1

    if getattr(args, 'json', False):
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(format_slo_summary(summary))
    return 0


def _parse_non_negative_int(value: object, default: int) -> int:
    try:
        parsed = int(value)
    except Exception:
        return int(default)
    return max(0, parsed)


def _parse_bool(value: object, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    text = str(value).strip().lower()
    if text in {'1', 'true', 'yes', 'y', 'on'}:
        return True
    if text in {'0', 'false', 'no', 'n', 'off'}:
        return False
    return default


def _parse_heartbeat_recovery_policy(heartbeat: dict, args: Optional[argparse.Namespace] = None) -> dict:
    return service_parse_heartbeat_recovery_policy(
        heartbeat,
        args=args,
        fallback_modes=_HEARTBEAT_FALLBACK_MODES,
    )


def _classify_heartbeat_ack(*, waited_for_ack: bool, last_state: Optional[str], timed_out: bool) -> tuple[str, str]:
    ack_status, failure_type, _reason_code = service_classify_heartbeat_ack(
        waited_for_ack=waited_for_ack,
        last_state=last_state,
        timed_out=timed_out,
    )
    return ack_status, failure_type


def _should_retry_heartbeat_attempt(*, failure_type: str, attempt_index: int, max_retries: int) -> bool:
    return service_should_retry_heartbeat_attempt(
        failure_type=failure_type,
        attempt_index=attempt_index,
        max_retries=max_retries,
    )


def _resolve_notifier_script(repo_root: Path) -> Optional[Path]:
    candidates = [
        repo_root / '.agent' / 'skills' / 'notifier' / 'scripts' / 'notify.py',
        repo_root / '.claude' / 'skills' / 'notifier' / 'scripts' / 'notify.py',
        Path.home() / '.agent' / 'skills' / 'notifier' / 'scripts' / 'notify.py',
        Path.home() / '.claude' / 'skills' / 'notifier' / 'scripts' / 'notify.py',
    ]
    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate
    return None


def _notify_heartbeat_failure(
    repo_root: Path,
    *,
    channel: str,
    agent_name: str,
    agent_id: str,
    heartbeat_id: str,
    failure_type: str,
) -> bool:
    return service_notify_heartbeat_failure(
        repo_root,
        channel=channel,
        agent_name=agent_name,
        agent_id=agent_id,
        heartbeat_id=heartbeat_id,
        failure_type=failure_type,
    )


def _schedule_pending_heartbeat_rescue_timer(
    *,
    agent_file_id: str,
    pending_heartbeat_id: str,
    delay_seconds: int,
    timeout_seconds: Optional[int],
) -> bool:
    delay = max(_HEARTBEAT_PENDING_RESCUE_MIN_DELAY_SECONDS, int(delay_seconds or 0))
    dedupe_key = f"pending-rescue:{str(agent_file_id or '').strip().lower()}:{pending_heartbeat_id}"
    args = argparse.Namespace(
        timer_command='rescue',
        agent=agent_file_id,
        delay=f'{delay}s',
        timeout=f'{int(timeout_seconds)}s' if timeout_seconds else None,
        reason='auto_pending_heartbeat_rescue',
        no_prime=False,
        fresh=False,
        heartbeat_id=pending_heartbeat_id,
        dedupe_key=dedupe_key,
    )
    return cmd_timer(args) == 0


def _restart_heartbeat_session_restore(agent_file_id: str, agent_name: str, agent_id: str) -> bool:
    print(f"♻️  Restarting '{agent_name}' in restore mode")
    if session_exists(agent_id):
        stop_session(agent_id)
        time.sleep(1)

    restart_args = argparse.Namespace(
        agent=agent_file_id,
        working_dir=None,
        restore=True,
        tmux_layout='sessions',
    )
    if cmd_start(restart_args) != 0:
        print(f"❌ Failed to restart '{agent_name}' in restore mode")
        return False
    return True


def _restart_heartbeat_session_fresh(agent_file_id: str, agent_name: str, agent_id: str) -> bool:
    return service_restart_heartbeat_session_fresh(
        agent_file_id,
        agent_name,
        agent_id,
        deps=sys.modules[__name__],
    )


def _run_heartbeat_attempt(
    *,
    agent_id: str,
    agent_name: str,
    launcher: str,
    heartbeat_message: str,
    timeout_seconds: Optional[int],
    is_codex: bool,
) -> dict:
    return service_run_heartbeat_attempt(
        agent_id=agent_id,
        agent_name=agent_name,
        launcher=launcher,
        heartbeat_message=heartbeat_message,
        timeout_seconds=timeout_seconds,
        is_codex=is_codex,
        deps=sys.modules[__name__],
    )


def _maybe_rollover_heartbeat_session(
    *,
    agent_name: str,
    agent_id: str,
    agent_file_id: str,
    launcher: str,
    timeout_seconds: Optional[int],
    heartbeat_id: str,
    session_mode: str,
) -> Optional[Path]:
    if session_mode not in {'auto', 'fresh'}:
        return None

    context_left_percent = _detect_agent_context_left_percent(agent_id, launcher=launcher)
    if context_left_percent is not None:
        print(f"   Context left: {context_left_percent}%")
    elif session_mode == 'auto':
        print("   Context left: unknown (skip auto rollover)")

    if not _should_rollover_heartbeat_session(session_mode, context_left_percent):
        return None

    reason = 'fresh session_mode' if session_mode == 'fresh' else f'context<{_HEARTBEAT_AUTO_CONTEXT_THRESHOLD}%'
    print(f"♻️  Heartbeat session rollover triggered ({reason})")

    is_codex = 'codex' in (launcher or '').lower()
    repo_root = get_repo_root()
    handoff_file = _write_heartbeat_handoff_template(repo_root, agent_id, heartbeat_id)
    handoff_prompt = _build_heartbeat_handoff_prompt(handoff_file, heartbeat_id)

    if not send_keys(
        agent_id,
        handoff_prompt,
        send_enter=True,
        clear_input=is_codex,
        escape_first=is_codex,
        enter_via_key=is_codex,
    ):
        print("⚠️  Failed to send handoff prompt; skip rollover")
        return None

    handoff_timeout = min(180, max(45, int(timeout_seconds or 90)))
    state_after_handoff = _wait_for_idle_after_handoff(agent_id, launcher=launcher, timeout_seconds=handoff_timeout)
    saved = _heartbeat_handoff_saved(handoff_file)
    if not saved:
        print(f"⚠️  Handoff not saved (state={state_after_handoff}); skip rollover")
        return None

    print(f"✅ Handoff saved: {handoff_file}")

    if not stop_session(agent_id):
        print(f"⚠️  Failed to stop session for '{agent_name}'; skip rollover")
        return None

    time.sleep(1)
    restart_args = argparse.Namespace(
        agent=agent_file_id,
        working_dir=None,
        restore=False,
        tmux_layout='sessions',
    )
    if cmd_start(restart_args) != 0:
        print(f"⚠️  Failed to restart '{agent_name}' with fresh session")
        return None

    # Give the restarted TUI a brief moment before sending heartbeat.
    time.sleep(2)
    return handoff_file


def build_mcp_config_json(agent_config: dict) -> str:
    """Build MCP config JSON for provider CLIs that support it.

    Agent frontmatter uses `mcps` (a mapping of server_name -> server_config).
    For Claude Code, we pass a JSON object with `mcpServers`.
    """
    mcps = agent_config.get('mcps')
    if mcps is None:
        mcps = {}

    if not isinstance(mcps, dict):
        raise ValueError("Invalid 'mcps' in agent config (expected a mapping)")

    if not mcps:
        return ""

    payload = {"mcpServers": mcps}
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def cleanup_old_logs(repo_root: Path, days: int = 7) -> int:
    """Remove log files older than specified days.

    Args:
        repo_root: Repository root path
        days: Number of days to retain logs (default: 7)

    Returns:
        Number of log files removed
    """
    log_dir = repo_root / '.crontab_logs'
    if not log_dir.exists():
        # Create log directory if it doesn't exist
        log_dir.mkdir(parents=True, exist_ok=True)
        return 0

    cutoff = time.time() - (days * 86400)
    removed = 0

    for log_file in log_dir.glob("*.log"):
        try:
            if log_file.stat().st_mtime < cutoff:
                log_file.unlink()
                removed += 1
        except (OSError, IOError):
            # Silently skip files that can't be removed
            pass

    return removed


def build_start_command(working_dir: str, launcher: str, launcher_args: list[str]) -> str:
    # Cron/tmux often runs with a minimal PATH; include common user-local bin dirs so
    # launchers like `ccc` can find `claude` (usually installed under ~/.local/bin).
    env_part = 'export PATH="$HOME/.local/bin:$HOME/bin:$PATH"'
    cd_part = f"cd {shlex.quote(working_dir)}"
    cmd_parts = [launcher] + list(launcher_args or [])
    exec_part = " ".join(shlex.quote(str(part)) for part in cmd_parts if part is not None and str(part) != "")
    return f"{env_part} && {cd_part} && {exec_part}".strip()


def get_agent_id(config: dict) -> str:
    """Get agent_id from config (file_id in lowercase, with hyphens)."""
    file_id = config.get('file_id', 'UNKNOWN')
    return file_id.lower().replace('_', '-')


def cmd_status(args):
    """Show status for one agent."""
    return status_cmd_status(args, deps=_lifecycle_deps_module())


def cmd_list(args):
    """List all agents (configured and running)."""
    return listing_cmd_list(args, deps=_lifecycle_deps_module())


def _tmux_install_hint() -> str:
    if sys.platform == 'darwin':
        return 'brew install tmux'
    if sys.platform.startswith('linux'):
        return 'sudo apt install tmux'
    return 'Install tmux and ensure it is on PATH'


def cmd_doctor(args):
    """Run basic environment checks for agent-manager."""
    return doctor_cmd_doctor(args, deps=_lifecycle_deps_module())


def _lifecycle_deps_module():
    return sys.modules[__name__]


def cmd_start(args):
    """Start an agent in tmux session."""
    return lifecycle_cmd_start(args, deps=_lifecycle_deps_module())


def cmd_stop(args):
    """Stop a running agent."""
    return lifecycle_cmd_stop(args, deps=_lifecycle_deps_module())


def cmd_monitor(args):
    """Monitor agent output."""
    return lifecycle_cmd_monitor(args, deps=_lifecycle_deps_module())


def cmd_send(args):
    """Send message to agent."""
    return lifecycle_cmd_send(args, deps=_lifecycle_deps_module())


def cmd_assign(args):
    """Assign task to agent."""
    return lifecycle_cmd_assign(args, deps=_lifecycle_deps_module(), start_handler=cmd_start)


def drain_main_inbound_once(*, agent_id: str = 'main', trigger: str = 'manual', deps=None):
    """Run one inbound replay pass for main."""
    deps_module = deps or _lifecycle_deps_module()
    return inbound_drain_main_inbound_once(
        deps=deps_module,
        agent_id=agent_id,
        trigger=trigger,
    )


def _maybe_run_main_inbound_heartbeat_sweep(
    *,
    repo_root: Path,
    agent_id: str,
    heartbeat_id: str,
    context_left_percent: Optional[int],
    session_mode: str,
) -> bool:
    """Consume one main heartbeat run on replayable inbound queue work."""
    if str(agent_id).strip().lower() != 'main':
        return False

    replayable = load_replayable_inbound_messages(repo_root, agent_id=agent_id)
    if not replayable:
        return False

    print("⏭️  Replayable inbound queue work detected; running inbound sweep before heartbeat dispatch")
    summary = drain_main_inbound_once(agent_id=agent_id, trigger='heartbeat_sweep')
    print(
        "   Inbound sweep summary: "
        f"drained={summary['drained']} "
        f"failed={summary['failed']} "
        f"dead_lettered={summary['dead_lettered']} "
        f"skipped={summary['skipped']}"
    )
    _append_heartbeat_audit_event(
        repo_root,
        agent_id=agent_id,
        heartbeat_id=heartbeat_id,
        send_status='skip',
        ack_status='not_checked',
        duration_ms=0,
        context_left=context_left_percent,
        failure_type='inbound_queue_sweep',
        session_mode=session_mode,
        phase='preflight',
        attempt=0,
        recovery_action='inbound_sweep',
        reason_code='HB_INBOUND_SWEEP',
    )
    return True


def cmd_inbound(args):
    """Handle inbound queue recovery subcommands."""
    return inbound_cmd_inbound(
        args,
        deps=_lifecycle_deps_module(),
        drain_once_handler=drain_main_inbound_once,
    )


def cmd_schedule(args):
    """Handle schedule subcommands."""
    return schedule_cmd_schedule(args, deps=_lifecycle_deps_module(), schedule_run_handler=cmd_schedule_run)


def cmd_heartbeat(args):
    """Handle heartbeat subcommands."""
    return heartbeat_cmd_heartbeat(
        args,
        run_handler=cmd_heartbeat_run,
        rescue_handler=cmd_heartbeat_rescue,
        trace_handler=cmd_heartbeat_trace,
        slo_handler=cmd_heartbeat_slo,
    )


def cmd_dream(args):
    """Handle dream subcommands."""
    return dream_cmd_dream(
        args,
        run_handler=cmd_dream_run,
    )


def cmd_timer(args):
    """Handle timer subcommands."""
    return timer_cmd_timer(args, deps=_lifecycle_deps_module())


def cmd_dream_run(args):
    """Run one dream task for an agent."""
    if not check_tmux():
        print("❌ tmux is not installed")
        return 1

    agent_config = resolve_agent(args.agent)
    if not agent_config:
        print(f"❌ Agent not found: {args.agent}")
        return 1

    agent_name = agent_config['name']
    agent_id = get_agent_id(agent_config)
    if not agent_config.get('enabled', True):
        print(f"⏭️  Agent '{agent_name}' is disabled - skipping dream")
        return 0

    heartbeat = agent_config.get('heartbeat')
    if not heartbeat or not isinstance(heartbeat, dict):
        print(f"❌ No heartbeat configured for agent '{agent_name}'")
        return 1

    dream_policy = _parse_dream_policy(heartbeat)
    if not dream_policy['enabled']:
        print(f"⏭️  Dream mode is disabled for agent '{agent_name}'")
        return 0

    if not session_exists(agent_id):
        print(f"⏭️  Agent '{agent_name}' is not running - skipping dream")
        return 0

    repo_root = get_repo_root()
    state = load_dream_state(repo_root, agent_id)
    expected_window_id = str(getattr(args, 'window_id', '') or '').strip()
    trigger_hb_id = str(getattr(args, 'trigger_hb_id', '') or '').strip()
    active_window_id = str(state.get('window_id') or '')
    if expected_window_id and active_window_id != expected_window_id:
        append_dream_audit_event(
            repo_root,
            agent_id=agent_id,
            event='run_stale',
            window_id=expected_window_id,
            hb_id=trigger_hb_id,
            reason_code='DREAM_STALE_WINDOW',
            detail=f'active={active_window_id}',
        )
        print(f"⏭️  Dream window is stale (expected={expected_window_id}, active={active_window_id})")
        return 0

    working_dir = _normalize_path(agent_config.get('working_directory') or '')
    dream_file = Path(working_dir) / 'DREAM.md' if working_dir else None
    if not dream_file or not dream_file.exists():
        append_dream_audit_event(
            repo_root,
            agent_id=agent_id,
            event='run_stale',
            window_id=active_window_id,
            hb_id=trigger_hb_id,
            reason_code='DREAM_NO_FILE',
            detail=str(dream_file or ''),
        )
        print("⏭️  DREAM.md not found - skipping dream")
        return 0

    if has_pending_inbound_messages(repo_root, agent_id=agent_id):
        append_dream_audit_event(
            repo_root,
            agent_id=agent_id,
            event='run_stale',
            window_id=active_window_id,
            hb_id=trigger_hb_id,
            reason_code='DREAM_USER_QUEUE_PENDING',
            detail='pending_inbound_messages',
        )
        print("⏭️  Pending inbound user work detected - skipping dream")
        return 0

    launcher = resolve_launcher_command(agent_config.get('launcher', ''))
    preflight_state, preflight_reason = _heartbeat_preflight_runtime_state(
        repo_root=repo_root,
        agent_id=agent_id,
        launcher=launcher,
    )
    if preflight_state != 'idle':
        append_dream_audit_event(
            repo_root,
            agent_id=agent_id,
            event='run_stale',
            window_id=active_window_id,
            hb_id=trigger_hb_id,
            reason_code='DREAM_AGENT_NOT_IDLE',
            detail=f'{preflight_state}:{preflight_reason}',
        )
        print(f"⏭️  Agent is not idle (state={preflight_state}, reason={preflight_reason}) - skipping dream")
        return 0

    timeout_text = str(getattr(args, 'timeout', '') or dream_policy.get('max_runtime') or '').strip()
    timeout_seconds = parse_duration(timeout_text) if timeout_text else int(dream_policy.get('max_runtime_seconds') or 900)
    if timeout_seconds is None:
        timeout_seconds = 900

    dream_id = time.strftime('%Y%m%d-%H%M%S')
    dream_message = _build_dream_prompt(dream_id=dream_id, trigger_hb_id=trigger_hb_id)
    append_dream_audit_event(
        repo_root,
        agent_id=agent_id,
        event='run_started',
        window_id=active_window_id,
        hb_id=trigger_hb_id,
        dream_id=dream_id,
        reason_code='DREAM_RUN_STARTED',
    )

    result = _run_dream_attempt(
        repo_root=repo_root,
        agent_id=agent_id,
        agent_name=agent_name,
        launcher=launcher,
        dream_message=dream_message,
        timeout_seconds=timeout_seconds,
        is_codex='codex' in launcher.lower(),
        dream_id=dream_id,
    )

    send_status = str(result.get('send_status', 'fail'))
    ack_status = str(result.get('ack_status', 'not_checked'))
    failure_type = str(result.get('failure_type', ''))
    if send_status == 'ok' and ack_status in {'ack', 'not_checked'} and not failure_type:
        state['last_dream_id'] = dream_id
        save_dream_state(repo_root, agent_id, state)
        append_dream_audit_event(
            repo_root,
            agent_id=agent_id,
            event='run_completed',
            window_id=active_window_id,
            hb_id=trigger_hb_id,
            dream_id=dream_id,
            reason_code='DREAM_RUN_OK',
        )
        print("✅ Dream completed successfully")
        return 0

    append_dream_audit_event(
        repo_root,
        agent_id=agent_id,
        event='run_failed',
        window_id=active_window_id,
        hb_id=trigger_hb_id,
        dream_id=dream_id,
        reason_code='DREAM_RUN_FAILED',
        detail=f'{send_status}:{ack_status}:{failure_type}',
    )
    print(f"❌ Dream failed (send={send_status}, ack={ack_status}, failure={failure_type or 'unknown'})")
    return 1


def cmd_heartbeat_rescue(args):
    """Force-stop/start one heartbeat session and optionally prime it."""
    if not check_tmux():
        print("❌ tmux is not installed")
        return 1

    agent_config = resolve_agent(args.agent)
    if not agent_config:
        print(f"❌ Agent '{args.agent}' not found")
        return 1

    agent_name = agent_config['name']
    agent_file_id = agent_config['file_id']
    agent_id = get_agent_id(agent_config)
    reason = str(getattr(args, 'reason', '') or '').strip()
    prime = not bool(getattr(args, 'no_prime', False))
    use_fresh = bool(getattr(args, 'fresh', False))

    print(f"🛟 Heartbeat rescue: {agent_name}")
    if reason:
        print(f"   Reason: {reason}")
    print(f"   Prime after restart: {'yes' if prime else 'no'}")
    print(f"   Restart mode: {'fresh' if use_fresh else 'restore'}")

    if use_fresh:
        restarted = _restart_heartbeat_session_fresh(
            agent_file_id,
            agent_name,
            agent_id,
            deps=_lifecycle_deps_module(),
        )
    else:
        restarted = _restart_heartbeat_session_restore(agent_file_id, agent_name, agent_id)
    if not restarted:
        return 1

    if not prime:
        print("✅ Heartbeat rescue completed (prime skipped)")
        return 0

    prime_args = argparse.Namespace(
        agent=agent_file_id,
        timeout=getattr(args, 'timeout', None),
        retry=0,
        backoff_seconds=0,
        fallback_mode='none',
        notify_on_failure=False,
        notifier_channel=None,
        force_session_mode='force',
    )
    prime_result = cmd_heartbeat_run(prime_args)
    if prime_result == 0:
        print("✅ Heartbeat rescue completed and prime pass succeeded")
    return prime_result


def cmd_heartbeat_run(args):
    """Run a heartbeat check for an agent."""
    if not check_tmux():
        print("❌ tmux is not installed")
        return 1

    # Resolve agent
    agent_config = resolve_agent(args.agent)
    if not agent_config:
        print(f"❌ Agent not found: {args.agent}")
        return 1

    agent_name = agent_config['name']
    agent_id = get_agent_id(agent_config)
    agent_file_id = agent_config.get('file_id', args.agent)

    # Check if agent is disabled
    if not agent_config.get('enabled', True):
        agent_file_path = agent_config.get('_file_path', f'agents/{agent_file_id}.md')
        print(f"⏭️  Agent '{agent_name}' is disabled - skipping heartbeat")
        print(f"   Config: {agent_file_path}")
        return 0

    # Get heartbeat config
    heartbeat = agent_config.get('heartbeat')
    if not heartbeat or not isinstance(heartbeat, dict):
        print(f"❌ No heartbeat configured for agent '{agent_name}'")
        return 1

    # Check if heartbeat is disabled
    if not heartbeat.get('enabled', True):
        print(f"⏭️  Heartbeat is disabled for agent '{agent_name}'")
        return 0

    dream_policy = _parse_dream_policy(heartbeat)
    fixed_dream_window = (
        resolve_active_dream_window(dream_policy)
        if dream_policy.get('enabled')
        else {'active': False, 'reason': 'dream_disabled', 'windows': []}
    )

    # Heartbeats only check running agents - don't start if not running
    if not session_exists(agent_id):
        print(f"⏭️  Agent '{agent_name}' is not running - skipping heartbeat")
        return 0

    # Check work schedule
    schedule_config = heartbeat.get('schedule')
    if schedule_config and not fixed_dream_window.get('active'):
        from services.work_schedule import is_within_work_schedule
        is_active, skip_reason = is_within_work_schedule(schedule_config)
        if not is_active:
            print(f"⏭️  Outside work schedule for '{agent_name}' - skipping heartbeat ({skip_reason})")
            return 0

    # Parse timeout
    timeout_seconds = None
    timeout_str = args.timeout or heartbeat.get('max_runtime', '')
    if timeout_str:
        timeout_seconds = parse_duration(timeout_str)

    print(f"💓 Heartbeat: {agent_name}")
    print(f"   Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    heartbeat_started_at = time.time()

    repo_root = get_repo_root()
    launcher = resolve_launcher_command(agent_config.get('launcher', ''))
    is_codex = 'codex' in launcher.lower()
    context_left_percent = _detect_agent_context_left_percent(agent_id, launcher=launcher)

    session_mode_raw = heartbeat.get('session_mode', 'restore')
    session_mode = _normalize_heartbeat_session_mode(session_mode_raw)
    if str(session_mode_raw).strip().lower() not in _HEARTBEAT_SESSION_MODES:
        print(f"⚠️  Unknown heartbeat session_mode '{session_mode_raw}', fallback to 'restore'")
    print(f"   Session mode: {session_mode}")

    recovery_policy = _parse_heartbeat_recovery_policy(heartbeat, args)
    auto_starvation_skip_threshold = _resolve_auto_starvation_skip_threshold(heartbeat)
    print(
        "   Recovery policy: "
        f"retry={recovery_policy['max_retries']} "
        f"backoff={recovery_policy['retry_backoff_seconds']}s "
        f"fallback={recovery_policy['fallback_mode']} "
        f"notify={recovery_policy['notify_on_failure']}"
    )
    if fixed_dream_window.get('active'):
        window_summary = str(fixed_dream_window.get('summary') or fixed_dream_window.get('window_id') or 'active')
        print(f"   Dream window: {window_summary}")
    elif dream_policy.get('fixed_windows'):
        print(f"   Dream window: inactive ({fixed_dream_window.get('reason')})")

    # Standard heartbeat message (with traceable id for delivery debugging)
    heartbeat_id = _generate_heartbeat_id()
    print(f"   HB_ID: {heartbeat_id}")
    recovery_action = ''

    if _maybe_run_main_inbound_heartbeat_sweep(
        repo_root=repo_root,
        agent_id=agent_id,
        heartbeat_id=heartbeat_id,
        context_left_percent=context_left_percent,
        session_mode=session_mode,
    ):
        _maybe_trigger_dream_from_heartbeat(
            repo_root=repo_root,
            agent_config=agent_config,
            agent_id=agent_id,
            agent_file_id=agent_file_id,
            heartbeat=heartbeat,
            heartbeat_id=heartbeat_id,
            heartbeat_timestamp=_utc_now_iso(),
            ack_status='not_checked',
            ack_evidence='none',
            failure_type='inbound_queue_sweep',
        )
        return 0

    if has_pending_inbound_messages(repo_root, agent_id=agent_id):
        note_pending_messages_yielded(
            repo_root,
            agent_id=agent_id,
            heartbeat_id=heartbeat_id,
            reason_code='HB_USER_QUEUE_PENDING',
            detail='heartbeat_pre_dispatch_yield',
        )
        print("⏭️  Pending inbound user work detected; yielding heartbeat before dispatch")
        _append_heartbeat_audit_event(
            repo_root,
            agent_id=agent_id,
            heartbeat_id=heartbeat_id,
            send_status='skip',
            ack_status='yielded',
            duration_ms=0,
            context_left=context_left_percent,
            failure_type='user_queue_yield',
            session_mode=session_mode,
            phase='preflight',
            attempt=0,
            recovery_action='yield_to_user',
            reason_code='HB_USER_QUEUE_PENDING',
            ack_evidence='yielded',
        )
        _maybe_trigger_dream_from_heartbeat(
            repo_root=repo_root,
            agent_config=agent_config,
            agent_id=agent_id,
            agent_file_id=agent_file_id,
            heartbeat=heartbeat,
            heartbeat_id=heartbeat_id,
            heartbeat_timestamp=_utc_now_iso(),
            ack_status='yielded',
            ack_evidence='yielded',
            failure_type='user_queue_yield',
        )
        return 0

    if session_mode == 'auto':
        preflight_state, preflight_reason = _heartbeat_preflight_runtime_state(
            repo_root=repo_root,
            agent_id=agent_id,
            launcher=launcher,
        )
        if preflight_state in {'busy', 'stuck', 'blocked', 'error'}:
            skip_failure_type = 'busy_skip'
            skip_reason_code = 'HB_AUTO_BUSY_SKIP'
            skip_recovery_action = 'skip_busy'
            if preflight_state == 'busy' and str(preflight_reason).startswith('preflight_pane_changed:'):
                skip_failure_type = 'active_skip'
                skip_reason_code = 'HB_AUTO_ACTIVE_SKIP'
            elif preflight_state == 'busy' and str(preflight_reason).startswith('pending_heartbeat:'):
                skip_failure_type = 'pending_skip'
                skip_reason_code = 'HB_AUTO_PENDING_SKIP'
                pending_hb_id = _parse_pending_heartbeat_reason(preflight_reason)
                pending_age_seconds = _heartbeat_id_age_seconds(pending_hb_id)
                pending_skip_count = _count_consecutive_auto_preflight_skips(
                    repo_root,
                    agent_id=agent_id,
                    reason_codes={'HB_AUTO_PENDING_SKIP'},
                )
                should_rescue_pending = (
                    (pending_age_seconds is not None and pending_age_seconds >= _HEARTBEAT_PENDING_RESCUE_AGE_SECONDS)
                    or pending_skip_count >= _HEARTBEAT_PENDING_RESCUE_SKIP_THRESHOLD
                )
                if should_rescue_pending:
                    age_desc = (
                        f"{pending_age_seconds}s old"
                        if pending_age_seconds is not None
                        else 'age=unknown'
                    )
                    print(
                        "🛟 Pending heartbeat rescue triggered "
                        f"(hb_id={pending_hb_id or 'unknown'}, age={age_desc}, "
                        f"consecutive_pending_skips={pending_skip_count})"
                    )
                    if not _restart_heartbeat_session_restore(agent_file_id, agent_name, agent_id):
                        print("⚠️  Pending heartbeat rescue failed; falling back to skip")
                    else:
                        recovery_action = 'auto_pending_rescue'
                        context_left_percent = _detect_agent_context_left_percent(agent_id, launcher=launcher)
                        print("♻️  Pending heartbeat rescue completed; continuing current heartbeat run")
                        preflight_state = 'idle'
                        preflight_reason = 'auto_pending_rescue_completed'
                elif pending_hb_id:
                    remaining_delay = _HEARTBEAT_PENDING_RESCUE_AGE_SECONDS
                    if pending_age_seconds is not None:
                        remaining_delay = max(
                            _HEARTBEAT_PENDING_RESCUE_MIN_DELAY_SECONDS,
                            _HEARTBEAT_PENDING_RESCUE_AGE_SECONDS - pending_age_seconds,
                        )
                    if _schedule_pending_heartbeat_rescue_timer(
                        agent_file_id=agent_file_id,
                        pending_heartbeat_id=pending_hb_id,
                        delay_seconds=remaining_delay,
                        timeout_seconds=timeout_seconds,
                    ):
                        skip_recovery_action = 'schedule_pending_rescue_timer'
            if preflight_state == 'idle':
                pass
            else:
                starvation_guard_armed = skip_reason_code != 'HB_AUTO_PENDING_SKIP'
                consecutive_skip_count = 0
                if starvation_guard_armed:
                    if auto_starvation_skip_threshold is None:
                        starvation_guard_armed = False
                    else:
                        consecutive_skip_count = _count_consecutive_auto_preflight_skips(
                            repo_root,
                            agent_id=agent_id,
                        )
                        if consecutive_skip_count >= auto_starvation_skip_threshold:
                            recovery_action = 'auto_starvation_bypass'
                            print(
                                "⚠️  Auto-mode starvation guard triggered after "
                                f"{consecutive_skip_count} consecutive preflight skips; "
                                "dispatching one heartbeat attempt anyway"
                            )
                        else:
                            starvation_guard_armed = False
                if not starvation_guard_armed:
                    print(
                        "⏭️  Agent is not idle "
                        f"(state={preflight_state}, reason={preflight_reason}); "
                        "skipping heartbeat dispatch in auto mode to avoid batch accumulation"
                    )
                    _append_heartbeat_audit_event(
                        repo_root,
                        agent_id=agent_id,
                        heartbeat_id=heartbeat_id,
                        send_status='skip',
                        ack_status='not_checked',
                        duration_ms=0,
                        context_left=context_left_percent,
                        failure_type=skip_failure_type,
                        session_mode=session_mode,
                        phase='preflight',
                        attempt=0,
                        recovery_action=skip_recovery_action,
                        reason_code=skip_reason_code,
                        ack_evidence='none',
                    )
                    _maybe_trigger_dream_from_heartbeat(
                        repo_root=repo_root,
                        agent_config=agent_config,
                        agent_id=agent_id,
                        agent_file_id=agent_file_id,
                        heartbeat=heartbeat,
                        heartbeat_id=heartbeat_id,
                        heartbeat_timestamp=_utc_now_iso(),
                        ack_status='not_checked',
                        ack_evidence='none',
                        failure_type=skip_failure_type,
                    )
                    return 0
    elif session_mode == 'force':
        print("   Force mode: bypass preflight idle check and always dispatch heartbeat")

    rollover_handoff_file = _maybe_rollover_heartbeat_session(
        agent_name=agent_name,
        agent_id=agent_id,
        agent_file_id=agent_file_id,
        launcher=launcher,
        timeout_seconds=timeout_seconds,
        heartbeat_id=heartbeat_id,
        session_mode=session_mode,
    )

    if fixed_dream_window.get('active'):
        dream_result = _run_fixed_dream_heartbeat(
            repo_root=repo_root,
            agent_config=agent_config,
            agent_id=agent_id,
            agent_name=agent_name,
            dream_policy=dream_policy,
            heartbeat_id=heartbeat_id,
            rollover_handoff_file=rollover_handoff_file,
            fixed_window=fixed_dream_window,
            fallback_timeout_seconds=timeout_seconds,
        )
        if not dream_result.get('ran'):
            return 0

        send_status = str(dream_result.get('send_status', 'fail'))
        ack_status = str(dream_result.get('ack_status', 'not_checked'))
        ack_evidence = str(dream_result.get('ack_evidence', 'none'))
        failure_type = str(dream_result.get('failure_type', ''))
        reason_code = str(dream_result.get('reason_code', ''))
        duration_ms = int(dream_result.get('duration_ms', 0) or 0)

        _append_heartbeat_audit_event(
            repo_root,
            agent_id=agent_id,
            heartbeat_id=heartbeat_id,
            send_status=send_status,
            ack_status=ack_status,
            duration_ms=duration_ms,
            context_left=context_left_percent,
            failure_type=failure_type,
            session_mode=session_mode,
            phase='attempt',
            attempt=1,
            recovery_action='dream_window',
            reason_code=reason_code,
            ack_evidence=ack_evidence,
        )

        if send_status == 'ok' and ack_status in {'ack', 'not_checked'} and not failure_type:
            print("✅ Heartbeat completed via fixed Dream window")
            return 0

        print(
            "❌ Fixed Dream window failed "
            f"(send={send_status}, ack={ack_status}, failure={failure_type or 'unknown'})"
        )
        return 1

    heartbeat_message = (
        "Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. "
        "Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK. "
        f"[HB_ID:{heartbeat_id}]"
    )
    if rollover_handoff_file is not None:
        heartbeat_message = (
            f"First read rollover handoff file: {rollover_handoff_file}.\n"
            + heartbeat_message
        )


    max_retries = int(recovery_policy['max_retries'])
    backoff_seconds = int(recovery_policy['retry_backoff_seconds'])
    fallback_mode = str(recovery_policy['fallback_mode'])
    notify_on_failure = bool(recovery_policy['notify_on_failure'])
    notifier_channel = str(recovery_policy['notifier_channel'] or 'all')

    final_attempt_result: Optional[dict] = None

    for attempt in range(max_retries + 1):
        if has_pending_inbound_messages(repo_root, agent_id=agent_id):
            note_pending_messages_yielded(
                repo_root,
                agent_id=agent_id,
                heartbeat_id=heartbeat_id,
                reason_code='HB_USER_QUEUE_PENDING',
                detail='heartbeat_pre_attempt_yield',
            )
            print("⏭️  Pending inbound user work detected; yielding heartbeat before next attempt")
            _append_heartbeat_audit_event(
                repo_root,
                agent_id=agent_id,
                heartbeat_id=heartbeat_id,
                send_status='skip',
                ack_status='yielded',
                duration_ms=0,
                context_left=context_left_percent,
                failure_type='user_queue_yield',
                session_mode=session_mode,
                phase='preflight',
                attempt=attempt,
                recovery_action='yield_to_user',
                reason_code='HB_USER_QUEUE_PENDING',
            )
            return 0
        attempt_no = attempt + 1
        print(f"   Attempt {attempt_no}/{max_retries + 1}")
        result = _run_heartbeat_attempt(
            agent_id=agent_id,
            agent_name=agent_name,
            launcher=launcher,
            heartbeat_message=heartbeat_message,
            timeout_seconds=timeout_seconds,
            is_codex=is_codex,
        )

        send_status = str(result.get('send_status', 'fail'))
        ack_status = str(result.get('ack_status', 'not_checked'))
        ack_evidence = str(result.get('ack_evidence', 'none'))
        failure_type = str(result.get('failure_type', ''))
        reason_code = str(result.get('reason_code', ''))
        duration_ms = int(result.get('duration_ms', 0) or 0)

        _append_heartbeat_audit_event(
            repo_root,
            agent_id=agent_id,
            heartbeat_id=heartbeat_id,
            send_status=send_status,
            ack_status=ack_status,
            duration_ms=duration_ms,
            context_left=context_left_percent,
            failure_type=failure_type,
            session_mode=session_mode,
            phase='attempt',
            attempt=attempt_no,
            recovery_action=recovery_action,
            reason_code=reason_code,
            ack_evidence=ack_evidence,
        )

        final_attempt_result = result

        if failure_type == 'user_queue_yield':
            note_pending_messages_yielded(
                repo_root,
                agent_id=agent_id,
                heartbeat_id=heartbeat_id,
                reason_code=reason_code or 'HB_USER_QUEUE_YIELD',
                detail='heartbeat_wait_yield',
            )
            print("⏭️  Inbound user work arrived during heartbeat; yielding to user-first priority")
            _maybe_trigger_dream_from_heartbeat(
                repo_root=repo_root,
                agent_config=agent_config,
                agent_id=agent_id,
                agent_file_id=agent_file_id,
                heartbeat=heartbeat,
                heartbeat_id=heartbeat_id,
                heartbeat_timestamp=_utc_now_iso(),
                ack_status=ack_status,
                ack_evidence=ack_evidence,
                failure_type=failure_type,
            )
            return 0

        if send_status == 'ok' and ack_status in {'ack', 'not_checked'}:
            break

        if _should_retry_heartbeat_attempt(
            failure_type=failure_type,
            attempt_index=attempt,
            max_retries=max_retries,
        ):
            if backoff_seconds > 0:
                print(f"   Retry backoff: {backoff_seconds}s")
                time.sleep(backoff_seconds)
            continue
        break

    if final_attempt_result is None:
        print("❌ Heartbeat failed before execution")
        return 1

    send_status = str(final_attempt_result.get('send_status', 'fail'))
    ack_status = str(final_attempt_result.get('ack_status', 'not_checked'))
    ack_evidence = str(final_attempt_result.get('ack_evidence', 'none'))
    failure_type = str(final_attempt_result.get('failure_type', ''))
    reason_code = str(final_attempt_result.get('reason_code', ''))

    if send_status == 'ok' and ack_status in {'ack', 'not_checked'}:
        _maybe_trigger_dream_from_heartbeat(
            repo_root=repo_root,
            agent_config=agent_config,
            agent_id=agent_id,
            agent_file_id=agent_file_id,
            heartbeat=heartbeat,
            heartbeat_id=heartbeat_id,
            heartbeat_timestamp=_utc_now_iso(),
            ack_status=ack_status,
            ack_evidence=ack_evidence,
            failure_type=failure_type,
        )
        print("✅ Heartbeat completed successfully")
        return 0

    if fallback_mode == 'fresh':
        recovery_action = 'fallback_fresh'
        print(f"⚠️  Heartbeat unresolved (failure={failure_type or 'unknown'}), applying fallback: fresh")
        if _restart_heartbeat_session_fresh(agent_file_id, agent_name, agent_id):
            fallback_result = None
            if is_codex and not stabilize_codex_session(agent_id, timeout=min(30, int(timeout_seconds or 30))):
                send_status = 'fail'
                ack_status = 'no_ack'
                failure_type = 'interrupted'
                reason_code = service_failure_reason_code(
                    failure_type=failure_type,
                    ack_status=ack_status,
                    send_status=send_status,
                )
                duration_ms = 0
                _append_heartbeat_audit_event(
                    repo_root,
                    agent_id=agent_id,
                    heartbeat_id=heartbeat_id,
                    send_status=send_status,
                    ack_status=ack_status,
                    duration_ms=duration_ms,
                    context_left=context_left_percent,
                    failure_type=failure_type,
                    session_mode='fresh',
                    phase='fallback',
                    attempt=max_retries + 2,
                    recovery_action='fallback_fresh_stabilize_failed',
                    reason_code=reason_code,
                )
                print("⚠️  Fresh Codex session did not stabilize after restart")
            else:
                fallback_result = _run_heartbeat_attempt(
                    agent_id=agent_id,
                    agent_name=agent_name,
                    launcher=launcher,
                    heartbeat_message=heartbeat_message,
                    timeout_seconds=timeout_seconds,
                    is_codex=is_codex,
                )
            if fallback_result is not None:
                send_status = str(fallback_result.get('send_status', 'fail'))
                ack_status = str(fallback_result.get('ack_status', 'not_checked'))
                ack_evidence = str(fallback_result.get('ack_evidence', 'none'))
                failure_type = str(fallback_result.get('failure_type', ''))
                reason_code = str(fallback_result.get('reason_code', ''))
                duration_ms = int(fallback_result.get('duration_ms', 0) or 0)
                _append_heartbeat_audit_event(
                    repo_root,
                    agent_id=agent_id,
                    heartbeat_id=heartbeat_id,
                    send_status=send_status,
                    ack_status=ack_status,
                    duration_ms=duration_ms,
                    context_left=context_left_percent,
                    failure_type=failure_type,
                    session_mode='fresh',
                    phase='fallback',
                    attempt=max_retries + 2,
                    recovery_action=recovery_action,
                    reason_code=reason_code,
                    ack_evidence=ack_evidence,
                )
        else:
            send_status = 'fail'
            ack_status = 'no_ack'
            if not failure_type:
                failure_type = 'timeout'
            reason_code = service_failure_reason_code(
                failure_type=failure_type,
                ack_status=ack_status,
                send_status=send_status,
            )

    if send_status == 'ok' and ack_status in {'ack', 'not_checked'}:
        _maybe_trigger_dream_from_heartbeat(
            repo_root=repo_root,
            agent_config=agent_config,
            agent_id=agent_id,
            agent_file_id=agent_file_id,
            heartbeat=heartbeat,
            heartbeat_id=heartbeat_id,
            heartbeat_timestamp=_utc_now_iso(),
            ack_status=ack_status,
            ack_evidence=ack_evidence,
            failure_type=failure_type,
        )
        print("✅ Heartbeat recovered via fallback policy")
        return 0

    _maybe_trigger_dream_from_heartbeat(
        repo_root=repo_root,
        agent_config=agent_config,
        agent_id=agent_id,
        agent_file_id=agent_file_id,
        heartbeat=heartbeat,
        heartbeat_id=heartbeat_id,
        heartbeat_timestamp=_utc_now_iso(),
        ack_status=ack_status,
        ack_evidence=ack_evidence,
        failure_type=failure_type,
    )

    if notify_on_failure:
        _notify_heartbeat_failure(
            repo_root,
            channel=notifier_channel,
            agent_name=agent_name,
            agent_id=agent_id,
            heartbeat_id=heartbeat_id,
            failure_type=failure_type,
        )

    print(f"❌ Heartbeat failed after recovery policy (failure={failure_type or 'unknown'})")
    return 1


def cmd_schedule_run(args):
    """Run a scheduled job for an agent."""
    return schedule_run_cmd_schedule_run(
        args,
        deps=_lifecycle_deps_module(),
        start_handler=cmd_start,
    )

def main():
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0
    handlers = get_command_handlers(
        cmd_list=cmd_list,
        cmd_doctor=cmd_doctor,
        cmd_start=cmd_start,
        cmd_stop=cmd_stop,
        cmd_status=cmd_status,
        cmd_monitor=cmd_monitor,
        cmd_send=cmd_send,
        cmd_assign=cmd_assign,
        cmd_schedule=cmd_schedule,
        cmd_heartbeat=cmd_heartbeat,
        cmd_dream=cmd_dream,
        cmd_timer=cmd_timer,
        cmd_inbound=cmd_inbound,
    )

    handler = handlers.get(args.command)
    if handler:
        return handler(args)

    parser.print_help()
    return 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except BrokenPipeError:
        # Allow piping to tools like `head` without dumping a stack trace.
        try:
            sys.stdout.close()
        finally:
            sys.exit(0)
