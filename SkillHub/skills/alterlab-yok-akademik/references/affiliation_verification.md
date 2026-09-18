# Affiliation verification — why YÖKSİS, and how to disambiguate

## Why YOK Akademik is the authoritative TR affiliation source

YOK Akademik is backed by **YÖKSİS** (the national Higher-Education Information
System). When a Turkish academic moves, changes title, or is appointed, the official
record flows through YÖKSİS — so the portal reflects the **current, official** kurum
(institution), fakülte/bölüm, and unvan (title).

For Turkish institutions this is **more reliable than ORCID or OpenAlex affiliation
strings**, which:

- lag (authors update ORCID rarely; OpenAlex infers affiliation from paper metadata
  that can be months/years stale),
- fragment one institution into many spellings (Turkish/English names, abbreviations,
  diacritic variants), and
- often show a *past* affiliation from an old paper rather than the person's current post.

So: for **"where does this person officially work right now?"** → YOK Akademik. For
**"what has this person published, with which DOIs and co-authors?"** →
`alterlab-openalex` (richer, deduped publication metadata). The two are complementary;
use YOK Akademik for the affiliation ground truth and OpenAlex for the bibliography.

## When you actually need this

- **Authorship bylines** — confirming the affiliation line for a Turkish co-author
  before submission.
- **Recommendation letters** — verifying the candidate's (or referee's) current title
  and institution. (This skill only supplies the verified affiliation that goes into the
  letter; it does not draft the letter itself.)
- **Grant teams / editorial boards** — confirming a named person's post and unvan.

## Disambiguation checklist (do this every time)

1. **Search** the normalized name (see `turkish_names.md`).
2. If **>1 candidate**, present a table — *name · unvan · university · faculty/dept* —
   and ask which one, or confirm the institution the user expected.
3. **Watch for common-name collisions**: Yılmaz, Demir, Kaya, Şahin, Çelik return
   many people. A bare name match is *not* a confirmation.
4. **Cross-check the unvan against the claim**: if the user calls someone "Professor"
   but YÖKSİS shows *Dr. Öğr. Üyesi*, surface the discrepancy rather than smoothing it.
5. **Report with provenance**: "Per YOK Akademik (YÖKSİS), as of <date>: <Unvan>,
   <Bölüm>, <Fakülte>, <Üniversite>." People move — the date matters.
6. **If the portal failed** (302/500, markup change, no match), say so and fall back to
   WebFetch on the search page. **Never** fabricate an affiliation, title, or authorId.

## What this skill does NOT decide

It does not judge research quality, compute **doçentlik** points
(`alterlab-docentlik-eligibility`) or **akademik teşvik** scores
(`alterlab-akademik-tesvik`), and it does not fetch thesis full text
(`alterlab-yok-tez`). It establishes *identity and current affiliation*, full stop.
