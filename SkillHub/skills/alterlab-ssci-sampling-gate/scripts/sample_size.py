#!/usr/bin/env python3
"""A-priori sample-size calculator (stdlib only, normal approximation).

Enforces the discipline the sampling gate cares about: you must state an effect size (or a
precision target) BEFORE collecting, and the number falls out of it. It does NOT run your
analysis and it does NOT compute post-hoc power (which carries no information).

    # two-group mean comparison, Cohen's d = 0.5, 80% power, alpha 0.05
    python sample_size.py mean --d 0.5

    # two-proportion comparison, 0.30 vs 0.45
    python sample_size.py prop --p1 0.30 --p2 0.45 --power 0.90

    # estimate a proportion to +/- 3 points at 95%
    python sample_size.py precision --margin 0.03 --p 0.5

Clustered/stratified designs: multiply the printed n by your design effect (see
references/sampling_and_power.md). SRS is assumed here.
"""
from __future__ import annotations

import argparse
import math


def _norm_ppf(p: float) -> float:
    """Inverse standard-normal CDF via the Acklam rational approximation (stdlib only).

    Accurate to ~1e-9 in the central region, ample for sample-size planning.
    """
    if not 0.0 < p < 1.0:
        raise ValueError("p must be in (0, 1)")
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    plow, phigh = 0.02425, 1 - 0.02425
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
               ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    if p > phigh:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
               ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    q = p - 0.5
    r = q * q
    return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / \
           (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)


def _z_pair(alpha: float, power: float) -> tuple[float, float]:
    return _norm_ppf(1 - alpha / 2), _norm_ppf(power)


def n_mean(d: float, alpha: float, power: float) -> int:
    """Per-group n for a two-sided two-sample mean comparison (Cohen's d)."""
    za, zb = _z_pair(alpha, power)
    return math.ceil(2 * (za + zb) ** 2 / d ** 2)


def n_prop(p1: float, p2: float, alpha: float, power: float) -> int:
    """Per-group n for a two-sided two-proportion comparison."""
    za, zb = _z_pair(alpha, power)
    num = (za + zb) ** 2 * (p1 * (1 - p1) + p2 * (1 - p2))
    return math.ceil(num / (p1 - p2) ** 2)


def n_precision(margin: float, p: float, alpha: float) -> int:
    """Total n to estimate a proportion within +/- margin at confidence 1 - alpha."""
    za = _norm_ppf(1 - alpha / 2)
    return math.ceil(za ** 2 * p * (1 - p) / margin ** 2)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="mode", required=True)

    m = sub.add_parser("mean", help="two-group mean comparison (Cohen's d)")
    m.add_argument("--d", type=float, required=True, help="smallest effect size of interest (Cohen's d)")
    m.add_argument("--alpha", type=float, default=0.05)
    m.add_argument("--power", type=float, default=0.80)

    pr = sub.add_parser("prop", help="two-proportion comparison")
    pr.add_argument("--p1", type=float, required=True)
    pr.add_argument("--p2", type=float, required=True)
    pr.add_argument("--alpha", type=float, default=0.05)
    pr.add_argument("--power", type=float, default=0.80)

    pc = sub.add_parser("precision", help="estimate a proportion to a target margin")
    pc.add_argument("--margin", type=float, required=True, help="desired half-width (e.g. 0.03)")
    pc.add_argument("--p", type=float, default=0.5, help="expected proportion (0.5 = conservative)")
    pc.add_argument("--alpha", type=float, default=0.05)

    args = ap.parse_args()
    if args.mode == "mean":
        n = n_mean(args.d, args.alpha, args.power)
        print(f"Two-group mean comparison | d={args.d}, alpha={args.alpha}, power={args.power}")
        print(f"  per group n = {n}   (total = {2 * n})")
        print("  Power on the SMALLEST meaningful effect, not a pilot's inflated one.")
    elif args.mode == "prop":
        n = n_prop(args.p1, args.p2, args.alpha, args.power)
        print(f"Two-proportion comparison | p1={args.p1}, p2={args.p2}, alpha={args.alpha}, power={args.power}")
        print(f"  per group n = {n}   (total = {2 * n})")
    else:
        n = n_precision(args.margin, args.p, args.alpha)
        print(f"Estimate a proportion | margin=+/-{args.margin}, p={args.p}, conf={1 - args.alpha:.0%}")
        print(f"  total n = {n}")
    print("SRS assumed. For clustered/stratified designs multiply by the design effect (DEFF).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
