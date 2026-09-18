#!/usr/bin/env python3
"""Install Alpha Insights into Codex Desktop and register hook wrappers."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


SKILL_NAME = "alpha-insights"
SOURCE_ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_NAMES = {
    ".git",
    ".DS_Store",
    "__pycache__",
    "node_modules",
    "build",
    "dist",
}


def _codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex").expanduser()


def _ignore(_directory: str, names: list[str]) -> set[str]:
    ignored = set()
    for name in names:
        if name in EXCLUDED_NAMES or name.endswith(".pyc"):
            ignored.add(name)
    return ignored


def _remove_frontmatter_hooks(text: str) -> str:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return text

    end = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end = idx
            break
    if end is None:
        return text

    output = [lines[0]]
    idx = 1
    while idx < end:
        line = lines[idx]
        if line.startswith("hooks:"):
            idx += 1
            while idx < end:
                candidate = lines[idx]
                if candidate.strip() and not candidate.startswith((" ", "\t", "#")):
                    break
                idx += 1
            continue
        output.append(line)
        idx += 1

    output.extend(lines[end:])
    return "".join(output)


def _adapt_skill_md(skill_path: Path, target: Path) -> None:
    text = skill_path.read_text(encoding="utf-8")
    text = _remove_frontmatter_hooks(text)
    text = text.replace("${CLAUDE_SKILL_DIR}", str(target))
    text = text.replace("${CLAUDE_PLUGIN_ROOT}", str(target))
    skill_path.write_text(text, encoding="utf-8")


def _remove_existing_target(target: Path) -> None:
    if target.is_dir() and not target.is_symlink():
        shutil.rmtree(target)
    elif target.exists() or target.is_symlink():
        target.unlink()


def _copy_skill_tree(target: Path) -> None:
    target = target.expanduser()
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_name(f".{target.name}.tmp-{os.getpid()}")
    if tmp.exists():
        shutil.rmtree(tmp)

    try:
        shutil.copytree(SOURCE_ROOT, tmp, ignore=_ignore)
        _adapt_skill_md(tmp / "SKILL.md", target)

        _remove_existing_target(target)
        shutil.move(str(tmp), str(target))
    except Exception:
        if tmp.exists():
            shutil.rmtree(tmp)
        raise


def _load_hooks(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"hooks": {}}
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    data.setdefault("hooks", {})
    return data


def _is_alpha_wrapper(command: str, wrapper_name: str) -> bool:
    return wrapper_name in command and "scripts/codex_hooks/" in command


def _replace_wrapper_entry(
    hooks_data: dict[str, Any],
    event: str,
    command: str,
    timeout: int,
    wrapper_name: str,
) -> None:
    hooks = hooks_data.setdefault("hooks", {})
    entries = hooks.setdefault(event, [])
    if not isinstance(entries, list):
        raise ValueError(f"hooks.{event} must be a list")

    cleaned = []
    for entry in entries:
        if not isinstance(entry, dict):
            cleaned.append(entry)
            continue
        hook_list = entry.get("hooks")
        if not isinstance(hook_list, list):
            cleaned.append(entry)
            continue
        filtered = [
            hook for hook in hook_list
            if not _is_alpha_wrapper(str(hook.get("command", "")), wrapper_name)
        ]
        if filtered:
            new_entry = dict(entry)
            new_entry["hooks"] = filtered
            cleaned.append(new_entry)

    cleaned.append({
        "matcher": ".*",
        "hooks": [{
            "type": "command",
            "command": command,
            "timeout": timeout,
        }],
    })
    hooks[event] = cleaned


def _register_hooks(hooks_json: Path, target: Path) -> None:
    hooks_json = hooks_json.expanduser()
    hooks_json.parent.mkdir(parents=True, exist_ok=True)
    data = _load_hooks(hooks_json)

    pre = target / "scripts" / "codex_hooks" / "alpha_insights_pre_tool.py"
    post = target / "scripts" / "codex_hooks" / "alpha_insights_post_tool.py"
    _replace_wrapper_entry(
        data,
        "PreToolUse",
        f"python3 {pre}",
        5,
        "alpha_insights_pre_tool.py",
    )
    _replace_wrapper_entry(
        data,
        "PostToolUse",
        f"python3 {post}",
        10,
        "alpha_insights_post_tool.py",
    )

    tmp = hooks_json.with_suffix(hooks_json.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(hooks_json)


def _run_verify(target: Path, hooks_json: Path) -> None:
    verifier = target / "scripts" / "verify_codex.py"
    subprocess.run(
        [sys.executable, str(verifier), "--skill-root", str(target), "--hooks-json", str(hooks_json)],
        check=True,
    )


def main() -> None:
    codex_home = _codex_home()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, default=codex_home / "skills" / SKILL_NAME)
    parser.add_argument("--hooks-json", type=Path, default=codex_home / "hooks.json")
    parser.add_argument("--verify", action="store_true", help="Run verify_codex.py after install (default behavior)")
    parser.add_argument("--skip-verify", action="store_true", help="Install without running verify_codex.py")
    args = parser.parse_args()

    target = args.target.expanduser()
    hooks_json = args.hooks_json.expanduser()
    _copy_skill_tree(target)
    _register_hooks(hooks_json, target)

    if not args.skip_verify:
        _run_verify(target, hooks_json)

    result = {
        "installed_path": str(target),
        "hooks_json": str(hooks_json),
        "status": "OK",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
