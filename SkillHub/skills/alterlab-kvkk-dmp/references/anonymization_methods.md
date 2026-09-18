# Anonymization under KVKK — Techniques and the Re-identification Trap

Anonymization (**anonim hale getirme**) is the primary lever in a KVKK research
DMP because **Art. 28(1)(b)** removes genuinely anonymized research/planning/
statistics data from the scope of the Law entirely. But the exemption only holds
if the data are **truly non-re-identifiable**. This file summarizes the
technique families described in the KVKK **By-Law on Erasure, Destruction or
Anonymization of Personal Data** and the KVKK anonymization guide, and the trap
that voids the exemption.

Sourced to the KVKK By-Law (kvkk.gov.tr/Icerik/6636) and the primary text of
Law 6698. Last verified 2026-06-06. This is methodological guidance, not a
guarantee of legal sufficiency for a given dataset.

## The definition that matters

**Anonymization = rendering personal data such that it can no longer be
associated with an identified or identifiable natural person, even by matching
with other data.** The "even by matching with other data" clause is the whole
game: if a third party can re-link the record using auxiliary information, the
data is **not** anonymized and stays fully in scope.

> **Pseudonymization is NOT anonymization.** Replacing a name with a code while
> keeping a re-identification key (or leaving quasi-identifiers intact) yields
> **pseudonymized** data, which remains **personal data** under KVKK and does
> **not** qualify for the Art. 28 exemption.

## Technique families

| Family | What it does | Research caveat |
|---|---|---|
| **Masking / removal (maskeleme)** | Delete or black out direct identifiers (name, TC kimlik no, e-mail, phone) | Necessary but rarely sufficient — quasi-identifiers can still re-identify |
| **Aggregation (toplama / kümeleme)** | Report only group-level statistics (counts, means) instead of records | Strongest for statistics-only outputs; destroys record-level analysis |
| **Generalization (genelleştirme)** | Coarsen values: exact age → age band; full date → year; district → province | Tune coarseness to the re-identification risk; pairs with k-anonymity reasoning |
| **k-anonymity-style grouping** | Ensure every combination of quasi-identifiers is shared by **≥ k** records | Guards against singling-out; consider l-diversity for sensitive attributes |
| **Suppression / record removal** | Drop outlier records that are unique on quasi-identifiers | Document what was removed and why |
| **Noise addition / perturbation** | Add controlled random noise to numeric fields | Preserves distributions; balance utility vs. protection |

## Quasi-identifiers — the usual re-identification vectors

Even after removing direct identifiers, combinations of these can single out an
individual, especially in small Turkish institutional samples:

- date of birth / exact age, postal code / district (mahalle/ilçe), gender,
  rare diagnosis or medication, department/title in a small faculty, unusual
  demographic combinations.

Assess the joint distribution of quasi-identifiers, not each field in isolation.

## Re-identification-risk check before claiming the exemption

Before a DMP asserts Art. 28(1)(b), confirm:

1. **No direct identifiers** remain in the released dataset.
2. **No re-identification key** is retained alongside it (else it is pseudonymized).
3. **Quasi-identifiers are generalized/suppressed** so no record is unique on
   them (k-anonymity ≥ a justified k; sensitive attributes l-diverse where
   relevant).
4. **No plausible external dataset** re-links the records ("matching with other
   data" test) — consider public registries, voter rolls, social media.
5. The assessment and the chosen techniques are **documented** in the DMP.

If any check fails, the data is still personal data: it needs an Art. 5/6 lawful
basis, VERBIS consideration, and Art. 9 transfer compliance — it does **not**
ride the exemption.

## DMP wording pattern

> "Direct identifiers are removed at collection; quasi-identifiers (age, district)
> are generalized to 5-year bands and province; the analytic dataset satisfies
> k-anonymity (k=5) with no retained re-identification key. On this basis the
> analytic dataset is treated as **anonymized** under KVKK Art. 28(1)(b) and
> outside the scope of the Law. The raw identifiable dataset, held only until
> anonymization completes, is governed by [Art. 5/6 basis] and destroyed under
> Art. 7 at purpose-end."
