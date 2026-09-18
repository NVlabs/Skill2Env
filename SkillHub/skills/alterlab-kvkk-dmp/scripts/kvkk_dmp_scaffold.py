#!/usr/bin/env python3
"""Generate a KVKK-aligned data management plan skeleton (TR / EN / both).

Part of the AlterLab Academic Skills suite (alterlab-kvkk-dmp).

This is a DETERMINISTIC, OFFLINE template generator. It does NOT reach the
network and it makes NO legal determination — it emits a structured KVKK DMP
skeleton (grounded in the article map encoded below, sourced to Law 6698) that a
researcher then completes and a veri sorumlusu / KVKK officer signs off.

Article wording traces to Law 6698 (mevzuat.gov.tr/mevzuatmetin/1.5.6698.pdf)
and the official KVKK English translation (kvkk.gov.tr/Icerik/6649). Amendments
by Law 7499 (published in the Official Gazette 12 Mar 2024, RG No. 32487; KVKK
provisions effective 1 Jun 2024) noted where relevant. Standard library only —
runs in a bare `uv run python` environment with zero extra dependencies.

Usage:
    uv run python kvkk_dmp_scaffold.py --title "My study" \
        --basis explicit-consent --special-category health \
        --retention "5 years post-publication" --cross-border none \
        --verbis registered --lang both --out kvkk_dmp.md

    uv run python kvkk_dmp_scaffold.py --self-check   # validate the encoded map
"""
from __future__ import annotations

import argparse
import sys
from datetime import date

# --- Encoded article map (sourced to Law 6698; see references/kvkk_articles.md) ---
# Kept minimal and verifiable. Each entry: article -> (TR label, EN label).
ARTICLES: dict[str, tuple[str, str]] = {
    "5": ("Madde 5 — Kişisel verilerin işlenme şartları (açık rıza varsayılan)",
          "Art. 5 — Conditions for processing personal data (explicit consent default)"),
    "6": ("Madde 6 — Özel nitelikli kişisel veriler (sağlık/genetik/biyometrik)",
          "Art. 6 — Special categories of personal data (health/genetic/biometric)"),
    "7": ("Madde 7 — Silme, yok etme veya anonim hale getirme",
          "Art. 7 — Erasure, destruction or anonymization"),
    "9": ("Madde 9 — Yurt dışına aktarma (7499 sayılı Kanun ile değişik; RG 12 Mart 2024, yürürlük 1 Haziran 2024)",
          "Art. 9 — Transfer abroad (amended by Law 7499; Official Gazette 12 Mar 2024, in force 1 Jun 2024)"),
    "13": ("Madde 13 — Veri sorumlusuna başvuru (otuz gün)",
           "Art. 13 — Application to the data controller (thirty days)"),
    "16": ("Madde 16 — Veri Sorumluları Sicili (VERBIS)",
           "Art. 16 — Data Controllers' Registry (VERBIS)"),
    "28": ("Madde 28 — İstisnalar (28(1)(b) anonimleştirme istisnası)",
           "Art. 28 — Exceptions (28(1)(b) anonymization exemption)"),
}

# Lawful-basis options under Art. 5 / Art. 6. KVKK has NO standalone research
# basis — these are the only valid choices the scaffold offers.
BASIS_CHOICES = {
    "explicit-consent": ("Açık rıza (Madde 5/6)", "Explicit consent (Art. 5/6)"),
    "legal-obligation": ("Kanunda açıkça öngörülme / hukuki yükümlülük (Madde 5/2)",
                         "Expressly provided by law / legal obligation (Art. 5(2))"),
    "contract": ("Sözleşmenin kurulması/ifası (Madde 5/2)",
                 "Necessary for a contract (Art. 5(2))"),
    "made-public": ("İlgili kişinin alenileştirmesi (Madde 5/2)",
                    "Data made public by the data subject (Art. 5(2))"),
    "legitimate-interest": ("Meşru menfaat (Madde 5/2)",
                            "Legitimate interest (Art. 5(2))"),
    "anonymized-exempt": ("Anonim — kapsam dışı (Madde 28(1)(b))",
                          "Anonymized — out of scope (Art. 28(1)(b))"),
}

SPECIAL_CATEGORIES = ("none", "health", "genetic", "biometric", "other")
CROSS_BORDER = ("none", "adequacy-decision", "standard-contract", "other-safeguard")
VERBIS_STATUS = ("registered", "exempt", "pending", "unknown")
LANGS = ("tr", "en", "both")


def _v(value: str, default: str = "[doldurun / fill in]") -> str:
    return value if value else default


def build_tr(args: argparse.Namespace) -> str:
    basis_tr = BASIS_CHOICES[args.basis][0]
    sc = args.special_category
    sc_line = ("Yok" if sc == "none"
               else f"{sc} (Madde 6 — yeterli önlemler gerekli)")
    cb = args.cross_border
    cb_line = ("Yurt dışı aktarım yok (yalnızca Türkiye)" if cb == "none"
               else f"Mekanizma: {cb} (Madde 9)")
    return f"""# Veri Yönetim Planı (KVKK — 6698 sayılı Kanun)

> Otomatik iskelet — hukuki görüş değildir. Veri sorumlusu / KVKK uyum
> görevlisi onayı gereklidir. 7499 sayılı Kanun (RG 12 Mart 2024; KVKK
> hükümleri 1 Haziran 2024'te yürürlüğe girdi) değişikliklerine karşı güncelliği
> teyit edin. Oluşturulma: {date.today().isoformat()}

## 1. Proje
- Başlık: {_v(args.title)}
- Sorumlu / kurum: [doldurun]

## 2. Veri kategorileri
- Kişisel veriler: [liste]
- Özel nitelikli veriler (Madde 6): {sc_line}
- Tanımlanabilir mi? Anonimleştirilecek mi? [doldurun]

## 3. Hukuki dayanak (Madde 5 / 6)
- Dayanak: {basis_tr}
- (KVKK'da bağımsız "bilimsel araştırma" dayanağı YOKTUR.)
- Özel nitelikli ise yeterli önlemler: [erişim kontrolü, şifreleme, ...]

## 4. Anonimleştirme (Madde 28(1)(b))
- Teknik(ler): [maskeleme / genelleştirme / k-anonimlik ...]
- Yeniden tanımlanabilirlik risk değerlendirmesi: [özet]
- İstisna kapsamı: [analiz veri seti / açık veri]

## 5. Saklama ve imha (Madde 7)
- Saklama süresi: {_v(args.retention)}
- Yöntem: [silme / yok etme / anonim hale getirme]

## 6. İlgili kişi hakları (Madde 13)
- İletişim noktası: [doldurun]
- Yanıt süresi: en geç otuz (30) gün

## 7. Yurt dışı aktarım (Madde 9)
- {cb_line}

## 8. VERBIS (Madde 16)
- Durum: {args.verbis}

## 9. Notlar
- Funder VYP / Aperta: alterlab-aperta
- Etik kurul: alterlab-tr-research-ethics
- KVKK Madde 18 idari para cezaları her Ocak ayında yeniden değerleme oranıyla
  güncellenir — güncel tutarı teyit edin.
"""


def build_en(args: argparse.Namespace) -> str:
    basis_en = BASIS_CHOICES[args.basis][1]
    sc = args.special_category
    sc_line = ("None" if sc == "none"
               else f"{sc} (Art. 6 — adequate measures required)")
    cb = args.cross_border
    cb_line = ("No transfer abroad (Türkiye only)" if cb == "none"
               else f"Mechanism: {cb} (Art. 9)")
    return f"""# Data Management Plan (KVKK — Law No. 6698)

> Auto-generated skeleton — NOT legal advice. Requires veri sorumlusu / KVKK
> officer sign-off. Verify currency against Law 7499 amendments (Official Gazette
> 12 Mar 2024; KVKK provisions effective 1 Jun 2024).
> Generated: {date.today().isoformat()}

## 1. Project
- Title: {_v(args.title)}
- PI / institution: [fill in]

## 2. Data categories
- Personal data: [list]
- Special-category data (Art. 6): {sc_line}
- Identifiable? To be anonymized? [fill in]

## 3. Lawful basis (Art. 5 / 6)
- Basis: {basis_en}
- (KVKK has NO standalone "scientific research" lawful basis.)
- If special category, adequate measures: [access control, encryption, ...]

## 4. Anonymization (Art. 28(1)(b))
- Technique(s): [masking / generalization / k-anonymity ...]
- Re-identification-risk assessment: [summary]
- Exemption claimed for: [analytic dataset / open deposit]

## 5. Retention & destruction (Art. 7)
- Retention period: {_v(args.retention)}
- Method: [erase / destroy / anonymize]

## 6. Data-subject rights (Art. 13)
- Contact point: [fill in]
- Response window: thirty (30) days at the latest

## 7. Cross-border transfer (Art. 9)
- {cb_line}

## 8. VERBIS (Art. 16)
- Status: {args.verbis}

## 9. Notes
- Funder VYP / Aperta deposit: alterlab-aperta
- Ethics committee (etik kurul): alterlab-tr-research-ethics
- KVKK Art. 18 administrative fines are revalued every January by the Tax
  Procedure Law rate — verify the current-year figure.
"""


def self_check() -> int:
    """Validate the encoded article map and choice tables; no network."""
    problems: list[str] = []
    required = {"5", "6", "7", "9", "13", "16", "28"}
    if set(ARTICLES) != required:
        problems.append(f"ARTICLES keys {set(ARTICLES)} != required {required}")
    for k, v in ARTICLES.items():
        if not (isinstance(v, tuple) and len(v) == 2 and all(v)):
            problems.append(f"Article {k} label malformed: {v!r}")
    if "explicit-consent" not in BASIS_CHOICES:
        problems.append("explicit-consent must be a valid basis (KVKK default)")
    if "anonymized-exempt" not in BASIS_CHOICES:
        problems.append("anonymized-exempt (Art. 28) lever missing")
    # Guard against accidentally inventing a 'research' basis (KVKK has none).
    for key in BASIS_CHOICES:
        if "research" in key.lower():
            problems.append(f"invalid 'research' basis present: {key} (KVKK has none)")
    if problems:
        for p in problems:
            print(f"FAIL: {p}", file=sys.stderr)
        return 1
    print(f"OK: {len(ARTICLES)} articles, {len(BASIS_CHOICES)} bases encoded; "
          "no fabricated research basis.")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--title", default="", help="Project title")
    p.add_argument("--basis", choices=sorted(BASIS_CHOICES), default="explicit-consent",
                   help="Lawful basis under Art. 5/6 (KVKK has no research basis)")
    p.add_argument("--special-category", choices=SPECIAL_CATEGORIES, default="none",
                   help="Special-category data type (Art. 6)")
    p.add_argument("--retention", default="", help="Retention period text")
    p.add_argument("--cross-border", choices=CROSS_BORDER, default="none",
                   help="Cross-border transfer mechanism (Art. 9)")
    p.add_argument("--verbis", choices=VERBIS_STATUS, default="unknown",
                   help="VERBIS registration status (Art. 16)")
    p.add_argument("--lang", choices=LANGS, default="both", help="Output language")
    p.add_argument("--out", default="", help="Output path (default: stdout)")
    p.add_argument("--self-check", action="store_true",
                   help="Validate the encoded article map and exit")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.self_check:
        return self_check()
    parts: list[str] = []
    if args.lang in ("tr", "both"):
        parts.append(build_tr(args))
    if args.lang in ("en", "both"):
        parts.append(build_en(args))
    out = "\n\n---\n\n".join(parts)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(out)
        print(f"Wrote {args.out} ({args.lang}).", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
