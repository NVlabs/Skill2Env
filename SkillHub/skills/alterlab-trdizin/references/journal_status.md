# Determining a journal's TR Dizin indexing status

The whole point of a status check is: **is this journal *currently* in TR Dizin?**
DergiPark hosting, a Crossref DOI, or an `/indexes` self-declaration do **not**
answer that — only the TR Dizin record does.

## The decision (from a journal `_source` record)

`scripts/query_trdizin.py journal "<title or ISSN>"` fetches the record and
applies this logic (`journal_status()`):

1. **Collect coverage years** = the set of `journalYear[].year` values. These are
   the years TR Dizin actually indexed the journal.
2. **`isActive`** (bool) — a record flag. **Do not trust it alone** (see below).
3. **`rejectYearList`** — a list of `{id, year}` for years the journal was
   **rejected**; `null` if it was never rejected. Reduce it to the set of years.
4. **Compare reject years to coverage.** Let `latest_coverage` = max coverage year
   and `latest_reject` = max rejected year.
5. **Verdict (evaluated in this order):**
   - `latest_reject` is newer than `latest_coverage` (or there is no coverage)
     → *No longer indexed — rejected after coverage* (list coverage end + reject
     years). **This wins even when `isActive == true`** — a de-indexed venue.
   - else `isActive == true` **and** coverage years exist
     → *Currently indexed (active; coverage years FIRST–LAST)*.
   - else `rejectYearList` is non-empty
     → *Rejected / not indexed* (list the rejected years).
   - else `isActive == false`
     → *Not currently active in TR Dizin*.
   - otherwise → *indeterminate; inspect raw fields*.

> **Why the reject-vs-coverage check comes first.** `isActive=true` does **not**
> mean "indexed now". Verified live: *Eğitim Bilim Toplum* (ISSN 1303-9202) carries
> `isActive=true` with coverage ending **2019** and `rejectYearList` = 2020, 2021,
> 2022, 2023, 2025. Trusting `isActive` would tell a doçentlik applicant the
> journal is "currently indexed" — a dangerous false positive. The reject years
> being newer than the last covered year is the decisive signal that it was
> de-indexed.

### Worked examples (verified live, 2026-06-06)

| Journal | `isActive` | Signal | Verdict |
|---------|-----------|--------|---------|
| *Bilig / Türk Dünyası Sosyal Bilimler Dergisi* (ISSN 1301-0549) | `true` | coverage years 2004–2026, no reject after coverage | Currently indexed (active) |
| *Eğitim Bilim Toplum* (ISSN 1303-9202) | `true` | coverage ends 2019; `rejectYearList` = 2020, 2021, 2022, 2023, 2025 | **No longer indexed — rejected after coverage** (isActive ignored) |
| *Toplum ve Bilim* (ISSN 1300-9354) | `false` | coverage ends 2015; `rejectYearList` = 2008, 2016, 2017, 2018, 2019 | No longer indexed — rejected after coverage |

## Why `firstIndexDate` / `indexDate` are excluded

On the public search endpoint these two fields are stamped with the **query time**
(they come back as "now"), so they carry no index-history information. Relying on
them would produce a fabricated "first indexed today" claim. The verdict uses
`journalYear` / `isActive` / `rejectYearList` only.

## Why this matters for Turkish academics

TR Dizin status is a real career gate, not a nicety:

- It is an input to **doçentlik** (associate-professorship) eligibility point
  thresholds — for *which field's* table and minima, route to
  `alterlab-docentlik-eligibility`.
- It feeds the **akademik teşvik** (academic-incentive) and **UBYT** publication
  payouts — for the actual score arithmetic, route to `alterlab-akademik-tesvik`.
- It is the de-facto national quality bar, so authors should **verify a target
  journal's live status *before* submitting**.

This skill answers only *"is it indexed right now?"* It does **not** compute
eligibility points or incentive scores — those live in the sibling skills above.

## Acceptance criteria (for context, not computed here)

The editorial criteria a journal must meet to be accepted/retained are published
at <https://trdizin.gov.tr/kriterler/>. This skill reports a journal's *current
status*; it does not adjudicate whether a journal *should* be accepted.
