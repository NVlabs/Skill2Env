#!/usr/bin/env python3
"""Map natural-language terms to ontology classes and properties."""

import argparse
import json
import os
import re
import sys
from typing import Dict, List, Optional


def _load_summary(ontology: Optional[str] = None,
                  summary_file: Optional[str] = None) -> Dict:
    """Load a summary JSON by ontology name or direct file path."""
    if summary_file:
        path = summary_file
    elif ontology:
        # Look for registry in ontology-explorer references
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


def _load_mappings(ontology: Optional[str] = None) -> Dict:
    """Load per-ontology mapping config (synonyms, property synonyms, etc.).

    Returns an empty dict if no mappings file exists for the ontology,
    enabling graceful fallback to generic matching.
    """
    if not ontology:
        return {}

    # Look for registry
    explorer_ref = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "..", "ontology-explorer", "references",
        "ontology_registry.json",
    )
    if not os.path.isfile(explorer_ref):
        return {}

    with open(explorer_ref, encoding="utf-8") as f:
        registry = json.load(f)

    key = ontology.lower()
    if key not in registry:
        return {}

    entry = registry[key]
    mappings_file = entry.get("mappings_file")
    if not mappings_file:
        return {}

    # Mappings live in ontology-mapper/references/
    mapper_ref = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "references",
    )
    path = os.path.join(mapper_ref, mappings_file)
    if not os.path.isfile(path):
        return {}

    with open(path, encoding="utf-8") as f:
        return json.load(f)


_MAX_TERM_LEN = 200
_MAX_TERMS = 100


def map_concept(
    summary: Dict,
    term: Optional[str] = None,
    terms: Optional[List[str]] = None,
    synonyms: Optional[Dict[str, str]] = None,
    property_synonyms: Optional[Dict[str, str]] = None,
    ontology: Optional[str] = None,
) -> Dict:
    """Map natural-language terms to ontology concepts.

    Parameters
    ----------
    summary : dict
        Ontology summary (as produced by ontology_summarizer.py).
    term : str, optional
        A single term to map.
    terms : list of str, optional
        Multiple terms to map.
    synonyms : dict, optional
        Term-to-class synonym table. Loaded from config if not provided.
    property_synonyms : dict, optional
        Term-to-property synonym table. Loaded from config if not provided.
    ontology : str, optional
        Ontology name, used to build a self-contained search suggestion for
        unmatched terms. If None, a ``<name>`` placeholder is emitted.

    Returns
    -------
    dict
        matches, suggestions, and unmatched terms.

    Raises
    ------
    ValueError
        If neither term nor terms is provided, or if a term exceeds the
        length / count limits.
    """
    if not term and not terms:
        raise ValueError("Provide --term or --terms")

    if synonyms is None:
        synonyms = {}
    if property_synonyms is None:
        property_synonyms = {}

    all_terms = []
    if term:
        all_terms.append(term)
    if terms:
        all_terms.extend(terms)

    if len(all_terms) > _MAX_TERMS:
        raise ValueError(f"Too many terms (max {_MAX_TERMS})")
    for t in all_terms:
        if not isinstance(t, str):
            raise ValueError("Each term must be a string")
        if len(t) > _MAX_TERM_LEN:
            raise ValueError(
                f"Term exceeds maximum length of {_MAX_TERM_LEN} characters"
            )

    classes = summary.get("classes", {})
    obj_props = summary.get("object_properties", {})
    data_props = summary.get("data_properties", {})

    all_labels = {}
    for name in classes:
        all_labels[name.lower()] = {"label": name, "type": "class"}
    for name in obj_props:
        all_labels[name.lower()] = {"label": name, "type": "object_property"}
    for name in data_props:
        all_labels[name.lower()] = {"label": name, "type": "data_property"}

    matches = []
    unmatched = []

    for t in all_terms:
        t_stripped = t.strip()
        t_lower = t_stripped.lower()
        found = False

        # 1. Check synonym table (loaded from per-ontology config)
        if t_lower in synonyms:
            target = synonyms[t_lower]
            info = classes.get(target) or obj_props.get(target) or data_props.get(target)
            iri = info.get("iri", "") if info else ""
            match_type = "class" if target in classes else "property"
            matches.append({
                "term": t_stripped,
                "matched": target,
                "match_type": f"synonym_{match_type}",
                "confidence": 0.9,
                "iri": iri,
            })
            found = True
            continue

        # Check property synonyms (loaded from per-ontology config)
        if t_lower in property_synonyms:
            target = property_synonyms[t_lower]
            info = obj_props.get(target) or data_props.get(target)
            iri = info.get("iri", "") if info else ""
            matches.append({
                "term": t_stripped,
                "matched": target,
                "match_type": "synonym_property",
                "confidence": 0.9,
                "iri": iri,
            })
            found = True
            continue

        # 2. Exact label match (case-insensitive)
        if t_lower in all_labels:
            entry = all_labels[t_lower]
            label = entry["label"]
            info = classes.get(label) or obj_props.get(label) or data_props.get(label)
            iri = info.get("iri", "") if info else ""
            matches.append({
                "term": t_stripped,
                "matched": label,
                "match_type": f"exact_{entry['type']}",
                "confidence": 1.0,
                "iri": iri,
            })
            found = True
            continue

        # 3. Substring match on labels
        pattern = re.compile(re.escape(t_lower), re.IGNORECASE)
        for label_lower, entry in all_labels.items():
            if pattern.search(label_lower):
                label = entry["label"]
                info = (classes.get(label) or obj_props.get(label)
                        or data_props.get(label))
                iri = info.get("iri", "") if info else ""
                matches.append({
                    "term": t_stripped,
                    "matched": label,
                    "match_type": f"substring_{entry['type']}",
                    "confidence": 0.7,
                    "iri": iri,
                })
                found = True

        # 4. Description search
        if not found:
            for name, info in classes.items():
                desc = info.get("description") or ""
                if pattern.search(desc):
                    matches.append({
                        "term": t_stripped,
                        "matched": name,
                        "match_type": "description_class",
                        "confidence": 0.5,
                        "iri": info.get("iri", ""),
                    })
                    found = True

        if not found:
            unmatched.append(t_stripped)

    # Deduplicate matches (same term+matched pair)
    seen = set()
    unique_matches = []
    for m in matches:
        key = (m["term"], m["matched"])
        if key not in seen:
            seen.add(key)
            unique_matches.append(m)

    # Generate suggestions from unmatched terms. The class_browser.py script
    # lives in the sibling ontology-explorer skill and requires --ontology, so
    # emit a fully-pathed, runnable command.
    ont = ontology or "<name>"
    suggestions = []
    for t in unmatched:
        suggestions.append(
            "Try: python skills/ontology/ontology-explorer/scripts/"
            f"class_browser.py --ontology {ont} --search '{t}'"
        )

    return {
        "matches": unique_matches,
        "unmatched": unmatched,
        "suggestions": suggestions,
    }


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Map natural-language terms to ontology concepts.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--ontology", help="Ontology name (e.g., cmso)")
    group.add_argument("--summary-file", help="Path to summary JSON file")
    parser.add_argument("--term", help="Single term to map")
    parser.add_argument("--terms", help="Comma-separated terms to map")
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
        # Load per-ontology synonyms from config
        mappings = _load_mappings(ontology=args.ontology)
        synonyms = mappings.get("synonyms", {})
        property_synonyms = mappings.get("property_synonyms", {})

        terms_list = None
        if args.terms:
            terms_list = [t.strip() for t in args.terms.split(",")]
        result = map_concept(
            summary=summary,
            term=args.term,
            terms=terms_list,
            synonyms=synonyms,
            property_synonyms=property_synonyms,
            ontology=args.ontology,
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
            "term": args.term,
            "terms": args.terms,
        },
        "results": result,
    }

    if args.json:
        json.dump(payload, sys.stdout, indent=2)
        print()
    else:
        if result["matches"]:
            print("Matches:")
            for m in result["matches"]:
                print(f"  {m['term']} -> {m['matched']} "
                      f"({m['match_type']}, confidence={m['confidence']})")
        if result["unmatched"]:
            print(f"Unmatched: {', '.join(result['unmatched'])}")
        for s in result["suggestions"]:
            print(f"  Suggestion: {s}")


if __name__ == "__main__":
    main()
