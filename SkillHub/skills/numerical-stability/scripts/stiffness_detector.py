#!/usr/bin/env python3
import argparse
import json
import os
import sys
from typing import Dict, Optional

import numpy as np


MAX_EIGS = 10000


def parse_eigs(raw: str) -> np.ndarray:
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    if not parts:
        raise ValueError("eigs must be a comma-separated list")
    if len(parts) > MAX_EIGS:
        raise ValueError(f"eigs list exceeds maximum of {MAX_EIGS} entries")
    return np.array([complex(p) for p in parts], dtype=complex)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Detect stiffness from eigenvalues or a Jacobian matrix.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--eigs", help="Comma-separated eigenvalues")
    group.add_argument("--jacobian", help="Path to Jacobian matrix (.npy or text)")
    parser.add_argument(
        "--delimiter",
        default=None,
        help="Delimiter for text Jacobians (default: any whitespace)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=1e3,
        help="Stiffness ratio threshold",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser.parse_args()


MAX_MATRIX_BYTES = 500 * 1024 * 1024  # 500 MB


def load_matrix(path: str, delimiter: Optional[str]) -> np.ndarray:
    if os.path.getsize(path) > MAX_MATRIX_BYTES:
        raise ValueError("matrix file exceeds 500 MB size limit")
    _, ext = os.path.splitext(path)
    if ext == ".npy":
        return np.load(path, allow_pickle=False)
    return np.loadtxt(path, delimiter=delimiter)


def compute_stiffness(eigs: np.ndarray, threshold: float) -> Dict[str, object]:
    if threshold <= 0:
        raise ValueError("threshold must be positive")
    if eigs.size == 0:
        raise ValueError("eigs must be non-empty")
    if not np.all(np.isfinite(eigs)):
        raise ValueError("eigs contain non-finite values")

    abs_eigs = np.abs(eigs)
    nonzero = abs_eigs[abs_eigs > 0]
    # Classical magnitude-based stiffness ratio (max|lambda| / min|lambda|).
    ratio = float(np.max(nonzero) / np.min(nonzero)) if nonzero.size else float("inf")

    # Real-part-based ratio over genuinely decaying modes (Re(lambda) < 0).
    # Classical stiffness reflects scale separation among DECAY rates; modes on
    # the imaginary axis are oscillatory, not stiff, and should not trigger an
    # implicit-solver recommendation on magnitude alone.
    re = np.real(eigs)
    im = np.abs(np.imag(eigs))
    decaying = -re[re < 0]  # positive decay rates
    if decaying.size:
        real_ratio = float(np.max(decaying) / np.min(decaying))
    else:
        real_ratio = None

    max_re = float(np.max(np.abs(re))) if re.size else 0.0
    max_im = float(np.max(im)) if im.size else 0.0
    # Imaginary-dominated: oscillation/advection/Hamiltonian character. Treat as
    # imag-dominated when the largest |Im| dwarfs the largest |Re| (or all Re~0).
    imag_dominated = bool(max_im > 100.0 * max_re)

    warning = None
    if real_ratio is not None and not imag_dominated:
        # Genuine scale separation among decaying modes -> classical stiffness.
        stiff = real_ratio >= threshold
    elif imag_dominated:
        # Spectrum dominated by the imaginary axis: wave/advection/Hamiltonian.
        stiff = False
        warning = (
            "Spectrum is imaginary-axis dominated (oscillatory/wave/Hamiltonian); "
            "magnitude-based stiffness is misleading. Prefer symplectic/leapfrog "
            "or an A-stable scheme sized by the CFL limit rather than BDF/Radau."
        )
    else:
        # No decaying modes resolved (e.g. all-zero spectrum); fall back to the
        # magnitude ratio so degenerate inputs keep a defined verdict.
        stiff = ratio >= threshold

    recommendation = "implicit (BDF/Radau)" if stiff else "explicit (RK/Adams)"

    return {
        "stiffness_ratio": ratio,
        "real_part_stiffness_ratio": real_ratio,
        "imag_dominated": imag_dominated,
        "stiff": stiff,
        "recommendation": recommendation,
        "warning": warning,
        "nonzero_count": int(nonzero.size),
        "total_count": int(eigs.size),
    }


def main() -> None:
    args = parse_args()
    try:
        if args.eigs is not None:
            eigs = parse_eigs(args.eigs)
            source = "eigs"
        else:
            if not os.path.exists(args.jacobian):
                print(f"Jacobian not found: {args.jacobian}", file=sys.stderr)
                sys.exit(2)
            jacobian = load_matrix(args.jacobian, args.delimiter)
            if jacobian.ndim != 2 or jacobian.shape[0] != jacobian.shape[1]:
                print("Jacobian must be square.", file=sys.stderr)
                sys.exit(2)
            eigs = np.linalg.eigvals(jacobian)
            source = "jacobian"
        results = compute_stiffness(eigs, args.threshold)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)

    payload = {
        "inputs": {
            "source": source,
            "threshold": args.threshold,
        },
        "results": results,
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return

    print("Stiffness detection")
    print(f"  stiffness ratio (magnitude): {results['stiffness_ratio']:.6g}")
    if results["real_part_stiffness_ratio"] is not None:
        print(f"  stiffness ratio (real part): {results['real_part_stiffness_ratio']:.6g}")
    print(f"  imag dominated: {results['imag_dominated']}")
    print(f"  stiff: {results['stiff']}")
    print(f"  recommendation: {results['recommendation']}")
    if results["warning"]:
        print(f"  warning: {results['warning']}")


if __name__ == "__main__":
    main()
