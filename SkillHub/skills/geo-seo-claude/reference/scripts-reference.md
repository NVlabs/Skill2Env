# SEO/GEO/AEO Scripts Reference

## Quick Start

```bash
# Full audit report (JSON, Markdown, HTML)
python scripts/audit_report.py ~/project/page.html --format all
# Output: ~/Documents/SEO_Audit_YYYY-MM-DD_HH-MM-SS/
```

## Phase 1: Analysis Scripts

| Script | Usage | Description |
|--------|-------|-------------|
| `analyze_content.py` | `<file>` | Extract metadata, schema, structure |
| `metadata_validator.py` | `<file>` | Validate meta tags, OG, Twitter Cards |
| `keyword_analyzer.py` | `<file> [--no-clusters]` | Extract keywords with semantic clustering |
| `entity_extractor.py` | `<file>` | Extract entities for Knowledge Graph |
| `audit_report.py` | `<file> --format [json\|md\|html\|all]` | Generate comprehensive reports |

## Phase 2: Implementation Scripts

| Script | Usage | Description |
|--------|-------|-------------|
| `content_optimizer.py` | `<file>` | Rewrite meta description, FAQ, data tables |
| `platform_optimizer.py` | `<file> <platform>` | Platform-specific optimization |
| `voice_optimizer.py` | `<file>` | Add Speakable schema for voice search |
| `freshness_monitor.py` | `<file>` | Check content age, recommend updates |
| `citation_enhancer.py` | `<file>` | Identify citation opportunities (+41% impact) |
| `auto_implementer.py` | `<file> [platform]` | Full optimization pipeline |

**Platforms**: chatgpt, perplexity, claude, gemini, grokipedia

## Schema Generation

```bash
# FAQ Schema (highest AI citation probability)
python scripts/schema_generator.py faq \
  --question "What is optimal LDL?" \
  --answer "Optimal LDL for longevity is <70 mg/dL."

# Article Schema with E-E-A-T
python scripts/schema_generator.py article \
  --title "Title" --author "Dr. Name" --credentials "MD, PhD" --date "2025-01-15"
```

**Schema Types**: faq, article, howto, breadcrumb, organization, person

## IndexNow Instant Indexing

```bash
# Generate key (one-time)
python scripts/indexnow_submit.py --generate-key --output ./public

# Submit URL
python scripts/indexnow_submit.py https://yoursite.com/page --key YOUR_KEY

# Batch submit
python scripts/indexnow_submit.py --batch urls.txt --key YOUR_KEY
```

## Performance

- All scripts: <2 seconds execution
- `audit_report.py`: 3-5 seconds
- Python 3.7+ stdlib only, works offline

## Supported Formats

**Input**: HTML, Markdown, React/JSX
**Output**: JSON, Markdown, HTML
