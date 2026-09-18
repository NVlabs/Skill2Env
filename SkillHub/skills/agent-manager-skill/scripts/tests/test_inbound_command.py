from __future__ import annotations

import argparse
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from commands.inbound import cmd_inbound  # noqa: E402


class InboundCommandTests(unittest.TestCase):
    def test_rescue_command_prints_cron_and_systemd_examples(self):
        temp_root = Path(tempfile.mkdtemp(prefix='agent-manager-inbound-rescue-'))
        deps = SimpleNamespace(
            __file__=str(temp_root / 'agent-manager' / 'scripts' / 'main.py'),
            Path=Path,
            get_repo_root=lambda: temp_root,
            resolve_agent=lambda _agent: {'name': 'main', 'file_id': 'main'},
            get_agent_id=lambda config: config.get('file_id', '').lower(),
        )

        output = io.StringIO()
        with redirect_stdout(output):
            rc = cmd_inbound(
                argparse.Namespace(inbound_command='rescue', agent='main'),
                deps=deps,
            )

        text = output.getvalue()
        self.assertEqual(rc, 0)
        self.assertIn('python3', text)
        self.assertIn('inbound drain main --once', text)
        self.assertIn('*/5 * * * *', text)
        self.assertIn('OnCalendar=*:0/5', text)
        self.assertIn('ExecStart=/usr/bin/env bash -lc', text)

    def test_rescue_command_rejects_non_main_agent(self):
        deps = SimpleNamespace(
            resolve_agent=lambda _agent: {'name': 'dev', 'file_id': 'EMP_0001'},
            get_agent_id=lambda config: config.get('file_id', '').lower(),
        )

        output = io.StringIO()
        with redirect_stdout(output):
            rc = cmd_inbound(
                argparse.Namespace(inbound_command='rescue', agent='dev'),
                deps=deps,
            )

        self.assertEqual(rc, 1)
        self.assertIn('currently supports only the main agent', output.getvalue())


if __name__ == '__main__':
    unittest.main()
