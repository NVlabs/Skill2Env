---
name: alterlab-tubitak-proposal
description: "Scaffolds TÜBİTAK ARDEB national research proposals (1001 Bilimsel ve Teknolojik Araştırma Projeleri and 1002-A Hızlı Destek Modülü) against the official .doc form trees: 1. ÖZGÜN DEĞER (konunun önemi/özgün değer, araştırma sorusu/hipotezi, amaç ve hedefler), 2. YÖNTEM, 3. PROJE YÖNETİMİ (iş-zaman çizelgesi/iş paketleri + B-Planı, araştırma olanakları), 4. YAYGIN ETKİ, EK-1 Kaynaklar, EK-2 Bütçe ve Gerekçesi. Enforces the 600-word TR/EN özet (abstract) caps, program caps (1001 <=36 months/3,000,000 TRY for 2026-1; 1002-A <=12 months/150,000 TRY, rolling), and the four panel review dimensions; submission via PBS (ardeb-pbs.tubitak.gov.tr) with ARBİS prerequisite. Delegates generic grant craft to alterlab-research-grants. Use when the user wants to write a TÜBİTAK 1001 or 1002-A proposal, draft özgün değer or yaygın etki sections, scaffold a Turkish national grant, or map broader-impacts framing to TÜBİTAK terms. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Write Edit Bash(python:*) WebFetch
compatibility: No API key required — generates proposal scaffolds offline; the structure checker runs via `uv run python` on stdlib only. Program caps/forms change each call period; WebFetch the live PBS/guide pages to confirm before submission.
metadata:
  skill-author: AlterLab
  version: "1.0.0"
  last_updated: "2026-06-06"
  depends_on: "alterlab-research-grants (generic grant-craft this skill delegates to)"
---

# TÜBİTAK ARDEB Proposal Scaffolder — 1001 & 1002-A

Scaffolds a TÜBİTAK ARDEB (Araştırma Destek Programları Başkanlığı — the Research
Support Programmes directorate) proposal against the **verified official form tree**,
in the directorate's own Turkish section order, then maps the researcher's content into
each heading and checks the hard caps the panel rejects on. It owns the **Turkish-specific
form structure, terminology, and program rules** only — generic grant-craft (broader-impacts
argumentation, feasibility narrative, Gantt aesthetics) is delegated to
`alterlab-research-grants`.

Two variants:

- **1001** — *Bilimsel ve Teknolojik Araştırma Projelerini Destekleme Programı* (Support
  Programme for Scientific and Technological Research Projects). The heavy, full-form program.
- **1002-A** — *Hızlı Destek Modülü* (Fast Support Module). The light, short-form, low-budget,
  rolling-application variant.

## Quick Start

```
Write me a TÜBİTAK 1001 proposal outline for <topic>
Draft the özgün değer (original value) section for my ARDEB 1001
Scaffold a 1002-A Hızlı Destek başvurusu
Turn my NSF broader-impacts paragraph into a TÜBİTAK yaygın etki section
```

→ Pick the variant, generate the section tree (`scripts/scaffold_proposal.py`), draft each
heading from the user's material, then run the cap/structure check
(`scripts/scaffold_proposal.py --check`) before reporting. Always print the
**verify-current-call** disclaimer — caps and forms change every application period.

## When to Use This Skill

Use this skill when the request is to **author, outline, or section-map a TÜBİTAK ARDEB
1001 or 1002-A proposal**, draft a specific Turkish section (özgün değer = original value;
yaygın etki = broader impact/dissemination; yöntem = method; iş paketi = work package), or
translate international broader-impacts framing into TÜBİTAK terminology.

### Does NOT Trigger

The route below sends adjacent requests to the correct sibling skill in the suite. This skill
does **not** check journal indexing, compute career points, or write a non-Turkish grant.

| The request is really about… | Route to |
|------------------------------|----------|
| Generic grant-craft / NSF / NIH / ERC narrative, broader-impacts argumentation in the abstract | `alterlab-research-grants` |
| Interim/final progress report (gelişme/sonuç raporu) for an **awarded** TÜBİTAK project | `alterlab-grant-reporting` |
| Is a target journal in **TR Dizin** (national index)? | `alterlab-trdizin` |
| Does a candidate clear **doçentlik** (associate-professor) point thresholds? | `alterlab-docentlik-eligibility` |
| Computing the **akademik teşvik** (academic-incentive) net score | `alterlab-akademik-tesvik` |
| The **etik kurul** (ethics-committee) application / informed-consent form | `alterlab-tr-research-ethics` |
| The KVKK-compliant data-management plan / TÜBİTAK Veri Yönetim Planı | `alterlab-kvkk-dmp` |
| Depositing the accepted manuscript on **Aperta** under the Open Science Policy | `alterlab-aperta` |
| Turkish APA-7 / TR Dizin manuscript style for the paper itself | `alterlab-tr-academic-style` |
| Searching DergiPark / YÖK theses for the literature review | `alterlab-dergipark`, `alterlab-yok-tez` |

---

## The Verified Form Tree

Both forms share the same backbone; 1002-A is the trimmed variant. Section names below are the
directorate's own headings (see `references/form_structure.md` for the full annotated tree and
the per-section drafting briefs).

| # | Section (TR) | English gloss | 1001 | 1002-A |
|---|--------------|---------------|------|--------|
| Özet | ÖZET (TR) + ABSTRACT (EN) | Abstract as **two separate blocks** (TR + EN), each with Anahtar Kelimeler / Keywords | ✅ | ✅ |
| 1 | **ÖZGÜN DEĞER** | Original value / significance | ✅ | ✅ |
| 1.1 | Konunun Önemi ve Özgün Değer | Importance & original value of the topic | ✅ | ✅ |
| 1.2 | Araştırma Sorusu / Hipotezi | Research question / hypothesis | ✅ | ✅ |
| 1.3 | Amaç ve Hedefler | Aim & objectives | ✅ | ✅ |
| 2 | **YÖNTEM** | Method | ✅ | ✅ |
| 3 | **PROJE YÖNETİMİ** | Project management | ✅ | (light) |
| 3.1 | İş-Zaman Çizelgesi ve İş Paketleri (+ **B-Planı**) | Work–time chart & work packages (+ contingency plan) | ✅ | ✅ |
| 3.2 | Araştırma Olanakları | Research facilities/resources | ✅ | ✅ |
| 4 | **YAYGIN ETKİ** | Broader impact / dissemination | ✅ | (light) |
| 4.1 | Öngörülen Çıktılar | Expected outputs | ✅ | ✅ |
| 4.2 | Öngörülen Etkiler / Bilim İletişimi | Expected impacts / science communication | ✅ | ✅ |
| EK-1 | Kaynaklar | References (cited literature) | ✅ | ✅ |
| EK-2 | Bütçe ve Gerekçesi | Budget & its justification | ✅ | ✅ |
| EK-3 | Diğer Projeler / TÜBİTAK Destekleri | Other projects & prior TÜBİTAK support | ✅ | (if applicable) |

**Map, don't invent.** The directorate evaluates against *these* headings; never silently
restructure them into an IMRaD paper. The özgün değer section is the single most weighted part
of a 1001 — it is where the panel decides novelty.

---

## The Hard Caps (panel rejects on these)

These are **administrative-eligibility** filters: a proposal that violates them can be returned
without scientific review. Pin them with `scripts/scaffold_proposal.py --check`; see
`references/program_profiles.md` for the full table with as-of dates.

| Item | 1001 | 1002-A |
|------|------|--------|
| Özet word cap (TR & EN each) | **600 words** | **600 words** |
| Project duration | **≤ 36 months** | **≤ 12 months** |
| Budget upper limit (PTİ/burs hariç) | **3,000,000 TRY** (2026-1 period) | **150,000 TRY/yr** (incl. burs, as of 2026-02-01) |
| Application window | Periodic call (çağrı) | **Rolling / year-round (sürekli)** |
| Form length | per current rehber (guide) | **≤ 12 pages** excl. annexes |
| PI (Yürütücü) requirement | Doctorate + eligible affiliation | per current rehber |

> **Verify-current-call disclaimer (always print).** Every TRY figure, page limit, and
> duration above is dated and *changes each application period*. Before the user submits,
> WebFetch the live program page and the current başvuru rehberi (application guide) listed in
> `references/program_profiles.md` and reconcile. Caps observed for the 2026-1 (1001) and
> 2026-02-01 (1002-A) periods; TÜBİTAK has announced major 1002 program changes, so treat
> 1002-A caps as especially volatile.

---

## The Four Review Dimensions

ARDEB panels score against four axes. Draft each section *to* its axis; the mapping below is
the lens the panelist (hakem) uses. Full criteria in `references/review_criteria.md`.

| Dimension (TR) | English | Carried mainly by |
|----------------|---------|-------------------|
| **Bilimsel/Teknolojik Nitelik ve Özgün Değer** | Scientific quality & original value | Özet, §1 ÖZGÜN DEĞER, EK-1 |
| **Yöntem** | Method & feasibility (yapılabilirlik) | §2 YÖNTEM |
| **Proje Yönetimi ve Araştırma Olanakları** | Project management & resources | §3 (iş paketleri, B-Planı, §3.2) |
| **Yaygın Etki** | Broader impact & dissemination | §4 YAYGIN ETKİ, EK-2 |

---

## Terminology Bridge (international ↔ TÜBİTAK)

When the user arrives with NSF/NIH/ERC material, translate the *concept*, not word-for-word.
Full glossary in `references/terminology_bridge.md`.

| International term | TÜBİTAK term | Note |
|-------------------|--------------|------|
| Significance / innovation / intellectual merit | **Özgün değer** | The most weighted axis; lead with what is genuinely new |
| Broader impacts | **Yaygın etki** | Split into çıktılar (outputs), etkiler (impacts), bilim iletişimi (sci-comm) |
| Feasibility | **Yapılabilirlik** | Lives inside §2 YÖNTEM + §3 management |
| Contingency / risk plan | **B-Planı** | A *required* sub-element of the work-package section, not optional |
| Work package / Gantt | **İş paketi / İş-Zaman Çizelgesi** | Gantt aesthetics → delegate to `alterlab-research-grants` |
| Aims & objectives | **Amaç ve Hedefler** | Hedefler should be measurable, tied to work packages |

---

## Pipeline (how to run it)

### 1. Choose the variant and generate the scaffold

```bash
uv run python skills/turkish-academia/alterlab-tubitak-proposal/scripts/scaffold_proposal.py \
    --program 1001 \
    --title "<project title>" \
    --out proposal_scaffold.md
```

`--program` accepts `1001` or `1002a`. The script emits the full Markdown section tree with the
TR heading, its English gloss, the panel dimension each section serves, and a short drafting
brief per heading. Use `--lang tr` (default) or `--lang both` for bilingual headings.

### 2. Draft each section from the user's material

Fill the scaffold from what the user provides. Keep the directorate's ordering. For özgün değer,
state the *gap* and the *new contribution* explicitly. For yaygın etki, populate all three
sub-parts (çıktılar / etkiler / bilim iletişimi). Pull literature into EK-1 Kaynaklar — and have
`alterlab-citation-verifier` existence-check the bibliography before submission.

### 3. Check the caps and structure

```bash
uv run python skills/turkish-academia/alterlab-tubitak-proposal/scripts/scaffold_proposal.py \
    --check proposal_scaffold.md --program 1001
```

The checker reports: missing required sections, TR/EN özet word counts vs the 600-word cap,
whether duration/budget statements (if present) exceed the program ceilings, and whether a
B-Planı sub-section exists. It is **advisory** — it never edits the proposal and it always
restates the verify-current-call disclaimer because the ceilings are period-specific.

### 4. Hand off and disclaim

- Budget detail / VYP-style data plan → name the sibling (`alterlab-kvkk-dmp`,
  `alterlab-aperta`); do not draft compliance text here.
- Always tell the user to confirm the live caps in the current rehberi before submission.

---

## Submission Surface (read-only facts)

- **PBS** — Proje Başvuru Sistemi at `ardeb-pbs.tubitak.gov.tr`. Proposals are entered and
  submitted here.
- **ARBİS** — Araştırmacı Bilgi Sistemi at `arbis.tubitak.gov.tr`. A current ARBİS record is a
  prerequisite; the PI/personnel CVs flow from it. Tell the user to refresh ARBİS *before*
  starting the PBS entry.

This skill does **not** automate or log into either system — it produces the document content
the researcher pastes/uploads.

---

## Self-Check Before Reporting

- Did you use the **directorate's section order and Turkish headings**, not an IMRaD remap?
- Is the **özet within 600 words in BOTH** Turkish and English?
- Did you state duration/budget **only with the verify-current-call disclaimer**, never as a
  guaranteed cap?
- Does §3 contain a **B-Planı**, and §4 all three yaygın-etki sub-parts?
- Did you **route** budget-compliance, ethics, indexing, and reporting asks to the correct
  siblings rather than answering them here?

---

## References

- `references/form_structure.md` — the full annotated 1001 & 1002-A section tree with a drafting
  brief per heading and the 1001-vs-1002-A delta.
- `references/program_profiles.md` — per-program caps (duration, budget, window, form length)
  with as-of dates and the live verification URLs.
- `references/review_criteria.md` — the four panel dimensions and how each section is scored.
- `references/terminology_bridge.md` — international ↔ TÜBİTAK concept glossary.

Part of the AlterLab Academic Skills suite.
