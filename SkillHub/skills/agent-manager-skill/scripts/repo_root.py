"""Repository root + skill location helpers.

This skill is designed to be installable via OpenSkills into arbitrary locations
(e.g. ~/.claude/skills/agent-manager). Therefore we must not assume the skill
code lives under <repo>/.agent/skills.

Repo root resolution priority:
1) $REPO_ROOT (if set)
2) git (superproject if in submodule, else toplevel)
3) walk up from cwd looking for .agent/ and agents/
4) fall back to cwd
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Iterable, Optional


def _run_git(cwd: Path, args: list[str]) -> Optional[str]:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            check=True,
        )
        value = (result.stdout or "").strip()
        return value or None
    except Exception:
        return None


def _walk_parents(start_dir: Path) -> Iterable[Path]:
    yield start_dir
    yield from start_dir.parents


def find_repo_root(start: Path) -> Path:
    repo_root_env = os.environ.get("REPO_ROOT")
    if repo_root_env:
        return Path(repo_root_env).expanduser()

    start_dir = start if start.is_dir() else start.parent

    # Prefer the superproject root if we're inside a git submodule.
    superproject = _run_git(start_dir, ["rev-parse", "--show-superproject-working-tree"])
    if superproject:
        return Path(superproject)

    toplevel = _run_git(start_dir, ["rev-parse", "--show-toplevel"])
    if toplevel:
        return Path(toplevel)

    # Fallback: detect a repo-like layout without requiring git.
    for candidate in _walk_parents(start_dir):
        if (candidate / ".agent").is_dir() and (candidate / "agents").is_dir():
            return candidate

    return start_dir


def get_repo_root() -> Path:
    return find_repo_root(Path.cwd())


def get_skill_search_dirs(repo_root: Optional[Path]) -> list[Path]:
    """Search roots (first match wins) for skill directories."""
    home = Path.home()
    roots: list[Path] = []

    if repo_root is not None:
        roots.append(repo_root / ".agent" / "skills")
    roots.append(home / ".agent" / "skills")

    if repo_root is not None:
        roots.append(repo_root / ".claude" / "skills")
    roots.append(home / ".claude" / "skills")

    return roots
