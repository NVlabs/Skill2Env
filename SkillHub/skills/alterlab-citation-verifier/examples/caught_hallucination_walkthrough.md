---
scenario: A real, existing paper is cited to support a claim it does not make (Frankenstein / Semantic Hallucination)
mode: existence check (verify_citations.py) + claim faithfulness (claim_faithfulness.py)
demonstrates: Why "the citation is real" and "the citation supports the claim" are two separate verdicts, and how the SH verdict is reached deterministically
taxonomy_hit: SH (Semantic Hallucination)
---

# Caught-Hallucination Walk-Through: A Real Paper, the Wrong Claim

This is the failure mode that fools careful humans and shared-training-data LLMs alike: the
cited paper is **completely real** — correct authors, correct year, resolvable DOI, thousands
of citations — and yet it **does not support the sentence it is attached to.** The reference
passes every existence check, so a reviewer skimming the bibliography sees nothing wrong. The
distortion lives in the gap between the claim and the source.

`alterlab-citation-verifier` is built around that gap. It runs **two** deterministic checks
and keeps their verdicts separate:

1. `scripts/verify_citations.py` — *does this work exist?* (Crossref / OpenAlex / Semantic
   Scholar / arXiv resolution, title+author similarity >= 0.70 via difflib `SequenceMatcher`,
   DOI/arXiv-ID resolution, retraction flag from Crossref `update-to` / OpenAlex `is_retracted`).
2. `scripts/claim_faithfulness.py` — *does this work support the claim?* (compares the user's
   sentence against the source's actual content, mapping the result to the
   TF / PAC / IH / PH / SH taxonomy).

A reference can PASS check 1 and FAIL check 2. That is exactly what happens here.

---

## The Request

> **Researcher:** I want to write this sentence in my methods discussion:
>
> > "Randomized controlled trials have shown that smartphone note-taking apps improve
> > undergraduate exam scores by 31% compared to handwriting (Mueller & Oppenheimer, 2014)."
>
> Is that citation supported by the source?
>
> Source: Mueller, P. A., & Oppenheimer, D. M. (2014). The pen is mightier than the keyboard:
> Advantages of longhand over laptop note taking. *Psychological Science, 25*(6), 1159-1168.

A reviewer would recognize Mueller & Oppenheimer (2014) instantly — it is a famous,
frequently cited study. That recognition is the trap: "I know this paper is real" silently
becomes "so the citation must be fine."

---

## Step 1 — Existence Check (`verify_citations.py`)

```
$ echo "Mueller, P. A., & Oppenheimer, D. M. (2014). The pen is mightier than the keyboard:
  Advantages of longhand over laptop note taking. Psychological Science, 25(6), 1159-1168." \
  | uv run python skills/core/alterlab-citation-verifier/scripts/verify_citations.py - \
      --format freeform --mailto alterlab.ieu@gmail.com

Resolving against Crossref / OpenAlex / Semantic Scholar / arXiv...

  Crossref:          MATCH   doi:10.1177/0956797614524581
  OpenAlex:          MATCH   W2relevant-id
  Semantic Scholar:  MATCH   corpusId confirmed
  Title ratio:       1.00  (exact; difflib SequenceMatcher)
  Author match:      Mueller, P. A. / Oppenheimer, D. M.  -> exact
  Retraction flag:   none (Crossref update-to / OpenAlex is_retracted)
  Year / venue:      2014 / Psychological Science 25(6), 1159-1168  -> confirmed

EXISTENCE VERDICT: VERIFIED
```

So far, **everything is green.** The paper is real, the DOI resolves, the metadata matches,
it is not retracted. If the verifier stopped here — the way a bibliography-only check does —
the citation would pass and the fabricated claim would sail into the manuscript.

This is the key design point: **VERIFIED existence is necessary but not sufficient.** The
verifier does not return a final PASS on existence alone when the user has supplied a *claim*.

---

## Step 2 — Claim Faithfulness (`claim_faithfulness.py`)

The verifier now compares the **claim** against what the source actually says.

```
$ uv run python skills/core/alterlab-citation-verifier/scripts/claim_faithfulness.py \
    --claim "smartphone note-taking apps improve undergraduate exam scores by 31% compared to handwriting" \
    --doi 10.1177/0956797614524581 --json

Fetching cited work's abstract (Crossref primary, OpenAlex fallback)...

Claim asserts:
  - intervention:  smartphone note-taking APPS
  - comparator:    handwriting
  - design:        randomized controlled trials
  - effect:        +31% exam scores

Source abstract reports:
  - intervention:  LAPTOP note-taking
  - comparator:    LONGHAND (handwriting)
  - design:        three lab studies (not RCTs of apps)
  - direction:     LONGHAND OUTPERFORMS laptop on conceptual questions
  - effect size:   NO "31%" exam-score figure in the abstract

Mismatch analysis (abstract_only: true):
  - intervention swapped (smartphone apps  <->  laptops) ......... MISMATCH
  - effect direction inverted (claim implies digital helps;
      abstract asserts handwriting helps) ....................... CONTRADICTION
  - "31%" statistic ............................................. NOT IN ABSTRACT (fabricated)

tool verdict:  contradict   (abstract asserts the opposite of the claim)
mapped verdict: MAJOR_DISTORTION / SH (Semantic Hallucination)
```

> Note on tool honesty: the heuristic tier abstains to `unsupported` (UNVERIFIABLE) whenever
> the abstract merely fails to mention a claim — it does NOT cry "contradiction" on silence.
> Here the abstract actively asserts the opposite direction (handwriting wins), so the signal
> is a genuine `contradict`, which the integrity gate maps to SH. The verdict carries
> `abstract_only: true`, so no one mistakes an abstract-level check for full-text verification.

The claim is a **Frankenstein**: a real, recognizable citation stitched onto a statistic the
source never reports, in a direction the source actively contradicts. The source is about
**longhand vs. laptop** note-taking and finds **handwriting wins**; the claim invents a
**smartphone-app RCT** that boosts scores **by 31%**. Three separate distortions, one fake
number, zero support.

---

## The Verdict

```markdown
# Citation Verification Report

## Citation
Mueller, P. A., & Oppenheimer, D. M. (2014). The pen is mightier than the keyboard:
Advantages of longhand over laptop note taking. Psychological Science, 25(6), 1159-1168.

## Existence:  ✅ VERIFIED   (real paper, DOI 10.1177/0956797614524581, not retracted)
## Faithfulness: ❌ FAIL — SH (Semantic Hallucination)

## Why it fails despite being a real paper
The reference EXISTS, but it does NOT support the claim attached to it. The source studies
longhand vs. laptop note-taking and finds handwriting superior; the claim asserts a 31%
exam-score gain from smartphone APPS via RCTs. The intervention is wrong, the effect
direction is inverted, and the 31% figure is fabricated (not present in the source).

## Taxonomy
SH — Semantic Hallucination: citation resolves but does not support the claim it is attached to.

## Recommended action
Do NOT cite Mueller & Oppenheimer (2014) for this sentence. Either:
  (a) restate the claim to match the source ("longhand note-taking improved performance on
      conceptual test questions relative to laptop note-taking (Mueller & Oppenheimer, 2014)"),
      removing the smartphone-app framing and the fabricated 31%; or
  (b) if you genuinely need a smartphone-app exam-score result, find and verify a source that
      actually reports it — this paper is not it.

## Audit trail
- verify_citations.py: Crossref/OpenAlex/Semantic Scholar all MATCH; title ratio 1.00; no retraction flag.
- claim_faithfulness.py: intervention mismatch, effect-direction contradiction, "31%" absent from source.
```

---

## Why This Matters

### 1. "Real citation" and "supported claim" are different questions
Bibliography-only checks — and most human reviewers — answer only the first. The dangerous
hallucinations of 2024-2026 increasingly pass the first check: the model attaches a famous,
real paper to a claim that paper never made. Separating the two verdicts is the whole point.

### 2. The SH verdict is reached deterministically, not from memory
The verifier never relies on the model "knowing" what Mueller & Oppenheimer found. It
resolves the DOI, fetches the cited work's abstract (Crossref/OpenAlex), and compares that
retrieved text against the claim. Same-source hallucination (the verifier and the writer
sharing training data) cannot launder a false claim through, because the comparison is
against the retrieved abstract, not recall. (The abstract is the ceiling of what the tool
sees; the verdict is stamped `abstract_only: true` so it is never mistaken for full-text
adjudication, and an abstract that is merely silent yields `unsupported`, not a false pass.)

### 3. The fabricated statistic is the tell
The "31%" appears nowhere in the source abstract. Invented precision — a specific percentage,
effect size, or sample count with no counterpart in the cited work — is one of the strongest
signals of a semantic hallucination. The verifier surfaces it rather than rounding past it.

### 4. Graceful degradation keeps the gate honest offline
When the network is unavailable, `verify_citations.py` emits an `unverified` verdict per entry
(repo verdict `UNVERIFIED`) with manual-check instructions, rather than silently returning a
pass; the agent then falls back to a WebSearch pass. An entry it genuinely cannot check is
reported as `unverified`, never quietly marked `verified` — the same zero-gray-zone discipline
the integrity agent enforces.

### 5. This is the case prompt-only taxonomies miss
A prose taxonomy can *describe* SH, but it cannot *retrieve and compare* the source. Wiring
the integrity and bibliography agents to call these two scripts turns the taxonomy from a
description into an executable gate — which is the entire reason this skill exists.
