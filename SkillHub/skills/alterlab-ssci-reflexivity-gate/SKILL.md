---
name: alterlab-ssci-reflexivity-gate
description: "Gates trustworthiness before qualitative or interpretivist claims are written — the qualitative analog of the measurement gate. Checks that researcher positionality and role are stated, that the four Lincoln & Guba trustworthiness criteria are addressed (credibility via triangulation / member-checking / prolonged engagement, transferability via thick description, dependability via an audit trail, confirmability via reflexive bracketing), and that reflexivity is evidenced rather than asserted. Fail-closed: interpretivist generalizing or causal language is refused without the corresponding warrant. Use when a study is qualitative / ethnographic / interpretivist, when reviewing trustworthiness or reflexivity, or before writing up thematic or grounded-theory findings. For quantitative measurement validity prefer alterlab-ssci-measurement-gate; for running the coding prefer alterlab-qualitative-analysis; for the final claim audit prefer alterlab-ssci-inference-gate. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Bash(python:*)
compatibility: "No API key required. A discipline-enforcing gate; coding execution is handed to alterlab-qualitative-analysis. Reads/writes the YAML Design Passport like the other ssci gates; the optional checklist linter runs locally via `uv run python` (standard library only)."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
    depends_on: "alterlab-ssci-orchestrator (pipeline), alterlab-qualitative-analysis (coding), alterlab-qualitative-methods (methodology); audited by alterlab-ssci-inference-gate"
---

# Reflexivity Gate — Trustworthiness Before the Interpretivist Claim

**Skill type: DISCIPLINE-ENFORCING.** This is the qualitative analog of the measurement gate in
the social-science methods spine. Where the measurement gate asks "is this number a valid,
reliable measure?", the reflexivity gate asks "is this interpretation *trustworthy* — and is the
researcher's hand in it made visible?" It runs no coding itself; it requires the warrant and
routes execution to `alterlab-qualitative-analysis`.

## The Core Rule

```
IN INTERPRETIVE WORK THE RESEARCHER IS THE INSTRUMENT. STATE POSITIONALITY AND EARN TRUSTWORTHINESS
BEFORE MAKING A CLAIM — DON'T ASSERT RIGOR, EVIDENCE IT.
```

Positivist validity does not transfer to interpretivist work. The field's analog is Lincoln &
Guba's **trustworthiness**: credibility, transferability, dependability, confirmability. A
qualitative claim is only as strong as the warrant behind each — and the researcher's positionality
shapes the finding, so it must be declared, not hidden behind a passive voice.

## When to Use This Skill

- "Review the trustworthiness / rigor of my qualitative study."
- "I'm writing up my thematic / grounded-theory / ethnographic findings — am I ready?"
- "How do I address reflexivity and positionality in my methods section?"
- "Can I say my interpretivist findings generalize to other settings?" (← transferability warrant)

### Does NOT Trigger

| The request is really about… | Route to | Why not this skill |
|---|---|---|
| Quantitative scale reliability / validity (omega, CFA, invariance) | `alterlab-ssci-measurement-gate` | This gate is the *qualitative* validity analog. |
| Actually coding the data / computing intercoder reliability | `alterlab-qualitative-analysis` | This gate requires trustworthiness; that skill does the coding. |
| Choosing the qualitative design / method (grounded theory, phenomenology) | `alterlab-qualitative-methods` | Method selection, upstream. |
| Auditing the final written claim against design + evidence | `alterlab-ssci-inference-gate` | Terminal claim audit. |
| Picking the study design in the first place | `alterlab-ssci-design-gate` | Design routing. |

## The four trustworthiness criteria (Lincoln & Guba)

| Criterion | Positivist analog | Warrant the gate requires |
|-----------|-------------------|---------------------------|
| **Credibility** | internal validity | triangulation (data / investigator / method), member-checking, prolonged engagement, negative-case analysis, peer debriefing |
| **Transferability** | external validity | **thick description** of context so a reader can judge fit — NOT a claim of statistical generalization |
| **Dependability** | reliability | an **audit trail**: documented, traceable decisions from raw data to themes |
| **Confirmability** | objectivity | findings grounded in data, not researcher bias — reflexive bracketing, an audit of the chain of evidence |

## Positionality & reflexivity — evidenced, not asserted

Require a positionality statement: the researcher's role, relationship to participants/setting, and
the standpoint (disciplinary, social, personal) that shapes interpretation. "Reflexivity" written as
a one-line claim is not evidence — the gate wants *how* positionality was examined and how it
affected coding/interpretation (e.g. a reflexive journal, bracketing notes, team debriefs).

## Gate verdict semantics (matches the other ssci gates)

- **PASS** — positionality stated; all four trustworthiness criteria have a named, evidenced warrant.
- **WARN** — a criterion is addressed thinly (e.g. member-checking claimed but not described);
  advance with the caveat recorded in `gate_log`.
- **BLOCK (fail-closed)** — no positionality statement at all, OR an **interpretivist generalization /
  causal claim with no transferability (thick-description) warrant**. The claim must be scoped to the
  studied case, or the warrant supplied, before writing proceeds.

## The Design Passport (hand-off)

Append the qualitative-validity stanza the orchestrator threads downstream:

```yaml
positionality: <researcher role, relationship to setting, standpoint — or "MISSING" (BLOCK)>
trustworthiness:
  credibility: <triangulation / member-checking / prolonged engagement — evidence, or "none">
  transferability: <thick description present? scope of any transfer claim>
  dependability: <audit trail present?>
  confirmability: <reflexive bracketing / evidence chain>
reflexivity_evidence: <journal / bracketing / debriefs — how positionality was examined>
claim_scope: <case-bounded (transferable by thick description) | over-generalized (BLOCK)>
```

`alterlab-ssci-inference-gate` later audits the written claims against `claim_scope`.

## Self-Check Before Advancing

- Is positionality stated and its effect on interpretation examined (not just asserted)?
- Does each of the four criteria have a *named, evidenced* warrant, not a bare label?
- Is any generalization scoped by thick description to what the case supports (not statistical)?
- Is the reliability step method-appropriate — a coefficient only for codebook/content-analytic
  work, consensus-and-reflexivity for reflexive TA (routed to `alterlab-qualitative-analysis`)?

## References

- `references/trustworthiness.md` — the four criteria, their techniques, positionality guidance, and a write-up template.
- `scripts/trustworthiness_checklist.py` — stdlib linter flagging missing positionality / criteria / over-generalized claims against the Passport facts.

Part of the AlterLab Academic Skills suite.
