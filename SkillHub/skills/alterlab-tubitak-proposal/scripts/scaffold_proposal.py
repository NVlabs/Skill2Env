#!/usr/bin/env python3
"""Scaffold and cap-check a TÜBİTAK ARDEB 1001 / 1002-A research proposal.

Two modes, both offline and dependency-free (Python standard library only):

  * **scaffold** (default) — emit the official ARDEB form section tree for the chosen
    program, in the directorate's own Turkish heading order, with an English gloss, the
    panel review dimension each section serves, and a short drafting brief per heading.

  * **--check FILE** — read an existing draft (Markdown) and report, advisory-only:
      - which required sections are missing,
      - the Turkish AND English özet (abstract) word counts vs the 600-word cap,
      - whether any stated duration / budget exceeds the program ceiling,
      - whether a B-Planı (contingency plan) sub-section is present.
    It never edits the draft and always restates the verify-current-call disclaimer,
    because every TRY figure / page limit / duration changes each application period.

The structure below is the VERIFIED official form tree (see ../references/form_structure.md).
The numeric caps are the values observed for the 2026-1 (1001) and 2026-02-01 (1002-A)
periods (see ../references/program_profiles.md). CAPS CHANGE EACH PERIOD — confirm against
the live program page and current başvuru rehberi before submission.

Usage:
    uv run python scaffold_proposal.py --program 1001 --title "My project" --out scaffold.md
    uv run python scaffold_proposal.py --program 1002a --lang both
    uv run python scaffold_proposal.py --check scaffold.md --program 1001
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass

DISCLAIMER = (
    "VERIFY CURRENT CALL: every TRY figure, page limit, and duration below is dated and "
    "changes each application period. Before submission, fetch the live program page and the "
    "current başvuru rehberi (application guide) and reconcile. Caps observed for the 2026-1 "
    "(1001) and 2026-02-01 (1002-A) periods; TÜBİTAK has announced major 1002 program changes."
)

# Program ceilings — see ../references/program_profiles.md. Dated, period-specific.
PROGRAMS = {
    "1001": {
        "name": "1001 - Bilimsel ve Teknolojik Araştırma Projelerini Destekleme Programı",
        "gloss": "Support Programme for Scientific and Technological Research Projects",
        "ozet_word_cap": 600,
        "max_months": 36,
        "budget_cap_try": 3_000_000,
        "budget_note": "üst limit excl. burs/PTİ/kurum hissesi; 2026-1 period",
        "window": "periodic çağrı (call)",
        "page_limit": None,
    },
    "1002a": {
        "name": "1002 - A Hızlı Destek Modülü",
        "gloss": "Fast Support Module",
        "ozet_word_cap": 600,
        "max_months": 12,
        "budget_cap_try": 150_000,
        "budget_note": "incl. burs; per year; as of 2026-02-01",
        "window": "rolling / year-round (sürekli)",
        "page_limit": 12,
    },
}


@dataclass
class Section:
    key: str          # stable id for the structure check
    number: str       # e.g. "1.1", "EK-2"
    tr: str           # Turkish heading (directorate's own)
    en: str           # English gloss
    dimension: str    # panel review axis it mainly serves
    brief: str        # one-line drafting brief
    required_1001: bool = True
    required_1002a: bool = True


# The verified ARDEB form tree (../references/form_structure.md).
SECTIONS: list[Section] = [
    # ÖZET and ABSTRACT are two SEPARATE blocks on the official form (one per language),
    # each capped independently — keep them split so each can be word-counted on its own.
    Section("ozet", "Özet", "ÖZET (TR) + Anahtar Kelimeler",
            "Turkish abstract (≤600 words) + Turkish keywords",
            "Bilimsel Nitelik / Özgün Değer",
            "Gap, aim, method, expected impact in one breath; ≤600 words."),
    Section("abstract", "Özet-EN", "ABSTRACT (EN) + Keywords",
            "English abstract (≤600 words) + English keywords",
            "Bilimsel Nitelik / Özgün Değer",
            "Faithful English rendering of the ÖZET; ≤600 words (counted separately)."),
    Section("ozgun_deger", "1", "ÖZGÜN DEĞER", "Original value / significance",
            "Bilimsel Nitelik / Özgün Değer",
            "The most weighted block; this is where novelty is decided."),
    Section("konu_onemi", "1.1", "Konunun Önemi ve Özgün Değer",
            "Importance & original value of the topic",
            "Bilimsel Nitelik / Özgün Değer",
            "Name the literature gap and the genuinely new contribution; cite into EK-1."),
    Section("soru_hipotez", "1.2", "Araştırma Sorusu / Hipotezi",
            "Research question / hypothesis", "Bilimsel Nitelik / Özgün Değer",
            "Sharp, falsifiable, tied to the aim."),
    Section("amac_hedefler", "1.3", "Amaç ve Hedefler", "Aim & objectives",
            "Bilimsel Nitelik / Özgün Değer",
            "One amaç; several MEASURABLE hedefler mapped 1:1 onto work packages."),
    Section("yontem", "2", "YÖNTEM", "Method", "Yöntem",
            "Design + materials + analysis; carries yapılabilirlik (feasibility)."),
    Section("proje_yonetimi", "3", "PROJE YÖNETİMİ", "Project management",
            "Proje Yönetimi ve Araştırma Olanakları",
            "Work packages, timeline, contingency, resources."),
    Section("is_paketleri", "3.1", "İş-Zaman Çizelgesi ve İş Paketleri (+ B-Planı)",
            "Work–time chart & work packages (+ contingency plan)",
            "Proje Yönetimi ve Araştırma Olanakları",
            "WPs with success criteria + İş-Zaman Çizelgesi; a B-Planı is REQUIRED."),
    Section("olanaklar", "3.2", "Araştırma Olanakları", "Research facilities/resources",
            "Proje Yönetimi ve Araştırma Olanakları",
            "Infrastructure, equipment, collaborator resources."),
    Section("yaygin_etki", "4", "YAYGIN ETKİ", "Broader impact / dissemination",
            "Yaygın Etki",
            "Populate ALL three sub-parts; thin yaygın etki is a common weakness."),
    Section("ciktilar", "4.1", "Öngörülen Çıktılar", "Expected outputs", "Yaygın Etki",
            "Publications, theses, datasets, software, patents, prototypes."),
    Section("etkiler", "4.2", "Öngörülen Etkiler / Bilim İletişimi",
            "Expected impacts / science communication", "Yaygın Etki",
            "Scientific/economic/societal effects + dissemination plan."),
    Section("kaynaklar", "EK-1", "Kaynaklar", "References",
            "Bilimsel Nitelik / Özgün Değer",
            "Cited literature; existence-check with alterlab-citation-verifier first."),
    Section("butce", "EK-2", "Bütçe ve Gerekçesi", "Budget & justification", "Yaygın Etki",
            "Itemized budget; every line tied to a work package; respect the budget cap."),
    Section("diger_projeler", "EK-3", "Diğer Projeler / TÜBİTAK Destekleri",
            "Other projects & prior TÜBİTAK support",
            "Proje Yönetimi ve Araştırma Olanakları",
            "Ongoing/recent projects for workload & duplication checks.",
            required_1001=True, required_1002a=False),
]


def _required(sec: Section, program: str) -> bool:
    return sec.required_1001 if program == "1001" else sec.required_1002a


def build_scaffold(program: str, title: str, lang: str) -> str:
    p = PROGRAMS[program]
    out: list[str] = []
    out.append(f"# {p['name']}")
    out.append(f"<!-- {p['gloss']} -->")
    if title:
        out.append("")
        out.append(f"**Proje Başlığı / Project Title:** {title}")
    out.append("")
    out.append(f"> {DISCLAIMER}")
    out.append("")
    out.append(
        f"> Program caps (verify): duration ≤ {p['max_months']} months; "
        f"budget ≤ {p['budget_cap_try']:,} TRY ({p['budget_note']}); "
        f"özet ≤ {p['ozet_word_cap']} words per language; window: {p['window']}"
        + (f"; form ≤ {p['page_limit']} pages excl. annexes." if p["page_limit"] else ".")
    )
    out.append("")
    for sec in SECTIONS:
        if not _required(sec, program):
            continue
        # The abstract sections have no numeric prefix; everything else leads with its number.
        prefix = "" if sec.number in ("Özet", "Özet-EN") else f"{sec.number}. "
        if lang == "en":
            heading = f"{prefix}{sec.en}"
        elif lang == "both":
            heading = f"{prefix}{sec.tr} — {sec.en}"
        else:  # tr (default)
            heading = f"{prefix}{sec.tr}"
        # Top-level (##) for Özet, single-digit sections, and EK-* annexes; sub-headings (###) otherwise.
        is_sub = "." in sec.number
        level = "###" if is_sub else "##"
        out.append(f"{level} {heading}")
        out.append(f"<!-- panel dimension: {sec.dimension} -->")
        out.append(f"<!-- brief: {sec.brief} -->")
        out.append("")
        out.append("_…_")
        out.append("")
    out.append("---")
    out.append(
        "Handoffs: data plan → alterlab-kvkk-dmp / alterlab-aperta; ethics → "
        "alterlab-tr-research-ethics; reference existence → alterlab-citation-verifier; "
        "generic grant-craft & Gantt → alterlab-research-grants."
    )
    return "\n".join(out) + "\n"


# ---- structure / cap check -------------------------------------------------

_WORD_RE = re.compile(r"\b[\wçğıöşüÇĞİÖŞÜ’'-]+\b", re.UNICODE)
_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_PLACEHOLDER_RE = re.compile(r"^\s*_…_\s*$", re.MULTILINE)


def _word_count(text: str) -> int:
    # Don't count scaffold annotations (<!-- brief/dimension -->) or the _…_ placeholder
    # toward the abstract word cap — only the researcher's own prose counts.
    text = _COMMENT_RE.sub(" ", text)
    text = _PLACEHOLDER_RE.sub(" ", text)
    return len(_WORD_RE.findall(text))


def _extract_block(body: str, *markers: str) -> str:
    """Return text under the first heading line containing any marker, up to the next heading."""
    lines = body.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.lstrip().startswith("#") and any(m.lower() in ln.lower() for m in markers):
            start = i + 1
            break
    if start is None:
        return ""
    chunk: list[str] = []
    for ln in lines[start:]:
        if ln.lstrip().startswith("#"):
            break
        chunk.append(ln)
    return "\n".join(chunk).strip()


def check_draft(path: str, program: str) -> dict:
    p = PROGRAMS[program]
    with open(path, encoding="utf-8") as fh:
        body = fh.read()
    low = body.lower()

    findings: list[dict] = []

    # 1) required sections present?
    missing: list[str] = []
    for sec in SECTIONS:
        if not _required(sec, program):
            continue
        # match on the Turkish heading's leading distinctive token(s)
        token = sec.tr.split("(")[0].strip()
        # use a robust contains check on a short distinctive substring
        needle = token.lower()[:18]
        if needle and needle not in low:
            # The two abstract blocks have non-numeric internal ids; show just the heading.
            label = sec.tr if sec.number in ("Özet", "Özet-EN") else f"{sec.number}. {sec.tr}"
            missing.append(label)
    if missing:
        findings.append({"level": "warn", "code": "missing-sections",
                         "detail": f"{len(missing)} required section(s) not found: " + "; ".join(missing)})

    # 2) özet word counts (TR + EN), each ≤ cap
    cap = p["ozet_word_cap"]
    tr_block = _extract_block(body, "özet")
    en_block = _extract_block(body, "summary", "abstract (en")
    tr_wc = _word_count(tr_block)
    en_wc = _word_count(en_block)
    if tr_block:
        lvl = "fail" if tr_wc > cap else "ok"
        findings.append({"level": lvl, "code": "ozet-tr-words",
                         "detail": f"Turkish özet: {tr_wc} words (cap {cap})"})
    else:
        findings.append({"level": "warn", "code": "ozet-tr-missing",
                         "detail": "No Turkish 'Özet' heading found to word-count."})
    if en_block:
        lvl = "fail" if en_wc > cap else "ok"
        findings.append({"level": lvl, "code": "ozet-en-words",
                         "detail": f"English summary: {en_wc} words (cap {cap})"})
    else:
        findings.append({"level": "warn", "code": "ozet-en-missing",
                         "detail": "No English 'Summary/Abstract' heading found to word-count."})

    # 3) duration / budget statements over the ceiling (best-effort; advisory)
    for m in re.finditer(r"(\d{1,3})\s*(?:ay|months?)\b", low):
        months = int(m.group(1))
        if months > p["max_months"]:
            findings.append({"level": "fail", "code": "duration-over",
                             "detail": f"Stated {months} months exceeds the {p['max_months']}-month ceiling."})
            break
    for m in re.finditer(r"([\d][\d.,]{4,})\s*(?:try|tl|₺)\b", low):
        digits = re.sub(r"[.,]", "", m.group(1))
        if digits.isdigit() and int(digits) > p["budget_cap_try"]:
            findings.append({"level": "fail", "code": "budget-over",
                             "detail": f"Stated {int(digits):,} TRY exceeds the {p['budget_cap_try']:,} TRY ceiling ({p['budget_note']})."})
            break

    # 4) B-Planı present?
    if "b-plan" not in low and "b planı" not in low and "b planı" not in low:
        findings.append({"level": "warn", "code": "b-plani-missing",
                         "detail": "No B-Planı (contingency plan) detected in §3 — it is a required sub-element."})

    # 5) page limit reminder (1002-A only; cannot measure pages from Markdown)
    if p["page_limit"]:
        findings.append({"level": "info", "code": "page-limit",
                         "detail": f"Reminder: the {program} form is limited to {p['page_limit']} pages excluding annexes — confirm in the rendered .doc."})

    levels = [f["level"] for f in findings]
    verdict = "FAIL" if "fail" in levels else ("REVIEW" if "warn" in levels else "OK")
    return {
        "tool": "alterlab-tubitak-proposal/scaffold_proposal.py",
        "program": p["name"],
        "verdict": verdict,
        "disclaimer": DISCLAIMER,
        "findings": findings,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--program", choices=["1001", "1002a"], default="1001",
                    help="ARDEB program variant (default: 1001)")
    ap.add_argument("--title", default="", help="Project title to stamp into the scaffold")
    ap.add_argument("--lang", choices=["tr", "en", "both"], default="tr",
                    help="Heading language (default: tr)")
    ap.add_argument("--out", help="Write the scaffold to this path (default: stdout)")
    ap.add_argument("--check", metavar="FILE",
                    help="Check an existing draft against the form structure and caps")
    ap.add_argument("--json", action="store_true", help="(--check) print JSON instead of text")
    args = ap.parse_args(argv)

    if args.check:
        report = check_draft(args.check, args.program)
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print(f"# Structure check — {report['program']}")
            print(f"Verdict: {report['verdict']}\n")
            for f in report["findings"]:
                print(f"  [{f['level'].upper()}] {f['code']}: {f['detail']}")
            print(f"\n{report['disclaimer']}")
        return 1 if report["verdict"] == "FAIL" else 0

    scaffold = build_scaffold(args.program, args.title, args.lang)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(scaffold)
        print(f"Wrote {args.program} scaffold to {args.out}")
    else:
        sys.stdout.write(scaffold)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
