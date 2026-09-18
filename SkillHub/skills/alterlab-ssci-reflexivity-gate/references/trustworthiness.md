# Trustworthiness — Criteria, Techniques, and Write-Up

Loaded on demand from the reflexivity-gate SKILL.md. The interpretivist analog of measurement
validity is Lincoln & Guba's (1985) **trustworthiness**. This gate requires each criterion to have
a *named, evidenced* warrant — not a label.

## The four criteria and their techniques

### Credibility (≈ internal validity)
Are the findings a credible reading of the participants' realities?
- **Triangulation** — data (multiple sources), investigator (multiple analysts), method (multiple
  techniques), theory (multiple lenses).
- **Member checking** — return interpretations to participants for corroboration.
- **Prolonged engagement / persistent observation** — enough time in the field to earn trust and
  distinguish the salient from the incidental.
- **Negative-case analysis** — actively seek and account for disconfirming instances.
- **Peer debriefing** — expose the analysis to a disinterested peer.

### Transferability (≈ external validity)
Can a reader judge whether findings apply to another setting? The warrant is **thick description**
of context, participants, and process — *not* a claim of statistical generalization. The
researcher supplies the description; the reader judges the transfer.

### Dependability (≈ reliability)
Is the process documented and traceable? The warrant is an **audit trail**: raw data → codes →
categories → themes, with the decisions between them recorded so an external auditor could follow
them.

### Confirmability (≈ objectivity)
Are findings grounded in the data rather than the researcher's bias? Warrants: **reflexive
bracketing** (making assumptions explicit and setting them aside), and a **confirmability audit**
of the evidence chain.

## Positionality and reflexivity (evidenced, not asserted)

In interpretive work the researcher is the instrument. A positionality statement names the
researcher's role, relationship to participants/setting, and standpoint (disciplinary, social,
personal), and — crucially — examines *how* that shaped data generation and interpretation. Reflexivity
is evidenced by artifacts: a reflexive journal, bracketing memos, team debriefs, an analytic-decision
log. A single sentence ("I was reflexive throughout") is an assertion, not evidence.

## When a coefficient is (and is not) the right reliability tool

Trustworthiness is not intercoder reliability. Route the reliability step by design:
- **Codebook / content-analytic** coding → compute an ICR coefficient (Krippendorff's α) — hand to
  `alterlab-qualitative-analysis`.
- **Reflexive thematic analysis** → the criterion is *consensus and reflexivity*, not a statistic;
  a coefficient misrepresents the epistemology. The gate says so and does not demand α.

## Write-up template (paste into the methods section / Design Passport)

```yaml
positionality: <role, relationship to setting, standpoint; how it shaped interpretation>
trustworthiness:
  credibility:     <triangulation type / member-checking / prolonged engagement / negative cases>
  transferability: <thick description of context; scope of any transfer claim>
  dependability:   <audit trail: data -> codes -> themes, decisions logged>
  confirmability:  <reflexive bracketing; confirmability audit of the evidence chain>
reflexivity_evidence: <journal / bracketing memos / debriefs / decision log>
claim_scope: <case-bounded, transferable by thick description | over-generalized (BLOCK)>
```

## Common failures this gate catches

- No positionality statement (the researcher's hand is invisible).
- Trustworthiness "criteria" listed as labels with no technique or evidence.
- A generalization ("these findings show that people…") with no thick-description warrant.
- A reliability coefficient forced onto reflexive TA where consensus/reflexivity is the criterion.

## References

- Lincoln, Y. S., & Guba, E. G. (1985). *Naturalistic Inquiry.*
- Nowell, L. S., et al. (2017). Thematic analysis: striving to meet the trustworthiness criteria.
- Braun, V., & Clarke, V. (2021). *Thematic Analysis: A Practical Guide* (reflexive TA).
- Tracy, S. J. (2010). Qualitative quality: eight "big-tent" criteria.
