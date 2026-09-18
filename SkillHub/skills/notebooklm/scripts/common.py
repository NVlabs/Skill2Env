#!/usr/bin/env python3
"""
Shared utilities for the NotebookLM skill scripts.
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from playwright.sync_api import Error as PlaywrightError


NOTEBOOKLM_HOME_URL = "https://notebooklm.google.com/"
NOTEBOOKLM_AUTH_URL = (
    "https://accounts.google.com/v3/signin/identifier?"
    "continue=https%3A%2F%2Fnotebooklm.google.com%2F&"
    "flowName=GlifWebSignIn&flowEntry=ServiceLogin"
)

_NOTEBOOK_URL_PATTERN = re.compile(
    r"^https://notebooklm\.google\.com/notebook/[A-Za-z0-9_-]+(?:[/?#].*)?$"
)

DEFAULT_DATA_DIR = Path.home() / ".config" / "claude" / "notebooklm-skill"
PROFILE_DIR_NAME = "chrome_profile"
LIBRARY_FILE_NAME = "library.json"
SOURCE_STATE_FILE_NAME = "source_state.json"
ARTIFACTS_DIR_NAME = "artifacts"
NOTES_DIR_NAME = "notes"


def now_iso() -> str:
    """Return current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def get_data_dir() -> Path:
    """Return configured data directory."""
    override = os.environ.get("NOTEBOOKLM_DATA_DIR")
    if override:
        return Path(override).expanduser().resolve()
    return DEFAULT_DATA_DIR


def sanitize_profile_name(profile: Optional[str]) -> str:
    """Normalize profile names to safe path fragments."""
    raw = (profile or "").strip().lower()
    if not raw or raw == "default":
        return "default"
    safe = re.sub(r"[^a-z0-9_-]+", "-", raw).strip("-")
    return safe or "default"


def get_profile_dir(profile: Optional[str] = None) -> Path:
    """Return persistent browser profile directory for the selected profile."""
    normalized = sanitize_profile_name(profile)
    if normalized == "default":
        return get_data_dir() / PROFILE_DIR_NAME
    return get_data_dir() / "profiles" / normalized


def get_library_path() -> Path:
    """Return notebook library JSON path."""
    return get_data_dir() / LIBRARY_FILE_NAME


def get_source_state_path() -> Path:
    """Return source state JSON path."""
    return get_data_dir() / SOURCE_STATE_FILE_NAME


def get_artifacts_dir() -> Path:
    """Return folder where debug artifacts are written."""
    return get_data_dir() / ARTIFACTS_DIR_NAME


def get_notes_dir() -> Path:
    """Return folder for exported answers/notes."""
    return get_data_dir() / NOTES_DIR_NAME


def ensure_data_dirs() -> None:
    """Ensure data and profile directories exist."""
    data_dir = get_data_dir()
    data_dir.mkdir(parents=True, exist_ok=True)
    get_profile_dir("default").mkdir(parents=True, exist_ok=True)
    get_artifacts_dir().mkdir(parents=True, exist_ok=True)
    get_notes_dir().mkdir(parents=True, exist_ok=True)


def is_valid_notebook_url(url: str) -> bool:
    """Validate NotebookLM notebook URL format."""
    return bool(_NOTEBOOK_URL_PATTERN.match(url.strip()))


def parse_csv_values(raw: Optional[str]) -> List[str]:
    """Parse comma-separated values into a cleaned list."""
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def _default_library() -> Dict[str, Any]:
    return {
        "version": "1.0.0",
        "active_notebook_id": None,
        "notebooks": [],
        "last_modified": now_iso(),
    }


def _default_source_state() -> Dict[str, Any]:
    return {
        "version": "1.0.0",
        "notebooks": {},
        "last_modified": now_iso(),
    }


def load_library() -> Dict[str, Any]:
    """Load library from disk, creating it if needed."""
    ensure_data_dirs()
    path = get_library_path()
    if not path.exists():
        library = _default_library()
        save_library(library)
        return library

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                data.setdefault("version", "1.0.0")
                data.setdefault("active_notebook_id", None)
                data.setdefault("notebooks", [])
                data.setdefault("last_modified", now_iso())
                return data
    except (json.JSONDecodeError, OSError):
        pass

    library = _default_library()
    save_library(library)
    return library


def save_library(library: Dict[str, Any]) -> None:
    """Persist library to disk."""
    ensure_data_dirs()
    library["last_modified"] = now_iso()
    with get_library_path().open("w", encoding="utf-8") as f:
        json.dump(library, f, indent=2)


def load_source_state() -> Dict[str, Any]:
    """Load source sync/hash state from disk, creating it if needed."""
    ensure_data_dirs()
    path = get_source_state_path()
    if not path.exists():
        state = _default_source_state()
        save_source_state(state)
        return state

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                data.setdefault("version", "1.0.0")
                data.setdefault("notebooks", {})
                data.setdefault("last_modified", now_iso())
                return data
    except (json.JSONDecodeError, OSError):
        pass

    state = _default_source_state()
    save_source_state(state)
    return state


def save_source_state(state: Dict[str, Any]) -> None:
    """Persist source sync/hash state to disk."""
    ensure_data_dirs()
    state["last_modified"] = now_iso()
    with get_source_state_path().open("w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def slugify(value: str) -> str:
    """Create a stable slug ID from a string."""
    base = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not base:
        base = "notebook"
    return base[:40]


def generate_notebook_id(name: str, existing_ids: List[str]) -> str:
    """Generate a unique notebook ID from notebook name."""
    root = slugify(name)
    candidate = root
    index = 1
    existing = set(existing_ids)
    while candidate in existing:
        candidate = f"{root}-{index}"
        index += 1
    return candidate


def get_notebook_by_id(library: Dict[str, Any], notebook_id: str) -> Optional[Dict[str, Any]]:
    """Find notebook by ID."""
    for notebook in library.get("notebooks", []):
        if notebook.get("id") == notebook_id:
            return notebook
    return None


def get_notebook_by_url(library: Dict[str, Any], notebook_url: str) -> Optional[Dict[str, Any]]:
    """Find notebook by URL."""
    target = notebook_url.strip()
    for notebook in library.get("notebooks", []):
        if str(notebook.get("url", "")).strip() == target:
            return notebook
    return None


def get_active_notebook(library: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Return active notebook entry if configured."""
    active_id = library.get("active_notebook_id")
    if not active_id:
        return None
    return get_notebook_by_id(library, active_id)


def launch_persistent_context(
    playwright,
    headless: bool,
    profile: Optional[str] = None,
    viewport: Optional[Tuple[int, int]] = None,
):
    """Launch a persistent Chromium context with reusable profile directory."""
    vw, vh = viewport or (1280, 900)
    profile_dir = str(get_profile_dir(profile))
    common_args = {
        "user_data_dir": profile_dir,
        "headless": headless,
        "viewport": {"width": vw, "height": vh},
        "args": [
            "--disable-blink-features=AutomationControlled",
            "--disable-dev-shm-usage",
            "--no-first-run",
            "--no-default-browser-check",
        ],
    }
    try:
        return playwright.chromium.launch_persistent_context(channel="chrome", **common_args)
    except PlaywrightError:
        return playwright.chromium.launch_persistent_context(**common_args)


def record_notebook_use(library: Dict[str, Any], notebook_id: str) -> Optional[Dict[str, Any]]:
    """Increment usage counters for a notebook and save the library."""
    notebook = get_notebook_by_id(library, notebook_id)
    if not notebook:
        return None

    notebook["use_count"] = int(notebook.get("use_count", 0)) + 1
    notebook["last_used"] = now_iso()
    save_library(library)
    return notebook
