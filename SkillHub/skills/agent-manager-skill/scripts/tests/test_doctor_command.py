from __future__ import annotations
import argparse
import io
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from commands.doctor import cmd_doctor  # noqa: E402


class _SubprocessOk:
    @staticmethod
    def run(*args, **kwargs):
        class _Result:
            returncode = 0

        return _Result()


class _SubprocessMissing:
    @staticmethod
    def run(*args, **kwargs):
        raise FileNotFoundError


class DoctorCommandTests(unittest.TestCase):
    def setUp(self):
        self.temp_root = Path(tempfile.mkdtemp(prefix='agent-manager-doctor-'))

    def tearDown(self):
        shutil.rmtree(self.temp_root, ignore_errors=True)

    def test_doctor_happy_path(self):
        (self.temp_root / 'agents').mkdir(parents=True, exist_ok=True)
        (self.temp_root / '.agent' / 'skills').mkdir(parents=True, exist_ok=True)
        (self.temp_root / '.claude').mkdir(parents=True, exist_ok=True)

        class Deps:
            sys = sys
            subprocess = _SubprocessOk
            Path = Path

            @staticmethod
            def get_repo_root():
                return self.temp_root

            @staticmethod
            def check_tmux():
                return True

            @staticmethod
            def list_all_agents(_agents_dir=None):
                return {'EMP_0001': {'file_id': 'EMP_0001', 'enabled': True}}

            @staticmethod
            def get_agent_id(config):
                return config.get('file_id', '').lower().replace('_', '-')

            @staticmethod
            def resolve_launcher_command(_launcher):
                return 'codex'

            @staticmethod
            def _tmux_install_hint():
                return 'install tmux'

        out = io.StringIO()
        with redirect_stdout(out):
            code = cmd_doctor(argparse.Namespace(deep=False), deps=Deps)

        text = out.getvalue()
        self.assertEqual(code, 0)
        self.assertIn('✅ Doctor checks passed', text)

    def test_doctor_reports_missing_tmux_and_crontab(self):
        class Deps:
            sys = sys
            subprocess = _SubprocessMissing
            Path = Path

            @staticmethod
            def get_repo_root():
                return self.temp_root

            @staticmethod
            def check_tmux():
                return False

            @staticmethod
            def list_all_agents(_agents_dir=None):
                return {}

            @staticmethod
            def get_agent_id(config):
                return config.get('file_id', '').lower().replace('_', '-')

            @staticmethod
            def resolve_launcher_command(_launcher):
                return ''

            @staticmethod
            def _tmux_install_hint():
                return 'install tmux'

        out = io.StringIO()
        with redirect_stdout(out):
            code = cmd_doctor(argparse.Namespace(deep=False), deps=Deps)

        text = out.getvalue()
        self.assertEqual(code, 1)
        self.assertIn('❌ tmux: missing', text)
        self.assertIn('❌ crontab: command not found', text)


if __name__ == '__main__':
    unittest.main()
