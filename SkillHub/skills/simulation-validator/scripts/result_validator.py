#!/usr/bin/env python3
import argparse
import json
import math
import sys
from typing import Dict, List, Optional


def positive_finite_float(raw: str) -> float:
    """argparse type: accept only finite, strictly-positive floats."""
    try:
        value = float(raw)
    except (TypeError, ValueError):
        raise argparse.ArgumentTypeError(f"not a number: {raw!r}")
    if not math.isfinite(value) or value <= 0:
        raise argparse.ArgumentTypeError(
            f"must be a finite positive number, got {raw!r}"
        )
    return value


def finite_float(raw: str) -> float:
    """argparse type: accept only finite floats (NaN/Inf rejected)."""
    try:
        value = float(raw)
    except (TypeError, ValueError):
        raise argparse.ArgumentTypeError(f"not a number: {raw!r}")
    if not math.isfinite(value):
        raise argparse.ArgumentTypeError(f"must be a finite number, got {raw!r}")
    return value


def load_metrics(path: str) -> Dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_metrics(
    metrics: Dict[str, object],
    bound_min: Optional[float],
    bound_max: Optional[float],
    mass_tol: float,
    variational: bool = False,
) -> Dict[str, object]:
    checks: Dict[str, bool] = {}
    failed: List[str] = []
    notes: List[str] = []

    mass_initial = metrics.get("mass_initial")
    mass_final = metrics.get("mass_final")
    if mass_initial is not None and mass_final is not None:
        try:
            drift = abs(float(mass_final) - float(mass_initial)) / max(abs(float(mass_initial)), 1e-12)
            checks["mass_conserved"] = drift <= mass_tol
            if not checks["mass_conserved"]:
                failed.append("mass_conserved")
        except (TypeError, ValueError):
            checks["mass_conserved"] = False
            failed.append("mass_conserved")

    # Energy check. The metrics file may opt in to the strict variational
    # (gradient-flow) semantics via "energy_variational": true, or the caller
    # may pass --variational. Otherwise a clearly-named weaker net-decrease
    # check is used, which does NOT detect mid-run spikes.
    energy_history = metrics.get("energy_history")
    use_variational = variational or bool(metrics.get("energy_variational"))
    if isinstance(energy_history, list) and energy_history:
        try:
            energies = [float(v) for v in energy_history]
            if use_variational:
                rel_tol = 1e-8
                abs_tol = 1e-12
                scale = max(abs(energies[0]), 1e-12)
                monotone = all(
                    energies[i + 1] <= energies[i] + rel_tol * scale + abs_tol
                    for i in range(len(energies) - 1)
                )
                checks["energy_monotone"] = monotone
                if not monotone:
                    failed.append("energy_monotone")
            else:
                checks["energy_net_decrease"] = energies[-1] <= energies[0]
                if not checks["energy_net_decrease"]:
                    failed.append("energy_net_decrease")
        except (TypeError, ValueError):
            key = "energy_monotone" if use_variational else "energy_net_decrease"
            checks[key] = False
            failed.append(key)

    field_min = metrics.get("field_min")
    field_max = metrics.get("field_max")
    if bound_min is not None or bound_max is not None:
        # Only mark bounds_satisfied when the relevant field value is actually
        # present and compared. A requested-but-unverifiable bound is a FAILED
        # check, not a vacuous pass.
        ok = True
        compared = False
        if bound_min is not None:
            if field_min is not None:
                ok = ok and (float(field_min) >= bound_min)
                compared = True
            else:
                ok = False
                notes.append("bound-min requested but field_min absent in metrics.")
        if bound_max is not None:
            if field_max is not None:
                ok = ok and (float(field_max) <= bound_max)
                compared = True
            else:
                ok = False
                notes.append("bound-max requested but field_max absent in metrics.")
        if compared and ok:
            checks["bounds_satisfied"] = True
        elif compared and not ok:
            checks["bounds_satisfied"] = False
            failed.append("bounds_satisfied")
        else:
            # No field value present at all to compare against requested bounds.
            checks["bounds_verifiable"] = False
            failed.append("bounds_unverifiable")

    has_nan = metrics.get("has_nan")
    if has_nan is not None:
        checks["no_nan"] = not bool(has_nan)
        if not checks["no_nan"]:
            failed.append("no_nan")

    # Distinguish "all checks passed" from "no substantive check ran". An empty
    # or unrecognized metrics file must NOT yield a green-light confidence of 1.0.
    substantive = [k for k in checks if k != "no_checks"]
    if not substantive:
        return {
            "checks": {"no_checks": True},
            "failed_checks": ["insufficient_data"],
            "confidence_score": None,
            "status": "INSUFFICIENT_DATA",
            "notes": ["No recognized metrics fields; no validation checks ran."],
        }

    passed = sum(1 for k, v in checks.items() if k in substantive and v)
    confidence = passed / len(substantive)
    status = "PASS" if not failed else "FAIL"

    result: Dict[str, object] = {
        "checks": checks,
        "failed_checks": failed,
        "confidence_score": confidence,
        "status": status,
    }
    if notes:
        result["notes"] = notes
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate simulation results from metrics JSON.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--metrics", required=True, help="Path to metrics JSON")
    parser.add_argument("--bound-min", type=finite_float, default=None, help="Minimum bound")
    parser.add_argument("--bound-max", type=finite_float, default=None, help="Maximum bound")
    parser.add_argument("--mass-tol", type=positive_finite_float, default=1e-3, help="Mass tolerance")
    parser.add_argument(
        "--variational",
        action="store_true",
        help="Enforce monotone non-increasing energy (gradient-flow/dissipative runs)",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if (
        args.bound_min is not None
        and args.bound_max is not None
        and args.bound_max <= args.bound_min
    ):
        print(
            f"--bound-max ({args.bound_max}) must be greater than "
            f"--bound-min ({args.bound_min}).",
            file=sys.stderr,
        )
        sys.exit(2)
    try:
        metrics = load_metrics(args.metrics)
        result = validate_metrics(
            metrics=metrics,
            bound_min=args.bound_min,
            bound_max=args.bound_max,
            mass_tol=args.mass_tol,
            variational=args.variational,
        )
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)

    payload = {
        "inputs": {
            "metrics": args.metrics,
            "bound_min": args.bound_min,
            "bound_max": args.bound_max,
            "mass_tol": args.mass_tol,
            "variational": args.variational,
        },
        "results": result,
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return

    print("Result validation")
    score = result["confidence_score"]
    score_str = "N/A" if score is None else f"{score:.6g}"
    print(f"  confidence_score: {score_str}")
    print(f"  status: {result.get('status')}")
    for name, status in result["checks"].items():
        print(f"  {name}: {status}")


if __name__ == "__main__":
    main()
