---
name: cite-check
description: Verify that citations actually exist and that the claims they support are faithful to the cited source. Runs deterministic existence checks (Crossref / OpenAlex / Semantic Scholar / arXiv) plus a claim-faithfulness pass via the alterlab-citation-verifier skill.
argument-hint: [path to .bib / manuscript, or pasted references]
disable-model-invocation: true
allowed-tools: Read Write Edit Bash WebFetch WebSearch
---

**Cite-check** the citations in: $ARGUMENTS

Use the `alterlab-citation-verifier` skill. This is a deterministic gate, not a
vibe check — do not assert that a reference is real because it *looks* plausible.

Steps:
1. **Collect** — Parse the references from $ARGUMENTS (a `.bib` file, a manuscript
   path, or a pasted list). If nothing was given, ask for the references or file.
2. **Existence check** — Run `scripts/verify_citations.py` to resolve each reference
   against Crossref, OpenAlex, Semantic Scholar, and arXiv (keyless public APIs via
   WebFetch / `requests` / stdlib `urllib`). Match title and authors with the difflib
   `SequenceMatcher` ratio threshold (≥ 0.70) and resolve any DOI / arXiv ID.
   Flag anything that matches nothing as **likely hallucinated**.
3. **Retraction screen** — Flag items marked retracted in Crossref (`update-to`) or
   OpenAlex (`is_retracted`).
4. **Claim faithfulness** — Where a claim is tied to a citation, check the claim is
   actually supported by that source and map any mismatch to the
   TF / PAC / IH / PH / SH taxonomy.
5. **Report** — A per-citation table: verdict (verified / unverified / hallucinated /
   retracted), the resolver that confirmed it, and the matched DOI/ID. Summarize how
   many of N citations could not be verified.

Degrade gracefully and say so explicitly when the network is unavailable: the script
emits `unverified` verdicts (never a silent pass), and you should fall back to a manual
WebSearch pass as the SKILL.md "Graceful Degradation" section describes.
