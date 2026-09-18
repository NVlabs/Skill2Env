---
name: DORA-third-party-register
description: EU DORA Article 28 register of ICT third-party arrangements: critical-or-important provider classification, contract clauses (Article 30), exit strategies, concentration risk assessment
when_to_use: Compliance documentation for regulated archetype with compliance:[dora]. Required for ICT third-party providers in EU financial sector
applies_to:
  - regulated
---

# DORA-third-party-register.md — Article 28 register of ICT third-party arrangements

> Mandatory artefact when `compliance: [dora]` in PROJECT.md.
> Required by `architect.md` compliance artefact gate. Article 28 of DORA mandates a register of all ICT third-party service arrangements at entity and group level.
> Source: `skills/great_cto/templates/DORA-third-party-register.md`.

## Register

| # | Provider | Service | Critical/Important per Art. 31? | Contract date | Subcontractors | Concentration risk | Exit strategy | Last review |
|---|---|---|---|---|---|---|---|---|
| 1 | {AWS} | {hosting + database} | yes | {date} | {chain} | {high if X% of services on this provider} | `docs/compliance/exit-AWS.md` | {date} |
| 2 | {Stripe} | {payment processing} | yes | {date} | {chain} | {assessment} | `docs/compliance/exit-stripe.md` | {date} |
| 3 | {provider} | {service} | {yes/no} | | | | | |

## Per-provider fields (one section per critical-or-important provider)

### {Provider 1}
- **Legal entity:** {name + jurisdiction}
- **Services in scope:** {list of services / data processed}
- **Data location(s):** {EEA / non-EEA + adequacy decision reference}
- **Contract clauses required by Article 30:**
  - [ ] Description of all services
  - [ ] Service location (with notification clause for changes)
  - [ ] Data processing terms (GDPR Art. 28 DPA)
  - [ ] Service levels with monitoring + reporting
  - [ ] Right to access + audit (Article 30(2)(e))
  - [ ] Cooperation with NCA + financial entity supervision
  - [ ] Termination rights (without notice for material breach)
  - [ ] Exit strategies + transition support
- **Concentration risk:** {is this provider >X% of total ICT spend? Are critical services single-vendor?}
- **Subcontractor chain:** {list, with notification rights for changes}
- **Last on-site / remote audit:** {date + findings ref}
- **Exit strategy summary:** {how do we move off this provider in N months — see `exit-{provider}.md`}

## Article 31 — Critical or important provider classification

ESA designation list: {check current ESMA/EBA/EIOPA published list}

| Provider | Designated by ESA? | Date | Implications |
|---|---|---|---|
| | | | (oversight by Lead Overseer; Article 31–44 obligations apply) |

## Article 28(8) — Contract review for material changes
- Review trigger: any of {provider acquisition, service location change, subcontractor change, security incident}
- Review owner: {role}
- Last reviewed: {date}

## Sign-off
| Role | Date |
|---|---|
| CISO | |
| Procurement / Vendor Management | |
| Legal | |
