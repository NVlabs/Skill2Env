#!/usr/bin/env python3
"""Parse an OWL/XML ontology file and extract its structure."""

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional
from urllib.request import urlopen
from urllib.error import URLError

# OWL/RDF/RDFS namespace URIs
NS = {
    "owl": "http://www.w3.org/2002/07/owl#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "xml": "http://www.w3.org/XML/1998/namespace",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "dc": "http://purl.org/dc/elements/1.1/",
    "terms": "http://purl.org/dc/terms/",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "obo": "http://purl.obolibrary.org/obo/",
}

# IAO annotation IRIs used by CMSO for definitions
IAO_DEFINITION = "http://purl.obolibrary.org/obo/IAO_0000115"


def _local_name(iri: str) -> str:
    """Extract local name from an IRI (after last # or /)."""
    if "#" in iri:
        return iri.rsplit("#", 1)[-1]
    return iri.rsplit("/", 1)[-1]


def _get_about(elem: ET.Element) -> Optional[str]:
    """Get rdf:about attribute from an element."""
    return elem.get(f"{{{NS['rdf']}}}about")


def _get_resource(elem: ET.Element) -> Optional[str]:
    """Get rdf:resource attribute from an element."""
    return elem.get(f"{{{NS['rdf']}}}resource")


def _find_label(elem: ET.Element) -> Optional[str]:
    """Find rdfs:label or skos:prefLabel text."""
    label_el = elem.find(f"{{{NS['rdfs']}}}label")
    if label_el is not None and label_el.text:
        return label_el.text.strip()
    label_el = elem.find(f"{{{NS['skos']}}}prefLabel")
    if label_el is not None and label_el.text:
        return label_el.text.strip()
    return None


def _find_description(elem: ET.Element) -> Optional[str]:
    """Find description from rdfs:comment, skos:definition, or IAO definition."""
    for tag in [
        f"{{{NS['rdfs']}}}comment",
        f"{{{NS['skos']}}}definition",
        f"{{{IAO_DEFINITION}}}",
    ]:
        desc_el = elem.find(tag)
        if desc_el is not None and desc_el.text:
            return desc_el.text.strip()
    # Try IAO as rdf:resource annotated property
    for ann in elem.findall(f"{{{NS['owl']}}}Annotation"):
        prop = ann.find(f"{{{NS['owl']}}}AnnotationProperty")
        if prop is not None and _get_resource(prop) == IAO_DEFINITION:
            literal = ann.find(f"{{{NS['owl']}}}Literal")
            if literal is not None and literal.text:
                return literal.text.strip()
    return None


def _find_parent_class(elem: ET.Element) -> Optional[str]:
    """Find the direct rdfs:subClassOf parent IRI (simple case only)."""
    sub = elem.find(f"{{{NS['rdfs']}}}subClassOf")
    if sub is not None:
        resource = _get_resource(sub)
        if resource:
            return resource
    return None


def _find_domain(elem: ET.Element) -> Optional[str]:
    """Find rdfs:domain, handling both simple and union cases."""
    dom_el = elem.find(f"{{{NS['rdfs']}}}domain")
    if dom_el is None:
        return None
    resource = _get_resource(dom_el)
    if resource:
        return _local_name(resource)
    # Check for owl:Class > owl:unionOf inside domain
    cls_el = dom_el.find(f"{{{NS['owl']}}}Class")
    if cls_el is not None:
        union = cls_el.find(f"{{{NS['owl']}}}unionOf")
        if union is not None:
            members = []
            for desc in union.findall(f"{{{NS['rdfs']}}}Description"):
                about = _get_about(desc)
                if about:
                    members.append(_local_name(about))
            for cls in union.findall(f"{{{NS['owl']}}}Class"):
                about = _get_about(cls)
                if about:
                    members.append(_local_name(about))
            if members:
                return " | ".join(members)
    return None


def _find_range(elem: ET.Element) -> Optional[str]:
    """Find rdfs:range IRI."""
    rng_el = elem.find(f"{{{NS['rdfs']}}}range")
    if rng_el is not None:
        resource = _get_resource(rng_el)
        if resource:
            return _local_name(resource)
    return None


def _build_hierarchy(classes: List[Dict]) -> Dict:
    """Build a nested tree dict from flat class list with parent pointers."""
    children_map: Dict[Optional[str], List[str]] = {}
    for cls in classes:
        parent = cls.get("parent")
        children_map.setdefault(parent, []).append(cls["label"])

    def _subtree(label: str) -> Dict:
        kids = children_map.get(label, [])
        return {k: _subtree(k) for k in sorted(kids)}

    roots = children_map.get(None, [])
    return {r: _subtree(r) for r in sorted(roots)}


def parse_owl(source: str) -> Dict:
    """Parse an OWL/XML file and return structured ontology representation.

    Parameters
    ----------
    source : str
        File path or URL to an OWL/XML file.

    Returns
    -------
    dict
        Keys: metadata, classes, object_properties, data_properties,
        class_hierarchy, imports.

    Raises
    ------
    ValueError
        If the source cannot be read or parsed.
    """
    if source.startswith("http://"):
        raise ValueError(
            "Insecure URL rejected: only https:// URLs are accepted for "
            "remote OWL sources (got http://)"
        )
    try:
        if source.startswith("https://"):
            with urlopen(source, timeout=30) as resp:
                xml_bytes = resp.read()
            root = ET.fromstring(xml_bytes)
        else:
            tree = ET.parse(source)
            root = tree.getroot()
    except (ET.ParseError, FileNotFoundError, URLError, OSError) as exc:
        raise ValueError(f"Cannot parse OWL source: {exc}") from exc

    # Extract ontology metadata
    ont_el = root.find(f"{{{NS['owl']}}}Ontology")
    metadata = {
        "iri": _get_about(ont_el) if ont_el is not None else None,
        "version": None,
        "title": None,
        "description": None,
    }
    if ont_el is not None:
        ver = ont_el.find(f"{{{NS['owl']}}}versionInfo")
        if ver is not None and ver.text:
            metadata["version"] = ver.text.strip()
        title = ont_el.find(f"{{{NS['dc']}}}title")
        if title is not None and title.text:
            metadata["title"] = title.text.strip()
        desc = ont_el.find(f"{{{NS['dc']}}}description")
        if desc is not None and desc.text:
            metadata["description"] = desc.text.strip()
        if not metadata["description"]:
            desc = ont_el.find(f"{{{NS['terms']}}}abstract")
            if desc is not None and desc.text:
                metadata["description"] = desc.text.strip()

    # Extract imports
    imports = []
    if ont_el is not None:
        for imp in ont_el.findall(f"{{{NS['owl']}}}imports"):
            resource = _get_resource(imp)
            if resource:
                imports.append(resource)

    # Extract classes
    classes = []
    for cls_el in root.findall(f"{{{NS['owl']}}}Class"):
        iri = _get_about(cls_el)
        if not iri:
            continue
        label = _find_label(cls_el) or _local_name(iri)
        description = _find_description(cls_el)
        parent_iri = _find_parent_class(cls_el)
        parent = _local_name(parent_iri) if parent_iri else None
        # Skip OWL built-in parents
        if parent in ("Thing", "Resource", "NamedIndividual"):
            parent = None
        classes.append({
            "iri": iri,
            "label": label,
            "parent": parent,
            "description": description,
        })

    # Extract object properties
    object_properties = []
    for prop_el in root.findall(f"{{{NS['owl']}}}ObjectProperty"):
        iri = _get_about(prop_el)
        if not iri:
            continue
        label = _find_label(prop_el) or _local_name(iri)
        description = _find_description(prop_el)
        domain = _find_domain(prop_el)
        range_ = _find_range(prop_el)
        object_properties.append({
            "iri": iri,
            "label": label,
            "domain": domain,
            "range": range_,
            "description": description,
        })

    # Extract data properties
    data_properties = []
    for prop_el in root.findall(f"{{{NS['owl']}}}DatatypeProperty"):
        iri = _get_about(prop_el)
        if not iri:
            continue
        label = _find_label(prop_el) or _local_name(iri)
        description = _find_description(prop_el)
        domain = _find_domain(prop_el)
        range_type = _find_range(prop_el)
        data_properties.append({
            "iri": iri,
            "label": label,
            "domain": domain,
            "range_type": range_type,
            "description": description,
        })

    # Build class hierarchy
    class_hierarchy = _build_hierarchy(classes)

    return {
        "metadata": metadata,
        "classes": classes,
        "object_properties": object_properties,
        "data_properties": data_properties,
        "class_hierarchy": class_hierarchy,
        "imports": imports,
    }


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Parse an OWL/XML ontology file and extract its structure.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Path or URL to an OWL/XML file",
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
        result = parse_owl(source=args.source)
    except ValueError as exc:
        if args.json:
            json.dump({"error": str(exc)}, sys.stdout)
            print()
        else:
            print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)

    payload = {
        "inputs": {"source": args.source},
        "results": {
            "metadata": result["metadata"],
            "num_classes": len(result["classes"]),
            "num_object_properties": len(result["object_properties"]),
            "num_data_properties": len(result["data_properties"]),
            "classes": result["classes"],
            "object_properties": result["object_properties"],
            "data_properties": result["data_properties"],
            "class_hierarchy": result["class_hierarchy"],
            "imports": result["imports"],
        },
    }

    if args.json:
        json.dump(payload, sys.stdout, indent=2)
        print()
    else:
        m = result["metadata"]
        print(f"Ontology: {m.get('title') or m.get('iri') or 'Unknown'}")
        print(f"  Version: {m.get('version', 'N/A')}")
        print(f"  Classes: {len(result['classes'])}")
        print(f"  Object properties: {len(result['object_properties'])}")
        print(f"  Data properties: {len(result['data_properties'])}")
        print()
        for cls in result["classes"]:
            parent = f" (subclass of {cls['parent']})" if cls["parent"] else ""
            print(f"  {cls['label']}{parent}")


if __name__ == "__main__":
    main()
