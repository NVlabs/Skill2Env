#!/usr/bin/env python3
"""Annotate a material sample description with ontology terms.

Universal knowledge (periodic table, element resolution) is hardcoded.
Ontology-specific knowledge (class names, material type rules, annotation
routing) is loaded from per-ontology config files, falling back to generic
labels when no config is available.
"""

import argparse
import json
import os
import sys
from typing import Dict, List, Optional

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPT_DIR)
from crystal_mapper import map_crystal  # noqa: E402
from concept_mapper import _load_summary, _load_mappings  # noqa: E402


# ---------- Universal knowledge (periodic table) ----------

ELEMENT_SYMBOLS = {
    "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne",
    "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca",
    "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
    "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr",
    "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn",
    "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd",
    "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb",
    "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg",
    "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th",
    "Pa", "U", "Np", "Pu",
}

ELEMENT_NAMES = {
    "hydrogen": "H", "helium": "He", "lithium": "Li", "beryllium": "Be",
    "boron": "B", "carbon": "C", "nitrogen": "N", "oxygen": "O",
    "fluorine": "F", "neon": "Ne", "sodium": "Na", "magnesium": "Mg",
    "aluminum": "Al", "aluminium": "Al", "silicon": "Si",
    "phosphorus": "P", "sulfur": "S", "chlorine": "Cl", "argon": "Ar",
    "potassium": "K", "calcium": "Ca", "scandium": "Sc", "titanium": "Ti",
    "vanadium": "V", "chromium": "Cr", "manganese": "Mn", "iron": "Fe",
    "cobalt": "Co", "nickel": "Ni", "copper": "Cu", "zinc": "Zn",
    "gallium": "Ga", "germanium": "Ge", "arsenic": "As", "selenium": "Se",
    "bromine": "Br", "krypton": "Kr", "rubidium": "Rb", "strontium": "Sr",
    "yttrium": "Y", "zirconium": "Zr", "niobium": "Nb", "molybdenum": "Mo",
    "ruthenium": "Ru", "rhodium": "Rh", "palladium": "Pd", "silver": "Ag",
    "cadmium": "Cd", "indium": "In", "tin": "Sn", "antimony": "Sb",
    "tellurium": "Te", "iodine": "I", "xenon": "Xe", "cesium": "Cs",
    "barium": "Ba", "lanthanum": "La", "cerium": "Ce", "gold": "Au",
    "platinum": "Pt", "tungsten": "W", "lead": "Pb", "uranium": "U",
}

# ---------- Default config (generic labels) ----------

_DEFAULT_SAMPLE_SCHEMA = {
    "sample_class": "Sample",
    "sample_subclass": "Atomic Scale Sample",
    "material_class": "Material",
    "element_class": "Chemical Element",
    "element_property": "chemical_symbol",
    "atom_count_class": "Atomic Scale Sample",
    "atom_count_property": "number_of_atoms",
}

_DEFAULT_MATERIAL_TYPE_RULES = {
    "keyword_rules": [
        {"keyword": "amorphous", "fields": ["material", "structure"], "maps_to": "Amorphous Material"},
        {"keyword": "poly", "fields": ["material", "structure"], "maps_to": "Polycrystal"},
        {"keyword": "bicrystal", "fields": ["material"], "maps_to": "Bicrystal"},
    ],
    "default": "Crystalline Material",
}

_DEFAULT_ANNOTATION_ROUTING = {
    "unit_cell_indicators": ["length", "angle", "Bravais"],
    "crystal_structure_class": "Crystal Structure",
    "unit_cell_class": "Unit Cell",
}


def _resolve_elements(sample: Dict) -> List[str]:
    """Extract chemical element symbols from sample description."""
    elements = []

    # Check 'elements' field (list or comma-separated)
    if "elements" in sample:
        val = sample["elements"]
        if isinstance(val, list):
            items = val
        else:
            items = [x.strip() for x in str(val).split(",")]
        for item in items:
            item_stripped = item.strip()
            if item_stripped in ELEMENT_SYMBOLS:
                elements.append(item_stripped)
            elif item_stripped.lower() in ELEMENT_NAMES:
                elements.append(ELEMENT_NAMES[item_stripped.lower()])

    # Check 'material' field for element names
    material = sample.get("material", "")
    if isinstance(material, str):
        mat_lower = material.lower().strip()
        if mat_lower in ELEMENT_NAMES:
            sym = ELEMENT_NAMES[mat_lower]
            if sym not in elements:
                elements.append(sym)
        elif material.strip() in ELEMENT_SYMBOLS:
            if material.strip() not in elements:
                elements.append(material.strip())

    return elements


def _classify_material(sample: Dict, rules: Dict) -> str:
    """Classify material type using keyword rules from config."""
    keyword_rules = rules.get("keyword_rules", [])
    default = rules.get("default", "Crystalline Material")

    for rule in keyword_rules:
        keyword = rule["keyword"].lower()
        fields = rule.get("fields", ["material", "structure"])
        for field in fields:
            field_val = str(sample.get(field, "")).lower()
            if keyword in field_val:
                return rule["maps_to"]

    return default


_MAX_SAMPLE_KEYS = 100
_MAX_STR_VALUE_LEN = 500


def _validate_against_summary(annotations: List[Dict], summary: Dict) -> None:
    """Flag emitted classes/properties that do not exist in the ontology.

    The ``summary`` dict (as produced by ontology_summarizer.py) is the
    authoritative list of classes and properties for the loaded ontology.
    Any emitted class absent from ``summary['classes']`` or property absent
    from both property tables is annotated in place with a
    ``validation_warning`` key and its confidence is dropped to 0.0, mirroring
    concept_mapper's behavior of refusing to vouch for unresolvable terms.

    A summary without a populated ``classes`` table (e.g. a bare/synthetic
    summary) disables validation so generic/test usage is unaffected.
    """
    classes = summary.get("classes") or {}
    if not classes:
        return
    obj_props = summary.get("object_properties") or {}
    data_props = summary.get("data_properties") or {}
    known_props = set(obj_props) | set(data_props)

    for ann in annotations:
        if ann.get("type") == "warning":
            continue
        # Validate the most specific class label emitted for this annotation.
        cls = ann.get("subclass") or ann.get("class")
        if cls is not None and cls not in classes:
            ann["validation_warning"] = (
                f"class '{cls}' is not defined in the loaded ontology"
            )
            ann["confidence"] = 0.0
        prop = ann.get("property")
        if prop is not None and prop not in known_props:
            existing = ann.get("validation_warning")
            msg = f"property '{prop}' is not defined in the loaded ontology"
            ann["validation_warning"] = f"{existing}; {msg}" if existing else msg
            ann["confidence"] = 0.0


def annotate_sample(
    summary: Dict,
    sample: Dict,
    mappings: Optional[Dict] = None,
) -> Dict:
    """Produce ontology annotations for a material sample description.

    Every emitted class/property is validated against ``summary`` (the
    authoritative ontology vocabulary). Terms not present in the ontology are
    flagged with a ``validation_warning`` and confidence 0.0 instead of being
    emitted silently, so e.g. running ``--ontology asmo`` on a crystalline
    sample no longer yields unresolvable CMSO-style crystal terms.

    Parameters
    ----------
    summary : dict
        Ontology summary. Used both for context and to validate that every
        emitted class/property actually exists in the ontology.
    sample : dict
        Sample description with keys like: material, structure, lattice_a,
        lattice_b, lattice_c, alpha, beta, gamma, space_group, elements, etc.
    mappings : dict, optional
        Per-ontology mapping config. If None, uses generic defaults.

    Returns
    -------
    dict
        annotations, sample_type, material_type, unmapped_fields,
        suggested_properties.

    Raises
    ------
    ValueError
        If sample is empty, not a dict, or exceeds size limits.
    """
    if not isinstance(sample, dict) or not sample:
        raise ValueError("Sample must be a non-empty dict")

    if len(sample) > _MAX_SAMPLE_KEYS:
        raise ValueError(f"Sample has too many keys (max {_MAX_SAMPLE_KEYS})")
    for key, value in sample.items():
        if not isinstance(key, str):
            raise ValueError("Sample keys must be strings")
        if isinstance(value, str) and len(value) > _MAX_STR_VALUE_LEN:
            raise ValueError(
                f"Sample value for '{key}' exceeds maximum length of "
                f"{_MAX_STR_VALUE_LEN} characters"
            )

    if mappings is None:
        mappings = {}

    # Load ontology-specific config, falling back to defaults
    schema = mappings.get("sample_schema", _DEFAULT_SAMPLE_SCHEMA)
    type_rules = mappings.get("material_type_rules", _DEFAULT_MATERIAL_TYPE_RULES)
    routing = mappings.get("annotation_routing", _DEFAULT_ANNOTATION_ROUTING)
    crystal_output = mappings.get("crystal_output")

    annotations: List[Dict] = []
    unmapped_fields: List[str] = []

    # Classify material type using config-driven rules
    material_type = _classify_material(sample, type_rules)
    is_amorphous = material_type.lower().startswith("amorphous")

    sample_class = schema.get("sample_class", "Sample")
    sample_subclass = schema.get("sample_subclass", "Atomic Scale Sample")
    material_class = schema.get("material_class", "Material")

    sample_type = sample_subclass

    annotations.append({
        "class": sample_class,
        "subclass": sample_type,
        "confidence": 1.0,
    })
    annotations.append({
        "class": material_class,
        "subclass": material_type,
        "confidence": 0.9 if is_amorphous else 0.95,
    })

    # Map crystal structure if not amorphous
    if not is_amorphous:
        crystal_result = map_crystal(
            system=sample.get("system"),
            bravais=sample.get("bravais") or sample.get("structure"),
            space_group=sample.get("space_group"),
            a=sample.get("lattice_a"),
            b=sample.get("lattice_b"),
            c=sample.get("lattice_c"),
            alpha=sample.get("alpha"),
            beta=sample.get("beta"),
            gamma=sample.get("gamma"),
            crystal_output=crystal_output,
            # The sample 'structure' field is free text (e.g. "rocksalt",
            # "perovskite") that need not be one of the 14 Bravais lattices.
            # Tolerate unrecognized values (warn, don't crash); the strict
            # --bravais CLI path still validates.
            strict_bravais=False,
        )

        # Route properties to classes using config
        unit_cell_indicators = routing.get("unit_cell_indicators", ["length", "angle", "Bravais"])
        unit_cell_class = routing.get("unit_cell_class", "Unit Cell")
        crystal_structure_class = routing.get("crystal_structure_class", "Crystal Structure")

        for prop in crystal_result["ontology_properties"]:
            prop_name = prop["property"]
            is_unit_cell = any(ind in prop_name for ind in unit_cell_indicators)
            annotations.append({
                "class": unit_cell_class if is_unit_cell else crystal_structure_class,
                "property": prop_name,
                "value": prop["value"],
                "confidence": 0.95,
            })
        if crystal_result["validation_warnings"]:
            for w in crystal_result["validation_warnings"]:
                annotations.append({
                    "type": "warning",
                    "message": w,
                    "confidence": 1.0,
                })

    # Map elements
    element_class = schema.get("element_class", "Chemical Element")
    element_property = schema.get("element_property", "chemical_symbol")
    elements = _resolve_elements(sample)
    for elem in elements:
        annotations.append({
            "class": element_class,
            "property": element_property,
            "value": elem,
            "confidence": 1.0,
        })

    # Map number of atoms
    atom_count_class = schema.get("atom_count_class", "Atomic Scale Sample")
    atom_count_property = schema.get("atom_count_property", "number_of_atoms")
    if "num_atoms" in sample or "number_of_atoms" in sample:
        n_atoms = sample.get("num_atoms") or sample.get("number_of_atoms")
        annotations.append({
            "class": atom_count_class,
            "property": atom_count_property,
            "value": n_atoms,
            "confidence": 1.0,
        })

    # Check for unmapped fields
    known_fields = {
        "material", "structure", "system", "bravais", "space_group",
        "lattice_a", "lattice_b", "lattice_c", "alpha", "beta", "gamma",
        "elements", "num_atoms", "number_of_atoms",
    }
    for key in sample:
        if key not in known_fields:
            unmapped_fields.append(key)

    # Suggest additional properties
    suggested = []
    if not elements:
        suggested.append("elements (list of chemical element symbols)")
    if sample.get("space_group") is None and not is_amorphous:
        suggested.append("space_group (integer 1-230)")
    if sample.get("lattice_a") is None and not is_amorphous:
        suggested.append("lattice_a (lattice parameter a in angstroms)")

    # Validate every emitted term against the loaded ontology. Terms not in
    # the ontology are flagged in place and their confidence dropped to 0.0.
    _validate_against_summary(annotations, summary)
    invalid_terms = sorted({
        ann["validation_warning"]
        for ann in annotations
        if "validation_warning" in ann
    })

    return {
        "annotations": annotations,
        "sample_type": sample_type,
        "material_type": material_type,
        "unmapped_fields": unmapped_fields,
        "suggested_properties": suggested,
        "validation_warnings": invalid_terms,
    }


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Annotate a material sample with ontology terms.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--ontology", help="Ontology name (e.g., cmso)")
    group.add_argument("--summary-file", help="Path to summary JSON file")
    parser.add_argument("--sample", help="JSON string describing the sample")
    parser.add_argument("--sample-file", help="Path to JSON file describing the sample")
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
        # Load per-ontology mappings config
        mappings = _load_mappings(ontology=args.ontology)

        if args.sample_file:
            with open(args.sample_file, encoding="utf-8") as f:
                sample = json.load(f)
        elif args.sample:
            sample = json.loads(args.sample)
        else:
            raise ValueError("Provide --sample or --sample-file")

        result = annotate_sample(summary=summary, sample=sample, mappings=mappings)
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
            "summary_file": args.summary_file,
            "sample": args.sample,
            "sample_file": args.sample_file,
        },
        "results": result,
    }

    if args.json:
        json.dump(payload, sys.stdout, indent=2)
        print()
    else:
        print(f"Sample type: {result['sample_type']}")
        print(f"Material type: {result['material_type']}")
        print("Annotations:")
        for ann in result["annotations"]:
            if ann.get("type") == "warning":
                print(f"  WARNING: {ann['message']}")
            elif "property" in ann:
                line = f"  {ann['class']}.{ann['property']} = {ann['value']}"
                if ann.get("validation_warning"):
                    line += f"  [!] {ann['validation_warning']}"
                print(line)
            else:
                cls = ann.get("subclass") or ann.get("class")
                line = f"  Class: {cls}"
                if ann.get("validation_warning"):
                    line += f"  [!] {ann['validation_warning']}"
                print(line)
        if result["validation_warnings"]:
            print("Validation warnings (terms not in ontology):")
            for w in result["validation_warnings"]:
                print(f"  - {w}")
        if result["unmapped_fields"]:
            print(f"Unmapped: {', '.join(result['unmapped_fields'])}")
        if result["suggested_properties"]:
            print("Suggested:")
            for s in result["suggested_properties"]:
                print(f"  {s}")


if __name__ == "__main__":
    main()
