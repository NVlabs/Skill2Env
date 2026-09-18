#!/usr/bin/env python3
"""Generate a compact JSON summary from an OWL/XML ontology file."""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from typing import Dict, List, Optional

# Import parse_owl from sibling module
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPT_DIR)
from owl_parser import parse_owl  # noqa: E402


def summarize_ontology(source: str) -> Dict:
    """Parse an OWL file and produce a compact summary dict.

    The summary is designed for fast lookup without re-parsing OWL.
    Classes and properties are keyed by label for direct name-based access.

    Parameters
    ----------
    source : str
        File path or URL to an OWL/XML file.

    Returns
    -------
    dict
        Summary with metadata, classes, class_hierarchy,
        object_properties, data_properties, and statistics.

    Raises
    ------
    ValueError
        If the source cannot be read or parsed.
    """
    parsed = parse_owl(source)

    # Build IRI-local-name -> label mapping for parent resolution
    local_to_label: Dict[str, str] = {}
    for cls in parsed["classes"]:
        local_name = cls["iri"].rsplit("#", 1)[-1].rsplit("/", 1)[-1]
        local_to_label[local_name] = cls["label"]

    # Build classes dict keyed by label
    classes: Dict[str, Dict] = {}
    # First pass: add all classes with parent resolved to label
    for cls in parsed["classes"]:
        parent_raw = cls["parent"]
        parent_label = local_to_label.get(parent_raw, parent_raw) if parent_raw else None
        classes[cls["label"]] = {
            "iri": cls["iri"],
            "parent": parent_label,
            "children": [],
            "description": cls["description"],
        }
    # Second pass: populate children lists
    for cls in parsed["classes"]:
        label = cls["label"]
        parent_label = classes[label]["parent"]
        if parent_label and parent_label in classes:
            if label not in classes[parent_label]["children"]:
                classes[parent_label]["children"].append(label)
    # Sort children lists
    for info in classes.values():
        info["children"].sort()

    # Helper to resolve IRI local names to labels in domain/range values
    def _resolve_domain_range(value: Optional[str]) -> Optional[str]:
        if not value:
            return value
        # Handle union domains like "A | B"
        parts = [p.strip() for p in value.split("|")]
        resolved = [local_to_label.get(p, p) for p in parts]
        return " | ".join(resolved)

    # Build object properties dict keyed by label
    object_properties: Dict[str, Dict] = {}
    for prop in parsed["object_properties"]:
        object_properties[prop["label"]] = {
            "iri": prop["iri"],
            "domain": _resolve_domain_range(prop["domain"]),
            "range": _resolve_domain_range(prop["range"]),
            "description": prop["description"],
        }

    # Build data properties dict keyed by label
    data_properties: Dict[str, Dict] = {}
    for prop in parsed["data_properties"]:
        data_properties[prop["label"]] = {
            "iri": prop["iri"],
            "domain": _resolve_domain_range(prop["domain"]),
            "range_type": prop["range_type"],
            "description": prop["description"],
        }

    # Build label-based class hierarchy from corrected classes dict
    def _build_label_hierarchy(classes_dict: Dict) -> Dict:
        children_of: Dict[Optional[str], List[str]] = {}
        for name, info in classes_dict.items():
            parent = info.get("parent")
            children_of.setdefault(parent, []).append(name)

        def _subtree(label: str) -> Dict:
            kids = children_of.get(label, [])
            return {k: _subtree(k) for k in sorted(kids)}

        roots = children_of.get(None, [])
        return {r: _subtree(r) for r in sorted(roots)}

    class_hierarchy = _build_label_hierarchy(classes)

    return {
        "metadata": {
            "iri": parsed["metadata"]["iri"],
            "title": parsed["metadata"]["title"],
            "version": parsed["metadata"]["version"],
            "description": parsed["metadata"]["description"],
            "source_url": source if source.startswith("http") else None,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
        "classes": classes,
        "class_hierarchy": class_hierarchy,
        "object_properties": object_properties,
        "data_properties": data_properties,
        "statistics": {
            "num_classes": len(classes),
            "num_object_properties": len(object_properties),
            "num_data_properties": len(data_properties),
        },
    }


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate a compact JSON summary from an OWL/XML ontology.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Path or URL to an OWL/XML file",
    )
    parser.add_argument(
        "--output",
        help="Output file path for the JSON summary (if omitted, prints to stdout)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON output",
    )
    return parser.parse_args()


def main() -> None:
    """CLI entry point."""
    args = parse_args()
    try:
        summary = summarize_ontology(source=args.source)
    except ValueError as exc:
        if args.json:
            json.dump({"error": str(exc)}, sys.stdout)
            print()
        else:
            print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
            f.write("\n")
        if args.json:
            payload = {
                "inputs": {"source": args.source, "output": args.output},
                "results": {
                    "output_file": args.output,
                    "statistics": summary["statistics"],
                },
            }
            json.dump(payload, sys.stdout, indent=2)
            print()
        else:
            stats = summary["statistics"]
            print(f"Summary written to {args.output}")
            print(f"  Classes: {stats['num_classes']}")
            print(f"  Object properties: {stats['num_object_properties']}")
            print(f"  Data properties: {stats['num_data_properties']}")
    else:
        if args.json:
            payload = {
                "inputs": {"source": args.source},
                "results": summary,
            }
            json.dump(payload, sys.stdout, indent=2)
            print()
        else:
            json.dump(summary, sys.stdout, indent=2)
            print()


if __name__ == "__main__":
    main()
