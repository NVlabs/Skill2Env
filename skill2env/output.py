# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Publish public tasks and retain private creator state."""

from __future__ import annotations

import json
import re
import secrets
import shutil
import string
from pathlib import Path
from typing import Any, Dict, Iterable

from .axes import AxisPreference
from .models import CreatorResult


def write_creator_state(
    state_dir: Path,
    *,
    task_name: str,
    result: CreatorResult,
    transcript: str,
    prompt: str,
    axes: AxisPreference | None = None,
) -> Path:
    """Persist private creator outputs outside the publishable task tree."""
    attempt = state_dir / "attempts" / task_name
    attempt.mkdir(parents=True, exist_ok=True)
    _write_json(attempt / "creator-result.json", result.to_dict())
    if axes is not None:
        _write_json(attempt / "axes.json", axes.to_dict())
    (attempt / "creator-transcript.jsonl").write_text(transcript, encoding="utf-8")
    (attempt / "creator-prompt.md").write_text(prompt + "\n", encoding="utf-8")
    return attempt


def publish_task(*, candidate: Path, output_dir: Path, task_name: str) -> Path:
    """Atomically copy a checked candidate into the corpus."""
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / task_name
    staging = output_dir / f".{task_name}.tmp"
    if destination.exists():
        raise FileExistsError(f"task already exists: {destination}")
    if staging.exists():
        shutil.rmtree(staging)
    shutil.copytree(candidate, staging, symlinks=True)
    staging.rename(destination)
    return destination


def write_corpus_manifest(output_dir: Path, attempts: Iterable[Dict[str, Any]]) -> Path:
    """Write the one compact public manifest for this corpus root."""
    root = output_dir.expanduser().resolve()
    entries = []
    for raw in attempts:
        entry = {
            key: raw.get(key)
            for key in ("task_name", "variant", "status", "reason_code", "path", "digest", "axes")
        }
        path = raw.get("path")
        if isinstance(path, str) and path:
            candidate = Path(path).expanduser().resolve()
            try:
                entry["path"] = candidate.relative_to(root).as_posix()
            except ValueError:
                entry["path"] = None
        entries.append(entry)
    path = root / "_corpus_manifest.json"
    _write_json(path, {"schema_version": "1.0", "attempts": entries})
    return path


def append_jsonl(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def safe_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "skill"


def format_task_name(skill_id: str) -> str:
    """Return a unique task directory / package short name for a Skill."""
    suffix = "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(8))
    return f"task_{safe_name(skill_id)}_{suffix}"


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
