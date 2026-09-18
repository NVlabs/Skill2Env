# MJML Advanced Components Reference

## mj-hero
Full-width banner section with background image support. Behaves like `mj-section` with a single `mj-column`, but generates VML for Outlook background image support.

Two modes:
- `fluid-height` (default): expands based on content
- `fixed-height`: requires `height` attribute

| Attribute | Accepts | Default |
|-----------|---------|---------|
| mode | fluid-height / fixed-height | fluid-height |
| height | px / % | 0px (required for fixed-height) |
| background-url | URL | null |
| background-color | CSS color | #ffffff |
| background-width | px / % | parent width (mandatory) |
| background-height | px / % | — (mandatory) |
| background-position | CSS keyword | center center |
| border-radius | string | — |
| vertical-align | top/middle/bottom | top |
| inner-background-color | CSS color | — |
| padding | px / % | 0px |

**Required attributes**: `background-width` and `background-height` are mandatory. Use image dimensions exactly.

**Fallback**: Always set `background-color` for clients that don't support background images.

**Outlook**: Background images in `mj-hero` work in Outlook (VML generated). Use keyword positions only (top, center, bottom) — pixel values ignored by Outlook.

```xml
<!-- Fixed height hero -->
<mj-hero
  mode="fixed-height"
  height="400px"
  background-url="https://cdn.example.com/hero.jpg"
  background-width="600px"
  background-height="400px"
  background-color="#1a1a2e"
  padding="80px 0">
  <mj-text align="center" color="#ffffff" font-size="36px" font-weight="bold"
    font-family="Arial, sans-serif" line-height="44px">
    Summer Sale — Up to 50% Off
  </mj-text>
  <mj-button href="https://example.com/sale" align="center"
    background-color="#E63946" color="#ffffff">
    Shop the Sale
  </mj-button>
</mj-hero>
```

```xml
<!-- Fluid height hero -->
<mj-hero
  mode="fluid-height"
  background-url="https://cdn.example.com/banner.jpg"
  background-width="600px"
  background-height="300px"
  background-color="#2a3448"
  padding="60px 0">
  <mj-text align="center" color="#ffffff" font-size="28px">
    New Arrivals
  </mj-text>
</mj-hero>
```

---

## mj-raw
Outputs raw HTML/text without MJML processing. Use for:
- Template engine tags (Handlebars, Liquid, Jinja)
- Custom HTML not achievable with MJML components
- Content before `<!doctype html>` (with `position="file-start"`)

| Attribute | Accepts | Description |
|-----------|---------|-------------|
| position | "file-start" | Places content before doctype |

**In mj-body**: inserted as-is in the email body.
**In mj-head**: content added at end of HTML `<head>`.
**Outside mj-head/mj-body + position="file-start"**: added before doctype.

```xml
<!-- Protecting template tags from minifier -->
<mj-raw>
  <!-- htmlmin:ignore --> {% if user.first_name %} <!-- htmlmin:ignore -->
</mj-raw>
<mj-text>Hello {{ user.first_name }}!</mj-text>
<mj-raw>
  {% else %}
</mj-raw>
<mj-text>Hello there!</mj-text>
<mj-raw>
  {% endif %}
</mj-raw>
```

**Minify warning**: The `<` character causes parse errors with minify. Wrap in `<!-- htmlmin:ignore -->` tags or use `&lt;`.

---

## mj-include
Includes an external `.mjml`, `.css`, or `.html` file at compile time.

| Attribute | Accepts | Description |
|-----------|---------|-------------|
| path | string | Relative path to file |
| type | css / html | Specify for non-mjml files |
| css-inline | "inline" | Inline the CSS (type="css" only) |

```xml
<!-- Include MJML partial -->
<mj-include path="./partials/header.mjml" />

<!-- Include CSS into head -->
<mj-include path="./styles/base.css" type="css" />
<mj-include path="./styles/inline.css" type="css" css-inline="inline" />

<!-- Include raw HTML -->
<mj-include path="./partials/footer.html" type="html" />
```

**Tip**: Wrap partials in `<mjml><mj-body>` tags for preview in editors, then include via path in the main template.

Use `--config.filePath` CLI flag to set a base path for includes independent of the compiled file's location.
