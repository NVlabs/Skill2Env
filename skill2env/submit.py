# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Publish generated tasks to the Harbor hub registry."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import List, Optional, Sequence

from .task_config import validate_harbor_task_toml


class SubmitError(RuntimeError):
    """Raised when a submission step cannot proceed."""


def discover_task_dirs(paths: Sequence[Path]) -> List[Path]:
    """Resolve task directories (any directory containing task.toml).

    Each input path may be a single task directory or a corpus root that is
    scanned recursively. Results are deduplicated and sorted.
    """
    found: dict[Path, None] = {}
    for raw in paths:
        path = raw.expanduser().resolve()
        if not path.is_dir():
            raise SubmitError(f"not a directory: {path}")
        if (path / "task.toml").is_file():
            found.setdefault(path, None)
            continue
        for config in sorted(path.rglob("task.toml")):
            if config.is_file() and not config.is_symlink():
                found.setdefault(config.parent.resolve(), None)
    return list(found)


def rewrite_task_org(task_dir: Path, org: str) -> str:
    """Rewrite the org segment of task.name in task.toml; return the new name."""
    org = org.strip().strip("/")
    if not org:
        raise SubmitError("--org must be a non-empty organization name")
    path = task_dir / "task.toml"
    config = validate_harbor_task_toml(path.read_text(encoding="utf-8"))
    current = (config.task.name if config.task and config.task.name else "") or task_dir.name
    short_name = current.rsplit("/", 1)[-1]
    new_name = f"{org}/{short_name}"
    if current == new_name:
        return new_name
    updated = config.model_copy(
        update={"task": config.task.model_copy(update={"name": new_name})}
    )
    text = updated.model_dump_toml().rstrip() + "\n"
    validate_harbor_task_toml(text)
    path.write_text(text, encoding="utf-8")
    return new_name


def harbor_executable() -> str:
    executable = shutil.which("harbor")
    if executable is None:
        raise SubmitError(
            "the 'harbor' CLI is not on PATH; install the harbor package "
            "(it ships with skill2env's dependencies) or activate the project environment"
        )
    return executable


def check_auth() -> None:
    """Fail fast with a login hint when the Harbor registry session is missing."""
    executable = harbor_executable()
    try:
        result = subprocess.run(
            [executable, "auth", "status"], capture_output=True, text=True, timeout=60
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise SubmitError(f"could not check Harbor auth status: {exc}") from exc
    output = ((result.stdout or "") + (result.stderr or "")).strip()
    # Some harbor versions report "Not logged in" with a zero exit code; treat
    # both signals as unauthenticated.
    if result.returncode != 0 or "not logged in" in output.casefold():
        raise SubmitError(
            "not signed in to the Harbor registry; run 'harbor auth login' "
            "(GitHub sign-in) and retry"
        )


def publish(
    task_dirs: Sequence[Path],
    *,
    tags: Sequence[str] = (),
    public: bool = False,
    concurrency: Optional[int] = None,
) -> int:
    """Run `harbor publish` on the resolved task directories, streaming output."""
    command = [harbor_executable(), "publish", *[str(path) for path in task_dirs]]
    for tag in tags:
        command.extend(["--tag", tag])
    if public:
        command.append("--public")
    if concurrency is not None:
        command.extend(["--concurrency", str(concurrency)])
    completed = subprocess.run(command)
    return completed.returncode


def submit_tasks(
    paths: Sequence[Path],
    *,
    org: Optional[str] = None,
    tags: Sequence[str] = (),
    public: bool = False,
    concurrency: Optional[int] = None,
    dry_run: bool = False,
) -> int:
    """End-to-end submission: discover, auth preflight, optional rename, publish."""
    task_dirs = discover_task_dirs(paths)
    if not task_dirs:
        raise SubmitError("no task directories (containing task.toml) found")

    if dry_run:
        visibility = "public" if public else "private"
        print(f"Would publish {len(task_dirs)} task(s) ({visibility}):")
        for task_dir in task_dirs:
            name = _task_name(task_dir)
            renamed = f" -> {org}/{name.rsplit('/', 1)[-1]}" if org else ""
            print(f"  {name}{renamed}  [{task_dir}]")
        return 0

    check_auth()
    if org:
        for task_dir in task_dirs:
            name = rewrite_task_org(task_dir, org)
            print(f"task.name set to {name}  [{task_dir}]")
    print(f"Publishing {len(task_dirs)} task(s) to the Harbor registry...")
    return publish(task_dirs, tags=tags, public=public, concurrency=concurrency)


def _task_name(task_dir: Path) -> str:
    try:
        config = validate_harbor_task_toml(
            (task_dir / "task.toml").read_text(encoding="utf-8")
        )
    except Exception:  # noqa: BLE001 - dry-run listing must not fail hard
        return task_dir.name
    if config.task and config.task.name:
        return config.task.name
    return task_dir.name
