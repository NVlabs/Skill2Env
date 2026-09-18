#!/usr/bin/env python3
"""Plan benchmark, MMS, and refinement checks for simulation V&V."""
from __future__ import annotations

import argparse
import json
import math
import sys
from typing import Dict, List


# Lightweight input caps so a planning helper never has to materialise pathological
# strings. These mirror the bounds advertised in the SKILL.md "## Security" section.
MAX_FIELD_LEN = 256

# Model families whose dynamics are time dependent (and 'general', which we treat as
# potentially transient by default). A model that falls back to 'general' is handled
# identically to the explicit 'general' family.
TIME_DEPENDENT_MODELS = {"diffusion", "advection", "phase-field", "fluid", "general"}


MODEL_BENCHMARKS = {
    "diffusion": ["1D heat equation analytic decay", "2D manufactured source", "thermal step relaxation"],
    "advection": ["solid-body rotation", "1D periodic wave transport", "Gaussian pulse translation"],
    "elasticity": ["uniaxial bar", "cantilever beam", "Kirsch plate with hole"],
    "phase-field": ["spinodal decomposition trend", "Allen-Cahn tanh interface", "grain-growth coarsening law"],
    "fluid": ["lid-driven cavity", "Poiseuille flow", "Taylor-Green vortex"],
    "general": ["conservation audit", "method-of-manufactured-solutions case", "published benchmark"],
}


def _positive_finite(value: float, name: str) -> float:
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be a positive finite number")
    return value


def plan_vv(
    model: str,
    quantity: str,
    dimension: int,
    expected_order: float,
    reference: str,
    risk: str,
) -> Dict:
    if dimension not in {1, 2, 3}:
        raise ValueError("dimension must be 1, 2, or 3")
    if len(model) > MAX_FIELD_LEN:
        raise ValueError(f"model must be at most {MAX_FIELD_LEN} characters")
    if len(quantity) > MAX_FIELD_LEN:
        raise ValueError(f"quantity must be at most {MAX_FIELD_LEN} characters")
    _positive_finite(expected_order, "expected_order")
    model_key = model.lower().strip() or "general"
    reference_key = reference.lower().strip()
    risk_key = risk.lower().strip()
    if risk_key not in {"low", "medium", "high"}:
        raise ValueError("risk must be one of: low, medium, high")
    if reference_key not in {"analytic", "benchmark", "experimental", "none"}:
        raise ValueError("reference must be one of: analytic, benchmark, experimental, none")

    # Resolve the effective model family exactly once. Unknown families fall back to
    # 'general' so that benchmark selection and the time-refinement decision stay
    # consistent (an unlisted but transient PDE must not be told to skip time
    # refinement just because its name is not in the table).
    effective_model = model_key if model_key in MODEL_BENCHMARKS else "general"

    refinement_levels = 4 if risk_key == "high" else 3
    # Observed-order acceptance band. This is an engineering screening heuristic, not a
    # certified bound: we accept an observed order within a fractional tolerance of the
    # formal order, floored at first-order convergence. Using a *relative* band keeps the
    # strictness consistent across formal orders (a fixed absolute offset is far stricter
    # in relative terms for high-order schemes). See references/vv_patterns.md.
    tolerance_fraction = 0.10 if risk_key == "high" else 0.20
    accept_observed_order_min = round(max(1.0, expected_order * (1.0 - tolerance_fraction)), 3)
    benchmark_cases = MODEL_BENCHMARKS[effective_model]
    warnings: List[str] = []

    if reference_key == "none":
        warnings.append("No reference source provided; use convergence and conservation only, not full validation.")
    if risk_key == "high" and reference_key in {"none", "experimental"}:
        warnings.append("High-risk claims need an independent analytic or published benchmark where possible.")

    strategy = "MMS plus benchmark validation" if reference_key == "analytic" else "benchmark-led validation"
    if reference_key == "none":
        strategy = "verification-only convergence audit"

    return {
        "verification_strategy": strategy,
        "effective_model": effective_model,
        "mms_plan": {
            "manufacture_solution": reference_key == "analytic",
            "recommended_norms": ["L2", "Linf"],
            "source_term_check": "derive symbolic/source forcing and test boundary terms",
            "quantity_of_interest": quantity,
        },
        "benchmark_cases": benchmark_cases[:3],
        "refinement_protocol": {
            "dimension": dimension,
            "levels": refinement_levels,
            "spacing_ratio": 2,
            "expected_order": expected_order,
            "accept_observed_order_min": accept_observed_order_min,
            "include_time_refinement": effective_model in TIME_DEPENDENT_MODELS,
        },
        "uncertainty_plan": {
            "propagate_inputs": risk_key in {"medium", "high"},
            "report_error_bars": risk_key == "high" or reference_key == "experimental",
            "separate_discretization_and_model_error": True,
        },
        "acceptance_criteria": [
            "observed order meets the minimum threshold",
            "quantity of interest changes monotonically or plateaus under refinement",
            "conservation or balance laws close within documented tolerance",
            "benchmark discrepancy is explained before production use",
        ],
        "warnings": warnings,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="general", help="Model family, e.g. diffusion, elasticity, phase-field")
    parser.add_argument("--quantity", required=True, help="Quantity of interest to validate")
    parser.add_argument("--dimension", type=int, default=2)
    parser.add_argument("--expected-order", type=float, default=2.0)
    parser.add_argument("--reference", default="benchmark", choices=["analytic", "benchmark", "experimental", "none"])
    parser.add_argument("--risk", default="medium", choices=["low", "medium", "high"])
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        results = plan_vv(
            model=args.model,
            quantity=args.quantity,
            dimension=args.dimension,
            expected_order=args.expected_order,
            reference=args.reference,
            risk=args.risk,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    payload = {
        "inputs": {
            "model": args.model,
            "quantity": args.quantity,
            "dimension": args.dimension,
            "expected_order": args.expected_order,
            "reference": args.reference,
            "risk": args.risk,
        },
        "results": results,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"Strategy: {results['verification_strategy']}")
        print(f"Benchmarks: {', '.join(results['benchmark_cases'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
