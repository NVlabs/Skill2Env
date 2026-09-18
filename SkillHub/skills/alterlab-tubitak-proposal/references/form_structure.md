# ARDEB 1001 & 1002-A Form Structure (annotated)

The section tree below is the directorate's own heading order, as carried by the official
TÜBİTAK ARDEB application forms (the `.doc` templates and their `başvuru rehberi` guides). Draft
**to these headings, in this order** — ARDEB hakem (referee) panels score against this structure,
not against an IMRaD paper. Keep the Turkish heading; the English in parentheses is a gloss for
the drafter, not a section to add.

Authoritative form/guide sources (verify the current period before relying on caps):

- 1001 form: `https://tubitak.gov.tr/sites/default/files/2024-04/1001_basvuru_formu.doc`
- 1001 guide: `https://tubitak.gov.tr/sites/default/files/2024-04/ardeb_1001_basvuru_rehberi.pdf`
- 1002-A form: `https://tubitak.gov.tr/sites/default/files/20689/1002_a_basvuru_formu.doc`
  (a newer dated form also exists, e.g. `…/2025-04/1002_a_basvuru_formu_2025.doc`)
- 1002-A guide: `https://tubitak.gov.tr/sites/default/files/2024-04/1002_a_programi_basvuru_rehberi.pdf`

> The exact wording of sub-headings is revised between periods. Treat the tree as the stable
> skeleton; reconcile sub-heading labels and any numbering shifts against the current rehber.

---

## ÖZET (TR) + ABSTRACT (EN)

- Written as **two separate blocks** — ÖZET (Turkish) and ABSTRACT (English) — each **≤ 600
  words** counted *independently* (see `program_profiles.md`). Keep them as distinct headings so
  the per-language cap can actually be measured; don't merge them into one block.
- Each is followed by its **Anahtar Kelimeler / Keywords**.
- This is the panel's first read. State the gap, the aim, the method in one breath, and the
  expected yaygın etki (broader impact). Do not exceed the word cap — it is an eligibility filter.

## 1. ÖZGÜN DEĞER (Original Value / Significance)

The most heavily weighted block of a 1001. This is where novelty is decided.

- **1.1 Konunun Önemi ve Özgün Değer** (Importance & original value of the topic) — situate the
  problem in the literature, name the specific gap, and state what is *genuinely new* in the
  proposal. Cite into EK-1.
- **1.2 Araştırma Sorusu / Hipotezi** (Research question / hypothesis) — explicit, falsifiable,
  tied to the aim.
- **1.3 Amaç ve Hedefler** (Aim & objectives) — one aim; several **measurable** hedefler
  (objectives) that map one-to-one onto work packages in §3.

## 2. YÖNTEM (Method)

- Research design, materials, data-collection and analysis methods, sample/dataset, statistical
  or computational approach.
- This section carries **yapılabilirlik** (feasibility): show the method is appropriate *and*
  achievable with the stated resources and timeline.
- If human/animal subjects or personal data are involved, state that ethics approval / data
  governance is handled — and route the actual etik kurul form to `alterlab-tr-research-ethics`
  and the data plan to `alterlab-kvkk-dmp`. Do not draft those here.

## 3. PROJE YÖNETİMİ (Project Management)

- **3.1 İş-Zaman Çizelgesi ve İş Paketleri** (Work–time chart & work packages) — break the
  project into iş paketleri (work packages, WPs); each WP has objectives, tasks, responsible
  personnel, success criteria, and a deliverable. Include the **İş-Zaman Çizelgesi** (a
  Gantt-style work–time chart). **A B-Planı (contingency/risk plan) is required** — identify the
  riskiest WPs and the fallback path. (Gantt rendering/aesthetics → delegate to
  `alterlab-research-grants`.)
- **3.2 Araştırma Olanakları** (Research facilities/resources) — institutional infrastructure,
  equipment, lab access, and any collaborators' resources that make the project feasible.

## 4. YAYGIN ETKİ (Broader Impact / Dissemination)

Populate **all three** sub-parts; a thin yaygın etki is a common weakness flagged by panels.

- **4.1 Öngörülen Çıktılar** (Expected outputs) — concrete deliverables: publications, theses,
  datasets, software, patents, prototypes.
- **4.2 Öngörülen Etkiler** (Expected impacts) — scientific, economic/commercial, and societal
  effects.
- **Bilim İletişimi / Yayılım** (Science communication / dissemination) — how results reach the
  scientific community and the public.

## EK-1. Kaynaklar (References)

Cited literature for §1–§4. Have `alterlab-citation-verifier` existence-check the bibliography
before submission — fabricated/AI-hallucinated references are a credibility risk in front of a
panel.

## EK-2. Bütçe ve Gerekçesi (Budget & Justification)

Itemized budget (equipment/makine-teçhizat, consumables/sarf, travel/seyahat, service
procurement/hizmet alımı, personnel/burs) **with a justification per line tied to the work
packages**. The total must respect the program budget ceiling (see `program_profiles.md`),
excluding the items the program excludes (e.g. PTİ/proje teşvik ikramiyesi and kurum hissesi for
1001). For KVKK/Aperta data-management costs and plans, route to `alterlab-kvkk-dmp` /
`alterlab-aperta`.

## EK-3. Diğer Projeler / TÜBİTAK Destekleri (Other Projects & Prior Support)

The PI's and team's other ongoing/recent projects and prior TÜBİTAK support, for workload and
duplication checks.

---

## 1001 vs 1002-A — the delta

1002-A (**Hızlı Destek Modülü** / Fast Support Module) is the **trimmed** variant:

- Same backbone (Özgün Değer → Yöntem → İş Paketleri → Yaygın Etki → Kaynaklar → Bütçe) but
  **lighter** — less depth expected in project-management and yaygın-etki blocks.
- Hard **≤ 12-page** form limit (excluding annexes); much shorter than a 1001.
- Lower budget ceiling and shorter duration (see `program_profiles.md`).
- **Rolling / year-round (sürekli)** submission, not a periodic çağrı (call).
- Aimed at short-term, low-budget, non-urgent R&D. (The separate **1002-B Acil Destek Modülü**
  is for *urgent* needs and is out of scope for this skill.)
