---
name: alterlab-citation-verifier
description: "Verifies that every entry in a bibliography ACTUALLY EXISTS by cross-checking it against four keyless public scholarly APIs (Crossref, OpenAlex, Semantic Scholar, arXiv) with a polite mailto identifier, resolving DOI/arXiv IDs, fuzzy-matching title and authors (difflib SequenceMatcher ratio >=0.70), flagging retractions marked in Crossref (update-to) or OpenAlex (is_retracted), and emitting per-entry JSON verdicts mapped to the AlterLab citation-hallucination taxonomy (TF/PAC/IH/PH/SH). Accepts BibTeX, a DOI/arXiv ID list, or free-form references; degrades gracefully offline by emitting 'unverified' verdicts and never silently passing. Use when the request mentions verify citations, check references, fabricated or hallucinated references, fake DOI, retraction check, bibliography audit, or reference existence check. Does NOT write or draft papers — for authoring a manuscript (whose citation-check mode inserts citations) prefer alterlab-paper-writer instead. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash WebSearch WebFetch
compatibility: No API key required — cross-checks four keyless public scholarly APIs (Crossref, OpenAlex, Semantic Scholar, arXiv) via WebFetch and `uv run python`; degrades gracefully offline to 'unverified' verdicts
metadata:
  skill-author: AlterLab
  version: "1.0.0"
  last_updated: "2026-06-06"
  depends_on: "alterlab-research-pipeline (shares the integrity taxonomy), alterlab-deep-research"
---

# Citation Verifier — Existence-Verify a Bibliography Against Public Scholarly APIs

The headline existence-verification skill: given a bibliography in any common
form, it proves entry-by-entry whether each reference **actually exists** by
querying four keyless public scholarly APIs, then maps each result to the
canonical AlterLab citation-hallucination taxonomy. It is the deterministic,
network-grounded companion to the LLM-driven `integrity_verification_agent` —
where that agent uses WebSearch + judgment, this skill uses authoritative API
records and a reproducible Python script, so the same input always yields the
same verdicts.

## Quick Start

```
Verify the citations in references.bib
Check whether these DOIs resolve to the papers I cited
Audit my bibliography for fabricated / hallucinated references
Does this reference list contain any fake citations or retractions?
```

→ Run `scripts/verify_citations.py` over the bibliography, read the JSON, then
present a verdict table grouped by severity. Always state the offline/degraded
status explicitly if the network was unavailable.

---

## WHAT This Does

For each bibliography entry the script:

1. **Parses** the input (auto-detects BibTeX / DOI-list / free-form), extracting
   title, authors, year, venue, DOI, and arXiv ID.
2. **Resolves identifiers** — looks up the cited DOI/arXiv ID directly when present.
3. **Searches by title** as a fallback across all four sources.
4. **Fuzzy-matches** the cited title (difflib `SequenceMatcher` ratio, default
   threshold **0.70**) and computes author-surname overlap.
5. **Flags retractions** marked in Crossref (`update-to: retraction`) or OpenAlex
   (`is_retracted`).
6. **Emits a verdict** per entry mapped to the taxonomy below, plus a repo-level
   `summary.verdict` (PASS / PASS_WITH_CONDITIONS / FAIL / UNVERIFIED).

### The four sources (all keyless, polite-pool)

| Source | Endpoint | Used for |
|--------|----------|----------|
| Crossref | `api.crossref.org/works` | DOI resolution, metadata, **retraction flag** |
| OpenAlex | `api.openalex.org/works` | DOI + title search, **`is_retracted`** |
| Semantic Scholar | `api.semanticscholar.org/graph/v1` | DOI/arXiv resolution, title search |
| arXiv | `export.arxiv.org/api/query` | arXiv ID resolution, preprint title search |

All requests carry a `mailto` parameter (defaults to `alterlab.ieu@gmail.com`)
to stay in each API's polite pool. **No API keys are required or used.**

## WHEN To Use It (and when not)

| Use this skill | Use something else |
|----------------|--------------------|
| "Verify / check / audit my citations or references exist" | Writing the paper → `alterlab-paper-writer` |
| "Did the AI hallucinate any of these references?" | Full integrity gate inside a pipeline → `alterlab-research-pipeline` Stage 2.5/4.5 |
| "Do these DOIs resolve to the papers I cited?" | Grading source quality / predatory journals → `alterlab-deep-research` `source_verification_agent` |
| "Check this bibliography for retractions" | Whether a claim is *supported* by its source (SH) → `claim_verification_protocol` (Phase E) |
| Reproducible, scriptable, offline-capable existence check | Markdown dead-link audit → `alterlab-link-health` |

This skill answers **"does the cited work exist, and does its identifier point
to it?"** It does **not** read the cited paper's full text, so it cannot by
itself confirm Semantic Hallucination (does the source support the claim?) —
that requires `claim_verification_protocol`. SH is surfaced only as an advisory
flag, never asserted from API metadata alone.

---

## Verdict Taxonomy (mirrors the canonical Five-Type Taxonomy)

Identical codes and definitions to
`alterlab-research-pipeline/agents/integrity_verification_agent.md`
(GPTZero × NeurIPS 2025; Ansari, 2026). Severity feeds the same
SERIOUS / MEDIUM / MINOR scale used in the Integrity Report schema.

| Code | Name | Severity | Script trigger |
|------|------|----------|----------------|
| `verified` | — (exists, matches) | NONE | Title ratio >= threshold AND author overlap OK AND year consistent in >=1 authoritative source |
| `TF` | Total Fabrication | **SERIOUS** | Found in **no** source; OR cited DOI/arXiv ID did not resolve anywhere and no close title match exists |
| `PAC` | Partial Attribute Corruption | MEDIUM | Entry found but >=1 metadata field disagrees (year mismatch, author overlap < 50%, or title ratio < threshold) |
| `IH` | Identifier Hijacking | **SERIOUS** | Cited DOI/arXiv ID **resolved** (method=id) but the resolved record's title is unrelated (ratio < threshold) |
| `PH` | Placeholder Hallucination | **SERIOUS** | Unresolved template/placeholder (`[CITATION NEEDED]`, `\cite{}`, `et al., YYYY`, `TODO`, `forthcoming`) — caught pre-network |
| `SH` | Semantic Hallucination | **SERIOUS** | Entry resolves but does not support its claim — **advisory only**; requires Phase E to assert |
| `unverified` | — (could not check) | MEDIUM | Offline, or all APIs failed for this entry. **Never treated as passing.** |

A `RETRACTED` flag is attached (and severity bumped to SERIOUS) whenever Crossref
or OpenAlex marks the matched work as retracted, independent of the existence
verdict.

### Repo-level verdict

- **PASS** — every entry `verified`, no SERIOUS/MEDIUM flags.
- **PASS_WITH_CONDITIONS** — only `PAC` / MEDIUM issues (wrong metadata, fixable).
- **FAIL** — any SERIOUS verdict (`TF` / `IH` / `PH` / retraction).
- **UNVERIFIED** — entries are `unverified` and no concrete fabrication was found
  (e.g. fully offline run). This is **not** a pass — re-run with network access.

---

## Pipeline (how to run it)

### 1. Locate or capture the bibliography

Accept any of: a `.bib` file, a `.txt` list of DOIs/arXiv IDs, a pasted
reference list, or inline text. The script auto-detects the format; override
with `--format bibtex|doi|freeform` if detection is wrong.

### 2. Run the verifier

```bash
uv run python skills/core/alterlab-citation-verifier/scripts/verify_citations.py \
    path/to/references.bib \
    --mailto alterlab.ieu@gmail.com \
    --threshold 0.70 \
    --out citation_report.json
```

- `path/to/references.bib` may also be `-` (stdin) or inline text.
- `--threshold` tunes the fuzzy title-match ratio (0..1; default 0.70).
- `--offline` skips the network and emits `unverified` verdicts deliberately.
- Omit `--out` to print the JSON report to stdout.

The script auto-selects an HTTP backend: it uses `requests` if installed, else
falls back to the Python stdlib (`urllib`) — so it runs with **zero extra
dependencies** in a bare `uv` environment.

### 3. Read the JSON and report

Parse `summary.verdict` and the per-entry `verdict` codes. Present:

1. The **headline verdict** and counts (`verdict_counts`, `severity_counts`).
2. A **table of every non-`verified` entry** with its code, severity, and `detail`.
3. For each `TF` / `IH` / `PH`: quote the cited entry and explain the evidence
   (e.g. "DOI 10.x resolved to an unrelated paper titled '…'").
4. Any `RETRACTED` flags, prominently.
5. If `verdict == UNVERIFIED`: state plainly that nothing was confirmed and relay
   the per-entry `manual_instructions`.

### 4. Route fixes

- `TF` / `PH` → the reference must be removed or replaced; it does not exist.
- `IH` → the DOI/arXiv ID is wrong; find and substitute the correct identifier.
- `PAC` → correct the specific metadata field(s) named in `detail`.
- `RETRACTED` → flag to the author; cite the retraction notice or drop the source.

---

## Graceful Degradation (no network)

Network failures are **never** silently swallowed into a pass:

- A DNS/connection failure raises `NetworkUnavailable`; the entry becomes
  `unverified` with a populated `manual_instructions` field.
- `--offline` forces every networked entry to `unverified` up front (placeholders
  are still caught locally as `PH`).
- The repo-level verdict becomes `UNVERIFIED` (distinct from `PASS`) whenever
  unverified entries exist without any concrete fabrication finding.

When degraded, instruct the user to re-run with connectivity, and fall back to
the LLM-driven `integrity_verification_agent` (WebSearch) for a manual pass.

---

## Output Shape (excerpt)

```json
{
  "tool": "alterlab-citation-verifier/verify_citations.py",
  "version": "1.0.0",
  "summary": {
    "total": 2,
    "verdict": "FAIL",
    "verdict_counts": {"verified": 1, "TF": 1, "PAC": 0, "IH": 0, "PH": 0, "SH": 0, "unverified": 0},
    "severity_counts": {"SERIOUS": 1, "MEDIUM": 0, "MINOR": 0},
    "citation_integrity_score": 0.5,
    "fabrication_risk_score": 0.5,
    "retracted": 0
  },
  "entries": [
    {"ref_id": "walters2023", "verdict": "verified", "severity": "NONE",
     "title_ratio": 1.0, "author_overlap": 1.0, "matches": [{"source": "crossref"}]},
    {"ref_id": "ghostpaper2021", "verdict": "TF", "severity": "SERIOUS",
     "detail": "Cited DOI/arXiv identifier did not resolve in any source..."}
  ]
}
```

`citation_integrity_score` and `fabrication_risk_score` (both 0..1) align with
the Integrity Report schema fields of the same name, so the report can feed
`alterlab-research-pipeline`'s integrity gate directly.

---

## Self-Check Before Reporting

- Did the run reach the network? If `config.http_backend` ran but every entry is
  `unverified`, the network was down — say so; do not imply a pass.
- Are there any `RETRACTED` flags? Surface them even on otherwise-`verified` entries.
- Did any entry score `IH`? Confirm the detail shows an **id-resolved** mismatch,
  not a loose title-search coincidence (the script enforces this distinction).
- Is the headline verdict consistent with the per-entry codes (any SERIOUS → FAIL)?

---

## References

- `alterlab-research-pipeline/agents/integrity_verification_agent.md` — canonical
  Five-Type Taxonomy, compound-deception patterns, and the Lin et al. (2020)
  mashup case study this skill is built to catch.
- `alterlab-research-pipeline/references/claim_verification_protocol.md` — Phase E
  claim-vs-source verification (the SH check this skill defers to).
- `shared/schemas/integrity_report.schema.json` — the integrity-report shape whose
  `citation_integrity_score` / `fabrication_risk_score` this skill mirrors.
- Walters, W. H., & Wilder, E. I. (2023). Fabrication and errors in the
  bibliographic citations generated by ChatGPT. *Scientific Reports, 13*, 14045.
  https://doi.org/10.1038/s41598-023-41032-5
- Ansari, S. (2026). Compound Deception in Elite Peer Review. *arXiv:2602.05930*.
