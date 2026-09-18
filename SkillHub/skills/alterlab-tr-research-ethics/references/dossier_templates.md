# Dossier Templates — Başvuru Formu, Dilekçe, Olur Formu

Bilingual skeletons for a Turkish etik kurul (ethics committee) submission.
Turkish is the primary language; the English gloss is for the researcher's
working copy and for bilingual studies. **The researcher's own university
committee form overrides these skeletons** wherever the two differ — always check
the institution's current template first.

Glossary: *başvuru formu* = application form; *dilekçe* = formal cover petition;
*öz* = abstract; *araştırmacı* = researcher/investigator; *ek* = annex/appendix.

---

## 1. Etik Kurul Başvuru Formu (Application Form skeleton)

```
ETİK KURUL BAŞVURU FORMU / ETHICS COMMITTEE APPLICATION FORM

1. Çalışmanın Başlığı / Study Title
   - TR:
   - EN:

2. Sorumlu Araştırmacı / Principal Investigator
   - Ad-Soyad, unvan / Name, title:
   - Kurum, birim / Institution, unit:
   - İletişim (e-posta, telefon) / Contact:

3. Araştırmacı Ekibi / Research Team
   - (ad, unvan, rol / name, title, role)

4. Öz / Abstract  (kısa amaç ve gerekçe / brief aim and rationale)
   - TR:
   - EN:

5. Çalışma Türü ve Tasarımı / Study Type & Design
   - (anket / görüşme / odak grup / gözlem / deney / klinik …)

6. Evren ve Örneklem / Population & Sample
   - Katılımcı sayısı, dahil/dışlama ölçütleri / N, inclusion/exclusion:

7. Veri Toplama Araçları / Instruments
   - (ölçek, anket formu, görüşme rehberi — Ek olarak ekleyin / attach as annex)

8. Risk ve Yarar Değerlendirmesi / Risk & Benefit Assessment

9. Aydınlatılmış Onam Süreci / Informed-Consent Procedure
   - (Bilgilendirilmiş Gönüllü Olur Formu Ek-? / consent form annex)

10. Veri Yönetimi ve Gizlilik / Data Management & Confidentiality
    - (KVKK uyumu için ayrı plan → alterlab-kvkk-dmp / KVKK plan handled separately)

11. Komite Türü / Committee Type
    - [ ] Girişimsel Olmayan Etik Kurulu (non-interventional)
    - [ ] TİTCK Klinik Araştırmalar Etik Kurulu + TİTCK izni (clinical + permit)

12. Ekler / Annexes  (see annex checklist below)
```

---

## 2. Başvuru Dilekçesi (Cover Petition skeleton)

```
[Üniversite] [...] ETİK KURULU BAŞKANLIĞINA

Aşağıda bilgileri verilen "[Çalışma Başlığı]" başlıklı çalışmanın etik açıdan
değerlendirilmesi ve onaylanması için gereğini arz ederim.

Çalışma türü        : [anket / görüşme / odak grup / gözlem / deney / klinik]
Sorumlu araştırmacı : [Ad-Soyad, unvan]
Kurum / birim       : [...]
Veri toplama dönemi : [...]
Ekler               : [Başvuru formu, ölçüm araçları, onam formu, CV(ler), izinler]

Tarih:
İmza:

--- English gloss ---
TO THE [University] [...] ETHICS COMMITTEE
I respectfully submit the study titled "[Title]" for ethical review and approval.
[fields as above]
```

---

## 3. Bilgilendirilmiş Gönüllü Olur Formu (Informed-Consent skeleton)

Build this against the TİTCK minimum-content checklist in
`consent_minimum_contents.md` and lint it with `scripts/consent_form_check.py`.

```
BİLGİLENDİRİLMİŞ GÖNÜLLÜ OLUR FORMU
(Her sayfada: Tarih __ | Versiyon __ | Sayfa __/__ | Gönüllü parafe: __)

Çalışmanın Amacı / Purpose:
   [sade dil ile / plain language]

Yapılacak İşlemler ve Süre / Procedures & Duration:
   [...]

Öngörülen Riskler ve Rahatsızlıklar / Foreseeable Risks & Discomforts:
   [...]

Beklenen Yararlar / Expected Benefits:
   [...]

Gizlilik ve Verilerin Kullanımı / Confidentiality & Data Use:
   [KVKK planına atıf / reference the KVKK plan]

Gönüllülük Beyanı / Voluntary Participation:
   Bu çalışmaya katılım tamamen gönüllülük esasına dayanır. Hiçbir baskı veya
   zorlama yoktur ve istediğiniz zaman, herhangi bir gerekçe göstermeksizin ve
   hak kaybına uğramaksızın çalışmadan ayrılabilirsiniz.
   (Participation is entirely voluntary; no coercion; you may withdraw at any
   time without penalty.)

24 Saat Ulaşılabilir İletişim / 24-hour Contact:
   [ad, telefon / name, phone]

[Klinik çalışmalar için ek / Clinical-track additions:
   Sigorta, alternatif tedaviler, sponsor/sorumlu araştırmacı bilgileri]

Gönüllü Ad-Soyad / Volunteer Name:  ____________   İmza/Signature: ______  Tarih: ____
Araştırmacı Ad-Soyad / Researcher:  ____________   İmza/Signature: ______  Tarih: ____
```

---

## 4. Ek / Annex Checklist

- [ ] Veri toplama araçları (anket, ölçek, görüşme rehberi) / instruments
- [ ] Bilgilendirilmiş Gönüllü Olur Formu / informed-consent form
- [ ] Araştırmacı özgeçmiş(ler)i / researcher CV(s)
- [ ] Veri toplama izinleri (kurum/okul/kuruluş) / data-collection permission letters
- [ ] (Klinik) TİTCK izni ve ilgili belgeler / (clinical) TİTCK permit & documents
- [ ] (Varsa) çocuk rızası / veli onamı formları / (if applicable) assent & guardian consent
- [ ] KVKK veri yönetim planı (→ alterlab-kvkk-dmp) / KVKK data plan

_Last verified: 2026-06-06. Field lists are illustrative skeletons; the binding
form is the one published by the researcher's own university ethics committee._
