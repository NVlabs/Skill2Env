#!/usr/bin/env python3
"""Select nonlinear solver based on problem characteristics."""
import argparse
import json
import sys
from typing import Any, Dict, List


# Security limit: cap on problem size to reject absurd / malformed input.
MAX_SIZE = 10_000_000_000  # 10 billion

# Problem-size threshold above which matrix-free / limited-memory methods are
# preferred over forming and factoring the full Jacobian. Matches the
# SKILL.md flowchart and references/solver_decision_tree.md (n >= 1000).
LARGE_PROBLEM_THRESHOLD = 1000


def select_solver(
    jacobian_available: bool,
    jacobian_expensive: bool,
    problem_size: int,
    spd_hessian: bool,
    smooth_objective: bool,
    constraint_type: str,
    memory_limited: bool,
    high_accuracy: bool,
    problem_type: str = "root-finding",
) -> Dict[str, List[str]]:
    """Select nonlinear solver based on problem characteristics.

    Args:
        jacobian_available: Whether analytic Jacobian is available
        jacobian_expensive: Whether Jacobian computation is expensive
        problem_size: Number of unknowns
        spd_hessian: Whether Hessian is symmetric positive definite
        smooth_objective: Whether objective/residual is smooth
        constraint_type: Type of constraints (none, bound, equality, inequality)
        memory_limited: Whether memory is constrained
        high_accuracy: Whether high accuracy is required
        problem_type: Class of problem (root-finding, optimization, least-squares)

    Returns:
        Dictionary with recommended solvers, alternatives, and notes
    """
    if not isinstance(problem_size, int):
        raise ValueError(
            f"problem_size must be an integer, got {type(problem_size).__name__}"
        )
    if problem_size <= 0:
        raise ValueError("problem_size must be positive")
    if problem_size > MAX_SIZE:
        raise ValueError(f"problem_size ({problem_size}) exceeds maximum ({MAX_SIZE})")

    valid_constraints = {"none", "bound", "equality", "inequality"}
    if constraint_type not in valid_constraints:
        raise ValueError(f"constraint_type must be one of {valid_constraints}")

    valid_problem_types = {"root-finding", "optimization", "least-squares"}
    if problem_type not in valid_problem_types:
        raise ValueError(f"problem_type must be one of {valid_problem_types}")

    recommended: List[str] = []
    alternatives: List[str] = []
    notes: List[str] = []

    large_problem = problem_size >= LARGE_PROBLEM_THRESHOLD

    # Handle nonlinear least-squares before generic unconstrained branching.
    # Sum-of-squares data fitting needs the least-squares solver class
    # (Levenberg-Marquardt / Gauss-Newton), not full Newton on the objective.
    if problem_type == "least-squares" and constraint_type == "none":
        # Prefer Gauss-Newton when the Jacobian is available and the problem is
        # well behaved (small residual, well-conditioned); LM otherwise, since
        # LM regularization is robust for large-residual / ill-conditioned fits.
        if jacobian_available and not jacobian_expensive:
            recommended.append("Levenberg-Marquardt")
            alternatives.append("Gauss-Newton")
            notes.append(
                "Nonlinear least-squares: Levenberg-Marquardt is the robust "
                "default; Gauss-Newton converges faster for small-residual, "
                "well-conditioned fits with an analytic Jacobian."
            )
        else:
            recommended.append("Levenberg-Marquardt")
            alternatives.append("Gauss-Newton")
            notes.append(
                "Nonlinear least-squares: Levenberg-Marquardt is preferred "
                "when the Jacobian is expensive, finite-differenced, or the "
                "problem is large-residual / ill-conditioned."
            )
        notes.append(
            "Use trust-region globalization (LM is itself a trust-region "
            "method); see globalization_advisor.py --problem-type least-squares."
        )
        if large_problem:
            notes.append(
                "For large least-squares, use a matrix-free / sparse LM "
                "(e.g., scipy.optimize.least_squares with lsmr) to avoid "
                "forming the full Jacobian."
            )
        return {"recommended": recommended, "alternatives": alternatives, "notes": notes}

    # Handle constrained optimization
    if constraint_type == "inequality":
        recommended.append("SQP (Sequential Quadratic Programming)")
        alternatives.append("Interior Point")
        notes.append("Inequality constraints require specialized solvers.")
        if not jacobian_available:
            notes.append("Consider finite-difference Jacobian or quasi-Newton Hessian.")
        return {"recommended": recommended, "alternatives": alternatives, "notes": notes}

    if constraint_type == "equality":
        recommended.append("SQP")
        alternatives.append("Augmented Lagrangian")
        notes.append("Equality constraints: use Lagrange multipliers or penalty methods.")
        return {"recommended": recommended, "alternatives": alternatives, "notes": notes}

    if constraint_type == "bound":
        if spd_hessian:
            recommended.append("L-BFGS-B")
            alternatives.append("Trust-Region Reflective")
        else:
            recommended.append("Trust-Region Reflective")
            alternatives.append("L-BFGS-B")
        notes.append("Bound constraints handled via projected methods.")
        return {"recommended": recommended, "alternatives": alternatives, "notes": notes}

    # Unconstrained case
    if jacobian_available and not jacobian_expensive:
        # Resolve problem size BEFORE high-accuracy: forming/factoring a full
        # Jacobian is infeasible for very large problems, so size dominates.
        if large_problem:
            recommended.append("Newton-Krylov (GMRES)")
            alternatives.append("Newton-Krylov (BiCGSTAB)")
            notes.append("Newton-Krylov avoids forming full Jacobian for large problems.")
            if high_accuracy:
                notes.append(
                    "Use a tight forcing sequence (e.g., Eisenstat-Walker with "
                    "eta_k -> 0) so Newton-Krylov retains Newton-level "
                    "superlinear/quadratic accuracy without forming/factoring J."
                )
        elif high_accuracy:
            recommended.append("Newton (full)")
            alternatives.append("Modified Newton")
            notes.append("Full Newton provides quadratic convergence near solution.")
        else:
            recommended.append("Newton (full)")
            alternatives.append("Modified Newton")
    elif jacobian_available and jacobian_expensive:
        if large_problem:
            # Large + expensive Jacobian: matrix-free Newton-Krylov needs only
            # Jacobian-vector products and never forms/factors J.
            recommended.append("Newton-Krylov (GMRES)")
            alternatives.append("L-BFGS" if memory_limited else "Modified Newton")
            notes.append(
                "Large + expensive Jacobian: prefer matrix-free Newton-Krylov "
                "(JFNK); it needs only Jacobian-vector products and never "
                "forms/factors J. Most effective when residual evaluations are "
                "cheap and a good preconditioner (ILU/AMG) is available."
            )
        elif memory_limited:
            recommended.append("L-BFGS")
            alternatives.append("Broyden")
            notes.append("L-BFGS uses limited memory quasi-Newton updates.")
        else:
            recommended.append("Modified Newton")
            alternatives.append("Broyden")
            notes.append("Modified Newton reuses Jacobian for multiple iterations.")
    else:
        # No Jacobian available
        if smooth_objective:
            if memory_limited or large_problem:
                recommended.append("L-BFGS")
                alternatives.append("Broyden (good)")
                notes.append("Quasi-Newton methods build approximate Jacobian.")
            else:
                recommended.append("BFGS")
                alternatives.append("SR1")
                notes.append("BFGS provides superlinear convergence for smooth problems.")
        else:
            recommended.append("Anderson Acceleration")
            alternatives.append("Picard (fixed-point)")
            notes.append("Non-smooth problems may benefit from fixed-point methods.")

    # Additional recommendations based on problem characteristics
    if spd_hessian and not jacobian_available:
        notes.append("SPD Hessian: BFGS maintains positive definiteness.")

    if not smooth_objective:
        notes.append("Non-smooth: consider subgradient or bundle methods.")

    return {"recommended": recommended, "alternatives": alternatives, "notes": notes}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Select a nonlinear solver based on problem characteristics.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--jacobian-available",
        action="store_true",
        help="Analytic Jacobian is available",
    )
    parser.add_argument(
        "--jacobian-expensive",
        action="store_true",
        help="Jacobian computation is expensive",
    )
    parser.add_argument(
        "--size",
        type=int,
        required=True,
        help="Problem size (number of unknowns)",
    )
    parser.add_argument(
        "--problem-type",
        type=str,
        default="root-finding",
        choices=["root-finding", "optimization", "least-squares"],
        help="Class of problem",
    )
    parser.add_argument(
        "--spd-hessian",
        action="store_true",
        help="Hessian is symmetric positive definite",
    )
    parser.add_argument(
        "--smooth",
        action="store_true",
        help="Objective/residual is smooth",
    )
    parser.add_argument(
        "--constraints",
        type=str,
        default="none",
        choices=["none", "bound", "equality", "inequality"],
        help="Type of constraints",
    )
    parser.add_argument(
        "--memory-limited",
        action="store_true",
        help="Memory is constrained",
    )
    parser.add_argument(
        "--high-accuracy",
        action="store_true",
        help="High accuracy is required",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        result = select_solver(
            jacobian_available=args.jacobian_available,
            jacobian_expensive=args.jacobian_expensive,
            problem_size=args.size,
            spd_hessian=args.spd_hessian,
            smooth_objective=args.smooth,
            constraint_type=args.constraints,
            memory_limited=args.memory_limited,
            high_accuracy=args.high_accuracy,
            problem_type=args.problem_type,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)

    payload: Dict[str, Any] = {
        "inputs": {
            "jacobian_available": args.jacobian_available,
            "jacobian_expensive": args.jacobian_expensive,
            "problem_type": args.problem_type,
            "problem_size": args.size,
            "spd_hessian": args.spd_hessian,
            "smooth_objective": args.smooth,
            "constraint_type": args.constraints,
            "memory_limited": args.memory_limited,
            "high_accuracy": args.high_accuracy,
        },
        "results": result,
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False))
        return

    print("Solver selection")
    print(f"  recommended: {', '.join(result['recommended'])}")
    if result["alternatives"]:
        print(f"  alternatives: {', '.join(result['alternatives'])}")
    for note in result["notes"]:
        print(f"  note: {note}")


if __name__ == "__main__":
    main()
