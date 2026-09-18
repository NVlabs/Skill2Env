# Checking a Journal's Preprint Policy (Sherpa Romeo v2 API)

Before posting a preprint — especially the *accepted* version — confirm the
intended journal **permits** preprints and on what conditions. The authoritative
machine-readable source is **Sherpa Romeo**, which aggregates publisher open-
access / self-archiving policies journal-by-journal.

## Contents

- [The API](#the-api)
- [Reading a prearchiving policy](#reading-a-prearchiving-policy)
- [Offline / no-key fallback](#offline--no-key-fallback)
- [What to report](#what-to-report)

## The API

- **Base endpoint:** `https://v2.sherpa.ac.uk/cgi/retrieve`
- **Requires a free, registered `api-key`** (request one from the Sherpa
  services site). The key is the only credential the deposition workflow needs.
- **Key parameters** (verified on `v2.sherpa.ac.uk/api`):
  - `item-type=publication` — query a journal/publication's policy.
  - `api-key=<YOUR-KEY>`
  - `format=Json` (or `Ids`).
  - `filter=` — a JSON array of `[fieldname, operator, value]` triples, e.g.
    filter by ISSN or title.
  - `limit` / `offset` — paging.

Example shape (do not run with a placeholder key):

```
https://v2.sherpa.ac.uk/cgi/retrieve?item-type=publication&api-key=<KEY>&format=Json&filter=[["issn","equals","1234-5678"]]
```

`scripts/journal_policy.py` wraps this: pass `--issn` or `--title` plus
`--api-key`, and it prints the journal's prearchiving permission and conditions.

## Reading a prearchiving policy

Sherpa Romeo distinguishes archiving by **version**:

- **submitted / prearchiving (the preprint)** — the manuscript *before* peer
  review. This is the version a preprint server hosts; check it is **can**
  (permitted).
- **accepted (AAM / postprint)** — after peer review, before typesetting.
- **published (version of record)** — the publisher PDF; rarely allowed on a
  preprint server.

Conditions to surface: required **embargo**, the **location** allowed (any
repository vs. specified), a **required statement/notice**, and whether a **link
to the published DOI** must be added.

## Offline / no-key fallback

If no API key is available or the network is down:

1. WebFetch the **publisher's own** preprint/sharing policy page and quote it.
2. State explicitly that the policy was read live (not from memory) and link the
   source.
3. If neither is reachable, instruct the user to check Sherpa Romeo manually and
   do **not** assert a policy.

## What to report

- The journal name + ISSN matched.
- The **preprint (prearchiving) permission**: permitted / restricted / not
  addressed.
- Any **conditions** (embargo, version, required notice, DOI link).
- The **source** (Sherpa Romeo record URL or the publisher policy URL).
- A recommendation: post now / post submitted version only / wait until after
  acceptance / pick a lower-friction license (cross-ref `licensing.md`).
