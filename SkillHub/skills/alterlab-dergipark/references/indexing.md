# DergiPark vs TR Dizin — Hosting Is Not Indexing

The single most common error when reasoning about a Turkish journal is conflating
**DergiPark** (where the journal is *hosted*) with **TR Dizin** (whether it is
*indexed* in the national citation index). They are different systems with
different gatekeeping. Encode this distinction in every answer about a journal's
quality or status.

## The two systems

| | DergiPark | TR Dizin |
|--|-----------|----------|
| Operator | TÜBİTAK ULAKBİM | TÜBİTAK ULAKBİM |
| Role | Journal **hosting** platform (OJS-based) | National **citation index** |
| URL | `https://dergipark.org.tr` | `https://trdizin.gov.tr` / search at `https://search.trdizin.gov.tr` |
| Entry bar | Open hosting; **no quality gate** | **Separate application** + evaluation each period |
| Scale (2024, as reported in prior research) | ~2,537 journals, 728k+ articles | ~1,741 journals |
| Implication | Being on DergiPark says **nothing** about quality or indexing | Indexing gates career mechanics (see below) |

**Hosting on DergiPark does NOT imply TR Dizin indexing.** A journal can be on
DergiPark and never have applied to, or have been rejected by, TR Dizin.

## Why TR Dizin status matters for Turkish academics

TR Dizin indexing is the de-facto national quality bar and feeds career mechanics:
- it gates **doçentlik** (associate-professorship) eligibility point thresholds;
- it feeds publication-incentive scoring (akademik teşvik / UBYT-type payouts);
- it is the bar reviewers and committees look for first.

So before recommending a target journal, verify its **live** TR Dizin status —
do not trust the journal's own `/indexes` page.

## The /indexes caveat

`/{lang}/pub/{slug}/indexes` lists indexing databases **as declared by the
journal**. DergiPark does not verify these claims. `scripts/journal_info.py`
retrieves the page but stamps a `DISCLAIMER` on it and points to authoritative
cross-checks.

## Authoritative cross-checks (do this instead of trusting /indexes)

- **TR Dizin (national index):** search `https://search.trdizin.gov.tr` by journal
  title or ISSN. For a programmatic, fielded status verdict (active / rejected
  years / first-index date), route to the sibling skill **alterlab-trdizin**, which
  wraps the TR Dizin search API.
- **DOAJ (open-access status):** `https://doaj.org/api/v4/search/journals/{query}`.
  (Prior research notes a DOAJ logo auto-appears on DergiPark for DOAJ-listed
  journals as of an April-2026 integration — UNVERIFIED here; confirm via DOAJ.)

## In-page TR Dizin signal (advisory only)

Prior art reports a `stats_trdizin_citation_count` meta tag on TR Dizin-covered
articles. It was **not present** on the articles probed for this skill, so treat it
as a *possible* positive signal only — never as proof. The authoritative answer is
TR Dizin's own record, not a page meta tag.

## Routing rule

| Question | Where it goes |
|----------|---------------|
| "Harvest / fetch / list / BibTeX from a DergiPark journal" | **this skill** |
| "Is journal X *indexed in TR Dizin* / what's its TR Dizin status" | **alterlab-trdizin** (authoritative status); this skill only fetches the self-declared `/indexes` page and points you there |
