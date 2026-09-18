---
name: alterlab-tr-research-ethics
description: "Scaffolds Turkish human-subjects etik kurul (ethics committee) applications and routes a study to the correct committee using the TR Dizin/ULAKBIM 2020 trigger rule: survey, interview, focus-group, observation, or experiment data collection requires a university Girisimsel Olmayan Etik Kurulu (non-interventional committee); drug, device, cosmetic, stem-cell, or BA-BE clinical studies also require a TITCK-approved Klinik Arastirmalar Etik Kurulu plus a separate TITCK permit. Generates bilingual (TR/EN) Etik Kurul Basvuru Formu, basvuru dilekcesi (cover petition), and Bilgilendirilmis Gonullu Olur Formu (informed consent), and lints a consent draft against the TITCK 2023 minimum-content checklist. Use when the user needs a Turkish etik kurul basvurusu, an onam/olur (consent) formu, asks which ethics committee a study requires, or needs TITCK approval guidance. For non-Turkey IRB/Belmont/GDPR use alterlab-research-ethics; for KVKK data plans use alterlab-kvkk-dmp. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Write Edit Bash(python:*)
compatibility: No API key required. Guidance + offline scaffolder; the consent linter (scripts/consent_form_check.py) runs locally via `uv run python` with the Python standard library only.
metadata:
  skill-author: AlterLab
  version: "1.0.0"
  last_updated: "2026-06-06"
  depends_on: "alterlab-research-ethics (international IRB/ethics sibling), alterlab-kvkk-dmp (data-protection plans)"
---

# TR Research Ethics — Turkish Etik Kurul & Onam Form Scaffolder

The Turkey-specific counterpart to `alterlab-research-ethics`. Given a study
description, it answers the first question every Turkish researcher faces —
**which etik kurul** (ethics committee) do I need? — then scaffolds the bilingual
dossier (başvuru formu, dilekçe, onam formu) and lints the consent form against
the TİTCK minimum-content checklist. Glossary on first use: *etik kurul* =
ethics committee; *onam / olur formu* = informed-consent form; *dilekçe* = formal
cover petition; *TİTCK* = Türkiye İlaç ve Tıbbi Cihaz Kurumu (Turkish Medicines
and Medical Devices Agency); *öz* = abstract.

This skill scaffolds and routes. It does **not** grant approval, and a draft it
produces is not a substitute for your institution's own committee templates,
which always take precedence.

## When to Use This Skill

Use it when the request is about **Turkish** human-subjects ethics review:

```
IEU anket çalışması için etik kurul başvurusu hazırla
Bu cihaz çalışması için TİTCK onayı / klinik araştırma etik kurulu gerekir mi?
Draft a Turkish bilgilendirilmiş onam (informed consent) form for an interview study
Which ethics committee do I need for a focus-group study at a Turkish university?
Check my olur formu against the TİTCK minimum-content rules
```

### Does NOT Trigger

Route adjacent requests to the correct sibling skill instead of firing here:

| Request | Route to |
|---------|----------|
| US/EU IRB, Belmont Report, HIPAA, GDPR, non-Turkey ethics board | `alterlab-research-ethics` |
| KVKK-compliant **data management plan**, anonymization, VERBIS, açık rıza data basis | `alterlab-kvkk-dmp` |
| TÜBİTAK Veri Yönetim Planı, Aperta deposit, open-access mandate | `alterlab-aperta` |
| Drafting the TÜBİTAK ARDEB 1001/1002-A **proposal** narrative | `alterlab-tubitak-proposal` |
| Survey **instrument design** / item wording (not the ethics dossier) | `alterlab-survey-design` |
| Qualitative interview/focus-group **method design** | `alterlab-qualitative-methods` |
| Pre-registration of hypotheses & analysis plan | `alterlab-open-science` |
| Checking a journal's TR Dizin indexing status | `alterlab-trdizin` |
| Docentlik (associate-professorship) eligibility / point math | `alterlab-docentlik-eligibility` |
| Akademik teşvik (academic-incentive) scoring | `alterlab-akademik-tesvik` |

The boundary with `alterlab-kvkk-dmp` matters: **ethics review (this skill)** and
**KVKK data protection (that skill)** are two separate legal tracks for the same
study. A full project usually needs both — scaffold the etik kurul dossier here,
then hand off to `alterlab-kvkk-dmp` for the data plan.

---

## The Routing Rule (do this first)

Turkish ethics review has **two doors**, and sending a study to the wrong one
wastes a review cycle. Route by what the study *does*, per
`references/etik_kurul_routing.md`:

**Door 1 — Üniversite Girişimsel Olmayan (non-interventional) Etik Kurulu.**
Triggered by the TR Dizin/ULAKBİM rule (mandatory for publications from **2020**):
any study collecting data **from participants** via **survey (anket), interview
(görüşme), focus group (odak grup), observation (gözlem), or experiment (deney)**
needs ethics-committee approval. For non-clinical social/behavioral/education
research this is the researcher's own university non-interventional committee.

**Door 2 — TİTCK-onaylı Klinik Araştırmalar Etik Kurulu + ayrı TİTCK izni.**
Studies on **human medicinal products, medical devices, cosmetics, stem cells,
or bioavailability/bioequivalence (BA/BE)** require a committee **approved by
TİTCK** *and* a **separate TİTCK start permit**. Per TİTCK, clinical research is
conducted "TİTCK tarafından onay verilen Etik Kurulların onayı ve Sağlık
Bakanlığının izni ile." **A decision from a committee not approved by TİTCK is
legally void for clinical research** — verify the committee's TİTCK accreditation
before you submit.

Governing instrument: *Beşeri Tıbbi Ürünlerin Klinik Araştırmaları Hakkında
Yönetmelik* (Regulation on Clinical Research of Human Medicinal Products),
mevzuat.gov.tr MevzuatNo 40207. See `references/etik_kurul_routing.md` for the
full decision tree, edge cases (retrospective record review, secondary data,
minors/vulnerable groups), and source citations.

> Some studies hit **both** doors (e.g. a device trial that also runs a patient
> survey). When in doubt, the clinical track governs and you escalate to Door 2.

---

## What It Produces

A bilingual (Turkish primary, English gloss) dossier skeleton. Pull the
templates from `references/dossier_templates.md`:

1. **Etik Kurul Başvuru Formu** — application form skeleton: title, PI/araştırmacı
   roster, aim & rationale (öz), design, population & sample, instruments,
   risk/benefit, data-handling summary (with a pointer to the KVKK plan), and the
   informed-consent procedure.
2. **Başvuru Dilekçesi** — the formal cover petition addressed to the committee.
3. **Bilgilendirilmiş Gönüllü Olur Formu** — the participant-facing consent form,
   built to satisfy the TİTCK minimum-content checklist (below).
4. **Ek/CV bundle checklist** — instruments, measurement tools, researcher CVs,
   data-collection-permission letters, and any institutional annexes.

Always tell the user that **their own university committee's official form
overrides this skeleton** where the two differ.

---

## Consent-Form Minimum Content (TİTCK, updated 29 Mar 2023)

The Bilgilendirilmiş Gönüllü Olur Formu must, at minimum, carry the elements in
`references/consent_minimum_contents.md`. Headline items:

- **Date, version, and page numbering on every page** (and volunteer initials per
  page for clinical-track forms).
- **Plain-language** statement of purpose, procedures, expected duration, and
  what participation involves.
- **Foreseeable risks/discomforts and benefits**, stated honestly.
- A **24-hour contact** for problems or questions.
- An explicit statement that participation is **voluntary** and the participant
  may **withdraw at any time without penalty**.
- An explicit **no-coercion** statement.
- For clinical-track studies: insurance, alternative treatments, and the
  sponsor/contact chain as the regulation requires.

### Lint a draft consent form

```bash
uv run python skills/turkish-academia/alterlab-tr-research-ethics/scripts/consent_form_check.py \
    path/to/olur_formu.md
```

The linter (`scripts/consent_form_check.py`, standard-library only) scans a draft
for the required elements above (in Turkish or English) and prints a per-element
PASS / MISSING table plus an overall verdict. It is a **completeness aid, not a
legal sign-off**: a PASS means the checklist elements are present, not that the
wording satisfies the committee. Run it, read the JSON/table, and report the
MISSING items to the user with the exact element name.

---

## Workflow

1. **Classify the study** → run the routing rule. State which door (committee
   type) applies and *why*, citing the trigger (e.g. "collects interview data →
   non-interventional committee" or "tests a medical device → TİTCK clinical
   committee + permit").
2. **Flag the clinical-track gate** when Door 2 applies: remind the user to
   confirm the committee is TİTCK-approved and that a separate TİTCK permit is
   required.
3. **Scaffold the dossier** from `references/dossier_templates.md`, filled with
   the study's specifics; keep Turkish as the primary language with an English
   gloss.
4. **Build & lint the consent form** against the TİTCK checklist; run
   `scripts/consent_form_check.py` and surface MISSING elements.
5. **Hand off** the data-protection half to `alterlab-kvkk-dmp` and (if funded /
   open-access) the deposit half to `alterlab-aperta`.
6. **Disclaim**: outputs are drafts; the institution's official forms and the
   committee's own decision are authoritative. Caps, forms, and checklists change
   — verify against the current TİTCK / university committee documents before
   submission.

---

## Self-Check Before Reporting

- Did I name the **specific committee type** (non-interventional vs TİTCK
  clinical) and the trigger that put the study there?
- For any clinical-track study, did I flag the **TİTCK-approval + separate permit**
  requirement and the "non-approved committee = legally void" rule?
- Did I run the consent linter and report **MISSING** elements by name, not just a
  pass/fail?
- Did I route data-protection to `alterlab-kvkk-dmp` rather than improvising KVKK
  advice here?
- Did I state that institutional forms override the skeleton and that figures/rules
  must be verified against current sources?

---

## References

- `references/etik_kurul_routing.md` — full two-door decision tree, trigger list,
  edge cases, and primary-source citations.
- `references/consent_minimum_contents.md` — the TİTCK minimum-content checklist
  the linter enforces, element by element.
- `references/dossier_templates.md` — bilingual başvuru formu, dilekçe, and olur
  formu skeletons plus the annex checklist.

### Primary sources

- TİTCK — Klinik Araştırmalar. https://www.titck.gov.tr/faaliyetalanlari/ilac/klinik-arastirmalar
- *Beşeri Tıbbi Ürünlerin Klinik Araştırmaları Hakkında Yönetmelik* — mevzuat.gov.tr MevzuatNo 40207 (R.G. 27/5/2023, No. 32203).
- TİTCK informed-consent minimum contents, updated 29 Mar 2023.
- TR Dizin (TÜBİTAK ULAKBİM) research-and-publication-ethics criteria — ethics-committee approval mandatory for participant data collection in publications from 2020. https://trdizin.gov.tr/

Part of the AlterLab Academic Skills suite.
