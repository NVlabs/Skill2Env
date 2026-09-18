#!/usr/bin/env python3
import argparse
import json
import math
import sys
from typing import Dict, List, Optional


def fornberg_coefficients(x: List[float], x0: float, m: int) -> List[float]:
    n = len(x)
    if n == 0:
        raise ValueError("x list must be non-empty")
    if m < 0:
        raise ValueError("m must be non-negative")
    c = [[0.0 for _ in range(m + 1)] for _ in range(n)]
    c[0][0] = 1.0
    c1 = 1.0
    c4 = x[0] - x0
    for i in range(1, n):
        mn = min(i, m)
        c2 = 1.0
        c5 = c4
        c4 = x[i] - x0
        for j in range(i):
            c3 = x[i] - x[j]
            if c3 == 0.0:
                raise ValueError("x points must be distinct")
            c2 *= c3
            if j == i - 1:
                for k in range(mn, 0, -1):
                    c[i][k] = (c1 * (k * c[i - 1][k - 1] - c5 * c[i - 1][k])) / c2
                c[i][0] = (-c1 * c5 * c[i - 1][0]) / c2
            for k in range(mn, 0, -1):
                c[j][k] = (c4 * c[j][k] - k * c[j][k - 1]) / c3
            c[j][0] = (c4 * c[j][0]) / c3
        c1 = c2
    return [c[i][m] for i in range(n)]


MAX_ORDER = 6
MAX_ACCURACY = 8
MAX_OFFSETS = 51


def stencil_offsets(order: int, accuracy: int, scheme: str) -> List[int]:
    if order <= 0:
        raise ValueError("order must be positive")
    if order > MAX_ORDER:
        raise ValueError(f"order must be <= {MAX_ORDER}")
    if accuracy <= 0:
        raise ValueError("accuracy must be positive")
    if accuracy > MAX_ACCURACY:
        raise ValueError(f"accuracy must be <= {MAX_ACCURACY}")
    if scheme not in {"central", "forward", "backward"}:
        raise ValueError("scheme must be central, forward, or backward")
    if scheme == "central" and accuracy % 2 != 0:
        raise ValueError("accuracy must be even for central")

    if scheme == "central":
        points = order + accuracy if order % 2 == 1 else order + accuracy - 1
        if points % 2 == 0:
            points += 1
        radius = points // 2
        return list(range(-radius, radius + 1))

    points = order + accuracy
    if scheme == "forward":
        return list(range(0, points))
    return list(range(0, -points, -1))


def generate_stencil(
    order: int,
    accuracy: int,
    scheme: str,
    dx: float,
    offsets: Optional[List[int]],
) -> Dict[str, object]:
    if not math.isfinite(dx) or dx <= 0:
        raise ValueError("dx must be positive")
    if offsets is None:
        offsets = stencil_offsets(order, accuracy, scheme)
    if not offsets:
        raise ValueError("offsets must be non-empty")
    if len(offsets) > MAX_OFFSETS:
        raise ValueError(f"offsets list too long (max {MAX_OFFSETS})")
    if len(set(offsets)) != len(offsets):
        raise ValueError("offsets must be distinct")
    if order >= len(offsets):
        raise ValueError("number of offsets must exceed derivative order")

    x = [float(o) * dx for o in offsets]
    coeffs = fornberg_coefficients(x, 0.0, order)
    return {
        "offsets": offsets,
        "coefficients": coeffs,
        "order": order,
        "accuracy": accuracy,
        "scheme": scheme,
    }


def parse_offsets(raw: str) -> List[int]:
    if len(raw) > 512:
        raise ValueError("offset list string too long")
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    if not parts:
        raise ValueError("offset list must be a comma-separated list")
    if len(parts) > MAX_OFFSETS:
        raise ValueError(f"offsets list too long (max {MAX_OFFSETS})")
    return [int(p) for p in parts]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate finite difference stencil coefficients.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--order", type=int, required=True, help="Derivative order")
    parser.add_argument("--accuracy", type=int, default=2, help="Accuracy order")
    parser.add_argument(
        "--scheme",
        choices=["central", "forward", "backward"],
        default="central",
        help="Stencil scheme",
    )
    parser.add_argument("--dx", type=float, default=1.0, help="Grid spacing")
    parser.add_argument("--offsets", default=None, help="Custom offsets (comma-separated)")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        offsets = parse_offsets(args.offsets) if args.offsets is not None else None
        result = generate_stencil(
            order=args.order,
            accuracy=args.accuracy,
            scheme=args.scheme,
            dx=args.dx,
            offsets=offsets,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)

    payload = {
        "inputs": {
            "order": args.order,
            "accuracy": args.accuracy,
            "scheme": args.scheme,
            "dx": args.dx,
            "offsets": offsets,
        },
        "results": result,
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return

    print("Stencil")
    print(f"  offsets: {result['offsets']}")
    print(f"  coefficients: {result['coefficients']}")


if __name__ == "__main__":
    main()
