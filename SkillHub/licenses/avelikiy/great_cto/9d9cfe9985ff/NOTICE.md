# Third-Party Attribution

`great_cto` bundles, adapts, or references work from the projects below. The
original license of each work is preserved; see the specific files for full
terms.

## agent-style (yzhao062/agent-style)

- Upstream: https://github.com/yzhao062/agent-style (pinned v0.3.1)
- Upstream license: CC-BY-4.0 (documentation / rules) and MIT (enforcement lists)
- Adapted files in this repo:
  - `skills/great_cto/prose-style.md` — subset of 7 rules from upstream `RULES.md`
    (CC-BY-4.0). Directive text and one BAD/GOOD pair per rule adapted;
    rationale condensed for agent-context budget. Upstream carries 5+ examples
    per rule and per-source citations (Strunk & White, Orwell, Pinker, Gopen &
    Swan) — consult upstream for the full blocks.
  - `enforcement/prose-deny.txt` — reference-only subset of upstream
    `enforcement/deny-phrases.txt` (MIT). Trimmed to phrases that fire in
    great_cto agent output (audit findings, QA/CSO reports, CHANGELOG). The
    file is a human-readable reference; the mechanical warn-grep in
    `agents/qa-engineer.md` inlines a smaller curated pattern list.

Applied rules: RULE-01 (curse of knowledge), RULE-03 (abstract vs concrete),
RULE-04 (needless words), RULE-05 (dying metaphors), RULE-08 (claim
calibration), RULE-A (bullet overuse), RULE-H (citation discipline for
factual claims).

## ui-ux-pro-max (nextlevelbuilder/ui-ux-pro-max-skill)

- Upstream: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- Upstream license: MIT (preserved at `skills/ui-ux-pro-max/LICENSE`)
- Vendored files in this repo (`skills/ui-ux-pro-max/`):
  - `SKILL.md` — design-intelligence skill (50+ styles, 161 palettes, 99 UX
    guidelines, 161 product types) covering landing pages, dashboards, admin
    panels, and mobile apps across React/Next/Vue/Svelte/SwiftUI/React Native/
    Flutter/Tailwind/shadcn.
  - `data/` — the CSV knowledge base (`landing.csv`, `app-interface.csv` with
    iOS/Android/React Native rules, `styles.csv`, `ux-guidelines.csv`, etc.).
  - `scripts/` — the design-system generator / search helpers (Python).
  - Trimmed: upstream `cli/`, `screenshots/`, `preview/`, marketing README, and
    the sibling skills (`design`, `banner-design`, `slides`, …) were not vendored.
    `data`/`scripts` symlinks were dereferenced to real files.
- Mounted by: `agents/design-advisor.md` (design planning).

## anydesign (uxKero/anydesign)

- Upstream: https://github.com/uxKero/anydesign
- Upstream license: MIT (preserved at `skills/anydesign/LICENSE`)
- Vendored files in this repo (`skills/anydesign/`):
  - `SKILL.md`, `scripts/`, `references/`, `requirements.txt` — analyze an image /
    URL / Figma file and emit a structured `design.md` (token system + component
    inventory + reconstruction notes) for building UI to a reference.
  - Trimmed: upstream `examples/` (~2.6 MB) and README/CHANGELOG were not vendored.
- Mounted by: `agents/design-advisor.md` (reverse-engineering a design reference).
