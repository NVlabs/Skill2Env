# MJML Head Components Reference

## mj-attributes
Sets default attributes for components globally or by component type. Use to avoid repetitive inline styling.

```xml
<mj-head>
  <mj-attributes>
    <mj-all font-family="Arial, sans-serif" />
    <mj-text padding="0" />
    <mj-class name="hero-text" color="#ffffff" font-size="24px" />
  </mj-attributes>
</mj-head>
```

- `<mj-all>` — applies attribute to every component
- `<mj-text padding="0" />` — overrides defaults for that component type
- `<mj-class name="foo" ... />` — named class, applied via `mj-class="foo"` on any component

Priority: inline attribute > mj-class > component default > mj-all

---

## mj-title
Sets the `<title>` tag and the `aria-label` on the body wrapper div (accessibility).

```xml
<mj-title>Your Email Subject or Title</mj-title>
```

---

## mj-preview
Sets the inbox preview text (visible in email client list before opening).

```xml
<mj-preview>Get 30% off this weekend only — shop now!</mj-preview>
```

No attributes. Content is plain text only.

---

## mj-font
Imports an external web font. Wraps import in MSO conditional comments so Outlook ignores it (preventing Times New Roman fallback). Always pair with a fallback font stack.

| Attribute | Accepts | Description |
|-----------|---------|-------------|
| name | string | Font name used in font-family |
| href | string | URL to hosted CSS file with @font-face |

```xml
<mj-font name="Raleway" href="https://fonts.googleapis.com/css?family=Raleway" />
<!-- Usage: font-family="Raleway, Arial, sans-serif" -->
```

**Outlook note**: Always include fallback fonts (Arial, sans-serif minimum). mj-font hides the @font-face from Outlook to prevent Times New Roman fallback.

---

## mj-breakpoint
Controls the width at which the layout switches from desktop to mobile view.

| Attribute | Accepts | Default |
|-----------|---------|---------|
| width | px | (600px implied) |

```xml
<mj-breakpoint width="480px" />
```

---

## mj-style
Adds custom CSS. Use `inline="inline"` to force Juice inlining (required for Gmail compatibility).

| Attribute | Accepts | Description |
|-----------|---------|-------------|
| inline | "inline" | Inlines CSS via Juice during compilation |

```xml
<!-- Inlined — safe for Gmail -->
<mj-style inline="inline">
  .dark-logo { display: none; }
</mj-style>

<!-- In <head> only — use sparingly -->
<mj-style>
  @media (prefers-color-scheme: dark) {
    .light-logo { display: none !important; }
    .dark-logo { display: block !important; }
  }
</mj-style>
```

**Gmail warning**: Gmail strips `<head>` CSS unless inlined. Critical layout styles must use component attributes, not CSS classes.

---

## mj-html-attributes
Adds custom HTML attributes (data-*, ARIA) to generated HTML elements via CSS selectors. Needed for editable templates or custom ARIA roles.

```xml
<mj-html-attributes>
  <mj-selector path=".custom div">
    <mj-html-attribute name="data-id">42</mj-html-attribute>
  </mj-selector>
</mj-html-attributes>
```

Note: `mj-text` compiles to `<td class="..."><div>`. Target `.custom div` to reach the inner div.
