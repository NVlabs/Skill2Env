# Entity SEO & Knowledge Graph Optimization

**Last Updated**: November 11, 2025
**Version**: 1.0
**Focus**: Google Knowledge Graph, entity recognition, semantic SEO

---

## Overview

Entity SEO focuses on establishing your organization, people, and concepts as recognized entities in Google's Knowledge Graph and other search engine databases. Recognized entities receive:
- Priority in AI citations (ChatGPT, Perplexity, Claude)
- Knowledge Panel display (Google)
- Rich results and enhanced features
- Higher authority signals
- Better context understanding

**Entity** = Thing or concept that is singular, unique, well-defined, and distinguishable.

Examples: "199 Clinic" (organization), "Dr. Sarah Johnson" (person), "Longevity Medicine" (concept)

---

## Why Entity SEO Matters

### Benefits

**For Organizations**:
- Google Knowledge Panel (right side of SERP)
- Enhanced brand visibility
- Rich snippets and features
- AI citation priority
- Credibility signals

**For People** (Authors, Experts):
- Author authority (E-E-A-T)
- Google Scholar integration
- Professional profile display
- +40% AI citation boost
- Career visibility

**For AI Search**:
- ChatGPT prioritizes known entities
- Claude validates entity credentials
- Perplexity links to entity profiles
- Gemini integrates with Knowledge Graph

---

## Entity Types

### 1. Organization Entities

**What Qualifies**:
- Businesses (clinics, companies, agencies)
- Educational institutions
- Non-profits
- Government agencies
- Professional associations

**Schema Types**:
- `Organization` (general)
- `LocalBusiness` (location-based)
- `MedicalBusiness` (healthcare)
- `ProfessionalService` (consulting, legal)
- `EducationalOrganization` (schools, universities)

**Example - MedicalBusiness**:
```json
{
  "@context": "https://schema.org",
  "@type": "MedicalBusiness",
  "name": "199 Clinic",
  "alternateName": "199 Biotechnologies Clinic",
  "url": "https://199clinic.com",
  "logo": "https://199clinic.com/logo.png",
  "description": "Board-certified physicians providing aesthetic medicine, regenerative treatments, and personalized wellness plans.",
  "foundingDate": "2018",
  "founders": [{
    "@type": "Person",
    "name": "Dr. Sarah Johnson"
  }],
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
    "contactType": "Customer Service"
  },
  "sameAs": [
    "https://twitter.com/199clinic",
    "https://linkedin.com/company/199clinic",
    "https://www.wikidata.org/wiki/Q12345678"
  ]
}
```

### 2. Person Entities (Authors, Experts)

**What Qualifies**:
- Authors with bylines
- Industry experts
- Company founders
- Medical professionals
- Academic researchers

**Schema Type**: `Person`

**Example - Medical Professional**:
```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Dr. Sarah Johnson",
  "honorificPrefix": "Dr.",
  "honorificSuffix": "MD, PhD, FAAD",
  "givenName": "Sarah",
  "familyName": "Johnson",
  "gender": "Female",
  "jobTitle": "Board-Certified Physician, Professor of Dermatology",
  "worksFor": {
    "@type": "Organization",
    "name": "199 Clinic",
    "sameAs": "https://199clinic.com"
  },
  "affiliation": [{
    "@type": "Organization",
    "name": "Stanford School of Medicine"
  }],
  "alumniOf": [{
    "@type": "EducationalOrganization",
    "name": "Harvard Medical School"
  }],
  "url": "https://199clinic.com/about/dr-sarah-johnson",
  "image": "https://199clinic.com/images/dr-johnson.jpg",
  "description": "Board-certified dermatologist specializing in regenerative medicine with 15+ years of clinical experience.",
  "sameAs": [
    "https://scholar.google.com/citations?user=ABC123",
    "https://orcid.org/0000-0001-2345-6789",
    "https://linkedin.com/in/sarahjohnsonmd",
    "https://twitter.com/drsarahjohnson",
    "https://www.wikidata.org/wiki/Q87654321"
  ],
  "knowsAbout": [
    "Dermatology",
    "Regenerative Medicine",
    "Longevity Science",
    "Aesthetic Medicine"
  ],
  "award": [
    "Top Dermatologist, San Francisco Magazine 2024",
    "Research Excellence Award, American Academy of Dermatology"
  ]
}
```

### 3. Concept Entities

**Examples**:
- "Longevity Medicine"
- "Generative Engine Optimization"
- "Optimal Biomarker Ranges"

**Strategy**: Build topical authority through comprehensive content, internal linking, and structured data.

---

## Building Entity Recognition

### Step 1: Entity Establishment

**For Organizations**:

1. **Create official profiles**:
   - Google Business Profile (essential)
   - LinkedIn Company Page
   - Wikidata entry (if eligible)
   - Crunchbase profile
   - Industry directories

2. **Consistent NAP** (Name, Address, Phone):
   - Exact same format everywhere
   - No variations or abbreviations
   - Complete address with ZIP code

3. **Official website**:
   - Clear About page
   - Contact information
   - Company history
   - Team profiles
   - Organization schema on homepage

**For People**:

1. **Professional profiles**:
   - LinkedIn (complete profile)
   - Google Scholar (if academic)
   - ORCID (if researcher)
   - Twitter/X (active presence)
   - Professional association profiles

2. **Author pages**:
   - Dedicated bio page on website
   - Consistent name usage
   - Credentials displayed
   - Photo professional quality
   - Links to publications

3. **Content authorship**:
   - Bylines on all content
   - Author schema on articles
   - Person schema on profile page
   - sameAs links to external profiles

### Step 2: Entity Validation

**Signals Google Uses**:

1. **Citations** (most important):
   - Mentions on other websites
   - News coverage
   - Industry publications
   - Academic papers
   - Social media

2. **Relationships**:
   - Affiliated with known entities
   - Works for established organizations
   - Alumni of recognized institutions
   - Member of professional bodies

3. **Consistency**:
   - Same information across sources
   - No conflicting data
   - Verified profiles
   - Authoritative sources agree

4. **Activity**:
   - Regular content publication
   - Social media engagement
   - Conference participation
   - Industry involvement

### Step 3: Entity Linking

**Internal Linking**:
Link entity mentions to entity pages

**Example**:
```markdown
This research was conducted by [Dr. Sarah Johnson](/about/dr-sarah-johnson),
board-certified physician at [199 Clinic](/about/clinic), in collaboration
with [Stanford School of Medicine](https://med.stanford.edu).
```

**External Linking** (via sameAs):
```json
"sameAs": [
  "https://scholar.google.com/citations?user=ABC123",
  "https://orcid.org/0000-0001-2345-6789",
  "https://linkedin.com/in/sarahjohnsonmd",
  "https://www.wikidata.org/wiki/Q87654321"
]
```

---

## Google Knowledge Graph Optimization

### Getting a Knowledge Panel

**Requirements** (Google's unofficial criteria):

1. **Notability**:
   - Significant media coverage
   - Wikipedia article (if eligible)
   - Wikidata entry
   - Industry recognition

2. **Authority**:
   - Official website
   - Verified social profiles
   - Professional credentials
   - Published works

3. **Consistency**:
   - Identical information across sources
   - No conflicting data
   - Regular content updates

4. **Entity type**:
   - Organization: Easier (register business profiles)
   - Person: Moderate (need public recognition)
   - Concept: Hardest (need widespread adoption)

### Knowledge Panel Optimization

**Once you have a panel**:

1. **Claim your panel**:
   - Search your entity name
   - Click "Claim this knowledge panel"
   - Verify ownership
   - Suggest edits

2. **Complete information**:
   - Logo/profile photo
   - Description
   - Website URL
   - Social profiles
   - Contact information

3. **Keep updated**:
   - Suggest edits for outdated info
   - Add new achievements
   - Update photos periodically
   - Monitor for accuracy

4. **Monitor mentions**:
   - Google Alerts for entity name
   - Track new citations
   - Correct misinformation
   - Build positive coverage

---

## Structured Data Implementation

### Homepage Entity Schema

**Organization Homepage**:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "MedicalBusiness",
  "name": "199 Clinic",
  "url": "https://199clinic.com",
  "logo": "https://199clinic.com/logo.png",
  "description": "Board-certified physicians providing aesthetic medicine, regenerative treatments, and personalized wellness plans in San Francisco.",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Market Street",
    "addressLocality": "San Francisco",
    "addressRegion": "CA",
    "postalCode": "94103"
  },
  "telephone": "+1-415-555-1234",
  "email": "contact@199clinic.com",
  "foundingDate": "2018",
  "sameAs": [
    "https://twitter.com/199clinic",
    "https://linkedin.com/company/199clinic",
    "https://facebook.com/199clinic"
  ],
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "127"
  }
}
</script>
```

### Author Profile Page

**Person Schema on Profile**:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Dr. Sarah Johnson",
  "honorificPrefix": "Dr.",
  "honorificSuffix": "MD, PhD",
  "url": "https://199clinic.com/about/dr-sarah-johnson",
  "image": "https://199clinic.com/images/dr-johnson-profile.jpg",
  "jobTitle": "Board-Certified Physician",
  "worksFor": {
    "@type": "Organization",
    "name": "199 Clinic",
    "url": "https://199clinic.com"
  },
  "alumniOf": {
    "@type": "EducationalOrganization",
    "name": "Harvard Medical School"
  },
  "sameAs": [
    "https://scholar.google.com/citations?user=ABC123",
    "https://linkedin.com/in/sarahjohnsonmd"
  ],
  "knowsAbout": ["Dermatology", "Regenerative Medicine", "Longevity"]
}
</script>
```

### Article with Author Entity

**Link article to author entity**:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Understanding Longevity Biomarkers",
  "author": {
    "@type": "Person",
    "@id": "https://199clinic.com/about/dr-sarah-johnson#person"
  },
  "publisher": {
    "@type": "Organization",
    "@id": "https://199clinic.com/#organization"
  }
}
</script>
```

**Note**: `@id` creates entity references that link together

---

## Entity Relationship Mapping

### Building Entity Networks

**Example Network**:
```
[199 Clinic] (Organization)
    ├─ foundedBy: [Dr. Sarah Johnson] (Person)
    ├─ location: [San Francisco] (Place)
    ├─ memberOf: [American Academy of Anti-Aging Medicine] (Organization)
    └─ offers: [Longevity Medicine] (Service)

[Dr. Sarah Johnson] (Person)
    ├─ worksFor: [199 Clinic] (Organization)
    ├─ alumniOf: [Harvard Medical School] (Organization)
    ├─ affiliation: [Stanford School of Medicine] (Organization)
    └─ knowsAbout: [Regenerative Medicine] (Concept)
```

**Implementation via Schema**:
```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://199clinic.com/#organization",
      "name": "199 Clinic",
      "founder": {
        "@id": "https://199clinic.com/about/dr-sarah-johnson#person"
      }
    },
    {
      "@type": "Person",
      "@id": "https://199clinic.com/about/dr-sarah-johnson#person",
      "name": "Dr. Sarah Johnson",
      "worksFor": {
        "@id": "https://199clinic.com/#organization"
      }
    }
  ]
}
```

---

## Entity SEO Checklist

### Organization Entity

- [ ] Google Business Profile claimed and optimized
- [ ] Consistent NAP across all citations
- [ ] Organization schema on homepage
- [ ] Logo 1:1 ratio, high quality
- [ ] Social profiles linked (sameAs)
- [ ] About page with company history
- [ ] Contact page with full address
- [ ] Wikipedia/Wikidata entry (if eligible)
- [ ] Industry directory listings
- [ ] Press coverage and media mentions

### Person Entity

- [ ] Dedicated profile page on website
- [ ] Person schema on profile page
- [ ] Professional headshot (high quality)
- [ ] Credentials clearly displayed
- [ ] LinkedIn profile complete and public
- [ ] Google Scholar profile (if applicable)
- [ ] ORCID (if researcher)
- [ ] Author bylines on all content
- [ ] External profile links (sameAs)
- [ ] Bio with expertise areas (knowsAbout)

### Content Integration

- [ ] Author schema on all articles
- [ ] Entity mentions linked internally
- [ ] Consistent entity references
- [ ] Schema relationships defined (@id)
- [ ] BreadcrumbList showing structure
- [ ] Topic cluster internal linking
- [ ] Entity-rich anchor text

---

## AI Citation Impact

### How Entities Improve AI Citations

**ChatGPT**:
- Prioritizes known entities
- Values institutional affiliations
- Requires author credentials
- +40% citation boost with recognized entities

**Perplexity**:
- Links to entity profiles
- Shows entity relationships
- Validates through Wikipedia/Wikidata
- Prefers entities with external validation

**Claude**:
- Validates entity credentials
- Checks institutional affiliations
- Requires primary source linkage
- Prioritizes academic entities

**Gemini**:
- Integrates with Knowledge Graph directly
- Uses GMB data heavily
- Values local entities
- Prioritizes community-validated entities

---

## Measurement & Monitoring

### Entity Tracking

**Google Search Console**:
- Monitor branded queries
- Track entity-related keywords
- Check Knowledge Graph presence

**Google Alerts**:
- Entity name mentions
- Brand monitoring
- Competitor entity tracking

**Manual Checks**:
- Search entity name monthly
- Verify Knowledge Panel accuracy
- Check entity relationships
- Monitor competing entities

### Success Metrics

**Month 1-2**:
- Organization schema implemented
- Person schemas for key authors
- Google Business Profile optimized
- Social profiles linked

**Month 3-4**:
- Entity citations appearing
- Knowledge Panel (if eligible)
- Branded search increase
- Entity-rich snippets

**Month 6+**:
- Established entity recognition
- AI platforms citing entity
- Knowledge Panel ownership
- Entity network built

---

**Last Updated**: November 11, 2025
**Next Review**: Quarterly
**Resources**: Google Knowledge Graph, Wikidata, Schema.org
