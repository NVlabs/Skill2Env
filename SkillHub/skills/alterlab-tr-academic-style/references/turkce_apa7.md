# Türkçe APA 7 — Turkish adaptation of APA 7th edition

This is the **Turkish-language adaptation of APA 7**: the same structure as
English APA 7, but with the connective words and abbreviations rendered in
Turkish. Use it for Turkish-language manuscripts whose journal mandates APA. For
**English-language** APA/IEEE/Vancouver output, use `alterlab-citation-mgmt` or
`alterlab-venue-templates` instead.

> Some Turkish institutions publish their own APA 7 guide (e.g. Ege
> Üniversitesi). When a journal names a specific institutional guide, follow it;
> the rules below are the common core.

## The deltas at a glance

| Situation | English APA 7 | Türkçe APA 7 |
|-----------|---------------|--------------|
| 3+ authors, in-text | Smith et al. | Yılmaz ve ark. **or** Yılmaz vd. |
| Two authors, narrative in-text | Smith and Jones | Yılmaz ve Demir |
| Two authors, parenthetical / reference list | Smith & Jones | Yılmaz & Demir |
| Page / pages | p. / pp. | s. / ss. |
| No date | n.d. | t.y. *(tarih yok)* |
| Translator | Trans. | Çev. *(çeviren)* |
| Editor(s) / compiler | Ed. / Eds. | Ed. / Haz. *(hazırlayan)* |
| As cited in (secondary) | as cited in | aktaran |
| Retrieved from | Retrieved from | Erişim adresi |
| Volume / issue | Vol. / No. | C. *(cilt)* / S. *(sayı)* |

## Core rules

1. **Ampersand `&`** is used **only** in the reference list and in
   **parenthetical** in-text citations. In running prose, write the Turkish word
   **ve**.
   - Narrative: *Yılmaz ve Demir (2020) …*
   - Parenthetical: *(Yılmaz & Demir, 2020)*
2. **`ve ark.` vs `vd.`** — both stand for "et al." (*ve arkadaşları* /
   *ve diğerleri*). **Choose one and use it consistently** across the whole
   manuscript. A journal guideline may mandate a specific one.
3. **Secondary citation — `aktaran`.** When you cite source A through source B
   (you read B, which quotes A), credit both:
   *(Yılmaz, 2018, aktaran Demir, 2021)*. List **only the source you actually
   read** (Demir, 2021) in the reference list.
4. **Diacritics & capitalization.** Preserve İ/ı, Ş/ş, Ğ/ğ, Ç/ç, Ö/ö, Ü/ü in
   author names and titles. Apply Turkish casing rules; sentence-case article
   and book titles as APA requires.

## Worked in-text examples

| Type | Türkçe APA 7 in-text |
|------|----------------------|
| One author, narrative | Demir (2021) çalışmasında … |
| One author, parenthetical | … bulgular desteklemektedir (Demir, 2021, s. 45). |
| Two authors, narrative | Yılmaz ve Demir (2020) … |
| Two authors, parenthetical | … (Yılmaz & Demir, 2020). |
| 3+ authors | Kaya vd. (2019) / (Kaya vd., 2019) |
| No date | (Aydın, t.y.) |
| Page range | (Çelik, 2022, ss. 12-15) |
| Secondary | (Yılmaz, 2018, aktaran Demir, 2021) |

## Worked reference-list examples

**Journal article (Türkçe)**
> Yılmaz, A., & Demir, B. (2020). Çevrimiçi öğrenmede etkileşim. *Eğitim ve
> Bilim, 45*(203), 112-130. https://doi.org/10.xxxx/xxxxx

**Book**
> Kaya, C. (2019). *Nitel araştırma yöntemleri* (3. baskı). Pegem Akademi.

**Book chapter (with editor / hazırlayan)**
> Aydın, D. (2021). Karma yöntem tasarımları. A. Yılmaz (Haz.), *Araştırma
> tasarımı* (ss. 75-98) içinde. Anı Yayıncılık.

**Translated work (Çev.)**
> Creswell, J. W. (2017). *Araştırma deseni* (S. B. Demir, Çev.). Eğiten Kitap.
> (Orijinal eserin yayın tarihi 2014).

**Thesis (YÖK Ulusal Tez Merkezi)**
> Çelik, E. (2022). *Başlık* (Yayın No. 123456) [Yüksek lisans tezi, İzmir
> Ekonomi Üniversitesi]. YÖK Ulusal Tez Merkezi.

(For searching/discovering theses themselves, route to `alterlab-yok-tez`.)

**Web source (Erişim adresi)**
> TÜBİTAK ULAKBİM. (t.y.). *TR Dizin değerlendirme kriterleri*. Erişim adresi
> https://trdizin.gov.tr/?p=456

## What this skill does not do

- It does **not** verify that a cited work exists — that is
  `alterlab-citation-verifier`.
- It does **not** produce English-venue templates — that is
  `alterlab-venue-templates` / `alterlab-citation-mgmt`.
