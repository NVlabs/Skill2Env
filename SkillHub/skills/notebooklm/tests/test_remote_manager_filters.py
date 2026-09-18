from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import remote_manager as rm  # noqa: E402


def test_parse_max_size_bytes() -> None:
    assert rm._parse_max_size_bytes("1024") == 1024
    assert rm._parse_max_size_bytes("1kb") == 1024
    assert rm._parse_max_size_bytes("2MB") == 2 * 1024 * 1024
    assert rm._parse_max_size_bytes(None) is None


@pytest.mark.parametrize("raw", ["abc", "10tb", "1.2.3mb"])
def test_parse_max_size_bytes_invalid(raw: str) -> None:
    with pytest.raises(ValueError):
        rm._parse_max_size_bytes(raw)


def test_parse_modified_since_epoch_relative() -> None:
    cutoff = rm._parse_modified_since_epoch("1d")
    assert cutoff is not None
    assert cutoff <= time.time()


def test_collect_source_files_filters(tmp_path: Path) -> None:
    keep = tmp_path / "keep.md"
    skip_ext = tmp_path / "skip.txt"
    skip_size = tmp_path / "big.md"

    keep.write_text("hello", encoding="utf-8")
    skip_ext.write_text("skip", encoding="utf-8")
    skip_size.write_text("x" * 4096, encoding="utf-8")

    files, filtered = rm._collect_source_files(
        files=None,
        dirs=[str(tmp_path)],
        recursive=False,
        include_ext_raw="md",
        exclude_patterns_raw=["skip*"],
        max_size_raw="2KB",
        modified_since_raw=None,
    )

    assert [p.name for p in files] == ["keep.md"]
    reasons = {item["reason"] for item in filtered}
    assert "extension-filtered" in reasons
    assert "size-filtered" in reasons


def test_ensure_unique_titles_detects_duplicates(tmp_path: Path) -> None:
    a_dir = tmp_path / "a"
    b_dir = tmp_path / "b"
    a_dir.mkdir()
    b_dir.mkdir()

    file_a = a_dir / "same.md"
    file_b = b_dir / "same.md"
    file_a.write_text("one", encoding="utf-8")
    file_b.write_text("two", encoding="utf-8")

    infos = [
        {
            "title": "same.md",
            "source_path": file_a,
            "upload_path": file_a,
            "size_bytes": os.path.getsize(file_a),
            "mtime_epoch": file_a.stat().st_mtime,
            "hash": "h1",
        },
        {
            "title": "same.md",
            "source_path": file_b,
            "upload_path": file_b,
            "size_bytes": os.path.getsize(file_b),
            "mtime_epoch": file_b.stat().st_mtime,
            "hash": "h2",
        },
    ]

    with pytest.raises(ValueError):
        rm._ensure_unique_titles(infos)
