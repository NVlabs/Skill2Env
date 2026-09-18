---
name: alterlab-digital-humanities
description: "Applies computational methods to humanities research — text mining and NLP (LDA/BERTopic topic modeling, sentiment, named entity recognition with spaCy/NLTK), corpus linguistics (concordance, collocation, keyness), digital archives (Dublin Core, TEI XML), GIS for history, network analysis, stylometry and authorship attribution, OCR (Tesseract, Kraken, Transkribus), and data visualization (Gephi, Palladio). Use when distant-reading a literary corpus, mapping historical events or trade networks, attributing disputed authorship, digitizing historical documents, or building digital scholarly editions. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Write Edit Bash(python:*)
compatibility: No API key required. Guidance-focused skill; optional NLP/OCR Python tooling (spaCy, NLTK, Tesseract) runs locally via `uv run python`.
metadata:
  skill-author: AlterLab
  version: "1.0.0"
  last_updated: "2026-03-18"
---

# Digital Humanities Methods and Tools

## Overview

Digital humanities (DH) applies computational methods to the study of human culture, history, language, and society. It is not the replacement of humanistic inquiry with algorithms but the augmentation of interpretive scholarship with tools that can reveal patterns invisible to unaided reading, connect dispersed archives, visualize historical processes, and make cultural heritage accessible to broader audiences.

This skill covers the major computational methods used in humanities research: text mining and natural language processing (topic modeling with LDA and BERTopic, sentiment analysis, named entity recognition), corpus linguistics (concordance, collocation, frequency analysis, keyness), digital archiving and metadata standards (Dublin Core, TEI XML), geographic information systems (GIS) for historical research, network analysis of historical figures and literary characters, stylometry and computational authorship attribution, optical character recognition (OCR) workflows for digitizing historical texts, digital scholarly editions, data visualization for humanities data, distant reading as theorized by Franco Moretti, cultural analytics as developed by Lev Manovich, and the Python ecosystem for humanities computing (spaCy, NLTK, Voyant Tools, AntConc).

The skill is designed for humanities scholars who want to integrate computational methods into their research -- whether they are analyzing Victorian novels, mapping colonial trade networks, studying the evolution of political rhetoric, or building digital archives of endangered languages. No prior programming experience is assumed, though some methods require basic Python or R skills. For each method, the skill describes the intellectual rationale, practical implementation, available tools (from no-code to full programming), and critical perspectives on the method's limitations.

## When to Use This Skill

Use this skill when you need to:

- Apply topic modeling (LDA, BERTopic) to a large text corpus to discover thematic patterns
- Perform sentiment analysis on historical texts, literary works, or political discourse
- Extract named entities (people, places, organizations, dates) from unstructured text
- Conduct corpus linguistics analysis: concordance, collocation, frequency, keyness
- Create or work with digital archives using Dublin Core or TEI XML metadata standards
- Use GIS to map historical events, trade routes, migration patterns, or spatial narratives
- Build and analyze networks of historical figures, literary characters, or intellectual influence
- Attribute authorship of disputed texts using stylometry and computational methods
- Digitize historical documents using OCR (Tesseract, Kraken, Transkribus)
- Create digital scholarly editions with critical apparatus
- Visualize humanities data using Palladio, Gephi, or custom tools
- Apply distant reading methods to analyze literary trends across large corpora
- Conduct cultural analytics on visual media, social media, or digital culture
- Work with Python NLP tools (spaCy, NLTK) for humanities text analysis

## Core Capabilities

Each capability below gives the WHAT/WHEN and the tools to reach for. Worked examples, code, parameter tables, and tool-comparison matrices live in the references (see the index at the end).

### Text Mining and NLP

NLP analyzes text at scales impossible for human readers — not a replacement for close reading but a complement that identifies patterns across thousands of texts and guides which passages to read closely.

- **Topic modeling** — discover latent themes. **LDA** (bag-of-words, specify k) for classic distant reading; **BERTopic** (transformer embeddings + HDBSCAN, auto k) for short/modern text and semantic coherence.
- **Sentiment analysis** — emotional valence over a text (e.g. a novel's emotional arc). Lexicon (VADER/NRC) → ML → transformer, in increasing accuracy and cost. Validate against human annotation; modern models misclassify historical prose.
- **Named entity recognition (NER)** — extract people, places, organizations, dates. spaCy is the best general-purpose tool; fine-tune on annotated historical text for archaic spelling and unfamiliar entities.

→ `references/methods-and-examples.md` (LDA workflow + example, BERTopic code, sentiment-arc code, NER tools + fine-tuning code).

### Corpus Linguistics

Empirical analysis of large, structured text collections.

- **Concordance (KWIC)** — every occurrence of a term in context; reveals usage patterns and collocates.
- **Collocation** — statistically significant co-occurring words (MI, t-score, log-likelihood, Log Dice).
- **Frequency and keyness** — keyness compares two corpora to surface what is distinctive about one.
- Tools: AntConc and Voyant (no-code), Sketch Engine / CQPweb (web), NLTK / quanteda (programmable).

→ `references/methods-and-examples.md` (KWIC/keyness examples, measure-comparison and software tables) and `references/dh-tools-guide.md` (AntConc and Voyant panel references, statistical measures).

### Digital Archives and Metadata

- **Dublin Core** — 15-element universal metadata vocabulary for describing digital resources.
- **TEI XML** — the standard for encoding literary/historical texts and building digital scholarly editions (`<persName>`, `<placeName>`, `<app>`/`<rdg>` apparatus, `<del>`/`<add>`, `<unclear>`, `<gap>`, `<choice>`).

→ `references/methods-and-examples.md` (Dublin Core element table, full TEI document example, key-element table) and `references/dh-tools-guide.md` (essential TEI elements).

### GIS for Historical Research

Spatial analysis of historical data — georeferencing old maps, event/trade-route mapping, literary geography, urban and environmental history. QGIS (free, full-featured) or ArcGIS; Palladio for humanities-friendly map+network views.

→ `references/methods-and-examples.md` (tool table, georeferencing workflow) and `references/dh-tools-guide.md` (detailed QGIS georeferencing).

### Network Analysis for Historical Figures

Reveals connection, influence, and community structure among historical actors (correspondence, co-occurrence, citation, kinship, trade, organizational networks). Build an edge list, then analyze in Gephi, NetworkX, or igraph (centrality, community detection, temporal filtering).

→ `references/methods-and-examples.md` (network-type table, source-to-edge-list workflow).

### Stylometry and Authorship Attribution

Statistical analysis of writing style — especially function-word frequencies — to attribute disputed texts. **Burrows Delta** (z-scores of most-frequent words) is the dominant method; run via the `stylo` R package, PyDelta, or JGAAP. Needs 2,000-5,000+ words per sample and genre-matched comparisons.

→ `references/methods-and-examples.md` (feature/tool tables, Delta algorithm, stylo R example) and `references/dh-tools-guide.md` (complete stylo guide).

### OCR Workflows

Convert images of text to machine-readable text; OCR quality is critical for all downstream analysis. Tesseract (general), Kraken (historical/non-Latin scripts), Transkribus (handwriting/HTR). Always report Character Error Rate (target CER < 5%, ideally < 2%).

→ `references/methods-and-examples.md` (engine table, prep→process→post→QA workflow, Tesseract commands) and `references/dh-tools-guide.md` (Tesseract/Kraken/Transkribus configuration).

### Digital Scholarly Editions

Primary texts with critical apparatus, annotation, facsimiles, search, and stable identifiers — beyond digitized facsimiles. Platforms: EVT, Versioning Machine, TextGrid, FromThePage, Scripto, IIIF.

→ `references/methods-and-examples.md` (components list, platform table).

### Data Visualization for Humanities

Visualization serves both analysis and argument. Palladio (maps/networks/timelines), Gephi (networks), Voyant (text), StoryMapJS/TimelineJS (narrative), D3.js (custom). Treat uncertainty as data, integrate visuals into argument, use accessible palettes, document for reproducibility.

→ `references/methods-and-examples.md` (tool table, visualization principles).

### Distant Reading and Cultural Analytics

- **Distant reading** (Moretti) — quantitative analysis of large literary corpora: genre trends, title analysis, plot/sentiment trajectories, character networks, stylistic change over literary history.
- **Cultural analytics** (Manovich) — extends distant reading to images, video, social media, and interface design using OpenCV, Pillow, scikit-image, and related tools.

→ `references/methods-and-examples.md` (methods, Moretti's arguments, cultural-analytics Python tools).

### Python Tools for Humanities Computing

spaCy (industrial NLP: NER, POS, dependency parsing, lemmatization), NLTK (educational corpora, frequency, concordance, collocations), plus no-code Voyant and desktop AntConc.

→ `references/methods-and-examples.md` (spaCy and NLTK code, Voyant/AntConc capability summaries).

## Best Practices and Pitfalls

- **Start with a humanistic question**; choose the simplest tool that works; learn iteratively; document every corpus, preprocessing, and parameter decision; validate computational patterns with close reading.
- **Corpus construction is an argument** — justify inclusion/exclusion. Report OCR error rates and preprocessing choices. Preserve raw originals separately.
- **Interpretation is required** — topic models and visualizations do not speak for themselves; acknowledge each method's blind spots and situate findings in disciplinary scholarship.
- **Common pitfalls:** black-box NLP use; anachronistic sentiment models on historical text; overclaiming from topics; small corpus with big claims; false geographic precision; stylometry with too little text or genre contamination.

→ `references/methods-and-examples.md` (full Best Practices and Pitfalls checklists) and `references/dh-tools-guide.md` (recommended project workflows by scale).

## Reference Index

- **`references/methods-and-examples.md`** — worked examples, code (LDA/BERTopic/sentiment/NER/spaCy/NLTK/stylo/Tesseract), parameter and tool-comparison tables, the full TEI document example, and complete Best-Practices/Pitfalls/References sections.
- **`references/dh-tools-guide.md`** — tool comparison matrix, topic-modeling parameter tuning, AntConc/Voyant panel references, OCR engine configuration (Tesseract/Kraken/Transkribus), essential TEI elements, QGIS georeferencing, the complete `stylo` R guide, recommended project workflows by scale, and further reading.

## References (selected)

- Moretti, F. (2005). *Graphs, Maps, Trees*. Verso. — (2013). *Distant Reading*. Verso.
- Manovich, L. (2020). *Cultural Analytics*. MIT Press.
- Blei, D. M., Ng, A. Y., & Jordan, M. I. (2003). Latent Dirichlet Allocation. *JMLR*, 3, 993-1022.
- Grootendorst, M. (2022). BERTopic. *arXiv*:2203.05794.
- Burrows, J. (2002). Delta. *Literary and Linguistic Computing*, 17(3), 267-287.
- Burnard, L., & Bauman, S. (Eds.). (2023). *TEI P5 Guidelines*. TEI Consortium.

Full bibliography in `references/methods-and-examples.md`.
