# SEO/GEO/AEO Troubleshooting Guide

## Low AI Citation Rate

**Solutions**:
1. Add TL;DR in first 60 words (+35% boost)
2. Display author credentials (MD, PhD) (+40% boost)
3. Link to primary sources (PubMed, arXiv)
4. Update `dateModified` weekly
5. Add FAQ schema (highest citation probability)

## Metadata Issues

### Title Too Short
- Expand to 50-60 characters with brand name

### Missing og:image
- Add 1200x630px image for social previews
- Use absolute URLs (https://...)

### No Schema Markup
- Generate FAQ/Article schema for AI citation
- Use `python scripts/schema_generator.py`

## Poor Social Media Previews

**Solutions**:
1. Add 1200x630px og:image (Facebook, LinkedIn, WhatsApp)
2. Use absolute URLs (https://...)
3. Include og:title and og:description
4. Test with platform validators:
   - Facebook: developers.facebook.com/tools/debug/
   - Twitter: cards-dev.twitter.com/validator
   - LinkedIn: linkedin.com/post-inspector/

## Knowledge Graph Not Showing

**Solutions**:
1. Add Organization schema to homepage
2. Create Person schema for key individuals
3. Ensure NAP consistency across web
4. Link external profiles (LinkedIn, Wikipedia)
5. Claim Google Business Profile

## Low Keyword Optimization Score

**Tips**:
- Primary keyword density: 1-3% (avoid stuffing)
- Add 3+ question keywords for voice search
- Long-tail phrases (3-4 words) for specificity
- Use keyword clusters for pillar content strategy

## E-E-A-T Signals Weak

**Enhancement**:
```markdown
**Author**: Dr. Sarah Johnson, MD, PhD, FAAD
**Affiliation**: Stanford School of Medicine
**Published**: 2025-01-15 | **Updated**: 2025-11-11
```

- Add full names with credentials
- Include institutional affiliations
- Link to external profiles (Google Scholar, LinkedIn)

## Voice Search Not Working

- Answers must be <=29 words
- Use natural language questions
- Provide direct, specific answers
- Add Speakable schema with `voice_optimizer.py`
