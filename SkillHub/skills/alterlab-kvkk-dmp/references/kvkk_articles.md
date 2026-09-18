# KVKK (Law 6698) — Article Map for Research Data Management

Article wording below is sourced to the primary text of **Law No. 6698**
(mevzuat.gov.tr/mevzuatmetin/1.5.6698.pdf) and the **official KVKK English
translation** (kvkk.gov.tr/Icerik/6649/Personal-Data-Protection-Law). Where an
amendment by **Law No. 7499** (published in the Official Gazette 12 Mar 2024, RG
No. 32487) changed the article, it is noted. This is a research-DMP-oriented
digest, not the full statute — consult the primary text before relying on an
output.

> **Maintenance note.** Last verified 2026-06-06 against the sources above.
> Re-verify against the current law before relying on any output. The most
> recent substantive change is Law 7499 — adopted 2 Mar 2024, published in the
> Official Gazette 12 Mar 2024 (RG No. 32487), with the KVKK provisions effective
> 1 Jun 2024 — touching Art. 6, 9, 18.

---

## Art. 5 — Conditions for processing personal data (kişisel verilerin işlenme şartları)

- **Default rule:** "Personal data shall not be processed without **explicit
  consent** (açık rıza) of the data subject."
- Processing **without** explicit consent is permitted **only** where one of the
  enumerated Art. 5(2) conditions applies, e.g.: expressly provided by law;
  necessary to protect life/bodily integrity where consent cannot be obtained;
  necessary for a contract; a legal obligation of the controller; data made
  public by the data subject; establishment/exercise/defence of a right; or the
  controller's legitimate interests without harming the subject's rights.
- **DMP consequence — the key divergence from GDPR:** there is **no standalone
  "scientific research" lawful basis** in KVKK Art. 5. If consent is not used,
  the processing must fit one of the enumerated alternatives, or the data must be
  anonymized (Art. 28). Do not invent a "research" basis.

## Art. 6 — Special categories of personal data (özel nitelikli kişisel veriler)

- Special categories include: race, ethnic origin, political opinion,
  philosophical belief, religion/sect, dress, association/foundation/union
  membership, **health (sağlık)**, sexual life, criminal convictions/security
  measures, and **biometric and genetic data**.
- Processing of special-category data is **prohibited** except in the enumerated
  cases (the regime was restructured by Law 7499, published in the Official
  Gazette 12 Mar 2024; KVKK provisions effective 1 Jun 2024). The Board may
  require **adequate measures** (yeterli önlemler) for such processing.
- **DMP consequence:** health/genetic/biometric research data needs an explicit
  Art. 6 basis (commonly açık rıza) **and** the Board-mandated adequate measures
  documented in the plan — or full anonymization to leave scope.

## Art. 7 — Erasure, destruction or anonymization (silme, yok etme veya anonim hale getirme)

- "Personal data shall be **erased, destroyed or anonymized** by the data
  controller, **ex officio** or **on the request of the data subject**, in the
  event that the reasons for the processing no longer exist."
- Procedure detailed in the **By-Law on Erasure, Destruction or Anonymization of
  Personal Data** (kvkk.gov.tr/Icerik/6636).
- **DMP consequence:** state a retention period and a destruction method
  (which of erase / destroy / anonymize) per data category, triggered at
  purpose-end.

## Art. 9 — Transfer of personal data abroad (yurt dışına aktarma) — *amended by Law 7499 (Official Gazette 12 Mar 2024; in force 1 Jun 2024)*

- Transfer abroad requires either an **adequacy decision** (yeterlilik kararı) by
  the Board, or — absent one — an enumerated **appropriate safeguard** (standard
  contracts / standart sözleşme, binding corporate rules / bağlayıcı şirket
  kuralları, written undertakings, etc.), with limited incidental-transfer
  exceptions.
- The Law 7499 amendment (Official Gazette 12 Mar 2024, in force 1 Jun 2024)
  **restructured** Art. 9 around adequacy decisions and standard contracts. **Do
  not reuse pre-2024 "explicit consent for every overseas transfer" boilerplate.**
- **DMP consequence:** any cloud/storage outside Türkiye must name its Art. 9
  mechanism. Flag US/EU cloud explicitly.

## Art. 13 — Application to the data controller (veri sorumlusuna başvuru)

- The controller must conclude a data-subject application **within thirty days**
  (otuz gün) at the latest, free of charge unless an extra cost is incurred.
- **DMP consequence:** name the contact point and the 30-day procedure for
  data-subject requests (access, rectification, erasure, etc.).

## Art. 16 — Data Controllers' Registry / VERBIS (Veri Sorumluları Sicili)

- Natural or legal persons who process personal data must **register with VERBIS
  prior to processing**; the Board may **exempt** categories of controllers by
  **objective criteria** (e.g. number of employees, annual balance sheet,
  activity type).
- **DMP consequence:** record VERBIS status — registered, exempt (state the
  objective criterion), or pending — and the registration timing relative to
  processing start.

## Art. 18 — Misdemeanours / administrative fines (kabahatler)

- Administrative fines attach to breaches (e.g. failure to fulfil disclosure,
  data-security, registration obligations); amended by Law 7499 (Official Gazette
  12 Mar 2024; in force 1 Jun 2024).
- **Fines are revalued every January** under the Tax Procedure Law (Vergi Usul
  Kanunu) revaluation rate. **Cite the mechanism, never a hard-coded current-year
  TRY amount** — it goes stale annually. Direct the user to the current figure.

## Art. 28 — Exceptions (istisnalar) — the research lever

The full exemption from the Law (not merely from some obligations) for the
relevant research cases:

- **Art. 28(1)(b):** personal data processed for official statistics, **provided
  that they are anonymized**, for purposes such as **research, planning and
  statistics**, are outside the scope of the Law. *(Exact translation of the
  bend (b) clause: "personal data are processed for official statistics and
  provided that they are being anonymized for the purposes for such as research,
  planning and statistics.")*
- **Art. 28(1)(c):** personal data processed for **artistic, historical,
  literary or scientific purposes**, or within the scope of freedom of
  expression, within stated limits (national defence, privacy, etc.), are outside
  the scope of the Law.

**DMP consequence — the primary compliance lever:** a **genuinely anonymized**
research dataset rides Art. 28(1)(b) and escapes consent, VERBIS, and transfer
constraints. This only holds if the data are **not re-identifiable** — see
`anonymization_methods.md`.
