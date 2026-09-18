#!/usr/bin/env python3
"""
Remote NotebookLM operations via browser automation.

Supports:
- list all notebooks visible in account
- create new notebook
- list/add/delete/sync sources in a notebook
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import shutil
import sys
import tempfile
import time
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Page, sync_playwright

from common import (
    NOTEBOOKLM_HOME_URL,
    generate_notebook_id,
    get_active_notebook,
    get_artifacts_dir,
    get_notebook_by_id,
    get_notebook_by_url,
    is_valid_notebook_url,
    launch_persistent_context,
    load_library,
    load_source_state,
    now_iso,
    parse_csv_values,
    sanitize_profile_name,
    save_library,
    save_source_state,
)

NOTEBOOK_ID_PATTERN = re.compile(r"project-([0-9a-fA-F-]{36})-title")
RETRYABLE_ERROR_KEYWORDS = [
    "timeout",
    "timed out",
    "net::",
    "connection",
    "target closed",
    "page crashed",
    "execution context was destroyed",
    "context closed",
    "protocol error",
    "browser has been closed",
    "closed",
]


def _safe_name(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", value).strip("-") or "item"


def _command_attempts(args) -> int:
    retries = int(getattr(args, "retries", 1) or 1)
    return max(1, retries)


def _is_retryable_error(message: str) -> bool:
    lower = message.lower().strip()
    return any(keyword in lower for keyword in RETRYABLE_ERROR_KEYWORDS)


def _artifact_dir_for_args(args) -> Path:
    raw = getattr(args, "artifacts_dir", None)
    if raw:
        return Path(raw).expanduser().resolve()
    return get_artifacts_dir()


def _capture_debug_artifacts(page: Page, args, command_name: str, attempt: int, error_message: str) -> Optional[Dict]:
    try:
        artifact_dir = _artifact_dir_for_args(args)
        artifact_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        prefix = f"{stamp}-{_safe_name(command_name)}-attempt{attempt}"
        screenshot_path = artifact_dir / f"{prefix}.png"
        html_path = artifact_dir / f"{prefix}.html"

        page.screenshot(path=str(screenshot_path), full_page=True)
        html_path.write_text(page.content(), encoding="utf-8")

        return {
            "attempt": attempt,
            "error": error_message,
            "url": page.url,
            "screenshot": str(screenshot_path),
            "html": str(html_path),
        }
    except Exception:  # noqa: BLE001
        return None


def _run_browser_command(args, command_name: str, action: Callable[[Page], Dict]) -> Dict:
    attempts = _command_attempts(args)
    profile = sanitize_profile_name(getattr(args, "profile", "default"))
    errors: List[str] = []
    artifacts: List[Dict] = []

    for attempt in range(1, attempts + 1):
        with sync_playwright() as p:
            context = launch_persistent_context(
                p,
                headless=not getattr(args, "show_browser", False),
                profile=profile,
                viewport=(1600, 1100),
            )
            page = context.new_page()
            try:
                result = action(page)
                if isinstance(result, dict) and result.get("error"):
                    error_message = str(result["error"])
                    if attempt < attempts and _is_retryable_error(error_message):
                        errors.append(error_message)
                        artifact = _capture_debug_artifacts(page, args, command_name, attempt, error_message)
                        if artifact:
                            artifacts.append(artifact)
                        time.sleep(min(attempt * 1.5, 5.0))
                        continue

                    if errors:
                        result = dict(result)
                        result.setdefault("previous_errors", errors)
                    if artifacts:
                        result = dict(result)
                        result.setdefault("artifacts", artifacts)
                    if attempt > 1:
                        result = dict(result)
                        result.setdefault("attempts", attempt)
                    return result

                if isinstance(result, dict):
                    if errors:
                        result = dict(result)
                        result.setdefault("previous_errors", errors)
                    if artifacts:
                        result = dict(result)
                        result.setdefault("artifacts", artifacts)
                    if attempt > 1:
                        result = dict(result)
                        result.setdefault("attempts", attempt)
                return result
            except Exception as exc:  # noqa: BLE001
                error_message = str(exc)
                errors.append(error_message)
                artifact = _capture_debug_artifacts(page, args, command_name, attempt, error_message)
                if artifact:
                    artifacts.append(artifact)
                if attempt >= attempts:
                    result = {
                        "error": f"{command_name} failed after {attempts} attempts: {error_message}",
                        "errors": errors,
                        "attempts": attempts,
                    }
                    if artifacts:
                        result["artifacts"] = artifacts
                    return result
                time.sleep(min(attempt * 1.5, 5.0))
            finally:
                context.close()

    # Unreachable, keeps mypy/linters happy.
    return {"error": f"{command_name} failed unexpectedly"}


def _wait_for(condition_fn, timeout_sec: int = 30, poll_ms: int = 400) -> bool:
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        if condition_fn():
            return True
        time.sleep(poll_ms / 1000.0)
    return False


def _ensure_logged_in(page: Page) -> Optional[Dict]:
    if "accounts.google.com" in page.url:
        return {
            "error": (
                "NotebookLM redirected to Google login. "
                "Run: python scripts/auth_manager.py setup"
            )
        }
    return None


def _go_to_home(page: Page) -> Optional[Dict]:
    page.goto(NOTEBOOKLM_HOME_URL, wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(2500)
    return _ensure_logged_in(page)


def _scroll_notebook_home(page: Page) -> None:
    stable_rounds = 0
    last_count = -1
    for _ in range(14):
        count = page.locator(
            "mat-card.project-button-card:not(.featured-project-card):not(.create-new-action-button)"
        ).count()
        if count == last_count:
            stable_rounds += 1
        else:
            stable_rounds = 0
        last_count = count
        if stable_rounds >= 3:
            break
        try:
            page.mouse.wheel(0, 3200)
        except PlaywrightError:
            pass
        page.wait_for_timeout(450)


def _parse_notebook_card(card) -> Optional[Dict]:
    try:
        title_el = card.query_selector(".project-button-title")
        subtitle_el = card.query_selector(".project-button-subtitle")
        button_el = card.query_selector("button.primary-action-button")

        title = title_el.inner_text().strip() if title_el else card.inner_text().split("\n")[0].strip()
        subtitle = subtitle_el.inner_text().strip() if subtitle_el else ""
        button_aria = button_el.get_attribute("aria-labelledby") if button_el else ""
        card_html = card.evaluate("e => e.outerHTML")

        notebook_id = None
        for haystack in [button_aria or "", card_html or ""]:
            match = NOTEBOOK_ID_PATTERN.search(haystack)
            if match:
                notebook_id = match.group(1)
                break

        source_count = None
        source_match = re.search(r"(\d+)\s+sources?", subtitle.lower())
        if source_match:
            source_count = int(source_match.group(1))

        is_public = "public" in card.inner_text().lower().split()

        return {
            "id": notebook_id,
            "url": f"https://notebooklm.google.com/notebook/{notebook_id}" if notebook_id else None,
            "name": title,
            "subtitle": subtitle,
            "source_count": source_count,
            "is_public": is_public,
        }
    except PlaywrightError:
        return None


def _list_remote_notebooks(page: Page) -> List[Dict]:
    # Ensure personal notebooks are visible.
    try:
        my_notebooks_toggle = page.get_by_role("button", name="My notebooks")
        if my_notebooks_toggle.count() > 0:
            my_notebooks_toggle.first.click()
            page.wait_for_timeout(1200)
    except PlaywrightError:
        pass

    _scroll_notebook_home(page)

    cards = page.query_selector_all(
        "mat-card.project-button-card:not(.featured-project-card):not(.create-new-action-button)"
    )
    notebooks: List[Dict] = []
    seen: set[str] = set()
    for card in cards:
        data = _parse_notebook_card(card)
        if not data:
            continue
        key = str(data.get("id") or data.get("name") or "").strip()
        if not key or key in seen:
            continue
        seen.add(key)
        notebooks.append(data)
    return notebooks


def _resolve_notebook_for_ops(args) -> Dict:
    library = load_library()
    notebook_url = args.notebook_url
    notebook_id = None

    if notebook_url:
        if not is_valid_notebook_url(notebook_url):
            return {"error": "Invalid --notebook-url format"}
        notebook = get_notebook_by_url(library, notebook_url)
        if notebook:
            notebook_id = notebook.get("id")
    elif args.notebook_id:
        notebook = get_notebook_by_id(library, args.notebook_id)
        if not notebook:
            return {"error": f"Notebook not found in library: {args.notebook_id}"}
        notebook_id = notebook.get("id")
        notebook_url = notebook.get("url")
    else:
        active = get_active_notebook(library)
        if not active:
            return {
                "error": (
                    "No notebook specified and no active notebook configured. "
                    "Use --notebook-url, --notebook-id, or activate a notebook first."
                )
            }
        notebook_id = active.get("id")
        notebook_url = active.get("url")

    if not notebook_url:
        return {"error": "Failed to resolve notebook URL"}

    return {"library": library, "notebook_id": notebook_id, "notebook_url": notebook_url}


def _ensure_source_panel_open(page: Page) -> None:
    try:
        expand = page.locator("button[aria-label='Expand source panel']")
        if expand.count() > 0 and expand.first.is_visible():
            expand.first.click()
            page.wait_for_timeout(700)
    except PlaywrightError:
        pass


def _dismiss_blocking_overlays(page: Page) -> None:
    # Handles transient NotebookLM modals/backdrops that can block pointer events.
    for _ in range(4):
        try:
            backdrop = page.locator(".cdk-overlay-backdrop.cdk-overlay-backdrop-showing")
            if backdrop.count() == 0:
                break
        except PlaywrightError:
            break

        for label in ["Close", "Cancel", "Done", "Not now", "Got it"]:
            try:
                btn = page.get_by_role("button", name=label)
                if btn.count() > 0 and btn.first.is_visible():
                    btn.first.click(timeout=1200)
                    page.wait_for_timeout(350)
                    break
            except PlaywrightError:
                continue

        try:
            page.keyboard.press("Escape")
        except PlaywrightError:
            pass
        page.wait_for_timeout(400)


def _read_sources(page: Page) -> List[Dict]:
    rows = page.query_selector_all(".single-source-container")
    results: List[Dict] = []
    for row in rows:
        try:
            title_el = row.query_selector(".source-title")
            if not title_el:
                continue
            title = title_el.inner_text().strip()
            if not title:
                continue
            icon_el = row.query_selector(".source-item-source-icon")
            source_type = icon_el.inner_text().strip() if icon_el else None
            menu_btn = row.query_selector("button.source-item-more-button")
            menu_btn_id = menu_btn.get_attribute("id") if menu_btn else None
            source_id = None
            if menu_btn_id:
                match = re.search(r"source-item-more-button-(.+)$", menu_btn_id)
                if match:
                    source_id = match.group(1)
            results.append(
                {
                    "title": title,
                    "type": source_type,
                    "source_id": source_id,
                }
            )
        except PlaywrightError:
            continue
    return results


def _wait_for_source_diff(page: Page, before_titles: List[str], timeout_sec: int = 120) -> List[str]:
    before_counter = Counter(before_titles)
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        current = _read_sources(page)
        current_titles = [src["title"] for src in current]
        cur_counter = Counter(current_titles)
        diff_counter = cur_counter - before_counter
        added = list(diff_counter.elements())
        if added:
            return added
        page.wait_for_timeout(800)
    return []


def _open_add_sources_dialog(page: Page) -> None:
    _dismiss_blocking_overlays(page)

    dialog = page.locator("add-sources-dialog")
    if dialog.count() == 0:
        add_btn = page.locator("button[aria-label='Add source']")
        if add_btn.count() == 0:
            add_btn = page.get_by_role("button", name="Add source")
        if add_btn.count() == 0:
            raise RuntimeError("Could not find 'Add source' button in notebook")

        add_btn.first.click()
        page.wait_for_timeout(900)
        dialog = page.locator("add-sources-dialog")

    if dialog.count() == 0:
        _dismiss_blocking_overlays(page)
        dialog = page.locator("add-sources-dialog")
        if dialog.count() == 0:
            raise RuntimeError("Add sources dialog did not open")


def _insert_text_source(page: Page, text: str) -> None:
    _open_add_sources_dialog(page)
    page.get_by_role("button", name="Copied text").click()
    page.wait_for_timeout(500)
    textarea = page.locator("textarea[placeholder='Paste text here']").first
    if textarea.count() == 0:
        raise RuntimeError("Could not find copied text textarea")
    textarea.fill(text)

    insert_btn = page.locator("mat-dialog-container button", has_text="Insert").first
    ready = _wait_for(
        lambda: insert_btn.count() > 0 and not insert_btn.is_disabled(),
        timeout_sec=25,
        poll_ms=350,
    )
    if not ready:
        raise RuntimeError("Insert button did not become ready. Check provided source content.")
    insert_btn.click()


def _insert_url_source(page: Page, url: str) -> None:
    _open_add_sources_dialog(page)
    page.get_by_role("button", name="Websites").click()
    page.wait_for_timeout(500)
    textarea = page.locator("textarea[placeholder='Paste any links']").first
    if textarea.count() == 0:
        raise RuntimeError("Could not find website URL textarea")
    textarea.fill(url)

    insert_btn = page.locator("mat-dialog-container button", has_text="Insert").first
    ready = _wait_for(
        lambda: insert_btn.count() > 0 and not insert_btn.is_disabled(),
        timeout_sec=25,
        poll_ms=350,
    )
    if not ready:
        raise RuntimeError("Insert button did not become ready. Check provided URL source.")
    insert_btn.click()


def _upload_file_sources(page: Page, files: List[Path]) -> None:
    if not files:
        return
    _open_add_sources_dialog(page)
    upload_btn = page.get_by_role("button", name="Upload files")
    if upload_btn.count() == 0:
        raise RuntimeError("Could not find 'Upload files' button in add sources dialog")

    with page.expect_file_chooser(timeout=25000) as chooser_info:
        upload_btn.first.click()
    chooser = chooser_info.value
    chooser.set_files([str(path) for path in files])


def _find_matching_source_indexes(sources: List[Dict], title: str, contains: bool) -> List[int]:
    matches: List[int] = []
    wanted = title.lower().strip()
    for idx, src in enumerate(sources):
        current = str(src.get("title", "")).lower().strip()
        if contains:
            if wanted in current:
                matches.append(idx)
        else:
            if wanted == current:
                matches.append(idx)
    return matches


def _delete_source_once(page: Page, row_index: int) -> None:
    row = page.locator(".single-source-container").nth(row_index)
    row.scroll_into_view_if_needed()
    row.locator("button.source-item-more-button").click(timeout=7000)
    page.wait_for_timeout(400)

    delete_menu = page.locator("button.more-menu-delete-source-button")
    if delete_menu.count() == 0:
        page.get_by_role("menuitem", name="Remove source").first.click(timeout=7000)
    else:
        delete_menu.first.click(timeout=7000)
    page.wait_for_timeout(500)

    # Confirm modal.
    if page.locator("mat-dialog-container").count() > 0:
        confirm = page.locator("button[aria-label='Confirm deletion']")
        if confirm.count() > 0:
            confirm.first.click(timeout=7000)
        else:
            submit = page.locator("button.submit")
            if submit.count() > 0:
                submit.first.click(timeout=7000)
            else:
                page.get_by_role("button", name="Delete").first.click(timeout=7000)
    page.wait_for_timeout(1300)


def _delete_all_exact_title(page: Page, title: str, max_delete: int = 40) -> int:
    removed = 0
    for _ in range(max_delete):
        current_sources = _read_sources(page)
        current_indexes = _find_matching_source_indexes(current_sources, title, contains=False)
        if not current_indexes:
            break
        _delete_source_once(page, current_indexes[0])
        _wait_for(
            lambda: len(_find_matching_source_indexes(_read_sources(page), title, contains=False))
            < len(current_indexes),
            timeout_sec=35,
            poll_ms=500,
        )
        removed += 1
    return removed


def _upsert_library_notebook(url: str, name: str, description: str, topics: List[str]) -> Dict:
    library = load_library()
    existing = get_notebook_by_url(library, url)
    if existing:
        existing["name"] = name
        existing["description"] = description
        existing["topics"] = topics
        existing["last_used"] = now_iso()
        save_library(library)
        return existing

    notebooks = library.get("notebooks", [])
    existing_ids = [n.get("id", "") for n in notebooks]
    notebook_id = generate_notebook_id(name, existing_ids)
    notebook = {
        "id": notebook_id,
        "url": url,
        "name": name,
        "description": description,
        "topics": topics,
        "tags": [],
        "added_at": now_iso(),
        "last_used": now_iso(),
        "use_count": 0,
    }
    notebooks.append(notebook)
    if not library.get("active_notebook_id"):
        library["active_notebook_id"] = notebook_id
    save_library(library)
    return notebook


def _parse_max_size_bytes(raw: Optional[str]) -> Optional[int]:
    if not raw:
        return None
    text = raw.strip().lower()
    match = re.match(r"^(\d+(?:\.\d+)?)\s*(b|kb|mb|gb)?$", text)
    if not match:
        raise ValueError(f"Invalid --max-size value: {raw}")
    number = float(match.group(1))
    unit = (match.group(2) or "b").lower()
    multiplier = {
        "b": 1,
        "kb": 1024,
        "mb": 1024**2,
        "gb": 1024**3,
    }[unit]
    return int(number * multiplier)


def _parse_modified_since_epoch(raw: Optional[str]) -> Optional[float]:
    if not raw:
        return None

    value = raw.strip()
    rel_match = re.match(r"^(\d+)\s*([dhm])$", value.lower())
    if rel_match:
        amount = int(rel_match.group(1))
        unit = rel_match.group(2)
        now = datetime.now(timezone.utc)
        if unit == "d":
            cutoff = now - timedelta(days=amount)
        elif unit == "h":
            cutoff = now - timedelta(hours=amount)
        else:
            cutoff = now - timedelta(minutes=amount)
        return cutoff.timestamp()

    normalized = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(
            "Invalid --modified-since format. Use ISO datetime/date or relative values like 7d, 24h, 90m"
        ) from exc

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.timestamp()


def _parse_exclude_patterns(raw_values: Optional[List[str]]) -> List[str]:
    patterns: List[str] = []
    for raw in raw_values or []:
        parts = parse_csv_values(raw)
        if parts:
            patterns.extend(parts)
        else:
            stripped = raw.strip()
            if stripped:
                patterns.append(stripped)
    return patterns


def _parse_include_extensions(raw: Optional[str]) -> set[str]:
    exts: set[str] = set()
    for value in parse_csv_values(raw):
        ext = value.lower().strip()
        if not ext:
            continue
        if not ext.startswith("."):
            ext = f".{ext}"
        exts.add(ext)
    return exts


def _collect_source_files(
    files: Optional[List[str]],
    dirs: Optional[List[str]],
    recursive: bool,
    include_ext_raw: Optional[str],
    exclude_patterns_raw: Optional[List[str]],
    max_size_raw: Optional[str],
    modified_since_raw: Optional[str],
) -> Tuple[List[Path], List[Dict]]:
    include_ext = _parse_include_extensions(include_ext_raw)
    exclude_patterns = _parse_exclude_patterns(exclude_patterns_raw)
    max_size = _parse_max_size_bytes(max_size_raw)
    modified_since = _parse_modified_since_epoch(modified_since_raw)

    candidates: List[Path] = []
    for raw in files or []:
        path = Path(raw).expanduser().resolve()
        if not path.exists():
            raise ValueError(f"File not found: {path}")
        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")
        candidates.append(path)

    for raw in dirs or []:
        dir_path = Path(raw).expanduser().resolve()
        if not dir_path.exists():
            raise ValueError(f"Directory not found: {dir_path}")
        if not dir_path.is_dir():
            raise ValueError(f"Path is not a directory: {dir_path}")
        iterator = dir_path.rglob("*") if recursive else dir_path.iterdir()
        for candidate in iterator:
            try:
                if candidate.is_file():
                    candidates.append(candidate.resolve())
            except OSError:
                continue

    deduped: List[Path] = []
    seen_paths: set[str] = set()
    filtered_out: List[Dict] = []

    for path in candidates:
        key = str(path)
        if key in seen_paths:
            filtered_out.append({"path": key, "reason": "duplicate-path"})
            continue
        seen_paths.add(key)

        try:
            stat = path.stat()
        except OSError:
            filtered_out.append({"path": key, "reason": "stat-failed"})
            continue

        if include_ext and path.suffix.lower() not in include_ext:
            filtered_out.append(
                {
                    "path": key,
                    "reason": "extension-filtered",
                    "allowed_extensions": sorted(include_ext),
                }
            )
            continue

        excluded = False
        for pattern in exclude_patterns:
            if fnmatch.fnmatch(path.name, pattern) or fnmatch.fnmatch(key, pattern):
                filtered_out.append({"path": key, "reason": f"excluded:{pattern}"})
                excluded = True
                break
        if excluded:
            continue

        if max_size is not None and stat.st_size > max_size:
            filtered_out.append(
                {
                    "path": key,
                    "reason": "size-filtered",
                    "size_bytes": stat.st_size,
                    "max_size_bytes": max_size,
                }
            )
            continue

        if modified_since is not None and stat.st_mtime < modified_since:
            filtered_out.append(
                {
                    "path": key,
                    "reason": "modified-since-filtered",
                    "mtime_epoch": stat.st_mtime,
                }
            )
            continue

        deduped.append(path)

    deduped.sort(key=lambda p: str(p).lower())
    return deduped, filtered_out


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _make_file_infos(paths: List[Path]) -> List[Dict]:
    infos: List[Dict] = []
    for path in paths:
        stat = path.stat()
        infos.append(
            {
                "title": path.name,
                "source_path": path,
                "upload_path": path,
                "size_bytes": stat.st_size,
                "mtime_epoch": stat.st_mtime,
                "hash": _hash_file(path),
            }
        )
    return infos


def _ensure_unique_titles(file_infos: List[Dict]) -> None:
    title_to_paths: Dict[str, List[str]] = {}
    for info in file_infos:
        title_to_paths.setdefault(info["title"], []).append(str(info["source_path"]))

    duplicates = {title: paths for title, paths in title_to_paths.items() if len(paths) > 1}
    if duplicates:
        details = "; ".join(f"{title}: {', '.join(paths)}" for title, paths in duplicates.items())
        raise ValueError(f"Duplicate filenames detected. Rename files to unique names before upload: {details}")


def _copy_infos_to_temp(file_infos: List[Dict]) -> Tuple[List[Dict], Optional[Path]]:
    if not file_infos:
        return file_infos, None

    temp_dir = Path(tempfile.mkdtemp(prefix="notebooklm-upload-"))
    copied_infos: List[Dict] = []
    for info in file_infos:
        src = info["source_path"]
        dst = temp_dir / src.name
        shutil.copy2(src, dst)
        cloned = dict(info)
        cloned["upload_path"] = dst
        copied_infos.append(cloned)
    return copied_infos, temp_dir


def _notebook_state_key(notebook_url: str) -> str:
    return notebook_url.strip()


def _get_notebook_state_sources(state: Dict, notebook_url: str) -> Dict[str, Dict]:
    notebooks = state.setdefault("notebooks", {})
    key = _notebook_state_key(notebook_url)
    notebook_entry = notebooks.setdefault(key, {"sources": {}, "updated_at": now_iso()})
    notebook_entry.setdefault("sources", {})
    return notebook_entry["sources"]


def _update_notebook_state_hashes(state: Dict, notebook_url: str, file_infos: List[Dict]) -> None:
    sources = _get_notebook_state_sources(state, notebook_url)
    for info in file_infos:
        sources[info["title"]] = {
            "hash": info["hash"],
            "size_bytes": info["size_bytes"],
            "mtime_epoch": info["mtime_epoch"],
            "source_path": str(info["source_path"]),
            "updated_at": now_iso(),
        }
    key = _notebook_state_key(notebook_url)
    state.setdefault("notebooks", {}).setdefault(key, {}).update({"updated_at": now_iso()})


def _remove_notebook_state_titles(state: Dict, notebook_url: str, titles: List[str]) -> None:
    sources = _get_notebook_state_sources(state, notebook_url)
    for title in titles:
        sources.pop(title, None)
    key = _notebook_state_key(notebook_url)
    state.setdefault("notebooks", {}).setdefault(key, {}).update({"updated_at": now_iso()})


def _read_manifest_paths(manifest_path: Path) -> List[str]:
    if not manifest_path.exists():
        raise ValueError(f"Manifest file not found: {manifest_path}")
    text = manifest_path.read_text(encoding="utf-8")

    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        payload = None

    if isinstance(payload, list):
        return [str(item).strip() for item in payload if str(item).strip()]
    if isinstance(payload, dict) and isinstance(payload.get("files"), list):
        return [str(item).strip() for item in payload["files"] if str(item).strip()]

    paths: List[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        paths.append(stripped)
    return paths


def cmd_list_remote_notebooks(args) -> Dict:
    def action(page: Page) -> Dict:
        auth_err = _go_to_home(page)
        if auth_err:
            return auth_err

        notebooks = _list_remote_notebooks(page)
        return {
            "status": "success",
            "count": len(notebooks),
            "notebooks": notebooks,
        }

    return _run_browser_command(args, "list-remote", action)


def cmd_create_remote_notebook(args) -> Dict:
    if args.dry_run:
        return {
            "status": "dry-run",
            "operation": "create-remote",
            "name": args.name,
            "skip_library": bool(args.skip_library),
            "description": args.description,
            "topics": parse_csv_values(args.topics),
            "profile": sanitize_profile_name(args.profile),
        }

    def action(page: Page) -> Dict:
        auth_err = _go_to_home(page)
        if auth_err:
            return auth_err

        clicked = False
        selectors = [
            "button[aria-label='Create new notebook']",
            "mat-card.create-new-action-button button.primary-action-button",
            "mat-card.create-new-action-button",
            "button[aria-label='Create notebook']",
        ]
        for selector in selectors:
            try:
                loc = page.locator(selector)
                if loc.count() > 0 and loc.first.is_visible():
                    loc.first.click()
                    clicked = True
                    break
            except PlaywrightError:
                continue

        if not clicked:
            return {"error": "Could not find create notebook button on NotebookLM home page"}

        created = _wait_for(lambda: "/notebook/" in page.url and "accounts.google.com" not in page.url, timeout_sec=45)
        if not created:
            return {"error": "Timed out waiting for new notebook creation"}

        page.wait_for_timeout(2000)
        notebook_url = page.url.split("?")[0]
        id_match = re.search(r"/notebook/([0-9a-fA-F-]+)", notebook_url)
        notebook_remote_id = id_match.group(1) if id_match else None

        # Set title if requested.
        try:
            title_input = page.locator("input.title-input").first
            if title_input.is_visible():
                title_input.click()
                try:
                    page.keyboard.press("Meta+A")
                except PlaywrightError:
                    page.keyboard.press("Control+A")
                title_input.fill(args.name)
                page.keyboard.press("Enter")
                page.wait_for_timeout(1000)
        except PlaywrightError:
            pass

        name = args.name
        try:
            title_input = page.locator("input.title-input").first
            if title_input.count() > 0:
                name = title_input.input_value().strip() or args.name
        except PlaywrightError:
            pass

        result: Dict = {
            "status": "success",
            "notebook": {
                "remote_id": notebook_remote_id,
                "url": notebook_url,
                "name": name,
            },
        }

        if not args.skip_library:
            topics = parse_csv_values(args.topics) or ["notebooklm"]
            description = (
                args.description.strip()
                if args.description
                else "Notebook created through NotebookLM remote manager"
            )
            library_entry = _upsert_library_notebook(
                url=notebook_url,
                name=name,
                description=description,
                topics=topics,
            )
            result["library_notebook"] = library_entry

        return result

    return _run_browser_command(args, "create-remote", action)


def cmd_list_sources(args) -> Dict:
    resolved = _resolve_notebook_for_ops(args)
    if resolved.get("error"):
        return {"error": resolved["error"]}

    def action(page: Page) -> Dict:
        page.goto(resolved["notebook_url"], wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(2500)
        auth_err = _ensure_logged_in(page)
        if auth_err:
            return auth_err
        _ensure_source_panel_open(page)
        sources = _read_sources(page)
        return {
            "status": "success",
            "notebook_url": resolved["notebook_url"],
            "notebook_id": resolved.get("notebook_id"),
            "count": len(sources),
            "sources": sources,
        }

    return _run_browser_command(args, "list-sources", action)


def cmd_add_source(args) -> Dict:
    resolved = _resolve_notebook_for_ops(args)
    if resolved.get("error"):
        return {"error": resolved["error"]}

    source_modes = [bool(args.text), bool(args.url), bool(args.file), bool(args.dir)]
    if sum(1 for mode in source_modes if mode) != 1:
        return {"error": "Provide exactly one source type: --text, --url, --file, or --dir"}

    if args.text and args.dry_run:
        return {
            "status": "dry-run",
            "operation": "add-source",
            "source_type": "text",
            "notebook_url": resolved["notebook_url"],
            "preview_chars": len(args.text),
        }

    if args.url and args.dry_run:
        return {
            "status": "dry-run",
            "operation": "add-source",
            "source_type": "url",
            "notebook_url": resolved["notebook_url"],
            "url": args.url,
        }

    file_infos: List[Dict] = []
    filtered_out: List[Dict] = []
    temp_dir_path: Optional[Path] = None

    if args.file or args.dir:
        try:
            resolved_files, filtered_out = _collect_source_files(
                files=args.file,
                dirs=args.dir,
                recursive=bool(args.recursive),
                include_ext_raw=args.include_ext,
                exclude_patterns_raw=args.exclude,
                max_size_raw=args.max_size,
                modified_since_raw=args.modified_since,
            )
        except ValueError as exc:
            return {"error": str(exc)}

        if not resolved_files:
            return {
                "error": "No files found to upload from provided --file/--dir input",
                "filtered_out": filtered_out,
            }

        file_infos = _make_file_infos(resolved_files)
        try:
            _ensure_unique_titles(file_infos)
        except ValueError as exc:
            return {"error": str(exc), "filtered_out": filtered_out}

        if args.copy_to_temp:
            file_infos, temp_dir_path = _copy_infos_to_temp(file_infos)

        if args.dry_run:
            return {
                "status": "dry-run",
                "operation": "add-source",
                "source_type": "files",
                "notebook_url": resolved["notebook_url"],
                "candidate_count": len(file_infos),
                "filtered_out": filtered_out,
                "files": [
                    {
                        "title": info["title"],
                        "source_path": str(info["source_path"]),
                        "upload_path": str(info["upload_path"]),
                        "size_bytes": info["size_bytes"],
                    }
                    for info in file_infos
                ],
            }

    state = load_source_state()
    state_sources = _get_notebook_state_sources(state, resolved["notebook_url"])

    try:
        def action(page: Page) -> Dict:
            page.goto(resolved["notebook_url"], wait_until="domcontentloaded", timeout=120000)
            page.wait_for_timeout(2500)
            auth_err = _ensure_logged_in(page)
            if auth_err:
                return auth_err

            _ensure_source_panel_open(page)
            before = _read_sources(page)
            before_titles = [src["title"] for src in before]

            skipped_unchanged: List[Dict] = []
            upload_infos = file_infos
            if file_infos and args.dedupe_hash:
                existing_titles = {src["title"] for src in before}
                selected: List[Dict] = []
                for info in file_infos:
                    previous = state_sources.get(info["title"], {})
                    previous_hash = previous.get("hash")
                    if previous_hash and previous_hash == info["hash"] and info["title"] in existing_titles:
                        skipped_unchanged.append(
                            {
                                "title": info["title"],
                                "source_path": str(info["source_path"]),
                                "hash": info["hash"],
                            }
                        )
                        continue
                    selected.append(info)
                upload_infos = selected

            if args.text:
                _insert_text_source(page, args.text)
            elif args.url:
                _insert_url_source(page, args.url)
            elif upload_infos:
                _upload_file_sources(page, [info["upload_path"] for info in upload_infos])

            added_titles: List[str] = []
            if args.text or args.url or upload_infos:
                page.wait_for_timeout(1200)
                added_titles = _wait_for_source_diff(page, before_titles, timeout_sec=args.timeout)

            after = _read_sources(page)
            result: Dict = {
                "status": "success",
                "notebook_url": resolved["notebook_url"],
                "notebook_id": resolved.get("notebook_id"),
                "before_count": len(before),
                "after_count": len(after),
                "added_sources": added_titles,
                "filtered_out": filtered_out,
                "skipped_unchanged": skipped_unchanged,
            }
            if file_infos:
                result["uploaded_files"] = [str(info["upload_path"]) for info in upload_infos]
                result["source_files"] = [str(info["source_path"]) for info in upload_infos]
                if args.dir:
                    result["uploaded_dirs"] = [str(Path(raw).expanduser().resolve()) for raw in args.dir]
                if args.copy_to_temp and temp_dir_path:
                    result["temp_upload_dir"] = str(temp_dir_path)
                result["uploaded_count"] = len(upload_infos)
            return result

        result = _run_browser_command(args, "add-source", action)
        if result.get("status") == "success" and file_infos:
            uploaded_sources = set(result.get("source_files", []))
            uploaded_infos = [
                info
                for info in file_infos
                if str(info["source_path"]) in uploaded_sources
            ]
            if uploaded_infos:
                _update_notebook_state_hashes(state, resolved["notebook_url"], uploaded_infos)
                save_source_state(state)

        return result
    finally:
        if temp_dir_path and temp_dir_path.exists():
            shutil.rmtree(temp_dir_path, ignore_errors=True)


def cmd_delete_source(args) -> Dict:
    resolved = _resolve_notebook_for_ops(args)
    if resolved.get("error"):
        return {"error": resolved["error"]}

    def action(page: Page) -> Dict:
        page.goto(resolved["notebook_url"], wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(2500)
        auth_err = _ensure_logged_in(page)
        if auth_err:
            return auth_err
        _ensure_source_panel_open(page)

        sources = _read_sources(page)
        if not sources:
            return {"error": "No sources found in notebook"}

        indexes = _find_matching_source_indexes(sources, args.source_title, args.contains)
        if not indexes:
            return {"error": f"No source matched: {args.source_title}"}

        matched_titles = [sources[i]["title"] for i in indexes]
        if len(indexes) > 1 and not args.all_matches:
            return {
                "error": (
                    f"Matched {len(indexes)} sources. Re-run with --all-matches "
                    "or use a more specific title."
                ),
                "matches": matched_titles,
            }

        to_delete_titles = matched_titles if args.all_matches else [matched_titles[0]]
        if args.dry_run:
            return {
                "status": "dry-run",
                "operation": "delete-source",
                "notebook_url": resolved["notebook_url"],
                "notebook_id": resolved.get("notebook_id"),
                "matched_count": len(to_delete_titles),
                "matched_titles": to_delete_titles,
            }

        removed: List[str] = []
        for title in to_delete_titles:
            current_sources = _read_sources(page)
            current_indexes = _find_matching_source_indexes(
                current_sources, title, contains=False
            )
            if not current_indexes:
                continue
            _delete_source_once(page, current_indexes[0])
            disappeared = _wait_for(
                lambda: len(_find_matching_source_indexes(_read_sources(page), title, contains=False)) == 0,
                timeout_sec=35,
                poll_ms=500,
            )
            if disappeared:
                removed.append(title)

        if removed:
            state = load_source_state()
            _remove_notebook_state_titles(state, resolved["notebook_url"], removed)
            save_source_state(state)

        final_sources = _read_sources(page)
        return {
            "status": "success",
            "notebook_url": resolved["notebook_url"],
            "notebook_id": resolved.get("notebook_id"),
            "removed_sources": removed,
            "remaining_count": len(final_sources),
        }

    return _run_browser_command(args, "delete-source", action)


def cmd_sync_sources(args) -> Dict:
    resolved = _resolve_notebook_for_ops(args)
    if resolved.get("error"):
        return {"error": resolved["error"]}

    manifest_files: List[str] = []
    if args.manifest:
        try:
            manifest_files = _read_manifest_paths(Path(args.manifest).expanduser().resolve())
        except ValueError as exc:
            return {"error": str(exc)}

    combined_files = list(args.file or []) + manifest_files

    try:
        resolved_files, filtered_out = _collect_source_files(
            files=combined_files,
            dirs=args.dir,
            recursive=bool(args.recursive),
            include_ext_raw=args.include_ext,
            exclude_patterns_raw=args.exclude,
            max_size_raw=args.max_size,
            modified_since_raw=args.modified_since,
        )
    except ValueError as exc:
        return {"error": str(exc)}

    if not resolved_files and not args.delete_missing:
        return {
            "error": "No local files resolved for sync. Provide --file/--dir/--manifest or use --delete-missing",
            "filtered_out": filtered_out,
        }

    file_infos = _make_file_infos(resolved_files)
    try:
        _ensure_unique_titles(file_infos)
    except ValueError as exc:
        return {"error": str(exc), "filtered_out": filtered_out}

    if args.copy_to_temp:
        file_infos, temp_dir = _copy_infos_to_temp(file_infos)
    else:
        temp_dir = None

    local_by_title = {info["title"]: info for info in file_infos}
    state = load_source_state()
    state_sources = _get_notebook_state_sources(state, resolved["notebook_url"])

    try:
        def action(page: Page) -> Dict:
            page.goto(resolved["notebook_url"], wait_until="domcontentloaded", timeout=120000)
            page.wait_for_timeout(2500)
            auth_err = _ensure_logged_in(page)
            if auth_err:
                return auth_err

            _ensure_source_panel_open(page)
            before_sources = _read_sources(page)
            remote_titles = [src["title"] for src in before_sources]
            remote_title_set = set(remote_titles)

            add_infos: List[Dict] = []
            update_infos: List[Dict] = []
            unchanged_infos: List[Dict] = []

            for title, info in local_by_title.items():
                if title not in remote_title_set:
                    add_infos.append(info)
                    continue

                previous_hash = state_sources.get(title, {}).get("hash")
                if args.force_update:
                    update_infos.append(info)
                elif previous_hash and previous_hash != info["hash"]:
                    update_infos.append(info)
                else:
                    unchanged_infos.append(info)

            delete_titles: List[str] = []
            if args.delete_missing:
                for title in sorted(remote_title_set):
                    if title not in local_by_title:
                        delete_titles.append(title)

            plan = {
                "to_add": [info["title"] for info in add_infos],
                "to_update": [info["title"] for info in update_infos],
                "to_delete": delete_titles,
                "unchanged": [info["title"] for info in unchanged_infos],
            }

            if args.dry_run:
                return {
                    "status": "dry-run",
                    "operation": "sync-sources",
                    "notebook_url": resolved["notebook_url"],
                    "notebook_id": resolved.get("notebook_id"),
                    "plan": plan,
                    "filtered_out": filtered_out,
                    "local_count": len(file_infos),
                    "remote_count": len(before_sources),
                }

            removed_titles: List[str] = []
            for title in delete_titles + [info["title"] for info in update_infos]:
                removed_count = _delete_all_exact_title(page, title)
                if removed_count > 0:
                    removed_titles.append(title)

            upload_infos = add_infos + update_infos
            added_titles: List[str] = []
            if upload_infos:
                before_after_delete = _read_sources(page)
                before_titles = [src["title"] for src in before_after_delete]
                _upload_file_sources(page, [info["upload_path"] for info in upload_infos])
                page.wait_for_timeout(1200)
                added_titles = _wait_for_source_diff(page, before_titles, timeout_sec=args.timeout)

            final_sources = _read_sources(page)
            return {
                "status": "success",
                "operation": "sync-sources",
                "notebook_url": resolved["notebook_url"],
                "notebook_id": resolved.get("notebook_id"),
                "plan": plan,
                "filtered_out": filtered_out,
                "uploaded_titles": [info["title"] for info in upload_infos],
                "added_sources": added_titles,
                "removed_titles": removed_titles,
                "before_count": len(before_sources),
                "after_count": len(final_sources),
                "final_sources": [src["title"] for src in final_sources],
            }

        result = _run_browser_command(args, "sync-sources", action)
        if result.get("status") == "success":
            # Record current local desired state hashes to enable future update detection/deduping.
            _update_notebook_state_hashes(state, resolved["notebook_url"], list(local_by_title.values()))
            if args.delete_missing:
                existing_titles = set(local_by_title.keys())
                current_state_titles = list(_get_notebook_state_sources(state, resolved["notebook_url"]).keys())
                to_remove = [title for title in current_state_titles if title not in existing_titles]
                if to_remove:
                    _remove_notebook_state_titles(state, resolved["notebook_url"], to_remove)
            save_source_state(state)
        return result
    finally:
        if temp_dir and temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)


def _add_common_browser_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--show-browser", action="store_true", help="Show browser instead of background mode")
    parser.add_argument("--profile", default="default", help="Auth/browser profile name (default: default)")
    parser.add_argument("--retries", type=int, default=2, help="Retry attempts for transient browser failures")
    parser.add_argument(
        "--artifacts-dir",
        help="Directory for failure screenshots/HTML dumps (default: NOTEBOOKLM data dir artifacts)",
    )


def _add_filter_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--include-ext",
        help="Comma-separated file extensions to include, e.g. md,txt,pdf",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        help="Exclude glob pattern(s), repeatable or comma-separated",
    )
    parser.add_argument("--max-size", help="Max file size (e.g. 5MB, 120KB)")
    parser.add_argument(
        "--modified-since",
        help="Only include files modified since ISO date/time or relative value like 7d, 24h, 90m",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="NotebookLM remote notebook manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_remote_parser = subparsers.add_parser("list-remote", help="List all visible notebooks from NotebookLM account")
    _add_common_browser_args(list_remote_parser)

    create_remote_parser = subparsers.add_parser("create-remote", help="Create a new notebook in NotebookLM")
    create_remote_parser.add_argument("--name", required=True, help="New notebook name")
    create_remote_parser.add_argument(
        "--skip-library",
        action="store_true",
        help="Do not add created notebook to local library",
    )
    create_remote_parser.add_argument("--description", help="Local library description")
    create_remote_parser.add_argument("--topics", help="Local library topics (comma-separated)")
    create_remote_parser.add_argument("--dry-run", action="store_true", help="Preview create action without making changes")
    _add_common_browser_args(create_remote_parser)

    list_sources_parser = subparsers.add_parser("list-sources", help="List sources in a notebook")
    list_sources_parser.add_argument("--notebook-id", help="Notebook ID from local library")
    list_sources_parser.add_argument("--notebook-url", help="NotebookLM URL")
    _add_common_browser_args(list_sources_parser)

    add_source_parser = subparsers.add_parser("add-source", help="Add source to a notebook")
    add_source_parser.add_argument("--notebook-id", help="Notebook ID from local library")
    add_source_parser.add_argument("--notebook-url", help="NotebookLM URL")
    add_source_parser.add_argument("--text", help="Copied text source content")
    add_source_parser.add_argument("--url", help="Website/YouTube URL source")
    add_source_parser.add_argument(
        "--file",
        action="append",
        help="Local file path to upload as source (repeat for multiple files)",
    )
    add_source_parser.add_argument(
        "--dir",
        action="append",
        help="Directory containing files to upload as sources",
    )
    add_source_parser.add_argument(
        "--recursive",
        action="store_true",
        help="When using --dir, include files from nested subdirectories",
    )
    add_source_parser.add_argument(
        "--copy-to-temp",
        action="store_true",
        help="Copy files to a temporary directory before uploading",
    )
    add_source_parser.add_argument(
        "--no-dedupe-hash",
        dest="dedupe_hash",
        action="store_false",
        help="Disable hash-based dedupe for file uploads",
    )
    add_source_parser.set_defaults(dedupe_hash=True)
    add_source_parser.add_argument("--timeout", type=int, default=120, help="Timeout in seconds for source to appear")
    add_source_parser.add_argument("--dry-run", action="store_true", help="Preview source changes without mutating remote notebook")
    _add_filter_args(add_source_parser)
    _add_common_browser_args(add_source_parser)

    delete_source_parser = subparsers.add_parser("delete-source", help="Delete source(s) from a notebook")
    delete_source_parser.add_argument("--notebook-id", help="Notebook ID from local library")
    delete_source_parser.add_argument("--notebook-url", help="NotebookLM URL")
    delete_source_parser.add_argument("--source-title", required=True, help="Source title to delete")
    delete_source_parser.add_argument(
        "--contains",
        action="store_true",
        help="Match source title by substring instead of exact match",
    )
    delete_source_parser.add_argument(
        "--all-matches",
        action="store_true",
        help="Delete all matched sources (otherwise deletes one)",
    )
    delete_source_parser.add_argument("--dry-run", action="store_true", help="Preview matched deletions without deleting")
    _add_common_browser_args(delete_source_parser)

    sync_sources_parser = subparsers.add_parser(
        "sync-sources",
        help="Sync local files to notebook sources with add/update/delete planning",
    )
    sync_sources_parser.add_argument("--notebook-id", help="Notebook ID from local library")
    sync_sources_parser.add_argument("--notebook-url", help="NotebookLM URL")
    sync_sources_parser.add_argument(
        "--file",
        action="append",
        help="Local file path(s) to include in desired source state",
    )
    sync_sources_parser.add_argument(
        "--dir",
        action="append",
        help="Directory containing desired source files",
    )
    sync_sources_parser.add_argument(
        "--manifest",
        help="Manifest file path containing file list (JSON list or newline-delimited)",
    )
    sync_sources_parser.add_argument(
        "--recursive",
        action="store_true",
        help="When using --dir, include nested files",
    )
    sync_sources_parser.add_argument(
        "--delete-missing",
        action="store_true",
        help="Delete remote sources that are missing from local desired state",
    )
    sync_sources_parser.add_argument(
        "--force-update",
        action="store_true",
        help="Re-upload sources that already exist even when hash has not changed",
    )
    sync_sources_parser.add_argument(
        "--copy-to-temp",
        action="store_true",
        help="Copy files to temporary folder before upload",
    )
    sync_sources_parser.add_argument("--timeout", type=int, default=180, help="Timeout in seconds for source updates")
    sync_sources_parser.add_argument("--dry-run", action="store_true", help="Preview sync plan without mutating remote notebook")
    _add_filter_args(sync_sources_parser)
    _add_common_browser_args(sync_sources_parser)

    args = parser.parse_args()
    handlers = {
        "list-remote": cmd_list_remote_notebooks,
        "create-remote": cmd_create_remote_notebook,
        "list-sources": cmd_list_sources,
        "add-source": cmd_add_source,
        "delete-source": cmd_delete_source,
        "sync-sources": cmd_sync_sources,
    }

    try:
        result = handlers[args.command](args)
    except Exception as exc:  # noqa: BLE001
        result = {"error": str(exc)}

    print(json.dumps(result, indent=2))
    if isinstance(result, dict) and result.get("error"):
        sys.exit(1)


if __name__ == "__main__":
    main()
