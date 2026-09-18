# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Load complete Agent Skill directories with stable provenance and no size policy."""

from __future__ import annotations

import codecs
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

from .models import ContractError, FileRecord, SkillBundle


ENTRY_DOCUMENTS = ("SKILL.md", "AGENTS.md", "skill-card.md")


class BundleError(ContractError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def load_skill_bundle(skill_path: Path) -> SkillBundle:
    """Inventory one directly supplied Agent Skill directory."""
    skill_root = skill_path.expanduser().resolve()
    if not skill_root.is_dir():
        raise BundleError("skill_not_found", f"skill directory not found: {skill_root}")

    entry_document = _find_entry_document(skill_root)
    records: List[FileRecord] = []
    aggregate = hashlib.sha256()

    for file_path in _walk_files(skill_root):
        relative = file_path.relative_to(skill_root).as_posix()
        if file_path.is_symlink():
            try:
                resolved = file_path.resolve()
                resolved.relative_to(skill_root)
            except (OSError, RuntimeError, ValueError) as exc:
                raise BundleError(
                    "symlink_escape", f"unsafe or escaping skill symlink: {relative}"
                ) from exc
        try:
            size, digest, kind, line_count = _inspect_file(file_path)
        except OSError as exc:
            raise BundleError("file_unreadable", f"cannot read {relative}: {exc}") from exc
        aggregate.update(relative.encode("utf-8"))
        aggregate.update(b"\0")
        aggregate.update(bytes.fromhex(digest))
        records.append(FileRecord(relative, size, digest, kind, line_count))

    entry_rel = entry_document.relative_to(skill_root).as_posix()
    entry_record = next((record for record in records if record.path == entry_rel), None)
    if entry_record is None or entry_record.kind != "text":
        raise BundleError("entry_not_text", f"entry document is not UTF-8 text: {entry_rel}")

    try:
        metadata = _parse_frontmatter_file(entry_document)
    except (OSError, UnicodeDecodeError) as exc:
        raise BundleError("entry_not_text", f"cannot read entry document {entry_rel}: {exc}") from exc
    skill_id = str(metadata.get("name") or skill_root.name or "skill").strip()
    if not skill_id:
        skill_id = skill_root.name or "skill"
    return SkillBundle(
        id=skill_id,
        provider="local",
        source_path=str(skill_root),
        root=skill_root,
        entry_document=entry_rel,
        name=skill_id,
        description=str(metadata.get("description") or "").strip(),
        license=_normalise_license(metadata.get("license")),
        files=records,
        digest=aggregate.hexdigest(),
    )


def _find_entry_document(root: Path) -> Path:
    for name in ENTRY_DOCUMENTS:
        candidate = root / name
        if candidate.is_file():
            return candidate
    for name in ENTRY_DOCUMENTS:
        matches = sorted(root.rglob(name))
        if matches:
            return matches[0]
    raise BundleError("entry_missing", f"no supported entry document under {root}")


def _walk_files(root: Path) -> List[Path]:
    paths: List[Path] = []
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        kept_dirs: List[str] = []
        for name in sorted(dirs):
            candidate = current_path / name
            if candidate.is_symlink():
                try:
                    candidate.resolve().relative_to(root)
                except (OSError, RuntimeError, ValueError) as exc:
                    relative = candidate.relative_to(root).as_posix()
                    raise BundleError(
                        "symlink_escape", f"unsafe or escaping skill symlink: {relative}"
                    ) from exc
                # Internal directory symlinks are not followed: the canonical
                # directory is inventoried once and cycles are impossible.
                continue
            kept_dirs.append(name)
        dirs[:] = kept_dirs
        for name in sorted(files):
            paths.append(current_path / name)
    return sorted(paths, key=lambda path: path.relative_to(root).as_posix())


def _inspect_file(path: Path) -> Tuple[int, str, str, int]:
    """Hash and classify a file incrementally so large assets need not be buffered."""
    digest = hashlib.sha256()
    decoder = codecs.getincrementaldecoder("utf-8")()
    size = 0
    is_text = True
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            size += len(chunk)
            digest.update(chunk)
            if b"\x00" in chunk:
                is_text = False
            if is_text:
                try:
                    decoder.decode(chunk)
                except UnicodeDecodeError:
                    is_text = False
        if is_text:
            try:
                decoder.decode(b"", final=True)
            except UnicodeDecodeError:
                is_text = False

    line_count = 0
    if is_text:
        with path.open("r", encoding="utf-8", newline=None) as handle:
            line_count = sum(1 for _ in handle)
    return size, digest.hexdigest(), "text" if is_text else "binary", line_count


def _parse_frontmatter_file(path: Path) -> Dict[str, Any]:
    lines: List[str] = []
    with path.open("r", encoding="utf-8") as handle:
        if handle.readline().strip() != "---":
            return {}
        for line in handle:
            if line.strip() == "---":
                break
            lines.append(line)
        else:
            return {}
    try:
        parsed = yaml.safe_load("".join(lines)) or {}
    except yaml.YAMLError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _normalise_license(value: Any) -> str:
    if value is None:
        return "unknown"
    if isinstance(value, str):
        return value.strip() or "unknown"
    return json.dumps(value, sort_keys=True, ensure_ascii=False)
