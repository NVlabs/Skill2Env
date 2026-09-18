#!/usr/bin/env python3
"""Map crystal structure parameters to ontology terms.

Universal crystallography (7 crystal systems, 14 Bravais lattices,
space groups 1-230, lattice validation) is hardcoded as immutable physics.
Ontology-specific output (class names, property names) is loaded from
per-ontology config files, falling back to generic labels.
"""

import argparse
import json
import math
import os
import sys
from typing import Dict, List, Optional

# ---------- Universal crystallography (immutable physics) ----------

# Crystal system definitions: constraints on lattice parameters
CRYSTAL_SYSTEMS = {
    "cubic": {
        "constraints": "a=b=c, alpha=beta=gamma=90",
        "bravais": ["cP", "cI", "cF"],
        "space_groups": (195, 230),
    },
    "hexagonal": {
        "constraints": "a=b!=c, alpha=beta=90, gamma=120",
        "bravais": ["hP"],
        "space_groups": (168, 194),
    },
    "trigonal": {
        "constraints": "a=b=c, alpha=beta=gamma!=90 (rhombohedral) or a=b!=c (hexagonal)",
        "bravais": ["hR", "hP"],
        "space_groups": (143, 167),
    },
    "tetragonal": {
        "constraints": "a=b!=c, alpha=beta=gamma=90",
        "bravais": ["tP", "tI"],
        "space_groups": (75, 142),
    },
    "orthorhombic": {
        "constraints": "a!=b!=c, alpha=beta=gamma=90",
        "bravais": ["oP", "oC", "oI", "oF"],
        "space_groups": (16, 74),
    },
    "monoclinic": {
        "constraints": "a!=b!=c, alpha=gamma=90, beta!=90",
        "bravais": ["mP", "mC"],
        "space_groups": (3, 15),
    },
    "triclinic": {
        "constraints": "a!=b!=c, alpha!=beta!=gamma",
        "bravais": ["aP"],
        "space_groups": (1, 2),
    },
}

# Common Bravais lattice aliases
BRAVAIS_ALIASES = {
    "fcc": "cF",
    "bcc": "cI",
    "sc": "cP",
    "simple cubic": "cP",
    "body-centered cubic": "cI",
    "face-centered cubic": "cF",
    "hcp": "hP",
    "hexagonal": "hP",
    "rhombohedral": "hR",
    "simple tetragonal": "tP",
    "body-centered tetragonal": "tI",
    "simple orthorhombic": "oP",
    "base-centered orthorhombic": "oC",
    "body-centered orthorhombic": "oI",
    "face-centered orthorhombic": "oF",
    "simple monoclinic": "mP",
    "base-centered monoclinic": "mC",
    "triclinic": "aP",
    "cf": "cF",
    "ci": "cI",
    "cp": "cP",
    "hp": "hP",
    "hr": "hR",
    "tp": "tP",
    "ti": "tI",
    "op": "oP",
    "oc": "oC",
    "oi": "oI",
    "of": "oF",
    "mp": "mP",
    "mc": "mC",
    "ap": "aP",
}

# The 14 canonical Bravais lattice Pearson symbols (the resolved/output form).
VALID_BRAVAIS_SYMBOLS = {
    "cP", "cI", "cF",
    "tP", "tI",
    "oP", "oC", "oI", "oF",
    "hP", "hR",
    "mP", "mC",
    "aP",
}

# Default output config (generic labels, no ontology-specific names)
_DEFAULT_CRYSTAL_OUTPUT = {
    "base_classes": [
        "Sample",
        "Crystalline Material",
        "Crystal Structure",
        "Unit Cell",
    ],
    "space_group_class": "Space Group",
    "lattice_parameter_class": "Lattice Parameter",
    "property_map": {
        "bravais_lattice": "bravais_lattice",
        "space_group_number": "space_group_number",
        "length_x": "length_x",
        "length_y": "length_y",
        "length_z": "length_z",
        "angle_alpha": "angle_alpha",
        "angle_beta": "angle_beta",
        "angle_gamma": "angle_gamma",
    },
}


def _system_from_space_group(sg: int) -> Optional[str]:
    """Infer crystal system from space group number."""
    if not 1 <= sg <= 230:
        return None
    for system, info in CRYSTAL_SYSTEMS.items():
        lo, hi = info["space_groups"]
        if lo <= sg <= hi:
            return system
    return None


def _validate_lattice(system: str, a: Optional[float],
                      b: Optional[float], c: Optional[float],
                      alpha: Optional[float], beta: Optional[float],
                      gamma: Optional[float]) -> List[str]:
    """Validate lattice parameters against crystal system constraints."""
    warnings = []
    tol = 1e-4

    if system == "cubic":
        if a is not None and b is not None and abs(a - b) > tol:
            warnings.append(f"Cubic requires a=b, but a={a}, b={b}")
        if a is not None and c is not None and abs(a - c) > tol:
            warnings.append(f"Cubic requires a=c, but a={a}, c={c}")
        for name, val in [("alpha", alpha), ("beta", beta), ("gamma", gamma)]:
            if val is not None and abs(val - 90.0) > tol:
                warnings.append(f"Cubic requires {name}=90, but {name}={val}")

    elif system == "hexagonal":
        if a is not None and b is not None and abs(a - b) > tol:
            warnings.append(f"Hexagonal requires a=b, but a={a}, b={b}")
        for name, val in [("alpha", alpha), ("beta", beta)]:
            if val is not None and abs(val - 90.0) > tol:
                warnings.append(f"Hexagonal requires {name}=90, but {name}={val}")
        if gamma is not None and abs(gamma - 120.0) > tol:
            warnings.append(f"Hexagonal requires gamma=120, but gamma={gamma}")

    elif system == "tetragonal":
        if a is not None and b is not None and abs(a - b) > tol:
            warnings.append(f"Tetragonal requires a=b, but a={a}, b={b}")
        for name, val in [("alpha", alpha), ("beta", beta), ("gamma", gamma)]:
            if val is not None and abs(val - 90.0) > tol:
                warnings.append(f"Tetragonal requires {name}=90, but {name}={val}")

    elif system == "orthorhombic":
        for name, val in [("alpha", alpha), ("beta", beta), ("gamma", gamma)]:
            if val is not None and abs(val - 90.0) > tol:
                warnings.append(
                    f"Orthorhombic requires {name}=90, but {name}={val}"
                )

    elif system == "monoclinic":
        for name, val in [("alpha", alpha), ("gamma", gamma)]:
            if val is not None and abs(val - 90.0) > tol:
                warnings.append(f"Monoclinic requires {name}=90, but {name}={val}")

    return warnings


def _load_crystal_output(ontology: Optional[str] = None) -> Dict:
    """Load ontology-specific output config, or fall back to defaults."""
    if not ontology:
        return _DEFAULT_CRYSTAL_OUTPUT

    explorer_ref = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "..", "ontology-explorer", "references",
        "ontology_registry.json",
    )
    if not os.path.isfile(explorer_ref):
        return _DEFAULT_CRYSTAL_OUTPUT

    with open(explorer_ref, encoding="utf-8") as f:
        registry = json.load(f)

    key = ontology.lower()
    if key not in registry:
        return _DEFAULT_CRYSTAL_OUTPUT

    mappings_file = registry[key].get("mappings_file")
    if not mappings_file:
        return _DEFAULT_CRYSTAL_OUTPUT

    mapper_ref = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "references",
    )
    path = os.path.join(mapper_ref, mappings_file)
    if not os.path.isfile(path):
        return _DEFAULT_CRYSTAL_OUTPUT

    with open(path, encoding="utf-8") as f:
        mappings = json.load(f)

    return mappings.get("crystal_output", _DEFAULT_CRYSTAL_OUTPUT)


def map_crystal(
    system: Optional[str] = None,
    bravais: Optional[str] = None,
    space_group: Optional[int] = None,
    a: Optional[float] = None,
    b: Optional[float] = None,
    c: Optional[float] = None,
    alpha: Optional[float] = None,
    beta: Optional[float] = None,
    gamma: Optional[float] = None,
    ontology: Optional[str] = None,
    crystal_output: Optional[Dict] = None,
    strict_bravais: bool = True,
) -> Dict:
    """Map crystal structure parameters to ontology terms.

    Parameters
    ----------
    system : str, optional
        Crystal system name (cubic, hexagonal, etc.).
    bravais : str, optional
        Bravais lattice type (FCC, BCC, cF, cI, etc.).
    space_group : int, optional
        Space group number (1-230).
    a, b, c : float, optional
        Lattice parameters in angstroms.
    alpha, beta, gamma : float, optional
        Lattice angles in degrees.
    ontology : str, optional
        Ontology name for loading output config. Ignored if crystal_output given.
    crystal_output : dict, optional
        Explicit output config (overrides ontology-based loading).

    Returns
    -------
    dict
        ontology_classes, ontology_properties, validation, and inferred parameters.

    Raises
    ------
    ValueError
        If inputs are invalid.
    """
    # Validate numeric inputs
    for name, val in [("a", a), ("b", b), ("c", c)]:
        if val is not None:
            if not math.isfinite(val):
                raise ValueError(f"{name} must be finite (no NaN or Inf)")
            if val <= 0:
                raise ValueError(f"{name} must be positive")
    for name, val in [("alpha", alpha), ("beta", beta), ("gamma", gamma)]:
        if val is not None:
            if not math.isfinite(val):
                raise ValueError(f"{name} must be finite (no NaN or Inf)")
            if val <= 0 or val >= 180:
                raise ValueError(f"{name} must be between 0 and 180 degrees")

    if space_group is not None and not 1 <= space_group <= 230:
        raise ValueError("space_group must be between 1 and 230")

    # Resolve Bravais lattice alias, validating against the fixed set of
    # recognized lattice symbols (aliases plus the 14 canonical Pearson codes).
    resolved_bravais = None
    unrecognized_bravais_warning = None
    if bravais:
        if not isinstance(bravais, str):
            raise ValueError("bravais must be a string")
        key = bravais.lower()
        if key in BRAVAIS_ALIASES:
            resolved_bravais = BRAVAIS_ALIASES[key]
        elif bravais in VALID_BRAVAIS_SYMBOLS:
            resolved_bravais = bravais
        elif strict_bravais:
            recognized = ", ".join(sorted(VALID_BRAVAIS_SYMBOLS))
            raise ValueError(
                f"Unrecognized Bravais lattice '{bravais}'. "
                f"Use a common name (FCC, BCC, HCP, ...) or a Pearson "
                f"symbol ({recognized})"
            )
        else:
            # Tolerant path (e.g. free-text sample 'structure' field): pass the
            # value through unmapped and surface a warning instead of crashing
            # the whole annotation. The strict CLI path still rejects it.
            resolved_bravais = None
            unrecognized_bravais_warning = (
                f"Unrecognized Bravais lattice '{bravais}'; left unmapped. "
                f"Use a common name (FCC, BCC, HCP, ...) or a Pearson symbol "
                f"to map it to a lattice term."
            )

    # Infer crystal system from space group
    inferred_system = None
    if space_group is not None:
        inferred_system = _system_from_space_group(space_group)

    # Determine effective system
    effective_system = system or inferred_system

    # Validate lattice parameters against system
    validation_warnings = []
    if effective_system:
        validation_warnings = _validate_lattice(
            effective_system, a, b, c, alpha, beta, gamma,
        )
    if unrecognized_bravais_warning:
        validation_warnings.append(unrecognized_bravais_warning)

    # Check system/space-group consistency
    if system and inferred_system and system != inferred_system:
        validation_warnings.append(
            f"Space group {space_group} implies {inferred_system}, "
            f"but {system} was specified"
        )

    # Load output config (ontology-specific class/property names)
    if crystal_output is None:
        crystal_output = _load_crystal_output(ontology)

    prop_map = crystal_output.get("property_map", _DEFAULT_CRYSTAL_OUTPUT["property_map"])

    # Build ontology classes list
    ontology_classes = list(crystal_output.get("base_classes", _DEFAULT_CRYSTAL_OUTPUT["base_classes"]))
    if space_group is not None:
        ontology_classes.append(crystal_output.get("space_group_class", "Space Group"))
    if any(v is not None for v in [a, b, c]):
        ontology_classes.append(crystal_output.get("lattice_parameter_class", "Lattice Parameter"))

    # Build ontology properties list
    ontology_properties = []
    if resolved_bravais:
        ontology_properties.append({
            "property": prop_map.get("bravais_lattice", "bravais_lattice"),
            "value": resolved_bravais,
            "type": "data",
        })
    if space_group is not None:
        ontology_properties.append({
            "property": prop_map.get("space_group_number", "space_group_number"),
            "value": space_group,
            "type": "data",
        })
    for param_name, param_val, prop_key in [
        ("a", a, "length_x"),
        ("b", b, "length_y"),
        ("c", c, "length_z"),
        ("alpha", alpha, "angle_alpha"),
        ("beta", beta, "angle_beta"),
        ("gamma", gamma, "angle_gamma"),
    ]:
        if param_val is not None:
            ontology_properties.append({
                "property": prop_map.get(prop_key, prop_key),
                "value": param_val,
                "type": "data",
            })

    return {
        "ontology_classes": ontology_classes,
        "ontology_properties": ontology_properties,
        "effective_system": effective_system,
        "inferred_system": inferred_system,
        "bravais_lattice": resolved_bravais,
        "validation_warnings": validation_warnings,
        "notes": [],
    }


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Map crystal structure parameters to ontology terms.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--ontology", help="Ontology name for output labels (e.g., cmso)")
    parser.add_argument("--system", help="Crystal system (cubic, hexagonal, ...)")
    parser.add_argument("--bravais", help="Bravais lattice (FCC, BCC, cF, cI, ...)")
    parser.add_argument("--space-group", type=int, help="Space group number (1-230)")
    parser.add_argument("--a", type=float, help="Lattice parameter a (angstroms)")
    parser.add_argument("--b", type=float, help="Lattice parameter b (angstroms)")
    parser.add_argument("--c", type=float, help="Lattice parameter c (angstroms)")
    parser.add_argument("--alpha", type=float, help="Lattice angle alpha (degrees)")
    parser.add_argument("--beta", type=float, help="Lattice angle beta (degrees)")
    parser.add_argument("--gamma", type=float, help="Lattice angle gamma (degrees)")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser.parse_args()


def main() -> None:
    """CLI entry point."""
    args = parse_args()
    try:
        result = map_crystal(
            system=args.system,
            bravais=args.bravais,
            space_group=args.space_group,
            a=args.a,
            b=args.b,
            c=args.c,
            alpha=args.alpha,
            beta=args.beta,
            gamma=args.gamma,
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
            "system": args.system,
            "bravais": args.bravais,
            "space_group": args.space_group,
            "a": args.a, "b": args.b, "c": args.c,
            "alpha": args.alpha, "beta": args.beta, "gamma": args.gamma,
        },
        "results": result,
    }

    if args.json:
        json.dump(payload, sys.stdout, indent=2)
        print()
    else:
        print(f"Crystal system: {result['effective_system'] or 'unknown'}")
        if result["bravais_lattice"]:
            print(f"Bravais lattice: {result['bravais_lattice']}")
        print(f"Ontology classes: {', '.join(result['ontology_classes'])}")
        if result["ontology_properties"]:
            print("Ontology properties:")
            for p in result["ontology_properties"]:
                print(f"  {p['property']} = {p['value']}")
        for w in result["validation_warnings"]:
            print(f"  WARNING: {w}")


if __name__ == "__main__":
    main()
