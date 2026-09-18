from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import schedule_helper  # noqa: E402


class ScheduleHelperTests(unittest.TestCase):
    @patch('schedule_helper.subprocess.run')
    def test_set_crontab_uses_stdin(self, mock_run):
        mock_run.return_value.returncode = 0

        result = schedule_helper.set_crontab('demo-cron')

        self.assertTrue(result)
        mock_run.assert_called_once_with(
            ['crontab', '-'],
            input='demo-cron',
            capture_output=True,
            text=True,
        )

    @patch('schedule_helper.subprocess.run')
    def test_set_crontab_returns_false_on_nonzero(self, mock_run):
        mock_run.return_value.returncode = 1

        result = schedule_helper.set_crontab('demo-cron')

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
