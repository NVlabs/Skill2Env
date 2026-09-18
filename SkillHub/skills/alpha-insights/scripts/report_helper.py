#!/usr/bin/env python3
"""
report_helper.py — Alpha Insights report generation helper

Two usage patterns:

1. build_report()(original API): pass all body HTML and charts at once; suitable for smaller reports.
2. ReportBuilder(recommended): incremental build mode for large reports:
   - template prefill: cover/TOC/chapter headers/footer generated automatically; model supplies only content
   - incremental generation: save_state()/load_state() support multiple calls, 2-3K tokens each

ReportBuilder Usage:
    from report_helper import ReportBuilder

    b = ReportBuilder("Report Title", "Subtitle")
    b.set_toc_conclusion("one-sentence core conclusion")

    b.add_chapter("01", "Executive Summary", "<h2>Core Conclusion</h2><p>...</p>")
    b.add_chart("chart1", {"xAxis": {"type": "category", "values": [...]}, ...}, claim_ids=["E-001"])

    b.add_chapter("02", "Market Landscape", "<h2>...</h2><p>...</p>")
    b.add_chart("chart2", {...}, claim_ids=["E-002"])

    b.build("workspace/project/report.html")

Incremental generation across multiple Bash calls:
    # Step 1
    b = ReportBuilder("Title", "Subtitle")
    b.save_state("/tmp/rpt.json")

    # Step 2
    b = ReportBuilder.load_state("/tmp/rpt.json")
    b.add_chapter(...)
    b.save_state("/tmp/rpt.json")

    # Step N(Final step)
    b = ReportBuilder.load_state("/tmp/rpt.json")
    b.build("workspace/project/report.html")

Core mechanism: the model writes the safe "values" key in Python dicts,
and this script maps "values" to "data" when serializing ECharts JS.
"""

import json
import html
import os
import re
import sys
from datetime import datetime
from pathlib import Path


# -- Core: safe values-to-data serialization ---------------------------------

def _escape_html(value):
    return html.escape(str(value or ""), quote=True)


def _to_js(obj, indent=0):
    """Serialize a Python object recursively as a JS object literal.

    Key rule: output "data" when a "values" key is encountered; ECharts requires that key.
    This avoids asking the model to write the fragile "data" + array pattern directly.
    """
    pad = "  " * indent
    pad_inner = "  " * (indent + 1)

    if obj is None:
        return "null"
    elif isinstance(obj, bool):
        return "true" if obj else "false"
    elif isinstance(obj, (int, float)):
        return str(obj)
    elif isinstance(obj, str):
        # Escape special string characters
        escaped = obj.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
        return f"'{escaped}'"
    elif isinstance(obj, list):
        if not obj:
            return "[]"
        # Short primitive arrays are emitted on one line
        if len(obj) <= 8 and all(isinstance(x, (int, float, str, bool, type(None))) for x in obj):
            items = ", ".join(_to_js(x) for x in obj)
            return f"[{items}]"
        # Long or nested arrays are emitted across multiple lines
        items = []
        for x in obj:
            items.append(f"{pad_inner}{_to_js(x, indent + 1)}")
        return "[\n" + ",\n".join(items) + f"\n{pad}]"
    elif isinstance(obj, dict):
        if not obj:
            return "{}"
        items = []
        for k, v in obj.items():
            # Core mapping: values -> data
            js_key = "data" if k == "values" else k
            # JS object keys: simple identifiers stay unquoted; others are quoted
            if re.match(r'^[a-zA-Z_$][a-zA-Z0-9_$]*$', js_key):
                key_str = js_key
            else:
                key_str = f"'{js_key}'"
            items.append(f"{pad_inner}{key_str}: {_to_js(v, indent + 1)}")
        return "{\n" + ",\n".join(items) + f"\n{pad}}}"
    else:
        return str(obj)


# ── Chart JS generation ──────────────────────────────────────────────

def _make_chart_js(charts):
    """Generate all ECharts initialization JS.

    Wrap every chart in its own try/catch so one failure does not break the rest.
    charts: list of dict, each dict contains "id" and "option" keys.
    """
    if not charts:
        return ""

    js_parts = []
    var_names = []
    for i, chart in enumerate(charts):
        chart_id = chart.get("id", f"chart{i+1}")
        option = chart.get("option", {})
        var_name = f"c{i+1}"
        chart_id_js = _to_js(str(chart_id))
        error_label_js = _to_js(f"ECharts init error [{chart_id}]:")
        evidence_meta = {
            k: v for k, v in {
                "claimIds": chart.get("claim_ids"),
                "sourceIds": chart.get("source_ids"),
            }.items() if v
        }
        evidence_js = (
            f"  {var_name}.__alphaEvidence = {_to_js(evidence_meta, 1)};\n"
            if evidence_meta else ""
        )
        var_names.append(var_name)

        # Each chart has an independent try/catch.
        js_parts.append(
            f"var {var_name};\n"
            f"try {{\n"
            f"  {var_name} = echarts.init(document.getElementById({chart_id_js}));\n"
            f"  {var_name}.setOption({_to_js(option, 1)});\n"
            f"{evidence_js}"
            f"}} catch(e) {{\n"
            f"  console.error({error_label_js}, e);\n"
            f"}}"
        )

    # Responsive resize, also guarded
    resize_lines = "".join(
        f"    if ({v}) {v}.resize();\n" for v in var_names
    )
    js_parts.append(
        f"window.addEventListener('resize', function() {{\n{resize_lines}}});"
    )

    return "\n\n".join(js_parts)


# ── Template loading ─────────────────────────────────────────────────

def _read_template(template_path=None):
    """Read report_template.html and extract <style> plus ECharts CDN."""
    if template_path is None:
        # Default path: relative to this script
        template_path = Path(__file__).parent.parent / "references" / "report_template.html"

    template_path = Path(template_path)
    if not template_path.exists():
        print(f"⚠️ template file missing: {template_path}, using minimal built-in style")
        return _minimal_style(), _ECHARTS_CDN, _FALLBACK_JS

    html = template_path.read_text(encoding="utf-8")

    # Extract <style>...</style>
    style_match = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
    style = style_match.group(0) if style_match else "<style></style>"

    # Extract ECharts CDN script tag and force crossorigin
    cdn_match = re.search(r'<script src="([^"]*echarts[^"]*)"[^>]*></script>', html)
    if cdn_match:
        cdn_url = cdn_match.group(1)
        cdn = f'<script src="{cdn_url}" crossorigin="anonymous"></script>'
    else:
        cdn = _ECHARTS_CDN

    # Extract fallback JS
    fallback_match = re.search(
        r'<!-- Chart render fallback.*?</script>', html, re.DOTALL
    )
    fallback_js = fallback_match.group(0) if fallback_match else _FALLBACK_JS

    return style, cdn, fallback_js


_ECHARTS_CDN = '<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js" crossorigin="anonymous"></script>'

_FALLBACK_JS = '''<!-- Chart render fallback -->
<script>
  window.addEventListener('load', function() {
    if (typeof echarts === 'undefined') return;
    document.querySelectorAll('.chart-container > div[style*="height"]').forEach(function(el) {
      var instance = echarts.getInstanceByDom(el);
      if (!instance) {
        el.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100%;min-height:200px;color:#94a3b8;font-size:14px;border:2px dashed #e2e8f0;border-radius:8px;padding:20px;text-align:center;">'
          + '<div>\\u26a0\\ufe0f Chart did not render<br><span style="font-size:12px;color:#cbd5e1;">Possible cause: data loading failed. Check the browser console.</span></div>'
          + '</div>';
      }
    });
  });
</script>'''


def _minimal_style():
    """Minimal style used when the template is unavailable."""
    return """<style>
  body { font-family: -apple-system, sans-serif; line-height: 1.6; color: #2D3748; background: #C9CED1; }
  .page { max-width: 900px; margin: 0 auto 20px; background: #fff; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
  .chart-container { margin: 20px 0; padding: 20px; background: #F1F5F9; border-radius: 8px; }
</style>"""


# ── Validation ─────────────────────────────────────────────────────

def _validate(html, expected_charts):
    """Validate ECharts data integrity in generated HTML."""
    init_count = len(re.findall(r'echarts\.init', html))
    data_count = len(re.findall(r'\bdata\s*:', html))
    empty_data = len(re.findall(r'\bdata\s*:\s*\[\s*\]', html))

    print(f"[chart self-check] ECharts instances: {init_count}, data keys: {data_count}, empty arrays: {empty_data}")

    ok = True
    if init_count != expected_charts:
        print(f"⚠️ expected {expected_charts} chart(s), actual {init_count} echarts.init call(s)")
        ok = False
    if data_count < init_count:
        print(f"⚠️ data key count ({data_count}) < ECharts instance count ({init_count}); chart data may be missing")
        ok = False
    if empty_data > 0:
        print(f"⚠️ found {empty_data} empty arrays; charts will render without data")
        ok = False
    if ok:
        print("✅ chart data integrity check passed")
    return ok


# ── Main entry point ────────────────────────────────────────────────────

def build_report(
    body=None,
    body_file=None,
    charts=None,
    title="Research Report",
    output="report.html",
    template=None,
    confidential="Internal",
    date=None,
):
    """
    Assemble the complete report HTML and write it to disk.

    Arguments:
        body:         HTML body string(all <div class="page"> blocks)
        body_file:    or read body HTML from file(mutually exclusive with body)
        charts:       ECharts chart configuration list, each item {"id": "chart1", "option": {...}}
                      option use "values" instead of "data"
        title:        Report Title
        output:       output file path
        template:     report_template.html path (None uses default)
        confidential: confidentiality level
        date:         date string(None uses today)
    """
    # Body
    if body is None and body_file is not None:
        body = Path(body_file).read_text(encoding="utf-8")
    if body is None:
        body = ""

    # Date
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    # Template assets
    style, cdn, fallback_js = _read_template(template)

    # Chart JS
    chart_js = _make_chart_js(charts or [])
    chart_script = f"\n<script>\n{chart_js}\n</script>" if chart_js else ""

    # Assemble
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{_escape_html(title)}</title>
  {style}
</head>
<body>

{body}

  <!-- Print button -->
  <div class="no-print">
    <button class="print-btn" onclick="window.print()">Print / Export PDF</button>
  </div>

  {cdn}
  {chart_script}

  {fallback_js}

</body>
</html>"""

    # Write output
    out_path = Path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")

    file_size = out_path.stat().st_size
    print(f"📄 report generated: {out_path} ({file_size:,} bytes)")

    # Validation
    if charts:
        _validate(html, len(charts))

    return str(out_path)


# ── ReportBuilder: incremental build + template prefill ────────────────────────

class ReportBuilder:
    """Build reports incrementally to avoid large one-shot generation bottlenecks.

    Core value:
    1. Template prefill — cover/TOC/chapter headers/footer generated automatically, reducing model output by 60-70%
    2. Incremental generation — save_state()/load_state() supports multiple Bash calls
    3. Automatic chart management — add_chart() automatically handles values->data mapping
    """

    def __init__(self, title="Research Report", subtitle="", date=None,
                 confidential="Internal", version="V1.0",
                 author="Alpha Insights Research"):
        self.title = title
        self.subtitle = subtitle
        self.date = date or datetime.now().strftime("%Y-%m-%d")
        self.confidential = confidential
        self.version = version
        self.author = author
        self.toc_conclusion = ""
        self.chapters = []   # list of [num_str, name, body_html]
        self.charts = []     # list of {"id": ..., "option": ...}

    # ── Content adding ──

    def set_toc_conclusion(self, text):
        """Set the TOC-page core conclusion (1-2 sentences)."""
        self.toc_conclusion = text
        return self

    def add_chapter(self, num, name, body_html):
        """Add one chapter.

        Args:
            num: chapter number, for example "01", 1, or 3.5
            name: chapter name, for example "Executive Summary"
            body_html: chapter body HTML inside <div class="chapter-body">
                       may include h2/h3/p/table/highlight-box/stat-card/chart-container, etc.
        """
        if isinstance(num, float) and not num.is_integer():
            num_str = str(num)          # 3.5 → "3.5"
        elif isinstance(num, (int, float)):
            num_str = f"{int(num):02d}"  # 1 → "01", 3.0 → "03"
        else:
            num_str = str(num)           # "01" → "01"
        self.chapters.append([num_str, name, body_html])
        return self

    def add_chart(self, chart_id, option, claim_ids=None, source_ids=None):
        """Register one ECharts chart.

        Args:
            chart_id: id of the corresponding HTML <div id="chart_id">
            option: ECharts option dict, use "values" instead of "data"
            claim_ids: Evidence Claim Ledger claim_id list for chart data
            source_ids: Evidence Claim Ledger source_id list for chart data
        """
        chart = {"id": chart_id, "option": option}
        if claim_ids:
            chart["claim_ids"] = list(claim_ids)
        if source_ids:
            chart["source_ids"] = list(source_ids)
        self.charts.append(chart)
        return self

    # -- State persistence for incremental generation across shell calls -------

    def save_state(self, path):
        """Save current state to JSON so the next Bash call can resume with load_state()."""
        state = {
            "title": self.title,
            "subtitle": self.subtitle,
            "author": self.author,
            "date": self.date,
            "confidential": self.confidential,
            "version": self.version,
            "toc_conclusion": self.toc_conclusion,
            "chapters": self.chapters,
            "charts": self.charts,
        }
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        print(f"💾 state saved: {path} ({len(self.chapters)} chapters, {len(self.charts)} charts)")
        return self

    @classmethod
    def load_state(cls, path):
        """Restore builder state from JSON."""
        with open(path, 'r', encoding='utf-8') as f:
            state = json.load(f)
        builder = cls(
            title=state["title"],
            subtitle=state.get("subtitle", ""),
            author=state.get("author", "Alpha Insights Research"),
            date=state.get("date"),
            confidential=state.get("confidential", "Internal"),
            version=state.get("version", "V1.0"),
        )
        builder.toc_conclusion = state.get("toc_conclusion", "")
        builder.chapters = state.get("chapters", [])
        builder.charts = state.get("charts", [])
        print(f"📂 state restored: {len(builder.chapters)} chapters, {len(builder.charts)} charts")
        return builder

    # -- Template generation; users should not hand-write these HTML blocks ----

    def _make_cover(self):
        return f'''<div class="page cover-page">
    <div class="cover-left">
      <div class="cover-number">AI</div>
    </div>
    <div class="cover-right">
      <div class="cover-badge">Alpha Insights - BizAdvisor</div>
      <h1 class="cover-title">{_escape_html(self.title)}</h1>
      <p class="cover-subtitle">{_escape_html(self.subtitle)}</p>
      <div class="cover-divider"></div>
      <p class="cover-meta">{_escape_html(self.author)}</p>
      <p class="cover-date">{_escape_html(self.date)}</p>
    </div>
    <div class="cover-footer">
      <span>{_escape_html(self.confidential)}</span>
      <span>{_escape_html(self.version)}</span>
    </div>
  </div>'''

    def _make_toc(self):
        items = "\n    ".join(
            f'<div class="toc-item">'
            f'<div class="toc-number">{_escape_html(ch[0])}</div>'
            f'<span class="toc-text">{_escape_html(ch[1])}</span>'
            f'</div>'
            for ch in self.chapters
        )
        conclusion = ""
        if self.toc_conclusion:
            conclusion = (
                f'<div class="toc-conclusion">'
                f'<div class="toc-conclusion-title">Core Conclusion</div>'
                f'<div class="toc-conclusion-text">{_escape_html(self.toc_conclusion)}</div>'
                f'</div>'
            )
        return f'''<div class="page toc-page">
    <div class="toc-header">
      <div class="toc-title">Contents</div>
    </div>
    {items}
    {conclusion}
  </div>'''

    def _make_chapter(self, num_str, name, body):
        return f'''<div class="page chapter-section">
    <div class="chapter-header">
      <div class="chapter-num">{_escape_html(num_str)}</div>
      <div class="chapter-name">{_escape_html(name)}</div>
    </div>
    <div class="chapter-body">
{body}
    </div>
  </div>'''

    def _make_footer(self):
        return f'''<div class="page footer-page">
    <div class="footer-content">
      <div class="footer-icon">📋</div>
      <div class="footer-title">{_escape_html(self.title)}</div>
      <div class="footer-divider"></div>
      <div class="footer-text">Generated by Alpha Insights-BizAdvisor</div>
      <div class="footer-text">{_escape_html(self.confidential)} · Do not distribute</div>
      <div class="footer-date">{_escape_html(self.date)}</div>
      <div class="footer-cta">
        <a href="https://github.com/Ericyoung-183/alpha-insights" target="_blank">Star Alpha Insights on GitHub</a>
      </div>
    </div>
  </div>'''

    # -- Build --

    def build(self, output, template=None):
        """Assemble all chapters and generate the final report HTML.

        Returns:
            output file path string
        """
        # Assemble body
        parts = [self._make_cover(), self._make_toc()]
        for ch in self.chapters:
            parts.append(self._make_chapter(ch[0], ch[1], ch[2]))
        parts.append(self._make_footer())
        body = "\n\n".join(parts)

        # Use build_report to assemble HTML, inject chart JS, and validate.
        return build_report(
            body=body,
            charts=self.charts,
            title=self.title,
            output=output,
            template=template,
            confidential=self.confidential,
            date=self.date,
        )


# -- CLI entry point -------------------------------------------------

if __name__ == "__main__":
    # Simple CLI: python3 report_helper.py --body-file body.html --output report.html
    import argparse

    parser = argparse.ArgumentParser(description="Alpha Insights report generator")
    parser.add_argument("--body-file", help="HTML body file path")
    parser.add_argument("--title", default="Research Report", help="Report Title")
    parser.add_argument("--output", default="report.html", help="output path")
    parser.add_argument("--template", help="template path")
    parser.add_argument("--confidential", default="Internal", help="confidentiality level")
    args = parser.parse_args()

    build_report(
        body_file=args.body_file,
        title=args.title,
        output=args.output,
        template=args.template,
        confidential=args.confidential,
    )
