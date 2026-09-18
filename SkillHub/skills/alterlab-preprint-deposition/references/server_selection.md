# Preprint Server Selection

Routing a finished manuscript to the right preprint server. Pick by **field
fit** first, then by secondary factors (DOI need, moderation tolerance, journal
plans, funder mandate).

## Contents

- [Decision tree](#decision-tree)
- [Per-server profiles](#per-server-profiles)
- [Secondary factors](#secondary-factors)
- [Common edge cases](#common-edge-cases)

## Decision tree

1. **Is the work clinical / health-related (human subjects, trials, public
   health)?** → **medRxiv**. (medRxiv screens for trial registration and
   ethics; do not post identifiable patient data.)
2. **Is it life sciences / biology (non-clinical)?** → **bioRxiv**.
3. **Is it physics, mathematics, computer science, statistics, electrical
   engineering & systems, economics, quantitative biology, or quantitative
   finance?** → **arXiv** (these map to arXiv's top-level archives:
   physics/math/cs/stat/eess/econ/q-bio/q-fin).
4. **Is it social science, law, business, or humanities?** → **SSRN** (or arXiv
   `econ` for economics that fits arXiv's scope).
5. **Cross-disciplinary, or a field with a dedicated community server (e.g.
   PsyArXiv, SocArXiv, EarthArXiv on OSF)?** → **OSF Preprints**.

When two servers both fit (e.g. computational biology → arXiv `q-bio` *or*
bioRxiv), prefer the one your **target community reads** and whose **DOI
behaviour** you need (see below). Posting the same manuscript to two preprint
servers is discouraged and can create duplicate-DOI confusion.

## Per-server profiles

### arXiv
- **Scope:** physics, math, CS, stat, eess, econ, q-bio, q-fin.
- **Identifier:** the **arXiv ID** is canonical (e.g. `2406.01234`). arXiv does
  not mint a DOI by default, though DataCite DOIs are available.
- **Versioning:** versions `v1, v2, …` are **permanent and immutable**. An
  announced paper **cannot be deleted**; a withdrawal creates a new version
  marked withdrawn (tombstone, no downloadable files). Revisions are submitted
  as **replacements**, not by editing in place.
- **Gatekeeping:** moderation by subject; first-time submitters in some archives
  need **endorsement**.
- **Licenses:** see `licensing.md`.

### bioRxiv
- **Scope:** life sciences / biology (Cold Spring Harbor Laboratory).
- **Identifier:** assigns a **DOI on posting** (CSHL prefix).
- **Versioning:** authors may post **revised versions**; prior versions remain
  available.
- **Linking:** detected preprint→journal links are exposed via the keyless
  `api.biorxiv.org` `/pubs/biorxiv/...` endpoint.

### medRxiv
- **Scope:** clinical and health sciences (CSHL + BMJ + Yale).
- **Identifier:** assigns a **DOI on posting**.
- **Extra screening:** trial registration, ethics, and a check that the work is
  not a case report with identifiable individuals. Same license set as bioRxiv.

### SSRN
- **Scope:** social sciences, economics, law, business, humanities (Elsevier).
- **Identifier:** DOI behaviour varies by network/series.
- **Note:** widely used in economics/law/management; abstract-first culture.

### OSF Preprints
- **Scope:** multi-disciplinary, plus community-run servers (PsyArXiv, SocArXiv,
  EarthArXiv, etc.) hosted on OSF infrastructure.
- **Identifier:** DOI via OSF.
- **Licenses:** No license / CC0 / CC BY / CC BY-NC-ND depending on provider.

## Secondary factors

| Factor | Favours |
|--------|---------|
| Need a citable **DOI immediately** | bioRxiv, medRxiv, OSF, SSRN (arXiv ID works as a citation but is not a DOI by default) |
| Strict **funder OA mandate** (CC BY required) | any server that offers **CC BY 4.0** |
| Submitting to a **closed/selective journal** later | check the journal's preprint policy first (`journal_policy.md`); pick the least-friction license |
| **Clinical** content | medRxiv only |
| First arXiv submission, no endorser | factor in endorsement delay; OSF/bioRxiv have no endorsement step |

## Common edge cases

- **Computational biology / bioinformatics:** arXiv `q-bio` and bioRxiv both
  accept it — choose by audience and DOI need.
- **Economics:** arXiv `econ`, SSRN, or RePEc-indexed venues; SSRN is the
  dominant social-science preprint culture.
- **Already submitted to a journal:** posting a preprint is usually still
  allowed (many journals permit the *submitted* version) but **verify the
  journal policy** before posting the *accepted* manuscript — see
  `journal_policy.md`.
- **Data / code, not a manuscript:** that is a **data repository** decision →
  defer to `alterlab-open-science` (Zenodo/Dryad/Figshare) or, for TÜBİTAK
  funding, `alterlab-aperta`.
