import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

from report_helper import ReportBuilder  # noqa: E402


class ReportHelperEscapingTests(unittest.TestCase):
    def test_builder_escapes_metadata_and_chart_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "report.html"
            builder = ReportBuilder(
                title="<script>alert(1)</script>",
                subtitle="<b>subtitle</b>",
                author="A & B",
                date="2026-06-01",
                confidential='internal "draft"',
                version="V1",
            )
            builder.set_toc_conclusion('<img src=x onerror="alert(1)">')
            builder.add_chapter("01", "<b>Chapter</b>", '<div id="chart1"></div>')
            builder.add_chart("chart1');alert(1);//", {"series": [{"values": [1, 2, 3]}]}, claim_ids=["E-001"])
            builder.build(str(output))

            html = output.read_text(encoding="utf-8")

            self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html)
            self.assertIn("A &amp; B", html)
            self.assertIn("&lt;img src=x onerror=&quot;alert(1)&quot;&gt;", html)
            self.assertNotIn("<b>Chapter</b>", html)
            self.assertNotIn("document.getElementById('chart1');alert", html)
            self.assertIn("document.getElementById('chart1\\');alert(1);//')", html)
            self.assertIn("claimIds: ['E-001']", html)


if __name__ == "__main__":
    unittest.main()
