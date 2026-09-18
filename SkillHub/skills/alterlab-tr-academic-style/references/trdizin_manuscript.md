# TR Dizin manuscript-formatting criteria

TR Dizin is **TÜBİTAK ULAKBİM's national citation index** (*Türkiye'nin ulusal
atıf dizini*). It is a curated index with editorial/ethical criteria — **not** a
hosting platform. This file covers only the *manuscript-formatting* rules a
Turkish-journal author applies while preparing a submission. To check whether a
specific journal is **currently indexed**, use the `alterlab-trdizin` skill,
which queries the live index — never assert index membership from memory.

> **Maintenance note.** ULAKBİM revises the TR Dizin criteria periodically.
> Re-verify against the official criteria page before relying on any rule below
> for a real submission. Source of record: https://trdizin.gov.tr/?p=456

## DergiPark vs TR Dizin (do not conflate)

- **DergiPark** (`dergipark.org.tr`) = ULAKBİM's national journal *hosting*
  platform. Hosting carries **no quality/index gate**.
- **TR Dizin** (`trdizin.gov.tr`) = a separate national *citation index* with an
  application and editorial criteria.
- A journal hosted on DergiPark is **not** therefore in TR Dizin. Presence on
  one does not imply the other.

For harvesting articles/metadata from a DergiPark journal, route to
`alterlab-dergipark`. For live TR Dizin index status, route to
`alterlab-trdizin`.

## What TR Dizin actually mandates vs. journal house conventions

Two distinct layers get conflated constantly. Keep them apart:

- **TR Dizin index criteria** — the rules in the official *Dergi Değerlendirme
  Kriterleri*. These are deliberately loose on manuscript mechanics: TR Dizin
  sets *whether* a rule must exist, not its exact number.
- **Journal house conventions** — the specific numbers (e.g. "öz 200-250 words,
  3-5 keywords") that most Turkish journals publish in their *yazım kuralları*.
  These are widespread but are the **journal's** rules, not TR Dizin's. Always
  read the target journal's own *yazım kuralları* for the binding figures.

### Abstract / öz — what TR Dizin requires

- TR Dizin requires only that **the journal set a word limit for the abstract
  and enforce it** — it specifies **no** number. Verbatim from the criteria:
  *"A word limit should be given for the abstract and this rule should be
  followed."*
- A **second-language** title/abstract/keywords is **suggested, not mandated**:
  *"It is suggested that the title, abstract and keywords be published in the
  journal in a language other than the article language."* So a Turkish article
  with only a Turkish öz can still satisfy TR Dizin, though most journals
  (and reviewers) expect an English abstract too.
- **House convention (very common, NOT a TR Dizin rule):** a Turkish **öz** and
  an English **abstract**, each **~200-250 words**. Treat this as the default to
  propose, but confirm it against the journal's *yazım kuralları*.

### Keywords — anahtar kelimeler

- TR Dizin requires that articles **contain keywords**; it specifies **no
  count**.
- **House convention (NOT a TR Dizin rule):** **3-5 keywords** per language.
  Use as a default, confirm against the journal guide.

### Latin alphabet — what TR Dizin requires

- TR Dizin mandates Latin script specifically for **non-Latin-alphabet
  articles**: *"Articles written in languages other than Latin alphabets should
  include the title, abstract, keywords and references written in Latin
  alphabets."* It also requires the **reference list** be in the Latin alphabet.
- For Turkish (already a Latin alphabet) this is automatically satisfied — the
  practical point is to use proper Turkish Latin letters with diacritics
  (İ/ı, Ş/ş, Ğ/ğ, Ç/ç, Ö/ö, Ü/ü), **not** ASCII substitutions, so the metadata
  block harvests cleanly.

### Structured abstract (journal-dependent)

- Some fields/journals — notably **health sciences** — require a **structured
  abstract** with labelled segments, typically: **Amaç** (Purpose/Aim),
  **Yöntem** (Method), **Bulgular** (Results), **Sonuç** (Conclusion). This is a
  journal/field convention; apply the labels the target journal specifies.

### External peer review — what TR Dizin requires

- TR Dizin requires **at least two referees per article, appointed from
  different institutions** (*farklı kurumlardan hakem*). Verbatim: *"The number
  of peer-reviewers must be at least two for each article, taking care to be
  from different institutions."* Prepare the manuscript to arrive review-ready
  (anonymized where double-blind, complete metadata block, references in Türkçe
  APA 7 or the journal's mandated style).

## Citation style inside the manuscript

TR Dizin does not impose a single citation style across all journals — the
**journal's own guideline** governs. For Turkish-language journals that follow
APA, format citations in **Türkçe APA 7** (see `turkce_apa7.md`). Confirm the
target journal's required style before converting.

## Sources

- TR Dizin journal evaluation criteria — official landing page:
  https://trdizin.gov.tr/?p=456 (re-verify; ULAKBİM updates periodically).
- TR Dizin application requirements & journal evaluation criteria (English) —
  the page carrying the verbatim word-limit / suggested-second-language /
  two-referees-from-different-institutions / Latin-alphabet wording quoted
  above: https://trdizin.gov.tr/en/tr-index-application-requirements-and-journal-evaluation-criteria-2/
- DergiPark hosting platform: https://dergipark.org.tr (distinct from TR Dizin).
