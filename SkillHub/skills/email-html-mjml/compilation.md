# MJML Compilation Reference

---

## Hard Rules

1. **No global install** — Never run `npm install -g mjml`. If missing, suggest `npm install -D mjml`.
2. **Use npx or relative path** — `npx mjml` or `./node_modules/.bin/mjml`. Never assume global `$PATH`.
3. **Verify source first** — Check that the `.mjml` file exists and contains valid XML before compiling.

---

## Environment Check

```bash
node -v          # Must succeed — Node is required
cat package.json # Look for "mjml" in dependencies or devDependencies
```

If `mjml` is not in `package.json`: suggest `npm install -D mjml` and wait for user confirmation.

---

## Standard Compilation Command

```bash
npx mjml <source.mjml> -o <output.html> --config.minify=true --config.validationLevel=strict
```

- `--config.minify=true` — **always required**: fixes iOS/Android column stacking bug and keeps payload under Gmail's 102KB clip threshold
- `--config.validationLevel=strict` — fail fast on syntax errors during development

---

## Output Pathing

Mirror source structure into `/dist`, or output alongside source:

- `src/emails/welcome.mjml` → `dist/emails/welcome.html`
- `emails/welcome.mjml` → `emails/welcome.html`

Ensure the output directory exists before compiling — MJML will not create it.

---

## Error Recovery

1. Parse error output for line/column number
2. Read the source file at that line
3. Fix the syntax issue
4. Re-attempt compilation once
5. If output `.html` exists but is 0 bytes — treat as failed, remove the partial file

---

## Implementation Standards

| Standard | Rule |
|----------|------|
| Idempotency | Running twice produces identical output, no duplicate files |
| Clean Up | Remove partial `.html` if compilation fails |
| Logging | Always log the exact CLI command used (user can audit) |
| Version Pinning | New `package.json` → pin MJML to latest stable major (e.g. `^4.15.3`) |
