---
name: alterlab-bgpt-search
description: Search scientific papers and retrieve structured experimental data extracted from full-text studies via the BGPT MCP server, returning 25+ fields per paper (methods, results, sample sizes, quality scores, conclusions). Use when running a literature review or evidence synthesis, or when needing experimental details (sample sizes, effect sizes, methods, quality scores) that abstracts alone do not provide. Part of the AlterLab Academic Skills suite.
allowed-tools: Bash
license: MIT
compatibility: Connects to the BGPT MCP server. Free tier allows 50 free results with no API key; higher volume needs a BGPT API key from bgpt.pro/mcp. Requires network access.
metadata:
    skill-author: AlterLab
    version: "1.0.1"
    skill-source: https://github.com/connerlambden/bgpt-mcp
---

# BGPT Paper Search

## Overview

BGPT is a remote MCP server that searches a curated database of scientific papers built from raw experimental data extracted from full-text studies. Unlike traditional literature databases that return titles and abstracts, BGPT returns structured data from the actual paper content — methods, quantitative results, sample sizes, quality assessments, and 25+ metadata fields per paper.

## When to Use This Skill

Use BGPT when the value is in structured full-text experimental data, not titles/abstracts:
- Building evidence tables for a meta-analysis, scoping review, or clinical guideline
- Extracting sample sizes, effect sizes, methods, protocols, or conclusions across studies
- Comparing methodologies, or filtering papers by quality score / evidence grading

For broad title/abstract discovery use `alterlab-pubmed`; for real-time web-grounded summaries of recent developments use `alterlab-perplexity`.

## Setup

BGPT is a remote MCP server — no local installation required.

### Claude Desktop / Claude Code

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "bgpt": {
      "command": "npx",
      "args": ["mcp-remote", "https://bgpt.pro/mcp/sse"]
    }
  }
}
```

### npm (alternative)

```bash
npx bgpt-mcp
```

## Usage

Once configured, use the `search_papers` tool provided by the BGPT MCP server:

```
Search for papers about: "CRISPR gene editing efficiency in human cells"
```

The server returns structured results including:
- **Title, authors, journal, year, DOI**
- **Methods**: Experimental techniques, models, protocols
- **Results**: Key findings with quantitative data
- **Sample sizes**: Number of subjects/samples
- **Quality scores**: Study quality assessments
- **Conclusions**: Author conclusions and implications

## Pricing

- **Free tier**: 50 free results, no API key required
- **Paid**: $0.02 per result (billed per result actually returned, not per search) with an API key from [bgpt.pro/mcp](https://bgpt.pro/mcp)

## Complementary Skills

Pairs well with:
- `alterlab-literature-review` — gather structured data with BGPT, then synthesize
- `alterlab-pubmed` — PubMed for broad discovery, BGPT for deep experimental data
- `alterlab-biorxiv` — combine preprint discovery with full-text data extraction
- `alterlab-pyzotero` — manage citations from BGPT search results
