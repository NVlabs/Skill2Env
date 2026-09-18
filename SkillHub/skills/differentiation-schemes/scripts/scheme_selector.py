#!/usr/bin/env python3
import argparse
import json
import sys
from typing import Dict, List


def select_scheme(
    smooth: bool,
    periodic: bool,
    discontinuous: bool,
    order: int,
    accuracy: int,
    boundary: bool,
) -> Dict[str, object]:
    if order <= 0:
        raise ValueError("order must be positive")
    if accuracy <= 0:
        raise ValueError("accuracy must be positive")
    if discontinuous and smooth:
        raise ValueError("smooth and discontinuous cannot both be true")

    recommended: List[str] = []
    alternatives: List[str] = []
    notes: List[str] = []

    if discontinuous:
        recommended.append("Finite Volume (FV) with limiter/WENO")
        alternatives.append("Upwind FD (low order)")
        notes.append("Avoid high-order central FD near discontinuities.")
    else:
        if periodic and smooth:
            recommended.append("Spectral (Fourier)")
            alternatives.append("High-order central FD")
        elif smooth:
            recommended.append("Central FD")
            alternatives.append("Higher-order upwind (2nd/4th)")
            if accuracy >= 4:
                alternatives.append("Compact FD")
            notes.append(
                "Run truncation_error.py to quantify the accuracy gain over 1st-order upwind."
            )
        else:
            recommended.append("Upwind FD")
            alternatives.append("FV")

    if boundary:
        notes.append("Use one-sided or ghost-cell stencils at boundaries.")

    return {
        "recommended": recommended,
        "alternatives": alternatives,
        "notes": notes,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Select a differentiation scheme based on problem characteristics.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--smooth", action="store_true", help="Field is smooth")
    parser.add_argument("--discontinuous", action="store_true", help="Field has discontinuities")
    parser.add_argument("--periodic", action="store_true", help="Domain is periodic")
    parser.add_argument("--boundary", action="store_true", help="Bounded domain (non-periodic)")
    parser.add_argument("--order", type=int, required=True, help="Derivative order")
    parser.add_argument("--accuracy", type=int, default=2, help="Desired accuracy")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        result = select_scheme(
            smooth=args.smooth,
            periodic=args.periodic,
            discontinuous=args.discontinuous,
            order=args.order,
            accuracy=args.accuracy,
            boundary=args.boundary,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)

    payload = {
        "inputs": {
            "smooth": args.smooth,
            "discontinuous": args.discontinuous,
            "periodic": args.periodic,
            "boundary": args.boundary,
            "order": args.order,
            "accuracy": args.accuracy,
        },
        "results": result,
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return

    print("Scheme selection")
    print(f"  recommended: {', '.join(result['recommended'])}")
    if result["alternatives"]:
        print(f"  alternatives: {', '.join(result['alternatives'])}")
    for note in result["notes"]:
        print(f"  note: {note}")


if __name__ == "__main__":
    main()
