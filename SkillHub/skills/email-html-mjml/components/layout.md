# MJML Layout Components Reference

## Document Hierarchy
```
mjml
├── mj-head
└── mj-body
    ├── mj-wrapper (optional grouping)
    │   └── mj-section
    ├── mj-section (row)
    │   ├── mj-column (or mj-group)
    │   │   └── [content components]
    │   └── mj-group
    │       └── mj-column
    └── mj-hero (special banner section)
```

**Hard rules:**
- `mj-section` and `mj-column` cannot be nested inside another `mj-column`
- Every content component inside a column inherits 100% of the column width
- Default email width: 600px (set on `mj-body`)

---

## Root `<mjml>` tag

| Attribute | Accepts | Default | Notes |
|-----------|---------|---------|-------|
| lang | string | "und" | Sets `lang` attribute on `<html>` and body `<div>`. Use for accessibility + RTL support. e.g. `lang="en"` |
| dir | ltr / rtl | auto | Text direction |
| owa | "desktop" | none | Forces desktop view for old self-hosted Outlook.com (rare) |

```xml
<mjml lang="en" dir="ltr">
```

---

## mj-body

| Attribute | Accepts | Default |
|-----------|---------|---------|
| background-color | CSS color | — |
| width | px | 600px |
| css-class | string | — |

---

## mj-section
A horizontal row. Contains `mj-column` or `mj-group` children.

| Attribute | Accepts | Default |
|-----------|---------|---------|
| background-color | CSS color | — |
| background-url | URL string | — |
| background-size | CSS string | auto |
| background-repeat | repeat / no-repeat | — |
| background-position | CSS keyword/% | top center |
| full-width | "full-width" | — |
| border | CSS border | — |
| border-radius | string | — |
| direction | ltr / rtl | ltr |
| padding | px / % | 20px 0 |
| text-align | left/center/right | center |

**Outlook background images**: Only `mj-section` and `mj-hero` support background images (MJML generates VML). Always set `background-size` and `background-color` fallback when using `background-url`. Use keyword positions (top, center) not pixels for Outlook.

```xml
<mj-section background-url="https://..." background-color="#2a3448"
  background-size="cover" background-repeat="no-repeat">
```

---

## mj-column
A responsive column inside a section. Columns stack vertically on mobile by default.

Width is auto-calculated: 2 columns = 50% each, 3 columns = 33.33% each. Override with `width`.

| Attribute | Accepts | Default |
|-----------|---------|---------|
| width | px / % | (100 / col count)% |
| background-color | CSS color | — |
| inner-background-color | CSS color | — |
| border | CSS border | — |
| border-radius | px / % | — |
| vertical-align | top/middle/bottom | top |
| padding | px / % | — |
| direction | ltr / rtl | ltr |

**vertical-align bug**: If any column in a section uses `vertical-align="middle"`, ALL columns in that section must also explicitly set `vertical-align="middle"` for it to render consistently.

```xml
<mj-section>
  <mj-column width="40%">...</mj-column>
  <mj-column width="60%">...</mj-column>
</mj-section>
```

---

## mj-group
Prevents columns from stacking on mobile. Wrap columns in `mj-group` to keep them side-by-side on small screens (e.g. social bars, logo headers).

| Attribute | Accepts | Default |
|-----------|---------|---------|
| width | px / % | (100 / count)% |
| background-color | CSS color | — |
| direction | ltr / rtl | ltr |
| vertical-align | CSS value | — |

**iOS stacking bug**: Even with `mj-group`, whitespace/comments between tags can cause stacking. Always compile with `--config.minify` to eliminate this.

```xml
<mj-section>
  <mj-group>
    <mj-column><mj-image src="icon1.png" alt="Facebook" /></mj-column>
    <mj-column><mj-image src="icon2.png" alt="Twitter" /></mj-column>
  </mj-group>
</mj-section>
```

---

## mj-wrapper
Groups multiple `mj-section` elements with a shared border, background, or padding. Useful for card-style layouts.

| Attribute | Accepts | Default |
|-----------|---------|---------|
| background-color | CSS color | — |
| background-url | URL | — |
| background-size | CSS string | auto |
| border | CSS border | — |
| border-radius | string | — |
| full-width | "full-width" | — |
| padding | px / % | 20px 0 |
| gap | px | — |

```xml
<mj-wrapper border="1px solid #e0e0e0" padding="20px 0">
  <mj-section>...</mj-section>
  <mj-section>...</mj-section>
</mj-wrapper>
```
