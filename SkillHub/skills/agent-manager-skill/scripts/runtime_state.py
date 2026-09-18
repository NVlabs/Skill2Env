"""Runtime state machine for agent status detection.

This module centralizes runtime state evaluation so callers can rely on one
consistent API.
"""

from __future__ import annotations
import re
from typing import Dict, Optional, Sequence, Any


RUNTIME_STATES = {
    'idle',
    'busy',
    'blocked',
    'stuck',
    'interrupted',
    'error',
    'unknown',
}


def normalize_runtime_state(state: str) -> str:
    value = (state or '').strip().lower()
    return value if value in RUNTIME_STATES else 'unknown'


def detect_first_pattern(output: str, patterns: Sequence[str]) -> Optional[str]:
    if not output or not patterns:
        return None
    for pattern in patterns:
        if pattern and pattern in output:
            return pattern
    return None


def _tail_text(output: str, *, max_lines: int) -> str:
    lines = str(output or '').splitlines()
    if len(lines) <= max_lines:
        return str(output or '')
    return "\n".join(lines[-max_lines:])


def _detect_codex_conversation_interrupted(output: str) -> bool:
    """True only when Codex's UI interrupted marker is visible.

    We intentionally do NOT treat the plain substring "Conversation interrupted" as
    a runtime state, because it can appear in user-provided text (e.g. Slack
    messages, quoted logs, runbooks) and would cause false positives.
    """
    # Codex renders a square marker at the start of the line.
    return bool(re.search(r'(?m)^\s*■\s*Conversation interrupted\b', str(output or '')))


def parse_elapsed_seconds(output: str) -> Optional[int]:
    """Best-effort parse of an on-screen elapsed timer (e.g., "[⏱ 5m 7s]")."""
    if not output:
        return None

    match = re.search(r"\[\s*(?:⏱|⏳)\s*(\d+)m\s*(\d+)s\s*\]", output)
    if match:
        minutes = int(match.group(1))
        seconds = int(match.group(2))
        return minutes * 60 + seconds

    match = re.search(r"\[\s*(?:⏱|⏳)\s*(\d+)s\s*\]", output)
    if match:
        return int(match.group(1))

    match = re.search(r"\b(\d+\.\d+)s\b", output)
    if match:
        try:
            return int(float(match.group(1)))
        except Exception:
            return None

    return None


def detect_error_reason(output: str) -> Optional[str]:
    """Best-effort detect a terminal/tool error in recent agent output."""
    if not output:
        return None

    lowered = output.lower()

    if 'stopped after 10 redirects' in lowered:
        return 'redirect_loop'
    if 'error 522' in lowered or 'cloudflare ray id' in lowered:
        return 'cloudflare_522'
    if 'error: 500 post ' in lowered:
        return 'http_500'

    if 'api error: 400' in lowered and 'unknown provider' in lowered:
        return 'unknown_provider'
    if 'invalid_request_error' in lowered:
        return 'invalid_request'

    # Be conservative with "timeout": it can appear in normal logs/metrics
    # (e.g. "timeout/cancel/unwind") and should not force an error state.
    if 'timed out' in lowered:
        return 'timeout'
    if 'timeout' in lowered:
        if re.search(r"\b(etimedout|deadline exceeded|context deadline exceeded)\b", lowered):
            return 'timeout'

        # Only treat "timeout" as an error when it is clearly part of an error line.
        # Avoid false positives where "timeout" appears in normal domain text
        # (e.g. "timeout/cancel/unwind" metrics) and other unrelated lines contain
        # words like "failure modes".
        for line in lowered.splitlines():
            if 'timeout' not in line:
                continue
            if re.search(r"\b(etimedout|deadline exceeded|context deadline exceeded|timed out)\b", line):
                return 'timeout'
            if re.search(r"\b(error|failed|exception|traceback)\b", line):
                return 'timeout'
            if re.search(r"\bfailure\b", line) and not re.search(r"\bfailure modes\b", line):
                return 'timeout'
    if 'econnrefused' in lowered or 'connection refused' in lowered:
        return 'connection_refused'
    if 'etimedout' in lowered:
        return 'connection_timed_out'

    return None


def evaluate_runtime_state(
    *,
    output: str,
    runtime_config: Optional[Dict[str, Any]] = None,
    elapsed_seconds: Optional[int] = None,
    error_reason: Optional[str] = None,
    session_running: bool = True,
    output_readable: bool = True,
    force_state: Optional[str] = None,
    force_reason: Optional[str] = None,
) -> Dict[str, object]:
    """Evaluate runtime state from pane output + provider runtime patterns.

    Returns dict with at least:
      - state: one of idle|busy|blocked|stuck|error|unknown
      - reason: trigger reason when available
      - elapsed_seconds: optional parsed timer
    """
    cfg = runtime_config or {}
    busy_patterns = list(cfg.get('busy_patterns', []) or [])
    blocked_patterns = list(cfg.get('blocked_patterns', []) or [])

    try:
        stuck_after_seconds = int(cfg.get('stuck_after_seconds', 180))
    except Exception:
        stuck_after_seconds = 180
    if stuck_after_seconds <= 0:
        stuck_after_seconds = 180

    payload: Dict[str, object] = {}
    if elapsed_seconds is not None:
        payload['elapsed_seconds'] = elapsed_seconds

    if force_state:
        payload['state'] = normalize_runtime_state(force_state)
        payload['reason'] = (force_reason or 'forced').strip()
        return payload

    if not session_running:
        payload['state'] = 'unknown'
        payload['reason'] = 'session_not_running'
        return payload

    if not output_readable:
        payload['state'] = 'unknown'
        payload['reason'] = 'unreadable_output'
        return payload

    if not isinstance(output, str):
        payload['state'] = 'unknown'
        payload['reason'] = 'invalid_output'
        return payload

    blocked_pattern = detect_first_pattern(output, blocked_patterns)
    if blocked_pattern:
        payload['state'] = 'blocked'
        payload['reason'] = f'blocked_pattern:{blocked_pattern}'
        return payload

    # Detect interrupted turn (Codex suggestion tip appeared mid-turn).
    interrupted_patterns = list(cfg.get('interrupted_patterns', []) or [])
    suggestion_tip_re = cfg.get('suggestion_tip_pattern')
    # Only classify as interrupted when Codex's UI marker is present in recent output.
    # Do not let arbitrary quoted text (e.g. Slack messages) trigger it.
    interrupted_match = detect_first_pattern(output, interrupted_patterns)
    if interrupted_match:
        tail = _tail_text(output, max_lines=20)
        if _detect_codex_conversation_interrupted(tail):
            payload['state'] = 'interrupted'
            payload['reason'] = f'interrupted:{interrupted_match}'
            return payload

    # Suggestion tip visible on last line(s) while no busy pattern → interrupted.
    if suggestion_tip_re:
        tail_lines = [ln.strip() for ln in output.strip().splitlines()[-5:] if ln.strip()]
        for line in tail_lines:
            if re.match(suggestion_tip_re, line) and '? for shortcuts' in output:
                payload['state'] = 'interrupted'
                payload['reason'] = f'suggestion_tip:{line[:60]}'
                return payload

    busy_pattern = detect_first_pattern(output, busy_patterns)
    if busy_pattern:
        if elapsed_seconds is not None and elapsed_seconds >= stuck_after_seconds:
            payload['state'] = 'stuck'
            payload['reason'] = f'busy_elapsed>={stuck_after_seconds}'
            return payload

        payload['state'] = 'busy'
        payload['reason'] = f'busy_pattern:{busy_pattern}'
        return payload

    if error_reason:
        payload['state'] = 'error'
        payload['reason'] = error_reason
        return payload

    if not output.strip():
        payload['state'] = 'unknown'
        payload['reason'] = 'empty_output'
        return payload

    payload['state'] = 'idle'
    payload['reason'] = 'ready'
    return payload
