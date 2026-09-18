---
name: hig-doctor-audit
description: "HIG Doctor audit workflow for scanning app projects against Apple Human Interface Guidelines. Use when the user asks for a HIG audit, Apple UI compliance scan, accessibility/design lint, HIG Doctor, severity report, CI gate, or wants to verify SwiftUI, UIKit, React, Next.js, Vue, Svelte, Angular, React Native, Flutter, Compose, Android XML, CSS, or HTML against Apple HIG rules."
---

# HIG Doctor Audit

Use this skill as the verification loop for Apple HIG work. It complements the `hig-*` reference skills: run the audit to find concrete concerns, then use the matching HIG skill and reference topic to fix them.

## Tooling

HIG Doctor is documented at <https://apple.raintree.technology> and published as `hig-doctor`.

```bash
npx hig-doctor ./path/to/project
npx hig-doctor ./path/to/project --export
npx hig-doctor ./path/to/project --stdout
npx hig-doctor ./path/to/project --json
npx hig-doctor ./path/to/project --fail-on critical
```

Requires Node 20+ for the published package. From the local source repo, the Bun entrypoint is:

```bash
cd /path/to/hig-doctor/packages/hig-doctor/src-termcast
bun run audit ./path/to/project
```

## Workflow

1. Confirm the project path and target platform/framework.
2. Run `npx hig-doctor <path> --export` for a human-readable `hig-audit.md`, or `--json` for CI/scripts.
3. If output is large, focus first on `critical`, then `serious`, then high-confidence `moderate`.
4. Map each category's `skill` field to the matching local HIG skill, such as `hig-foundations` or `hig-components-controls`.
5. Read only the specific HIG reference topics needed for the flagged issue.
6. Fix concrete code issues and rerun the audit with the same flags.
7. For CI, use `--fail-on critical` first. Raise to `serious` only after existing serious issues are cleaned up.

## Ignore File

Use `.higauditignore` for intentional fixtures, generated output, stories, or demos:

```text
**/*.stories.tsx
examples
components/audit-demo-fixtures.ts
```

Keep ignores narrow. Do not hide application UI code to make the audit pass.

## Interpretation

- `critical`: accessibility-breaking or interaction-blocking. Treat as release blockers unless clearly a false positive.
- `serious`: significant HIG or UX degradation. Fix before shipping visible UI.
- `moderate`: style or best-practice drift. Batch when the issue is repeated across a design system.
- `positive`: useful evidence, not work to do.

HIG Doctor is regex-based. Verify each finding against the code and the relevant HIG reference before editing.
