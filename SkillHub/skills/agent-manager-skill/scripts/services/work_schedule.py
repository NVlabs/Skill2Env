"""Work schedule gate for heartbeat and scheduled jobs.

Determines whether the current moment falls within the configured work schedule
(work hours, work days, holidays, extra workdays).  Supports multiple schedule
rules with conditional ``when`` expressions for multi-machine deployments.
"""

from __future__ import annotations
import os
import re
import subprocess
from datetime import datetime, time as dt_time, date as dt_date
from typing import Optional
from zoneinfo import ZoneInfo


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def is_within_work_schedule(
    schedule: object,
    *,
    now: Optional[datetime] = None,
    env: Optional[dict] = None,
) -> tuple[bool, str]:
    """Check whether the current time is inside the configured work schedule.

    Args:
        schedule: ``heartbeat.schedule`` -- a single dict or a list of dicts.
        now:      Override the current wall-clock time (for testing).
        env:      Override environment variables (for testing).

    Returns:
        ``(is_active, reason)`` -- ``True`` when the heartbeat should proceed.
    """
    rules = _normalize_schedule(schedule)
    if not rules:
        return True, ""

    if env is None:
        env = dict(os.environ)

    for rule in rules:
        when_expr = str(rule.get("when") or "").strip()
        if when_expr and not _evaluate_when(when_expr, env):
            continue  # condition not met, try next rule
        return _check_single_rule(rule, now)

    # All rules had ``when`` conditions and none matched.
    return False, "no_matching_rule"


def format_schedule_summary(schedule: object) -> str:
    """Return a compact one-line human-readable summary.

    Examples::

        Asia/Shanghai 09:00-18:00 Mon-Fri 3holidays 1extra
        2rules when:$HOSTNAME
    """
    rules = _normalize_schedule(schedule)
    if not rules:
        return ""

    if len(rules) == 1:
        return _format_single_rule(rules[0])

    parts = [f"{len(rules)}rules"]
    has_when = any(str(r.get("when") or "").strip() for r in rules)
    if has_when:
        parts.append("when:conditional")
    return " ".join(parts)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_WHEN_CMP_RE = re.compile(
    r'^\$([A-Za-z_][A-Za-z0-9_]*)\s*(==|!=)\s*(.+)$'
)
_WHEN_TRUTHY_RE = re.compile(
    r'^\$([A-Za-z_][A-Za-z0-9_]*)$'
)
# $(command) == value  or  $(command) != value  or  $(command)
_WHEN_CMD_CMP_RE = re.compile(
    r'^\$\((.+?)\)\s*(==|!=)\s*(.+)$'
)
_WHEN_CMD_TRUTHY_RE = re.compile(
    r'^\$\((.+?)\)$'
)


def _run_when_command(cmd: str) -> str:
    """Run a shell command and return stripped stdout. Empty on failure."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=5,
        )
        return result.stdout.strip()
    except Exception:
        return ""


def _evaluate_when(expr: str, env: dict) -> bool:
    """Evaluate a simple condition expression.

    Supported forms::

        $VAR == value       env var comparison
        $VAR != value
        $VAR                env var truthy
        $(cmd) == value     shell command comparison
        $(cmd) != value
        $(cmd)              shell command truthy
    """
    # --- $(command) forms ---
    m = _WHEN_CMD_CMP_RE.match(expr)
    if m:
        actual = _run_when_command(m.group(1))
        op, expected = m.group(2), m.group(3).strip()
        if op == "==":
            return actual == expected
        return actual != expected

    m = _WHEN_CMD_TRUTHY_RE.match(expr)
    if m:
        return bool(_run_when_command(m.group(1)))

    # --- $VAR forms ---
    m = _WHEN_CMP_RE.match(expr)
    if m:
        var_name, op, expected = m.group(1), m.group(2), m.group(3).strip()
        actual = str(env.get(var_name, "")).strip()
        if op == "==":
            return actual == expected
        return actual != expected

    m = _WHEN_TRUTHY_RE.match(expr)
    if m:
        return bool(str(env.get(m.group(1), "")).strip())

    # Unrecognised expression -- fail open (treat as matched).
    return True


def _normalize_schedule(schedule: object) -> list[dict]:
    """Normalise schedule config into a list of rule dicts."""
    if not schedule:
        return []
    if isinstance(schedule, dict):
        return [schedule]
    if isinstance(schedule, list):
        return [r for r in schedule if isinstance(r, dict)]
    return []


def _check_single_rule(
    rule: dict,
    now: Optional[datetime],
) -> tuple[bool, str]:
    """Evaluate time/day/holiday constraints for one rule."""
    tz_name = str(rule.get("timezone") or "").strip()

    # Resolve timezone (needed for date/time checks).
    tz: Optional[ZoneInfo] = None
    if tz_name:
        try:
            tz = ZoneInfo(tz_name)
        except (KeyError, Exception):
            # Timezone specified but invalid -- fail open.
            return True, ""

    if now is None:
        now = datetime.now(tz) if tz else datetime.now()
    elif tz:
        if now.tzinfo is None:
            now = now.replace(tzinfo=tz)
        else:
            now = now.astimezone(tz)

    today = now.date()
    current_time = now.time().replace(tzinfo=None)
    iso_weekday = today.isoweekday()  # 1=Mon .. 7=Sun

    extra_workdays = _parse_date_list(rule.get("extra_workdays"))
    holidays = _parse_date_list(rule.get("holidays"))
    is_extra = today in extra_workdays

    if not is_extra:
        if today in holidays:
            return False, f"holiday:{today.isoformat()}"

        work_days = rule.get("work_days")
        if work_days is None:
            work_days = [1, 2, 3, 4, 5]
        if iso_weekday not in {int(d) for d in work_days}:
            return False, f"non_workday:{today.strftime('%a')}"

    # Work hours (applies to extra workdays too).
    work_hours = rule.get("work_hours")
    if work_hours and isinstance(work_hours, dict):
        start_str = str(work_hours.get("start") or "").strip()
        end_str = str(work_hours.get("end") or "").strip()
        if start_str and end_str:
            try:
                start_t = _parse_time(start_str)
                end_t = _parse_time(end_str)
            except (ValueError, IndexError):
                return True, ""  # malformed -- fail open
            if start_t <= end_t:
                # Normal range: e.g. 09:00-18:00
                in_range = start_t <= current_time < end_t
            else:
                # Overnight range: e.g. 21:00-09:00 → active if >= 21:00 OR < 09:00
                in_range = current_time >= start_t or current_time < end_t
            if not in_range:
                return False, f"outside_hours:{current_time.strftime('%H:%M')}"

    return True, ""


def _parse_date_list(raw: object) -> set[dt_date]:
    if not raw or not isinstance(raw, list):
        return set()
    result: set[dt_date] = set()
    for item in raw:
        try:
            result.add(dt_date.fromisoformat(str(item).strip()))
        except (ValueError, TypeError):
            continue
    return result


def _parse_time(s: str) -> dt_time:
    parts = s.split(":")
    return dt_time(int(parts[0]), int(parts[1]))


def _format_single_rule(rule: dict) -> str:
    parts: list[str] = []

    tz = str(rule.get("timezone") or "").strip()
    if tz:
        parts.append(tz)

    work_hours = rule.get("work_hours")
    if work_hours and isinstance(work_hours, dict):
        s = str(work_hours.get("start") or "").strip()
        e = str(work_hours.get("end") or "").strip()
        if s and e:
            parts.append(f"{s}-{e}")

    day_names = {1: "Mon", 2: "Tue", 3: "Wed", 4: "Thu", 5: "Fri", 6: "Sat", 7: "Sun"}
    work_days = rule.get("work_days")
    if work_days is not None:
        names = [day_names.get(int(d), "?") for d in work_days]
        if names == ["Mon", "Tue", "Wed", "Thu", "Fri"]:
            parts.append("Mon-Fri")
        else:
            parts.append(",".join(names))

    holidays = rule.get("holidays")
    if holidays and isinstance(holidays, list):
        parts.append(f"{len(holidays)}holidays")

    extra = rule.get("extra_workdays")
    if extra and isinstance(extra, list):
        parts.append(f"{len(extra)}extra")

    when_expr = str(rule.get("when") or "").strip()
    if when_expr:
        parts.append(f"when:{when_expr}")

    return " ".join(parts)
