#!/usr/bin/env python3
import argparse
import json
import math
import sys
from typing import Dict, Optional

# Upper bound to reject unreasonable cell sizes
MAX_CELL_SIZE = 1e12


def _validate_cell_size(name: str, value: float) -> None:
    """Validate that a cell size is a finite positive number within bounds."""
    if not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number, got {type(value).__name__}")
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be a finite positive number, got {value}")
    if value > MAX_CELL_SIZE:
        raise ValueError(f"{name} exceeds maximum ({MAX_CELL_SIZE}), got {value}")


def compute_quality(
    dx: float, dy: float, dz: Optional[float] = None
) -> Dict[str, object]:
    """Estimate mesh quality from axis-aligned cell spacings.

    This script describes orthogonal Cartesian cells defined purely by their
    edge spacings (dx, dy, dz). For any such cell all interior angles are
    exactly 90 degrees, so the true angular skewness
    (max(|90 deg - theta_i|) / 90 deg, per references/quality_metrics.md) is
    identically 0 regardless of how elongated the cell is. We therefore report
    skewness = 0.0 for these cells and never flag "high_skewness".

    Elongation/anisotropy of the cell is captured separately by ``aspect_ratio``
    and the redundant convenience field ``size_anisotropy`` (= 1 - 1/AR); the
    latter is informational only and does not by itself indicate a defective
    mesh (e.g. wall-aligned boundary-layer cells are intentionally anisotropic).
    """
    for name, val in [("dx", dx), ("dy", dy), ("dz", dz)]:
        if name == "dz" and val is None:
            continue
        _validate_cell_size(name, val)

    is_2d = dz is None
    sizes = [dx, dy] if is_2d else [dx, dy, dz]
    aspect_ratio = max(sizes) / min(sizes)

    # True angular skewness of an axis-aligned rectangular cell is 0: every
    # interior angle is exactly 90 deg. Do NOT confuse this with elongation.
    skewness = 0.0
    # Redundant elongation measure kept for convenience (equals 1 - 1/AR).
    size_anisotropy = (max(sizes) - min(sizes)) / max(sizes)

    flags = []
    if aspect_ratio > 5.0:
        flags.append("high_aspect_ratio")

    result: Dict[str, object] = {
        "aspect_ratio": aspect_ratio,
        "skewness": skewness,
        "size_anisotropy": size_anisotropy,
        "quality_flags": flags,
        "dims": 2 if is_2d else 3,
    }
    if is_2d:
        result["notes"] = ["dz not supplied; treated as a 2D cell."]
    else:
        result["notes"] = []
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Estimate mesh quality metrics from spacing.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--dx", type=float, required=True, help="Cell size in x")
    parser.add_argument("--dy", type=float, required=True, help="Cell size in y")
    parser.add_argument(
        "--dz",
        type=float,
        default=None,
        help="Cell size in z (omit for a 2D cell)",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        result = compute_quality(args.dx, args.dy, args.dz)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)

    payload = {
        "inputs": {"dx": args.dx, "dy": args.dy, "dz": args.dz},
        "results": result,
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return

    print("Mesh quality")
    print(f"  dims: {result['dims']}")
    print(f"  aspect_ratio: {result['aspect_ratio']:.6g}")
    print(f"  skewness: {result['skewness']:.6g}")
    print(f"  size_anisotropy: {result['size_anisotropy']:.6g}")
    for flag in result["quality_flags"]:
        print(f"  flag: {flag}")
    for note in result["notes"]:
        print(f"  note: {note}")


if __name__ == "__main__":
    main()
