from __future__ import annotations
import argparse
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import agent_config  # noqa: E402
import main  # noqa: E402
import tmux_helper  # noqa: E402
from services.inbound_queue import enqueue_inbound_message  # noqa: E402
from services.inbound_queue import mark_inbound_message_state  # noqa: E402
from services.inbound_queue import load_pending_inbound_messages  # noqa: E402
from services.inbound_queue import note_pending_messages_yielded  # noqa: E402
from services.inbound_queue import read_inbound_events  # noqa: E402
from services.inbound_queue import was_message_yielded  # noqa: E402
from services.inbound_queue import append_inbound_message_event  # noqa: E402
from commands.lifecycle import cmd_assign, cmd_monitor, cmd_send  # noqa: E402


class MainAgentConfigTests(unittest.TestCase):
    def test_resolve_agent_main_returns_reserved_config(self):
        config = agent_config.resolve_agent('main', agents_dir=Path('/tmp/not-needed'))

        self.assertIsNotNone(config)
        self.assertEqual(config.get('name'), 'main')
        self.assertEqual(config.get('file_id'), 'main')
        self.assertTrue(bool(config.get('working_directory')))
        self.assertTrue(bool(config.get('launcher')))

    @patch('agent_config.get_repo_root')
    def test_resolve_agent_main_defaults_to_bundled_codex_model_file(self, mock_get_repo_root):
        temp_root = Path(tempfile.mkdtemp(prefix='agent-manager-main-default-model-'))
        mock_get_repo_root.return_value = temp_root

        config = agent_config.resolve_agent('main', agents_dir=temp_root / 'agents')

        launcher_config = config.get('launcher_config') or {}
        model_file = launcher_config.get('model_instructions_file', '')
        self.assertTrue(model_file.endswith('/agent-manager/.codex/main-codex-model.md'))
        self.assertTrue(Path(model_file).exists())

    def test_list_all_agents_includes_main_without_agents_dir(self):
        temp_root = Path(tempfile.mkdtemp(prefix='agent-manager-main-agent-'))
        agents_dir = temp_root / 'agents'

        agents = agent_config.list_all_agents(agents_dir=agents_dir)

        self.assertIn('main', agents)
        self.assertEqual(agents['main'].get('name'), 'main')

    @patch('agent_config.get_repo_root')
    @patch.dict(os.environ, {'AGENT_MANAGER_MAIN_LAUNCHER': 'custom-launcher'})
    def test_main_launcher_env_override(self, mock_get_repo_root):
        mock_get_repo_root.return_value = Path('/tmp/fake-repo')
        config = agent_config.resolve_agent('main', agents_dir=Path('/tmp/not-needed'))
        self.assertEqual(config.get('launcher'), 'custom-launcher')
        self.assertEqual(config.get('launcher_config'), {})


class MainAgentTmuxNamingTests(unittest.TestCase):
    def test_session_name_for_main_has_no_prefix(self):
        self.assertEqual(tmux_helper._session_name_for_agent('main'), 'main')
        self.assertEqual(tmux_helper._window_name_for_agent('main'), 'main')
        self.assertEqual(tmux_helper._session_name_for_agent('emp-0001'), 'agent-emp-0001')


class MainAgentLifecycleTests(unittest.TestCase):
    def test_send_main_routes_message_to_main_agent_id(self):
        calls = []
        temp_root = Path(tempfile.mkdtemp(prefix='agent-manager-main-send-queue-'))

        deps = SimpleNamespace(
            __file__='main.py',
            resolve_agent=lambda _agent: {'name': 'main', 'file_id': 'main', 'launcher': 'droid'},
            get_agent_id=lambda config: config.get('file_id', '').lower(),
            check_tmux=lambda: True,
            session_exists=lambda agent_id: agent_id == 'main',
            Path=Path,
            resolve_launcher_command=lambda launcher: launcher,
            _should_use_codex_file_pointer=lambda _msg: False,
            get_repo_root=lambda: temp_root,
            write_codex_message_file=lambda *_args, **_kwargs: Path('/tmp/message.md'),
            send_keys=lambda agent_id, message, **kwargs: calls.append((agent_id, message, kwargs)) or True,
            enqueue_inbound_message=enqueue_inbound_message,
            mark_inbound_message_state=mark_inbound_message_state,
            was_message_yielded=was_message_yielded,
            append_inbound_message_event=append_inbound_message_event,
        )

        output = io.StringIO()
        with redirect_stdout(output):
            rc = cmd_send(
                argparse.Namespace(agent='main', message='hello-main', send_enter=True),
                deps=deps,
            )

        self.assertEqual(rc, 0)
        self.assertEqual(calls[0][0], 'main')
        self.assertIn('Message sent to main', output.getvalue())
        self.assertEqual(load_pending_inbound_messages(temp_root, agent_id='main'), [])

    def test_assign_main_reads_stdin_and_sends(self):
        calls = []
        temp_root = Path(tempfile.mkdtemp(prefix='agent-manager-main-assign-queue-'))

        deps = SimpleNamespace(
            __file__='main.py',
            resolve_agent=lambda _agent: {'name': 'main', 'file_id': 'main', 'launcher': 'droid'},
            get_agent_id=lambda config: config.get('file_id', '').lower(),
            check_tmux=lambda: True,
            session_exists=lambda agent_id: agent_id == 'main',
            argparse=argparse,
            time=SimpleNamespace(sleep=lambda _s: None),
            resolve_launcher_command=lambda launcher: launcher,
            _should_use_codex_file_pointer=lambda _msg: False,
            get_repo_root=lambda: temp_root,
            write_codex_message_file=lambda *_args, **_kwargs: Path('/tmp/assign.md'),
            send_keys=lambda agent_id, message, **kwargs: calls.append((agent_id, message, kwargs)) or True,
            Path=Path,
            sys=SimpleNamespace(stdin=io.StringIO('run health check')),
            enqueue_inbound_message=enqueue_inbound_message,
            mark_inbound_message_state=mark_inbound_message_state,
            was_message_yielded=was_message_yielded,
            append_inbound_message_event=append_inbound_message_event,
        )

        output = io.StringIO()
        with redirect_stdout(output):
            rc = cmd_assign(
                argparse.Namespace(agent='main', task_file=None),
                deps=deps,
                start_handler=lambda _args: 0,
            )

        self.assertEqual(rc, 0)
        self.assertEqual(calls[0][0], 'main')
        self.assertIn('# Task Assignment', calls[0][1])
        self.assertIn('Task assigned to main', output.getvalue())
        self.assertEqual(load_pending_inbound_messages(temp_root, agent_id='main'), [])
        events = read_inbound_events(temp_root, agent_id='main')
        self.assertEqual([event.get('event') for event in events], ['received', 'queued', 'dispatching', 'dispatched', 'handled', 'replied'])
        self.assertEqual(events[-1].get('reply_evidence'), 'repo_local')
        self.assertEqual(events[-1].get('transport_ack_status'), 'unverified')

    def test_assign_main_marks_transport_ack_when_delivery_confirmed(self):
        calls = []
        temp_root = Path(tempfile.mkdtemp(prefix='agent-manager-main-assign-ack-queue-'))

        deps = SimpleNamespace(
            __file__='main.py',
            resolve_agent=lambda _agent: {'name': 'main', 'file_id': 'main', 'launcher': 'droid'},
            get_agent_id=lambda config: config.get('file_id', '').lower(),
            check_tmux=lambda: True,
            session_exists=lambda agent_id: agent_id == 'main',
            argparse=argparse,
            time=SimpleNamespace(sleep=lambda _s: None),
            resolve_launcher_command=lambda launcher: launcher,
            _should_use_codex_file_pointer=lambda _msg: False,
            get_repo_root=lambda: temp_root,
            write_codex_message_file=lambda *_args, **_kwargs: Path('/tmp/assign.md'),
            send_keys=lambda agent_id, message, **kwargs: calls.append((agent_id, message, kwargs)) or True,
            get_agent_runtime_state=lambda _agent_id, launcher='': {'state': 'busy', 'reason': 'busy_pattern:Thinking...'},
            Path=Path,
            sys=SimpleNamespace(stdin=io.StringIO('run health check')),
            enqueue_inbound_message=enqueue_inbound_message,
            mark_inbound_message_state=mark_inbound_message_state,
            was_message_yielded=was_message_yielded,
            append_inbound_message_event=append_inbound_message_event,
        )

        output = io.StringIO()
        with redirect_stdout(output):
            rc = cmd_assign(
                argparse.Namespace(agent='main', task_file=None),
                deps=deps,
                start_handler=lambda _args: 0,
            )

        self.assertEqual(rc, 0)
        self.assertEqual(calls[0][0], 'main')
        events = read_inbound_events(temp_root, agent_id='main')
        self.assertEqual([event.get('event') for event in events], ['received', 'queued', 'dispatching', 'dispatched', 'handled', 'replied'])
        self.assertEqual(events[-1].get('reply_evidence'), 'transport_ack')
        self.assertEqual(events[-1].get('transport_ack_status'), 'ack')
        self.assertEqual(events[-1].get('transport_ack_detail'), 'busy:busy_pattern:Thinking...')

    def test_monitor_main_shows_main_session_label(self):
        deps = SimpleNamespace(
            check_tmux=lambda: True,
            resolve_agent=lambda _agent: {'name': 'main', 'file_id': 'main'},
            get_agent_id=lambda config: config.get('file_id', '').lower(),
            capture_output=lambda _agent_id, _lines: 'line-1\nline-2\n',
            time=SimpleNamespace(sleep=lambda _s: None),
        )

        output = io.StringIO()
        with redirect_stdout(output):
            rc = cmd_monitor(
                argparse.Namespace(agent='main', follow=False, lines=20),
                deps=deps,
            )

        text = output.getvalue()
        self.assertEqual(rc, 0)
        self.assertIn('Last 20 lines from main(main)', text)
        self.assertNotIn('agent-main', text)

    def test_send_warns_when_runtime_not_idle_before_dispatch(self):
        calls = []
        temp_root = Path(tempfile.mkdtemp(prefix='agent-manager-main-busy-queue-'))

        deps = SimpleNamespace(
            __file__='main.py',
            resolve_agent=lambda _agent: {'name': 'main', 'file_id': 'main', 'launcher': 'droid'},
            get_agent_id=lambda config: config.get('file_id', '').lower(),
            check_tmux=lambda: True,
            session_exists=lambda agent_id: agent_id == 'main',
            Path=Path,
            resolve_launcher_command=lambda launcher: launcher,
            _should_use_codex_file_pointer=lambda _msg: False,
            get_repo_root=lambda: temp_root,
            write_codex_message_file=lambda *_args, **_kwargs: Path('/tmp/message.md'),
            send_keys=lambda agent_id, message, **kwargs: calls.append((agent_id, message, kwargs)) or True,
            get_agent_runtime_state=lambda _agent_id, launcher='': {'state': 'busy', 'reason': 'busy_pattern:Thinking...'},
            enqueue_inbound_message=enqueue_inbound_message,
            mark_inbound_message_state=mark_inbound_message_state,
            was_message_yielded=was_message_yielded,
            append_inbound_message_event=append_inbound_message_event,
        )

        output = io.StringIO()
        with redirect_stdout(output):
            rc = cmd_send(
                argparse.Namespace(agent='main', message='hello-main', send_enter=True),
                deps=deps,
            )

        text = output.getvalue()
        self.assertEqual(rc, 0)
        self.assertEqual(calls[0][0], 'main')
        self.assertIn("runtime is busy", text)
        self.assertIn("message may be delayed or ignored", text)
        self.assertEqual(load_pending_inbound_messages(temp_root, agent_id='main'), [])

    def test_send_warns_when_delivery_unconfirmed(self):
        calls = []
        temp_root = Path(tempfile.mkdtemp(prefix='agent-manager-main-unconfirmed-queue-'))

        class _FakeTime:
            def __init__(self):
                self._now = 0.0

            def time(self):
                return self._now

            def sleep(self, seconds):
                self._now += float(seconds)

        fake_time = _FakeTime()

        deps = SimpleNamespace(
            __file__='main.py',
            resolve_agent=lambda _agent: {'name': 'main', 'file_id': 'main', 'launcher': 'droid'},
            get_agent_id=lambda config: config.get('file_id', '').lower(),
            check_tmux=lambda: True,
            session_exists=lambda agent_id: agent_id == 'main',
            Path=Path,
            resolve_launcher_command=lambda launcher: launcher,
            _should_use_codex_file_pointer=lambda _msg: False,
            get_repo_root=lambda: temp_root,
            write_codex_message_file=lambda *_args, **_kwargs: Path('/tmp/message.md'),
            send_keys=lambda agent_id, message, **kwargs: calls.append((agent_id, message, kwargs)) or True,
            get_agent_runtime_state=lambda _agent_id, launcher='': {'state': 'idle', 'reason': 'ready'},
            time=fake_time,
            enqueue_inbound_message=enqueue_inbound_message,
            mark_inbound_message_state=mark_inbound_message_state,
            was_message_yielded=was_message_yielded,
            append_inbound_message_event=append_inbound_message_event,
        )

        output = io.StringIO()
        with redirect_stdout(output):
            rc = cmd_send(
                argparse.Namespace(agent='main', message='hello-main', send_enter=True),
                deps=deps,
            )

        text = output.getvalue()
        self.assertEqual(rc, 0)
        self.assertEqual(calls[0][0], 'main')
        self.assertIn("Delivery unconfirmed: agent remained idle after send", text)
        self.assertEqual(load_pending_inbound_messages(temp_root, agent_id='main'), [])

    def test_assign_warns_when_delivery_unconfirmed(self):
        calls = []
        temp_root = Path(tempfile.mkdtemp(prefix='agent-manager-main-assign-unconfirmed-queue-'))

        class _FakeTime:
            def __init__(self):
                self._now = 0.0

            def time(self):
                return self._now

            def sleep(self, seconds):
                self._now += float(seconds)

        fake_time = _FakeTime()

        deps = SimpleNamespace(
            __file__='main.py',
            resolve_agent=lambda _agent: {'name': 'main', 'file_id': 'main', 'launcher': 'droid'},
            get_agent_id=lambda config: config.get('file_id', '').lower(),
            check_tmux=lambda: True,
            session_exists=lambda agent_id: agent_id == 'main',
            argparse=argparse,
            time=fake_time,
            resolve_launcher_command=lambda launcher: launcher,
            _should_use_codex_file_pointer=lambda _msg: False,
            get_repo_root=lambda: temp_root,
            write_codex_message_file=lambda *_args, **_kwargs: Path('/tmp/assign.md'),
            send_keys=lambda agent_id, message, **kwargs: calls.append((agent_id, message, kwargs)) or True,
            get_agent_runtime_state=lambda _agent_id, launcher='': {'state': 'idle', 'reason': 'ready'},
            Path=Path,
            sys=SimpleNamespace(stdin=io.StringIO('run health check')),
            enqueue_inbound_message=enqueue_inbound_message,
            mark_inbound_message_state=mark_inbound_message_state,
            was_message_yielded=was_message_yielded,
            append_inbound_message_event=append_inbound_message_event,
        )

        output = io.StringIO()
        with redirect_stdout(output):
            rc = cmd_assign(
                argparse.Namespace(agent='main', task_file=None),
                deps=deps,
                start_handler=lambda _args: 0,
            )

        text = output.getvalue()
        self.assertEqual(rc, 0)
        self.assertEqual(calls[0][0], 'main')
        self.assertIn("Delivery unconfirmed: agent remained idle after assign", text)
        self.assertEqual(load_pending_inbound_messages(temp_root, agent_id='main'), [])

    def test_send_main_failure_keeps_message_pending_in_queue(self):
        temp_root = Path(tempfile.mkdtemp(prefix='agent-manager-main-send-fail-queue-'))
        deps = SimpleNamespace(
            __file__='main.py',
            resolve_agent=lambda _agent: {'name': 'main', 'file_id': 'main', 'launcher': 'droid'},
            get_agent_id=lambda config: config.get('file_id', '').lower(),
            check_tmux=lambda: True,
            session_exists=lambda agent_id: agent_id == 'main',
            Path=Path,
            resolve_launcher_command=lambda launcher: launcher,
            _should_use_codex_file_pointer=lambda _msg: False,
            get_repo_root=lambda: temp_root,
            write_codex_message_file=lambda *_args, **_kwargs: Path('/tmp/message.md'),
            send_keys=lambda *_args, **_kwargs: False,
            enqueue_inbound_message=enqueue_inbound_message,
            mark_inbound_message_state=mark_inbound_message_state,
            was_message_yielded=was_message_yielded,
            append_inbound_message_event=append_inbound_message_event,
        )

        output = io.StringIO()
        with redirect_stdout(output):
            rc = cmd_send(
                argparse.Namespace(agent='main', message='keep-pending', send_enter=True),
                deps=deps,
            )

        self.assertEqual(rc, 1)
        pending = load_pending_inbound_messages(temp_root, agent_id='main')
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0].get('state'), 'failed')

    def test_send_main_marks_resumed_and_handled_after_prior_yield(self):
        calls = []
        temp_root = Path(tempfile.mkdtemp(prefix='agent-manager-main-resume-queue-'))
        message_id = enqueue_inbound_message(
            temp_root,
            agent_id='main',
            source='send',
            message_kind='message',
            message='resume-this',
        )
        note_pending_messages_yielded(
            temp_root,
            agent_id='main',
            heartbeat_id='HB-123',
            reason_code='HB_USER_QUEUE_PENDING',
            detail='heartbeat_pre_dispatch_yield',
        )

        deps = SimpleNamespace(
            __file__='main.py',
            resolve_agent=lambda _agent: {'name': 'main', 'file_id': 'main', 'launcher': 'droid'},
            get_agent_id=lambda config: config.get('file_id', '').lower(),
            check_tmux=lambda: True,
            session_exists=lambda agent_id: agent_id == 'main',
            Path=Path,
            resolve_launcher_command=lambda launcher: launcher,
            _should_use_codex_file_pointer=lambda _msg: False,
            get_repo_root=lambda: temp_root,
            write_codex_message_file=lambda *_args, **_kwargs: Path('/tmp/message.md'),
            send_keys=lambda agent_id, message, **kwargs: calls.append((agent_id, message, kwargs)) or True,
            get_agent_runtime_state=lambda _agent_id, launcher='': {'state': 'busy', 'reason': 'busy_pattern:Thinking...'},
            enqueue_inbound_message=lambda *_args, **_kwargs: message_id,
            mark_inbound_message_state=mark_inbound_message_state,
            was_message_yielded=was_message_yielded,
            append_inbound_message_event=append_inbound_message_event,
        )

        output = io.StringIO()
        with redirect_stdout(output):
            rc = cmd_send(
                argparse.Namespace(agent='main', message='resume-this', send_enter=True),
                deps=deps,
            )

        self.assertEqual(rc, 0)
        events = read_inbound_events(temp_root, agent_id='main', message_id=message_id)
        names = [event.get('event') for event in events]
        self.assertEqual(
            names,
            ['received', 'queued', 'yielded', 'resumed', 'dispatching', 'dispatched', 'handled', 'replied'],
        )
        self.assertEqual(events[-1].get('reply_evidence'), 'transport_ack')
        self.assertEqual(events[-1].get('transport_ack_status'), 'ack')
        self.assertEqual(events[-1].get('transport_ack_detail'), 'busy:busy_pattern:Thinking...')

    def test_inbound_drain_once_replays_pending_main_message(self):
        calls = []
        temp_root = Path(tempfile.mkdtemp(prefix='agent-manager-main-drain-queue-'))
        message_id = enqueue_inbound_message(
            temp_root,
            agent_id='main',
            source='assign',
            message_kind='task_assignment',
            message='finish issue 122',
        )

        with patch('main.resolve_agent', return_value={'name': 'main', 'file_id': 'main', 'launcher': 'codex'}), \
             patch('main.get_agent_id', side_effect=lambda config: config.get('file_id', '').lower()), \
             patch('main.check_tmux', return_value=True), \
             patch('main.session_exists', return_value=True), \
             patch('main.get_repo_root', return_value=temp_root), \
             patch('main.resolve_launcher_command', return_value='codex'), \
             patch('main._should_use_codex_file_pointer', return_value=False), \
             patch('main.get_agent_runtime_state', return_value={'state': 'busy', 'reason': 'busy_pattern:Thinking'}), \
             patch('main.send_keys', side_effect=lambda agent_id, message, **kwargs: calls.append((agent_id, message, kwargs)) or True):
            output = io.StringIO()
            with redirect_stdout(output):
                rc = main.cmd_inbound(
                    argparse.Namespace(inbound_command='drain', agent='main', once=True),
                )

        self.assertEqual(rc, 0)
        self.assertEqual(calls[0][0], 'main')
        self.assertIn('# Task Assignment', calls[0][1])
        events = read_inbound_events(temp_root, agent_id='main', message_id=message_id)
        self.assertEqual(
            [event.get('event') for event in events],
            ['received', 'queued', 'claimed', 'dispatching', 'dispatched', 'handled', 'replied'],
        )
        self.assertEqual(events[-1].get('reply_evidence'), 'transport_ack')
        self.assertEqual(events[-1].get('transport_ack_status'), 'ack')
        self.assertEqual(events[-1].get('transport_ack_detail'), 'busy:busy_pattern:Thinking')
        self.assertIn('drained=1', output.getvalue())

    def test_inbound_drain_once_does_not_mark_handled_when_delivery_unconfirmed(self):
        calls = []
        temp_root = Path(tempfile.mkdtemp(prefix='agent-manager-main-drain-unconfirmed-queue-'))
        message_id = enqueue_inbound_message(
            temp_root,
            agent_id='main',
            source='send',
            message_kind='message',
            message='pending replay',
        )

        class _FakeTime:
            def __init__(self):
                self._now = 0.0

            def time(self):
                return self._now

            def sleep(self, seconds):
                self._now += float(seconds)

        fake_time = _FakeTime()

        with patch('main.resolve_agent', return_value={'name': 'main', 'file_id': 'main', 'launcher': 'codex'}), \
             patch('main.get_agent_id', side_effect=lambda config: config.get('file_id', '').lower()), \
             patch('main.check_tmux', return_value=True), \
             patch('main.session_exists', return_value=True), \
             patch('main.get_repo_root', return_value=temp_root), \
             patch('main.resolve_launcher_command', return_value='codex'), \
             patch('main._should_use_codex_file_pointer', return_value=False), \
             patch('main.get_agent_runtime_state', return_value={'state': 'idle', 'reason': 'ready'}), \
             patch('main.time', fake_time), \
             patch('main.send_keys', side_effect=lambda agent_id, message, **kwargs: calls.append((agent_id, message, kwargs)) or True):
            output = io.StringIO()
            with redirect_stdout(output):
                rc = main.cmd_inbound(
                    argparse.Namespace(inbound_command='drain', agent='main', once=True),
                )

        self.assertEqual(rc, 1)
        self.assertEqual(calls[0][0], 'main')
        events = read_inbound_events(temp_root, agent_id='main', message_id=message_id)
        self.assertEqual(
            [event.get('event') for event in events],
            ['received', 'queued', 'claimed', 'dispatching', 'dispatched', 'failed'],
        )
        self.assertNotIn('handled', [event.get('event') for event in events])
        self.assertNotIn('replied', [event.get('event') for event in events])

    def test_inbound_drain_once_marks_reclaimed_for_stale_dispatching(self):
        calls = []
        temp_root = Path(tempfile.mkdtemp(prefix='agent-manager-main-drain-reclaim-queue-'))
        message_id = enqueue_inbound_message(
            temp_root,
            agent_id='main',
            source='send',
            message_kind='message',
            message='reclaim pending replay',
        )
        append_inbound_message_event(
            temp_root,
            agent_id='main',
            message_id=message_id,
            event='dispatching',
            state='dispatching',
            detail='prior_dispatch_start',
            attempt_count=1,
            dispatching_at='2026-03-18T00:00:00Z',
        )

        class _FakeTime:
            def __init__(self):
                self._now = 0.0

            def time(self):
                return self._now

            def sleep(self, seconds):
                self._now += float(seconds)

        fake_time = _FakeTime()

        with patch('main.resolve_agent', return_value={'name': 'main', 'file_id': 'main', 'launcher': 'codex'}), \
             patch('main.get_agent_id', side_effect=lambda config: config.get('file_id', '').lower()), \
             patch('main.check_tmux', return_value=True), \
             patch('main.session_exists', return_value=True), \
             patch('main.get_repo_root', return_value=temp_root), \
             patch('main.resolve_launcher_command', return_value='codex'), \
             patch('main._should_use_codex_file_pointer', return_value=False), \
             patch('main.get_agent_runtime_state', return_value={'state': 'busy', 'reason': 'busy_pattern:Thinking'}), \
             patch('main.time', fake_time), \
             patch('main.send_keys', side_effect=lambda agent_id, message, **kwargs: calls.append((agent_id, message, kwargs)) or True):
            output = io.StringIO()
            with redirect_stdout(output):
                rc = main.cmd_inbound(
                    argparse.Namespace(inbound_command='drain', agent='main', once=True),
                )

        self.assertEqual(rc, 0)
        self.assertEqual(calls[0][0], 'main')
        events = read_inbound_events(temp_root, agent_id='main', message_id=message_id)
        self.assertEqual(
            [event.get('event') for event in events],
            ['received', 'queued', 'dispatching', 'reclaimed', 'claimed', 'dispatching', 'dispatched', 'handled', 'replied'],
        )
        reclaimed = events[3]
        self.assertEqual(reclaimed.get('detail'), 'inbound_drain_reclaimed:cli:stale_dispatching_lease')
        self.assertEqual(events[-1].get('reply_evidence'), 'transport_ack')
        self.assertEqual(events[-1].get('transport_ack_status'), 'ack')
        self.assertEqual(events[-1].get('transport_ack_detail'), 'busy:busy_pattern:Thinking')

    def test_start_restore_main_runs_one_inbound_drain_pass_for_existing_session(self):
        args = argparse.Namespace(agent='main', working_dir=None, restore=True, tmux_layout='sessions')

        with patch('main.check_tmux', return_value=True), \
             patch('main.resolve_agent', return_value={'name': 'main', 'file_id': 'main', 'launcher': 'codex', 'enabled': True}), \
             patch('main.get_agent_id', return_value='main'), \
             patch('main.session_exists', return_value=True), \
             patch('main.get_session_info', return_value={'session': 'main', 'mode': 'sessions'}), \
             patch('main.drain_main_inbound_once', return_value={'rc': 0, 'drained': 1, 'failed': 0, 'dead_lettered': 0, 'skipped': 0}) as mock_drain:
            output = io.StringIO()
            with redirect_stdout(output):
                rc = main.cmd_start(args)

        self.assertEqual(rc, 0)
        mock_drain.assert_called_once_with(agent_id='main', trigger='start_restore')
        self.assertIn('Restored existing session', output.getvalue())
        self.assertIn('Inbound drain after restore', output.getvalue())


if __name__ == '__main__':
    unittest.main()
