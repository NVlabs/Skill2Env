#!/usr/bin/env python3
"""Browse and query ontology class hierarchy from a summary JSON."""

import argparse
import json
import os
import re
import sys
from typing import Dict, List, Optional

# Safe-character pattern for --class / --search inputs.
# Allows letters, digits, whitespace, and a few punctuation marks common in
# ontology labels (hyphen, slash, underscore, parentheses). Bounded length.
_SAFE_NAME_RE = re.compile(r"^[\w \-/()]{1,128}$")
_MAX_SEARCH_LEN = 128
# Cap on the number of search results returned, to prevent output flooding.
_MAX_RESULTS = 200


def _validate_name(value: Optional[str], field: str) -> None:
    """Reject inputs that exceed the length cap or contain unsafe characters."""
    if value is None:
        return
    if len(value) > _MAX_SEARCH_LEN:
        raise ValueError(
            f"{field} is too long (max {_MAX_SEARCH_LEN} characters)"
        )
    if not _SAFE_NAME_RE.match(value):
        raise ValueError(
            f"{field} contains unsupported characters; allowed: "
            "letters, digits, space, and - / _ ( )"
        )


def _norm(value: str) -> str:
    """Normalize a label/domain token: drop spaces and lowercase."""
    return value.replace(" ", "").lower()


def _load_summary(ontology: Optional[str] = None,
                  summary_file: Optional[str] = None) -> Dict:
    """Load a summary JSON by ontology name or direct file path."""
    if summary_file:
        path = summary_file
    elif ontology:
        registry_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "references", "ontology_registry.json",
        )
        if not os.path.isfile(registry_path):
            raise ValueError(f"Ontology registry not found at {registry_path}")
        with open(registry_path, encoding="utf-8") as f:
            registry = json.load(f)
        key = ontology.lower()
        if key not in registry:
            available = ", ".join(sorted(registry.keys()))
            raise ValueError(
                f"Ontology '{ontology}' not in registry. Available: {available}"
            )
        ref_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "references",
        )
        path = os.path.join(ref_dir, registry[key]["summary_file"])
    else:
        raise ValueError("Provide --ontology or --summary-file")

    if not os.path.isfile(path):
        raise ValueError(f"Summary file not found: {path}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _path_to_root(classes: Dict, label: str) -> List[str]:
    """Return the path from a class to the root of the hierarchy."""
    path = [label]
    current = label
    seen = set()
    while current in classes and classes[current].get("parent"):
        parent = classes[current]["parent"]
        if parent in seen:
            break
        seen.add(parent)
        path.append(parent)
        current = parent
    path.reverse()
    return path


def _subtree(classes: Dict, label: str, depth: int, current: int = 0) -> Dict:
    """Build a subtree dict down to a given depth."""
    if depth >= 0 and current >= depth:
        return {}
    children = classes.get(label, {}).get("children", [])
    return {
        child: _subtree(classes, child, depth, current + 1)
        for child in sorted(children)
    }


def _applicable_properties(summary: Dict, label: str) -> Dict:
    """Find object and data properties where the class is in the domain."""
    def _domain_matches(domain: Optional[str]) -> bool:
        # Domains may be a single class or a union like "A | B"; normalize both
        # sides identically (space-insensitive, case-insensitive).
        if not domain:
            return False
        target = _norm(label)
        return any(_norm(part.strip()) == target for part in domain.split("|"))

    obj_props = []
    for name, info in summary.get("object_properties", {}).items():
        if _domain_matches(info.get("domain")):
            obj_props.append({
                "name": name,
                "range": info.get("range"),
                "description": info.get("description"),
            })
    data_props = []
    for name, info in summary.get("data_properties", {}).items():
        if _domain_matches(info.get("domain")):
            data_props.append({
                "name": name,
                "range_type": info.get("range_type"),
                "description": info.get("description"),
            })
    return {"object_properties": obj_props, "data_properties": data_props}


def browse_class(
    summary: Dict,
    class_name: Optional[str] = None,
    list_roots: bool = False,
    search: Optional[str] = None,
    depth: int = -1,
) -> Dict:
    """Browse ontology class hierarchy.

    Parameters
    ----------
    summary : dict
        Ontology summary (as produced by ontology_summarizer.py).
    class_name : str, optional
        Name of a specific class to inspect.
    list_roots : bool
        If True, list root classes (no parent).
    search : str, optional
        Search term to match against class labels (case-insensitive).
    depth : int
        Max depth for subtree expansion (-1 = unlimited).

    Returns
    -------
    dict
        Query results with class_info, subtree, properties, path_to_root,
        roots, or search_results depending on the query mode.

    Raises
    ------
    ValueError
        If no valid query mode is specified or class not found.
    """
    classes = summary.get("classes", {})

    if not class_name and not list_roots and not search:
        raise ValueError(
            "Provide --class, --list-roots, or --search"
        )

    _validate_name(class_name, "--class")
    _validate_name(search, "--search")

    result: Dict = {}

    if list_roots:
        roots = [
            name for name, info in classes.items()
            if not info.get("parent")
        ]
        result["roots"] = sorted(roots)

    if search:
        pattern = re.compile(re.escape(search), re.IGNORECASE)
        matches = []
        for name, info in classes.items():
            score = 0
            if pattern.search(name):
                score = 1
            desc = info.get("description") or ""
            if pattern.search(desc):
                score = max(score, 0.5)
            if score > 0:
                matches.append({
                    "label": name,
                    "parent": info.get("parent"),
                    "description": info.get("description"),
                    "relevance": score,
                })
        matches.sort(key=lambda m: (-m["relevance"], m["label"]))
        result["search_results"] = matches[:_MAX_RESULTS]

    if class_name:
        # Try exact match first, then case-insensitive
        matched_label = None
        if class_name in classes:
            matched_label = class_name
        else:
            for name in classes:
                if name.lower() == class_name.lower():
                    matched_label = name
                    break
            if not matched_label:
                # Try without spaces
                normalized = class_name.replace(" ", "").lower()
                for name in classes:
                    if name.replace(" ", "").lower() == normalized:
                        matched_label = name
                        break
        if not matched_label:
            available = sorted(classes.keys())
            raise ValueError(
                f"Class '{class_name}' not found. "
                f"Available: {', '.join(available[:20])}"
                + ("..." if len(available) > 20 else "")
            )

        info = classes[matched_label]
        result["class_info"] = {
            "label": matched_label,
            "iri": info.get("iri"),
            "parent": info.get("parent"),
            "children": info.get("children", []),
            "description": info.get("description"),
        }
        result["subtree"] = _subtree(classes, matched_label, depth)
        result["path_to_root"] = _path_to_root(classes, matched_label)
        result["properties"] = _applicable_properties(summary, matched_label)

    return result


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Browse and query ontology class hierarchy.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--ontology", help="Ontology name (e.g., cmso)")
    group.add_argument("--summary-file", help="Path to summary JSON file")
    parser.add_argument("--class", dest="class_name", help="Class name to inspect")
    parser.add_argument("--list-roots", action="store_true", help="List root classes")
    parser.add_argument("--search", help="Search term for class labels")
    parser.add_argument("--depth", type=int, default=-1,
                        help="Max subtree depth (-1 = unlimited)")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser.parse_args()


def main() -> None:
    """CLI entry point."""
    args = parse_args()
    try:
        summary = _load_summary(
            ontology=args.ontology,
            summary_file=args.summary_file,
        )
        result = browse_class(
            summary=summary,
            class_name=args.class_name,
            list_roots=args.list_roots,
            search=args.search,
            depth=args.depth,
        )
    except ValueError as exc:
        if args.json:
            json.dump({"error": str(exc)}, sys.stdout)
            print()
        else:
            print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)

    payload = {
        "inputs": {
            "ontology": args.ontology,
            "summary_file": args.summary_file,
            "class": args.class_name,
            "list_roots": args.list_roots,
            "search": args.search,
            "depth": args.depth,
        },
        "results": result,
    }

    if args.json:
        json.dump(payload, sys.stdout, indent=2)
        print()
    else:
        if "roots" in result:
            print("Root classes:")
            for r in result["roots"]:
                print(f"  {r}")
        if "search_results" in result:
            print(f"Search results for '{args.search}':")
            for m in result["search_results"]:
                parent = f" (subclass of {m['parent']})" if m["parent"] else ""
                print(f"  {m['label']}{parent}")
        if "class_info" in result:
            info = result["class_info"]
            print(f"Class: {info['label']}")
            if info["description"]:
                print(f"  Description: {info['description']}")
            if info["parent"]:
                print(f"  Parent: {info['parent']}")
            if info["children"]:
                print(f"  Children: {', '.join(info['children'])}")
            print(f"  Path to root: {' > '.join(result['path_to_root'])}")
            props = result["properties"]
            if props["object_properties"]:
                print("  Object properties:")
                for p in props["object_properties"]:
                    print(f"    {p['name']} -> {p['range']}")
            if props["data_properties"]:
                print("  Data properties:")
                for p in props["data_properties"]:
                    print(f"    {p['name']} [{p['range_type']}]")


if __name__ == "__main__":
    main()
