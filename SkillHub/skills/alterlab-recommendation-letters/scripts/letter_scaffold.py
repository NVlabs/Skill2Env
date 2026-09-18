#!/usr/bin/env python3
"""letter_scaffold.py — emit a type-appropriate recommendation-letter skeleton.

Given a letter ``--type`` (and optional candidate / relationship / target), this
tool prints a Markdown section skeleton matched to the *reader and decision* of
that letter type (see ``references/letter_types.md``). Each body section carries
an inline reminder of the **Claim -> Evidence -> Significance** pattern and
bracketed prompts for the recommender to fill from their own dossier.

It is a deterministic scaffolder, NOT a generator: it writes structure and
prompts, never claims or facts. Filling the sections — and doing so only from the
supplied dossier — is the drafting step that follows. The companion linter,
``claim_guard.py``, then checks the filled draft for evidence-free assertions.

Supported letter types (slugs)::

    grad-admission      Graduate-admission committee: potential + trajectory
    faculty-hiring      Search committee: research program + independence
    tenure-external     P&T external review: evaluation (NOT advocacy) + standing
    fellowship          Competitive panel: distinctiveness vs the pool
    award-nomination    Awards committee: the single defining contribution

Usage
-----
    # list the supported types and exit
    uv run python letter_scaffold.py --list-types

    # scaffold a tenure external-review letter to a file
    uv run python letter_scaffold.py \
        --type tenure-external \
        --candidate "Dr. A. Yilmaz" \
        --target "promotion to Professor, Dept. of X, University of Y" \
        --relationship "external reviewer; known through the field since 2016" \
        --out letter_skeleton.md

    # offline self-test (no network; verifies every type renders)
    uv run python letter_scaffold.py --self-test

Dependencies: Python standard library only (argparse/sys/textwrap). No network,
no third-party packages — runs under ``uv run python`` with no extra installs.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional

# Claim -> Evidence -> Significance reminder reused in every body section.
CES = (
    "<!-- Claim -> Evidence -> Significance: lead with the evaluative claim, then a "
    "SPECIFIC dossier-sourced example that earns it, then why it matters / how it "
    "ranks. A claim with no example here will be flagged by claim_guard.py. -->"
)


@dataclass
class LetterType:
    slug: str
    title: str
    reader: str
    register: str
    # Body sections: (heading, bracketed prompt for the recommender)
    sections: List[tuple] = field(default_factory=list)
    note: str = ""


LETTER_TYPES: Dict[str, LetterType] = {
    "grad-admission": LetterType(
        slug="grad-admission",
        title="Graduate Admission Recommendation",
        reader="Admissions committee deciding program fit and funding",
        register="Grounded advocacy — argue POTENTIAL from concrete evidence.",
        sections=[
            ("Relationship and basis for assessment",
             "[recommender: course(s) taught / project supervised, capacity, and how long you have known the candidate]"),
            ("Intellectual ability",
             "[recommender: one specific moment showing how the candidate thinks — a question, a problem solved]"),
            ("Research aptitude and independence",
             "[recommender: one concrete instance of independent or original work]"),
            ("Personal qualities for graduate study",
             "[recommender: persistence / collegiality / how they handled a setback — with an example]"),
            ("Calibrated ranking",
             "[recommender: ranking against YOUR OWN students, with the population and basis, e.g. 'top 2 of ~40 I have taught']"),
            ("Recommendation",
             "[recommender: clear statement of support + offer to elaborate]"),
        ],
    ),
    "faculty-hiring": LetterType(
        slug="faculty-hiring",
        title="Faculty Hiring Recommendation",
        reader="Search committee evaluating a future colleague",
        register="Peer assessment — evaluate the RESEARCH PROGRAM, not just talent.",
        sections=[
            ("Relationship and standing to assess",
             "[recommender: how you know the candidate's work and your standing to judge it]"),
            ("Research program",
             "[recommender: the central problem, its originality and significance, and trajectory]"),
            ("Independence and scholarly identity",
             "[recommender: evidence the candidate is independent of advisors/collaborators]"),
            ("Teaching and mentoring",
             "[recommender: teaching/mentoring evidence if known — else leave bracketed]"),
            ("Collegiality and fit",
             "[recommender: collegiality / departmental fit, with an example]"),
            ("Placement in the field and recommendation",
             "[recommender: where the candidate sits in the subfield + your recommendation]"),
        ],
    ),
    "tenure-external": LetterType(
        slug="tenure-external",
        title="Tenure / Promotion External Review",
        reader="P&T committee + administration weighing a permanent decision",
        register="EVALUATION, NOT ADVOCACY — judge the record and standing; "
                 "answer 'would this candidate get tenure at your institution?'",
        sections=[
            ("Relationship and conflict disclosure",
             "[recommender: state the relationship plainly and disclose any conflict / confirm arms-length, with basis for assessment]"),
            ("Central research contribution",
             "[recommender: the lasting, central work and WHY it matters to the field — not a publication count]"),
            ("Impact and influence",
             "[recommender: how the field uses the work — venues, influence, trajectory]"),
            ("Standing relative to peers at the same stage",
             "[recommender: honest comparison to named/anonymized peers at the same career stage, with the comparison basis — omit if you cannot support it]"),
            ("Direct evaluation",
             "[recommender: direct answer to the institution's evaluation question]"),
        ],
        note="External review is evaluative. Overheated praise REDUCES credibility "
             "here; do not write this as an advocacy letter.",
    ),
    "fellowship": LetterType(
        slug="fellowship",
        title="Fellowship Recommendation",
        reader="Competitive selection panel choosing among strong applicants",
        register="Grounded advocacy emphasizing DISTINCTIVENESS vs the pool.",
        sections=[
            ("Relationship and framing against the pool",
             "[recommender: relationship + why the candidate stands out in a strong field]"),
            ("Distinctive strength",
             "[recommender: the defining strength, anchored to a specific accomplishment]"),
            ("Fit to the fellowship's aims",
             "[recommender: how the candidate maps to THIS fellowship's stated criteria/mission]"),
            ("Trajectory the fellowship would accelerate",
             "[recommender: evidence of the trajectory the award is meant to support]"),
            ("Recommendation",
             "[recommender: strong, specific recommendation]"),
        ],
    ),
    "award-nomination": LetterType(
        slug="award-nomination",
        title="Award Nomination",
        reader="Awards committee citing a specific achievement",
        register="Citation-style — tight and focused on the defining contribution.",
        sections=[
            ("Nomination statement",
             "[recommender: who is nominated, for what award]"),
            ("Defining contribution",
             "[recommender: the single defining contribution, precise and anchored]"),
            ("Significance",
             "[recommender: why this contribution merits THIS award]"),
            ("Supporting context",
             "[recommender: brief standing/breadth context if the award asks for it]"),
        ],
    ),
}


def render(
    ltype: LetterType,
    candidate: Optional[str],
    target: Optional[str],
    relationship: Optional[str],
) -> str:
    cand = candidate or "[candidate name and role]"
    tgt = target or "[program / position / award + institution]"
    rel = relationship or "[how, in what capacity, and how long you have known the candidate]"

    out: List[str] = []
    out.append(f"# {ltype.title}")
    out.append("")
    out.append(f"- **Candidate:** {cand}")
    out.append(f"- **Target:** {tgt}")
    out.append(f"- **Reader / decision:** {ltype.reader}")
    out.append(f"- **Register:** {ltype.register}")
    out.append(f"- **Relationship:** {rel}")
    if ltype.note:
        out.append("")
        out.append(f"> NOTE: {ltype.note}")
    out.append("")
    out.append("---")
    out.append("")
    out.append(
        "[Salutation — to the named committee/individual if known, else "
        "'To the Selection/Search Committee:']"
    )
    out.append("")
    for heading, prompt in ltype.sections:
        out.append(f"## {heading}")
        out.append("")
        out.append(CES)
        out.append("")
        out.append(prompt)
        out.append("")
    out.append("[Closing — calibrated to the register above, then signature block.]")
    out.append("")
    out.append("---")
    out.append(
        "<!-- Before sending: fill every bracketed gap from your dossier (do NOT "
        "invent facts), then run claim_guard.py on the finished draft and resolve "
        "every flag by adding evidence or softening the claim. You verify and sign. -->"
    )
    out.append("")
    return "\n".join(out)


def list_types() -> str:
    lines = ["Supported letter types:", ""]
    for t in LETTER_TYPES.values():
        lines.append(f"  {t.slug:<18} {t.title}")
        lines.append(f"  {'':<18} reader: {t.reader}")
    return "\n".join(lines)


def run_self_test() -> int:
    ok = True
    for slug, t in LETTER_TYPES.items():
        text = render(t, "Test Candidate", "Test Target", "test relationship")
        # Every rendered skeleton must carry its title, at least one section, and
        # the Claim->Evidence->Significance reminder.
        checks = [
            t.title in text,
            text.count("## ") >= len(t.sections),
            "Claim -> Evidence -> Significance" in text,
        ]
        status = "PASS" if all(checks) else "FAIL"
        if not all(checks):
            ok = False
        print(f"[{status}] {slug}: sections={text.count('## ')} expected>={len(t.sections)}")
    print("\nSELF-TEST:", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="Emit a type-appropriate recommendation-letter skeleton.",
    )
    ap.add_argument("--type", choices=sorted(LETTER_TYPES), help="Letter type slug.")
    ap.add_argument("--candidate", help="Candidate name and role.")
    ap.add_argument("--target", help="Program / position / award + institution.")
    ap.add_argument("--relationship", help="How/how long the recommender knows them.")
    ap.add_argument("--out", help="Write skeleton to this file (else stdout).")
    ap.add_argument("--list-types", action="store_true", help="List supported types and exit.")
    ap.add_argument("--self-test", action="store_true", help="Run offline self-test and exit.")
    args = ap.parse_args(argv)

    if args.self_test:
        return run_self_test()
    if args.list_types:
        print(list_types())
        return 0
    if not args.type:
        ap.error("--type is required (or use --list-types / --self-test)")

    text = render(LETTER_TYPES[args.type], args.candidate, args.target, args.relationship)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"Wrote {args.type} skeleton to {args.out}", file=sys.stderr)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
