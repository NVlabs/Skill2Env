# Veri Yönetim Planı (VYP) / Data Management Plan — Section Tree

> **Last verified: 2026-06-06.** The VYP is prepared at TÜBİTAK grant-application
> time and covers the full data lifecycle. Confirm the current required structure
> against the live application before submission — TÜBİTAK may update the template.

This is the bilingual (TR/EN) section tree that `scripts/vyp_scaffold.py` emits.
It follows the data-lifecycle structure required by the TÜBİTAK Açık Bilim
Politikası (see `policy_mandates.md`). It is a **scaffold**, not the official form
verbatim — fill each section with the project's specifics.

## Section tree

| # | Turkish | English | What goes here |
|---|---------|---------|----------------|
| 1 | Veri Toplama ve Üretme | Data collection & generation | What data the project will create/collect; types, sources, volume; how/with what instruments |
| 2 | Veri Formatları ve Standartları | Formats & standards | File formats, metadata standards, naming conventions, documentation |
| 3 | Veri Depolama ve Yedekleme | Storage & backup | Where data lives during the project; backup; access control; security |
| 4 | Yasal ve Etik Hususlar | Legal & ethical considerations | **KVKK** lawful basis, personal/special-category data, **etik kurul** approval, consent; informs which data can be opened |
| 5 | Veri Paylaşımı ve Erişim | Sharing & access | What is shared openly vs restricted; repository = **Aperta**; embargo per field ceiling (≤6 mo STEM / ≤12 mo SSH); licence |
| 6 | Kapalı Veri Gerekçesi (İlke-6) | Closed-data justification (Principle 6) | If any data stays closed: the documented reason (KVKK/commercial/security/ethics), restricted-access plan, who may request access, opening trigger |
| 7 | Uzun Süreli Saklama ve Koruma | Long-term preservation | Retention period; preservation after project end; deletion/anonymisation plan |
| 8 | Sorumluluklar ve Kaynaklar | Roles & resources | Who is responsible for data management; resources/costs |

## How the script populates it

- `--field stem|ssh` writes the correct embargo ceiling into section 5.
- `--data-closed` activates section 6 and inserts an İlke-6 stub; `--closed-reason`
  picks the justification wording (KVKK / commercial / security / ethics).
- `--lang tr|en|both` selects Turkish, English, or a stacked bilingual document.

## KVKK / İlke-6 cross-link (important)

Sections 4 and 6 are where the **KVKK** decision lands. This skill records *that*
data is open or closed and *why* at the funder level. It does **not** run the KVKK
lawful-basis / anonymisation analysis — that is `alterlab-kvkk-dmp`'s job. Workflow:

1. Run `alterlab-kvkk-dmp` to get the lawful basis and the anonymisation/
   pseudonymisation outcome.
2. Paste that conclusion into VYP section 4, and — if data stays closed — into the
   İlke-6 justification in section 6.

This way one pass yields both the funder-facing VYP and the KVKK-compliance plan,
with the İlke-6 "why closed" paragraph populated from the KVKK decision.

## Disclaimer

Always tell the user to verify the current required VYP structure and any
field-specific guidance against the live TÜBİTAK application system before
submitting. Do not present this section tree as the immutable official form.
