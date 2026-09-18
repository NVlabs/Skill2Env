import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


INSTALLER = Path(__file__).resolve().parents[1] / "install_codex.py"


class CodexInstallTests(unittest.TestCase):
    def test_reinstall_replaces_target_without_sibling_backups(self) -> None:
        with tempfile.TemporaryDirectory(prefix="alpha-codex-install-") as tmp:
            codex_home = Path(tmp) / "codex"
            env = os.environ.copy()
            env["CODEX_HOME"] = str(codex_home)

            for _ in range(2):
                subprocess.run(
                    [sys.executable, str(INSTALLER), "--skip-verify"],
                    check=True,
                    env=env,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )

            skills_dir = codex_home / "skills"
            alpha_entries = sorted(path.name for path in skills_dir.glob("alpha-insights*"))
            self.assertEqual(alpha_entries, ["alpha-insights"])

            hooks = json.loads((codex_home / "hooks.json").read_text(encoding="utf-8"))
            commands = [
                hook.get("command", "")
                for entries in hooks.get("hooks", {}).values()
                for entry in entries
                for hook in entry.get("hooks", [])
            ]
            install_root = codex_home / "skills" / "alpha-insights"
            self.assertIn(
                f"python3 {install_root / 'scripts/codex_hooks/alpha_insights_pre_tool.py'}",
                commands,
            )
            self.assertIn(
                f"python3 {install_root / 'scripts/codex_hooks/alpha_insights_post_tool.py'}",
                commands,
            )

    def test_reinstall_removes_stale_custom_wrapper_paths(self) -> None:
        with tempfile.TemporaryDirectory(prefix="alpha-codex-install-") as tmp:
            codex_home = Path(tmp) / "codex"
            hooks_json = codex_home / "hooks.json"
            hooks_json.parent.mkdir(parents=True)
            stale_root = Path(tmp) / "old-custom-alpha-insights"
            hooks_json.write_text(
                json.dumps({
                    "hooks": {
                        "PreToolUse": [{
                            "matcher": ".*",
                            "hooks": [{
                                "type": "command",
                                "command": f"python3 {stale_root / 'scripts/codex_hooks/alpha_insights_pre_tool.py'}",
                                "timeout": 5,
                            }],
                        }],
                        "PostToolUse": [{
                            "matcher": ".*",
                            "hooks": [{
                                "type": "command",
                                "command": f"python3 {stale_root / 'scripts/codex_hooks/alpha_insights_post_tool.py'}",
                                "timeout": 10,
                            }],
                        }],
                    },
                }),
                encoding="utf-8",
            )

            env = os.environ.copy()
            env["CODEX_HOME"] = str(codex_home)
            subprocess.run(
                [sys.executable, str(INSTALLER), "--skip-verify"],
                check=True,
                env=env,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            hooks = json.loads(hooks_json.read_text(encoding="utf-8"))
            commands = [
                hook.get("command", "")
                for entries in hooks.get("hooks", {}).values()
                for entry in entries
                for hook in entry.get("hooks", [])
            ]
            self.assertTrue(commands)
            self.assertFalse(any(str(stale_root) in command for command in commands))
            self.assertEqual(
                sum("alpha_insights_pre_tool.py" in command for command in commands),
                1,
            )
            self.assertEqual(
                sum("alpha_insights_post_tool.py" in command for command in commands),
                1,
            )


if __name__ == "__main__":
    unittest.main()
