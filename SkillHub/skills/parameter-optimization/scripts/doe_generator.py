#!/usr/bin/env python3
import argparse
import json
import random
import sys
import warnings
from typing import Dict, List


def lhs_samples(dim: int, budget: int, seed: int) -> List[List[float]]:
    rng = random.Random(seed)
    samples = []
    for d in range(dim):
        points = [(i + rng.random()) / budget for i in range(budget)]
        rng.shuffle(points)
        if d == 0:
            samples = [[p] for p in points]
        else:
            for i, p in enumerate(points):
                samples[i].append(p)
    return samples


def quasi_random_samples(dim: int, budget: int, seed: int) -> List[List[float]]:
    """Generate quasi-random samples using additive recurrence.

    Note: This is a simplified quasi-random sequence, not a true Sobol sequence.
    For production use, consider scipy.stats.qmc.Sobol for actual Sobol sequences.
    """
    rng = random.Random(seed)
    # Use golden ratio based quasi-random for better uniformity than pure random
    phi = (1 + 5 ** 0.5) / 2  # golden ratio
    alpha = [((i + 1) * phi) % 1 for i in range(dim)]
    samples = []
    start = rng.random()
    for n in range(budget):
        point = [((start + (n + 1) * alpha[d]) % 1) for d in range(dim)]
        samples.append(point)
    return samples


def factorial_levels_from_budget(dim: int, budget: int) -> int:
    """Back-compute the per-parameter level count from a sample budget."""
    return max(int(round(budget ** (1.0 / dim))), 2)


def factorial_samples(dim: int, levels: int) -> List[List[float]]:
    """Full factorial grid with `levels` evenly spaced values per parameter.

    Produces exactly levels**dim samples (all corners/combinations).
    """
    levels = max(levels, 2)
    grid = [i / (levels - 1) for i in range(levels)]
    samples = [[]]
    for _ in range(dim):
        samples = [s + [g] for s in samples for g in grid]
    return samples


MAX_DIM = 1000
MAX_BUDGET = 1_000_000
MAX_LEVELS = 1000


def generate_doe(
    dim: int,
    budget: int,
    method: str,
    seed: int,
    levels: int = None,
) -> Dict[str, object]:
    if dim <= 0:
        raise ValueError("params must be positive")
    if dim > MAX_DIM:
        raise ValueError(f"params ({dim}) exceeds maximum ({MAX_DIM})")
    valid_methods = {"lhs", "sobol", "quasi-random", "factorial"}
    if method not in valid_methods:
        raise ValueError(f"method must be one of: {', '.join(sorted(valid_methods))}")

    # --budget is optional only for factorial when --levels is given explicitly.
    if budget is None:
        if not (method == "factorial" and levels is not None):
            raise ValueError("budget must be positive")
    else:
        if budget <= 0:
            raise ValueError("budget must be positive")
        if budget > MAX_BUDGET:
            raise ValueError(f"budget ({budget}) exceeds maximum ({MAX_BUDGET})")

    note = None
    if method == "lhs":
        samples = lhs_samples(dim, budget, seed)
    elif method in {"sobol", "quasi-random"}:
        if method == "sobol":
            warnings.warn(
                "Method 'sobol' is deprecated; use 'quasi-random' instead. "
                "This is NOT a true Sobol sequence but a quasi-random additive recurrence.",
                DeprecationWarning,
                stacklevel=2,
            )
        samples = quasi_random_samples(dim, budget, seed)
    else:  # factorial
        levels_explicit = levels is not None
        if levels_explicit:
            if levels < 2:
                raise ValueError("levels must be >= 2")
            if levels > MAX_LEVELS:
                raise ValueError(f"levels ({levels}) exceeds maximum ({MAX_LEVELS})")
        else:
            levels = factorial_levels_from_budget(dim, budget)
        expected = levels ** dim
        if expected > MAX_BUDGET:
            raise ValueError(
                f"factorial design with {levels} levels^{dim} dims = {expected} samples "
                f"exceeds budget maximum ({MAX_BUDGET})"
            )
        samples = factorial_samples(dim, levels)
        realized = len(samples)
        # Only warn when the user supplied a --budget that we could not honor
        # exactly. When --levels is explicit, the budget is intentionally ignored.
        if not levels_explicit and realized != budget:
            note = (
                f"factorial realized {realized} samples ({levels} levels^{dim} dims) "
                f"for requested budget {budget}; budget is not honored exactly for "
                f"factorial designs. Pass --levels to set the grid resolution explicitly."
            )
            warnings.warn(note, stacklevel=2)

    result = {
        "method": method,
        "samples": samples,
        "coverage": {"count": len(samples), "dimension": dim},
    }
    if method == "factorial":
        result["coverage"]["levels"] = levels
        result["requested_budget"] = budget
    if note is not None:
        result["note"] = note
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate design of experiments samples.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--params", type=int, required=True, help="Number of parameters")
    parser.add_argument(
        "--budget",
        type=int,
        default=None,
        help="Sample budget (required for all methods except factorial when "
        "--levels is given)",
    )
    parser.add_argument(
        "--method",
        choices=["lhs", "sobol", "quasi-random", "factorial"],
        default="lhs",
        help="DOE method (sobol uses quasi-random sequence)",
    )
    parser.add_argument("--seed", type=int, default=0, help="Random seed")
    parser.add_argument(
        "--levels",
        type=int,
        default=None,
        help="Levels per parameter for factorial method (overrides --budget; "
        "samples = levels**params)",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        result = generate_doe(
            args.params, args.budget, args.method, args.seed, args.levels
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)

    payload = {
        "inputs": {
            "params": args.params,
            "budget": args.budget,
            "method": args.method,
            "seed": args.seed,
            "levels": args.levels,
        },
        "results": result,
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return

    print("DOE samples")
    print(f"  method: {result['method']}")
    print(f"  count: {result['coverage']['count']}")


if __name__ == "__main__":
    main()
