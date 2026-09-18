# Figure QA — Checklist & Recipes

Full rubric and recipes for `alterlab-figure-qa`. The Matplotlib APIs below are stable, but
confirm details against your installed version.

## The checklist

| # | Criterion | Pass condition |
|---|-----------|----------------|
| 1 | Data fidelity | series/point counts, axis ranges, and category labels match the source data exactly |
| 2 | Label floor | no text below the venue's minimum font size at final render size |
| 3 | Label ceiling | titles/annotations do not crowd or overflow the panel |
| 4 | Clipping | no tick label / annotation clipped at the axes boundary |
| 5 | Collisions | no overlapping text/legend/marker bounding boxes |
| 6 | Legend placement | legend does not cover data points |
| 7 | Resolution | raster ≥ 300 dpi; vector (PDF/SVG/EPS) where the venue requires |
| 8 | Dimensions | figure width matches the column/page spec; fonts embedded |
| 9 | Color/accessibility | colorblind-safe palette; sufficient contrast (report, don't hard-fail) |

## Bounding-box / collision recipe (Matplotlib)

Render once, then measure text/legend extents in display coordinates and test for overlap:

```python
fig.canvas.draw()  # required before extents are available
renderer = fig.canvas.get_renderer()
boxes = [t.get_window_extent(renderer) for t in fig.findobj(match=Text) if t.get_text()]
# pairwise overlap test on Bbox objects → report colliding pairs
```

Compare each label's `get_window_extent` to the axes' `get_window_extent` to detect clipping
(label extends beyond the axes box).

## Resolution / export check

```python
fig.savefig("out.png", dpi=300)          # raster: assert dpi >= 300
fig.savefig("out.pdf")                     # vector where required
# For an existing raster, read its DPI/size with Pillow and assert the floor.
```

## Data-fidelity check

Recompute, from the source dataframe, the number of series, points per series, and per-axis
min/max, and assert they equal what the artists actually drew (`ax.get_lines()`,
`collection.get_offsets()`, etc.). This catches a series plotted from the wrong column or a
filtered subset.

## Journal legibility floors

Many venues set a minimum font size (commonly ~5–7 pt at final size) and a preferred column
width. Encode the target venue's numbers and assert against them; treat unknown venues with a
conservative floor and report.

## Relationship to the plotting skills

`alterlab-figure-qa` **verifies**; it does not create. Build the figure with
`alterlab-matplotlib` / `alterlab-seaborn` / `alterlab-plotly`, lay out multi-panel figures
with `alterlab-scientific-viz`, then run this QA pass before submission.
