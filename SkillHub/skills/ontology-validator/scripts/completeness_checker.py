#!/usr/bin/env python3
"""Check completeness of property annotations for an ontology class."""

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
MAX_PROVIDED = 1000
MAX_NAME_LEN = 500


def _is_subclass_of(classes: Dict, child: str, parent: str) -> bool:
    """Check if child is the same as or a subclass of parent.

    Walks the single-parent chain in the ontology summary. Matching is
    case-insensitive. Returns True when ``child`` IS-A ``parent``.
    """
    if not child or not parent:
        return False
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


def _domain_applies(classes: Dict, target_class: str, domain: str) -> bool:
    """Return True when ``target_class`` IS-A every-or-any domain part.

    A property domain may be a single class or a ``|``-separated union of
    classes. The property applies to ``target_class`` when the class is the
    same as, or a subclass of, at least one domain part.
    """
    if not domain:
        return False
    parts = [d.strip() for d in domain.split("|") if d.strip()]
    return any(_is_subclass_of(classes, target_class, d) for d in parts)


def _load_constraints(ontology: Optional[str] = None,
                      constraints_file: Optional[str] = None) -> Dict:
    """Load constraints JSON."""
    if constraints_file:
        path = constraints_file
    elif ontology:
        path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "references", f"{ontology.lower()}_constraints.json",
        )
    else:
        return {}

    if not os.path.isfile(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def check_completeness(
    summary: Dict,
    constraints: Dict,
    class_name: str,
    provided_properties: List[str],
) -> Dict:
    """Check completeness of property annotations for a class.

    Parameters
    ----------
    summary : dict
        Ontology summary.
    constraints : dict
        Validation constraints with required/recommended/optional per class.
    class_name : str
        Class to check completeness for.
    provided_properties : list of str
        Property names that have been provided.

    Returns
    -------
    dict
        completeness_score, required_missing, recommended_missing,
        optional_missing, provided, unrecognized.

    Raises
    ------
    ValueError
        If class_name is empty.
    """
    if not class_name:
        raise ValueError("class_name must not be empty")
    if not isinstance(class_name, str) or len(class_name) > MAX_NAME_LEN:
        raise ValueError(
            f"class_name must be a string of at most {MAX_NAME_LEN} chars"
        )
    if len(provided_properties) > MAX_PROVIDED:
        raise ValueError(
            f"Too many provided properties ({len(provided_properties)}); "
            f"maximum is {MAX_PROVIDED}"
        )
    for p in provided_properties:
        if not isinstance(p, str) or len(p) > MAX_NAME_LEN:
            raise ValueError(
                f"Provided property names must be strings of at most "
                f"{MAX_NAME_LEN} chars"
            )

    classes = summary.get("classes", {})
    obj_props = summary.get("object_properties", {})
    data_props = summary.get("data_properties", {})

    # Find class (case-insensitive)
    matched_class = None
    for c in classes:
        if c.lower() == class_name.lower():
            matched_class = c
            break
    if not matched_class:
        raise ValueError(f"Class '{class_name}' not found in ontology")

    # Get all properties where this class IS-A the declared domain. Uses exact
    # class-name equality plus subclass traversal (not substring containment),
    # so e.g. a bare "Material" is not credited with "Crystalline Material"
    # properties such as "has crystallographic defect".
    all_class_props = set()
    for name, info in obj_props.items():
        if _domain_applies(classes, matched_class, info.get("domain", "")):
            all_class_props.add(name)
    for name, info in data_props.items():
        if _domain_applies(classes, matched_class, info.get("domain", "")):
            all_class_props.add(name)

    # Get constraints for this class
    cls_constraints = constraints.get(matched_class, {})
    required = set(cls_constraints.get("required", []))
    recommended = set(cls_constraints.get("recommended", []))
    optional = set(cls_constraints.get("optional", []))

    # If no constraints defined, treat all domain properties as recommended
    if not required and not recommended and not optional:
        recommended = all_class_props

    # Normalize provided property names (case-insensitive matching)
    provided_set = set()
    unrecognized = []
    all_props = {}
    all_props.update(obj_props)
    all_props.update(data_props)
    all_prop_names_lower = {p.lower(): p for p in all_props}

    for p in provided_properties:
        p_stripped = p.strip()
        if p_stripped in all_props:
            provided_set.add(p_stripped)
        elif p_stripped.lower() in all_prop_names_lower:
            provided_set.add(all_prop_names_lower[p_stripped.lower()])
        else:
            unrecognized.append(p_stripped)

    # Compute missing
    required_missing = sorted(required - provided_set)
    recommended_missing = sorted(recommended - provided_set)
    optional_missing = sorted(optional - provided_set)

    # Compute completeness score
    total_tracked = len(required) + len(recommended) + len(optional)
    if total_tracked == 0:
        completeness_score = 1.0 if not all_class_props else 0.0
    else:
        provided_tracked = (
            len(required & provided_set)
            + len(recommended & provided_set)
            + len(optional & provided_set)
        )
        completeness_score = round(provided_tracked / total_tracked, 3)

    return {
        "class_name": matched_class,
        "completeness_score": completeness_score,
        "required_missing": required_missing,
        "recommended_missing": recommended_missing,
        "optional_missing": optional_missing,
        "provided": sorted(provided_set),
        "unrecognized": unrecognized,
    }


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Check completeness of property annotations for a class.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--ontology", help="Ontology name (e.g., cmso)")
    group.add_argument("--summary-file", help="Path to summary JSON file")
    parser.add_argument("--class", dest="class_name", required=True,
                        help="Class name to check completeness for")
    parser.add_argument("--provided", required=True,
                        help="Comma-separated list of provided property names")
    parser.add_argument("--constraints-file",
                        help="Path to constraints JSON file")
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
        constraints = _load_constraints(
            ontology=args.ontology,
            constraints_file=args.constraints_file,
        )
        if len(args.provided.encode("utf-8")) > MAX_INPUT_BYTES:
            raise ValueError(
                f"--provided exceeds maximum size of {MAX_INPUT_BYTES} bytes"
            )
        provided = [p.strip() for p in args.provided.split(",")]
        result = check_completeness(
            summary=summary,
            constraints=constraints,
            class_name=args.class_name,
            provided_properties=provided,
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
            "class": args.class_name,
            "provided": args.provided,
        },
        "results": result,
    }

    if args.json:
        json.dump(payload, sys.stdout, indent=2)
        print()
    else:
        print(f"Class: {result['class_name']}")
        print(f"Completeness: {result['completeness_score']:.0%}")
        if result["required_missing"]:
            print(f"  Required missing: {', '.join(result['required_missing'])}")
        if result["recommended_missing"]:
            print(f"  Recommended missing: {', '.join(result['recommended_missing'])}")
        if result["unrecognized"]:
            print(f"  Unrecognized: {', '.join(result['unrecognized'])}")


if __name__ == "__main__":
    main()
