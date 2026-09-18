#!/usr/bin/env python3
import argparse
import json
import math
import sys
from typing import Dict


def estimate_truncation_error(dx: float, accuracy: int, scale: float) -> Dict[str, object]:
    if not math.isfinite(dx) or dx <= 0:
        raise ValueError("dx must be positive")
    if accuracy <= 0:
        raise ValueError("accuracy must be positive")
    if accuracy > 12:
        raise ValueError("accuracy must be <= 12")
    if not math.isfinite(scale) or scale < 0:
        raise ValueError("scale must be non-negative")

    error_scale = scale * (dx ** accuracy)
    reduction_if_halved = 2 ** accuracy
    return {
        "error_scale": error_scale,
        "order": accuracy,
        "reduction_if_halved": reduction_if_halved,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Estimate truncation error scaling for a scheme.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--dx", type=float, required=True, help="Grid spacing")
    parser.add_argument("--accuracy", type=int, required=True, help="Scheme order")
    parser.add_argument(
        "--scale",
        type=float,
        default=1.0,
        help="Scale of higher derivative (C term)",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        result = estimate_truncation_error(args.dx, args.accuracy, args.scale)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)

    payload = {
        "inputs": {
            "dx": args.dx,
            "accuracy": args.accuracy,
            "scale": args.scale,
        },
        "results": result,
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return

    print("Truncation error estimate")
    print(f"  error_scale: {result['error_scale']:.6g}")
    print(f"  order: {result['order']}")
    print(f"  reduction_if_halved: {result['reduction_if_halved']}")


if __name__ == "__main__":
    main()
