# MJML Content Components Reference

## mj-text
Displays styled text. Content can include raw HTML (`<h1>`, `<p>`, `<a>`, `<strong>`, etc.).

| Attribute | Accepts | Default |
|-----------|---------|---------|
| color | CSS color | #000000 |
| font-family | string | Ubuntu, Helvetica, Arial, sans-serif |
| font-size | px | 13px |
| font-style | string | — |
| font-weight | string | — |
| line-height | px / % | 1 |
| letter-spacing | px / em | — |
| align | left/right/center/justify | left |
| text-decoration | string | — |
| text-transform | string | — |
| padding | px / % | 10px 25px |
| height | px | — |
| container-background-color | CSS color | — |

**Accessibility**: Do NOT set `role` or `aria-level` directly on `mj-text` — illegal under strict validation. Use `mj-html-attributes` in the head instead:

```xml
<!-- In mj-head -->
<mj-html-attributes>
  <mj-selector path=".email-heading div">
    <mj-html-attribute name="role">heading</mj-html-attribute>
    <mj-html-attribute name="aria-level">1</mj-html-attribute>
  </mj-selector>
</mj-html-attributes>

<!-- On the component -->
<mj-text css-class="email-heading" font-family="Arial, sans-serif" font-size="28px"
  font-weight="bold" color="#1a1a1a">
  Welcome to Our Newsletter
</mj-text>
```

**Ending tag**: Content is not processed by MJML. Don't use MJML components inside mj-text. Escape `<` as `&lt;` if needed.

---

## mj-image
Responsive image. If no width set, uses parent column width.

| Attribute | Accepts | Default |
|-----------|---------|---------|
| src | URL | — |
| alt | string | '' |
| width | px | parent width |
| height | px | auto |
| max-height | px / % | — |
| href | URL | — |
| target | string | _blank |
| fluid-on-mobile | boolean | false |
| border | CSS border | 0 |
| border-radius | px / % | — |
| align | left/center/right | center |
| padding | px / % | 10px 25px |
| title | string | — |

**Required**: Always include `alt` for accessibility. Alt text is shown when images are disabled.

**Image format**: Always use PNG, JPG, or WebP. SVG is not supported in Outlook and unreliable in other clients.

**fluid-on-mobile**: Set to `true` to force full viewport width on mobile even if `width` is set.

```xml
<mj-image src="https://cdn.example.com/logo.png" alt="Company Logo"
  width="200px" href="https://example.com" />
```

---

## mj-button
A cross-client compatible CTA button (uses HTML table internally, not CSS button).

| Attribute | Accepts | Default |
|-----------|---------|---------|
| href | URL | — |
| background-color | CSS color | #414141 |
| color | CSS color | #ffffff |
| font-family | string | Ubuntu, Helvetica, Arial, sans-serif |
| font-size | px | 13px |
| font-weight | string | normal |
| border-radius | string | 3px |
| border | CSS border | none |
| inner-padding | px / % | 10px 25px |
| padding | px / % | 10px 25px |
| align | left/center/right | center |
| target | string | _blank |
| width | px / % | — |
| height | px / % | — |
| text-decoration | string | none |
| text-transform | string | none |
| letter-spacing | px / em | — |

**Critical**: `href` is required — without it, button text may fail to render in some clients.

```xml
<mj-button href="https://example.com/shop" background-color="#E63946"
  color="#ffffff" font-family="Arial, sans-serif" border-radius="4px"
  inner-padding="12px 30px">
  Shop Now
</mj-button>
```

---

## mj-divider
A horizontal rule / separator line.

| Attribute | Accepts | Default |
|-----------|---------|---------|
| border-color | CSS color | #000000 |
| border-style | dashed/dotted/solid | solid |
| border-width | px | 4px |
| width | px / % | 100% |
| align | left/center/right | center |
| padding | px / % | 10px 25px |

```xml
<mj-divider border-color="#e0e0e0" border-width="1px" border-style="solid" />
```

---

## mj-spacer
Blank vertical space. Prefer over padding for predictable cross-client spacing.

| Attribute | Accepts | Default |
|-----------|---------|---------|
| height | px / % | 0px |
| padding | px / % | — |

```xml
<mj-spacer height="24px" />
```

---

## mj-table
Renders a data table using plain HTML inside. Only accepts standard HTML (`<tr>`, `<td>`, `<th>`).

| Attribute | Accepts | Default |
|-----------|---------|---------|
| align | left/right/center | left |
| border | CSS border | none |
| cellpadding | integer | 0 |
| cellspacing | integer | 0 |
| color | CSS color | #000000 |
| font-family | string | Ubuntu, Helvetica, Arial, sans-serif |
| font-size | px | 13px |
| line-height | px / % | 22px |
| table-layout | auto/fixed/initial | auto |
| width | px / % / auto | 100% |
| padding | px / % | 10px 25px |
| role | none / presentation | — |

**Use case**: Order receipts, line items, pricing tables. Always inline styles on `<td>` and `<th>` tags.

```xml
<mj-table>
  <tr style="border-bottom:1px solid #ecedee;text-align:left;">
    <th style="padding:0 15px 0 0;">Item</th>
    <th style="padding:0 15px;">Qty</th>
    <th style="padding:0 0 0 15px;">Price</th>
  </tr>
  <tr>
    <td style="padding:8px 15px 0 0;">Widget Pro</td>
    <td style="padding:8px 15px 0;">2</td>
    <td style="padding:8px 0 0 15px;">$49.00</td>
  </tr>
</mj-table>
```
