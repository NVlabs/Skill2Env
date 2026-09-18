#!/usr/bin/env python3
"""Shared utility: locate the active workspace directory from cwd."""

import os
import glob

KNOWN_DELIVERABLES = [
    "user_brief.md",
    "research_definition.md",
    "research_plan.md",
    "interview_guides.md",
    "evidence_base.md",
    "insights.md",
    "report.html",
]


def find_workspace(cwd):
    """Find workspace directory containing _state.json, starting from cwd.

    Returns absolute path string or None.
    """
    if not cwd or not os.path.isdir(cwd):
        return None

    # 1. cwd itself is the workspace (has _state.json or known deliverables)
    if os.path.isfile(os.path.join(cwd, "_state.json")):
        return cwd
    for f in KNOWN_DELIVERABLES:
        if os.path.isfile(os.path.join(cwd, f)):
            return cwd

    # 2. Scan workspace/*/ under cwd and ancestors (up to 5 levels)
    search_dir = cwd
    for _ in range(5):
        ws = _scan_workspace_subdir(search_dir)
        if ws:
            return ws
        parent = os.path.dirname(search_dir)
        if parent == search_dir:
            break
        search_dir = parent

    # 3. Fallback: find directory with known deliverable files
    ws_glob = os.path.join(cwd, "workspace", "*")
    for candidate in glob.glob(ws_glob):
        if not os.path.isdir(candidate):
            continue
        for f in KNOWN_DELIVERABLES:
            if os.path.isfile(os.path.join(candidate, f)):
                return candidate

    return None


def _scan_workspace_subdir(base):
    """Scan base/workspace/*/ for dirs containing _state.json."""
    ws_dir = os.path.join(base, "workspace")
    if not os.path.isdir(ws_dir):
        return None

    candidates = []
    try:
        for entry in os.listdir(ws_dir):
            full = os.path.join(ws_dir, entry)
            state_file = os.path.join(full, "_state.json")
            if os.path.isdir(full) and os.path.isfile(state_file):
                mtime = os.path.getmtime(state_file)
                candidates.append((mtime, full))
    except OSError:
        return None

    if candidates:
        candidates.sort(reverse=True)  # most recent first
        return candidates[0][1]
    return None
