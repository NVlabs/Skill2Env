#!/usr/bin/env python3
import argparse
import json
import sys
from typing import Dict, List


MAX_SIZE = 10_000_000_000  # 10 billion

# Dense factorization is memory-bound: a dense n x n float64 matrix needs
# n*n*8 bytes. Above a few GB this is infeasible on a workstation, so dense
# direct solvers (Cholesky/LU/LDL^T) are only recommended below this bound.
# 2 GB corresponds to n ~= 16384, consistent with the documented "small dense"
# regime used throughout the decision tree.
MAX_DENSE_BYTES = 2 * 1024 ** 3  # 2 GiB
BYTES_PER_ENTRY = 8  # float64


def select_solver(
    symmetric: bool,
    positive_definite: bool,
    sparse: bool,
    size: int,
    nearly_symmetric: bool,
    ill_conditioned: bool,
    complex_valued: bool,
    memory_limited: bool,
    saddle_point: bool = False,
) -> Dict[str, List[str] | str]:
    if not isinstance(size, int):
        raise ValueError(f"size must be an integer, got {type(size).__name__}")
    if size <= 0:
        raise ValueError("size must be positive")
    if size > MAX_SIZE:
        raise ValueError(f"size ({size}) exceeds maximum ({MAX_SIZE})")

    recommended: List[str] = []
    alternatives: List[str] = []
    notes: List[str] = []

    # Dense direct factorization is only feasible while the dense matrix fits in
    # memory. Compute the storage a dense n x n float64 matrix would need and only
    # allow a dense direct solver when it stays under MAX_DENSE_BYTES.
    dense_bytes = size * size * BYTES_PER_ENTRY
    dense_feasible = dense_bytes <= MAX_DENSE_BYTES
    # "small dense" = dense matrix, not memory-constrained, small enough to factor.
    small_dense = (not sparse) and (not memory_limited) and dense_feasible

    # Saddle-point systems are symmetric-indefinite by block structure and require
    # specialized block/Schur treatment regardless of the symmetric flag.
    if saddle_point:
        recommended.append("Schur complement / Uzawa")
        alternatives.append("Block-preconditioned MINRES/GMRES")
        notes.append(
            "Saddle-point (e.g. velocity-pressure) system: use a block "
            "preconditioner; unpreconditioned CG/GMRES will fail."
        )
    elif symmetric:
        if positive_definite:
            if small_dense:
                recommended.append("Cholesky")
                alternatives.append("CG")
            else:
                recommended.append("CG")
                alternatives.append("MINRES")
                notes.append("Use IC/AMG preconditioning for SPD systems.")
                if (not sparse) and not dense_feasible:
                    notes.append(
                        f"Dense factorization needs ~{dense_bytes / 1e9:.0f} GB; "
                        f"use iterative CG with IC/AMG instead."
                    )
        else:
            if small_dense:
                recommended.append("LDL^T (Bunch-Kaufman)")
                alternatives.append("MINRES")
                notes.append("Indefinite symmetric system; avoid CG.")
            else:
                recommended.append("MINRES")
                alternatives.append("SYMMLQ")
                notes.append("Indefinite symmetric system; avoid CG.")
                if (not sparse) and not dense_feasible:
                    notes.append(
                        f"Dense factorization needs ~{dense_bytes / 1e9:.0f} GB; "
                        f"use iterative MINRES instead."
                    )
    else:
        if small_dense:
            recommended.append("LU (partial pivoting)")
            alternatives.append("GMRES (restarted)")
            notes.append("Small dense nonsymmetric system; direct LU is robust.")
        elif nearly_symmetric:
            recommended.append("BiCGSTAB")
            alternatives.append("GMRES")
        else:
            recommended.append("GMRES (restarted)")
            alternatives.append("BiCGSTAB")
            notes.append("Use ILU/AMG preconditioning for nonsymmetric systems.")
            if (not sparse) and not dense_feasible:
                notes.append(
                    f"Dense factorization needs ~{dense_bytes / 1e9:.0f} GB; "
                    f"use iterative GMRES instead."
                )

    if complex_valued:
        notes.append("Ensure solver supports complex arithmetic.")
    if ill_conditioned:
        notes.append("Consider scaling/equilibration and stronger preconditioning.")

    if memory_limited and "GMRES (restarted)" in recommended:
        notes.append("Restarted GMRES reduces memory at the cost of robustness.")

    return {
        "recommended": recommended,
        "alternatives": alternatives,
        "notes": notes,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Select a linear solver based on matrix properties.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--symmetric", action="store_true", help="Matrix is symmetric")
    parser.add_argument(
        "--positive-definite",
        action="store_true",
        help="Matrix is positive definite",
    )
    parser.add_argument("--sparse", action="store_true", help="Matrix is sparse")
    parser.add_argument("--size", type=int, required=True, help="Matrix size (n)")
    parser.add_argument(
        "--nearly-symmetric",
        action="store_true",
        help="Matrix is nearly symmetric",
    )
    parser.add_argument(
        "--ill-conditioned",
        action="store_true",
        help="Matrix is ill-conditioned",
    )
    parser.add_argument(
        "--complex-valued",
        action="store_true",
        help="Matrix has complex entries",
    )
    parser.add_argument(
        "--memory-limited",
        action="store_true",
        help="Memory is constrained",
    )
    parser.add_argument(
        "--saddle-point",
        action="store_true",
        help="System has saddle-point (block KKT) structure",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        result = select_solver(
            symmetric=args.symmetric,
            positive_definite=args.positive_definite,
            sparse=args.sparse,
            size=args.size,
            nearly_symmetric=args.nearly_symmetric,
            ill_conditioned=args.ill_conditioned,
            complex_valued=args.complex_valued,
            memory_limited=args.memory_limited,
            saddle_point=args.saddle_point,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)

    payload = {
        "inputs": {
            "symmetric": args.symmetric,
            "positive_definite": args.positive_definite,
            "sparse": args.sparse,
            "size": args.size,
            "nearly_symmetric": args.nearly_symmetric,
            "ill_conditioned": args.ill_conditioned,
            "complex_valued": args.complex_valued,
            "memory_limited": args.memory_limited,
            "saddle_point": args.saddle_point,
        },
        "results": result,
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return

    print("Solver selection")
    print(f"  recommended: {', '.join(result['recommended'])}")
    if result["alternatives"]:
        print(f"  alternatives: {', '.join(result['alternatives'])}")
    for note in result["notes"]:
        print(f"  note: {note}")


if __name__ == "__main__":
    main()
