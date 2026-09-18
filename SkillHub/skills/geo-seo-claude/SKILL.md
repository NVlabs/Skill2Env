---
name: geo-seo-claude
description: Audit and optimize content for SEO, GEO (generative engine optimization), and AEO (answer engine optimization). Use when user asks to "audit SEO", "check search visibility", "optimize for AI search", "generate schema markup", "validate metadata", "extract keywords", "optimize for Perplexity/ChatGPT/Gemini", "check Open Graph tags", "submit to IndexNow", or mentions SEO, GEO, AEO, or search optimization. Do NOT use for creating new content from scratch or image optimization.
---

# SEO/GEO/AEO Optimizer

Audit content for search engine and AI platform visibility. Generates schema markup, validates metadata, extracts keywords, and produces actionable reports.

## When NOT to Use

- Creating new content from scratch (use content generation tools)
- Image optimization (use image-specific tools)
- Server-side performance (use web performance tools)

## Decision Matrix

Pick the right script based on user intent:

| User Wants | Script | Input |
|-----------|--------|-------|
| Full audit with report | `scripts/audit_report.py <file> --format all` | HTML/MD/JSX |
| Content structure analysis | `scripts/analyze_content.py <file>` | HTML/MD/JSX |
| Meta tag validation | `scripts/metadata_validator.py <file>` | HTML |
| Keyword extraction | `scripts/keyword_analyzer.py <file>` | Any text |
| Entity extraction | `scripts/entity_extractor.py <file>` | Any text |
| Schema markup generation | `scripts/schema_generator.py <type> [args]` | CLI args |
| AI platform optimization | `scripts/auto_implementer.py <file> <platform>` | HTML + platform |
| Content optimization | `scripts/content_optimizer.py <file>` | HTML/MD |
| Citation enhancement | `scripts/citation_enhancer.py <file>` | HTML/MD |
| Voice search optimization | `scripts/voice_optimizer.py <file>` | HTML/MD |
| Freshness monitoring | `scripts/freshness_monitor.py <file>` | HTML |
| IndexNow submission | `scripts/indexnow_submit.py <url>` | URL |

**Platforms for auto_implementer**: chatgpt, perplexity, claude, gemini, grokipedia

**Schema types**: faq, article, howto, organization, person

## Preflight

Before running any script, verify:
1. File exists and is a supported type (.html, .md, .mdx, .jsx, .tsx)
2. Python 3.7+ available (scripts use stdlib only, no external deps)

## Error Handling

- **FileNotFoundError**: Check the path. Scripts accept absolute or relative paths.
- **JSON decode errors**: The input file may have malformed schema markup. Run `metadata_validator.py` first to identify issues.
- **Low scores (< 50)**: Not an error. Run `audit_report.py --format all` for detailed recommendations, then apply fixes with `auto_implementer.py`.
- **Script import errors**: All scripts share `scripts/shared/` utilities. Ensure the full scripts directory is intact.

## Output

Reports saved to `~/Documents/SEO_Audit_YYYY-MM-DD_HH-MM-SS/` in three formats:
- **JSON**: Raw audit data for programmatic use
- **Markdown**: Readable report with recommendations
- **HTML**: Visual dashboard with scores and charts

## References

| File | When to Read |
|------|-------------|
| `reference/scripts-reference.md` | Detailed script flags and options |
| `reference/troubleshooting.md` | Common issues and solutions |
| `reference/platform-strategies.md` | Platform-specific optimization strategies |
| `reference/citation-optimization-guide.md` | AI citation and GEO strategies |
| `reference/schema-library.md` | Complete JSON-LD schema reference |
| `reference/entity-seo-guide.md` | Knowledge Graph optimization |
| `reference/voice-search-guide.md` | Voice search and AEO optimization |
| `reference/social-preview-guide.md` | Open Graph and Twitter Card setup |
| `reference/statistics-2026.md` | May 2026 review — what shifted, what survived, what to drop |
