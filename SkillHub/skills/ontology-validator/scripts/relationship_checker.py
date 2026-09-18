#!/usr/bin/env python3
"""Validate object property relationships against ontology domain/range constraints."""

import argparse
import json
import os
import sys
from typing import Dict, List, Optional


def _load_summary(ontology: Optional[str] = None,
                  summary_file: Optional[str] = None) -> Dict:
    """Load a summary JSON by ontology name or direct file path."""
    if summary_file:
        path = summary_file
    elif ontology:
        explorer_ref = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "..", "ontology-explorer", "references",
            "ontology_registry.json",
        )
        if not os.path.isfile(explorer_ref):
            raise ValueError(f"Ontology registry not found at {explorer_ref}")
        with open(explorer_ref, encoding="utf-8") as f:
            registry = json.load(f)
        key = ontology.lower()
        if key not in registry:
            available = ", ".join(sorted(registry.keys()))
            raise ValueError(
                f"Ontology '{ontology}' not in registry. Available: {available}"
            )
        ref_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "..", "ontology-explorer", "references",
        )
        path = os.path.join(ref_dir, registry[key]["summary_file"])
    else:
        raise ValueError("Provide --ontology or --summary-file")

    if not os.path.isfile(path):
        raise ValueError(f"Summary file not found: {path}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# Input-validation caps (lightweight DoS / abuse guards, see SKILL.md Security)
MAX_INPUT_BYTES = 1_000_000
MAX_RELATIONSHIPS = 1000
MAX_NAME_LEN = 500


def _is_subclass_of(classes: Dict, child: str, parent: str) -> bool:
    """Check if child is the same as or a subclass of parent."""
    if child.lower() == parent.lower():
        return True
    current = child
    seen = set()
    while current in classes:
        if current in seen:
            break
        seen.add(current)
        p = classes[current].get("parent")
        if not p:
            break
        if p.lower() == parent.lower():
            return True
        current = p
    return False


def check_relationships(
    summary: Dict,
    relationships: List[Dict],
) -> Dict:
    """Validate object property relationships.

    Parameters
    ----------
    summary : dict
        Ontology summary.
    relationships : list of dict
        Each dict: {"subject_class": str, "property": str, "object_class": str}

    Returns
    -------
    dict
        valid (bool), results (per-relationship), errors (list).

    Raises
    ------
    ValueError
        If relationships is empty or not a list.
    """
    if not isinstance(relationships, list) or not relationships:
        raise ValueError("Relationships must be a non-empty list of dicts")
    if len(relationships) > MAX_RELATIONSHIPS:
        raise ValueError(
            f"Too many relationships ({len(relationships)}); "
            f"maximum is {MAX_RELATIONSHIPS}"
        )

    classes = summary.get("classes", {})
    obj_props = summary.get("object_properties", {})

    results_list: List[Dict] = []
    all_errors: List[str] = []

    for rel in relationships:
        if not isinstance(rel, dict):
            continue

        subject = rel.get("subject_class", "")
        prop_name = rel.get("property", "")
        obj = rel.get("object_class", "")
        for field_val in (subject, prop_name, obj):
            if not isinstance(field_val, str) or len(field_val) > MAX_NAME_LEN:
                raise ValueError(
                    "subject_class, property, and object_class must be "
                    f"strings of at most {MAX_NAME_LEN} chars"
                )
        rel_errors: List[str] = []

        # Find the property (case-insensitive)
        prop_info = None
        matched_prop = None
        for p_name, p_info in obj_props.items():
            if p_name.lower() == prop_name.lower():
                prop_info = p_info
                matched_prop = p_name
                break

        if not prop_info:
            rel_errors.append(f"Property '{prop_name}' not found in ontology")
        else:
            # Check domain
            domain = prop_info.get("domain", "")
            if domain and subject:
                domain_parts = [d.strip() for d in domain.split("|")]
                domain_ok = any(
                    _is_subclass_of(classes, subject, d) for d in domain_parts
                )
                if not domain_ok:
                    rel_errors.append(
                        f"Subject '{subject}' is not compatible with "
                        f"property domain '{domain}'"
                    )

            # Check range
            range_ = prop_info.get("range", "")
            if range_ and obj:
                range_ok = _is_subclass_of(classes, obj, range_)
                if not range_ok:
                    rel_errors.append(
                        f"Object '{obj}' is not compatible with "
                        f"property range '{range_}'"
                    )

        is_valid = len(rel_errors) == 0
        results_list.append({
            "subject_class": subject,
            "property": matched_prop or prop_name,
            "object_class": obj,
            "valid": is_valid,
            "errors": rel_errors,
        })
        all_errors.extend(rel_errors)

    return {
        "valid": len(all_errors) == 0,
        "results": results_list,
        "errors": all_errors,
    }


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Validate object property relationships.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--ontology", help="Ontology name (e.g., cmso)")
    group.add_argument("--summary-file", help="Path to summary JSON file")
    parser.add_argument(
        "--relationships",
        required=True,
        help='JSON array of relationships: [{"subject_class":"A","property":"p","object_class":"B"}]',
    )
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
        if args.relationships is not None and (
            len(args.relationships.encode("utf-8")) > MAX_INPUT_BYTES
        ):
            raise ValueError(
                f"--relationships exceeds maximum size of "
                f"{MAX_INPUT_BYTES} bytes"
            )
        relationships = json.loads(args.relationships)
        result = check_relationships(
            summary=summary,
            relationships=relationships,
        )
    except (ValueError, json.JSONDecodeError) as exc:
        if args.json:
            json.dump({"error": str(exc)}, sys.stdout)
            print()
        else:
            print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)

    payload = {
        "inputs": {
            "ontology": args.ontology,
            "relationships": args.relationships,
        },
        "results": result,
    }

    if args.json:
        json.dump(payload, sys.stdout, indent=2)
        print()
    else:
        status = "ALL VALID" if result["valid"] else "ERRORS FOUND"
        print(f"Relationship validation: {status}")
        for r in result["results"]:
            mark = "OK" if r["valid"] else "FAIL"
            print(f"  [{mark}] {r['subject_class']} --{r['property']}--> {r['object_class']}")
            for e in r["errors"]:
                print(f"         {e}")


if __name__ == "__main__":
    main()
