# `skills/great_cto/templates/` — mandatory artefact templates

> One template per compliance / technical artefact required by `architect.md`, `senior-dev.md`, `qa-engineer.md` hard halts (v1.0.131 + v1.0.132).
> Agents read these to know what shape an artefact should have. Users copy them into project repos under `docs/compliance/`, `docs/architecture/`, `docs/sec-threats/`, `tests/eval/`, or `docs/decisions/`.

## When each template gets copied

| Trigger | Template | Destination in project repo |
|---|---|---|
| `archetype: ai-system | agent-product` | `ARCH-ai.md` | `docs/architecture/ARCH-{slug}.md` |
| `archetype: game` | `ARCH-game.md` | `docs/architecture/ARCH-{slug}.md` |
| `archetype: browser-extension` | `ARCH-browser-extension.md` | `docs/architecture/ARCH-{slug}.md` |
| `archetype: web3` (defi / bridge / lending / dex) | `ARCH-defi-protocol.md` | `docs/architecture/ARCH-{slug}.md` |
| All other archetypes (web-service / library / mobile-app / data-platform / infra) | `ARCH-default.md` | `docs/architecture/ARCH-{slug}.md` |
| `archetype: ai-system | agent-product` | `THREAT-MODEL-AI.md` | `docs/sec-threats/TM-{slug}.md` |
| `archetype: browser-extension` | `THREAT-MODEL-AI.md` (adapted by web-store-reviewer) | `docs/sec-threats/TM-{slug}.md` |
| `archetype: ai-system | agent-product` | `EVAL-template.md` (×3 or ×5) | `tests/eval/EVAL-{scenario}.md` |
| AI / agent project picks LLM | `ADR-LLM.md` | `docs/decisions/ADR-{NN}-LLM-{model}.md` |
| AI / agent project writes prompt | `ADR-PROMPT.md` | `docs/decisions/ADR-{NN}-PROMPT-{name}.md` |
| `compliance: [dora]` | `DORA-ICT-risk-assessment.md` + `DORA-third-party-register.md` | `docs/compliance/` |
| `compliance: [nis2]` | `NIS2-article21-controls.md` | `docs/compliance/` |
| `compliance: [gxp]` or `[21cfr11]` | `21CFR11-checklist.md` | `docs/compliance/` |
| `compliance: [tisax]` | `TISAX-VDA-ISA-results.md` | `docs/compliance/` |
| `compliance: [iso27001]` | `ISO27001-SoA.md` | `docs/compliance/` |
| `compliance: [sox]` | `SOX-ITGC-checklist.md` | `docs/compliance/` |
| `compliance: [pci-dss-saq-a]` | `PCI-DSS-SAQ-A.md` | `docs/compliance/` |
| `compliance: [pci-dss]` (full scope) | `PCI-DSS-SAQ-D.md` | `docs/compliance/` |
| every senior-dev task (pm Step 7b) | `IMPL-BRIEF-template.md` (×N, one per task) | `docs/impl-briefs/IMPL-BRIEF-{task-id}.md` |
| `/audit` or `/migrate` finds gate gaps in a legacy repo | `GAP-REGISTER-template.yaml` + `GAP-WAVE-PLAN-template.yaml` | `docs/governance/` |

## How agents use these

`architect.md` SECURITY_REQUIRED block (v1.0.132) checks for the destination artefact and exits 1 if missing. If the user says "I don't know what shape this should take", architect points them at the matching template.

`senior-dev.md` Step 0b uses `## Security` section in ARCH and the `TM-*.md` file to inform implementation rules. Both come from these templates.

`qa-engineer.md` Step 0b validates `tests/eval/EVAL-*.md` count against archetype thresholds — `EVAL-template.md` is what each scenario file looks like.

`project-auditor.md` Phase 4 (planned v1.0.133) reads `monthly-budget-llm-usd` from PROJECT.md and the `## Cost Model` section of `ARCH-ai.md` to detect cost-cap violations.

`pm.md` Step 7b emits one `IMPL-BRIEF-{task-id}.md` per task (governance Phase 3) — files-to-modify / files-NOT-to-modify / API-CONTRACT / TEST-SPEC / ACCEPTANCE. `senior-dev.md` Step 4 reads it before coding and Step 6b runs `node scripts/lib/impl-brief.mjs check <brief> <changed-files…>` to refuse a commit that touches a denylisted file. `validate` / `check` make the brief machine-enforceable, not just prose.

`/audit` and `/migrate` emit `GAP-REGISTER.yaml` + `GAP-WAVE-PLAN.yaml` (governance Phase 5) when a legacy repo would fail strict-mode gates cold. `scripts/lib/gap-waves.mjs plan` schedules gaps into waves (criticals first) and prints the interim `/exception create` commands that keep gates green while each deferred gap stays tracked + expiring — the sanctioned path from "fails every strict gate" to "fully gated".

## What's NOT in this directory

- ARCH templates for non-AI archetypes (web-service, mobile-app, library, …) — `architect.md` has these inline because they're rarely customised
- Threat model template for traditional surface (STRIDE) — `/sec threat` already generates this
- Code-review checklists — `/review` 12-angle is built in
- Per-pack templates (game-pack `## Performance budget` section, web3-pack `## Upgradeability matrix`) — those live inside the pack files in `skills/great_cto/packs/`

## Updating templates

Templates ship with the plugin. To customise:
1. Copy template into your project repo at the destination path
2. Edit freely — your copy survives plugin upgrades
3. If you find a structural improvement that benefits all users, open a PR against `skills/great_cto/templates/`
