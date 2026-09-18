#!/usr/bin/env python3
"""Scaffold a TÜBİTAK Veri Yönetim Planı (VYP) / data management plan.

Emits a bilingual (TR/EN) data-management-plan skeleton following the section
tree documented in references/vyp_template.md, which mirrors the data-lifecycle
structure required by the TÜBİTAK Açık Bilim Politikası (Open Science Policy).

This is a *scaffold generator*, not a submission tool. It does NOT contact
TÜBİTAK, Aperta, or any network service — it only writes Markdown. It also does
NOT perform any KVKK lawful-basis or anonymisation analysis; for that, run the
alterlab-kvkk-dmp skill and paste its conclusion into sections 4 and 6.

Stdlib only. Run via uv:

    uv run python scripts/vyp_scaffold.py --project "Proje adı" --field stem \\
        --lang both --data-closed --closed-reason kvkk --out vyp.md

Always remind the user to verify the current required VYP structure and the
embargo ceilings against the live TÜBİTAK application before submission.
"""
from __future__ import annotations

import argparse
import datetime
import sys

# Embargo ceilings from the TÜBİTAK Open Science Policy (see
# references/policy_mandates.md). These are *upper bounds*; immediate open access
# is always allowed and preferred.
EMBARGO = {
    "stem": ("Fen ve mühendislik bilimleri (STEM)", "6 ay / 6 months"),
    "ssh": ("Sosyal ve beşeri bilimler (SSH)", "12 ay / 12 months"),
}

# İlke-6 closed-data justification stubs (the *reason*, not a KVKK analysis).
CLOSED_REASON = {
    "kvkk": (
        "KVKK (6698 sayılı Kanun) kapsamında kişisel/özel nitelikli veri olduğu için.",
        "Personal / special-category data under KVKK (Law 6698). "
        "NOTE: obtain the lawful-basis and anonymisation determination from "
        "alterlab-kvkk-dmp and paste its conclusion here.",
    ),
    "commercial": (
        "Ticari gizlilik / fikrî mülkiyet nedeniyle.",
        "Commercial confidentiality / intellectual property.",
    ),
    "security": (
        "Güvenlik / ulusal çıkar kısıtı nedeniyle.",
        "Security / national-interest restriction.",
    ),
    "ethics": (
        "Etik kurul kararıyla getirilen paylaşım kısıtı nedeniyle.",
        "Sharing restriction imposed by an ethics committee (etik kurul) decision.",
    ),
}

# Section tree: (number, Turkish heading, English heading, TR prompt, EN prompt).
SECTIONS = [
    (1, "Veri Toplama ve Üretme", "Data Collection & Generation",
     "Projede hangi veriler üretilecek/toplanacak? Tür, kaynak, hacim ve yöntem.",
     "What data will the project create/collect? Types, sources, volume, methods."),
    (2, "Veri Formatları ve Standartları", "Formats & Standards",
     "Dosya formatları, üst veri (metadata) standartları, adlandırma kuralları.",
     "File formats, metadata standards, naming conventions, documentation."),
    (3, "Veri Depolama ve Yedekleme", "Storage & Backup",
     "Proje süresince veri nerede saklanacak? Yedekleme, erişim denetimi, güvenlik.",
     "Where data lives during the project; backup; access control; security."),
    (4, "Yasal ve Etik Hususlar", "Legal & Ethical Considerations",
     "KVKK dayanağı, kişisel/özel nitelikli veri, etik kurul onayı, onam. "
     "(Karar için alterlab-kvkk-dmp ve alterlab-tr-research-ethics.)",
     "KVKK lawful basis, personal/special-category data, ethics approval, consent. "
     "(Get the decision from alterlab-kvkk-dmp and alterlab-tr-research-ethics.)"),
    (5, "Veri Paylaşımı ve Erişim", "Sharing & Access",
     "Hangi veri açık, hangisi kısıtlı paylaşılacak? Depo: Aperta. Ambargo tavanı: {embargo}.",
     "What is shared openly vs restricted. Repository: Aperta. Embargo ceiling: {embargo}."),
    (6, "Kapalı Veri Gerekçesi (İlke-6)", "Closed-Data Justification (Principle 6)",
     "Kapalı kalan veri varsa belgelenmiş gerekçe, kısıtlı erişim planı, kimlerin erişebileceği.",
     "If any data stays closed: documented reason, restricted-access plan, who may request access."),
    (7, "Uzun Süreli Saklama ve Koruma", "Long-Term Preservation",
     "Saklama süresi; proje sonrası koruma; silme/anonimleştirme planı.",
     "Retention period; preservation after project end; deletion/anonymisation plan."),
    (8, "Sorumluluklar ve Kaynaklar", "Roles & Resources",
     "Veri yönetiminden kim sorumlu? Gerekli kaynaklar/maliyetler.",
     "Who is responsible for data management; resources/costs."),
]

DISCLAIMER_TR = (
    "> Bu bir taslaktır. Ambargo tavanlarını ve gerekli VYP yapısını başvurudan "
    "önce güncel TÜBİTAK Açık Bilim Politikası ve canlı başvuru sistemiyle "
    "doğrulayın."
)
DISCLAIMER_EN = (
    "> This is a scaffold. Verify the embargo ceilings and the required VYP "
    "structure against the current TÜBİTAK Open Science Policy and the live "
    "application system before submitting."
)


def _closed_block(reason_key: str, lang: str) -> str:
    tr, en = CLOSED_REASON[reason_key]
    if lang == "tr":
        return f"Gerekçe: {tr}\n\nKısıtlı erişim (açık üst veri) önerilir."
    if lang == "en":
        return f"Reason: {en}\n\nUse restricted access with open metadata."
    return f"Gerekçe / Reason: {tr}\n\n{en}\n\nKısıtlı erişim / restricted access with open metadata."


def build(project: str, field: str, lang: str, data_closed: bool,
          closed_reason: str) -> str:
    field_label, embargo = EMBARGO[field]
    today = datetime.date.today().isoformat()
    out: list[str] = []

    title = "Veri Yönetim Planı (VYP) / Data Management Plan"
    out.append(f"# {title}")
    out.append("")
    out.append(f"- **Proje / Project:** {project}")
    out.append(f"- **Alan / Field:** {field_label}")
    out.append(f"- **Ambargo tavanı / Embargo ceiling:** {embargo} (üst sınır / upper bound)")
    out.append(f"- **Depo / Repository:** Aperta — https://aperta.ulakbim.gov.tr/")
    out.append(f"- **Tarih / Date:** {today}")
    out.append("")

    for num, tr_h, en_h, tr_p, en_p in SECTIONS:
        if lang == "tr":
            out.append(f"## {num}. {tr_h}")
            out.append("")
            out.append(tr_p.format(embargo=embargo))
        elif lang == "en":
            out.append(f"## {num}. {en_h}")
            out.append("")
            out.append(en_p.format(embargo=embargo))
        else:
            out.append(f"## {num}. {tr_h} / {en_h}")
            out.append("")
            out.append(tr_p.format(embargo=embargo))
            out.append("")
            out.append(en_p.format(embargo=embargo))
        out.append("")
        # Section 6: inject the İlke-6 justification when data is closed.
        if num == 6:
            if data_closed:
                out.append(_closed_block(closed_reason, lang))
            else:
                msg_tr = "Tüm veriler açık olarak paylaşılacaktır; kapalı veri yoktur."
                msg_en = "All data will be shared openly; no closed data."
                out.append({"tr": msg_tr, "en": msg_en}.get(lang, f"{msg_tr} / {msg_en}"))
            out.append("")

    if lang == "tr":
        out.append(DISCLAIMER_TR)
    elif lang == "en":
        out.append(DISCLAIMER_EN)
    else:
        out.append(DISCLAIMER_TR)
        out.append("")
        out.append(DISCLAIMER_EN)
    out.append("")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--project", required=True, help="Project name / Proje adı")
    p.add_argument("--field", choices=["stem", "ssh"], default="stem",
                   help="Field bucket; sets the embargo ceiling (6 mo STEM / 12 mo SSH)")
    p.add_argument("--lang", choices=["tr", "en", "both"], default="both",
                   help="Output language")
    p.add_argument("--data-closed", action="store_true",
                   help="Some data must stay closed; inject an İlke-6 justification")
    p.add_argument("--closed-reason", choices=list(CLOSED_REASON),
                   default="kvkk", help="Reason for closure (used with --data-closed)")
    p.add_argument("--out", help="Write to this path instead of stdout")
    args = p.parse_args(argv)

    doc = build(args.project, args.field, args.lang, args.data_closed,
                args.closed_reason)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(doc)
        print(f"Wrote VYP scaffold to {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(doc)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
