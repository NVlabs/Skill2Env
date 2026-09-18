#!/usr/bin/env python3
"""Map a quasi-experimental design to its estimator, identifying assumption, and verified call.

Stdlib-only. It does NOT estimate anything — it prints the estimator you should use, the
assumption you must defend first, the diagnostic to run, and a refutation to run after, using the
verified Python causal stack (statsmodels / linearmodels / pyfixest / dowhy / econml / rdrobust).

    python estimator_router.py did
    python estimator_router.py iv
    python estimator_router.py --list
"""
from __future__ import annotations

import argparse

# design -> (estimator call, assumption, diagnostic, refutation)
_MAP = {
    "did": (
        "pyfixest: pf.event_study(df, yname, idname, tname, gname, estimator='did2s')  |  or "
        "smf.ols('y ~ treat*post').fit(cov_type='cluster', cov_kwds={'groups': df.unit})",
        "PARALLEL TRENDS — treated & control would have moved together absent treatment",
        "pre-trend / event-study plot; for staggered adoption use Sun-Abraham sunab() or did2s",
        "placebo (fake) treatment timing; leave-one-cohort-out",
    ),
    "fe": (
        "linearmodels: PanelOLS.from_formula('y ~ 1 + x + EntityEffects + TimeEffects', panel)"
        ".fit(cov_type='clustered', cluster_entity=True)",
        "NO TIME-VARYING CONFOUNDERS (unit/time effects differenced out)",
        "compare within vs between estimates; Hausman if choosing FE vs RE",
        "add unit-specific time trends; check sensitivity to the FE structure",
    ),
    "iv": (
        "linearmodels: IV2SLS.from_formula('y ~ 1 + exog + [treat ~ z1 + z2]', df).fit()",
        "EXCLUSION RESTRICTION + relevance — instrument affects Y only through treatment",
        "first-stage F (weak-instrument, F > 10 rule of thumb); over-ID test if >1 instrument",
        "defend exclusion substantively; check reduced form; alternative instruments",
    ),
    "rdd": (
        "rdrobust: rdrobust(y, x, c=cutoff); rdbwselect(y, x, c=cutoff); rdplot(y, x, c=cutoff)",
        "CONTINUITY at the cutoff — units cannot precisely manipulate the running variable",
        "McCrary/density test for sorting; covariate-continuity at the cutoff",
        "bandwidth sensitivity; placebo cutoffs; donut RD",
    ),
    "psm": (
        "dowhy: CausalModel(df, treatment, outcome, graph).identify_effect() -> "
        "estimate_effect(method_name='backdoor.propensity_score_matching')",
        "CONDITIONAL IGNORABILITY — no unmeasured confounding (strongest, least testable)",
        "overlap / common support; covariate balance after matching",
        "dowhy.refute_estimate('random_common_cause' | 'placebo_treatment_refuter'); E-value",
    ),
    "cate": (
        "econml: LinearDML() or CausalForestDML(); est.fit(Y, T, X=X, W=W); est.effect(X_test)",
        "conditional ignorability + OVERLAP across the covariate space",
        "propensity overlap; honesty/cross-fitting (DML built-in)",
        "ignorability sensitivity; compare DML vs DR learners",
    ),
}

_ALIASES = {
    "difference-in-differences": "did", "diff-in-diff": "did", "event-study": "did",
    "fixed-effects": "fe", "panel": "fe",
    "instrumental-variables": "iv", "2sls": "iv",
    "regression-discontinuity": "rdd", "rd": "rdd",
    "propensity": "psm", "matching": "psm", "selection-on-observables": "psm",
    "heterogeneous": "cate", "dml": "cate",
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("design", nargs="?", help="did | fe | iv | rdd | psm | cate (or an alias)")
    ap.add_argument("--list", action="store_true", help="list all designs")
    args = ap.parse_args()

    if args.list or not args.design:
        for k in _MAP:
            print(f"{k:5s} -> {_MAP[k][1]}")
        return 0

    key = _ALIASES.get(args.design.lower(), args.design.lower())
    if key not in _MAP:
        print(f"unknown design '{args.design}'. Try one of: {', '.join(_MAP)} (or --list).")
        return 2
    call, assumption, diag, refute = _MAP[key]
    print(f"DESIGN:      {key}")
    print(f"ASSUMPTION:  {assumption}   <- defend BEFORE estimating")
    print(f"ESTIMATOR:   {call}")
    print(f"DIAGNOSTIC:  {diag}")
    print(f"REFUTATION:  {refute}   <- run AFTER, report beside the estimate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
