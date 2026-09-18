#!/usr/bin/env python3
"""Trustworthiness linter for interpretivist studies (stdlib only).

Audits a qualitative study's trustworthiness warrants against the Design Passport facts: is
positionality stated, is each Lincoln & Guba criterion evidenced, and does a written claim
over-generalize beyond what thick description supports? It does NOT judge quality — it surfaces
missing warrants and emits a PASS / WARN / BLOCK verdict mirroring the other ssci gates.

    python trustworthiness_checklist.py --positionality yes \\
        --credibility yes --transferability no --dependability yes --confirmability yes \\
        --claim "These findings show that remote workers everywhere are more satisfied."
"""
from __future__ import annotations

import argparse

_CRITERIA = ("credibility", "transferability", "dependability", "confirmability")

# Words that assert broad generalization — suspect in interpretivist write-ups.
_GENERALIZE = [
    "everyone", "everywhere", "all ", "in general", "generally", "universally",
    "always", "any organization", "people are", "workers are", "prove", "proves", "proven",
    "causes", "causo", "the population",
]


def audit(positionality: bool, criteria: dict[str, bool], claim: str) -> tuple[str, list[str]]:
    findings: list[str] = []
    verdict = "PASS"

    if not positionality:
        findings.append("BLOCK: no positionality statement — the researcher is the instrument; "
                        "state role, relationship to the setting, and standpoint.")
        verdict = "BLOCK"

    missing = [c for c in _CRITERIA if not criteria.get(c, False)]
    for c in missing:
        if c == "transferability":
            findings.append("WARN: transferability warrant missing — provide thick description of "
                            "context (NOT a claim of statistical generalization).")
        else:
            findings.append(f"WARN: {c} warrant missing — name the technique and its evidence "
                            f"({_TECH[c]}).")
        if verdict != "BLOCK":
            verdict = "WARN"

    low = claim.lower()
    gen_hits = [g.strip() for g in _GENERALIZE if g in low]
    if gen_hits and not criteria.get("transferability", False):
        findings.append(
            f"BLOCK: claim generalizes ({', '.join(sorted(set(gen_hits)))}) with no transferability "
            "warrant — scope it to the studied case or supply thick description.")
        verdict = "BLOCK"

    return verdict, findings


_TECH = {
    "credibility": "triangulation / member-checking / prolonged engagement / negative-case analysis",
    "dependability": "an audit trail of traceable decisions from data to themes",
    "confirmability": "reflexive bracketing and an auditable chain of evidence",
    "transferability": "thick description of context",
}


def _yn(v: str) -> bool:
    return v.lower() in ("yes", "y", "true", "1")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--positionality", choices=["yes", "no"], required=True)
    for c in _CRITERIA:
        ap.add_argument(f"--{c}", choices=["yes", "no"], default="no",
                        help=f"is the {c} warrant evidenced?")
    ap.add_argument("--claim", default="", help="a written claim to scan for over-generalization")
    args = ap.parse_args()

    criteria = {c: _yn(getattr(args, c)) for c in _CRITERIA}
    verdict, findings = audit(_yn(args.positionality), criteria, args.claim)
    print(f"VERDICT: {verdict}")
    if not findings:
        print("  positionality stated; all four trustworthiness criteria evidenced. Advance.")
    for f in findings:
        print(f"  - {f}")
    if verdict == "BLOCK":
        print("Fail-closed: resolve the BLOCK item(s) before writing the interpretivist claim.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
