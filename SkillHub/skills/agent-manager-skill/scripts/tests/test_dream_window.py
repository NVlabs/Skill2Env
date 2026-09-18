from __future__ import annotations

import sys
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from services.dream_window import normalize_dream_fixed_windows, resolve_active_dream_window  # noqa: E402


CST = ZoneInfo("Asia/Shanghai")


class DreamWindowTests(unittest.TestCase):
    def test_overnight_fixed_window_is_active_after_midnight(self):
        dream = {
            "fixed_windows": [
                {"timezone": "Asia/Shanghai", "start": "23:00", "end": "08:00"},
            ],
        }

        result = resolve_active_dream_window(
            dream,
            now=datetime(2026, 5, 6, 2, 0, tzinfo=CST),
        )

        self.assertTrue(result["active"])
        self.assertEqual(result["window_id"], "fixed-window-1")

    def test_fixed_windows_default_to_every_day(self):
        windows = normalize_dream_fixed_windows({
            "fixed_windows": [{"start": "23:00", "end": "08:00"}],
        })

        self.assertEqual(windows[0]["work_days"], [1, 2, 3, 4, 5, 6, 7])

    def test_multiple_windows_are_or_rules(self):
        dream = {
            "fixed_windows": [
                {"timezone": "Asia/Shanghai", "start": "23:00", "end": "23:30"},
                {"timezone": "Asia/Shanghai", "start": "02:00", "end": "03:00"},
            ],
        }

        result = resolve_active_dream_window(
            dream,
            now=datetime(2026, 5, 6, 2, 15, tzinfo=CST),
        )

        self.assertTrue(result["active"])
        self.assertEqual(result["window_id"], "fixed-window-2")

    def test_string_window_shorthand(self):
        windows = normalize_dream_fixed_windows({
            "timezone": "Asia/Shanghai",
            "fixed_windows": ["23:00-08:00"],
        })

        self.assertEqual(windows[0]["timezone"], "Asia/Shanghai")
        self.assertEqual(windows[0]["work_hours"], {"start": "23:00", "end": "08:00"})


if __name__ == '__main__':
    unittest.main()
