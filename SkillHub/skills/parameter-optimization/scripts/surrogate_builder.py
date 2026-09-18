#!/usr/bin/env python3
import argparse
import json
import math
import sys
from typing import Dict, List

# Security limits
MAX_LIST_LENGTH = 100_000


def parse_list(raw: str) -> List[float]:
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    if not parts:
        raise ValueError("value list must be a comma-separated list")
    if len(parts) > MAX_LIST_LENGTH:
        raise ValueError(f"list length ({len(parts)}) exceeds limit ({MAX_LIST_LENGTH})")
    values = [float(p) for p in parts]
    if any(not math.isfinite(v) for v in values):
        raise ValueError("list contains non-finite values")
    return values


def _solve(matrix: List[List[float]], rhs: List[float]) -> List[float]:
    """Solve a small linear system A w = b via Gaussian elimination with
    partial pivoting. Returns the solution vector. Raises ValueError if the
    system is singular (cannot be solved)."""
    n = len(matrix)
    # Build augmented matrix.
    aug = [row[:] + [rhs[i]] for i, row in enumerate(matrix)]
    for col in range(n):
        # Partial pivot: find row with largest absolute value in this column.
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot][col]) < 1e-12:
            raise ValueError("singular system; cannot fit surrogate")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        pivot_val = aug[col][col]
        for r in range(n):
            if r == col:
                continue
            factor = aug[r][col] / pivot_val
            for c in range(col, n + 1):
                aug[r][c] -= factor * aug[col][c]
    return [aug[i][n] / aug[i][i] for i in range(n)]


def _poly_fit(x: List[float], y: List[float], degree: int) -> List[float]:
    """Least-squares polynomial fit via the normal equations.

    Returns coefficients [c0, c1, ..., c_degree] for c0 + c1*x + ... .
    """
    n = degree + 1
    # Vandermonde-based normal equations: (V^T V) c = V^T y.
    # Precompute power sums to avoid building the full Vandermonde matrix.
    power_sums = [sum(xi ** p for xi in x) for p in range(2 * degree + 1)]
    ata = [[power_sums[i + j] for j in range(n)] for i in range(n)]
    atb = [sum((xi ** i) * yi for xi, yi in zip(x, y)) for i in range(n)]
    return _solve(ata, atb)


def _poly_eval(coeffs: List[float], xi: float) -> float:
    return sum(c * (xi ** p) for p, c in enumerate(coeffs))


def _rbf_weights(centers: List[float], y: List[float], epsilon: float) -> List[float]:
    """Solve for Gaussian RBF interpolation weights: Phi w = y."""
    n = len(centers)
    phi = [
        [math.exp(-((centers[i] - centers[j]) / epsilon) ** 2) for j in range(n)]
        for i in range(n)
    ]
    return _solve(phi, y)


def _rbf_eval(centers: List[float], weights: List[float], epsilon: float, xi: float) -> float:
    return sum(
        w * math.exp(-((xi - c) / epsilon) ** 2)
        for c, w in zip(centers, weights)
    )


def _rbf_epsilon(x: List[float]) -> float:
    """Heuristic shape parameter: mean nearest-neighbor distance."""
    xs = sorted(x)
    gaps = [xs[i + 1] - xs[i] for i in range(len(xs) - 1) if xs[i + 1] - xs[i] > 0]
    if gaps:
        return sum(gaps) / len(gaps)
    span = (max(x) - min(x)) or 1.0
    return span / max(len(x) - 1, 1)


def build_surrogate(x: List[float], y: List[float], model: str) -> Dict[str, object]:
    if len(x) != len(y):
        raise ValueError("x and y must have same length")
    if model not in {"rbf", "poly"}:
        raise ValueError("model must be rbf or poly")
    if len(x) < 2:
        raise ValueError("need at least 2 samples")

    n = len(x)
    mean_y = sum(y) / n
    output_variance = sum((yi - mean_y) ** 2 for yi in y) / n
    notes: List[str] = []

    if model == "poly":
        # Degree capped so the system is well-determined for the given data.
        degree = min(2, n - 1)
        try:
            coeffs = _poly_fit(x, y, degree)
            residuals = [yi - _poly_eval(coeffs, xi) for xi, yi in zip(x, y)]
            mse = sum(r * r for r in residuals) / n
        except ValueError:
            # Fall back to baseline variance if the fit is degenerate.
            mse = output_variance
            notes.append("Polynomial fit was degenerate; reporting baseline variance.")
        cv_error = _loo_cv_poly(x, y, degree)
        notes.append(f"Least-squares polynomial fit (degree {degree}); MSE is the fit residual.")
    else:  # rbf
        epsilon = _rbf_epsilon(x)
        try:
            weights = _rbf_weights(x, y, epsilon)
            residuals = [yi - _rbf_eval(x, weights, epsilon, xi) for xi, yi in zip(x, y)]
            mse = sum(r * r for r in residuals) / n
        except ValueError:
            mse = output_variance
            notes.append("RBF system was singular; reporting baseline variance.")
        cv_error = _loo_cv_rbf(x, y, epsilon)
        notes.append(
            "Gaussian RBF interpolation; in-sample MSE is near zero by construction, "
            "so use cv_error (leave-one-out) to judge fit quality."
        )

    notes.append("Surrogate is a lightweight stdlib implementation; use scipy/scikit-learn for production.")

    return {
        "model_type": model,
        "metrics": {
            "mse": mse,
            "cv_error": cv_error,
            "output_variance": output_variance,
        },
        "notes": notes,
    }


def _loo_cv_poly(x: List[float], y: List[float], degree: int) -> float:
    """Leave-one-out cross-validation mean squared error for the poly fit."""
    n = len(x)
    if n <= degree + 1:
        return float("nan")
    total = 0.0
    for i in range(n):
        xt = x[:i] + x[i + 1:]
        yt = y[:i] + y[i + 1:]
        try:
            coeffs = _poly_fit(xt, yt, degree)
            pred = _poly_eval(coeffs, x[i])
        except ValueError:
            return float("nan")
        total += (y[i] - pred) ** 2
    return total / n


def _loo_cv_rbf(x: List[float], y: List[float], epsilon: float) -> float:
    """Leave-one-out cross-validation mean squared error for the RBF fit."""
    n = len(x)
    if n < 3:
        return float("nan")
    total = 0.0
    for i in range(n):
        xt = x[:i] + x[i + 1:]
        yt = y[:i] + y[i + 1:]
        try:
            weights = _rbf_weights(xt, yt, epsilon)
            pred = _rbf_eval(xt, weights, epsilon, x[i])
        except ValueError:
            return float("nan")
        total += (y[i] - pred) ** 2
    return total / n


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a simple surrogate model summary.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--x", required=True, help="Comma-separated input values")
    parser.add_argument("--y", required=True, help="Comma-separated output values")
    parser.add_argument("--model", choices=["rbf", "poly"], default="rbf", help="Surrogate type")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        x = parse_list(args.x)
        y = parse_list(args.y)
        result = build_surrogate(x, y, args.model)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)

    payload = {
        "inputs": {"x": x, "y": y, "model": args.model},
        "results": result,
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return

    metrics = result["metrics"]
    print("Surrogate summary")
    print(f"  model: {result['model_type']}")
    print(f"  mse: {metrics['mse']:.6g}")
    print(f"  cv_error: {metrics['cv_error']:.6g}")


if __name__ == "__main__":
    main()
