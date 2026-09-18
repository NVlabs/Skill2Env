# Worked Walkthrough — KVKK DMP for a Survey + Health-Data Study

A concrete pass through the six decisions for a representative project, plus a
fill-in DMP outline. Article references trace to `kvkk_articles.md`. This is an
illustrative template, not legal advice — adapt to the actual study and obtain a
veri sorumlusu / KVKK-officer sign-off for high-risk processing.

## Sample project

> A university research team runs an online **survey** (demographics, attitudes)
> and collects **clinical health measurements** (special-category data) from
> consenting adult participants at a Türkiye site. Survey responses are stored on
> a Türkiye-hosted server; the team wants to analyze de-identified data and
> deposit an open dataset.

## The six decisions, resolved

1. **Lawful basis (Art. 5 / Art. 6).** Survey personal data and the
   special-category **health** measurements: collect under **açık rıza** (explicit
   consent), because KVKK has no standalone research basis. Health data
   additionally engages **Art. 6** — document the Board-mandated **adequate
   measures** (access control, encryption at rest, restricted personnel).

2. **Anonymization exemption (Art. 28(1)(b)).** Plan to **anonymize** the
   analytic dataset (remove direct identifiers, generalize quasi-identifiers,
   k-anonymity) so the *analysis and the open deposit* fall outside the Law's
   scope. The **raw identifiable dataset** does not — it is governed by the
   consent basis above until anonymization completes. (See
   `anonymization_methods.md`.)

3. **Retention & destruction (Art. 7).** Raw identifiable data retained only
   until anonymization is verified; destroyed (yok etme) thereafter. Anonymized
   analytic dataset retained for [e.g. 5 years post-publication] for
   reproducibility. State method per category.

4. **Data-subject rights (Art. 13).** Name a contact point; commit to a
   **30-day** (otuz gün) response for access/rectification/erasure requests on the
   identifiable data (anonymized data has no data subject to serve).

5. **Cross-border transfer (Art. 9).** Identifiable data stays on the
   Türkiye-hosted server → no Art. 9 issue. If a non-Türkiye cloud were used,
   name the Art. 9 mechanism (adequacy decision or standard contract under the
   Law 7499 regime — Official Gazette 12 Mar 2024, in force 1 Jun 2024). The
   **anonymized** open deposit is out of scope, so a
   foreign repository is unproblematic.

6. **VERBIS (Art. 16).** Record the institution's VERBIS status (registered /
   exempt-by-objective-criterion / pending) for the processing.

## Fill-in DMP outline (the scaffold emits this shape)

```
# Veri Yönetim Planı (KVKK) / Data Management Plan (KVKK)

## 1. Proje / Project
   - Başlık, sorumlu, kurum / title, PI, institution

## 2. Veri kategorileri / Data categories
   - Kişisel / personal:            [list]
   - Özel nitelikli / special (Art. 6): [list — health/genetic/biometric?]
   - Tanımlanabilir mi? / identifiable vs. (intended-)anonymized

## 3. Hukuki dayanak / Lawful basis (Art. 5 / 6)
   - Basis: [açık rıza / enumerated alternative]
   - Art. 6 adequate measures (if special category): [list]

## 4. Anonimleştirme / Anonymization (Art. 28(1)(b))
   - Technique(s): [masking / generalization / k-anonymity ...]
   - Re-identification-risk assessment: [summary]
   - Exemption claimed for: [analytic dataset / open deposit]

## 5. Saklama ve imha / Retention & destruction (Art. 7)
   - Per category: retention period + method (silme/yok etme/anonim hale getirme)

## 6. İlgili kişi hakları / Data-subject rights (Art. 13)
   - Contact point; 30-day procedure

## 7. Yurt dışı aktarım / Cross-border transfer (Art. 9)
   - Storage location; mechanism for any non-Türkiye host

## 8. VERBIS (Art. 16)
   - Status: [registered / exempt (criterion) / pending]

## 9. Notlar / Notes
   - Law 7499 currency check (Official Gazette 12 Mar 2024; KVKK provisions
     effective 1 Jun 2024); sign-off; links to funder VYP
     (alterlab-aperta) and etik kurul approval (alterlab-tr-research-ethics)
```

## Hand-offs

- The **funder-facing TÜBİTAK VYP** (veri yönetim planı) and Aperta open-science
  deposit are owned by `alterlab-aperta`; pass this plan's anonymization /
  lawful-basis decision to it to populate the open-science Principle-6
  "why data is closed" justification.
- The **etik kurul** (ethics committee) application is owned by
  `alterlab-tr-research-ethics`.
