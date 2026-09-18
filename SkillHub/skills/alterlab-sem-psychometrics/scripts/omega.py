#!/usr/bin/env python3
"""McDonald's omega (and coefficient H) from standardized factor loadings — stdlib only.

Neither semopy nor pingouin returns omega, so this computes it directly from the standardized
loadings a CFA/EFA gives you. For a unidimensional (congeneric) factor with standardized loadings
lambda_i and standardized error variances (1 - lambda_i**2):

    omega_total = (sum lambda_i)**2 / [ (sum lambda_i)**2 + sum (1 - lambda_i**2) ]

Also reports coefficient H (construct reliability / maximal reliability):

    H = 1 / ( 1 + 1 / sum( lambda_i**2 / (1 - lambda_i**2) ) )

    python omega.py 0.72 0.68 0.81 0.55
    python omega.py --loadings 0.72,0.68,0.81,0.55
"""
from __future__ import annotations

import argparse


def omega_total(loadings: list[float]) -> float:
    s = sum(loadings)
    err = sum(1.0 - lam * lam for lam in loadings)
    denom = s * s + err
    if denom == 0:
        raise ValueError("degenerate loadings (zero denominator)")
    return (s * s) / denom


def coefficient_h(loadings: list[float]) -> float:
    total = 0.0
    for lam in loadings:
        e = 1.0 - lam * lam
        if e <= 0:
            # a loading of |1| means error-free; H -> 1
            return 1.0
        total += (lam * lam) / e
    return 1.0 / (1.0 + 1.0 / total) if total > 0 else 0.0


def _parse(values: list[str]) -> list[float]:
    out = []
    for v in values:
        for part in v.split(","):
            part = part.strip()
            if part:
                out.append(float(part))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("loadings", nargs="*", help="standardized loadings, space- or comma-separated")
    ap.add_argument("--loadings", dest="loadings_flag", default=None,
                    help="comma-separated standardized loadings")
    args = ap.parse_args()

    raw = list(args.loadings)
    if args.loadings_flag:
        raw.append(args.loadings_flag)
    lams = _parse(raw)
    if len(lams) < 2:
        ap.error("provide at least 2 standardized loadings")
    if any(abs(x) > 1.0 for x in lams):
        ap.error("standardized loadings must be within [-1, 1]")

    ot = omega_total(lams)
    h = coefficient_h(lams)
    print(f"items:        {len(lams)}")
    print(f"loadings:     {', '.join(f'{x:.3f}' for x in lams)}")
    print(f"omega_total:  {ot:.3f}")
    print(f"coefficient H:{h:.3f}")
    print("Report omega alongside alpha. omega assumes a correct unidimensional CFA — check fit first.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
