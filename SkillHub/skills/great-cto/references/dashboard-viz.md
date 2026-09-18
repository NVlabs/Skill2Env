# Dashboard visualization contract (charts)

**Loaded by senior-dev when building a `dashboard` (or analytics-heavy) product.**
Owns the OUT half of the dashboard archetype: turning the data the
`connector-builder` ingests into polished, accessible charts. Pairs with
`skills/ui-ux-pro-max/data/charts.csv` (chart-type selection) — this file adds the
generation + shipping contract.

## The pilot decision (why this exists)

An LLM agent hand-writing ECharts/Chart.js config produces inconsistent, rarely
polished charts (the library exposes hundreds of low-level knobs). **Flint**
(`flint-chart`, MIT) is a semantic chart language: the agent emits a compact spec
(chart type + encodings + semantic field types) and Flint derives scales, axes,
spacing, labels, and layout — then **compiles to a native ECharts spec**.

**We use Flint at BUILD time only and ship the compiled native ECharts config.**
The generated product depends on **ECharts**, not on Flint. This gets Flint's
"agents reliably produce good charts" benefit while keeping a mature, stable
runtime dependency in the client's product — and makes the choice reversible
(drop Flint, keep the shipped native config).

> Flint is early (v0.1.x). It is a **dev/build tool** here, never a runtime dep of
> a shipped product. If Flint is unavailable or a spec fails to compile, fall back
> to authoring the ECharts config directly using `charts.csv` guidance.

## Build steps

1. **Pick the chart** with `skills/ui-ux-pro-max/data/charts.csv`: match the
   insight (trend → line, compare → bar, part-to-whole → donut ≤5 slices,
   correlation → scatter), respect the "avoid when" column, and honour the
   rendering thresholds (SVG < ~1k points; Canvas / downsample above; aggregate
   > 10k) and the a11y rules (differentiate series by style+pattern, not colour
   alone; always ship a data-table fallback for pie/donut).
2. **Author a Flint `ChartAssemblyInput`** per chart — `data.values`,
   `semantic_types` (field → semantic type: `Price`, `Rank`, `Country`, `Date`,
   `Category`, `Quantity`, …), and `chart_spec` (`chartType` — the same names as
   `charts.csv`, e.g. `'Bar Chart'`, `'Line Chart'` — plus `encodings`). Keep the
   inputs small and human-editable; commit them under `viz/specs/` in the product.
3. **Compile to native ECharts at build time.** `flint-chart` is a **library, not
   a CLI** (verified v0.1.3). Add it as a **devDependency** and, in a build/codegen
   step, call `assembleECharts(input)` — it returns a plain ECharts `option`
   object. Write that option out and render it with the shipped `echarts` runtime.
   Do NOT add `flint-chart` to the product's runtime `dependencies`.

   ```ts
   // build step (dev only) — flint-chart → native ECharts option
   import { assembleECharts, type ChartAssemblyInput } from 'flint-chart';
   const input: ChartAssemblyInput = {
     data: { values: rows },
     semantic_types: { month: 'Month', revenue: 'Price' },
     chart_spec: { chartType: 'Bar Chart', encodings: { x: { field: 'month' }, y: { field: 'revenue' } } },
   };
   const option = assembleECharts(input);   // ship this; echarts renders it
   ```
   (`assembleVegaLite` / `assembleChartjs` exist too if the product uses those.)
4. **Wire to live data**: charts read from the connector-builder's warehouse-lite
   schema (respect freshness SLAs); paginate/aggregate server-side before the
   chart per the thresholds above.
5. **A11y + fallback**: every chart ships keyboard focus, an accessible title/desc,
   and a togglable data table (mandatory for pie/donut). WCAG AA contrast.

## Pinned choices (per stack-baseline)

- **Runtime chart lib (shipped): ECharts** — sanctioned alt Recharts for simple
  React-native-feel dashboards. One chart lib per product.
- **Build-time generator: Flint** — optional, reversible; compiles to the above.

## Measure the pilot

Build one reference dashboard product (e.g. a profitability dashboard) with this
contract, then score its charts with the `product-quality` harness. Escalate to a
dedicated `viz-engineer` agent only if the measured chart quality is meaningfully
better than hand-authored ECharts. Until then this reference IS the contract.
