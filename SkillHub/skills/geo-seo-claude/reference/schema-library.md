# Schema Markup Library: Complete JSON-LD Reference

**Last Updated**: November 11, 2025
**Version**: 1.0
**Standard**: Schema.org (latest)

---

## Overview

Comprehensive reference for all schema types used in SEO/GEO optimization. Each schema includes:
- Purpose and SEO impact
- Required vs. optional properties
- Complete code examples
- Platform-specific optimization notes
- Validation guidelines

---

## Schema Priority (Implementation Order)

**Tier 1: Critical (Highest AI Citation Impact)**
1. **FAQPage** - Highest citation probability across all LLMs
2. **Article** - E-E-A-T signals, 40% citation boost with author credentials
3. **Speakable** - Voice search optimization (embedded in Article)

**Tier 2: High Priority**
4. **HowTo** - Voice search optimized, tutorial content
5. **BreadcrumbList** - Site hierarchy, helps AI understand structure
6. **Organization/LocalBusiness** - Entity recognition, Knowledge Graph

**Tier 3: Supporting**
7. **Person** - Author profiles, E-E-A-T enhancement
8. **WebPage** - Page-level metadata
9. **ImageObject** - Image optimization
10. **VideoObject** - Video content optimization

---

## 1. FAQPage Schema ⭐ HIGHEST PRIORITY

### Purpose
- **Highest AI citation probability** across ChatGPT, Perplexity, Claude, Gemini
- Optimized for voice search (Google Assistant, Siri, Alexa)
- Featured Snippet eligibility (40.7% of voice answers)
- Direct answer format preferred by LLMs

### SEO Impact
- ✅ 40.7% of voice search answers from Featured Snippets
- ✅ 80%+ of voice answers from top 3 results
- ✅ Highest citation rate in ChatGPT/Perplexity testing
- ✅ 29-word answers optimal for voice assistants

### When to Use
- Pages with Q&A content
- Product pages with common questions
- Support/help pages
- Educational content
- Guides and tutorials

### Required Properties
- `@context`: "https://schema.org"
- `@type`: "FAQPage"
- `mainEntity`: Array of Question objects
  - Each Question requires:
    - `@type`: "Question"
    - `name`: The question text
    - `acceptedAnswer`: Answer object
      - `@type`: "Answer"
      - `text`: The answer text (aim for 29 words for voice)

### Complete Example

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is SEO optimization?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SEO (Search Engine Optimization) is the practice of improving website visibility in search engines like Google through technical optimization, quality content, and authoritative backlinks to increase organic traffic."
      }
    },
    {
      "@type": "Question",
      "name": "What is GEO optimization?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "GEO (Generative Engine Optimization) is the practice of optimizing content for AI search engines like ChatGPT, Perplexity, and Claude to increase citation probability in AI-generated responses."
      }
    },
    {
      "@type": "Question",
      "name": "How long does SEO take to show results?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SEO typically takes 3-6 months to show significant results. Technical fixes work faster (1-2 months) while content and backlink strategies require 4-6 months for measurable traffic increases."
      }
    }
  ]
}
```

### Voice Search Optimization
- **Answer length**: Target 29 words (average voice answer length)
- **Natural language**: Write as you'd speak
- **Direct answers**: Start with the answer, then elaborate
- **Question format**: Use "What", "How", "Why", "When", "Where", "Who"

### Platform Notes
- **ChatGPT**: Prefers comprehensive answers (can be longer than 29 words)
- **Perplexity**: Values concise, citation-rich answers
- **Claude**: Prioritizes accurate, evidence-based answers
- **Google Assistant**: Strictly prefers 29-word answers

### Validation Checklist
- [ ] Valid JSON syntax (no trailing commas)
- [ ] All questions have acceptedAnswer
- [ ] Answer text is non-empty
- [ ] Questions use natural language
- [ ] Answers are direct and specific

---

## 2. Article Schema ⭐ CRITICAL FOR E-E-A-T

### Purpose
- E-E-A-T signals (Experience, Expertise, Authoritativeness, Trustworthiness)
- **40% citation boost** when author credentials included
- Platform prioritization (ChatGPT, Claude especially)
- Publication date tracking (critical for Perplexity)

### SEO Impact
- ✅ 40% citation boost with author credentials (MD, PhD, MBA)
- ✅ DateModified tracking (critical for Perplexity)
- ✅ E-E-A-T validation (ChatGPT, Claude)
- ✅ Speakable integration (voice search)

### When to Use
- Blog posts
- News articles
- Educational content
- Research content
- Opinion pieces
- Case studies

### Required Properties
- `@context`: "https://schema.org"
- `@type`: "Article"
- `headline`: Article title (max 110 chars)
- `author`: Person or Organization object
- `datePublished`: ISO 8601 date (YYYY-MM-DD)
- `publisher`: Organization object with name

### Optional But Recommended
- `dateModified`: Last update date (critical for Perplexity)
- `description`: Brief summary
- `image`: Article image (ImageObject)
- `wordCount`: Article word count
- `keywords`: Comma-separated keywords
- `speakable`: Voice search optimization
- `mainEntityOfPage`: Canonical URL

### Complete Example (Optimized for 2025)

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Understanding Longevity Biomarkers: A Complete Guide",
  "description": "Learn how optimal biomarker ranges differ from lab references and can predict longevity more accurately.",
  "image": {
    "@type": "ImageObject",
    "url": "https://example.com/images/biomarkers-guide.jpg",
    "width": 1200,
    "height": 630
  },
  "author": {
    "@type": "Person",
    "name": "Dr. Sarah Johnson",
    "honorificPrefix": "Dr.",
    "honorificSuffix": "MD, PhD",
    "jobTitle": "Board-Certified Physician",
    "affiliation": {
      "@type": "Organization",
      "name": "Stanford School of Medicine"
    },
    "url": "https://example.com/about/dr-sarah-johnson"
  },
  "publisher": {
    "@type": "Organization",
    "name": "199 Clinic",
    "url": "https://199clinic.com",
    "logo": {
      "@type": "ImageObject",
      "url": "https://199clinic.com/logo.png"
    }
  },
  "datePublished": "2025-01-15",
  "dateModified": "2025-11-11",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://example.com/blog/longevity-biomarkers"
  },
  "wordCount": 2450,
  "keywords": "longevity, biomarkers, optimal ranges, health optimization, preventive medicine",
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": [".article-summary", ".article-intro", "h1", "h2"]
  }
}
```

### E-E-A-T Enhancement

**Author Credentials (40% Citation Boost)**:
```json
"author": {
  "@type": "Person",
  "name": "Dr. Sarah Johnson",
  "honorificPrefix": "Dr.",
  "honorificSuffix": "MD, PhD, FAAD",  // ← Critical for ChatGPT/Claude
  "jobTitle": "Professor of Dermatology",
  "affiliation": {
    "@type": "Organization",
    "name": "Harvard Medical School"
  },
  "sameAs": [
    "https://scholar.google.com/citations?user=ABC123",
    "https://orcid.org/0000-0001-2345-6789"
  ]
}
```

### Speakable for Voice Search
```json
"speakable": {
  "@type": "SpeakableSpecification",
  "cssSelector": [
    ".article-summary",  // TL;DR section
    ".article-intro",    // Introduction
    "h1",                // Main heading
    "h2"                 // Section headings
  ]
}
```

### Platform Notes
- **ChatGPT**: Requires author with credentials, values comprehensive content
- **Perplexity**: dateModified is critical, updates prioritized
- **Claude**: Requires author affiliation, values primary sources
- **Gemini**: Standard Article schema sufficient

### Validation Checklist
- [ ] Author has honorificSuffix (MD, PhD, etc.) for 40% boost
- [ ] dateModified is recent (weekly updates ideal)
- [ ] Publisher has name and URL
- [ ] Image is 1200×630px for social sharing
- [ ] Speakable cssSelector points to valid elements

---

## 3. HowTo Schema (Voice Search Optimized)

### Purpose
- Tutorial and guide content
- Voice search optimization
- Step-by-step instructions
- Featured Snippet eligibility

### SEO Impact
- ✅ Voice search friendly (step-by-step format)
- ✅ Featured Snippet eligible
- ✅ Google Assistant prefers HowTo format
- ✅ Clear structure for AI parsing

### Complete Example

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Optimize Content for AI Search",
  "description": "Step-by-step guide to optimize your content for ChatGPT, Perplexity, Claude, and other AI search engines.",
  "image": {
    "@type": "ImageObject",
    "url": "https://example.com/images/ai-optimization-guide.jpg"
  },
  "totalTime": "PT15M",
  "estimatedCost": {
    "@type": "MonetaryAmount",
    "currency": "USD",
    "value": "0"
  },
  "step": [
    {
      "@type": "HowToStep",
      "name": "Add TL;DR in first 60 words",
      "text": "Create a direct answer summary in the first 40-60 words of your content. This increases AI citation probability by 35% according to 2025 studies.",
      "url": "https://example.com/guide#step-1",
      "image": "https://example.com/images/step-1.jpg"
    },
    {
      "@type": "HowToStep",
      "name": "Implement FAQ schema",
      "text": "Add FAQ JSON-LD schema to your page. FAQ schema has the highest AI citation probability across all platforms including ChatGPT and Perplexity.",
      "url": "https://example.com/guide#step-2"
    },
    {
      "@type": "HowToStep",
      "name": "Add author credentials",
      "text": "Include author byline with credentials (MD, PhD, MBA). Author credentials increase citation probability by 40% in ChatGPT and Claude.",
      "url": "https://example.com/guide#step-3"
    }
  ]
}
```

### Time Format (ISO 8601 Duration)
- `PT5M` = 5 minutes
- `PT15M` = 15 minutes
- `PT1H` = 1 hour
- `PT1H30M` = 1 hour 30 minutes
- `P1D` = 1 day

---

## 4. BreadcrumbList Schema

### Purpose
- Site hierarchy visualization
- Navigation path clarity
- Helps AI understand site structure
- Improves internal linking context

### Complete Example

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://example.com/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Blog",
      "item": "https://example.com/blog"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "SEO Guides",
      "item": "https://example.com/blog/seo"
    },
    {
      "@type": "ListItem",
      "position": 4,
      "name": "AI Search Optimization",
      "item": "https://example.com/blog/seo/ai-optimization"
    }
  ]
}
```

---

## 5. Organization / LocalBusiness Schema

### Purpose
- Entity recognition (Google Knowledge Graph)
- Business information
- Contact details
- Local SEO (Gemini, Google Assistant)

### Organization Example

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "199 Clinic",
  "alternateName": "199 Biotechnologies Clinic",
  "url": "https://199clinic.com",
  "logo": "https://199clinic.com/logo.png",
  "description": "Board-certified physicians providing aesthetic medicine, regenerative treatments, and personalized wellness plans.",
  "foundingDate": "2018",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Market Street",
    "addressLocality": "San Francisco",
    "addressRegion": "CA",
    "postalCode": "94103",
    "addressCountry": "US"
  },
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+1-415-555-1234",
    "contactType": "Customer Service",
    "email": "contact@199clinic.com",
    "availableLanguage": ["English", "Spanish"]
  },
  "sameAs": [
    "https://twitter.com/199clinic",
    "https://linkedin.com/company/199clinic",
    "https://instagram.com/199clinic"
  ]
}
```

### LocalBusiness Example (for Gemini/GMB)

```json
{
  "@context": "https://schema.org",
  "@type": "MedicalBusiness",
  "name": "199 Clinic",
  "url": "https://199clinic.com",
  "telephone": "+1-415-555-1234",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Market Street",
    "addressLocality": "San Francisco",
    "addressRegion": "CA",
    "postalCode": "94103",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "37.7749",
    "longitude": "-122.4194"
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "09:00",
      "closes": "18:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": "Saturday",
      "opens": "10:00",
      "closes": "16:00"
    }
  ],
  "priceRange": "$$",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "127"
  }
}
```

---

## 6. Person Schema (Author Profiles)

### Purpose
- Author E-E-A-T signals
- Credentials display
- Professional profiles
- 40% citation boost when complete

### Complete Example

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Dr. Sarah Johnson",
  "honorificPrefix": "Dr.",
  "honorificSuffix": "MD, PhD, FAAD",
  "givenName": "Sarah",
  "familyName": "Johnson",
  "jobTitle": "Board-Certified Physician, Professor of Dermatology",
  "worksFor": {
    "@type": "Organization",
    "name": "Stanford School of Medicine"
  },
  "alumniOf": {
    "@type": "EducationalOrganization",
    "name": "Harvard Medical School"
  },
  "url": "https://example.com/about/dr-sarah-johnson",
  "image": "https://example.com/images/dr-johnson.jpg",
  "description": "Board-certified dermatologist specializing in regenerative medicine with 15+ years of clinical experience. Published researcher in longevity and aesthetic medicine.",
  "sameAs": [
    "https://scholar.google.com/citations?user=ABC123",
    "https://orcid.org/0000-0001-2345-6789",
    "https://linkedin.com/in/sarahjohnsonmd",
    "https://twitter.com/drsarahjohnson"
  ],
  "knowsAbout": [
    "Dermatology",
    "Regenerative Medicine",
    "Longevity Science",
    "Aesthetic Medicine"
  ]
}
```

---

## Multiple Schemas on One Page

### Best Practice: Combine Related Schemas

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Article",
      "headline": "Complete SEO Guide",
      "author": {
        "@type": "Person",
        "@id": "#author"
      },
      "datePublished": "2025-01-15"
    },
    {
      "@type": "Person",
      "@id": "#author",
      "name": "Dr. Sarah Johnson",
      "honorificSuffix": "MD, PhD"
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "What is SEO?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "SEO is Search Engine Optimization..."
          }
        }
      ]
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "https://example.com/"
        }
      ]
    }
  ]
}
</script>
```

---

## Schema Validation

### Tools
1. **Google Rich Results Test**: https://search.google.com/test/rich-results
2. **Schema.org Validator**: https://validator.schema.org/
3. **JSON-LD Validator**: https://json-ld.org/playground/

### Validation Checklist
- [ ] Valid JSON syntax (use JSONLint.com)
- [ ] All required properties present
- [ ] URLs are absolute (not relative)
- [ ] Dates in ISO 8601 format (YYYY-MM-DD)
- [ ] Images are absolute URLs
- [ ] No broken internal @id references

### Common Errors
1. **Trailing commas** in JSON (invalid)
2. **Missing required properties** (headline, author, datePublished)
3. **Relative URLs** (use absolute: https://example.com/page)
4. **Invalid date format** (use YYYY-MM-DD, not MM/DD/YYYY)
5. **Broken @id references** (ensure @id matches usage)

---

## Quick Reference: Property Types

### Common Data Types

**Text**: Simple string
```json
"name": "Example Text"
```

**URL**: Absolute URL
```json
"url": "https://example.com/page"
```

**Date**: ISO 8601 (YYYY-MM-DD)
```json
"datePublished": "2025-01-15"
```

**DateTime**: ISO 8601 with time
```json
"dateModified": "2025-11-11T10:30:00-08:00"
```

**Duration**: ISO 8601 duration
```json
"totalTime": "PT15M"
```

**Number**: Numeric value
```json
"wordCount": 2450
```

**Boolean**: true or false
```json
"isAccessibleForFree": true
```

---

**Last Updated**: November 11, 2025
**Next Review**: Quarterly (Schema.org updates regularly)
**Reference**: https://schema.org/docs/full.html
