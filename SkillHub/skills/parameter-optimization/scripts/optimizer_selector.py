#!/usr/bin/env python3
import argparse
import json
import sys
from typing import Dict, List


MAX_DIM = 100_000
MAX_BUDGET = 10_000_000


def select_optimizer(dim: int, budget: int, noise: str, constraints: bool) -> Dict[str, object]:
    if dim <= 0:
        raise ValueError("dim must be positive")
    if dim > MAX_DIM:
        raise ValueError(f"dim ({dim}) exceeds maximum ({MAX_DIM})")
    if budget <= 0:
        raise ValueError("budget must be positive")
    if budget > MAX_BUDGET:
        raise ValueError(f"budget ({budget}) exceeds maximum ({MAX_BUDGET})")
    if noise not in {"low", "medium", "high"}:
        raise ValueError("noise must be low, medium, or high")

    recommended: List[str] = []
    notes: List[str] = []
    if dim <= 10 and budget <= 100:
        recommended.append("Bayesian Optimization")
    elif dim <= 20:
        recommended.append("CMA-ES")
    else:
        recommended.append("Random Search")

    if noise == "high":
        notes.append("Use noise-aware acquisition or resampling.")
    if constraints:
        notes.append("Use constrained BO or penalty methods.")

    expected = min(budget, max(20, dim * 10))
    return {
        "recommended": recommended,
        "expected_evals": expected,
        "notes": notes,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Select optimization strategy for simulation calibration.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--dim", type=int, required=True, help="Parameter dimension")
    parser.add_argument("--budget", type=int, required=True, help="Evaluation budget")
    parser.add_argument("--noise", choices=["low", "medium", "high"], default="low", help="Noise level")
    parser.add_argument("--constraints", action="store_true", help="Constraints present")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        result = select_optimizer(args.dim, args.budget, args.noise, args.constraints)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)

    payload = {
        "inputs": {
            "dim": args.dim,
            "budget": args.budget,
            "noise": args.noise,
            "constraints": args.constraints,
        },
        "results": result,
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return

    print("Optimizer selection")
    print(f"  recommended: {', '.join(result['recommended'])}")
    print(f"  expected_evals: {result['expected_evals']}")


if __name__ == "__main__":
    main()
