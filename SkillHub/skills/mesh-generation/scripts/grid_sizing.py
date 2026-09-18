#!/usr/bin/env python3
import argparse
import json
import math
import sys
from typing import Dict, Optional

# Numeric bounds to prevent resource exhaustion
MAX_LENGTH = 1e12
MAX_RESOLUTION = 10_000_000
MAX_DX = 1e12
VALID_DIMS = (1, 2, 3)


def _validate_positive_finite(name: str, value: float, upper: float) -> None:
    """Validate that a numeric parameter is finite, positive, and within bounds."""
    if not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number, got {type(value).__name__}")
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite, got {value}")
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")
    if value > upper:
        raise ValueError(f"{name} exceeds maximum ({upper}), got {value}")


def compute_grid(
    length: float,
    resolution: int,
    dims: int,
    dx: Optional[float],
) -> Dict[str, object]:
    _validate_positive_finite("length", length, MAX_LENGTH)
    _validate_positive_finite("resolution", resolution, MAX_RESOLUTION)
    if dims not in VALID_DIMS:
        raise ValueError(f"dims must be one of {VALID_DIMS}, got {dims}")

    notes = []
    if dx is None:
        # dx derived from the requested resolution: the cell count is exactly
        # the requested resolution. Do NOT recompute via ceil(length/dx) -- the
        # float round-trip can push length/dx just past an integer and yield an
        # off-by-one count (e.g. resolution=500 -> 501).
        dx = length / resolution
        _validate_positive_finite("dx", dx, MAX_DX)
        per_dim = int(resolution)
    else:
        # dx supplied explicitly: derive the count from the domain length, but
        # snap to the nearest integer when length/dx is an integer to within
        # floating-point noise (relative tolerance), so genuine partial cells
        # are preserved while float-noise off-by-ones are eliminated.
        _validate_positive_finite("dx", dx, MAX_DX)
        q = length / dx
        n = round(q)
        if n >= 1 and math.isclose(q, n, rel_tol=1e-9, abs_tol=0.0):
            per_dim = n
        else:
            per_dim = int(math.ceil(q))
        notes.append(
            f"dx specified explicitly; --resolution ({int(resolution)}) "
            f"ignored for spacing."
        )

    counts = [per_dim for _ in range(dims)]
    if dx * counts[0] < length:
        notes.append("Grid does not fully cover length; consider smaller dx.")

    return {
        "dx": dx,
        "counts": counts,
        "notes": notes,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Estimate grid spacing and cell counts.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--length", type=float, required=True, help="Domain length")
    parser.add_argument(
        "--resolution",
        type=int,
        required=True,
        help="Target number of cells along length",
    )
    parser.add_argument("--dims", type=int, default=2, help="Dimensions (1,2,3)")
    parser.add_argument("--dx", type=float, default=None, help="Override dx")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        result = compute_grid(
            length=args.length,
            resolution=args.resolution,
            dims=args.dims,
            dx=args.dx,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)

    payload = {
        "inputs": {
            "length": args.length,
            "resolution": args.resolution,
            "dims": args.dims,
            "dx": args.dx,
        },
        "results": result,
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return

    print("Grid sizing")
    print(f"  dx: {result['dx']:.6g}")
    print(f"  counts: {result['counts']}")
    for note in result["notes"]:
        print(f"  note: {note}")


if __name__ == "__main__":
    main()
