#!/usr/bin/env python3
"""Claim linter: flag inferential overreach against the Design Passport (stdlib only).

Reads the study's facts (design, whether the identifying assumption is defended, sample type) and
a draft claim sentence, then flags three kinds of overreach:

  1. causal language not licensed by the design,
  2. population generalization from a non-probability sample,
  3. common p-value / confidence-interval misreadings.

It does NOT rewrite for you and it does NOT judge substance — it surfaces sentences to audit.

    python claim_audit.py --design observational --assumption-defended no \\
        --sample non-probability --claim "Remote work increases satisfaction among adults."
"""
from __future__ import annotations

import argparse
import re

# Designs that can identify a causal effect IF their assumption is defended.
_CAUSAL_DESIGNS = {"experiment", "did", "iv", "rdd", "its", "fe"}
# Design that never licenses causal language without an explicit defended assumption.
_CAUSAL_VERBS = [
    "causes", "cause", "caused", "increases", "increase", "increased", "reduces", "reduce",
    "reduced", "improves", "improve", "improved", "decreases", "decrease", "leads to", "led to",
    "results in", "the effect of", "effect on", "impact of", "impacts", "drives", "produces",
]
_GENERALIZE = [
    "adults", "everyone", "people generally", "the population", "all ", "in general",
    "consumers", "humans", "society", "the public",
]
_PVALUE_MISUSE = [
    (r"\bno effect\b", "Non-significance is not proof of no effect (absence of evidence). Report the CI."),
    (r"chance (that|the) .*null", "A p-value is not the probability the null is true."),
    (r"\bproves?\b", "Statistics support or fail to reject; they do not 'prove'."),
    (r"95%?\s*(chance|probability).*(interval|true value|parameter)",
     "A 95% CI is long-run procedure coverage, not a 95% probability the parameter is inside."),
    (r"trend(ing)? toward significance", "There is no 'trending toward significance'; report the estimate + CI."),
    (r"significant,? so it (matters|is important)",
     "Statistical significance is not practical importance; report the effect size."),
]


def audit(design: str, assumption_defended: bool, sample: str, claim: str) -> list[str]:
    findings: list[str] = []
    low = claim.lower()

    causal_hits = [v for v in _CAUSAL_VERBS if v in low]
    if causal_hits:
        licensed = (design in _CAUSAL_DESIGNS and assumption_defended)
        if not licensed:
            why = ("observational design" if design not in _CAUSAL_DESIGNS
                   else "identifying assumption not defended")
            findings.append(
                f"CAUSAL LANGUAGE ({', '.join(sorted(set(causal_hits)))}) not licensed — {why}. "
                f"Downgrade to associational (is associated with / predicts / correlates with).")

    if sample.startswith("non"):
        gen_hits = [g.strip() for g in _GENERALIZE if g in low]
        if gen_hits:
            findings.append(
                f"GENERALIZATION ({', '.join(sorted(set(gen_hits)))}) from a non-probability sample — "
                f"scope the claim to the studied cases (analytical, not statistical, generalization).")

    for pattern, msg in _PVALUE_MISUSE:
        if re.search(pattern, low):
            findings.append(f"UNCERTAINTY: {msg}")

    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--design", required=True,
                    choices=["experiment", "did", "iv", "rdd", "its", "fe", "observational", "qualitative"])
    ap.add_argument("--assumption-defended", choices=["yes", "no"], default="no")
    ap.add_argument("--sample", choices=["probability", "non-probability"], default="non-probability")
    ap.add_argument("--claim", required=True, help="the draft claim sentence to audit")
    args = ap.parse_args()

    findings = audit(args.design, args.assumption_defended == "yes", args.sample, args.claim)
    if not findings:
        print("No overreach flagged. Still confirm the effect size + CI are reported.")
        return 0
    print(f"{len(findings)} issue(s) to audit:")
    for i, f in enumerate(findings, 1):
        print(f"  {i}. {f}")
    print("\nRewrite each flagged sentence down to what the design, sample, and uncertainty support.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
