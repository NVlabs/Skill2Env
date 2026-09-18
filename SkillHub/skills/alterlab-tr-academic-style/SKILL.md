---
name: alterlab-tr-academic-style
description: "Formats manuscripts for Turkish journals: TR Dizin submission rules (TR Dizin mandates a set abstract word limit, two referees from different institutions, Latin script for non-Latin-alphabet articles, and only suggests a second-language abstract; bilingual oz/abstract ~200-250 words and 3-5 keywords are common journal house conventions to confirm against the journal's yazim kurallari) and the Turkish adaptation of APA-7 (ve ark./vd. for multi-author cites, ampersand only in the reference list, s. for page, Cev. for translator, t.y. for no date, aktaran for as-cited-in, Turkish capitalization). Use when writing for a Turkish/Turkce journal, preparing a TR Dizin submission, needing Turkce APA 7 in-text or reference formatting, or formatting a bilingual oz. For English-language citation styles prefer alterlab-citation-mgmt or alterlab-venue-templates; for live TR Dizin index status use alterlab-trdizin. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Write Edit Bash(python:*)
compatibility: No API key or network required — applies the official TR Dizin evaluation criteria (and flags journal house conventions separately) plus the Turkish APA-7 adaptation offline; the linter in scripts/ runs on stdlib only
metadata:
  skill-author: AlterLab
  version: "1.0.0"
  last_updated: "2026-06-06"
  depends_on: "alterlab-trdizin (live index-status check), alterlab-citation-mgmt + alterlab-venue-templates (English citation styles)"
---

# Turkish APA-7 and TR Dizin Style

Applies Turkish academic-writing conventions to a manuscript: the **TR Dizin**
(TUBITAK ULAKBIM's national citation index — *Türkiye'nin ulusal atıf dizini*)
manuscript-formatting rules, and the **Türkçe APA 7** (the Turkish-language
adaptation of APA 7th edition) for in-text citations and the reference list.
This is the *style/formatting* skill for the Turkish track — it does not check
whether a journal is actually indexed (that is `alterlab-trdizin`), and it is
distinct from the English citation skills.

It exists because the suite's other writing skills (`alterlab-citation-mgmt`,
`alterlab-venue-templates`, `alterlab-paper-writer`) target English-language
APA/IEEE/Vancouver output. Turkish journals impose their own bilingual
**öz** (*abstract*) requirements and a citation dialect with Turkish
abbreviations (*ve ark.*, *vd.*, *s.*, *Çev.*, *t.y.*, *aktaran*) that those
skills do not produce.

## When to Use This Skill

Use this skill when the request is about **writing/formatting** a Turkish
manuscript or its citations:

- "Bu makaleyi TR Dizin formatına göre düzenle" — format a manuscript to TR Dizin rules.
- "Türkçe APA 7'ye göre kaynakça/atıf düzelt" — fix references / in-text cites to Turkish APA 7.
- Writing a bilingual **öz** + abstract pair (Turkish öz and Latin-script English abstract).
- Deciding whether to write *ve ark.* or *vd.*, where the *&* ampersand is allowed, how to write *s.*/*ss.*, *Çev.*, *t.y.*, or *aktaran*.
- Checking a Turkish journal manuscript against TR Dizin's structural requirements before submission.

### Does NOT Trigger

Route adjacent requests to the correct sibling skill:

| The user wants… | Route to |
|-----------------|----------|
| English-language APA/Vancouver/IEEE citations or a reference manager workflow | `alterlab-citation-mgmt` |
| A journal- or publisher-specific submission template (English venues) | `alterlab-venue-templates` |
| Whether a journal is **currently indexed** in TR Dizin (live status) | `alterlab-trdizin` |
| Find/harvest articles or metadata from a DergiPark-hosted journal | `alterlab-dergipark` |
| Search/cite a Turkish graduate thesis (YÖK Ulusal Tez Merkezi) | `alterlab-yok-tez` |
| Write or scaffold the whole paper (IMRaD, structure, drafting) | `alterlab-paper-writer` |
| Compute docentlik (*associate-professorship*) or akademik teşvik (*academic-incentive*) points | `alterlab-docentlik-eligibility` / `alterlab-akademik-tesvik` |
| Turkish etik kurul (*ethics-committee*) application or KVKK data plan | `alterlab-tr-research-ethics` / `alterlab-kvkk-dmp` |
| Verify that cited references actually exist (hallucination check) | `alterlab-citation-verifier` |

This skill owns **how Turkish text and citations are formatted**, not whether
the underlying journal/index/claim is real.

## TR Dizin manuscript requirements

TR Dizin is a **citation index with editorial criteria**, separate from
DergiPark hosting — hosting on DergiPark does not imply TR Dizin indexing.
**Distinguish two layers** and never present house conventions as index rules:

**What TR Dizin itself mandates** (from its official evaluation criteria):

- **A word limit for the abstract** must be set and enforced — TR Dizin
  specifies **no** number, and gives **no** keyword count.
- **Second-language metadata is *suggested*, not required.** TR Dizin only
  *suggests* a title/abstract/keywords in a language other than the article's.
  It *mandates* Latin script only for **non-Latin-alphabet articles** (their
  title/abstract/keywords/references), and requires the reference list in Latin
  script.
- **At least two referees per article, from different institutions**
  (*farklı kurumlardan hakem*); a manuscript should arrive review-ready.

**Common Turkish-journal house conventions** (widespread, but the *journal's*
rules — confirm against its *yazım kuralları*, do not attribute to TR Dizin):

- **Bilingual abstract:** a Turkish **öz** + an English **abstract**, each
  **~200-250 words** — a frequent default, not a TR Dizin figure.
- **Keywords:** **3-5** (*anahtar kelimeler*) per language — a frequent default.
- **Structured abstract** where the field requires it (e.g. health sciences):
  purpose, method, results, conclusion as labelled segments.
- **Latin Turkish letters with diacritics** in the metadata block (İ/ı, Ş/ş,
  Ğ/ğ, Ç/ç, Ö/ö, Ü/ü), not ASCII — so the record harvests cleanly.

Full criteria detail, the verbatim TR Dizin wording, and source links live in
`references/trdizin_manuscript.md`. For **live index status** ("is journal X
in TR Dizin right now?") do not guess — defer to `alterlab-trdizin`.

> Verify current TR Dizin criteria against the official page before a real
> submission — ULAKBIM revises them periodically. Source of record:
> https://trdizin.gov.tr/?p=456

## Türkçe APA 7 — the deltas from English APA 7

Turkish APA 7 keeps APA's structure but swaps the connective words and
abbreviations into Turkish. The high-frequency deltas:

| Situation | English APA 7 | Türkçe APA 7 |
|-----------|---------------|--------------|
| 3+ authors, in-text | Smith et al. | Yılmaz ve ark. **or** Yılmaz vd. |
| Two authors joined, **in-text (narrative)** | Smith and Jones | Yılmaz ve Demir |
| Two authors joined, **reference list / parenthetical** | Smith & Jones | Yılmaz & Demir (`&` only here) |
| Page / pages | p. / pp. | s. / ss. |
| No date | n.d. | t.y. (*tarih yok*) |
| Translator | Trans. | Çev. (*çeviren*) |
| Editor(s) | Ed./Eds. | Ed./Haz. (*hazırlayan*) |
| Secondary / as-cited-in | as cited in | aktaran |
| Retrieved from | Retrieved from | Erişim adresi |

Key rules:

1. **Ampersand `&` belongs only in the reference list and in *parenthetical*
   in-text citations.** In running Turkish prose use the word **ve**.
2. **`ve ark.` vs `vd.`** — both render "et al." Pick one and apply it
   consistently across the whole manuscript (a journal may mandate one).
3. **`aktaran`** marks a secondary citation (you read source B citing source
   A): `(Yılmaz, 2018, aktaran Demir, 2021)`.
4. **Turkish capitalization & diacritics** are preserved in titles and author
   names — never strip İ/ı, Ş/ş, Ğ/ğ, Ç/ç, Ö/ö, Ü/ü. Sentence-case article
   titles as in APA, using Turkish casing rules.

Worked in-text and reference-list examples (book, chapter, journal article,
thesis, translated work, secondary citation) are in
`references/turkce_apa7.md`.

## Workflow

1. **Identify the target.** Confirm the journal is Turkish/Türkçe and whether
   it follows TR Dizin rules and/or Türkçe APA 7. If the user actually needs an
   English venue template, stop and route to `alterlab-venue-templates`.
2. **Structure the metadata block.** Draft or check the öz/abstract and keywords.
   Propose the common house defaults (bilingual öz + abstract ~200-250 words
   each, 3-5 keywords each) but tell the user these are the *journal's*
   convention — TR Dizin itself only requires a word limit be set — so they must
   confirm the figures against the journal's *yazım kuralları*. Keep the
   metadata in proper Latin Turkish letters with diacritics. See the TR Dizin
   section.
3. **Convert citations.** Rewrite in-text citations and the reference list into
   Türkçe APA 7 using the delta table; preserve all diacritics.
4. **Lint.** Run the citation linter to catch the common mechanical errors
   (English abbreviations left in, `&` used in narrative prose, mixed
   `ve ark.`/`vd.`):

   ```bash
   uv run python skills/turkish-academia/alterlab-tr-academic-style/scripts/tr_apa_lint.py manuscript.md
   ```

   It reads a `.md`/`.txt`/`.tex` file (or stdin), reports line-numbered
   findings as text or `--json`, and is stdlib-only (no network, no deps).
5. **Report.** Present the corrected text plus the lint findings. Flag any
   point where a journal's own guide may override the default (e.g. it
   mandates `vd.` not `ve ark.`), and remind the user to confirm live TR Dizin
   status via `alterlab-trdizin` before submitting.

## Self-Check Before Reporting

- Did you present 200-250 words / 3-5 keywords / mandatory-bilingual as the journal's house convention (to confirm against its *yazım kuralları*), not as a TR Dizin index rule?
- Did you scope TR Dizin's own requirements correctly (word limit set; 2 referees from different institutions; second-language abstract *suggested*; Latin script mandated for non-Latin-alphabet articles)?
- Is `&` confined to the reference list and parenthetical cites (never narrative prose)?
- Is `ve ark.`/`vd.` consistent throughout?
- Are all Turkish diacritics intact in names and titles?
- Did you avoid asserting a journal's TR Dizin index status from memory? (That is `alterlab-trdizin`'s job.)

## References

- `references/trdizin_manuscript.md` — TR Dizin manuscript-formatting criteria, the DergiPark-vs-TR-Dizin distinction, and source links.
- `references/turkce_apa7.md` — full Türkçe APA 7 delta tables with worked in-text and reference-list examples.

Part of the AlterLab Academic Skills suite.
