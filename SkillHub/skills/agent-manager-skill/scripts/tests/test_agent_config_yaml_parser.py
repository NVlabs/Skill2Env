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

import agent_config  # noqa: E402


class AgentConfigYamlParserTests(unittest.TestCase):
    def setUp(self):
        self.temp_root = Path(tempfile.mkdtemp(prefix="agent-manager-yaml-"))

    def tearDown(self):
        shutil.rmtree(self.temp_root, ignore_errors=True)

    def _write_agent_file(self, rel_path: str, frontmatter: str, body: str = "# role\n") -> Path:
        path = self.temp_root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"---\n{frontmatter.strip()}\n---\n{body}", encoding="utf-8")
        return path

    def test_parse_block_list_for_launcher_args_and_skills(self):
        agent_file = self._write_agent_file(
            "agents/EMP_0001/AGENTS.md",
            """
name: dev
description: Dev Agent
working_directory: ${REPO_ROOT}
launcher: claude
launcher_args:
  - --dangerously-skip-permissions
  - --model
  - sonnet
skills:
  - agent-manager
  - team-manager
""",
        )

        config = agent_config.parse_agent_file(agent_file)
        self.assertEqual(
            config.get("launcher_args"),
            ["--dangerously-skip-permissions", "--model", "sonnet"],
        )
        self.assertEqual(config.get("skills"), ["agent-manager", "team-manager"])

    def test_parse_yaml_value_scalar_types(self):
        self.assertIsNone(agent_config._parse_yaml_value("~"))
        self.assertIsNone(agent_config._parse_yaml_value("NULL"))
        self.assertIsNone(agent_config._parse_yaml_value("None"))

        self.assertTrue(agent_config._parse_yaml_value("true"))
        self.assertTrue(agent_config._parse_yaml_value("Yes"))
        self.assertFalse(agent_config._parse_yaml_value("false"))
        self.assertFalse(agent_config._parse_yaml_value("NO"))

        self.assertEqual(agent_config._parse_yaml_value(""), "")
        self.assertEqual(agent_config._parse_yaml_value("  "), "")

        self.assertEqual(agent_config._parse_yaml_value("42"), 42)
        self.assertEqual(agent_config._parse_yaml_value("3.14"), 3.14)
        self.assertEqual(agent_config._parse_yaml_value('"hello"'), "hello")
        self.assertEqual(agent_config._parse_yaml_value("'world'"), "world")
        self.assertEqual(agent_config._parse_yaml_value("plain-string"), "plain-string")
        self.assertEqual(agent_config._parse_yaml_value("[1, \"two\", false]"), [1, "two", False])

    def test_parse_yaml_list_quotes_commas_and_escaped_quotes(self):
        parsed = agent_config._parse_yaml_list('"a,b", \'c,d\', plain, 1, true, null')
        self.assertEqual(parsed, ["a,b", "c,d", "plain", 1, True, None])

        parsed2 = agent_config._parse_yaml_list(r'"x\"y", z')
        self.assertEqual(parsed2, ['x\\"y', "z"])

    def test_looks_like_mapping_entry(self):
        self.assertTrue(agent_config._looks_like_mapping_entry("name: value"))
        self.assertTrue(agent_config._looks_like_mapping_entry("key_1: 123"))
        self.assertFalse(agent_config._looks_like_mapping_entry("1name: value"))
        self.assertFalse(agent_config._looks_like_mapping_entry("https://example.com/a:b"))

    def test_parse_block_list_of_dicts_for_schedules(self):
        agent_file = self._write_agent_file(
            "agents/EMP_0002/AGENTS.md",
            """
name: qa
description: QA Agent
working_directory: ${REPO_ROOT}
launcher: codex
schedules:
  - name: daily-check
    cron: "0 9 * * *"
    enabled: true
    max_runtime: 30m
  - name: weekly-report
    cron: "0 18 * * 5"
    enabled: false
""",
        )

        config = agent_config.parse_agent_file(agent_file)
        schedules = config.get("schedules")

        self.assertIsInstance(schedules, list)
        self.assertEqual(len(schedules), 2)
        self.assertEqual(schedules[0]["name"], "daily-check")
        self.assertEqual(schedules[0]["cron"], "0 9 * * *")
        self.assertTrue(schedules[0]["enabled"])
        self.assertEqual(schedules[0]["max_runtime"], "30m")
        self.assertEqual(schedules[1]["name"], "weekly-report")
        self.assertFalse(schedules[1]["enabled"])

    def test_parse_block_list_with_empty_item_and_non_item_lines(self):
        lines = [
            "  # comment",
            "",
            "  -",
            "    foo: bar",
            "  -",
            "  - https://example.com/a:b",
            "  key: value",  # not a list item, should be ignored by block-list parser
            "not-indented-enough",
        ]
        parsed = agent_config._parse_yaml_block_list(lines, parent_indent=0)
        self.assertEqual(parsed[0], {"foo": "bar"})
        self.assertIsNone(parsed[1])
        self.assertEqual(parsed[2], "https://example.com/a:b")

    def test_parse_block_list_handles_blank_continuation_lines(self):
        lines = [
            "  - name: job1",
            "",
            "    cron: \"*/5 * * * *\"",
            "  - plain",
        ]
        parsed = agent_config._parse_yaml_block_list(lines, parent_indent=0)
        self.assertEqual(parsed[0]["name"], "job1")
        self.assertEqual(parsed[0]["cron"], "*/5 * * * *")
        self.assertEqual(parsed[1], "plain")

    def test_parse_yaml_dict_handles_nested_blocks_and_malformed_lines(self):
        lines = [
            "name: dev",
            "",
            "# comment",
            "badline-without-colon",
            "heartbeat:",
            "  cron: \"*/10 * * * *\"",
            "",
            "  enabled: true",
            "skills:",
            "  - agent-manager",
            "  - team-manager",
        ]
        parsed = agent_config._parse_yaml_dict(lines, indent_level=0)
        self.assertEqual(parsed["name"], "dev")
        self.assertEqual(parsed["heartbeat"]["cron"], "*/10 * * * *")
        self.assertTrue(parsed["heartbeat"]["enabled"])
        self.assertEqual(parsed["skills"], ["agent-manager", "team-manager"])

    def test_parse_yaml_dict_nested_branch_without_result_and_empty_value(self):
        # Indented content with no previous key should be skipped safely.
        parsed = agent_config._parse_yaml_dict(["  child: 1"], indent_level=0)
        self.assertEqual(parsed, {})

        # Empty value with no nested block becomes None.
        parsed2 = agent_config._parse_yaml_dict(["name:"], indent_level=0)
        self.assertEqual(parsed2, {"name": None})

        # Early break path: current indent less than indent_level.
        parsed3 = agent_config._parse_yaml_dict(["name: dev"], indent_level=2)
        self.assertEqual(parsed3, {})

    def test_parse_yaml_dict_nested_branch_reassigns_last_key(self):
        parsed_list = agent_config._parse_yaml_dict(
            [
                "root: null",
                "  - one",
                "  - two",
                "after: ok",
            ],
            indent_level=0,
        )
        self.assertEqual(parsed_list["root"], ["one", "two"])
        self.assertEqual(parsed_list["after"], "ok")

        parsed_map = agent_config._parse_yaml_dict(
            [
                "root: null",
                "  child: 1",
                "",
                "after: ok",
            ],
            indent_level=0,
        )
        self.assertEqual(parsed_map["root"]["child"], 1)
        self.assertEqual(parsed_map["after"], "ok")

    def test_parse_yaml_frontmatter_variants(self):
        no_frontmatter = "hello world"
        self.assertEqual(agent_config._parse_yaml_frontmatter(no_frontmatter), {})

        empty_frontmatter = "---\n\n---\nbody"
        self.assertEqual(agent_config._parse_yaml_frontmatter(empty_frontmatter), {})

        valid_frontmatter = "---\nname: demo\nenabled: true\n---\nbody"
        self.assertEqual(
            agent_config._parse_yaml_frontmatter(valid_frontmatter),
            {"name": "demo", "enabled": True},
        )

    def test_parse_agent_file_invalid_format_raises(self):
        path = self.temp_root / "agents" / "EMP_9999" / "AGENTS.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("name: missing-frontmatter-markers\n", encoding="utf-8")

        with self.assertRaises(ValueError):
            agent_config.parse_agent_file(path)

    @patch("agent_config.get_repo_root")
    def test_resolve_main_keeps_block_list_launcher_args(self, mock_get_repo_root):
        repo_root = self.temp_root
        mock_get_repo_root.return_value = repo_root

        (repo_root / "agents").mkdir(parents=True, exist_ok=True)
        (repo_root / "AGENTS.md").write_text(
            """---
name: main
description: Main
working_directory: ${REPO_ROOT}
launcher: claude
launcher_args:
  - --dangerously-skip-permissions
skills:
  - agent-manager
---
# Main Agent
""",
            encoding="utf-8",
        )

        cfg = agent_config.resolve_agent("main")
        self.assertEqual(cfg.get("launcher"), "claude")
        self.assertEqual(cfg.get("launcher_args"), ["--dangerously-skip-permissions"])
        self.assertEqual(cfg.get("skills"), ["agent-manager"])

    @patch("agent_config.get_repo_root")
    def test_resolve_main_reads_launcher_config(self, mock_get_repo_root):
        repo_root = self.temp_root
        mock_get_repo_root.return_value = repo_root

        (repo_root / "agents").mkdir(parents=True, exist_ok=True)
        (repo_root / "AGENTS.md").write_text(
            """---
name: main
description: Main
working_directory: ${REPO_ROOT}
launcher: codex
launcher_config:
  model_instructions_file: ${REPO_ROOT}/.codex/main-codex-model.md
skills:
  - agent-manager
---
# Main Agent
""",
            encoding="utf-8",
        )

        cfg = agent_config.resolve_agent("main")
        self.assertTrue(cfg.get("launcher_config", {}).get("model_instructions_file", "").endswith("/.codex/main-codex-model.md"))

    def test_parse_agent_file_sets_defaults_for_optional_fields(self):
        agent_file = self._write_agent_file(
            "agents/EMP_0003/AGENTS.md",
            """
name: simple
description: simple
working_directory: ${REPO_ROOT}
launcher: claude
""",
        )
        cfg = agent_config.parse_agent_file(agent_file)
        self.assertEqual(cfg.get("launcher_args"), [])
        self.assertEqual(cfg.get("skills"), [])
        self.assertEqual(cfg.get("schedules"), [])
        self.assertEqual(cfg.get("mcps"), {})
        self.assertEqual(cfg.get("launcher_config"), {})
        self.assertTrue(cfg.get("enabled"))
        self.assertIsNone(cfg.get("heartbeat"))

    def test_parse_agent_file_supports_launcher_config(self):
        agent_file = self._write_agent_file(
            "agents/EMP_0004/AGENTS.md",
            """
name: shade
description: shade
working_directory: ${REPO_ROOT}
launcher: codex
launcher_config:
  model_instructions_file: ${REPO_ROOT}/prompt/shade.md
  feature_flag: true
""",
        )
        cfg = agent_config.parse_agent_file(agent_file)
        self.assertEqual(
            cfg.get("launcher_config"),
            {
                "model_instructions_file": "${REPO_ROOT}/prompt/shade.md",
                "feature_flag": True,
            },
        )


if __name__ == "__main__":
    unittest.main()
