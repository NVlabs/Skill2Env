---
name: alterlab-aperta
description: "Drives TÜBİTAK Açık Bilim Politikası (Open Science Policy) compliance and deposition into Aperta — TÜBİTAK ULAKBİM's national open archive at aperta.ulakbim.gov.tr — encoding the binding mandates (green-road deposit of the accepted manuscript on acceptance; open access within 6 months for fen/mühendislik (STEM) and 12 months for sosyal/beşeri (SSH); İlke-6 documentation when data must stay closed for KVKK/privacy reasons) and scaffolding a TÜBİTAK Veri Yönetim Planı / VYP (data management plan) at grant-application time. Use when depositing to Aperta, complying with the TÜBİTAK açık bilim policy, preparing a TÜBİTAK data management plan (VYP), reporting open-access compliance in a final report, or documenting a justified data embargo. For Zenodo/Dryad/OSF and international DMPs prefer alterlab-open-science; for the KVKK lawful-basis/anonymisation plan prefer alterlab-kvkk-dmp. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Write Edit Bash(python:*) WebFetch
compatibility: "No API key required. Guidance + scaffolding skill; uses WebFetch for live policy/repository checks and optional Python helpers via `uv run python` (stdlib-only, requests optional)."
metadata:
  skill-author: AlterLab
  version: "1.0.0"
  last_updated: "2026-06-06"
  depends_on: "alterlab-kvkk-dmp (İlke-6 closed-data justification), alterlab-open-science (international repositories/DMPs)"
---

# Aperta & TÜBİTAK Open Science Compliance

Turkey's national open-science track. Given a TÜBİTAK-funded output (an
accepted manuscript, a dataset, or a grant proposal that needs a data plan),
this skill turns the **TÜBİTAK Açık Bilim Politikası** (Open Science Policy) into
a concrete checklist: deposit the right object to **Aperta**, set the correct
open-access embargo, justify any closed data under **İlke-6** (Principle 6, the
closed-data clause), and produce a **Veri Yönetim Planı / VYP** (data management
plan) for the application. It is the Turkish/TÜBİTAK counterpart to the
international-facing `alterlab-open-science`.

Canonical Turkish terms used below (English gloss on first use): *açık bilim*
(open science), *Veri Yönetim Planı / VYP* (data management plan), *kabul edilmiş
makale* (accepted manuscript), *ambargo* (embargo), *İlke* (Principle), *etik
kurul* (ethics committee), *KVKK* (Turkish Personal Data Protection Law 6698).

## When to Use This Skill

```
Aperta'ya makalemi nasıl yüklerim? (How do I deposit my article to Aperta?)
Prepare a TÜBİTAK data management plan (VYP) for my 1001 application
My article was just accepted — what does the TÜBİTAK open-science policy require?
Justify keeping my clinical dataset closed under TÜBİTAK İlke-6 (privacy/KVKK)
Document open-access compliance for my project's final report (sonuç raporu)
What embargo applies to my social-sciences paper under TÜBİTAK policy?
```

→ Identify the object (manuscript / dataset / proposal), apply the policy rule
from `references/policy_mandates.md`, and either generate the deposit checklist,
the VYP, or the İlke-6 justification. Always end with the
**verify-against-current-policy** disclaimer (see below).

### Does NOT Trigger

This skill owns **TÜBİTAK/Aperta** open science only. Route adjacent asks to the
correct sibling:

| The ask is really about… | Route to |
|--------------------------|----------|
| Zenodo / Dryad / Figshare / OSF deposit, FAIR, CC licences, an **NSF/NIH/ERC/UKRI** DMP, Green/Gold/Diamond OA in general | `alterlab-open-science` |
| The **KVKK** lawful-basis selector, anonymisation vs pseudonymisation, VERBİS, cross-border transfer plan | `alterlab-kvkk-dmp` |
| Which **etik kurul** (ethics committee) is needed, informed-consent / onam form, TİTCK permit | `alterlab-tr-research-ethics` |
| Scaffolding the **ARDEB 1001 / 1002-A proposal** narrative (özgün değer, yaygın etki, work packages) | `alterlab-tubitak-proposal` |
| Posting a **preprint** to a server (arXiv, bioRxiv, SSRN) before/independent of acceptance, or open-access routes in general | `alterlab-open-science` |
| Writing the TÜBİTAK **sonuç raporu / ara rapor** narrative itself (progress, deliverables) — this skill writes only the open-science/data-deposition compliance statement, not the report body | (out of scope — narrative report writing) |
| Checking a journal's **TR Dizin** indexing status before submitting | `alterlab-trdizin` |
| Depositing a graduate **thesis** to YÖK Ulusal Tez Merkezi | `alterlab-yok-tez` |

The line: this skill answers **"what must I deposit/embargo/justify to satisfy
TÜBİTAK's open-science policy, and how do I do it in Aperta?"** It does not write
the proposal, choose the ethics committee, or run the KVKK analysis — it consumes
the KVKK decision (closed/anonymised?) and emits the İlke-6 justification.

## What Aperta Is

| Property | Value |
|----------|-------|
| Operator | TÜBİTAK ULAKBİM (the national academic-IT centre) |
| URL | `https://aperta.ulakbim.gov.tr/` |
| Role | National open archive for TÜBİTAK-funded outputs, UBYT-incentivised works, TÜBİTAK-affiliated publications, and the research data behind TÜBİTAK academic-journal articles |
| Platform | InvenioRDM-based research-data repository |
| Identifiers | Assigns a **DOI** per record |
| Access modes | Open, **restricted/embargoed**, and **versioned** records — supports keeping a record (or its data) closed while metadata stays open |

Aperta scope and operator are confirmed by ULAKBİM's own page
(`ulakbim.tubitak.gov.tr/en/turkey-open-archive-aperta/`). Full repository
mechanics and the deposit workflow live in `references/aperta_repository.md`.

## The Binding Mandates (summary)

The **TÜBİTAK Açık Bilim Politikası** (in force 14 March 2019) imposes these on
TÜBİTAK-funded research. Full citations, principle numbers, and the exact
embargo wording are in `references/policy_mandates.md` — treat that file as the
authority and cite it, not memory.

1. **Green-road deposit, on acceptance.** Deposit the *kabul edilmiş makale*
   (accepted manuscript / author-accepted version) into Aperta when the article
   is accepted — not only after publication.
2. **Open-access embargo ceilings.** The deposited work must be openly accessible
   within **≤ 6 months** for *fen ve mühendislik bilimleri* (STEM) and
   **≤ 12 months** for *sosyal ve beşeri bilimler* (SSH). These are **ceilings**:
   immediate open access is always allowed and preferred.
3. **VYP at application time.** A *Veri Yönetim Planı* (data management plan)
   covering the full data lifecycle is prepared with the grant application.
4. **İlke-6 closed-data documentation.** Where data must stay closed (e.g.
   personal/clinical data under **KVKK**, commercial confidentiality, security),
   the reason must be documented; the dataset can be deposited to Aperta under
   **restricted access** with open metadata.
5. **Report compliance in the final report.** Open-access/data deposition
   compliance is reported in the project *sonuç raporu* (final report).

> **Do not invent specifics.** Exact embargo start-points, the list of qualifying
> exceptions, and any TRY/figure caps are NOT asserted here unless they are in
> `references/policy_mandates.md`. If a fact is not in that file, omit it and tell
> the user to confirm against the current policy PDF.

## Workflows

### A. Deposit an accepted manuscript or dataset to Aperta

1. Classify the object: *kabul edilmiş makale* vs dataset vs both.
2. Determine the field bucket — STEM (≤ 6 mo) or SSH (≤ 12 mo) — to set the
   embargo ceiling. Default to **immediate open** unless the user needs a delay.
3. Decide access mode: open, or **restricted** if İlke-6 applies (see workflow C).
4. Walk the deposit checklist in `references/aperta_repository.md` (record
   metadata, file upload, licence, DOI minting, version).
5. Confirm the DOI and the open-access date satisfy the embargo ceiling.

### B. Scaffold a TÜBİTAK Veri Yönetim Planı (VYP)

Run the generator, then refine its prose with the user's specifics:

```bash
uv run python skills/turkish-academia/alterlab-aperta/scripts/vyp_scaffold.py \
    --project "Proje adı" --field stem --lang both \
    --data-closed --closed-reason kvkk \
    --out vyp.md
```

- `--field stem|ssh` sets the embargo ceiling cited in the plan.
- `--lang tr|en|both` emits a Turkish VYP, an English DMP, or both.
- `--data-closed` + `--closed-reason kvkk|commercial|security|ethics` injects an
  İlke-6 justification stub. **If the reason is KVKK, hand the lawful-basis /
  anonymisation decision to `alterlab-kvkk-dmp` and paste its conclusion in** —
  this skill records *that* data is closed and *why* at the funder level; it does
  not perform the KVKK analysis.

The VYP section tree the generator follows is documented in
`references/vyp_template.md`.

### C. Justify a closed dataset under İlke-6

1. Confirm the closure reason is legitimate (KVKK personal/special-category data,
   commercial confidentiality, security, or an active ethics restriction).
2. For KVKK reasons, get the lawful-basis + anonymisation outcome from
   `alterlab-kvkk-dmp` first — note that **re-identifiable "anonymised" data does
   not qualify** as truly anonymous.
3. Choose the Aperta access mode: **restricted record with open metadata** (so the
   dataset is discoverable and citable even while access is gated).
4. Write the İlke-6 justification (one paragraph: what data, which legal/ethical
   basis for closure, who may request access, and any future-opening trigger).
5. Carry that justification into both the VYP and the *sonuç raporu*.

### D. Final-report open-access compliance check

Produce a short compliance statement for the *sonuç raporu*: for each output,
list the Aperta DOI, the access mode, and the open-access date, and confirm it
meets the field embargo ceiling — or, if closed, cite the İlke-6 justification.

## Live verification (optional)

When the user needs the current policy or to confirm a repository feature, fetch:

- Policy PDF: `https://tubitak.gov.tr/sites/default/files/tubitak_acik_bilim_politikasi_190316.pdf`
- ULAKBİM Aperta page: `https://ulakbim.tubitak.gov.tr/en/turkey-open-archive-aperta/`
- The repository itself: `https://aperta.ulakbim.gov.tr/`

`scripts/policy_check.py` does a light reachability + keyword probe of these so
you can tell the user whether the live policy matches what this skill encodes
(it does **not** scrape or assert new mandates).

## Verify-Against-Current-Policy Disclaimer

TÜBİTAK revises the Açık Bilim Politikası and Aperta's deposit flow over time.
**Always close by telling the user to confirm the embargo ceilings, the deposit
object, and the VYP template against the current policy PDF and the live Aperta
submission form before they rely on this output.** Never present an embargo month
count or a deposit rule as immutable.

## References

- `references/policy_mandates.md` — the TÜBİTAK Açık Bilim Politikası mandates
  (deposit, 6/12-month ceilings, VYP, İlke-6), with sources and last-verified date.
- `references/aperta_repository.md` — what Aperta is, its InvenioRDM features, and
  the record-by-record deposit checklist.
- `references/vyp_template.md` — the Veri Yönetim Planı / DMP section tree the
  scaffold script emits, bilingual.

Part of the AlterLab Academic Skills suite.
