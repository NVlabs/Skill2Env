"""
Tmux session helper for agent-manager skill.

Wraps tmux commands for managing agent sessions.
Sessions are named: agent-{agent_id} where agent_id is file_id in lowercase (e.g., emp-0001)
"""

from __future__ import annotations
import subprocess
import time
import re
import os
import shutil
from typing import Optional, List, Dict, Any, Tuple

from runtime_state import (
    evaluate_runtime_state,
    parse_elapsed_seconds,
    detect_error_reason,
)


# Session prefix for all agent sessions
SESSION_PREFIX = "agent-"
MAIN_AGENT_ID = "main"

# Optional "single session" mode: keep all agents in one tmux session, each in its own window.
DEFAULT_GROUP_SESSION_NAME = "agent-manager"
GROUP_SESSION_ENV_VAR = "AGENT_MANAGER_TMUX_GROUP_SESSION"


def get_group_session_name() -> str:
    return os.environ.get(GROUP_SESSION_ENV_VAR, DEFAULT_GROUP_SESSION_NAME)


def _ensure_tmux_in_path() -> bool:
    """Ensure `tmux` is resolvable even in restricted service environments."""
    if shutil.which("tmux"):
        return True

    candidates = [
        os.environ.get("TMUX_BIN", ""),
        "/opt/homebrew/bin/tmux",  # macOS Homebrew (Apple Silicon)
        "/usr/local/bin/tmux",     # macOS Homebrew (Intel)
        "/opt/local/bin/tmux",     # MacPorts
        "/usr/bin/tmux",
    ]

    for candidate in candidates:
        candidate = str(candidate or "").strip()
        if not candidate:
            continue
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            bin_dir = os.path.dirname(candidate)
            path = os.environ.get("PATH", "")
            path_parts = [p for p in path.split(":") if p]
            if bin_dir not in path_parts:
                os.environ["PATH"] = f"{bin_dir}:{path}" if path else bin_dir
            return True
    return False


# Try once at import-time so all subprocess(['tmux', ...]) calls can resolve.
_ensure_tmux_in_path()


def _is_main_agent_id(agent_id: str) -> bool:
    return str(agent_id).strip().lower() == MAIN_AGENT_ID


def _session_name_for_agent(agent_id: str) -> str:
    if _is_main_agent_id(agent_id):
        return MAIN_AGENT_ID
    return f"{SESSION_PREFIX}{agent_id}"


def _window_name_for_agent(agent_id: str) -> str:
    if _is_main_agent_id(agent_id):
        return MAIN_AGENT_ID
    return f"{SESSION_PREFIX}{agent_id}"


def _tmux_has_session(session_name: str) -> bool:
    result = subprocess.run(['tmux', 'has-session', '-t', session_name], capture_output=True)
    return result.returncode == 0


def _group_session_exists() -> bool:
    return _tmux_has_session(get_group_session_name())


def _group_window_exists(agent_id: str) -> bool:
    group = get_group_session_name()
    window_name = _window_name_for_agent(agent_id)
    result = subprocess.run(
        ['tmux', 'list-windows', '-t', group, '-F', '#{window_name}'],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return False
    return any(line.strip() == window_name for line in result.stdout.splitlines())


def _agent_attach_target(agent_id: str) -> Optional[str]:
    dedicated = _session_name_for_agent(agent_id)
    if _tmux_has_session(dedicated):
        return dedicated
    if _group_window_exists(agent_id):
        group = get_group_session_name()
        return f"{group}:{_window_name_for_agent(agent_id)}"
    return None


def _agent_container_target(agent_id: str) -> Optional[str]:
    dedicated = _session_name_for_agent(agent_id)
    if _tmux_has_session(dedicated):
        return dedicated
    if _group_window_exists(agent_id):
        group = get_group_session_name()
        return f"{group}:{_window_name_for_agent(agent_id)}"
    return None


def _agent_pane_target(agent_id: str) -> Optional[str]:
    """Best-effort stable tmux target for an agent (pane_id preferred)."""
    container = _agent_container_target(agent_id)
    if not container:
        return None

    expected_title = _window_name_for_agent(agent_id)
    result = subprocess.run(
        ['tmux', 'list-panes', '-t', container, '-F', '#{pane_id}\t#{pane_title}'],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        for line in result.stdout.splitlines():
            try:
                pane_id, pane_title = line.split('\t', 1)
            except ValueError:
                continue
            if pane_title.strip() == expected_title:
                return pane_id.strip()

    # Fall back to the container target (uses the active pane).
    return container


def _set_agent_pane_title(agent_id: str) -> None:
    """Set the initial agent pane title so we can target it even after splits."""
    container = _agent_container_target(agent_id)
    if not container:
        return
    title = _window_name_for_agent(agent_id)
    # Best-effort; older tmux versions may not support -T.
    subprocess.run(['tmux', 'select-pane', '-t', container, '-T', title], capture_output=True, text=True)

_CODEX_MENU_OPTION_RE = re.compile(r'^[›❯]\s*\d+\.')
_CODEX_MODEL_PROMPT_FAILURE_THROTTLE_S = 15.0
_CODEX_MODEL_PROMPT_LAST_FAILURE: Dict[str, float] = {}


def check_tmux() -> bool:
    """
    Check if tmux is available.

    Returns:
        True if tmux is installed and accessible
    """
    return _ensure_tmux_in_path() and shutil.which("tmux") is not None


def list_sessions() -> List[str]:
    """
    List all agent-* tmux sessions.

    Returns:
        List of agent_id values (e.g., ['emp-0001', 'emp-0002'])
    """
    agent_ids: set[str] = set()

    result = subprocess.run(['tmux', 'ls'], capture_output=True, text=True)
    if result.returncode == 0:
        for line in result.stdout.split('\n'):
            if ':' in line:
                session_name = line.split(':')[0]
                if session_name.startswith(SESSION_PREFIX):
                    agent_ids.add(session_name[len(SESSION_PREFIX):])
                elif session_name == MAIN_AGENT_ID:
                    agent_ids.add(MAIN_AGENT_ID)

    group = get_group_session_name()
    result = subprocess.run(
        ['tmux', 'list-windows', '-t', group, '-F', '#{window_name}'],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        for window_name in result.stdout.splitlines():
            window_name = window_name.strip()
            if window_name.startswith(SESSION_PREFIX):
                agent_ids.add(window_name[len(SESSION_PREFIX):])
            elif window_name == MAIN_AGENT_ID:
                agent_ids.add(MAIN_AGENT_ID)

    return sorted(agent_ids)


def session_exists(agent_id: str) -> bool:
    """
    Check if an agent session exists.

    Args:
        agent_id: Agent ID (e.g., 'emp-0001', without agent- prefix)

    Returns:
        True if session exists
    """
    if _tmux_has_session(_session_name_for_agent(agent_id)):
        return True
    return _group_window_exists(agent_id)


def start_session(agent_id: str, command: str, *, layout: str = "sessions") -> bool:
    """
    Start a new tmux session for an agent.

    Args:
        agent_id: Agent ID (e.g., 'emp-0001', will be prefixed with agent-)
        command: Command to run in the session

    Returns:
        True if session was started successfully
    """
    if session_exists(agent_id):
        return False

    if layout == "windows":
        group = get_group_session_name()
        window_name = _window_name_for_agent(agent_id)
        if _group_session_exists():
            result = subprocess.run(
                ['tmux', 'new-window', '-d', '-t', group, '-n', window_name, command],
                capture_output=True,
                text=True,
            )
        else:
            result = subprocess.run(
                ['tmux', 'new-session', '-d', '-s', group, '-n', window_name, command],
                capture_output=True,
                text=True,
            )
        ok = result.returncode == 0
        if ok:
            _set_agent_pane_title(agent_id)
        return ok

    session_name = _session_name_for_agent(agent_id)
    result = subprocess.run(
        ['tmux', 'new-session', '-d', '-s', session_name, command],
        capture_output=True,
        text=True,
    )
    ok = result.returncode == 0
    if ok:
        _set_agent_pane_title(agent_id)
    return ok


_LAYOUT_SPLIT_ALIASES = {
    'h': 'h',
    'horizontal': 'h',
    'v': 'v',
    'vertical': 'v',
}


def _normalize_layout_node(node: Any, *, path: str = "tmux.layout") -> Optional[dict]:
    """Normalize a nested layout spec into a canonical dict structure.

    Leaves are represented as {} or null (both treated as a leaf pane).
    """
    if node is None or node == {}:
        return None
    if not isinstance(node, dict):
        raise ValueError(f"Invalid {path}: expected a mapping")

    allowed_keys = {'split', 'panes'}
    extra_keys = set(node.keys()) - allowed_keys
    if extra_keys:
        extra = ", ".join(sorted(extra_keys))
        raise ValueError(f"Invalid {path}: unexpected keys {extra}")

    split = node.get('split')
    panes = node.get('panes')
    if split is None or panes is None:
        raise ValueError(f"Invalid {path}: expected 'split' and 'panes'")
    if not isinstance(split, str):
        raise ValueError(f"Invalid {path}: 'split' must be a string")

    split_key = _LAYOUT_SPLIT_ALIASES.get(split.strip().lower())
    if split_key not in {'h', 'v'}:
        raise ValueError(f"Invalid {path}: 'split' must be 'h' or 'v'")

    if not isinstance(panes, list) or len(panes) != 2:
        raise ValueError(f"Invalid {path}: 'panes' must be a list of 2 items")

    return {
        'split': split_key,
        'panes': [
            _normalize_layout_node(panes[0], path=f"{path}.panes[0]"),
            _normalize_layout_node(panes[1], path=f"{path}.panes[1]"),
        ],
    }


def _parse_target_path(value: Any) -> Tuple[int, ...]:
    if value is None:
        raise ValueError("tmux.target_pane is required when tmux.layout is set")
    if isinstance(value, (int, bool)):
        parts = [value]
    elif isinstance(value, list):
        parts = value
    elif isinstance(value, str):
        text = value.strip()
        if not text:
            return tuple()
        parts = text.replace('/', '.').split('.')
    else:
        raise ValueError("tmux.target_pane must be a list or dot-separated string")

    path: list[int] = []
    for item in parts:
        if isinstance(item, bool):
            raise ValueError("tmux.target_pane entries must be 0 or 1")
        try:
            index = int(item)
        except (TypeError, ValueError):
            raise ValueError("tmux.target_pane entries must be 0 or 1")
        if index not in (0, 1):
            raise ValueError("tmux.target_pane entries must be 0 or 1")
        path.append(index)
    return tuple(path)


def _resolve_pane_id(target: str) -> str:
    result = subprocess.run(
        ['tmux', 'display-message', '-p', '-t', target, '#{pane_id}'],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        error = (result.stderr or result.stdout).strip()
        raise ValueError(f"Failed to resolve pane id for tmux target {target}: {error}")
    pane_id = result.stdout.strip()
    if not pane_id:
        raise ValueError(f"Failed to resolve pane id for tmux target {target}")
    return pane_id


def _set_pane_title(pane_target: str, title: str) -> None:
    subprocess.run(
        ['tmux', 'select-pane', '-t', pane_target, '-T', title],
        capture_output=True,
        text=True,
    )


def _split_pane(pane_id: str, split: str) -> str:
    split_flag = '-h' if split == 'h' else '-v'
    result = subprocess.run(
        ['tmux', 'split-window', split_flag, '-d', '-t', pane_id, '-P', '-F', '#{pane_id}'],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        error = (result.stderr or result.stdout).strip()
        raise ValueError(f"Failed to split pane {pane_id}: {error}")
    new_pane_id = result.stdout.strip()
    if not new_pane_id:
        raise ValueError(f"Failed to resolve new pane id for {pane_id}")
    return new_pane_id


def _build_layout(
    pane_id: str,
    layout: Optional[dict],
    *,
    pane_map: Dict[Tuple[int, ...], str],
    path: Tuple[int, ...] = (),
) -> None:
    if layout is None:
        pane_map[path] = pane_id
        return

    new_pane_id = _split_pane(pane_id, layout['split'])
    _build_layout(pane_id, layout['panes'][0], pane_map=pane_map, path=path + (0,))
    _build_layout(new_pane_id, layout['panes'][1], pane_map=pane_map, path=path + (1,))


def start_session_with_layout(
    agent_id: str,
    command: str,
    *,
    layout_spec: Any,
    target_path: Any,
    session_layout: str = "sessions",
) -> str:
    """Start an agent and place it into a specific pane within a generated layout.

    This starts a placeholder shell first, creates the tmux split layout, then respawns the
    configured target pane to run the real command.
    """
    layout = _normalize_layout_node(layout_spec)
    if layout is None:
        raise ValueError("tmux.layout must define at least one split")
    target = _parse_target_path(target_path)

    if not start_session(agent_id, "bash", layout=session_layout):
        raise ValueError("Failed to start tmux container for agent")

    try:
        root_target = _agent_pane_target(agent_id)
        if not root_target:
            raise ValueError("Failed to resolve agent tmux target after startup")
        root_pane_id = _resolve_pane_id(root_target)

        pane_map: Dict[Tuple[int, ...], str] = {}
        _build_layout(root_pane_id, layout, pane_map=pane_map)
        if target not in pane_map:
            raise ValueError(f"tmux.target_pane {target} does not match any leaf pane")

        expected_title = _window_name_for_agent(agent_id)
        for path, pane_id in pane_map.items():
            if path == target:
                _set_pane_title(pane_id, expected_title)
            else:
                suffix = ".".join(str(i) for i in path) if path else "root"
                _set_pane_title(pane_id, f"{expected_title}:{suffix}")

        target_pane = pane_map[target]
        result = subprocess.run(
            ['tmux', 'respawn-pane', '-k', '-t', target_pane, command],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            error = (result.stderr or result.stdout).strip()
            raise ValueError(f"Failed to launch command in target pane: {error}")

        subprocess.run(['tmux', 'select-pane', '-t', target_pane], capture_output=True, text=True)
        return target_pane
    except Exception:
        stop_session(agent_id)
        raise


def stop_session(agent_id: str) -> bool:
    """
    Stop (kill) a tmux session.

    Args:
        agent_id: Agent ID (e.g., 'emp-0001', without agent- prefix)

    Returns:
        True if session was stopped
    """
    session_name = _session_name_for_agent(agent_id)
    if _tmux_has_session(session_name):
        result = subprocess.run(
            ['tmux', 'kill-session', '-t', session_name],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0

    if _group_window_exists(agent_id):
        group = get_group_session_name()
        window_name = _window_name_for_agent(agent_id)
        result = subprocess.run(
            ['tmux', 'kill-window', '-t', f"{group}:{window_name}"],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0

    return False


def capture_output(agent_id: str, lines: int = 100) -> Optional[str]:
    """
    Capture recent output from a tmux session.

    Args:
        agent_id: Agent ID (e.g., 'emp-0001', without agent- prefix)
        lines: Number of lines to capture (from the end)

    Returns:
        Captured output, or None if session doesn't exist
    """
    if not session_exists(agent_id):
        return None

    target = _agent_pane_target(agent_id)
    if not target:
        return None

    result = subprocess.run([
        'tmux', 'capture-pane', '-p', '-t', target, f'-S-{lines}'
    ], capture_output=True, text=True)

    if result.returncode != 0:
        return None

    return result.stdout


def send_keys(
    agent_id: str,
    keys: str,
    *,
    send_enter: bool = True,
    clear_input: bool = False,
    escape_first: bool = False,
    enter_via_key: bool = False,
) -> bool:
    """
    Send keys to a tmux session.

    Args:
        agent_id: Agent ID (e.g., 'emp-0001', without agent- prefix)
        keys: Keys to send
        send_enter: Whether to send Enter after the keys (default: True)
        clear_input: Whether to clear current input line before sending text
        escape_first: Whether to send Escape before sending text
        enter_via_key: Whether to send Enter as a real keypress first (needed by some TUIs)

    Returns:
        True if keys were sent successfully
    """
    if not session_exists(agent_id):
        return False

    target = _agent_pane_target(agent_id)
    if not target:
        return False

    def _send_tmux_key(key: str) -> bool:
        result = subprocess.run(
            ['tmux', 'send-keys', '-t', target, key],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0

    def _send_literal(text: str) -> bool:
        if not text:
            return True
        result = subprocess.run(
            ['tmux', 'send-keys', '-t', target, '-l', text],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0

    op_gap_seconds = 0.12

    def _send_enter() -> bool:
        # Some TUIs (notably Codex) require a real Enter keypress to confirm submit.
        # Try native key first when requested, and verify pane output changes.
        # If output does not change, fall back to newline paste to avoid idle stalls.
        def _capture_tail(lines: int = 30) -> Optional[str]:
            result = subprocess.run(
                ['tmux', 'capture-pane', '-p', '-t', target, f'-S-{max(1, int(lines))}'],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                return None
            return result.stdout

        def _pane_changed(reference: Optional[str], *, attempts: int = 3, interval: float = 0.1) -> bool:
            if reference is None:
                return False
            for _ in range(max(1, attempts)):
                time.sleep(interval)
                current = _capture_tail()
                if current is not None and current != reference:
                    return True
            return False

        if enter_via_key:
            before = _capture_tail()
            if _send_tmux_key('C-m') or _send_tmux_key('Enter'):
                if _pane_changed(before):
                    return True

        # Fallback: paste a newline for TUIs where keypress Enter is unreliable.
        fallback_before = _capture_tail()
        try:
            subprocess.run(
                ['tmux', 'load-buffer', '-b', 'enter-key', '-'],
                input='\n',
                capture_output=True,
                text=True,
                check=True,
            )
            subprocess.run(
                ['tmux', 'paste-buffer', '-d', '-b', 'enter-key', '-t', target],
                capture_output=True,
                text=True,
                check=True,
            )
            return _pane_changed(fallback_before)
        except Exception:
            return False

    if escape_first:
        _send_tmux_key('Escape')
        time.sleep(op_gap_seconds)

    if clear_input:
        _send_tmux_key('C-u')
        time.sleep(op_gap_seconds)

    # For multi-line content, paste via tmux buffer (more reliable than send-keys).
    if '\n' in keys:
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(keys)
            temp_file = f.name

        try:
            subprocess.run(
                ['tmux', 'load-buffer', '-b', 'agent-send', temp_file],
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ['tmux', 'paste-buffer', '-d', '-b', 'agent-send', '-t', target],
                capture_output=True,
                check=True,
            )
            # Wait for paste to complete before sending Enter
            time.sleep(1.0)
        except Exception:
            return False
        finally:
            import os
            try:
                os.unlink(temp_file)
            except Exception:
                pass
    else:
        # Chunk long messages to avoid dropping keys under load.
        chunk_size = 100
        for start in range(0, len(keys), chunk_size):
            chunk = keys[start:start + chunk_size]
            if not _send_literal(chunk):
                return False
            time.sleep(0.1)

    # Send carriage return as a separate command (more reliable than combining in one send-keys).
    if send_enter:
        return _send_enter()

    return True


def _is_codex_model_choice_prompt(output: str) -> bool:
    """Detect Codex first-run/upgrade model selection prompt (non-interactive blocker)."""
    if not output:
        return False
    lowered = output.lower()
    if 'codex just got an upgrade' in lowered:
        return True
    if 'choose how you' in lowered and 'codex' in lowered and 'try new model' in lowered and 'use existing model' in lowered:
        return True
    return False


def _tmux_send_key(agent_id: str, key: str) -> bool:
    """Send a tmux key name (e.g., 'Down') to an agent pane (layout-safe)."""
    if not session_exists(agent_id):
        return False
    target = _agent_pane_target(agent_id)
    if not target:
        return False
    result = subprocess.run(
        ['tmux', 'send-keys', '-t', target, key],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def _dismiss_codex_model_choice_prompt(agent_id: str) -> bool:
    """Best-effort dismissal of Codex model selection prompt."""
    if not session_exists(agent_id):
        return False

    # Prefer "Use existing model" (option 2) to preserve prior behavior.
    if not send_keys(agent_id, "2", send_enter=True, enter_via_key=True):
        return False

    time.sleep(1.0)
    tail = capture_output(agent_id, lines=80) or ""
    if not _is_codex_model_choice_prompt(tail):
        return True

    # Fallback: move selection down then Enter (or just Enter if Down fails).
    _tmux_send_key(agent_id, 'Down')
    send_keys(agent_id, "", send_enter=True, enter_via_key=True)
    time.sleep(1.0)
    tail_after = capture_output(agent_id, lines=80) or ""
    return not _is_codex_model_choice_prompt(tail_after)


def recover_codex_interrupted(agent_id: str) -> bool:
    """Dismiss a Codex suggestion tip and return the agent to a clean prompt.

    When Codex drops a suggestion tip mid-turn (``› Write tests for @filename``),
    the turn is interrupted and the agent is stuck.  This function sends Escape
    to dismiss the suggestion, waits briefly, and verifies the prompt is clean.

    Returns True if the agent appears recovered (idle at clean prompt).
    """
    if not session_exists(agent_id):
        return False

    # Escape dismisses the inline suggestion tip.
    send_keys(agent_id, '', send_enter=False, escape_first=True)
    time.sleep(0.5)
    # Clear any leftover text on the input line.
    send_keys(agent_id, '', send_enter=False, clear_input=True)
    time.sleep(0.5)

    output = capture_output(agent_id, lines=30) or ''
    # Check that 'Conversation interrupted' is no longer in recent output
    # and no suggestion tip remains.
    if 'Conversation interrupted' in output:
        # One more Escape + clear cycle
        send_keys(agent_id, '', send_enter=False, escape_first=True)
        time.sleep(0.3)
        send_keys(agent_id, '', send_enter=False, clear_input=True)
        time.sleep(0.5)

    return True


def _is_codex_loading_output(output: str) -> bool:
    return bool(re.search(r'\bmodel:\s+loading\b', str(output or ''), re.IGNORECASE))


def _codex_recent_output(output: str, *, max_lines: int = 20) -> str:
    lines = str(output or '').splitlines()
    if len(lines) <= max_lines:
        return str(output or '')
    return '\n'.join(lines[-max_lines:])


def stabilize_codex_session(
    agent_id: str,
    *,
    timeout: int = 20,
    stable_samples: int = 2,
    poll_interval: float = 1.0,
) -> bool:
    """Wait until a Codex session is actually usable for the next turn.

    A visible Codex prompt is not sufficient. Fresh sessions often surface
    loading banners, inline suggestion tips, or "Conversation interrupted"
    state before they become stable. This helper actively clears recoverable
    interrupted states and only returns once the session is idle for multiple
    consecutive samples.
    """
    if not session_exists(agent_id):
        return False

    target = _agent_pane_target(agent_id)
    if not target:
        return False

    stable_needed = max(1, int(stable_samples))
    sleep_seconds = max(0.2, float(poll_interval))
    deadline = time.time() + max(1, int(timeout))
    stable_count = 0
    model_prompt_attempts = 0

    while time.time() < deadline:
        capture = subprocess.run(
            ['tmux', 'capture-pane', '-p', '-t', target, '-S-40'],
            capture_output=True,
            text=True,
        )
        output = capture.stdout if capture.returncode == 0 else ''
        recent_output = _codex_recent_output(output, max_lines=20)

        if _is_codex_model_choice_prompt(recent_output):
            stable_count = 0
            if model_prompt_attempts < 3:
                model_prompt_attempts += 1
                _dismiss_codex_model_choice_prompt(agent_id)
            time.sleep(sleep_seconds)
            continue

        runtime = get_agent_runtime_state(agent_id, launcher='codex')
        state = str(runtime.get('state', 'unknown'))
        reason = str(runtime.get('reason', 'unknown'))

        if _is_codex_loading_output(recent_output):
            stable_count = 0
            time.sleep(sleep_seconds)
            continue

        if (
            state == 'interrupted'
            or 'Conversation interrupted' in recent_output
            or reason.startswith('interrupted:')
            or reason.startswith('suggestion_tip:')
        ):
            stable_count = 0
            recover_codex_interrupted(agent_id)
            time.sleep(sleep_seconds)
            continue

        if state == 'idle':
            stable_count += 1
            if stable_count >= stable_needed:
                return True
        else:
            stable_count = 0

        time.sleep(sleep_seconds)

    return False


def inject_system_prompt(agent_id: str, prompt: str) -> bool:
    """
    Inject system prompt to agent and wait for it to be processed.

    Args:
        agent_id: Agent ID (e.g., 'emp-0001')
        prompt: System prompt content

    Returns:
        True if injection successful
    """
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))

    target = _agent_pane_target(agent_id)
    if not target:
        return False

    # Write prompt to a temp file for reliable multi-line injection
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(prompt)
        f.write('\n')  # Ensure trailing newline
        temp_file = f.name

    try:
        # Use tmux's load-buffer to paste the content
        # This is more reliable than send-keys for multi-line content
        subprocess.run([
            'tmux', 'load-buffer', '-b', 'agent-prompt', temp_file
        ], capture_output=True, check=True)

        # Paste the buffer content
        subprocess.run([
            'tmux', 'paste-buffer', '-d', '-b', 'agent-prompt', '-t', target
        ], capture_output=True, check=True)

        # Wait a bit for paste to complete
        time.sleep(1)

        # Send Enter to execute the pasted content using load-buffer (more reliable)
        subprocess.run(
            ['tmux', 'load-buffer', '-b', 'enter-key', '-'],
            input='\n',
            capture_output=True,
            text=True,
            check=True,
        )
        subprocess.run(
            ['tmux', 'paste-buffer', '-d', '-b', 'enter-key', '-t', target],
            capture_output=True,
            text=True,
            check=True,
        )

        return True
    except Exception as e:
        print(f"  Debug: Injection error - {e}")
        return False
    finally:
        import os
        try:
            os.unlink(temp_file)
        except:
            pass


def wait_for_agent_ready(agent_id: str, launcher: str, timeout: int = 45) -> bool:
    """
    Wait for agent to be ready after system prompt injection.

    This checks if the agent has processed the system prompt and is ready for tasks.

    Args:
        agent_id: Agent ID (e.g., 'emp-0001')
        launcher: Launcher path/name to detect CLI type
        timeout: Maximum seconds to wait (default: 45)

    Returns:
        True if agent is ready, False if timeout
    """
    target = _agent_pane_target(agent_id)
    if not target:
        return False

    # Import provider system
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from providers import get_prompt_patterns

    prompt_patterns = get_prompt_patterns(launcher)

    start_time = time.time()
    check_interval = 2  # Check every 2 seconds
    min_wait = 3  # Minimum wait time before first check

    # Some TUIs (e.g., OpenCode) don't expose a stable prompt via tmux capture-pane.
    # In that case, treat "started" as "ready" after the minimum wait.
    if not prompt_patterns:
        time.sleep(min_wait)
        return True

    # Detect provider for special handling
    launcher_lower = launcher.lower()
    is_droid = 'droid' in launcher_lower
    is_codex = 'codex' in launcher_lower

    # Give agent time to process the prompt
    time.sleep(min_wait)

    if is_codex:
        remaining = max(1, int(timeout - (time.time() - start_time)))
        return stabilize_codex_session(agent_id, timeout=remaining, stable_samples=2, poll_interval=1.0)

    codex_model_prompt_attempts = 0
    while (time.time() - start_time) < timeout:
        # Capture recent output
        result = subprocess.run([
            'tmux', 'capture-pane', '-p', '-t', target, '-S-15'
        ], capture_output=True, text=True)

        if result.returncode == 0:
            output = result.stdout

            # Special handling for droid: check for droid-specific patterns
            if is_droid:
                # Droid shows help text when ready
                if '? for help' in output or '/ide for VS Code' in output:
                    return True

            # Special handling for codex: dismiss first-run/upgrade model selection prompt.
            if is_codex and codex_model_prompt_attempts < 3 and _is_codex_model_choice_prompt(output):
                codex_model_prompt_attempts += 1
                _dismiss_codex_model_choice_prompt(agent_id)
                time.sleep(1.0)
                continue

            # Special handling for codex: prompt may include inline suggestions (e.g. "› Summarize...")
            if is_codex:
                for line in output.split('\n'):
                    stripped = line.strip()
                    if stripped.startswith(('›', '❯')) and not _CODEX_MENU_OPTION_RE.match(stripped):
                        return True
                # Also check for mode line which indicates readiness
                if 'Auto (High)' in output or 'shift+tab to cycle modes' in output:
                    return True

            # Check for prompt pattern (agent ready for input)
            for pattern in prompt_patterns:
                if pattern in output:
                    lines = output.split('\n')
                    for line in lines:
                        stripped = line.strip()
                        # For droid, be more lenient with prompt detection
                        if is_droid:
                            if stripped.startswith('>'):
                                return True
                        elif is_codex:
                            if stripped.startswith(pattern) and not _CODEX_MENU_OPTION_RE.match(stripped):
                                return True
                        else:
                            # Look for standalone prompt
                            if stripped == pattern or (stripped.startswith(pattern) and len(stripped) <= 3):
                                return True

        time.sleep(check_interval)

    return False


def get_session_info(agent_id: str) -> Optional[Dict[str, str]]:
    """
    Get detailed information about a session.

    Args:
        agent_id: Agent ID (e.g., 'emp-0001', without agent- prefix)

    Returns:
        Dict with 'agent_id', 'session', 'status', or None if not found
    """
    if not session_exists(agent_id):
        return None

    session_name = _session_name_for_agent(agent_id)
    if _tmux_has_session(session_name):
        # Get session info from tmux ls
        result = subprocess.run(['tmux', 'ls'], capture_output=True, text=True)

        if result.returncode != 0:
            return None

        for line in result.stdout.split('\n'):
            if line.startswith(f"{session_name}:"):
                # Parse session info (e.g., "agent-emp-0001: 1 windows (created Fri Jan  3 10:00:00 2025)")
                parts = line.split('(', 1)
                status = "running" if len(parts) > 1 else "unknown"

                return {
                    'agent_id': agent_id,
                    'session': session_name,
                    'status': status,
                    'mode': 'sessions',
                }

        return {
            'agent_id': agent_id,
            'session': session_name,
            'status': 'running',
            'mode': 'sessions',
        }

    if _group_window_exists(agent_id):
        group = get_group_session_name()
        window_name = _window_name_for_agent(agent_id)
        return {
            'agent_id': agent_id,
            'session': f"{group}:{window_name}",
            'status': 'running',
            'mode': 'windows',
        }

    return None


def is_agent_busy(agent_id: str, launcher: str = "") -> bool:
    """
    Check if an agent is currently busy (processing/thinking).

    Args:
        agent_id: Agent ID (e.g., 'emp-0001')
        launcher: Optional launcher path for provider-specific detection

    Returns:
        True if agent is busy (should not send new tasks)
    """
    runtime = get_agent_runtime_state(agent_id, launcher=launcher)
    return str(runtime.get('state', 'unknown')) in {'busy', 'stuck'}


def _parse_elapsed_seconds(output: str) -> Optional[int]:
    return parse_elapsed_seconds(output)


def _detect_error_reason(output: str) -> Optional[str]:
    return detect_error_reason(output)


def is_agent_blocked(agent_id: str, launcher: str = "") -> bool:
    runtime = get_agent_runtime_state(agent_id, launcher=launcher)
    return str(runtime.get('state', 'unknown')) == 'blocked'


def _get_runtime_config(launcher: str) -> Dict[str, object]:
    runtime_config: Dict[str, object] = {
        'busy_patterns': [
            '✻ Thinking',
            'Thinking...',
            '⏳ Thinking',
            '(esc to interrupt',
        ],
        'blocked_patterns': [
            'all actions require approval',
            'actions require approval',
            'requires approval',
            'waiting for approval',
        ],
        'stuck_after_seconds': 180,
    }
    try:
        import sys
        from pathlib import Path

        sys.path.insert(0, str(Path(__file__).parent.parent))
        from providers import get_runtime_config

        provider_runtime_config = get_runtime_config(launcher)
        if isinstance(provider_runtime_config, dict):
            runtime_config.update(provider_runtime_config)
    except Exception:
        pass
    return runtime_config


def get_agent_runtime_state(agent_id: str, launcher: str = "") -> Dict[str, object]:
    """Return unified runtime state using the shared runtime state machine.

    States are normalized to:
      idle|busy|blocked|stuck|error|unknown
    """
    runtime_config = _get_runtime_config(launcher)

    if not session_exists(agent_id):
        return evaluate_runtime_state(
            output="",
            runtime_config=runtime_config,
            session_running=False,
        )

    target = _agent_pane_target(agent_id)
    if not target:
        return evaluate_runtime_state(
            output="",
            runtime_config=runtime_config,
            output_readable=False,
            force_state='unknown',
            force_reason='missing_tmux_target',
        )

    result = subprocess.run(
        ['tmux', 'capture-pane', '-p', '-t', target, '-S-200'],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return evaluate_runtime_state(
            output="",
            runtime_config=runtime_config,
            output_readable=False,
        )

    output = result.stdout
    if launcher and 'codex' in launcher.lower():
        output = _codex_recent_output(output)
    elapsed_seconds = _parse_elapsed_seconds(output)

    if launcher and 'codex' in launcher.lower() and _is_codex_model_choice_prompt(output):
        now = time.time()
        last_failure = _CODEX_MODEL_PROMPT_LAST_FAILURE.get(agent_id)
        if last_failure is not None and (now - last_failure) < _CODEX_MODEL_PROMPT_FAILURE_THROTTLE_S:
            return evaluate_runtime_state(
                output=output,
                runtime_config=runtime_config,
                elapsed_seconds=elapsed_seconds,
                force_state='blocked',
                force_reason='codex_model_choice',
            )

        if _dismiss_codex_model_choice_prompt(agent_id):
            time.sleep(0.5)
            recapture = subprocess.run(
                ['tmux', 'capture-pane', '-p', '-t', target, '-S-200'],
                capture_output=True,
                text=True,
            )
            if recapture.returncode == 0:
                output = recapture.stdout
                elapsed_seconds = _parse_elapsed_seconds(output)
            else:
                return evaluate_runtime_state(
                    output="",
                    runtime_config=runtime_config,
                    output_readable=False,
                )
        else:
            _CODEX_MODEL_PROMPT_LAST_FAILURE[agent_id] = now
            return evaluate_runtime_state(
                output=output,
                runtime_config=runtime_config,
                elapsed_seconds=elapsed_seconds,
                force_state='blocked',
                force_reason='codex_model_choice',
            )

    return evaluate_runtime_state(
        output=output,
        runtime_config=runtime_config,
        elapsed_seconds=elapsed_seconds,
        error_reason=_detect_error_reason(output),
    )


def attach_session(agent_id: str) -> bool:
    """
    Attach to a tmux session (for interactive use).

    Args:
        agent_id: Agent ID (e.g., 'emp-0001', without agent- prefix)

    Returns:
        True if attachment succeeded (note: this blocks the terminal)
    """
    if not session_exists(agent_id):
        return False

    attach_target = _agent_attach_target(agent_id)
    if not attach_target:
        return False

    # This will block and take over the terminal
    result = subprocess.run(['tmux', 'attach', '-t', attach_target])

    return result.returncode == 0


def wait_for_prompt(agent_id: str, launcher: str, timeout: int = 30) -> bool:
    """
    Wait for CLI prompt to appear in the session.

    Args:
        agent_id: Agent ID (e.g., 'emp-0001')
        launcher: Launcher path/name to detect CLI type
        timeout: Maximum seconds to wait (default: 30)

    Returns:
        True if prompt detected, False if timeout
    """
    # Import provider system
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from providers import get_prompt_patterns, get_startup_wait, PROVIDERS

    target = _agent_pane_target(agent_id)
    if not target:
        return False

    # Get prompt patterns based on launcher (provider)
    prompt_patterns = get_prompt_patterns(launcher)
    startup_wait = get_startup_wait(launcher)

    # Detect provider for special handling
    launcher_lower = launcher.lower()
    is_droid = 'droid' in launcher_lower
    is_codex = 'codex' in launcher_lower

    # Initial wait for CLI to start
    time.sleep(startup_wait)

    # Some TUIs (e.g., OpenCode) don't expose a stable prompt via tmux capture-pane.
    # In that case, treat "started" as "ready" after startup_wait.
    if not prompt_patterns:
        return True

    start_time = time.time()
    check_interval = 1  # Check every second

    codex_model_prompt_attempts = 0
    while (time.time() - start_time) < timeout:
        # Capture last few lines of output
        result = subprocess.run([
            'tmux', 'capture-pane', '-p', '-t', target, '-S-20'
        ], capture_output=True, text=True)

        if result.returncode == 0:
            output = result.stdout

            # Special handling for droid: check for droid-specific patterns
            if is_droid:
                # Droid shows help text when ready
                if '? for help' in output or '/ide for VS Code' in output:
                    return True

            # Special handling for codex: dismiss first-run/upgrade model selection prompt.
            if is_codex and codex_model_prompt_attempts < 3 and _is_codex_model_choice_prompt(output):
                codex_model_prompt_attempts += 1
                _dismiss_codex_model_choice_prompt(agent_id)
                time.sleep(1.0)
                continue

            # Special handling for codex: prompt may include inline suggestions (e.g. "› Summarize...")
            if is_codex:
                for line in output.split('\n'):
                    stripped = line.strip()
                    if stripped.startswith(('›', '❯')) and not _CODEX_MENU_OPTION_RE.match(stripped):
                        return True
                # Also check for mode line which indicates readiness
                if 'Auto (High)' in output or 'shift+tab to cycle modes' in output:
                    return True

            # Standard prompt detection
            for pattern in prompt_patterns:
                if pattern in output:
                    lines = output.split('\n')
                    for line in lines:
                        stripped = line.strip()
                        # For droid, be more lenient with prompt detection
                        if is_droid:
                            if stripped.startswith('>'):
                                return True
                        elif is_codex:
                            if stripped.startswith(pattern) and not _CODEX_MENU_OPTION_RE.match(stripped):
                                return True
                        else:
                            # Standard check: line is just the prompt
                            if stripped == pattern or (stripped.startswith(pattern) and len(stripped) <= 3):
                                return True

        time.sleep(check_interval)

    return False
