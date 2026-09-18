#!/usr/bin/env python3
"""
Notebook library manager for NotebookLM skill.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Dict, List

from common import (
    generate_notebook_id,
    get_active_notebook,
    get_notebook_by_id,
    is_valid_notebook_url,
    load_library,
    now_iso,
    parse_csv_values,
    save_library,
)


def cmd_add(args) -> Dict:
    library = load_library()
    notebooks: List[Dict] = library.get("notebooks", [])

    if not is_valid_notebook_url(args.url):
        return {"error": "Invalid NotebookLM URL. Expected https://notebooklm.google.com/notebook/<id>"}

    existing_ids = [n.get("id", "") for n in notebooks]
    notebook_id = generate_notebook_id(args.name, existing_ids)
    topics = parse_csv_values(args.topics)
    tags = parse_csv_values(args.tags)

    if not topics:
        return {"error": "--topics is required and must include at least one topic"}

    notebook = {
        "id": notebook_id,
        "url": args.url.strip(),
        "name": args.name.strip(),
        "description": args.description.strip(),
        "topics": topics,
        "tags": tags,
        "added_at": now_iso(),
        "last_used": now_iso(),
        "use_count": 0,
    }

    notebooks.append(notebook)
    if not library.get("active_notebook_id"):
        library["active_notebook_id"] = notebook_id
    save_library(library)
    return {"status": "success", "notebook": notebook}


def cmd_list(_args) -> Dict:
    library = load_library()
    return {
        "active_notebook_id": library.get("active_notebook_id"),
        "count": len(library.get("notebooks", [])),
        "notebooks": library.get("notebooks", []),
    }


def cmd_get(args) -> Dict:
    library = load_library()
    notebook = get_notebook_by_id(library, args.id)
    if not notebook:
        return {"error": f"Notebook not found: {args.id}"}
    return {"notebook": notebook, "active": library.get("active_notebook_id") == args.id}


def cmd_activate(args) -> Dict:
    library = load_library()
    notebook = get_notebook_by_id(library, args.id)
    if not notebook:
        return {"error": f"Notebook not found: {args.id}"}
    library["active_notebook_id"] = args.id
    notebook["last_used"] = now_iso()
    save_library(library)
    return {"status": "success", "active_notebook_id": args.id, "notebook": notebook}


def cmd_remove(args) -> Dict:
    library = load_library()
    notebooks = library.get("notebooks", [])
    before = len(notebooks)
    notebooks = [n for n in notebooks if n.get("id") != args.id]
    if len(notebooks) == before:
        return {"error": f"Notebook not found: {args.id}"}

    library["notebooks"] = notebooks
    if library.get("active_notebook_id") == args.id:
        library["active_notebook_id"] = notebooks[0]["id"] if notebooks else None

    save_library(library)
    return {"status": "success", "removed_id": args.id, "remaining": len(notebooks)}


def cmd_search(args) -> Dict:
    library = load_library()
    query = args.query.lower().strip()
    results = []
    for notebook in library.get("notebooks", []):
        haystack = " ".join(
            [
                str(notebook.get("name", "")),
                str(notebook.get("description", "")),
                " ".join(notebook.get("topics", [])),
                " ".join(notebook.get("tags", [])),
            ]
        ).lower()
        if query in haystack:
            results.append(notebook)
    return {"query": args.query, "count": len(results), "results": results}


def cmd_update(args) -> Dict:
    library = load_library()
    notebook = get_notebook_by_id(library, args.id)
    if not notebook:
        return {"error": f"Notebook not found: {args.id}"}

    if args.name:
        notebook["name"] = args.name.strip()
    if args.description:
        notebook["description"] = args.description.strip()
    if args.topics is not None:
        notebook["topics"] = parse_csv_values(args.topics)
    if args.tags is not None:
        notebook["tags"] = parse_csv_values(args.tags)
    if args.url:
        if not is_valid_notebook_url(args.url):
            return {"error": "Invalid NotebookLM URL. Expected https://notebooklm.google.com/notebook/<id>"}
        notebook["url"] = args.url.strip()

    save_library(library)
    return {"status": "success", "notebook": notebook}


def cmd_stats(_args) -> Dict:
    library = load_library()
    notebooks = library.get("notebooks", [])
    total_queries = sum(int(n.get("use_count", 0)) for n in notebooks)
    most_used = None
    if notebooks:
        most_used = max(notebooks, key=lambda n: int(n.get("use_count", 0))).get("id")

    active = get_active_notebook(library)
    return {
        "total_notebooks": len(notebooks),
        "active_notebook_id": library.get("active_notebook_id"),
        "active_notebook_name": active.get("name") if active else None,
        "most_used_notebook_id": most_used,
        "total_queries": total_queries,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="NotebookLM notebook library manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add notebook to local library")
    add_parser.add_argument("--url", required=True, help="NotebookLM notebook URL")
    add_parser.add_argument("--name", required=True, help="Notebook display name")
    add_parser.add_argument("--description", required=True, help="Notebook description")
    add_parser.add_argument("--topics", required=True, help="Comma-separated topics")
    add_parser.add_argument("--tags", default="", help="Comma-separated tags")

    subparsers.add_parser("list", help="List notebooks")

    get_parser = subparsers.add_parser("get", help="Get notebook by ID")
    get_parser.add_argument("--id", required=True, help="Notebook ID")

    activate_parser = subparsers.add_parser("activate", help="Set active notebook")
    activate_parser.add_argument("--id", required=True, help="Notebook ID")

    remove_parser = subparsers.add_parser("remove", help="Remove notebook")
    remove_parser.add_argument("--id", required=True, help="Notebook ID")

    search_parser = subparsers.add_parser("search", help="Search notebooks")
    search_parser.add_argument("--query", required=True, help="Search query")

    update_parser = subparsers.add_parser("update", help="Update notebook metadata")
    update_parser.add_argument("--id", required=True, help="Notebook ID")
    update_parser.add_argument("--name", help="Notebook name")
    update_parser.add_argument("--description", help="Notebook description")
    update_parser.add_argument("--topics", help="Comma-separated topics")
    update_parser.add_argument("--tags", help="Comma-separated tags")
    update_parser.add_argument("--url", help="Notebook URL")

    subparsers.add_parser("stats", help="Show library stats")

    args = parser.parse_args()
    handlers = {
        "add": cmd_add,
        "list": cmd_list,
        "get": cmd_get,
        "activate": cmd_activate,
        "remove": cmd_remove,
        "search": cmd_search,
        "update": cmd_update,
        "stats": cmd_stats,
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
