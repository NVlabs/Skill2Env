from __future__ import annotations
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import main  # noqa: E402


class HeartbeatSessionModeTests(unittest.TestCase):
    def setUp(self):
        self.temp_root = Path(tempfile.mkdtemp(prefix='heartbeat-mode-'))

    def tearDown(self):
        shutil.rmtree(self.temp_root, ignore_errors=True)

    def test_normalize_heartbeat_session_mode(self):
        self.assertEqual(main._normalize_heartbeat_session_mode('auto'), 'auto')
        self.assertEqual(main._normalize_heartbeat_session_mode('fresh'), 'fresh')
        self.assertEqual(main._normalize_heartbeat_session_mode('force'), 'force')
        self.assertEqual(main._normalize_heartbeat_session_mode('restore'), 'restore')
        self.assertEqual(main._normalize_heartbeat_session_mode('AUTO'), 'auto')
        self.assertEqual(main._normalize_heartbeat_session_mode('unknown'), 'restore')
        self.assertEqual(main._normalize_heartbeat_session_mode(None), 'restore')

    def test_normalize_heartbeat_mode(self):
        self.assertEqual(main._normalize_heartbeat_mode('full_speed'), 'full_speed')
        self.assertEqual(main._normalize_heartbeat_mode('FULL_SPEED'), 'full_speed')
        self.assertEqual(main._normalize_heartbeat_mode('normal'), 'normal')
        self.assertEqual(main._normalize_heartbeat_mode('unknown'), 'normal')
        self.assertEqual(main._normalize_heartbeat_mode(None), 'normal')

    def test_extract_context_left_percent_prefers_latest_match(self):
        output = (
            '... 43% context left\n'
            '... some more text\n'
            '... 18% context left\n'
        )
        self.assertEqual(main._extract_context_left_percent(output, launcher='codex'), 18)

    def test_extract_context_left_percent_handles_missing_values(self):
        self.assertIsNone(main._extract_context_left_percent('no context marker here', launcher='codex'))
        self.assertIsNone(main._extract_context_left_percent('999% context left', launcher='codex'))

    def test_extract_context_left_percent_respects_provider_patterns(self):
        output = '18% context left'
        self.assertEqual(main._extract_context_left_percent(output, launcher='codex'), 18)
        self.assertEqual(main._extract_context_left_percent(output, launcher='unknown-cli'), 18)

    def test_heartbeat_handoff_saved_detection(self):
        temp_root = Path(tempfile.mkdtemp(prefix='hb-handoff-'))
        try:
            handoff_file = temp_root / 'handoff.md'
            handoff_file.write_text('- Status: pending\n', encoding='utf-8')
            self.assertFalse(main._heartbeat_handoff_saved(handoff_file))

            handoff_file.write_text('- Status: saved\n## Next Action\n- run', encoding='utf-8')
            self.assertTrue(main._heartbeat_handoff_saved(handoff_file))

            handoff_file.write_text('\n'.join(['line'] * 40), encoding='utf-8')
            self.assertTrue(main._heartbeat_handoff_saved(handoff_file))
        finally:
            shutil.rmtree(temp_root, ignore_errors=True)

    def test_should_rollover_heartbeat_session(self):
        self.assertTrue(main._should_rollover_heartbeat_session('fresh', None))
        self.assertTrue(main._should_rollover_heartbeat_session('auto', 24))
        self.assertFalse(main._should_rollover_heartbeat_session('auto', 25))
        self.assertFalse(main._should_rollover_heartbeat_session('auto', None))
        self.assertFalse(main._should_rollover_heartbeat_session('restore', 1))

    def test_sync_codex_fullspeed_stop_hook_writes_managed_hook(self):
        workspace = self.temp_root / 'workspace'
        codex_dir = workspace / '.codex'
        codex_dir.mkdir(parents=True, exist_ok=True)
        (workspace / '.git').mkdir()
        hooks_payload = {
            'hooks': {
                'Stop': [
                    {
                        'hooks': [
                            {
                                'type': 'command',
                                'command': 'python3 /tmp/fullspeed_stop_hook.py --agent EMP_0001',
                                'statusMessage': main._FULL_SPEED_STOP_HOOK_STATUS_MESSAGE,
                            },
                            {
                                'type': 'command',
                                'command': 'python3 /tmp/custom.py',
                                'statusMessage': 'custom stop hook',
                            },
                        ]
                    }
                ]
            }
        }
        hooks_path = codex_dir / 'hooks.json'
        hooks_path.write_text(__import__('json').dumps(hooks_payload, ensure_ascii=False, indent=2) + "\n", encoding='utf-8')
        agent_config = {
            'name': 'dev',
            'file_id': 'EMP_0001',
            'working_directory': str(workspace),
            'launcher': 'codex',
            'heartbeat': {
                'enabled': True,
                'mode': 'full_speed',
                'max_runtime': '5m',
            },
        }

        with patch('main.get_repo_root', return_value=self.temp_root):
            result = main._sync_codex_fullspeed_stop_hook(agent_config, working_dir=str(workspace), repo_root=self.temp_root)

        self.assertTrue(result['enabled'])
        self.assertTrue(hooks_path.exists())
        self.assertFalse(result['active'])

        payload = __import__('json').loads(hooks_path.read_text(encoding='utf-8'))
        stop_groups = payload['hooks']['Stop']
        self.assertEqual(len(stop_groups), 1)
        self.assertEqual(stop_groups[0]['hooks'][0]['statusMessage'], 'custom stop hook')

    def test_sync_codex_fullspeed_stop_hook_keeps_managed_hook_when_mode_normal(self):
        workspace = self.temp_root / 'workspace'
        codex_dir = workspace / '.codex'
        codex_dir.mkdir(parents=True, exist_ok=True)
        (workspace / '.git').mkdir()
        managed_command = 'python3 /tmp/fullspeed_stop_hook.py --agent EMP_0001'
        hooks_payload = {
            'hooks': {
                'Stop': [
                    {
                        'hooks': [
                            {
                                'type': 'command',
                                'command': managed_command,
                                'statusMessage': main._FULL_SPEED_STOP_HOOK_STATUS_MESSAGE,
                            },
                            {
                                'type': 'command',
                                'command': 'python3 /tmp/custom.py',
                                'statusMessage': 'custom stop hook',
                            },
                        ]
                    }
                ]
            }
        }
        hooks_path = codex_dir / 'hooks.json'
        hooks_path.write_text(__import__('json').dumps(hooks_payload, ensure_ascii=False, indent=2) + "\n", encoding='utf-8')
        agent_config = {
            'name': 'dev',
            'file_id': 'EMP_0001',
            'working_directory': str(workspace),
            'launcher': 'codex',
            'heartbeat': {
                'enabled': True,
                'mode': 'normal',
            },
        }

        with patch('main.get_repo_root', return_value=self.temp_root):
            result = main._sync_codex_fullspeed_stop_hook(agent_config, working_dir=str(workspace), repo_root=self.temp_root)

        self.assertTrue(result['enabled'])
        self.assertFalse(result['active'])
        payload = __import__('json').loads(hooks_path.read_text(encoding='utf-8'))
        stop_groups = payload['hooks']['Stop']
        self.assertEqual(len(stop_groups), 1)
        self.assertEqual(stop_groups[0]['hooks'][0]['statusMessage'], 'custom stop hook')


if __name__ == '__main__':
    unittest.main()
