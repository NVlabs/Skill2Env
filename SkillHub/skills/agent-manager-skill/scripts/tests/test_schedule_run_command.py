from __future__ import annotations
import argparse
import io
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from commands.schedule_run import (  # noqa: E402
    _build_task_message_for_provider,
    _decide_runtime_action,
    _resolve_schedule_task_path,
    cmd_schedule_run,
)


class ScheduleRunCommandTests(unittest.TestCase):
    def _run(self, deps, args=None):
        args = args or argparse.Namespace(agent='dev', job='daily', timeout=None)
        out = io.StringIO()
        with redirect_stdout(out):
            code = cmd_schedule_run(args, deps=deps, start_handler=lambda _args: 0)
        return code, out.getvalue()

    def test_schedule_run_fails_when_tmux_missing(self):
        deps = SimpleNamespace(check_tmux=lambda: False)
        code, text = self._run(deps)

        self.assertEqual(code, 1)
        self.assertIn('tmux is not installed', text)

    def test_schedule_run_fails_when_schedule_missing(self):
        deps = SimpleNamespace(
            check_tmux=lambda: True,
            get_agent_schedule=lambda _agent, _job: None,
        )
        code, text = self._run(deps)

        self.assertEqual(code, 1)
        self.assertIn("Schedule 'daily' not found", text)

    def test_schedule_run_skips_disabled_agent(self):
        deps = SimpleNamespace(
            check_tmux=lambda: True,
            get_agent_schedule=lambda _agent, _job: {
                '_agent_config': {
                    'name': 'dev',
                    'enabled': False,
                    'file_id': 'EMP_0001',
                    '_file_path': 'agents/EMP_0001.md',
                },
                'enabled': True,
            },
            get_agent_id=lambda _cfg: 'emp-0001',
        )
        code, text = self._run(deps)

        self.assertEqual(code, 0)
        self.assertIn("Agent 'dev' is disabled", text)
        self.assertIn('agents/EMP_0001.md', text)

    def test_schedule_run_skips_disabled_schedule(self):
        deps = SimpleNamespace(
            check_tmux=lambda: True,
            get_agent_schedule=lambda _agent, _job: {
                '_agent_config': {
                    'name': 'dev',
                    'enabled': True,
                    'file_id': 'EMP_0001',
                },
                'enabled': False,
            },
            get_agent_id=lambda _cfg: 'emp-0001',
        )
        code, text = self._run(deps)

        self.assertEqual(code, 0)
        self.assertIn("Schedule 'daily' is disabled", text)


class ScheduleRunFlowHelperTests(unittest.TestCase):
    def test_decide_runtime_action_blocked(self):
        action, reason = _decide_runtime_action(state='blocked', elapsed=None, timeout_seconds=None, reason='')
        self.assertEqual(action, 'skip')
        self.assertEqual(reason, 'blocked')

    def test_decide_runtime_action_error(self):
        action, reason = _decide_runtime_action(state='error', elapsed=None, timeout_seconds=None, reason='timeout')
        self.assertEqual(action, 'restart')
        self.assertEqual(reason, 'error:timeout')

    def test_decide_runtime_action_stuck_restart_threshold(self):
        action, reason = _decide_runtime_action(state='stuck', elapsed=901, timeout_seconds=None, reason='')
        self.assertEqual(action, 'restart')
        self.assertEqual(reason, 'stuck>900s')

    def test_decide_runtime_action_stuck_below_threshold(self):
        action, reason = _decide_runtime_action(state='stuck', elapsed=120, timeout_seconds=300, reason='')
        self.assertEqual(action, 'skip')
        self.assertEqual(reason, 'stuck_below_threshold')

    def test_decide_runtime_action_busy_with_timeout_restart(self):
        action, reason = _decide_runtime_action(state='busy', elapsed=500, timeout_seconds=300, reason='')
        self.assertEqual(action, 'restart')
        self.assertEqual(reason, 'busy>300s')

    def test_decide_runtime_action_busy_without_timeout_skips(self):
        action, reason = _decide_runtime_action(state='busy', elapsed=500, timeout_seconds=None, reason='')
        self.assertEqual(action, 'skip')
        self.assertEqual(reason, 'busy')

    def test_resolve_schedule_task_path_returns_none_for_inline_task(self):
        schedule = {'task': 'inline task', 'task_file': 'agents/task.md'}
        path = _resolve_schedule_task_path(schedule, Path('/tmp'), expand_env_vars=lambda value: value)
        self.assertIsNone(path)

    def test_resolve_schedule_task_path_resolves_existing_relative_file(self):
        temp_root = Path(tempfile.mkdtemp(prefix='agent-manager-schedule-run-'))
        try:
            task_file = temp_root / 'agents' / 'task.md'
            task_file.parent.mkdir(parents=True, exist_ok=True)
            task_file.write_text('hello', encoding='utf-8')

            schedule = {'task': '', 'task_file': 'agents/task.md'}
            path = _resolve_schedule_task_path(schedule, temp_root, expand_env_vars=lambda value: value)
            self.assertEqual(path, task_file)
        finally:
            shutil.rmtree(temp_root, ignore_errors=True)

    def test_build_task_message_non_codex_keeps_original_task(self):
        task_message = _build_task_message_for_provider(
            provider_key='droid',
            task='run task',
            schedule_task_path=None,
            repo_root=Path('/tmp'),
            agent_id='emp-0001',
            job_name='daily',
            deps=SimpleNamespace(
                _should_use_codex_file_pointer=lambda _task: False,
                write_scheduled_task_file=lambda *_args: Path('/tmp/not-used.md'),
            ),
        )
        self.assertEqual(task_message, 'run task')

    def test_build_task_message_codex_prefers_schedule_task_path(self):
        task_path = Path('/tmp/agents/daily.md')
        task_message = _build_task_message_for_provider(
            provider_key='codex',
            task='run task',
            schedule_task_path=task_path,
            repo_root=Path('/tmp'),
            agent_id='emp-0001',
            job_name='daily',
            deps=SimpleNamespace(
                _should_use_codex_file_pointer=lambda _task: True,
                write_scheduled_task_file=lambda *_args: Path('/tmp/generated.md'),
            ),
        )
        self.assertIn("Run scheduled job 'daily'", task_message)
        self.assertIn(str(task_path), task_message)

    def test_schedule_run_restart_does_not_arm_fullspeed_skip(self):
        send_calls = []
        runtime_states = iter([
            {'state': 'error', 'elapsed_seconds': 0, 'reason': 'timeout'},
            {'state': 'idle', 'elapsed_seconds': 0, 'reason': ''},
            {'state': 'busy', 'elapsed_seconds': 1, 'reason': ''},
            {'state': 'idle', 'elapsed_seconds': 2, 'reason': ''},
        ])
        deps = SimpleNamespace(
            check_tmux=lambda: True,
            get_agent_schedule=lambda _agent, _job: {
                '_agent_config': {
                    'name': 'dev',
                    'enabled': True,
                    'file_id': 'EMP_0001',
                    'launcher': 'codex',
                },
                'enabled': True,
                'max_runtime': '1s',
                'task': 'run task',
            },
            get_agent_id=lambda _cfg: 'emp-0001',
            get_repo_root=lambda: Path('/tmp'),
            cleanup_old_logs=lambda _repo_root, days=7: 0,
            get_schedule_task=lambda _schedule, _repo_root: 'run task',
            expand_env_vars=lambda value: value,
            parse_duration=lambda _value: 1,
            session_exists=lambda _agent_id: True,
            resolve_launcher_command=lambda _launcher: 'codex',
            get_agent_runtime_state=lambda _agent_id, launcher='codex': next(runtime_states),
            stop_session=lambda _agent_id: True,
            get_provider_key=lambda _launcher: 'codex',
            send_keys=lambda *args, **kwargs: send_calls.append((args, kwargs)) or True,
            capture_output=lambda _agent_id, lines=200: 'done',
            arm_codex_fullspeed_stop_hook_skip=lambda *_args, **_kwargs: (_ for _ in ()).throw(
                AssertionError('arm_codex_fullspeed_stop_hook_skip should not be called for forced restart')
            ),
            _should_use_codex_file_pointer=lambda _task: False,
            write_scheduled_task_file=lambda *_args: Path('/tmp/generated.md'),
        )

        out = io.StringIO()
        with redirect_stdout(out):
            with unittest.mock.patch('commands.schedule_run.time.sleep', return_value=None):
                code = cmd_schedule_run(
                    argparse.Namespace(agent='dev', job='daily', timeout='1s'),
                    deps=deps,
                    start_handler=lambda _args: 0,
                )

        self.assertEqual(code, 0)
        self.assertEqual(len(send_calls), 1)


if __name__ == '__main__':
    unittest.main()
