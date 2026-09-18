#!/usr/bin/env python3
"""claim_faithfulness.py — score claim support against a cited work's abstract.

Given one or more (claim, DOI) pairs, this tool fetches the cited work's abstract
from Crossref (primary) or OpenAlex (fallback, with inverted-index reconstruction)
and scores whether the abstract **supports**, **contradicts**, or leaves the claim
**unsupported**. It is the Phase-E ("Semantic Hallucination", SH) half of the
AlterLab citation gate; existence/metadata checks (TF/PAC/IH/PH) live in
``verify_citations.py``.

Two scoring tiers are available:

* ``heuristic`` (default, deterministic, offline-friendly once the abstract is
  fetched): a transparent keyword-overlap + lightweight negation/antonym signal.
  It is **honest about its limits** — it cannot do real entailment, so its
  default verdict is ``unsupported`` (abstain) rather than a false ``support``.
* ``llm`` (optional): an LLM-judge tier that asks the model configured via the
  ``ALTERLAB_MODEL`` convention (see ``skills/core/shared/model_env.md``) to
  classify support/contradict/unsupported. NEVER hardcodes a model id. Falls back
  to the heuristic verdict (clearly flagged) if the ``claude`` CLI is unavailable.

The abstract is the ceiling of what this tool can see. An abstract that does not
mention the claim is **not** evidence of contradiction — only of non-coverage.
The tool therefore returns ``unsupported`` (not ``contradict``) in that case, and
the verdict object records ``abstract_only: true`` so downstream consumers never
mistake an abstract-level pass for full-text verification.

Verdict vocabulary (this tool) and its mapping to the corpus claim taxonomy
(``integrity_verification_agent.md`` Phase E / SH; see ``docs/integrity.md``):

    support      -> VERIFIED            (claim consistent with abstract)
    contradict   -> MAJOR_DISTORTION/SH (abstract asserts the opposite)
    unsupported  -> UNVERIFIABLE (abstain) — abstract does not establish the claim

Usage
-----
    # single pair
    uv run python claim_faithfulness.py \
        --claim "Transformers outperform RNNs on translation" \
        --doi 10.5555/3295222.3295349

    # batch from JSON ([{"claim": "...", "doi": "..."}, ...]) -> JSON report
    uv run python claim_faithfulness.py --input pairs.json --json

    # LLM-judge tier (uses $ALTERLAB_MODEL, default reviewed 2026-06-06)
    uv run python claim_faithfulness.py --input pairs.json --tier llm --json

    # offline self-test (no network) on a toy pair
    uv run python claim_faithfulness.py --self-test

Dependencies: Python standard library only (urllib/json/re). No ``requests``,
no third-party packages — runs under ``uv run python`` with no extra installs.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Tuple

# --------------------------------------------------------------------------- #
# Model convention — default reviewed 2026-06-06; override via ALTERLAB_MODEL.  #
# See skills/core/shared/model_env.md before changing the default.             #
# This is the ONLY place a model id literal may appear (rule 1 of model_env).  #
# --------------------------------------------------------------------------- #
DEFAULT_MODEL = "claude-opus-4-8"


def alterlab_model() -> str:
    """Return $ALTERLAB_MODEL if set/non-empty, else the dated default."""
    return os.environ.get("ALTERLAB_MODEL") or DEFAULT_MODEL


# Polite-pool contact; OpenAlex/Crossref give better rate limits with a mailto.
CONTACT_EMAIL = os.environ.get("ALTERLAB_CONTACT_EMAIL", "alterlab.ieu@gmail.com")
USER_AGENT = f"AlterLab-CitationVerifier/2.0 (mailto:{CONTACT_EMAIL})"

VERDICTS = ("support", "contradict", "unsupported")

# Verdict -> corpus taxonomy mapping (see module docstring / docs/integrity.md).
TAXONOMY_MAP = {
    "support": "VERIFIED",
    "contradict": "MAJOR_DISTORTION/SH",
    "unsupported": "UNVERIFIABLE",
}

# Lightweight English stopword set for keyword extraction. Intentionally small
# and transparent — this is a heuristic, not an NLP pipeline.
STOPWORDS = frozenset(
    """
    a an and are as at be been being but by for from had has have he her his
    in into is it its of on or our that the their them they this to was were
    what when where which who will with we you your i s t can may might must
    not no nor than then these those such over under more most less least
    using used use based study paper results show shows showed found find
    """.split()
)

# Cheap negation / polarity signals for the heuristic contradiction check.
NEGATION_TOKENS = frozenset(
    "not no never none cannot without fails failed fail lacks lack absent".split()
)
# Antonym-ish stems that frequently flip a claim's truth value in abstracts.
# Matched at the STEM level (see ``_stem``) so inflections like
# "increase/increases/increasing" and "decrease/decreasing" all collapse and
# compare correctly. Keep these as lowercase stems, not full inflected forms.
ANTONYM_PAIRS = [
    ("increas", "decreas"), ("higher", "lower"), ("more", "fewer"),
    ("positive", "negative"), ("significant", "insignificant"),
    ("effective", "ineffective"), ("improv", "worsen"),
    ("outperform", "underperform"), ("better", "worse"), ("gain", "loss"),
    ("rise", "fall"), ("present", "absent"), ("support", "refut"),
    ("confirm", "refut"), ("reduc", "rais"),
]


def _stem(token: str) -> str:
    """Crude suffix stripper so antonym matching tolerates inflection.

    Deliberately simple and transparent — this is a heuristic, not a lemmatizer.
    """
    for suf in ("ing", "ed", "es", "s", "er", "ly"):
        if token.endswith(suf) and len(token) - len(suf) >= 4:
            return token[: -len(suf)]
    return token


# --------------------------------------------------------------------------- #
# Data model                                                                   #
# --------------------------------------------------------------------------- #
@dataclass
class FaithfulnessResult:
    claim: str
    doi: str
    verdict: str  # one of VERDICTS
    taxonomy: str  # corpus mapping (see TAXONOMY_MAP)
    confidence: float  # 0.0-1.0; heuristic confidence is deliberately capped
    tier: str  # "heuristic" | "llm" | "llm->heuristic-fallback"
    rationale: str
    abstract_only: bool = True  # abstracts only — never claim full-text coverage
    abstract_found: bool = True
    source: str = ""  # "crossref" | "openalex" | ""
    signals: Dict[str, Any] = field(default_factory=dict)


# --------------------------------------------------------------------------- #
# Abstract fetching (Crossref primary, OpenAlex fallback)                       #
# --------------------------------------------------------------------------- #
def _http_get_json(url: str, timeout: int = 20) -> Optional[dict]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status != 200:
                return None
            return json.loads(resp.read().decode("utf-8", errors="replace"))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError,
            json.JSONDecodeError, ValueError):
        return None


_TAG_RE = re.compile(r"<[^>]+>")


def _strip_jats(text: str) -> str:
    """Crossref abstracts are JATS-XML; strip tags to plain text."""
    return re.sub(r"\s+", " ", _TAG_RE.sub(" ", text)).strip()


def _reconstruct_openalex_abstract(inv: Dict[str, List[int]]) -> str:
    """Rebuild plain text from OpenAlex abstract_inverted_index."""
    if not inv:
        return ""
    positions: List[Tuple[int, str]] = []
    for word, idxs in inv.items():
        for i in idxs:
            positions.append((i, word))
    positions.sort(key=lambda p: p[0])
    return " ".join(word for _, word in positions)


def fetch_abstract(doi: str, timeout: int = 20) -> Tuple[Optional[str], str]:
    """Return (abstract_text_or_None, source). Crossref first, then OpenAlex."""
    doi_clean = doi.strip()
    doi_clean = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", doi_clean, flags=re.I)
    enc = urllib.parse.quote(doi_clean, safe="")

    # 1) Crossref
    cr = _http_get_json(
        f"https://api.crossref.org/works/{enc}?mailto={urllib.parse.quote(CONTACT_EMAIL)}",
        timeout=timeout,
    )
    if cr:
        abstract = (cr.get("message") or {}).get("abstract")
        if abstract:
            text = _strip_jats(abstract)
            if text:
                return text, "crossref"

    # 2) OpenAlex (reconstruct from inverted index)
    oa = _http_get_json(
        f"https://api.openalex.org/works/doi:{enc}?mailto={urllib.parse.quote(CONTACT_EMAIL)}",
        timeout=timeout,
    )
    if oa:
        inv = oa.get("abstract_inverted_index")
        if inv:
            text = _reconstruct_openalex_abstract(inv)
            if text:
                return text, "openalex"

    return None, ""


# --------------------------------------------------------------------------- #
# Tier 1 — heuristic (keyword overlap + entailment-lite). Honest about limits.  #
# --------------------------------------------------------------------------- #
def _tokenize(text: str) -> List[str]:
    return re.findall(r"[a-z][a-z0-9\-]+", text.lower())


def _content_terms(text: str) -> List[str]:
    return [t for t in _tokenize(text) if t not in STOPWORDS and len(t) > 2]


def _negation_count(text: str) -> int:
    toks = set(_tokenize(text))
    return sum(1 for n in NEGATION_TOKENS if n in toks)


def heuristic_score(claim: str, abstract: str) -> FaithfulnessResult:
    """Transparent keyword-overlap + lightweight polarity heuristic.

    Design principle: this tier CANNOT do real entailment, so it is biased toward
    abstaining (``unsupported``) rather than emitting a false ``support``. It only
    asserts ``support`` on strong lexical overlap, and ``contradict`` only when an
    explicit antonym/negation-polarity flip co-occurs with topical overlap.

    Known blind spots (documented honestly, not worked around): bag-of-words
    overlap is invariant to word order, so SUBJECT-OBJECT ROLE REVERSAL ("A
    outperforms B" vs "B outperforms A") looks identical and will read as
    ``support``; it also misses numeric mismatches, scope/qualifier changes, and
    sarcasm. Use the ``llm`` tier or full-text verification when role/number
    fidelity matters. The heuristic's job is to cheaply triage, not to adjudicate.
    """
    claim_terms = set(_content_terms(claim))
    abs_terms = set(_content_terms(abstract))

    if not claim_terms:
        return FaithfulnessResult(
            claim=claim, doi="", verdict="unsupported",
            taxonomy=TAXONOMY_MAP["unsupported"], confidence=0.0,
            tier="heuristic",
            rationale="Claim contains no content-bearing terms to match.",
            signals={"overlap": 0.0},
        )

    overlap_terms = claim_terms & abs_terms
    overlap = len(overlap_terms) / len(claim_terms)

    # Polarity / antonym-flip signal: does the abstract assert the opposite of a
    # directional word in the claim, given topical overlap? Compared on stemmed
    # token sets so inflections (increase/increases/increasing) line up.
    claim_stems = {_stem(t) for t in _tokenize(claim)}
    abs_stems = {_stem(t) for t in _tokenize(abstract)}
    flips: List[str] = []
    for a, b in ANTONYM_PAIRS:
        ca, cb = a in claim_stems, b in claim_stems
        aa, ab = a in abs_stems, b in abs_stems
        # Claim says one pole, abstract says the other and NOT the claim's pole.
        if (ca and ab and not aa) or (cb and aa and not ab):
            flips.append(f"{a}/{b}")

    neg_delta = abs(_negation_count(claim) - _negation_count(abstract))

    signals = {
        "overlap": round(overlap, 3),
        "overlap_terms": sorted(overlap_terms),
        "n_claim_terms": len(claim_terms),
        "antonym_flips": flips,
        "negation_delta": neg_delta,
    }

    # Decision logic — deliberately conservative.
    if overlap >= 0.30 and flips:
        verdict = "contradict"
        # confidence capped: abstract-level lexical flip is suggestive, not proof
        conf = min(0.55, 0.30 + 0.10 * len(flips))
        rationale = (
            f"Topical overlap ({overlap:.0%}) with polarity flip on "
            f"{', '.join(flips)} — abstract appears to assert the opposite. "
            "Heuristic only; confirm against full text."
        )
    elif overlap >= 0.60 and not flips and neg_delta == 0:
        verdict = "support"
        conf = min(0.60, 0.30 + overlap * 0.40)  # cap heuristic 'support' at 0.60
        rationale = (
            f"Strong lexical overlap ({overlap:.0%}) and no polarity conflict. "
            "Heuristic lexical match only — NOT semantic entailment; verify key "
            "numbers/qualifiers against full text."
        )
    else:
        verdict = "unsupported"
        conf = 0.20 if overlap < 0.30 else 0.30
        if overlap >= 0.60 and neg_delta != 0:
            why = (
                f"Lexical overlap is high ({overlap:.0%}) but a negation "
                f"mismatch (delta={neg_delta}) makes naive 'support' unsafe"
            )
        elif overlap >= 0.60:
            why = (
                f"Lexical overlap is high ({overlap:.0%}) but a polarity/"
                "negation signal prevents a confident 'support'"
            )
        else:
            why = f"Lexical overlap {overlap:.0%} is below the support threshold"
        rationale = (
            f"{why} and no clear contradiction signal. Heuristic abstains: the "
            "abstract does not establish the claim (this is non-coverage, not "
            "refutation). Use the llm tier or full text to resolve."
        )

    return FaithfulnessResult(
        claim=claim, doi="", verdict=verdict, taxonomy=TAXONOMY_MAP[verdict],
        confidence=round(conf, 3), tier="heuristic", rationale=rationale,
        signals=signals,
    )


# --------------------------------------------------------------------------- #
# Tier 2 — optional LLM judge (uses ALTERLAB_MODEL; never hardcodes an id)      #
# --------------------------------------------------------------------------- #
_LLM_PROMPT = """You are a strict citation-faithfulness judge.

Decide whether the cited work's ABSTRACT supports, contradicts, or leaves the \
CLAIM unsupported. You can see ONLY the abstract, not the full text. If the \
abstract does not contain enough information to establish the claim, answer \
"unsupported" (this is non-coverage, NOT contradiction). Answer "contradict" \
only if the abstract asserts something logically incompatible with the claim.

Respond with a single minified JSON object and nothing else:
{{"verdict": "support|contradict|unsupported", "confidence": 0.0-1.0, \
"rationale": "one sentence"}}

CLAIM:
{claim}

ABSTRACT:
{abstract}
"""


def _claude_cli_available() -> bool:
    try:
        subprocess.run(
            ["claude", "--version"],
            capture_output=True, timeout=15, check=False,
        )
        return True
    except (FileNotFoundError, subprocess.SubprocessError):
        return False


def _extract_json_object(text: str) -> Optional[dict]:
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


def llm_score(claim: str, abstract: str, timeout: int = 120) -> FaithfulnessResult:
    """LLM-judge tier. Falls back to the heuristic (flagged) if CLI is missing."""
    fallback = heuristic_score(claim, abstract)

    if not _claude_cli_available():
        fallback.tier = "llm->heuristic-fallback"
        fallback.rationale = (
            "LLM tier requested but `claude` CLI unavailable; "
            "degraded to heuristic. " + fallback.rationale
        )
        return fallback

    prompt = _LLM_PROMPT.format(claim=claim, abstract=abstract[:6000])
    try:
        proc = subprocess.run(
            ["claude", "--model", alterlab_model(), "-p", prompt],
            capture_output=True, text=True, timeout=timeout, check=False,
        )
    except subprocess.SubprocessError as exc:
        fallback.tier = "llm->heuristic-fallback"
        fallback.rationale = (
            f"LLM tier failed ({type(exc).__name__}); degraded to heuristic. "
            + fallback.rationale
        )
        return fallback

    parsed = _extract_json_object(proc.stdout or "")
    if not parsed or parsed.get("verdict") not in VERDICTS:
        fallback.tier = "llm->heuristic-fallback"
        fallback.rationale = (
            "LLM tier returned unparseable output; degraded to heuristic. "
            + fallback.rationale
        )
        return fallback

    verdict = parsed["verdict"]
    try:
        conf = float(parsed.get("confidence", 0.5))
    except (TypeError, ValueError):
        conf = 0.5
    conf = max(0.0, min(1.0, conf))

    return FaithfulnessResult(
        claim=claim, doi="", verdict=verdict, taxonomy=TAXONOMY_MAP[verdict],
        confidence=round(conf, 3), tier="llm",
        rationale=str(parsed.get("rationale", "")).strip()[:400]
        or "(no rationale returned)",
        signals={"model": alterlab_model()},
    )


# --------------------------------------------------------------------------- #
# Orchestration                                                                #
# --------------------------------------------------------------------------- #
def score_pair(
    claim: str, doi: str, tier: str = "heuristic",
    abstract_override: Optional[str] = None, timeout: int = 20,
) -> FaithfulnessResult:
    """Score one (claim, DOI) pair. ``abstract_override`` skips network (tests)."""
    if abstract_override is not None:
        abstract, source = abstract_override, "override"
    else:
        abstract, source = fetch_abstract(doi, timeout=timeout)

    if not abstract:
        return FaithfulnessResult(
            claim=claim, doi=doi, verdict="unsupported",
            taxonomy=TAXONOMY_MAP["unsupported"], confidence=0.0,
            tier=tier, abstract_found=False, source=source,
            rationale=(
                "No abstract available from Crossref or OpenAlex for this DOI. "
                "Cannot assess faithfulness — treat as UNVERIFIABLE_ACCESS and "
                "fall back to full-text / WebSearch verification."
            ),
            signals={},
        )

    if tier == "llm":
        result = llm_score(claim, abstract, timeout=max(timeout, 120))
    else:
        result = heuristic_score(claim, abstract)

    result.doi = doi
    result.source = source
    return result


def score_pairs(
    pairs: List[Dict[str, str]], tier: str = "heuristic", timeout: int = 20,
) -> List[FaithfulnessResult]:
    out: List[FaithfulnessResult] = []
    for p in pairs:
        out.append(score_pair(p.get("claim", ""), p.get("doi", ""), tier=tier, timeout=timeout))
    return out


# --------------------------------------------------------------------------- #
# Self-test (offline, deterministic; no network)                               #
# --------------------------------------------------------------------------- #
_TOY_ABSTRACT = (
    "We introduce the Transformer, a model architecture based solely on "
    "attention mechanisms, dispensing with recurrence entirely. Experiments on "
    "machine translation tasks show these models outperform recurrent networks "
    "in quality while being more parallelizable and requiring less time to "
    "train, decreasing the training time needed relative to prior approaches."
)


def run_self_test() -> int:
    cases = [
        # claim, abstract_override, expected_verdict
        (
            "Transformers outperform recurrent networks on machine translation",
            _TOY_ABSTRACT, "support",
        ),
        # Polarity flip the bag-of-words heuristic CAN catch: the claim asserts
        # an *increase* in training time; the abstract reports a *decrease*.
        (
            "The Transformer architecture increases the training time required "
            "for machine translation models relative to recurrent networks",
            _TOY_ABSTRACT, "contradict",
        ),
        (
            "Transformers reduce carbon emissions in data centers by 40 percent",
            _TOY_ABSTRACT, "unsupported",
        ),
    ]
    ok = True
    for claim, abstract, expected in cases:
        r = score_pair(claim, "10.0000/self-test", tier="heuristic",
                       abstract_override=abstract)
        status = "PASS" if r.verdict == expected else "FAIL"
        if r.verdict != expected:
            ok = False
        print(f"[{status}] expected={expected:<12} got={r.verdict:<12} "
              f"conf={r.confidence:.2f} :: {claim}")
        print(f"        rationale: {r.rationale}")
    print("\nSELF-TEST:", "OK" if ok else "FAILED")
    return 0 if ok else 1


# --------------------------------------------------------------------------- #
# CLI                                                                          #
# --------------------------------------------------------------------------- #
def _load_pairs(args: argparse.Namespace) -> List[Dict[str, str]]:
    if args.input:
        with open(args.input, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, list):
            raise SystemExit("--input JSON must be a list of {claim, doi} objects")
        return data
    if args.claim and args.doi:
        return [{"claim": args.claim, "doi": args.doi}]
    raise SystemExit("Provide --claim and --doi, or --input pairs.json, or --self-test")


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="Score (claim, DOI) faithfulness against the cited abstract.",
    )
    ap.add_argument("--claim", help="A single claim string.")
    ap.add_argument("--doi", help="DOI for the single claim.")
    ap.add_argument("--input", help="JSON file: [{\"claim\":..., \"doi\":...}, ...]")
    ap.add_argument("--tier", choices=["heuristic", "llm"], default="heuristic",
                    help="Scoring tier (default: heuristic).")
    ap.add_argument("--timeout", type=int, default=20, help="HTTP timeout seconds.")
    ap.add_argument("--json", action="store_true", help="Emit JSON report.")
    ap.add_argument("--self-test", action="store_true",
                    help="Run offline deterministic self-test and exit.")
    args = ap.parse_args(argv)

    if args.self_test:
        return run_self_test()

    pairs = _load_pairs(args)
    results = score_pairs(pairs, tier=args.tier, timeout=args.timeout)

    if args.json:
        print(json.dumps([asdict(r) for r in results], indent=2, ensure_ascii=False))
    else:
        for r in results:
            print(f"verdict={r.verdict}  taxonomy={r.taxonomy}  "
                  f"conf={r.confidence:.2f}  tier={r.tier}  source={r.source}")
            print(f"  claim: {r.claim}")
            print(f"  doi:   {r.doi}")
            print(f"  why:   {r.rationale}\n")

    # Exit non-zero if any pair contradicts — useful as a CI gate.
    return 1 if any(r.verdict == "contradict" for r in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
