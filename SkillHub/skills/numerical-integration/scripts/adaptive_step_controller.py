#!/usr/bin/env python3
import argparse
import json
import math
import sys
from typing import Dict, Optional


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(max_value, value))


MAX_ORDER = 20


def compute_step(
    dt: float,
    error_norm: float,
    order: int,
    accept_threshold: float,
    safety: float,
    min_factor: float,
    max_factor: float,
    controller: str,
    prev_error: Optional[float],
) -> Dict[str, object]:
    if not math.isfinite(dt) or dt <= 0:
        raise ValueError("dt must be a positive finite number")
    if order < 1 or order > MAX_ORDER:
        raise ValueError(f"order must be between 1 and {MAX_ORDER}")
    if not math.isfinite(accept_threshold) or accept_threshold <= 0:
        raise ValueError("accept_threshold must be a positive finite number")
    if not math.isfinite(safety) or safety <= 0:
        raise ValueError("safety must be a positive finite number")
    if not math.isfinite(min_factor) or min_factor <= 0:
        raise ValueError("min_factor must be a positive finite number")
    if not math.isfinite(max_factor) or max_factor <= 0:
        raise ValueError("max_factor must be a positive finite number")
    if min_factor > max_factor:
        raise ValueError("min_factor must be <= max_factor")
    if error_norm < 0 or not math.isfinite(error_norm):
        raise ValueError("error_norm must be finite and non-negative")
    if prev_error is not None and (prev_error <= 0 or not math.isfinite(prev_error)):
        raise ValueError("prev_error must be positive and finite when provided")

    accept = error_norm <= accept_threshold
    if error_norm == 0:
        factor = max_factor
        controller_used = "zero-error"
    else:
        exp = 1.0 / (order + 1.0)
        if controller == "pi" and prev_error is not None:
            # Standard PI controller (Hairer & Wanner / Gustafsson):
            #   dt_new = dt * safety * err^(-alpha) * err_prev^(beta)
            # with alpha = 0.7/(p+1), beta = 0.4/(p+1). Generalized for an
            # arbitrary accept_threshold thr by replacing err -> err/thr:
            #   factor = safety * (thr/err)^alpha * (err_prev/thr)^beta
            k1 = 0.7 * exp
            k2 = 0.4 * exp
            factor = safety * (accept_threshold / error_norm) ** k1
            factor *= (prev_error / accept_threshold) ** k2
            controller_used = "pi"
        else:
            factor = safety * (accept_threshold / error_norm) ** exp
            controller_used = "p"

    factor = clamp(factor, min_factor, max_factor)
    dt_next = dt * factor
    note = None
    if not accept:
        note = "Step rejected; consider reducing dt or using a stiffer method."

    return {
        "accept": accept,
        "dt_next": dt_next,
        "factor": factor,
        "controller_used": controller_used,
        "note": note,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Adaptive step size controller for time integration.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--dt", type=float, required=True, help="Current time step")
    parser.add_argument("--error-norm", type=float, required=True, help="Scaled error norm")
    parser.add_argument("--order", type=int, required=True, help="Method order")
    parser.add_argument(
        "--accept-threshold",
        type=float,
        default=1.0,
        help="Acceptance threshold for error norm",
    )
    parser.add_argument("--safety", type=float, default=0.9, help="Safety factor")
    parser.add_argument("--min-factor", type=float, default=0.2, help="Min dt factor")
    parser.add_argument("--max-factor", type=float, default=5.0, help="Max dt factor")
    parser.add_argument(
        "--controller",
        choices=["p", "pi"],
        default="p",
        help="Controller type",
    )
    parser.add_argument(
        "--prev-error",
        type=float,
        default=None,
        help="Previous error norm (for PI controller)",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        payload = compute_step(
            dt=args.dt,
            error_norm=args.error_norm,
            order=args.order,
            accept_threshold=args.accept_threshold,
            safety=args.safety,
            min_factor=args.min_factor,
            max_factor=args.max_factor,
            controller=args.controller,
            prev_error=args.prev_error,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)

    result = {
        "inputs": {
            "dt": args.dt,
            "error_norm": args.error_norm,
            "order": args.order,
            "accept_threshold": args.accept_threshold,
            "safety": args.safety,
            "min_factor": args.min_factor,
            "max_factor": args.max_factor,
            "controller": args.controller,
            "prev_error": args.prev_error,
        },
        "results": payload,
    }

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return

    print("Adaptive step control")
    print(f"  accept: {payload['accept']}")
    print(f"  factor: {payload['factor']:.6g}")
    print(f"  dt_next: {payload['dt_next']:.6g}")
    print(f"  controller: {payload['controller_used']}")
    if payload["note"]:
        print(f"  note: {payload['note']}")


if __name__ == "__main__":
    main()
