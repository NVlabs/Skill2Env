# Evidence-Anchored Claims and Calibrated Specificity

The quality of a recommendation letter is decided almost entirely by **how its
claims relate to evidence**. A strong letter is not the one with the most
superlatives; it is the one where every strong claim is *earned* by something the
reader can act on. This file is the rulebook behind `scripts/claim_guard.py`.

---

## The Claim → Evidence → Significance pattern

Every evaluative claim in a letter should travel through three beats:

1. **Claim** — the evaluative assertion ("an unusually independent researcher").
2. **Evidence** — a specific, checkable instance from the dossier ("after a null
   result in year two she reframed the question and designed the follow-up assay
   herself").
3. **Significance / calibration** — why that evidence matters and how it ranks
   ("work I would expect from a senior postdoc, not a second-year student").

A claim that reaches the reader **without beat 2** is the defect this skill
exists to prevent. The reader cannot distinguish a recommender who has watched the
candidate closely from one writing warm boilerplate.

---

## The claim taxonomy (what the guard looks for)

| Pattern | Example | Why it is flagged |
|---|---|---|
| **Unsupported superlative** | "the best student I have ever taught" with no following instance | A maximal claim with no evidence is read as inflation |
| **Unanchored ranking** | "top 1%" / "top 5 students" with no denominator or basis | A ranking with no population is uncheckable |
| **Evidence-free evaluative claim** | "exceptionally creative", "a natural leader" with no nearby example | An adjective the reader cannot verify |
| **Borrowed comparison** | "top 5%" the recommender never actually computed | A comparison the writer cannot stand behind = fabrication |

The guard is a **lint, not a censor**: it flags these patterns and prompts the
recommender to either *anchor* the claim with a real example or *soften* it. It
never deletes the claim and never invents the missing evidence.

---

## Calibrated specificity — superlatives are good, *when grounded*

The fix for an inflated letter is **not** to strip out all strong language —
hedged, generic letters hurt strong candidates. The fix is **calibration**: make
every strong claim *grounded* and *bounded*.

Weak vs. strong forms of the same praise:

- ✗ "She is in the top 1% of students." (no population, no basis)
- ✓ "She is, with one other, the strongest of the ~40 PhD students I have advised
  over 18 years." (population + basis + bound)

- ✗ "He is an exceptional teacher."
- ✓ "His intro-mechanics sections drew the highest evaluations in our department
  that term, and two students switched into the major after taking them."

### Ranking grammar

A defensible ranking states three things: the **superlative or percentile**, the
**population** it is drawn from, and the **recommender's basis** for the
comparison. Drop any of the three and the ranking weakens. Never *upgrade* a
ranking the recommender gave you (do not turn "one of my best" into "the best").

### Comparison rhetoric (especially external review)

Tenure external-review letters are frequently asked for an explicit comparison to
**named or anonymized peers at the same career stage**. Make the comparison set
explicit and the basis honest ("relative to others I have reviewed for tenure in
this subfield in the past five years"). Decline to manufacture a comparison the
writer is not positioned to make; say so rather than fabricating a peer set.

---

## Register, not just evidence

Calibration also means matching the *strength of language* to the **letter type**
(see `letter_types.md`). Advocacy registers (admission, fellowship, award) permit
warmer language; the external-review register is evaluative and arms-length, where
overheated praise *reduces* credibility. The guard is type-agnostic — it checks
for evidence regardless — but the human author should dial register to type.

---

## What "thin dossier" looks like, and the right response

If the recommender supplies enthusiasm but few specifics, the correct output is a
**draft with bracketed gaps** plus an explicit ask list, e.g.:

> "[recommender: one concrete example of independent problem-solving]"
> Facts still needed: (1) how long / in what capacity you knew the candidate;
> (2) one anchored instance for the independence claim; (3) the population for any
> ranking you want to assert.

Returning a fluent, fully-populated letter built on invented anecdotes is the
failure this skill is designed to refuse. A letter is a **signed personal
attestation**; its content must come from the signer.
