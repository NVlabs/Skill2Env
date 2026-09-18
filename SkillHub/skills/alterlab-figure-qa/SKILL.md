---
name: alterlab-figure-qa
description: Verify publication figures with a render-then-check QA pass — data-fidelity against every underlying row, axis/label floor-and-ceiling legibility, bounding-box collision detection for overlapping text/markers, and 300-dpi print-readiness. Use when proofing or auditing a finished figure for correctness and print quality, catching mislabeled or overlapping elements, or confirming a plot faithfully represents its data before submission. For CREATING the plot prefer alterlab-matplotlib (or alterlab-seaborn / alterlab-plotly); for multi-panel publication layout prefer alterlab-scientific-viz; for schematic diagrams prefer alterlab-scientific-schematics. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: "Runs under `uv run python` with the plotting stack already used to make the figure (Matplotlib and, for image/text-box checks, Pillow). No GPU, no account. Operates on a rendered figure plus the source data — it re-renders and inspects, it does not need network access."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# Figure QA (render-then-verify)

## Overview

A finished figure can look fine and still be wrong: a series plotted from the wrong column,
a legend covering a data point, tick labels clipped at the axis edge, or a 150-dpi export that
pixelates in print. This skill is a **render-then-verify** QA pass — it re-renders the figure
and checks it against a concrete, measurable checklist before submission. It **complements**
the plotting skills (which *make* figures); it does not create plots.

## When to Use This Skill

Use this skill when the user wants to:
- **Proof a finished figure** for correctness and print-readiness before submission.
- Confirm the plot **faithfully represents its data** (every row/series accounted for).
- Catch **overlapping or clipped** labels, legends, and markers.
- Verify **resolution / export** settings (e.g. 300 dpi, vector where required).

### Does NOT Trigger

| Scenario | Use instead |
|----------|-------------|
| Create/plot the figure in the first place | `alterlab-matplotlib` / `alterlab-seaborn` / `alterlab-plotly` |
| Lay out a multi-panel publication figure | `alterlab-scientific-viz` |
| Draw a schematic / diagram | `alterlab-scientific-schematics` |
| Build an infographic | `alterlab-infographics` |

## Core Capabilities

### 1. Data-fidelity check

Verify the rendered marks against **every row** of the source data: series count, point count
per series, min/max/range on each axis, and that categorical labels match the data's
categories. Flag any series plotted from the wrong column or a silently dropped subset.

### 2. Label floor-and-ceiling legibility

Check that tick labels, axis titles, and annotations are within legibility bounds — a **font
floor** (nothing below the journal's minimum pt at final size) and a **ceiling** (titles not
so large they crowd the panel) — and that nothing is clipped at the axis boundary.

### 3. Bounding-box collision detection

Compute the bounding boxes of text, legend, and markers and detect **overlaps/collisions**
(legend over data, colliding labels, out-of-axes text). Report each collision with its
location so it can be nudged.

### 4. Resolution and export QA

Confirm the export meets the target: **≥300 dpi** for raster, vector format where the venue
requires it, correct figure dimensions/column width, and embedded fonts. Fail the check if the
raster resolution is below the floor.

### 5. Report

Emit a pass/fail checklist per criterion with the specific offending element(s), so the fix is
actionable. See `references/figure_qa_checklist.md` for the full rubric and Matplotlib bbox
recipes.

## Resources

- `references/figure_qa_checklist.md` — the full QA rubric, Matplotlib renderer/bbox recipes
  for collision detection, dpi/vector export checks, and journal legibility floors. Loaded on
  demand.

Part of the AlterLab Academic Skills suite.
