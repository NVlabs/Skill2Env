# Social Media Preview Optimization Guide

**Last Updated**: November 11, 2025
**Version**: 1.0
**Platforms**: Facebook, Twitter/X, LinkedIn, WhatsApp, iMessage, Instagram, Slack, Discord

---

## Overview

Social media previews (link cards) appear when URLs are shared across platforms. Proper optimization ensures:
- Professional appearance
- Higher click-through rates
- Accurate information display
- Consistent branding
- Better engagement

**Impact**: Well-optimized previews can increase CTR by 2-3x versus default previews.

---

## Open Graph Protocol (Facebook, LinkedIn, WhatsApp, iMessage)

### Purpose
- Created by Facebook (Meta)
- Adopted by most platforms
- Controls preview appearance
- Industry standard for social sharing

### Required Tags

**Minimum Implementation**:
```html
<!-- Essential Open Graph Tags -->
<meta property="og:title" content="Your Page Title - 60-90 characters">
<meta property="og:description" content="Compelling description that encourages clicks. Keep it engaging and specific. 150-200 characters ideal.">
<meta property="og:image" content="https://example.com/images/social-preview.jpg">
<meta property="og:url" content="https://example.com/page">
<meta property="og:type" content="website">
```

### Complete Implementation

```html
<!-- Complete Open Graph Tags -->
<meta property="og:title" content="Understanding Longevity Biomarkers | 199 Clinic">
<meta property="og:description" content="Learn how optimal biomarker ranges differ from lab references and predict longevity more accurately. Evidence-based guide from board-certified physicians.">
<meta property="og:image" content="https://199clinic.com/images/biomarkers-guide-social.jpg">
<meta property="og:image:alt" content="Infographic showing optimal vs. lab biomarker ranges">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="https://199clinic.com/blog/longevity-biomarkers">
<meta property="og:type" content="article">
<meta property="og:site_name" content="199 Clinic">
<meta property="og:locale" content="en_US">

<!-- Article-Specific Tags -->
<meta property="article:published_time" content="2025-01-15T09:00:00Z">
<meta property="article:modified_time" content="2025-11-11T14:30:00Z">
<meta property="article:author" content="Dr. Sarah Johnson">
<meta property="article:section" content="Longevity">
<meta property="article:tag" content="Biomarkers">
<meta property="article:tag" content="Longevity">
<meta property="article:tag" content="Health Optimization">
```

### Property Reference

**og:title**:
- **Purpose**: Preview title (appears as headline)
- **Length**: 60-90 characters (truncates around 88)
- **Best Practice**: Front-load key information, include brand
- **Example**: "5 Biomarkers That Predict Longevity | 199 Clinic"

**og:description**:
- **Purpose**: Preview description (appears below title)
- **Length**: 150-200 characters (varies by platform)
- **Best Practice**: Compelling, benefit-focused, call-to-action
- **Example**: "Discover the optimal biomarker ranges that predict healthspan. Learn why standard lab ranges aren't enough for longevity optimization."

**og:image**:
- **Purpose**: Preview image
- **Size**: 1200×630px (recommended)
- **Minimum**: 600×315px
- **Format**: JPG or PNG (JPG preferred for file size)
- **File Size**: <1MB (ideally <300KB)
- **Best Practice**: High-quality, text legible at small sizes, branded

**og:url**:
- **Purpose**: Canonical URL
- **Format**: Absolute URL (https://example.com/page)
- **Best Practice**: Use canonical URL, no query parameters

**og:type**:
- **Purpose**: Content type
- **Values**: website, article, video.movie, video.episode, music.song, etc.
- **Default**: "website"
- **Article pages**: Use "article"

**og:site_name**:
- **Purpose**: Website brand name
- **Best Practice**: Company/brand name only
- **Example**: "199 Clinic" (not "199 Clinic - Longevity Medicine")

---

## Twitter Cards (Twitter/X)

### Purpose
- Twitter-specific preview format
- Overrides Open Graph (if present)
- Two main formats: Summary and Summary with Large Image

### Required Tags

**Summary Card** (small image):
```html
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="Your Page Title">
<meta name="twitter:description" content="Page description here">
<meta name="twitter:image" content="https://example.com/image.jpg">
```

**Summary Large Image Card** (recommended):
```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Understanding Longevity Biomarkers">
<meta name="twitter:description" content="Learn how optimal biomarker ranges predict longevity more accurately than standard lab references.">
<meta name="twitter:image" content="https://199clinic.com/images/biomarkers-twitter.jpg">
<meta name="twitter:image:alt" content="Chart comparing optimal vs. lab biomarker ranges">
<meta name="twitter:site" content="@199clinic">
<meta name="twitter:creator" content="@drsarahjohnson">
```

### Property Reference

**twitter:card**:
- **Values**: summary, summary_large_image, app, player
- **Recommended**: summary_large_image (better engagement)
- **Summary**: Small 1:1 image (left side)
- **Summary Large**: Large 2:1 image (below title)

**twitter:image**:
- **Size** (summary): 400×400px minimum (1:1 ratio)
- **Size** (large): 1200×628px recommended (1.91:1 ratio)
- **Format**: JPG, PNG, WEBP, GIF
- **File Size**: <5MB
- **Best Practice**: Use large card for article content

**twitter:site**:
- **Purpose**: @username of website
- **Format**: "@yourbrand"
- **Example**: "@199clinic"

**twitter:creator**:
- **Purpose**: @username of content creator
- **Format**: "@authorname"
- **Example**: "@drsarahjohnson"
- **Note**: Appears as "by @authorname" in card

---

## Platform-Specific Optimization

### Facebook

**Image Specifications**:
- **Recommended**: 1200×630px (1.91:1 ratio)
- **Minimum**: 600×315px
- **Maximum**: 8MB

**Text Overlay**:
- Avoid >20% text on image (old rule, less strict now)
- Ensure text is legible at thumbnail size
- Use high contrast

**Best Practices**:
- Use og:type="article" for blog posts
- Include article:published_time and article:modified_time
- Add article:author for attribution
- Use engaging, benefit-focused descriptions

**Testing**:
- Facebook Sharing Debugger: https://developers.facebook.com/tools/debug/

### LinkedIn

**Image Specifications**:
- **Recommended**: 1200×627px (1.91:1 ratio)
- **Minimum**: 1200×627px (LinkedIn is strict)
- **Format**: PNG or JPG

**Best Practices**:
- Professional, business-focused imagery
- Include credentials and titles
- Use company logo/branding
- Highlight professional value

**Testing**:
- LinkedIn Post Inspector: https://www.linkedin.com/post-inspector/

### WhatsApp

**Behavior**:
- Uses Open Graph tags (same as Facebook)
- Heavily cached (updates can take hours/days)
- Shows smaller image than Facebook

**Image Specifications**:
- **Same as Facebook**: 1200×630px
- **Note**: Appears smaller in WhatsApp
- **Tip**: Keep key visual elements centered

**Best Practices**:
- Clear, simple images (small display)
- Short, punchy titles
- Descriptions should stand alone
- Test on mobile device

### iMessage (iOS)

**Behavior**:
- Uses ONLY og:title and og:image
- Does NOT use og:description
- Very simple preview format

**Image Specifications**:
- **Recommended**: 1200×630px
- **Also works**: Square images (400×400px)
- **Note**: Shows very small thumbnail

**Best Practices**:
- Focus on og:title (description not shown)
- Use simple, clear images
- Ensure image is recognizable at tiny sizes
- Test on iPhone/iPad

**Example (iMessage-optimized)**:
```html
<meta property="og:title" content="5 Biomarkers for Longevity | 199 Clinic">
<meta property="og:image" content="https://199clinic.com/images/biomarkers-simple.jpg">
<!-- og:description not shown in iMessage, but include for other platforms -->
<meta property="og:description" content="Evidence-based guide to optimal biomarker ranges.">
```

### Instagram

**Behavior**:
- Limited Open Graph support (Stories only)
- No clickable links in captions
- Bio link is primary external link
- Uses Open Graph for link stickers in Stories
- No automatic previews in Feed posts
- Link-in-bio tools required for multiple links

**Important Limitations**:
- Instagram does NOT support OG previews in feed posts
- Captions cannot contain clickable links
- Only verified accounts (10K+ followers) get swipe-up Stories
- Bio limited to 150 characters + 1 link

**Image Specifications (2025)**:

| Format | Dimensions | Aspect Ratio | Use Case |
|--------|-----------|--------------|----------|
| **Stories** | 1080×1920px | 9:16 (vertical) | Full-screen mobile |
| **Feed Post** | 1080×1350px | 4:5 (portrait) | Primary feed format |
| **Grid Preview** | 1080×1440px | 3:4 (portrait) | 2025 grid update |
| **Link Preview** | 1200×630px | 1.91:1 (landscape) | External link stickers |
| **Reels** | 1080×1920px | 9:16 (vertical) | Video format |

**Stories Safe Zone**:
- **Full canvas**: 1080×1920px
- **Safe area**: 1080×1610px (center)
- **Avoid areas**: Top 155px (profile), bottom 155px (reply bar)

**Open Graph Tags for Instagram Stories**:
```html
<!-- Instagram uses standard OG tags for link stickers -->
<meta property="og:title" content="Page Title (60-90 chars)">
<meta property="og:description" content="Description (150-200 chars)">
<meta property="og:image" content="https://example.com/image-1200x630.jpg">
<meta property="og:url" content="https://example.com/page">
<meta property="og:type" content="website">
```

**Bio Link Optimization**:
- **URL shorteners**: Use branded short links (bit.ly, Linktree)
- **UTM tracking**: Track Instagram traffic separately
- **Mobile-first**: 85%+ of Instagram users are mobile
- **Landing page**: Optimize for mobile (fast load, touch targets)

**Meta Tags for Bio Link Pages**:
```html
<!-- Optimize destination pages for mobile -->
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta property="og:title" content="Company Name | Key Offering">
<meta property="og:description" content="Mobile-friendly description">
<meta property="og:image" content="https://example.com/mobile-optimized.jpg">

<!-- Instagram-specific metadata (for external tools) -->
<meta name="instagram:profile" content="@yourusername">
```

**Link-in-Bio Tools** (Multiple Links):
- Linktree, Later, Shorby, Pallyy
- Milkshake, Lnk.Bio, Sked Link
- Built-in Instagram (max 5 links)

**2025 Grid Changes**:
- **Old format**: 1:1 square preview
- **New format**: 3:4 portrait preview (taller)
- **Strategy**: Center important content in center square
- **Maximum dimensions**: 1080×1350px (4:5 ratio)

**Best Practices**:
- **Mobile-first**: 85%+ mobile users, optimize page speed
- **Stories**: Use 9:16 vertical format, keep text in safe zone
- **Feed**: Use 4:5 portrait (1080×1350px) for maximum visibility
- **Grid**: Center key elements in 1:1 square for mixed feeds
- **Bio link**: Use link aggregators for multiple destinations
- **Tracking**: Use UTM parameters to measure Instagram traffic
- **Open Graph**: Required for Stories link stickers
- **Image quality**: High resolution (Instagram compresses heavily)

**Testing Instagram Previews**:
- No official Instagram validator
- Test Stories manually (share to yourself)
- Use OpenGraph.xyz for OG tag validation
- Test bio link on mobile device
- Check page load speed (<3 seconds on 4G)

### Slack

**Behavior**:
- Uses Open Graph tags
- Shows rich previews by default
- Can be disabled by users

**Image Specifications**:
- **Recommended**: 1200×630px
- **Shows**: Medium-sized preview
- **Truncates**: Long titles and descriptions

**Best Practices**:
- Professional imagery
- Clear, descriptive titles
- Concise descriptions
- Test in Slack workspace

### Discord

**Behavior**:
- Uses Open Graph tags
- Rich embeds for links
- Can customize with embed color

**Image Specifications**:
- **Recommended**: 1200×630px
- **Shows**: Medium-large preview
- **Supports**: GIFs and videos

**Best Practices**:
- Eye-catching images
- Gaming/tech-friendly aesthetic
- Consider animated GIFs
- Test in Discord server

---

## Image Optimization

### Size Recommendations

**Primary Recommendation** (works everywhere):
- **Dimensions**: 1200×630px
- **Ratio**: 1.91:1 (landscape)
- **Why**: Accepted by all major platforms

**Alternative Formats**:

| Platform | Ideal Size | Ratio | Notes |
|----------|-----------|-------|-------|
| Facebook | 1200×630px | 1.91:1 | Standard OG |
| Twitter Large | 1200×628px | 1.91:1 | Slightly different |
| Twitter Summary | 400×400px | 1:1 | Square card |
| LinkedIn | 1200×627px | 1.91:1 | Strict minimum |
| WhatsApp | 1200×630px | 1.91:1 | Same as Facebook |
| iMessage | 1200×630px | 1.91:1 | Small display |
| Instagram Stories | 1080×1920px | 9:16 | Vertical full-screen |
| Instagram Feed | 1080×1350px | 4:5 | Primary feed format |
| Instagram Grid | 1080×1440px | 3:4 | 2025 grid update |
| Instagram Link | 1200×630px | 1.91:1 | Link sticker preview |

### File Optimization

**Format Selection**:
- **JPG**: Photos, complex images (smaller file size)
- **PNG**: Graphics, text, transparency needs
- **WEBP**: Modern format (not universally supported yet)

**Compression**:
- **Target**: <300KB for fast loading
- **Maximum**: <1MB (some platforms have 5-8MB limits)
- **Tools**: TinyPNG, ImageOptim, Squoosh

**Quality**:
- **High quality**: 85-90% (JPG)
- **Mobile preview**: Image will be scaled down
- **Retina displays**: 2x resolution beneficial

### Design Best Practices

**Visual Hierarchy**:
1. **Main focal point**: Center or left-aligned
2. **Text overlay**: Large, legible font (min 60px)
3. **Branding**: Logo in corner (consistent placement)
4. **Contrast**: High contrast for readability
5. **Safe area**: Keep important elements centered

**Text on Images**:
- **Minimum font size**: 60px for body text
- **Heading size**: 120px+ for main message
- **Font weight**: Bold or heavy for legibility
- **Color contrast**: WCAG AA minimum (4.5:1)
- **Background**: Semi-transparent overlay for text areas

**Brand Consistency**:
- Use brand colors
- Include logo (subtle, not overwhelming)
- Consistent style across all social images
- Template system for efficiency

**Example Template Structure**:
```
[Background Image: 1200×630px]
  ├─ [Logo: Top-left corner, 80×80px]
  ├─ [Main Headline: Center, 120px font]
  ├─ [Subheading: Below headline, 60px font]
  └─ [Brand Color Strip: Bottom, 80px height]
```

---

## Complete Meta Tags Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- Primary Meta Tags -->
  <title>Understanding Longevity Biomarkers | 199 Clinic</title>
  <meta name="title" content="Understanding Longevity Biomarkers | 199 Clinic">
  <meta name="description" content="Learn how optimal biomarker ranges differ from lab references and predict longevity more accurately. Evidence-based guide from board-certified physicians.">

  <!-- Open Graph / Facebook / LinkedIn / WhatsApp -->
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://199clinic.com/blog/longevity-biomarkers">
  <meta property="og:title" content="Understanding Longevity Biomarkers | 199 Clinic">
  <meta property="og:description" content="Learn how optimal biomarker ranges differ from lab references and predict longevity more accurately. Evidence-based guide from board-certified physicians.">
  <meta property="og:image" content="https://199clinic.com/images/biomarkers-social.jpg">
  <meta property="og:image:alt" content="Infographic showing optimal vs. lab biomarker ranges">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:site_name" content="199 Clinic">
  <meta property="og:locale" content="en_US">

  <!-- Article-Specific Tags -->
  <meta property="article:published_time" content="2025-01-15T09:00:00Z">
  <meta property="article:modified_time" content="2025-11-11T14:30:00Z">
  <meta property="article:author" content="Dr. Sarah Johnson">
  <meta property="article:section" content="Longevity">
  <meta property="article:tag" content="Biomarkers">

  <!-- Twitter / X -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:url" content="https://199clinic.com/blog/longevity-biomarkers">
  <meta name="twitter:title" content="Understanding Longevity Biomarkers | 199 Clinic">
  <meta name="twitter:description" content="Learn how optimal biomarker ranges differ from lab references and predict longevity more accurately.">
  <meta name="twitter:image" content="https://199clinic.com/images/biomarkers-twitter.jpg">
  <meta name="twitter:image:alt" content="Chart comparing optimal vs. lab biomarker ranges">
  <meta name="twitter:site" content="@199clinic">
  <meta name="twitter:creator" content="@drsarahjohnson">

  <!-- Canonical URL -->
  <link rel="canonical" href="https://199clinic.com/blog/longevity-biomarkers">
</head>
<body>
  <!-- Page content -->
</body>
</html>
```

---

## Testing & Validation

### Testing Tools

**Facebook**:
- URL: https://developers.facebook.com/tools/debug/
- Shows: Preview + cache status
- Action: Clear cache and re-scrape

**Twitter**:
- URL: https://cards-dev.twitter.com/validator
- Shows: Live preview
- Note: Requires Twitter login

**LinkedIn**:
- URL: https://www.linkedin.com/post-inspector/
- Shows: Preview + warnings
- Action: Clear cache

**General**:
- URL: https://www.opengraph.xyz/
- Shows: Multi-platform preview
- Action: Test all platforms at once

### Manual Testing

**Test on Actual Devices**:
1. Share URL in private message to yourself
2. Check preview appearance
3. Test on mobile + desktop
4. Verify image loads correctly
5. Check title and description truncation

**Platforms to Test**:
- [ ] Facebook (mobile + desktop)
- [ ] Twitter/X (mobile + desktop)
- [ ] LinkedIn (mobile + desktop)
- [ ] WhatsApp (mobile)
- [ ] iMessage (iOS)
- [ ] Slack (desktop)
- [ ] Discord (desktop)

### Common Issues

**Image Not Showing**:
- ✓ Check absolute URL (not relative)
- ✓ Verify HTTPS (not HTTP)
- ✓ Ensure image is publicly accessible
- ✓ Check file size (<5MB)
- ✓ Verify dimensions (min 600×315px)
- ✓ Clear platform cache

**Wrong Image Showing**:
- ✓ Clear platform cache
- ✓ Wait 24-48 hours for cache expiration
- ✓ Use unique filename for new image
- ✓ Add cache-busting query parameter (?v=2)

**Title/Description Truncated**:
- ✓ Reduce title to 60-90 characters
- ✓ Reduce description to 150-200 characters
- ✓ Front-load important information
- ✓ Test on multiple platforms

**Preview Not Updating**:
- ✓ Clear platform cache (use debugger tools)
- ✓ Change og:url to force re-scrape
- ✓ Wait 24 hours for natural cache expiry
- ✓ Verify meta tags in page source (not just CMS)

---

## Best Practices Summary

### Do's ✅

- Use 1200×630px images (works everywhere)
- Include alt text for accessibility
- Use absolute URLs (https://example.com/image.jpg)
- Test on multiple platforms
- Optimize images (<300KB)
- Use high-contrast, legible text
- Include branding consistently
- Write compelling descriptions
- Test on mobile devices
- Clear cache when updating

### Don'ts ❌

- Use relative URLs (/images/photo.jpg)
- Exceed 1MB image file size
- Use tiny images (<600px width)
- Forget alt text
- Use >20% text overlay (Facebook)
- Use HTTP instead of HTTPS
- Forget to test before sharing
- Use stock photos without customization
- Ignore mobile preview
- Update without clearing cache

---

**Last Updated**: November 11, 2025
**Next Review**: Quarterly
**Testing Recommended**: Before every major content launch
