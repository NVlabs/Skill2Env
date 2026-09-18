# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Minimal must-have static checks for creator-authored Harbor tasks.

Static validation is intentionally thin: the Harbor Oracle/NOP acceptance run is
the authoritative quality gate. These checks only stop (a) material that must
never ship (Codex credentials, private source provenance) and (b) states that
would make the Harbor acceptance run itself meaningless (missing required files,
shell syntax errors, verifier material baked into the environment image).
Small imperfections in generated data are tolerated by design.
"""

from __future__ import annotations

import math
import os
import re
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence

from .axes import TaskAxes
from .models import ContractError, CreatorResult, SkillBundle
from .task_config import HarborTaskConfigError, validate_harbor_task_toml


REQUIRED_FILES = (
    "instruction.md",
    "task.toml",
    "environment/Dockerfile",
    "tests/rubric.md",
    "tests/test.sh",
    "solution/solve.sh",
)
REQUIRED_DIRECTORIES = ("environment", "tests", "solution")
MIB_BYTES = 1024 * 1024
DEFAULT_MAX_TASK_SIZE_MIB = 128

# Names the environment image must never ingest: doing so leaks the verifier,
# the reference solution, or private creator state to the solving agent.
PRIVILEGED_NAMES = {
    "instruction.md",
    "rubric.md",
    "task.toml",
    "tests",
    "solution",
    "creator-result.json",
}

# Public names that would corrupt grading or leak private creator state.
# Everything else (stray logs, extra helper dirs) is tolerated.
FORBIDDEN_PUBLIC_NAMES = {
    "creator-result.json",
    "reward.txt",
    "reward.json",
}


class PostCheckError(ContractError):
    def __init__(self, errors: Sequence[str]):
        self.errors = list(errors)
        super().__init__("; ".join(self.errors))


@dataclass
class PostCheckReport:
    ok: bool
    checks: Dict[str, bool] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class TaskPostChecker:
    """Check structure, shell syntax, Harbor schema validity, and privacy."""

    def check(
        self,
        task_dir: Path,
        *,
        expected_name: str,
        bundle: SkillBundle,
        creator_result: CreatorResult,
        axes: TaskAxes | None = None,
    ) -> PostCheckReport:
        del expected_name, creator_result, axes  # host authors task.toml itself
        task_dir = task_dir.resolve()
        report = PostCheckReport(ok=False)
        errors: List[str] = []

        self._check_structure(task_dir, errors)
        report.checks["structure"] = not errors
        if errors:
            report.errors = errors
            return report

        dockerfile = _read_text(task_dir / "environment" / "Dockerfile", errors)

        before = len(errors)
        self._check_task_toml(task_dir / "task.toml", errors)
        report.checks["task_toml"] = len(errors) == before

        before = len(errors)
        self._check_shell(task_dir / "tests" / "test.sh", errors)
        self._check_shell(task_dir / "solution" / "solve.sh", errors)
        report.checks["scripts"] = len(errors) == before

        before = len(errors)
        self._check_privacy(task_dir, dockerfile, bundle, errors)
        report.checks["privacy"] = len(errors) == before

        report.errors = errors
        report.ok = not errors
        return report

    @staticmethod
    def _check_structure(task_dir: Path, errors: List[str]) -> None:
        if not task_dir.is_dir():
            errors.append(f"task directory missing: {task_dir}")
            return
        for relative in REQUIRED_FILES:
            path = task_dir / relative
            if not path.is_file() or path.is_symlink():
                errors.append(f"required regular file missing: {relative}")
        if (task_dir / "rubric.md").exists():
            errors.append("root rubric.md is not allowed; use tests/rubric.md")
        for directory in REQUIRED_DIRECTORIES:
            path = task_dir / directory
            if not path.is_dir() or path.is_symlink():
                errors.append(f"required regular directory missing: {directory}")

        for root, directories, files in os.walk(task_dir, followlinks=False):
            root_path = Path(root)
            for name in directories + files:
                path = root_path / name
                relative = path.relative_to(task_dir)
                if path.name in FORBIDDEN_PUBLIC_NAMES:
                    errors.append(f"private/generated artifact is public: {relative}")
                if not path.is_symlink():
                    continue
                try:
                    subtree = task_dir / relative.parts[0]
                    path.resolve(strict=True).relative_to(subtree)
                except (OSError, RuntimeError, ValueError):
                    errors.append(f"symlink escapes its task subtree or is broken: {relative}")

    @staticmethod
    def _check_task_toml(path: Path, errors: List[str]) -> None:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"cannot read task.toml: {exc}")
            return
        try:
            validate_harbor_task_toml(text)
        except HarborTaskConfigError as exc:
            errors.append(str(exc))

    @staticmethod
    def _check_shell(path: Path, errors: List[str]) -> None:
        try:
            syntax = subprocess.run(
                ["bash", "-n", str(path)], capture_output=True, text=True, timeout=10
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            errors.append(f"cannot statically validate {path.name}: {exc}")
        else:
            if syntax.returncode != 0:
                errors.append(f"invalid Bash in {path.name}: {syntax.stderr.strip()}")

    @staticmethod
    def _check_privacy(
        task_dir: Path,
        dockerfile: str,
        bundle: SkillBundle,
        errors: List[str],
    ) -> None:
        for line in _dockerfile_logical_lines(dockerfile):
            if not re.match(r"^\s*(COPY|ADD)\b", line, re.I):
                continue
            lowered = line.casefold()
            if ".." in line:
                errors.append("Dockerfile COPY/ADD cannot use parent paths")
            if any(
                re.search(
                    rf"(?:^|[/\s\[\"']){re.escape(name)}(?:[/\s\]\"']|$)",
                    lowered,
                )
                for name in PRIVILEGED_NAMES
            ):
                errors.append(f"Dockerfile may ingest privileged task material: {line.strip()}")

        private_patterns = [
            (token, re.compile(re.escape(token), re.I))
            for token in (bundle.source_path, bundle.digest)
            if token
        ]
        for path in task_dir.rglob("*"):
            if not path.is_file() or path.is_symlink():
                continue
            relative = path.relative_to(task_dir)
            if path.name.casefold() == "auth.json" or ".codex" in path.parts:
                errors.append(f"task may contain Codex credentials: {relative}")
                continue
            # task.toml legitimately records the bundle digest in its metadata.
            if path.name != "task.toml":
                for _, pattern in private_patterns:
                    if _text_file_matches(path, pattern):
                        errors.append(f"task contains private source provenance: {relative}")
                        break


def completed_task_size_bytes(task_dir: Path) -> int:
    """Sum regular-file sizes in a completed public task without following symlinks."""
    total = 0
    for root, _, files in os.walk(task_dir, followlinks=False):
        root_path = Path(root)
        for name in files:
            path = root_path / name
            if not path.is_symlink() and path.is_file():
                total += path.stat().st_size
    return total


def reward_passes(value: Any) -> bool:
    """True when every numeric reward leaf equals 1 (a full pass)."""
    leaves = list(_numeric_leaves(value))
    if not leaves:
        raise ValueError("reward contains no numeric values")
    return all(math.isclose(item, 1.0, abs_tol=1e-9) for item in leaves)


def reward_mean(value: Any) -> float:
    """Mean over numeric reward leaves; used to gate NOP free partial credit."""
    leaves = list(_numeric_leaves(value))
    if not leaves:
        raise ValueError("reward contains no numeric values")
    return sum(leaves) / len(leaves)


def _numeric_leaves(value: Any) -> Iterable[float]:
    if isinstance(value, bool):
        return
    if isinstance(value, (int, float)):
        number = float(value)
        if not math.isfinite(number):
            raise ValueError("reward values must be finite")
        yield number
    elif isinstance(value, dict):
        for item in value.values():
            yield from _numeric_leaves(item)
    elif isinstance(value, list):
        for item in value:
            yield from _numeric_leaves(item)


def _read_text(path: Path, errors: List[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"cannot read {path.name}: {exc}")
        return ""


def _text_file_matches(path: Path, pattern: re.Pattern[str]) -> bool:
    overlap = ""
    try:
        with path.open("r", encoding="utf-8") as handle:
            while chunk := handle.read(64 * 1024):
                value = overlap + chunk
                if pattern.search(value):
                    return True
                overlap = value[-256:]
    except (OSError, UnicodeDecodeError):
        return False
    return False


def _dockerfile_logical_lines(value: str) -> List[str]:
    logical: List[str] = []
    current = ""
    for line in value.splitlines():
        stripped = line.rstrip()
        current += stripped[:-1] + " " if stripped.endswith("\\") else stripped
        if not stripped.endswith("\\"):
            logical.append(current)
            current = ""
    if current:
        logical.append(current)
    return logical
