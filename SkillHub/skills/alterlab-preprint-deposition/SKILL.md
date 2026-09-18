---
name: alterlab-preprint-deposition
description: "Drives preprint deposition across servers (arXiv, bioRxiv, medRxiv, SSRN, OSF Preprints): picks the right server by field, prepares submission metadata, sets the license (arXiv offers CC BY/BY-SA/BY-NC-SA/BY-NC-ND 4.0, the arXiv non-exclusive license, or CC0; bioRxiv/medRxiv offer CC BY/BY-NC/BY-ND/BY-NC-ND/CC0 or No-reuse), maps arXiv category taxonomy, handles immutable versioning and preprint DOIs, checks a journal's preprint/self-archiving policy via the Sherpa Romeo v2 API, and links the posted preprint to the published article. Reuses alterlab-arxiv and alterlab-biorxiv for metadata and alterlab-open-science for data-repository choice. Use when depositing a preprint, choosing a preprint server, preparing an arXiv or bioRxiv submission, setting a preprint license, or checking journal preprint policy; for Zenodo/Dryad/Figshare data deposition prefer alterlab-open-science, for TÜBİTAK Aperta prefer alterlab-aperta. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Write Edit Bash(python:*) WebFetch
compatibility: "No API key required for the deposition workflow itself. Optional Python helpers run via `uv run python` (stdlib-only, requests optional). The journal-policy check uses the Sherpa Romeo v2 API, which requires a free registered api-key; the bioRxiv/medRxiv preprint-to-publication check uses the keyless api.biorxiv.org content API."
metadata:
  skill-author: AlterLab
  version: "1.0.0"
  last_updated: "2026-06-06"
  depends_on: "alterlab-arxiv, alterlab-biorxiv (metadata/search), alterlab-open-science (data-repository & DMP choice)"
---

# Preprint Deposition — Pick a Server, Prepare the Submission, Link the Published Version

The **write/deposit** side of preprinting. Given a finished manuscript, this
skill turns "I want to post a preprint" into a concrete, server-specific plan:
**which** server fits the field, **what** metadata and category to enter,
**which license** to choose (and what it commits you to), **how** versioning and
the preprint DOI work, **whether** the target journal even allows a preprint,
and **how** to link the preprint to the article once it is published.

It is deliberately the deposit-side complement to the read-side connectors
`alterlab-arxiv` and `alterlab-biorxiv` (which *search and fetch* preprints) and
to `alterlab-open-science` (which chooses *data* repositories and writes DMPs).
This skill does **not** reimplement their search/metadata code — it calls them.

## Quick Start

```
I finished a CS paper — how do I post it to arXiv? Which category and license?
Should this biology manuscript go on bioRxiv or medRxiv?
Does Elsevier's journal X allow me to post a preprint before submission?
My preprint just got accepted — how do I link the published DOI to the arXiv version?
What license should I pick on arXiv if I might publish in a closed journal later?
```

→ Identify the field → route to a server (see the matrix) → assemble metadata →
choose a license → run the journal-policy check **before** posting → after
acceptance, link the published DOI back to the preprint.

---

## When to Use This Skill

Use this skill when the user wants to **act on** a preprint — post it, choose
where, prepare its metadata/license, or reconcile it with a journal or a
published version. Core jobs:

1. **Server selection** — match field + manuscript type to arXiv, bioRxiv,
   medRxiv, SSRN, or OSF Preprints. See `references/server_selection.md`.
2. **Submission metadata** — title, authors + ORCID, abstract, **arXiv primary
   + cross-list categories** or bioRxiv/medRxiv subject collection, funding,
   declarations. See `references/submission_metadata.md`.
3. **License choice** — pick from each server's actual license set and explain
   the downstream commitment (e.g. CC BY is irrevocable; a later journal may
   object to a permissive preprint license). See `references/licensing.md`.
4. **Versioning & DOI** — arXiv versions (v1, v2, …) are **immutable and
   permanent**; a withdrawal is a *new* version with a tombstone, never a
   deletion; bioRxiv/medRxiv assign a DOI on posting and accept revisions.
5. **Journal preprint policy** — query the **Sherpa Romeo v2 API** for the
   target journal's prearchiving (preprint) policy before posting. See
   `references/journal_policy.md`.
6. **Post-publication linking** — connect the preprint to the published article
   (publisher field on the server; the keyless `api.biorxiv.org` `/pubs/`
   endpoint surfaces bioRxiv→journal links).

### Does NOT Trigger — route adjacent requests to the right sibling

| The request is really about… | Route to | Why not here |
|------------------------------|----------|--------------|
| **Searching / fetching** existing arXiv preprints, resolving an arXiv ID | `alterlab-arxiv` | Read-side connector; this skill deposits, it does not search |
| **Searching / fetching** existing bioRxiv preprints for a lit review | `alterlab-biorxiv` | Read-side connector |
| Choosing a **data** repository (Zenodo, Dryad, Figshare), writing a grant **DMP**, preregistration, FAIR | `alterlab-open-science` | That is data/DMP/repository policy, not manuscript preprinting |
| Depositing to **TÜBİTAK Aperta**, the açık bilim mandate, a VYP | `alterlab-aperta` | National Turkish open-science track with its own embargo rules |
| Whether cited references actually **exist** / hallucinated DOIs | `alterlab-citation-verifier` | Existence-verification, not deposition |
| **Dead-link / 404** checks across a bibliography | `alterlab-link-health` | HTTP reachability, not preprint posting |
| Picking a **target journal** / formatting for journal submission | `alterlab-open-science` (OA route) then the journal's own guide | This skill only checks whether a journal *permits* a preprint |

This skill answers **"how and where do I deposit this manuscript as a preprint,
and is that compatible with my journal plans?"** It makes no claim about
manuscript quality, novelty, or whether the work should be published.

---

## Server Matrix (summary — full detail in `references/server_selection.md`)

| Server | Field fit | DOI on post | Default-ish license note | Moderation |
|--------|-----------|-------------|--------------------------|------------|
| **arXiv** | physics, math, CS, quant-bio (q-bio), q-fin, stat, EE/sys (eess), econ | No native DOI (arXiv ID is canonical; DataCite DOIs available) | arXiv non-exclusive license, or CC BY / BY-SA / BY-NC-SA / BY-NC-ND 4.0 / CC0 | Moderation + endorsement for new submitters |
| **bioRxiv** | life sciences / biology | Yes (CSHL-issued DOI) | CC BY / BY-NC / BY-ND / BY-NC-ND / CC0 / No-reuse | Basic screening |
| **medRxiv** | clinical / health sciences | Yes (CSHL-issued DOI) | Same license set as bioRxiv | Screening incl. ethics/▲non-trial checks |
| **SSRN** | social sciences, economics, law, humanities | DOI varies by network | Author selects; SSRN posting terms | Light screening |
| **OSF Preprints** | multi/cross-disciplinary + community servers | Yes (DOI via OSF) | CC0 / CC BY / CC BY-NC-ND / No license | Per-provider |

> Category/license rows above name the **real** option sets each server
> presents at submission. License *implications* (irrevocability, journal
> friction) are in `references/licensing.md`; never assert a "best" license
> without stating the trade-off.

---

## Workflow

### 1. Determine the field and route to a server

Read the manuscript's domain. STEM-formal (physics/math/CS/stat/eess/econ/q-bio/
q-fin) → **arXiv**. Biology → **bioRxiv**. Clinical/health → **medRxiv**.
Social science/law/economics → **SSRN** (or arXiv econ). Cross-disciplinary or a
field-specific community server → **OSF Preprints**. Edge cases and the full
decision tree live in `references/server_selection.md`.

### 2. Run the journal-policy check FIRST (if a target journal is known)

Before posting, confirm the intended journal permits preprints. Use
`scripts/journal_policy.py` to query the **Sherpa Romeo v2 API**
(`https://v2.sherpa.ac.uk/cgi/retrieve`, `item-type=publication`, requires a
free `api-key`). Report the journal's **prearchiving** (preprint) permission,
any conditions (embargo, version allowed, required statement), and link the
source. If no key is available, fall back to WebFetch on the publisher's policy
page and say so. Details: `references/journal_policy.md`.

> Most major publishers permit preprints, but conditions vary (some bar posting
> the *accepted* version, some require a DOI link or a specific notice). Never
> assert a policy from memory — verify it per journal.

### 3. Assemble submission metadata

Build the metadata block the server needs: title, all authors with ORCID and
affiliations, abstract, **arXiv primary category + optional cross-lists** (or
bioRxiv/medRxiv subject collection), declarations (competing interests, funding,
data/code availability, ethics/IRB for medRxiv), and the manuscript PDF. The
canonical field-by-field checklist is in `references/submission_metadata.md`.
To *look up* an existing arXiv/bioRxiv record's metadata for reuse, defer to
`alterlab-arxiv` / `alterlab-biorxiv` rather than re-querying here.

### 4. Choose the license deliberately

Present the actual license set for the chosen server (see the matrix), then
explain the commitment:

- **CC BY 4.0** — maximum reuse; **irrevocable**; some closed-access journals
  dislike a permissive preprint and may ask you to change it (you cannot revoke
  CC BY on already-posted versions).
- **arXiv non-exclusive license 1.0** — arXiv-specific; you keep copyright,
  grant arXiv a distribution license; the least journal-friction option on arXiv.
- **CC BY-NC-*/-ND** — narrower reuse; check it against any funder open-access
  mandate (e.g. cOAlition S Plan S generally requires CC BY).
- **CC0** — public-domain dedication; broadest, also irrevocable.

Confirm whether a funder mandate forces a specific license before recommending.
Full table + funder-mandate notes: `references/licensing.md`.

### 5. Post, then manage versions

After posting: record the **arXiv ID / preprint DOI** and the **version**.
Revisions are *replacements* (arXiv) or new versions (bioRxiv/medRxiv) — the old
version stays public and immutable. Do **not** advise "deleting" an announced
arXiv paper; that is impossible — only a withdrawal-version with a tombstone.

### 6. Link the published article after acceptance

When the paper is published, link the DOI back to the preprint (the server's
"published in" / publisher field; bioRxiv/medRxiv auto-detect many links and
expose them via `api.biorxiv.org` `/pubs/{server}/...`). This makes the version
of record discoverable from the preprint and vice versa.

---

## Scripts

- `scripts/journal_policy.py` — query the Sherpa Romeo v2 API for a journal's
  preprint/self-archiving policy by ISSN or title (needs a free `--api-key`;
  prints a structured summary; degrades to a manual-check instruction offline).
- `scripts/server_recommender.py` — given a few flags (field, has-clinical-data,
  target-journal-known, needs-DOI), prints a recommended server + license
  shortlist with the trade-offs, from the rules in `references/server_selection.md`.
- `scripts/preprint_link_check.py` — query the keyless `api.biorxiv.org`
  `/details/` and `/pubs/` endpoints to confirm a bioRxiv/medRxiv DOI exists and
  surface any detected preprint→published-article link.

All scripts are stdlib-first (use `requests` if present, else `urllib`), run in a
bare `uv run python`, and never require a key except the Sherpa Romeo lookup.

---

## Self-Check Before Reporting

- Did I **verify** the journal's preprint policy (Sherpa Romeo or the live
  publisher page), or did I assert it from memory? Only the former is allowed.
- Did I name the server's **real** license options and state the irrevocability
  / journal-friction trade-off, not a bare "use CC BY"?
- Did I route a *search/fetch* request to `alterlab-arxiv`/`alterlab-biorxiv`,
  and a *data-repository/DMP* request to `alterlab-open-science`, and a TÜBİTAK
  request to `alterlab-aperta`, instead of handling it here?
- Did I avoid telling the user to "delete" an already-announced arXiv preprint?

---

## References

- `references/server_selection.md` — full server decision tree, field-by-field.
- `references/submission_metadata.md` — per-server metadata field checklist.
- `references/licensing.md` — license option sets, irrevocability, funder mandates.
- `references/journal_policy.md` — Sherpa Romeo v2 API usage and policy reading.

Part of the AlterLab Academic Skills suite.
