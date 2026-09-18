# MJML Interactive Components Reference

## mj-accordion
Collapsible content sections. Falls back to expanded view in clients without CSS support (Outlook, older Gmail).

Structure: `mj-accordion` > `mj-accordion-element` > `mj-accordion-title` + `mj-accordion-text`

### mj-accordion attributes

| Attribute | Accepts | Default |
|-----------|---------|---------|
| border | CSS border | 2px solid black |
| font-family | string | Ubuntu, Helvetica, Arial, sans-serif |
| icon-align | top/middle/bottom | middle |
| icon-position | left/right | right |
| icon-width | px / % | 32px |
| icon-height | px / % | 32px |
| icon-wrapped-url | URL | default + icon |
| icon-unwrapped-url | URL | default - icon |
| icon-wrapped-alt | string | + |
| icon-unwrapped-alt | string | - |
| padding | px / % | 10px 25px |

### mj-accordion-title attributes
| Attribute | Accepts | Default |
|-----------|---------|---------|
| background-color | CSS color | — |
| color | CSS color | — |
| font-family | string | — |
| font-size | px | 13px |
| font-weight | string | — |
| padding | px / % | 16px |

### mj-accordion-text attributes
| Attribute | Accepts | Default |
|-----------|---------|---------|
| background-color | CSS color | — |
| color | CSS color | — |
| font-family | string | — |
| font-size | px | 13px |
| font-weight | string | — |
| line-height | px / % | 1 |
| letter-spacing | px / em | — |
| padding | px / % | 16px |

```xml
<mj-accordion>
  <mj-accordion-element>
    <mj-accordion-title>Shipping Policy</mj-accordion-title>
    <mj-accordion-text>Free shipping on orders over $50.</mj-accordion-text>
  </mj-accordion-element>
  <mj-accordion-element>
    <mj-accordion-title>Return Policy</mj-accordion-title>
    <mj-accordion-text>30-day returns, no questions asked.</mj-accordion-text>
  </mj-accordion-element>
</mj-accordion>
```

---

## mj-carousel
Image gallery/slider inside an email. Falls back to first image only in unsupported clients.

Structure: `mj-carousel` > `mj-carousel-image`

### mj-carousel attributes

| Attribute | Accepts | Default |
|-----------|---------|---------|
| align | left/center/right | center |
| border-radius | px / % | 6px |
| thumbnails | visible/hidden/supported | hidden |
| tb-width | px / % | — |
| tb-border | CSS border | 2px solid transparent |
| tb-border-radius | px / % | 6px |
| tb-hover-border-color | CSS color | #fead0d |
| tb-selected-border-color | CSS color | #ccc |
| icon-width | px / % | 44px |
| left-icon | URL | default arrow |
| right-icon | URL | default arrow |
| padding | px / % | — |

### mj-carousel-image attributes

| Attribute | Accepts | Default |
|-----------|---------|---------|
| src | URL | — |
| alt | string | '' |
| href | URL | — |
| target | string | _blank |
| title | string | — |
| border-radius | px / % | — |
| thumbnails-src | URL | (same as src) |
| tb-border | CSS border | — |
| tb-border-radius | px / % | — |

```xml
<mj-carousel thumbnails="visible">
  <mj-carousel-image src="https://cdn.example.com/product-1.jpg" alt="Product 1" href="https://example.com/p1" />
  <mj-carousel-image src="https://cdn.example.com/product-2.jpg" alt="Product 2" href="https://example.com/p2" />
  <mj-carousel-image src="https://cdn.example.com/product-3.jpg" alt="Product 3" href="https://example.com/p3" />
</mj-carousel>
```

---

## mj-social
Social media icon bar. Contains `mj-social-element` children.

### mj-social attributes

| Attribute | Accepts | Default |
|-----------|---------|---------|
| mode | horizontal/vertical | horizontal |
| align | left/center/right | center |
| font-family | string | Ubuntu, Helvetica, Arial, sans-serif |
| font-size | px | 13px |
| icon-size | px / % | 20px |
| icon-height | px / % | icon-size |
| icon-padding | px / % | — |
| border-radius | px / % | 3px |
| color | CSS color | #333333 |
| line-height | px / % | 22px |
| text-decoration | string | none |
| padding | px / % | 10px 25px |
| inner-padding | px / % | null |

### mj-social-element attributes

| Attribute | Accepts | Default |
|-----------|---------|---------|
| name | string (see list below) | — |
| href | URL | — |
| src | URL | network default |
| background-color | CSS color | network default |
| alt | string | '' |
| title | string | — |
| icon-size | px / % | — |
| icon-position | left/right | — |
| font-size | px | 13px |
| color | CSS color | #000 |
| border-radius | px | 3px |
| padding | px / % | 4px |
| text-padding | px / % | 4px 4px 4px 0 |
| target | string | _blank |
| vertical-align | top/middle/bottom | middle |

**Supported network names** (with share URL): `facebook`, `twitter`, `x`, `google`, `pinterest`, `linkedin`, `tumblr`, `xing`

**Without share URL**: `github`, `instagram`, `web`, `snapchat`, `youtube`, `vimeo`, `medium`, `soundcloud`, `dribbble`

**To link profile instead of share**: append `-noshare` — e.g. `name="twitter-noshare"`

```xml
<mj-social font-size="13px" icon-size="24px" mode="horizontal">
  <mj-social-element name="facebook-noshare" href="https://facebook.com/yourpage">
    Facebook
  </mj-social-element>
  <mj-social-element name="instagram-noshare" href="https://instagram.com/yourhandle">
    Instagram
  </mj-social-element>
  <mj-social-element name="linkedin-noshare" href="https://linkedin.com/company/yours">
    LinkedIn
  </mj-social-element>
</mj-social>
```

---

## mj-navbar
Responsive navigation bar with optional hamburger menu on mobile. Hamburger support limited to CSS-capable clients.

### mj-navbar attributes

| Attribute | Accepts | Default |
|-----------|---------|---------|
| align | left/center/right | center |
| base-url | string | null |
| hamburger | "hamburger" | null |
| ico-color | CSS color | #000000 |
| ico-font-size | px / % | 30px |
| ico-align | left/center/right | center |
| ico-open | string | &#9776; |
| ico-close | string | &#8855; |
| ico-padding | px / % | 10px |
| padding | px / % | — |

### mj-navbar-link attributes

| Attribute | Accepts | Default |
|-----------|---------|---------|
| href | URL | — |
| color | CSS color | #000000 |
| font-family | string | Ubuntu, Helvetica, Arial, sans-serif |
| font-size | px | 13px |
| font-weight | string | — |
| padding | px / % | 15px 10px |
| text-decoration | string | none |
| text-transform | string | uppercase |
| target | string | — |

```xml
<mj-navbar base-url="https://example.com" hamburger="hamburger" ico-color="#333333">
  <mj-navbar-link href="/products" color="#333333">Products</mj-navbar-link>
  <mj-navbar-link href="/about" color="#333333">About</mj-navbar-link>
  <mj-navbar-link href="/contact" color="#333333">Contact</mj-navbar-link>
</mj-navbar>
```
