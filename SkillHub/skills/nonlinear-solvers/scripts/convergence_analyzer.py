#!/usr/bin/env python3
"""Analyze residual history to classify convergence type."""
import argparse
import json
import math
import sys
from typing import Any, Dict, List, Optional


# Security limit: cap residual-list length to prevent memory exhaustion.
MAX_LIST_LENGTH = 100_000


def _estimate_order(residuals: List[float]) -> Optional[float]:
    """Estimate the convergence order p from a residual sequence.

    Uses the standard residual-ratio estimate (references/convergence_diagnostics.md):
        p ~= log(r_{k+1}/r_k) / log(r_k/r_{k-1})
    averaged over the last few usable triples. Returns None if there are not
    enough strictly decreasing, positive residuals to form an estimate.
    """
    # Keep only the trailing positive residuals.
    positive = [r for r in residuals if r > 1e-300]
    if len(positive) < 3:
        return None

    orders: List[float] = []
    # Use up to the last 5 residuals (4 ratios, 3 order estimates).
    window = positive[-5:]
    for i in range(2, len(window)):
        r_prev, r_cur, r_next = window[i - 2], window[i - 1], window[i]
        denom_ratio = r_cur / r_prev
        numer_ratio = r_next / r_cur
        # Order estimate is only meaningful when residuals are decreasing.
        if 0.0 < denom_ratio < 1.0 and 0.0 < numer_ratio < 1.0:
            log_denom = math.log(denom_ratio)
            if abs(log_denom) > 1e-12:
                p = math.log(numer_ratio) / log_denom
                if math.isfinite(p):
                    orders.append(p)

    if not orders:
        return None
    return sum(orders) / len(orders)


def _classify_order(residuals: List[float], avg_rate: float) -> str:
    """Classify convergence type from the estimated order and average ratio.

    Textbook definitions (references/convergence_diagnostics.md):
      - linear:      r_{k+1}/r_k -> constant in (0, 1)        -> order p ~= 1
      - superlinear: r_{k+1}/r_k -> 0 with ratios decreasing  -> 1 < p < 2
      - quadratic:   r_{k+1} ~ C r_k^2                         -> order p ~= 2

    A CONSTANT contraction ratio (even a small one like 0.1) is LINEAR, not
    superlinear; superlinear requires the ratio to tend to zero.
    """
    p = _estimate_order(residuals)

    if avg_rate >= 0.9:
        return "sublinear"

    if p is None:
        # Not enough decreasing data to estimate order; fall back to rate only.
        # Without evidence that ratios are shrinking, treat as (fast) linear.
        return "linear"

    if p >= 1.8:
        return "quadratic"
    if p > 1.2:
        return "superlinear"
    # p ~= 1: constant contraction ratio -> linear (annotate 'fast' downstream).
    return "linear"


def analyze_convergence(
    residuals: List[float],
    tolerance: float = 1e-10,
) -> Dict[str, Any]:
    """Analyze residual history to classify convergence behavior.

    Args:
        residuals: List of residual norms from solver iterations
        tolerance: Convergence tolerance

    Returns:
        Dictionary with convergence analysis results
    """
    if not residuals:
        raise ValueError("residuals must not be empty")

    if len(residuals) > MAX_LIST_LENGTH:
        raise ValueError(
            f"residual list length ({len(residuals)}) exceeds limit "
            f"({MAX_LIST_LENGTH})"
        )

    if any(not math.isfinite(r) for r in residuals):
        raise ValueError("residuals must be finite")

    if any(r < 0 for r in residuals):
        raise ValueError("residuals must be non-negative")

    if not math.isfinite(tolerance) or tolerance <= 0:
        raise ValueError("tolerance must be a positive finite number")

    n = len(residuals)
    final_residual = residuals[-1]
    converged = final_residual <= tolerance

    # Handle single residual case
    if n == 1:
        return {
            "converged": converged,
            "iterations": n,
            "final_residual": final_residual,
            "convergence_type": "unknown",
            "estimated_rate": None,
            "diagnosis": "Insufficient data for convergence analysis.",
            "recommended_action": "Continue iterations to gather more data.",
        }

    # Check for divergence
    if n >= 2 and residuals[-1] > residuals[0] * 1.1:
        return {
            "converged": False,
            "iterations": n,
            "final_residual": final_residual,
            "convergence_type": "diverged",
            "estimated_rate": None,
            "diagnosis": "Residuals are increasing; solver is diverging.",
            "recommended_action": "Reduce step size, add damping, or check Jacobian accuracy.",
        }

    # Check for stagnation
    if n >= 3:
        recent = residuals[-3:]
        if len(recent) == 3:
            rel_change = abs(recent[-1] - recent[0]) / (abs(recent[0]) + 1e-30)
            if rel_change < 0.01 and not converged:
                return {
                    "converged": False,
                    "iterations": n,
                    "final_residual": final_residual,
                    "convergence_type": "stagnated",
                    "estimated_rate": None,
                    "diagnosis": "Residual has stagnated without reaching tolerance.",
                    "recommended_action": "Improve preconditioner, check for near-singularity, or use different solver.",
                }

    # Estimate convergence rate from log-residuals
    rates = []
    for i in range(1, n):
        if residuals[i - 1] > 1e-30 and residuals[i] > 1e-30:
            ratio = residuals[i] / residuals[i - 1]
            if ratio > 0 and ratio < 1:
                rates.append(ratio)

    if not rates:
        convergence_type = "unknown"
        estimated_rate = None
    else:
        avg_rate = sum(rates) / len(rates)
        estimated_rate = avg_rate

        convergence_type = _classify_order(residuals, avg_rate)

    # Generate diagnosis and recommendation
    diagnosis_map = {
        "quadratic": "Quadratic convergence indicates optimal Newton behavior.",
        "superlinear": "Superlinear convergence; quasi-Newton methods working well.",
        "linear": "Linear convergence; rate is acceptable but could be improved.",
        "sublinear": "Sublinear convergence; solver is making slow progress.",
        "unknown": "Could not determine convergence type.",
    }

    action_map = {
        "quadratic": "Continue with current solver; convergence is optimal.",
        "superlinear": "Current setup is effective; monitor for stagnation.",
        "linear": "Consider stronger preconditioner or switch to Newton if Jacobian available.",
        "sublinear": "Switch to Newton method, improve globalization, or check problem formulation.",
        "unknown": "Gather more iterations for analysis.",
    }

    diagnosis = diagnosis_map.get(convergence_type, "Unknown convergence behavior.")
    recommended_action = action_map.get(convergence_type, "Review solver configuration.")

    # Annotate fast (but still linear) convergence: a small constant contraction
    # ratio is fast-linear, not superlinear.
    if convergence_type == "linear" and estimated_rate is not None and estimated_rate < 0.2:
        diagnosis = (
            "Fast linear convergence (small constant contraction ratio); "
            "this is not superlinear, but the rate is good."
        )

    if converged:
        recommended_action = "Solver converged successfully."

    return {
        "converged": converged,
        "iterations": n,
        "final_residual": final_residual,
        "convergence_type": convergence_type,
        "estimated_rate": estimated_rate,
        "diagnosis": diagnosis,
        "recommended_action": recommended_action,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze convergence from residual history.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--residuals",
        type=str,
        required=True,
        help="Comma-separated residual values",
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=1e-10,
        help="Convergence tolerance",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    try:
        residuals = [float(x.strip()) for x in args.residuals.split(",")]
    except ValueError:
        print("Error: residuals must be comma-separated numbers", file=sys.stderr)
        sys.exit(2)

    try:
        result = analyze_convergence(
            residuals=residuals,
            tolerance=args.tolerance,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)

    payload: Dict[str, Any] = {
        "inputs": {
            "residuals": residuals,
            "tolerance": args.tolerance,
        },
        "results": result,
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False))
        return

    print("Convergence analysis")
    print(f"  converged: {result['converged']}")
    print(f"  iterations: {result['iterations']}")
    print(f"  final_residual: {result['final_residual']:.2e}")
    print(f"  convergence_type: {result['convergence_type']}")
    if result["estimated_rate"] is not None:
        print(f"  estimated_rate: {result['estimated_rate']:.4f}")
    print(f"  diagnosis: {result['diagnosis']}")
    print(f"  recommended_action: {result['recommended_action']}")


if __name__ == "__main__":
    main()
