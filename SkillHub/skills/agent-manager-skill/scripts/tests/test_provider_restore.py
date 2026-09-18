from __future__ import annotations
import os
import tempfile
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(SCRIPTS_DIR.parent) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR.parent))

import main  # noqa: E402
from providers import get_session_restore_flag, get_session_restore_mode  # noqa: E402


class ProviderRestoreTests(unittest.TestCase):
    def test_codex_provider_restore_config(self):
        self.assertEqual(get_session_restore_mode("codex"), "cli_optional_arg")
        self.assertEqual(get_session_restore_flag("codex"), "resume")

    def test_codex_restore_args_are_prefixed_with_resume_and_session(self):
        args = main._apply_session_restore_args(
            provider_key="codex",
            launcher="codex",
            launcher_args=["--model=gpt-5.3-codex", "--dangerously-bypass-approvals-and-sandbox"],
            restore_flag="resume",
            session_id="019c3eb0-bca0-7ab0-8b93-3b54b5f582dc",
        )
        self.assertGreaterEqual(len(args), 2)
        self.assertEqual(args[0], "resume")
        self.assertEqual(args[1], "019c3eb0-bca0-7ab0-8b93-3b54b5f582dc")
        self.assertIn("--model=gpt-5.3-codex", args)

    def test_find_new_codex_session_id_filters_by_owner_marker_and_cwd(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sessions_root = Path(tmpdir)
            target_cwd = "/home/elliot245/work-assistant"
            agent_id = "main"
            good_id = "019c3eb0-bca0-7ab0-8b93-3b54b5f582dc"
            bad_id = "019c3eb0-bca0-7ab0-8b93-3b54b5f582dd"
            marker = main._codex_session_owner_marker(agent_id)

            good_file = sessions_root / f"rollout-good-{good_id}.jsonl"
            good_file.write_text(
                '{"type":"session_meta","payload":{"id":"%s","cwd":"%s","base_instructions":{"text":"%s\\nmain prompt"}}}\n'
                % (good_id, target_cwd, marker),
                encoding="utf-8",
            )

            bad_file = sessions_root / f"rollout-bad-{bad_id}.jsonl"
            bad_file.write_text(
                '{"type":"session_meta","payload":{"id":"%s","cwd":"%s","base_instructions":{"text":"other session"}}}\n'
                % (bad_id, target_cwd),
                encoding="utf-8",
            )
            os.utime(good_file, (1, 1))
            os.utime(bad_file, (2, 2))

            with patch("main._codex_sessions_dir", return_value=sessions_root):
                session_id = main._find_new_codex_session_id(
                    target_cwd,
                    before_jsonl_paths=set(),
                    agent_id=agent_id,
                )

            self.assertEqual(session_id, good_id)

    def test_find_new_codex_session_id_filters_by_cwd_for_non_main(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sessions_root = Path(tmpdir)
            target_cwd = "/home/elliot245/work-assistant-a"
            other_cwd = "/home/elliot245/work-assistant-b"
            agent_id = "emp-0002"
            good_id = "019c3eb0-bca0-7ab0-8b93-3b54b5f582de"
            bad_id = "019c3eb0-bca0-7ab0-8b93-3b54b5f582df"

            good_file = sessions_root / f"rollout-good-{good_id}.jsonl"
            good_file.write_text(
                '{"type":"session_meta","payload":{"id":"%s","cwd":"%s","base_instructions":{"text":"coder prompt"}}}\n'
                % (good_id, target_cwd),
                encoding="utf-8",
            )

            bad_file = sessions_root / f"rollout-bad-{bad_id}.jsonl"
            bad_file.write_text(
                '{"type":"session_meta","payload":{"id":"%s","cwd":"%s","base_instructions":{"text":"other cwd"}}}\n'
                % (bad_id, other_cwd),
                encoding="utf-8",
            )
            os.utime(good_file, (1, 1))
            os.utime(bad_file, (2, 2))

            with patch("main._codex_sessions_dir", return_value=sessions_root):
                session_id = main._find_new_codex_session_id(
                    target_cwd,
                    before_jsonl_paths=set(),
                    agent_id=agent_id,
                )

            self.assertEqual(session_id, good_id)

    def test_codex_session_exists_rejects_wrong_owner(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sessions_root = Path(tmpdir)
            session_id = "019c3eb0-bca0-7ab0-8b93-3b54b5f582dc"
            session_file = sessions_root / f"rollout-{session_id}.jsonl"
            session_file.write_text(
                '{"type":"session_meta","payload":{"id":"%s","cwd":"/home/elliot245/work-assistant","base_instructions":{"text":"other owner"}}}\n'
                % session_id,
                encoding="utf-8",
            )

            with patch("main._codex_sessions_dir", return_value=sessions_root):
                ok = main._codex_session_exists(
                    "/home/elliot245/work-assistant",
                    session_id,
                    agent_id="main",
                )

            self.assertFalse(ok)

    def test_codex_session_exists_rejects_wrong_cwd_for_non_main(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sessions_root = Path(tmpdir)
            session_id = "019c3eb0-bca0-7ab0-8b93-3b54b5f582e0"
            session_file = sessions_root / f"rollout-{session_id}.jsonl"
            session_file.write_text(
                '{"type":"session_meta","payload":{"id":"%s","cwd":"/home/elliot245/work-assistant-b","base_instructions":{"text":"other owner"}}}\n'
                % session_id,
                encoding="utf-8",
            )

            with patch("main._codex_sessions_dir", return_value=sessions_root):
                ok = main._codex_session_exists(
                    "/home/elliot245/work-assistant-a",
                    session_id,
                    agent_id="emp-0002",
                )

            self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
