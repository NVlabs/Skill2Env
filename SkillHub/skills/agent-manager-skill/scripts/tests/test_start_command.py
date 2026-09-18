from __future__ import annotations
import os
import sys
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import main  # noqa: E402


class BuildStartCommandTests(unittest.TestCase):
    def test_quotes_working_dir_and_args_with_spaces(self):
        cmd = main.build_start_command(
            working_dir="/tmp/a b",
            launcher="/path/with space/codex",
            launcher_args=["--model=gpt-5.2", "--flag", "value with space"],
        )
        self.assertIn("cd '/tmp/a b'", cmd)
        self.assertIn("'/path/with space/codex'", cmd)
        self.assertIn("'value with space'", cmd)

    def test_filters_empty_and_none_args(self):
        cmd = main.build_start_command(
            working_dir="/tmp",
            launcher="codex",
            launcher_args=["", None, "--x", 0],
        )
        self.assertIn("codex", cmd)
        self.assertIn("--x", cmd)
        self.assertNotIn("None", cmd)
        self.assertNotIn("''", cmd)

    def test_path_env_prefix_is_present(self):
        cmd = main.build_start_command(
            working_dir="/tmp",
            launcher="codex",
            launcher_args=[],
        )
        self.assertIn('export PATH="$HOME/.local/bin:$HOME/bin:$PATH"', cmd)


class LauncherCliConfigTests(unittest.TestCase):
    def test_build_launcher_config_overrides_from_flat_launcher_config(self):
        cfg = {
            "launcher": "codex",
            "launcher_config": {
                "model_instructions_file": "prompts/shade.md",
                "feature_flag": True,
                "retries": 3,
            },
            "heartbeat": {
                "enabled": True,
                "mode": "normal",
            },
        }
        overrides = main.build_launcher_config_overrides(cfg, working_dir="/repo")
        self.assertEqual(overrides["model_instructions_file"], "/repo/prompts/shade.md")
        self.assertTrue(overrides["feature_flag"])
        self.assertEqual(overrides["retries"], 3)

    def test_build_launcher_config_overrides_does_not_force_codex_hooks(self):
        cfg = {
            "launcher": "codex",
            "launcher_config": {},
            "heartbeat": {
                "enabled": False,
                "mode": "normal",
            },
        }
        overrides = main.build_launcher_config_overrides(cfg, working_dir="/repo")
        self.assertNotIn("features.codex_hooks", overrides)

    def test_to_toml_literal_supports_scalars_lists_and_dicts(self):
        self.assertEqual(main._to_toml_literal("x"), '"x"')
        self.assertEqual(main._to_toml_literal(True), "true")
        self.assertEqual(main._to_toml_literal([1, "two"]), '[1, "two"]')
        self.assertEqual(main._to_toml_literal({"flag": True, "count": 2}), '{ "flag" = true, "count" = 2 }')


if __name__ == "__main__":
    unittest.main()
