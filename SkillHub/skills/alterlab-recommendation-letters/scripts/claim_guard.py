#!/usr/bin/env python3
"""claim_guard.py — lint a recommendation-letter draft for evidence-free claims.

This is the **no-fabrication guard** behind ``alterlab-recommendation-letters``.
It scans a finished draft sentence-by-sentence and flags the three defects that
make a letter uninformative or inflated (see ``references/evidence_and_specificity.md``):

    unsupported-superlative   A maximal claim ("the best student I have ever
                              taught") with no concrete instance nearby.
    unanchored-ranking        A ranking/percentile ("top 1%", "top 5 students")
                              with no population or basis stated.
    evidence-free-claim       An evaluative adjective ("exceptionally creative")
                              with no specific, checkable example nearby.

It is a transparent LINT, not a censor or a generator. It NEVER rewrites the
draft and NEVER invents the missing evidence — it flags the sentence and prints a
fix prompt asking the recommender to *anchor* the claim with a real example or
*soften* it. Resolving a flag by adding fabricated support defeats the purpose.

How "evidence nearby" is detected (heuristic, deliberately conservative):
a flagged claim is considered ANCHORED if the same sentence, or an adjacent
sentence, contains a concrete signal — a quoted phrase, a population/basis cue
("of the N students I have advised", "in my X years"), or a specific-instance cue
("for example", "when she", "in 2023 he"). A *bare* number is deliberately NOT an
anchor on its own: a stray digit (a year, a citation count, or the "1" inside an
unanchored "top 1%") must not silently clear the superlatives and adjectives
around it — that bug let an unanchored ranking suppress the very flags it should
sit beside. A number counts as evidence only inside a population/basis or
instance cue (which already require the surrounding words). The heuristic cannot
understand meaning, so it errs toward FLAGGING (false positives the human clears)
rather than passing an unanchored claim. It is a triage aid, not a judge.

Usage
-----
    # human-readable report
    uv run python claim_guard.py letter_draft.md

    # JSON report (for piping / programmatic use)
    uv run python claim_guard.py letter_draft.md --json

    # read from stdin
    uv run python claim_guard.py - < letter_draft.md

    # offline self-test (no network; deterministic fixtures)
    uv run python claim_guard.py --self-test

Exit code: 0 if no flags, 1 if any flag is raised (usable as a pre-send gate).
Dependencies: Python standard library only (argparse/json/re/sys). No network,
no third-party packages — runs under ``uv run python`` with no extra installs.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from typing import List, Optional

# --------------------------------------------------------------------------- #
# Signal vocabularies (transparent; tune in references/evidence_and_specificity.md)
# --------------------------------------------------------------------------- #
SUPERLATIVES = re.compile(
    r"\b(best|finest|strongest|smartest|brightest|greatest|most\s+\w+|"
    r"top|exceptional|outstanding|extraordinary|unparalleled|unmatched|"
    r"without\s+(?:a\s+)?peer|one\s+of\s+the\s+(?:best|finest|strongest|top))\b",
    re.IGNORECASE,
)

# Ranking / percentile language that demands a population + basis.
# A bare "\d+%" is NOT a ranking — effect sizes, error reductions, and score
# percentages are exactly the concrete evidence the skill wants recommenders to
# include. A percentage only counts as a *ranking* in a ranking context: after a
# ranking cue ("top 5%"), or as an explicit percentile ("95th percentile").
RANKING = re.compile(
    r"\b(top\s+\d+\s*%?|top\s+\d+|"
    r"(?:top|rank(?:ed|ing)?|best|strongest|finest)\b[^.]*?\b\d+\s*%|"
    r"\d+\s*(?:st|nd|rd|th)\s+percentile|"
    r"top\s+(?:tier|percentile)|"
    r"rank(?:ed|s|ing)?|percentile|"
    r"one\s+of\s+the\s+(?:best|top|strongest|finest))",
    re.IGNORECASE,
)

# Fixed endorsement-closing formulae ("my strongest possible endorsement",
# "highest recommendation", "without reservation"). Here the superlative modifies
# the *endorsement*, not the candidate — it is boilerplate sign-off, not an
# unsupported claim about the person, so it must not be flagged as a superlative.
ENDORSEMENT_FORMULA = re.compile(
    r"\b(?:strongest|highest|warmest|fullest|unreserved)\s+possible\s+"
    r"(?:endorsement|recommendation|support)\b|"
    r"\b(?:strongest|highest|warmest|fullest)\s+(?:endorsement|recommendation|support)\b|"
    r"\bwithout\s+(?:reservation|hesitation|qualification)\b",
    re.IGNORECASE,
)

# Bare evaluative adjectives that need a concrete instance.
EVAL_ADJECTIVES = re.compile(
    r"\b(brilliant|creative|innovative|independent|diligent|dedicated|"
    r"talented|gifted|remarkable|impressive|insightful|rigorous|"
    r"hardworking|hard-working|conscientious|exceptional|outstanding|"
    r"a\s+natural\s+leader|a\s+born\s+\w+)\b",
    re.IGNORECASE,
)

# Concrete-evidence signals: if present in or adjacent to the claim, treat the
# claim as anchored and do not flag it.
#
# A bare digit is intentionally NOT in this set. Counting any "\b\d" as evidence
# let a stray number (a year, a citation count, or the "1" inside an unanchored
# "top 1%") clear the superlatives and adjectives around it — so an unanchored
# ranking paradoxically suppressed the flags it should sit beside. Numbers only
# count as evidence when they appear inside a POPULATION_BASIS or INSTANCE_CUE
# match, both of which require the surrounding words ("of the 40 students",
# "in 2023 she …") rather than a digit on its own.
QUOTE = re.compile(r"[\"“”‘’']")
POPULATION_BASIS = re.compile(
    r"\b(of\s+the\s+\d+|of\s+(?:my|the)\s+\w+\s+(?:students|advisees|reviewees|"
    r"applicants|candidates|colleagues)|"
    r"in\s+(?:my|the\s+past)\s+\d+\s+years|over\s+\d+\s+years|"
    r"i\s+have\s+(?:advised|taught|supervised|reviewed|mentored)|"
    r"the\s+\d+\s+(?:students|candidates)|"
    r"cohort|out\s+of)\b",
    re.IGNORECASE,
)
# Strong, keyword-bearing instance cues. These name an example explicitly
# ("for example", "when she", "after the …"), so they anchor across the window —
# including into an adjacent sentence, which is the canonical "Claim. For
# example, …" pattern the skill recommends.
INSTANCE_CUE = re.compile(
    r"\b(for\s+example|for\s+instance|specifically|in\s+particular|"
    r"e\.g\.|such\s+as|when\s+(?:she|he|they|the\s+candidate)|"
    r"during\s+\w+|after\s+(?:a|the|her|his|their))\b",
    re.IGNORECASE,
)
# A bare year ("in 2019") is a weak, number-only cue. It anchors a claim ONLY in
# the SAME sentence ("in 2023 he designed the follow-up assay himself"), never
# across a sentence boundary — a date stamped on a separate, generic sentence
# ("She attended a conference in 2019.") must not clear an unrelated adjective.
YEAR_CUE = re.compile(r"\bin\s+(?:19|20)\d{2}\b", re.IGNORECASE)

REASONS = {
    "unsupported-superlative": "Maximal claim with no concrete instance nearby — anchor it with a specific example or soften it.",
    "unanchored-ranking": "Ranking/percentile with no population or basis — state the population AND your basis (e.g. 'top 2 of ~40 I have advised'), or drop it.",
    "evidence-free-claim": "Evaluative adjective with no specific example nearby — add a concrete, dossier-sourced instance or soften the claim.",
}


@dataclass
class Flag:
    sentence_index: int
    sentence: str
    code: str
    matched: str
    reason: str


_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
# Markdown noise to strip before sentence analysis (headings, comments, bullets).
_HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_BRACKET_PROMPT = re.compile(r"\[recommender:.*?\]", re.IGNORECASE | re.DOTALL)


def _clean(text: str) -> str:
    text = _HTML_COMMENT.sub(" ", text)
    text = _BRACKET_PROMPT.sub(" ", text)  # scaffold prompts are not claims
    return text


def split_sentences(text: str) -> List[str]:
    out: List[str] = []
    for raw_line in _clean(text).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith(">"):
            continue
        line = line.lstrip("-*").strip()
        if not line:
            continue
        for s in _SENT_SPLIT.split(line):
            s = s.strip()
            if s:
                out.append(s)
    return out


def _has_evidence(window: str, sentence: str = "") -> bool:
    """Does the text contain a concrete-evidence signal?

    ``window`` is the claim sentence plus its neighbours; ``sentence`` is the
    claim sentence alone. A bare number is deliberately not a signal: only a
    quoted phrase, a population/basis cue, or a keyword instance cue anchors
    across the window. A bare year (``YEAR_CUE``) is a weak, number-only signal
    that anchors ONLY when it is in the claim sentence itself — a date on a
    separate generic sentence must not clear an unrelated claim.
    """
    return bool(
        QUOTE.search(window)
        or POPULATION_BASIS.search(window)
        or INSTANCE_CUE.search(window)
        or (sentence and YEAR_CUE.search(sentence))
    )


def _strip_rankings(text: str) -> str:
    """Blank out RANKING matches so a ranking cannot count as evidence.

    A sentence's own ranking — and its neighbours' rankings — must NOT anchor a
    superlative or adjective: an unanchored "top 1%" is itself a flagged defect,
    not the evidence that earns the praise beside it. Removing ranking spans
    before the evidence check keeps a ranking from self-anchoring or anchoring
    the sentences around it.
    """
    return RANKING.sub(" ", text)


def lint(text: str) -> List[Flag]:
    sentences = split_sentences(text)
    flags: List[Flag] = []
    for i, sent in enumerate(sentences):
        prev_s = sentences[i - 1] if i > 0 else ""
        next_s = sentences[i + 1] if i + 1 < len(sentences) else ""
        window = " ".join([prev_s, sent, next_s])
        # Evidence is judged on the window with all ranking spans removed, so an
        # unanchored ranking can never clear the claims it sits beside. A bare
        # year only anchors when it is in the claim sentence itself.
        anchored = _has_evidence(_strip_rankings(window), _strip_rankings(sent))

        # Ranking is the strictest: a ranking ("top 5%", "ranks in the top tier")
        # needs an explicit POPULATION/BASIS in-window — a nearby unrelated number
        # (e.g. a citation count) does NOT anchor a percentile claim.
        m_rank = RANKING.search(sent)
        if m_rank and not POPULATION_BASIS.search(window):
            flags.append(Flag(i, sent, "unanchored-ranking",
                              m_rank.group(0), REASONS["unanchored-ranking"]))
            continue

        if anchored:
            continue  # superlative/adjective is earned by nearby evidence

        # An endorsement-closing formula ("my strongest possible endorsement")
        # uses a superlative to qualify the *endorsement*, not the candidate —
        # standard boilerplate sign-off, not an unsupported claim about a person.
        if ENDORSEMENT_FORMULA.search(sent):
            continue

        m_sup = SUPERLATIVES.search(sent)
        if m_sup:
            flags.append(Flag(i, sent, "unsupported-superlative",
                              m_sup.group(0), REASONS["unsupported-superlative"]))
            continue

        m_adj = EVAL_ADJECTIVES.search(sent)
        if m_adj:
            flags.append(Flag(i, sent, "evidence-free-claim",
                              m_adj.group(0), REASONS["evidence-free-claim"]))
    return flags


def report_text(flags: List[Flag], n_sentences: int) -> str:
    if not flags:
        return f"OK — no evidence-free claims flagged across {n_sentences} sentences."
    lines = [f"FLAGGED {len(flags)} claim(s) needing evidence (of {n_sentences} sentences):", ""]
    for f in flags:
        lines.append(f"  [{f.code}] matched: {f.matched!r}")
        lines.append(f"    sentence: {f.sentence}")
        lines.append(f"    fix: {f.reason}")
        lines.append("")
    lines.append("Resolve each by ADDING the recommender's real example or SOFTENING "
                 "the claim — never by inventing support.")
    return "\n".join(lines)


def run_self_test() -> int:
    cases = [
        # (text, expected_codes_subset)
        ("She is the best student I have ever taught.", {"unsupported-superlative"}),
        ("He ranks in the top 1% of researchers.", {"unanchored-ranking"}),
        ("She is exceptionally creative.", {"evidence-free-claim"}),
        # Regression: an unanchored ranking must NOT suppress the superlative or
        # adjective beside it. The "1" in "top 1%" used to anchor both neighbours.
        ("She is the best student I have ever had. She is in the top 1% of students.",
         {"unsupported-superlative", "unanchored-ranking"}),
        ("She is exceptionally creative. She attended a conference in 2019.",
         {"evidence-free-claim"}),
        ("He is remarkably innovative. His h-index is 12.", {"evidence-free-claim"}),
        # Anchored — should NOT flag:
        ("She is the strongest of the ~40 PhD students I have advised over 18 years.", set()),
        ("He is exceptionally creative: in 2023 he designed the follow-up assay himself "
         "after a null result.", set()),
        # Regression: a factual metric percentage is concrete evidence, not an
        # unanchored ranking — "30%" here must NOT flag.
        ("Her method reduced error by 30%.", set()),
        ("Accuracy improved from 70% to 92% under her redesign.", set()),
        # An endorsement-closing formula is boilerplate, not an unsupported claim.
        ("I give her my strongest possible endorsement.", set()),
    ]
    ok = True
    for text, expected in cases:
        flags = lint(text)
        codes = {f.code for f in flags}
        passed = expected.issubset(codes) if expected else not flags
        if not passed:
            ok = False
        print(f"[{'PASS' if passed else 'FAIL'}] expected={sorted(expected) or 'no-flags'} "
              f"got={sorted(codes) or 'no-flags'} :: {text[:60]}")
    print("\nSELF-TEST:", "OK" if ok else "FAILED")
    return 0 if ok else 1


def _read_input(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="Lint a recommendation-letter draft for evidence-free claims.",
    )
    ap.add_argument("path", nargs="?", help="Draft file, or '-' for stdin.")
    ap.add_argument("--json", action="store_true", help="Emit a JSON report.")
    ap.add_argument("--self-test", action="store_true", help="Run offline self-test and exit.")
    args = ap.parse_args(argv)

    if args.self_test:
        return run_self_test()
    if not args.path:
        ap.error("provide a draft path (or '-' for stdin), or use --self-test")

    text = _read_input(args.path)
    flags = lint(text)
    n = len(split_sentences(text))

    if args.json:
        print(json.dumps(
            {"total_sentences": n, "flag_count": len(flags),
             "flags": [asdict(f) for f in flags]},
            indent=2, ensure_ascii=False,
        ))
    else:
        print(report_text(flags, n))

    return 1 if flags else 0


if __name__ == "__main__":
    raise SystemExit(main())
