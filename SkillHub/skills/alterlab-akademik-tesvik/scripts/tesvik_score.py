#!/usr/bin/env python3
"""tesvik_score.py — Akademik Teşvik (academic-incentive) score calculator.

Computes the annual Turkish academic-incentive (akademik teşvik) score for a
Devlet (state) university öğretim elemanı (academic staff member) from a list of
research activities, applying the rules of the Akademik Teşvik Ödeneği
Yönetmeliği (Bakanlar Kurulu 14/5/2018 No. 2018/11834; RG 27/6/2018 No. 30461;
amended CK-2043 of 17/1/2020). All ceilings and coefficients below are
transcribed from that regulation's Faaliyet Hesaplama Tablosu (Tablo 4) and the
k/p/r tables (Tablo 1/2/3). See ../references/tablo4.md for source provenance.

It is DETERMINISTIC and OFFLINE: it does no network I/O and uses only the
stdlib, so the same input always yields the same verdict. It scores a list of
already-classified activities; it does NOT classify a CV or fetch publications.

REGULATION ALGORITHM (MADDE 8/2). The official method has TWO steps and NO
dynamic "rescale each type to 30% of the gross" pass:

  8/2(a) Per activity, the regulation row supplies an `oran` (a percentage-style
         multiplier, e.g. a Q1 SSCI research article = k x p x 0.60; a TÜBİTAK
         1001 yürütücü = r x 0.80; yurt içi araştırma = 0.10 x months). Each
         activity TYPE's puanı = (Σ of that type's faaliyet oranları) x the
         type's headline puan ("akademik faaliyet türü için belirlenmiş puan").
  8/2(b) The akademik teşvik puanı = Σ of all type puanları.

  8/3   Each type puanı cannot exceed its headline puan; the total cannot
         exceed 100. (These per-type ceilings are how the regulation encodes the
         %30 weighting from MADDE 1 — the %30 is a fixed table-DESIGN constraint
         on the ceilings, not a per-run reduction. There is no runtime
         "30% of computed gross" rescaling step in the regulation.)

  10/3  Net-30 gate: the incentive is payable only if the final puan >= 30
         ("akademik teşvik puanının en az otuz olması gerekir", MADDE 10/3 —
         "Diğer hükümler"). Below 30, no payment regardless of activity volume.

INPUT MODEL. This script takes the per-activity `oran` directly, because the
oran is the regulation's actual unit of account and the per-row oran formulas
are field-dependent (A1–A4 columns) and too numerous to hardcode safely. For
each activity supply:
  type   (required) one of the nine canonical türler (Turkish spelling OK).
  oran   (required) the regulation row's computed oran for that activity, i.e.
         the value of cells like "k x p x 60" / "r x 80" / "15 x ay" EXPRESSED
         AS A FRACTION OF THE HEADLINE PUAN. Concretely: take the table cell,
         treat the trailing integer as a percentage, and apply k/p/r/months.
         Examples (headline puan in parentheses):
           Q1 SSCI research article, 2 authors  -> k=0.8, p=1.0, cell=60
                oran = 0.8 * 1.0 * 0.60 = 0.48            (YAYIN, 30 puan)
           TÜBİTAK 1001 yürütücü (A1)            -> r=1.0, cell=80
                oran = 1.0 * 0.80 = 0.80                  (PROJE, 20 puan)
           Yurt içi araştırma, 6 months         -> cell = "10 x ay"
                oran = 0.10 * 6 = 0.60                    (ARAŞTIRMA, 15 puan)
           1 citation in an SCI article         -> cell = 8
                oran = 0.08                               (ATIF, 30 puan)
  count  (optional) integer multiplier for identical repeated activities
         (e.g. number of citations of the same kind). Default 1.
  label  (optional) human description (passed through to the report).

So a TYPE's puanı = headline x Σ(oran x count), capped at the headline (8/3).

This script reports the score and the gate verdict. It does NOT compute the TRY
payout (that depends on the current memur aylık katsayısı, which changes every
six months and is intentionally NOT hardcoded — see references).

Usage:
    uv run python tesvik_score.py activities.json
    uv run python tesvik_score.py -            # read JSON from stdin
    echo '[...]' | uv run python tesvik_score.py - --json
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field

# --- Verified constants (Akademik Teşvik Ödeneği Yönetmeliği, ekli Tablo 4) ---

# Per-type headline puan ("akademik faaliyet türü için belirlenmiş olan puan"),
# from the Faaliyet Hesaplama Tablosu headers, e.g. "PROJE (20 puan)",
# "YAYIN (30 puan)". This is BOTH the multiplier in türü puanı = Σ(oran) x puan
# AND the per-type ceiling enforced by MADDE 8/3. Keys are ASCII-folded for
# input robustness; canonical Turkish names live in references/tablo4.md.
TYPE_HEADLINE: dict[str, int] = {
    "proje": 20,       # PROJE (20 puan)
    "arastirma": 15,   # ARAŞTIRMA (15 puan)
    "yayin": 30,       # YAYIN (30 puan)
    "tasarim": 15,     # TASARIM (15 puan)
    "sergi": 15,       # SERGİ (15 puan)
    "patent": 30,      # PATENT (30 puan)
    "atif": 30,        # ATIF (30 puan)
    "teblig": 20,      # TEBLİĞ (20 puan)
    "odul": 20,        # ÖDÜL (20 puan)
}

SCORE_CAP = 100   # total akademik teşvik puanı cannot exceed 100 (MADDE 8/3)
NET_GATE = 30     # incentive payable only if final puan >= 30 (MADDE 10/3)

# ASCII-folding for Turkish input keys so "Yayın", "yayin", "YAYIN" all match.
_FOLD = str.maketrans({
    "ı": "i", "İ": "i", "ş": "s", "Ş": "s", "ğ": "g", "Ğ": "g",
    "ç": "c", "Ç": "c", "ö": "o", "Ö": "o", "ü": "u", "Ü": "u",
})


def fold(s: str) -> str:
    return s.translate(_FOLD).strip().lower()


@dataclass
class TypeResult:
    type: str
    headline: float = 0.0          # type headline puan (also the MADDE 8/3 cap)
    oran_sum: float = 0.0          # Σ of this type's faaliyet oranları x count
    raw: float = 0.0               # headline x oran_sum (before the 8/3 cap)
    final: float = 0.0             # min(raw, headline) — after MADDE 8/3 cap
    capped_at_ceiling: bool = False
    activities: list[dict] = field(default_factory=list)


@dataclass
class Report:
    per_type: list[TypeResult]
    gross: float              # Σ of per-type final puanları (before 100 cap)
    final_score: float        # after the 100 cap
    capped_at_100: bool
    payable: bool             # net-30 gate (MADDE 10/3)
    warnings: list[str] = field(default_factory=list)


def _activity_oran(act: dict) -> float:
    """Per-activity oran x count. `oran` is the regulation row value expressed
    as a fraction of the type headline (see module docstring)."""
    oran = float(act.get("oran", 0))
    count = float(act.get("count", 1))
    return oran * count


def score(activities: list[dict]) -> Report:
    warnings: list[str] = []
    by_type: dict[str, TypeResult] = {}

    for act in activities:
        raw_type = str(act.get("type", "")).strip()
        key = fold(raw_type)
        if key not in TYPE_HEADLINE:
            warnings.append(
                f"Unknown activity type {raw_type!r}; recognised types: "
                + ", ".join(sorted(TYPE_HEADLINE)) + ". Activity skipped."
            )
            continue
        if "oran" not in act:
            warnings.append(
                f"Activity {act.get('label', raw_type)!r} has no 'oran' field; "
                "supply the regulation row's oran as a fraction of the headline "
                "(see references/hesaplama.md). Treated as oran=0."
            )
        tr = by_type.setdefault(
            key, TypeResult(type=key, headline=TYPE_HEADLINE[key])
        )
        o = _activity_oran(act)
        tr.oran_sum += o
        tr.activities.append({**act, "_oran_contrib": round(o, 6)})

    # MADDE 8/2(a): türü puanı = Σ(oran) x headline. MADDE 8/3: cap at headline.
    for tr in by_type.values():
        tr.raw = tr.headline * tr.oran_sum
        tr.final = min(tr.raw, tr.headline)
        if tr.raw > tr.headline:
            tr.capped_at_ceiling = True
            warnings.append(
                f"Type '{tr.type}' hit its headline ceiling (MADDE 8/3): "
                f"{tr.raw:.2f} -> {tr.final:.2f} (tavan {tr.headline:g})."
            )

    # MADDE 8/2(b) + 8/3: total puan, capped at 100.
    gross = sum(tr.final for tr in by_type.values())
    final_score = min(gross, SCORE_CAP)
    capped_100 = gross > SCORE_CAP

    # MADDE 10/3: net-30 gate.
    payable = final_score >= NET_GATE
    if not payable:
        warnings.append(
            f"Net-30 gate NOT met: final score {final_score:.2f} < {NET_GATE}. "
            "No incentive is payable for this year (MADDE 10/3)."
        )

    per_type = sorted(by_type.values(), key=lambda t: t.type)
    return Report(
        per_type=per_type,
        gross=round(gross, 4),
        final_score=round(final_score, 4),
        capped_at_100=capped_100,
        payable=payable,
        warnings=warnings,
    )


def report_to_dict(r: Report) -> dict:
    return {
        "tool": "alterlab-akademik-tesvik/tesvik_score.py",
        "regulation": "Akademik Teşvik Ödeneği Yönetmeliği (2018/11834, am. 2020)",
        "final_score": r.final_score,
        "capped_at_100": r.capped_at_100,
        "net_30_gate_met": r.payable,
        "payable": r.payable,
        "gross_before_100_cap": r.gross,
        "per_type": [
            {
                "type": t.type,
                "headline_puan": t.headline,
                "oran_sum": round(t.oran_sum, 6),
                "raw_puan": round(t.raw, 4),
                "final_puan": round(t.final, 4),
                "capped_at_headline": t.capped_at_ceiling,
                "n_activities": len(t.activities),
            }
            for t in r.per_type
        ],
        "warnings": r.warnings,
        "notes": [
            "türü puanı = Σ(faaliyet oranları) x type headline puan (MADDE 8/2a);"
            " capped at the headline and the 100 total (MADDE 8/3). The %30 from"
            " MADDE 1 is a fixed table-design weight (it sets the ceilings), NOT"
            " a per-run rescaling step.",
            "Net-30 gate is MADDE 10/3 ('Diğer hükümler').",
            "Score only. TRY payout = (kadro orani) x (score/100) x [(1500+8000)"
            " x memur aylik katsayisi] (MADDE 8/1); the katsayi is NOT hardcoded"
            " (changes every 6 months) — verify the current value before quoting.",
            "Applies to Devlet (state) higher-education staff only.",
        ],
    }


def render_text(r: Report) -> str:
    lines = []
    lines.append("Akademik Teşvik — annual score")
    lines.append("=" * 48)
    for t in r.per_type:
        flag = "  [tavan]" if t.capped_at_ceiling else ""
        lines.append(
            f"  {t.type:<10} Σoran={t.oran_sum:7.4f}  headline={t.headline:<3g}"
            f"  raw={t.raw:6.2f}  final={t.final:6.2f}  (n={len(t.activities)}){flag}"
        )
    lines.append("-" * 48)
    lines.append(f"  Gross (before 100 cap): {r.gross:.2f}")
    lines.append(
        f"  FINAL SCORE: {r.final_score:.2f}"
        + ("  [capped at 100]" if r.capped_at_100 else "")
    )
    gate = "PAYABLE (>= 30)" if r.payable else "NOT PAYABLE (< 30)"
    lines.append(f"  Net-30 gate (MADDE 10/3): {gate}")
    if r.warnings:
        lines.append("-" * 48)
        lines.append("  Warnings:")
        for w in r.warnings:
            lines.append(f"   - {w}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Akademik Teşvik score calculator.")
    ap.add_argument("input", help="Path to activities JSON, or '-' for stdin.")
    ap.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    args = ap.parse_args(argv)

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    try:
        activities = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"error: input is not valid JSON: {e}", file=sys.stderr)
        return 2
    if not isinstance(activities, list):
        print("error: input JSON must be a list of activity objects.", file=sys.stderr)
        return 2

    rep = score(activities)
    if args.json:
        print(json.dumps(report_to_dict(rep), ensure_ascii=False, indent=2))
    else:
        print(render_text(rep))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
