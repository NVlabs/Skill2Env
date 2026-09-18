from __future__ import annotations
import argparse
import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from commands.listing import cmd_list  # noqa: E402


class _Deps:
    @staticmethod
    def list_all_agents():
        return {
            'EMP_0001': {
                'file_id': 'EMP_0001',
                'name': 'dev',
                'description': 'Dev agent',
                'working_directory': '/tmp/dev',
                'skills': ['review-pr'],
                'enabled': True,
            },
            'EMP_0002': {
                'file_id': 'EMP_0002',
                'name': 'qa',
                'description': 'QA agent',
                'working_directory': '/tmp/qa',
                'enabled': False,
            },
            'EMP_0003': {
                'file_id': 'EMP_0003',
                'name': 'ops',
                'description': 'Ops agent',
                'working_directory': '/tmp/ops',
                'enabled': True,
            },
        }

    @staticmethod
    def list_sessions():
        return ['emp-0001']

    @staticmethod
    def get_agent_id(config):
        return config.get('file_id', '').lower().replace('_', '-')

    @staticmethod
    def get_session_info(agent_id):
        if agent_id == 'emp-0001':
            return {'session': 'agent-emp-0001'}
        return None




class _MainDeps:
    @staticmethod
    def list_all_agents():
        return {
            'main': {
                'file_id': 'main',
                'name': 'main',
                'description': 'Reserved main agent',
                'working_directory': '/tmp/workspace',
                'enabled': True,
            },
        }

    @staticmethod
    def list_sessions():
        return ['main']

    @staticmethod
    def get_agent_id(config):
        return config.get('file_id', '').lower().replace('_', '-')

    @staticmethod
    def get_session_info(agent_id):
        if agent_id == 'main':
            return {'session': 'main'}
        return None


class ListCommandTests(unittest.TestCase):
    def _run(self, running=False):
        out = io.StringIO()
        args = argparse.Namespace(running=running)
        with redirect_stdout(out):
            cmd_list(args, deps=_Deps)
        return out.getvalue()

    def test_list_shows_running_stopped_and_disabled(self):
        text = self._run(running=False)

        self.assertIn('📋 Agents:', text)
        self.assertIn('✅ Running agent-emp-0001(dev)', text)
        self.assertIn('⭕ Stopped agent-emp-0003(ops)', text)
        self.assertIn('⛔ Disabled agent-emp-0002(qa)', text)
        self.assertIn('Skills: review-pr', text)

    def test_list_running_filter_only_shows_running(self):
        text = self._run(running=True)

        self.assertIn('✅ Running agent-emp-0001(dev)', text)
        self.assertNotIn('⭕ Stopped agent-emp-0003(ops)', text)
        self.assertNotIn('⛔ Disabled agent-emp-0002(qa)', text)

    def test_list_supports_reserved_main_agent_session_name(self):
        out = io.StringIO()
        args = argparse.Namespace(running=False)
        with redirect_stdout(out):
            cmd_list(args, deps=_MainDeps)

        text = out.getvalue()
        self.assertIn('✅ Running main(main)', text)
        self.assertNotIn('agent-main', text)


if __name__ == '__main__':
    unittest.main()
