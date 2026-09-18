"""Tests for services.work_schedule module."""

from __future__ import annotations

import os
import sys
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from services.work_schedule import is_within_work_schedule, format_schedule_summary  # noqa: E402

CST = ZoneInfo("Asia/Shanghai")
UTC = ZoneInfo("UTC")


# ---------------------------------------------------------------------------
# is_within_work_schedule
# ---------------------------------------------------------------------------

class TestNoSchedule(unittest.TestCase):
    """No schedule configured → always active."""

    def test_none(self):
        self.assertEqual(is_within_work_schedule(None), (True, ""))

    def test_empty_dict(self):
        self.assertEqual(is_within_work_schedule({}), (True, ""))

    def test_empty_list(self):
        self.assertEqual(is_within_work_schedule([]), (True, ""))

    def test_non_dict_non_list(self):
        self.assertEqual(is_within_work_schedule("bogus"), (True, ""))


class TestWorkHours(unittest.TestCase):
    SCHED = {"timezone": "Asia/Shanghai", "work_hours": {"start": "09:00", "end": "18:00"}}

    def test_within(self):
        now = datetime(2026, 2, 25, 10, 30, tzinfo=CST)  # Wed 10:30
        active, _ = is_within_work_schedule(self.SCHED, now=now)
        self.assertTrue(active)

    def test_before(self):
        now = datetime(2026, 2, 25, 8, 59, tzinfo=CST)
        active, reason = is_within_work_schedule(self.SCHED, now=now)
        self.assertFalse(active)
        self.assertIn("outside_hours", reason)

    def test_at_start_inclusive(self):
        now = datetime(2026, 2, 25, 9, 0, tzinfo=CST)
        active, _ = is_within_work_schedule(self.SCHED, now=now)
        self.assertTrue(active)

    def test_at_end_exclusive(self):
        now = datetime(2026, 2, 25, 18, 0, tzinfo=CST)
        active, reason = is_within_work_schedule(self.SCHED, now=now)
        self.assertFalse(active)
        self.assertIn("outside_hours", reason)

    def test_after(self):
        now = datetime(2026, 2, 25, 22, 0, tzinfo=CST)
        active, reason = is_within_work_schedule(self.SCHED, now=now)
        self.assertFalse(active)
        self.assertIn("outside_hours", reason)


class TestOvernightWorkHours(unittest.TestCase):
    """Overnight range: start > end, e.g. 21:00-09:00."""
    SCHED = {"timezone": "Asia/Shanghai", "work_hours": {"start": "21:00", "end": "09:00"}, "work_days": [1,2,3,4,5,6,7]}

    def test_late_night_active(self):
        now = datetime(2026, 2, 25, 23, 0, tzinfo=CST)
        active, _ = is_within_work_schedule(self.SCHED, now=now)
        self.assertTrue(active)

    def test_early_morning_active(self):
        now = datetime(2026, 2, 26, 2, 0, tzinfo=CST)
        active, _ = is_within_work_schedule(self.SCHED, now=now)
        self.assertTrue(active)

    def test_at_start_inclusive(self):
        now = datetime(2026, 2, 25, 21, 0, tzinfo=CST)
        active, _ = is_within_work_schedule(self.SCHED, now=now)
        self.assertTrue(active)

    def test_at_end_exclusive(self):
        now = datetime(2026, 2, 26, 9, 0, tzinfo=CST)
        active, reason = is_within_work_schedule(self.SCHED, now=now)
        self.assertFalse(active)
        self.assertIn("outside_hours", reason)

    def test_daytime_inactive(self):
        now = datetime(2026, 2, 26, 14, 0, tzinfo=CST)
        active, reason = is_within_work_schedule(self.SCHED, now=now)
        self.assertFalse(active)
        self.assertIn("outside_hours", reason)


class TestWorkDays(unittest.TestCase):
    SCHED = {"timezone": "Asia/Shanghai", "work_days": [1, 2, 3, 4, 5]}

    def test_weekday_active(self):
        now = datetime(2026, 2, 25, 12, 0, tzinfo=CST)  # Wednesday
        active, _ = is_within_work_schedule(self.SCHED, now=now)
        self.assertTrue(active)

    def test_weekend_inactive(self):
        now = datetime(2026, 2, 28, 12, 0, tzinfo=CST)  # Saturday
        active, reason = is_within_work_schedule(self.SCHED, now=now)
        self.assertFalse(active)
        self.assertIn("non_workday", reason)
        self.assertIn("Sat", reason)

    def test_default_work_days_mon_fri(self):
        sched = {"timezone": "Asia/Shanghai"}  # no work_days specified
        now = datetime(2026, 3, 1, 12, 0, tzinfo=CST)  # Sunday
        active, reason = is_within_work_schedule(sched, now=now)
        self.assertFalse(active)
        self.assertIn("non_workday", reason)

    def test_custom_work_days(self):
        sched = {"timezone": "Asia/Shanghai", "work_days": [6, 7]}
        now = datetime(2026, 2, 28, 12, 0, tzinfo=CST)  # Saturday
        active, _ = is_within_work_schedule(sched, now=now)
        self.assertTrue(active)


class TestHolidays(unittest.TestCase):
    SCHED = {"timezone": "Asia/Shanghai", "holidays": ["2026-01-01", "2026-01-28"]}

    def test_holiday_skips(self):
        now = datetime(2026, 1, 1, 12, 0, tzinfo=CST)  # Thursday
        active, reason = is_within_work_schedule(self.SCHED, now=now)
        self.assertFalse(active)
        self.assertIn("holiday", reason)
        self.assertIn("2026-01-01", reason)

    def test_non_holiday_passes(self):
        now = datetime(2026, 1, 2, 12, 0, tzinfo=CST)  # Friday
        active, _ = is_within_work_schedule(self.SCHED, now=now)
        self.assertTrue(active)


class TestExtraWorkdays(unittest.TestCase):
    def test_overrides_weekend(self):
        sched = {
            "timezone": "Asia/Shanghai",
            "work_days": [1, 2, 3, 4, 5],
            "extra_workdays": ["2026-02-28"],  # Saturday
        }
        now = datetime(2026, 2, 28, 12, 0, tzinfo=CST)
        active, _ = is_within_work_schedule(sched, now=now)
        self.assertTrue(active)

    def test_overrides_holiday(self):
        sched = {
            "timezone": "Asia/Shanghai",
            "holidays": ["2026-01-25"],
            "extra_workdays": ["2026-01-25"],
        }
        now = datetime(2026, 1, 25, 12, 0, tzinfo=CST)
        active, _ = is_within_work_schedule(sched, now=now)
        self.assertTrue(active)

    def test_still_respects_hours(self):
        sched = {
            "timezone": "Asia/Shanghai",
            "work_hours": {"start": "09:00", "end": "18:00"},
            "extra_workdays": ["2026-02-28"],
        }
        now = datetime(2026, 2, 28, 7, 0, tzinfo=CST)  # Saturday 07:00
        active, reason = is_within_work_schedule(sched, now=now)
        self.assertFalse(active)
        self.assertIn("outside_hours", reason)


class TestTimezoneConversion(unittest.TestCase):
    SCHED = {
        "timezone": "Asia/Shanghai",
        "work_hours": {"start": "09:00", "end": "18:00"},
    }

    def test_utc_to_shanghai_active(self):
        # 01:00 UTC = 09:00 CST → active
        now = datetime(2026, 2, 25, 1, 0, tzinfo=UTC)
        active, _ = is_within_work_schedule(self.SCHED, now=now)
        self.assertTrue(active)

    def test_utc_to_shanghai_inactive(self):
        # 00:00 UTC = 08:00 CST → before work hours
        now = datetime(2026, 2, 25, 0, 0, tzinfo=UTC)
        active, reason = is_within_work_schedule(self.SCHED, now=now)
        self.assertFalse(active)
        self.assertIn("outside_hours", reason)

    def test_invalid_timezone_fails_open(self):
        sched = {"timezone": "Invalid/Nowhere", "work_hours": {"start": "09:00", "end": "18:00"}}
        active, _ = is_within_work_schedule(sched)
        self.assertTrue(active)


# ---------------------------------------------------------------------------
# when conditions
# ---------------------------------------------------------------------------

class TestWhenExpression(unittest.TestCase):
    def test_eq_match(self):
        sched = [{"when": "$MYHOST == worker1", "timezone": "Asia/Shanghai"}]
        env = {"MYHOST": "worker1"}
        now = datetime(2026, 2, 25, 12, 0, tzinfo=CST)
        active, _ = is_within_work_schedule(sched, now=now, env=env)
        self.assertTrue(active)

    def test_eq_no_match(self):
        sched = [{"when": "$MYHOST == worker1", "timezone": "Asia/Shanghai"}]
        env = {"MYHOST": "worker2"}
        now = datetime(2026, 2, 25, 12, 0, tzinfo=CST)
        active, reason = is_within_work_schedule(sched, now=now, env=env)
        self.assertFalse(active)
        self.assertEqual(reason, "no_matching_rule")

    def test_neq(self):
        sched = [{"when": "$MYHOST != worker1", "timezone": "Asia/Shanghai"}]
        env = {"MYHOST": "worker2"}
        now = datetime(2026, 2, 25, 12, 0, tzinfo=CST)
        active, _ = is_within_work_schedule(sched, now=now, env=env)
        self.assertTrue(active)

    def test_truthy_set(self):
        sched = [{"when": "$ACTIVE", "timezone": "Asia/Shanghai"}]
        env = {"ACTIVE": "yes"}
        now = datetime(2026, 2, 25, 12, 0, tzinfo=CST)
        active, _ = is_within_work_schedule(sched, now=now, env=env)
        self.assertTrue(active)

    def test_truthy_unset(self):
        sched = [{"when": "$ACTIVE", "timezone": "Asia/Shanghai"}]
        env = {}
        now = datetime(2026, 2, 25, 12, 0, tzinfo=CST)
        active, reason = is_within_work_schedule(sched, now=now, env=env)
        self.assertFalse(active)
        self.assertEqual(reason, "no_matching_rule")

    def test_truthy_empty(self):
        sched = [{"when": "$ACTIVE", "timezone": "Asia/Shanghai"}]
        env = {"ACTIVE": ""}
        now = datetime(2026, 2, 25, 12, 0, tzinfo=CST)
        active, reason = is_within_work_schedule(sched, now=now, env=env)
        self.assertFalse(active)

    def test_missing_env_var_treated_as_empty(self):
        sched = [{"when": "$NOPE == hello", "timezone": "Asia/Shanghai"}]
        env = {}
        now = datetime(2026, 2, 25, 12, 0, tzinfo=CST)
        active, reason = is_within_work_schedule(sched, now=now, env=env)
        self.assertFalse(active)

    def test_cmd_eq_match(self):
        sched = [{"when": "$(hostname) == worker001", "timezone": "Asia/Shanghai"}]
        now = datetime(2026, 2, 25, 12, 0, tzinfo=CST)
        import subprocess
        actual_hostname = subprocess.run("hostname", capture_output=True, text=True).stdout.strip()
        expected_active = actual_hostname == "worker001"
        active, _ = is_within_work_schedule(sched, now=now, env={})
        self.assertEqual(active, expected_active)

    def test_cmd_eq_no_match(self):
        sched = [{"when": "$(echo nope) == yes", "timezone": "Asia/Shanghai"}]
        now = datetime(2026, 2, 25, 12, 0, tzinfo=CST)
        active, reason = is_within_work_schedule(sched, now=now, env={})
        self.assertFalse(active)
        self.assertEqual(reason, "no_matching_rule")

    def test_cmd_neq(self):
        sched = [{"when": "$(echo hello) != world", "timezone": "Asia/Shanghai"}]
        now = datetime(2026, 2, 25, 12, 0, tzinfo=CST)
        active, _ = is_within_work_schedule(sched, now=now, env={})
        self.assertTrue(active)

    def test_cmd_truthy(self):
        sched = [{"when": "$(echo yes)", "timezone": "Asia/Shanghai"}]
        now = datetime(2026, 2, 25, 12, 0, tzinfo=CST)
        active, _ = is_within_work_schedule(sched, now=now, env={})
        self.assertTrue(active)

    def test_cmd_truthy_empty(self):
        sched = [{"when": "$(echo)", "timezone": "Asia/Shanghai"}]
        now = datetime(2026, 2, 25, 12, 0, tzinfo=CST)
        active, reason = is_within_work_schedule(sched, now=now, env={})
        self.assertFalse(active)
        self.assertEqual(reason, "no_matching_rule")


class TestMultipleRules(unittest.TestCase):
    def test_first_matching_rule_wins(self):
        sched = [
            {
                "name": "worker1-day",
                "when": "$HOST == w1",
                "timezone": "Asia/Shanghai",
                "work_hours": {"start": "09:00", "end": "18:00"},
            },
            {
                "name": "worker2-night",
                "when": "$HOST == w2",
                "timezone": "Asia/Shanghai",
                "work_hours": {"start": "18:00", "end": "23:59"},
            },
        ]
        env = {"HOST": "w2"}
        # 20:00 CST → within worker2's hours
        now = datetime(2026, 2, 25, 20, 0, tzinfo=CST)
        active, _ = is_within_work_schedule(sched, now=now, env=env)
        self.assertTrue(active)

    def test_first_match_can_reject(self):
        sched = [
            {
                "name": "worker1-day",
                "when": "$HOST == w1",
                "timezone": "Asia/Shanghai",
                "work_hours": {"start": "09:00", "end": "18:00"},
            },
            {
                "name": "worker2-night",
                "when": "$HOST == w2",
                "timezone": "Asia/Shanghai",
                "work_hours": {"start": "18:00", "end": "23:59"},
            },
        ]
        env = {"HOST": "w1"}
        # 20:00 CST → outside worker1's hours
        now = datetime(2026, 2, 25, 20, 0, tzinfo=CST)
        active, reason = is_within_work_schedule(sched, now=now, env=env)
        self.assertFalse(active)
        self.assertIn("outside_hours", reason)

    def test_no_when_always_matches(self):
        sched = [
            {"timezone": "Asia/Shanghai", "work_hours": {"start": "09:00", "end": "18:00"}},
        ]
        now = datetime(2026, 2, 25, 12, 0, tzinfo=CST)
        active, _ = is_within_work_schedule(sched, now=now, env={})
        self.assertTrue(active)

    def test_all_when_miss_returns_no_matching_rule(self):
        sched = [
            {"when": "$HOST == w1", "timezone": "Asia/Shanghai"},
            {"when": "$HOST == w2", "timezone": "Asia/Shanghai"},
        ]
        env = {"HOST": "w3"}
        now = datetime(2026, 2, 25, 12, 0, tzinfo=CST)
        active, reason = is_within_work_schedule(sched, now=now, env=env)
        self.assertFalse(active)
        self.assertEqual(reason, "no_matching_rule")


class TestDictBackwardsCompat(unittest.TestCase):
    """Single dict schedule (not a list) should work like before."""

    def test_dict_treated_as_single_rule(self):
        sched = {
            "timezone": "Asia/Shanghai",
            "work_hours": {"start": "09:00", "end": "18:00"},
            "work_days": [1, 2, 3, 4, 5],
        }
        now = datetime(2026, 2, 25, 12, 0, tzinfo=CST)  # Wednesday
        active, _ = is_within_work_schedule(sched, now=now)
        self.assertTrue(active)


class TestCombined(unittest.TestCase):
    def test_full_schedule(self):
        sched = {
            "timezone": "Asia/Shanghai",
            "work_hours": {"start": "09:00", "end": "18:00"},
            "work_days": [1, 2, 3, 4, 5],
            "holidays": ["2026-01-01"],
            "extra_workdays": ["2026-01-25"],
        }
        now = datetime(2026, 2, 25, 14, 0, tzinfo=CST)
        active, reason = is_within_work_schedule(sched, now=now)
        self.assertTrue(active)
        self.assertEqual(reason, "")


# ---------------------------------------------------------------------------
# format_schedule_summary
# ---------------------------------------------------------------------------

class TestFormatScheduleSummary(unittest.TestCase):
    def test_full_single_rule(self):
        sched = {
            "timezone": "Asia/Shanghai",
            "work_hours": {"start": "09:00", "end": "18:00"},
            "work_days": [1, 2, 3, 4, 5],
            "holidays": ["2026-01-01", "2026-01-28"],
            "extra_workdays": ["2026-01-25"],
        }
        s = format_schedule_summary(sched)
        self.assertIn("Asia/Shanghai", s)
        self.assertIn("09:00-18:00", s)
        self.assertIn("Mon-Fri", s)
        self.assertIn("2holidays", s)
        self.assertIn("1extra", s)

    def test_empty(self):
        self.assertEqual(format_schedule_summary(None), "")
        self.assertEqual(format_schedule_summary({}), "")

    def test_custom_work_days(self):
        sched = {"timezone": "UTC", "work_days": [1, 3, 5]}
        s = format_schedule_summary(sched)
        self.assertIn("Mon,Wed,Fri", s)

    def test_multi_rule_summary(self):
        sched = [
            {"when": "$HOST == w1", "timezone": "Asia/Shanghai"},
            {"when": "$HOST == w2", "timezone": "Asia/Shanghai"},
        ]
        s = format_schedule_summary(sched)
        self.assertIn("2rules", s)
        self.assertIn("when:conditional", s)

    def test_multi_rule_no_when(self):
        sched = [
            {"timezone": "Asia/Shanghai"},
            {"timezone": "UTC"},
        ]
        s = format_schedule_summary(sched)
        self.assertIn("2rules", s)
        self.assertNotIn("when", s)


if __name__ == "__main__":
    unittest.main()
