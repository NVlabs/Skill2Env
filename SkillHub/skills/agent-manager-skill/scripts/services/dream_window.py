"""Fixed Dream window helpers.

These helpers intentionally reuse the heartbeat work-schedule rule shape for
timezone/day/holiday handling, but fixed Dream windows are OR-ed time windows:
if any configured window is active, the heartbeat should dispatch a Dream task.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from .work_schedule import format_schedule_summary, is_within_work_schedule


_ALL_DAYS = [1, 2, 3, 4, 5, 6, 7]
_WINDOW_KEYS = (
    "fixed_windows",
    "fixed_window",
    "windows",
    "window",
    "periods",
    "period",
)


def normalize_dream_fixed_windows(dream_config: object) -> list[dict[str, Any]]:
    """Normalize ``heartbeat.dream`` fixed window config into schedule rules.

    Preferred shape::

        dream:
          enabled: true
          fixed_windows:
            - timezone: Asia/Shanghai
              start: "23:00"
              end: "08:00"

    ``work_hours: {start, end}`` is also accepted. Unlike generic work
    schedules, fixed Dream windows default to all seven days because sleep /
    maintenance windows are usually daily unless explicitly constrained.
    """
    if not isinstance(dream_config, dict):
        return []

    raw_windows: list[Any] = []
    for key in _WINDOW_KEYS:
        value = dream_config.get(key)
        if value is None:
            continue
        if isinstance(value, list):
            raw_windows.extend(value)
        else:
            raw_windows.append(value)

    default_timezone = str(dream_config.get("timezone") or "").strip()
    windows: list[dict[str, Any]] = []
    for raw in raw_windows:
        rule = _coerce_window_rule(raw, default_timezone=default_timezone)
        if rule:
            windows.append(rule)
    return windows


def resolve_active_dream_window(
    dream_config: object,
    *,
    now: Optional[datetime] = None,
) -> dict[str, Any]:
    """Return the active fixed Dream window, if any."""
    windows = normalize_dream_fixed_windows(dream_config)
    if not windows:
        return {"active": False, "reason": "no_fixed_windows", "windows": []}

    last_reason = "outside_fixed_windows"
    for index, rule in enumerate(windows, start=1):
        active, reason = is_within_work_schedule(rule, now=now)
        if active:
            return {
                "active": True,
                "index": index,
                "rule": rule,
                "summary": format_schedule_summary(rule),
                "window_id": f"fixed-window-{index}",
                "windows": windows,
            }
        if reason:
            last_reason = reason

    return {"active": False, "reason": last_reason, "windows": windows}


def _coerce_window_rule(raw: Any, *, default_timezone: str = "") -> dict[str, Any]:
    if isinstance(raw, str):
        return _coerce_string_window(raw, default_timezone=default_timezone)
    if not isinstance(raw, dict):
        return {}

    rule = dict(raw)
    if default_timezone and not str(rule.get("timezone") or "").strip():
        rule["timezone"] = default_timezone

    if "work_hours" not in rule or not isinstance(rule.get("work_hours"), dict):
        start = str(rule.pop("start", rule.pop("from", "")) or "").strip()
        end = str(rule.pop("end", rule.pop("to", "")) or "").strip()
        if start and end:
            rule["work_hours"] = {"start": start, "end": end}

    if not _has_valid_work_hours(rule):
        return {}

    if "work_days" not in rule:
        days = rule.pop("days", rule.pop("weekdays", None))
        rule["work_days"] = _normalize_days(days) if days is not None else list(_ALL_DAYS)

    return rule


def _coerce_string_window(raw: str, *, default_timezone: str = "") -> dict[str, Any]:
    text = str(raw or "").strip()
    if not text:
        return {}

    timezone = default_timezone
    range_text = text
    parts = text.split()
    if len(parts) == 2:
        timezone, range_text = parts[0], parts[1]

    if "-" not in range_text:
        return {}
    start, end = [part.strip() for part in range_text.split("-", 1)]
    if not start or not end:
        return {}

    rule: dict[str, Any] = {
        "work_hours": {"start": start, "end": end},
        "work_days": list(_ALL_DAYS),
    }
    if timezone:
        rule["timezone"] = timezone
    return rule


def _has_valid_work_hours(rule: dict[str, Any]) -> bool:
    work_hours = rule.get("work_hours")
    if not isinstance(work_hours, dict):
        return False
    return bool(str(work_hours.get("start") or "").strip() and str(work_hours.get("end") or "").strip())


def _normalize_days(raw: Any) -> list[int]:
    if isinstance(raw, str):
        items = [part.strip() for part in raw.split(",")]
    elif isinstance(raw, list):
        items = raw
    else:
        return list(_ALL_DAYS)

    result: list[int] = []
    for item in items:
        try:
            day = int(item)
        except Exception:
            continue
        if 1 <= day <= 7 and day not in result:
            result.append(day)
    return result or list(_ALL_DAYS)
