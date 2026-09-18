#!/usr/bin/env python3
"""
SEO/GEO Comprehensive Audit Report Generator

Orchestrates all analysis scripts and generates comprehensive multi-format reports:
- JSON (raw data)
- Markdown (readable text)
- HTML (visual dashboard)

Usage:
    python audit_report.py <file_path> [options]
    python audit_report.py <file_path> --format html
    python audit_report.py <file_path> --format all --open
    python audit_report.py --help

Options:
    --format <format>     Output format: json, md, html, all (default: all)
    --open                Auto-open HTML report in browser
    --output-dir <dir>    Custom output directory (default: ~/Documents/SEO_Audit_YYYY-MM-DD_HH-MM-SS/)

Requirements:
    Python 3.7+ (stdlib only)

Output:
    Comprehensive audit report with:
    - Overall SEO/GEO score (0-100)
    - Metadata validation results
    - Keyword analysis
    - Entity extraction
    - Content structure analysis
    - Prioritized recommendations
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import webbrowser
import os

# Import other scripts
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from analyze_content import analyze_file
from metadata_validator import validate_metadata
from keyword_analyzer import analyze_keywords
from entity_extractor import extract_entities


def run_full_audit(file_path: str) -> Dict:
    """Run all analysis scripts and aggregate results"""

    print(f"🔍 Running comprehensive SEO/GEO audit on: {file_path}")
    print("-" * 60)

    results = {
        'file': file_path,
        'timestamp': datetime.now().isoformat(),
        'audit_type': 'comprehensive'
    }

    # 1. Basic content analysis
    print("📄 Analyzing content structure...")
    try:
        results['content_analysis'] = analyze_file(file_path)
    except Exception as e:
        results['content_analysis'] = {'error': str(e)}
        print(f"   ⚠️  Error: {e}")

    # 2. Metadata validation
    print("✅ Validating metadata...")
    try:
        results['metadata_validation'] = validate_metadata(file_path)
    except Exception as e:
        results['metadata_validation'] = {'error': str(e)}
        print(f"   ⚠️  Error: {e}")

    # 3. Keyword analysis
    print("🔑 Analyzing keywords...")
    try:
        results['keyword_analysis'] = analyze_keywords(file_path)
    except Exception as e:
        results['keyword_analysis'] = {'error': str(e)}
        print(f"   ⚠️  Error: {e}")

    # 4. Entity extraction
    print("👤 Extracting entities...")
    try:
        results['entity_analysis'] = extract_entities(file_path)
    except Exception as e:
        results['entity_analysis'] = {'error': str(e)}
        print(f"   ⚠️  Error: {e}")

    print("-" * 60)
    print("✅ Audit complete!")

    return results


def calculate_overall_score(audit_results: Dict) -> int:
    """Calculate weighted overall SEO/GEO score"""

    weights = {
        'metadata': 0.30,      # 30% - Most critical
        'content': 0.25,       # 25% - Structure and quality
        'keywords': 0.20,      # 20% - Keyword optimization
        'entities': 0.15,      # 15% - E-E-A-T signals
        'schema': 0.10         # 10% - Technical implementation
    }

    scores = {}

    # Metadata score
    if 'metadata_validation' in audit_results:
        meta = audit_results['metadata_validation']
        if 'summary' in meta:
            scores['metadata'] = meta['summary'].get('overall_score', 0)

    # Content score
    if 'content_analysis' in audit_results:
        content = audit_results['content_analysis']
        if 'score' in content:
            scores['content'] = content['score']

    # Keywords score (based on presence and quality)
    if 'keyword_analysis' in audit_results:
        kw = audit_results['keyword_analysis']
        if 'summary' in kw:
            summary = kw['summary']
            kw_score = 0
            # Check for good keyword coverage
            if summary.get('primary_keywords', 0) >= 5:
                kw_score += 30
            if summary.get('longtail_keywords', 0) >= 3:
                kw_score += 25
            if summary.get('question_keywords', 0) >= 3:
                kw_score += 25
            if summary.get('semantic_keywords', 0) >= 10:
                kw_score += 20
            scores['keywords'] = kw_score

    # Entity score (based on presence and quality)
    if 'entity_analysis' in audit_results:
        ent = audit_results['entity_analysis']
        if 'summary' in ent:
            summary = ent['summary']
            ent_score = 0
            # Check for entity coverage
            if summary.get('total_persons', 0) > 0:
                ent_score += 30
            if summary.get('persons_with_credentials', 0) > 0:
                ent_score += 30  # Major boost for credentials
            if summary.get('total_organizations', 0) > 0:
                ent_score += 20
            if summary.get('total_places', 0) > 0:
                ent_score += 10
            if summary.get('knowledge_graph_ready', False):
                ent_score += 10
            scores['entities'] = min(100, ent_score)

    # Schema score
    if 'content_analysis' in audit_results:
        content = audit_results['content_analysis']
        if 'schema' in content and content['schema']:
            scores['schema'] = 80  # Has schema
        else:
            scores['schema'] = 20  # No schema

    # Calculate weighted average
    weighted_score = 0
    total_weight = 0

    for key, weight in weights.items():
        if key in scores:
            weighted_score += scores[key] * weight
            total_weight += weight

    if total_weight > 0:
        overall = int(weighted_score / total_weight)
    else:
        overall = 0

    return overall


def get_score_grade(score: int) -> tuple:
    """Convert score to letter grade and color"""
    if score >= 90:
        return ("A+", "Excellent", "#10b981")
    elif score >= 80:
        return ("A", "Good", "#22c55e")
    elif score >= 70:
        return ("B", "Fair", "#eab308")
    elif score >= 60:
        return ("C", "Poor", "#f97316")
    else:
        return ("F", "Critical", "#ef4444")


def aggregate_recommendations(audit_results: Dict) -> Dict:
    """Aggregate and prioritize recommendations from all analyses"""

    critical = []
    high_priority = []
    medium_priority = []
    low_priority = []
    successes = []

    # From metadata validation
    if 'metadata_validation' in audit_results:
        meta = audit_results['metadata_validation']
        if 'issues' in meta:
            critical.extend(meta['issues'].get('critical', []))
            high_priority.extend(meta['issues'].get('regular', []))
        if 'recommendations' in meta:
            for rec in meta['recommendations']:
                if rec.startswith('✅'):
                    successes.append(rec)
                elif 'CRITICAL' in rec or 'Missing' in rec:
                    high_priority.append(rec)
                else:
                    medium_priority.append(rec)

    # From keyword analysis
    if 'keyword_analysis' in audit_results:
        kw = audit_results['keyword_analysis']
        if 'recommendations' in kw:
            for rec in kw['recommendations']:
                if rec.startswith('✅'):
                    successes.append(rec)
                elif 'Add' in rec:
                    medium_priority.append(rec)
                else:
                    low_priority.append(rec)

    # From entity analysis
    if 'entity_analysis' in audit_results:
        ent = audit_results['entity_analysis']
        if 'recommendations' in ent:
            for rec in ent['recommendations']:
                if rec.startswith('✅'):
                    successes.append(rec)
                elif 'credentials' in rec.lower():
                    critical.append(rec)
                else:
                    high_priority.append(rec)

    return {
        'critical': list(set(critical)),
        'high_priority': list(set(high_priority)),
        'medium_priority': list(set(medium_priority)),
        'low_priority': list(set(low_priority)),
        'successes': list(set(successes))
    }


def generate_json_report(audit_results: Dict, output_dir: Path) -> Path:
    """Generate JSON report"""

    output_file = output_dir / 'audit_report.json'

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(audit_results, f, indent=2, ensure_ascii=False)

    return output_file


def generate_markdown_report(audit_results: Dict, output_dir: Path) -> Path:
    """Generate Markdown report"""

    output_file = output_dir / 'audit_report.md'

    # Calculate overall score
    overall_score = calculate_overall_score(audit_results)
    grade, grade_text, _ = get_score_grade(overall_score)

    # Aggregate recommendations
    recommendations = aggregate_recommendations(audit_results)

    # Generate markdown
    md = f"""# SEO/GEO Audit Report

**File**: `{audit_results['file']}`
**Date**: {audit_results['timestamp']}
**Overall Score**: {overall_score}/100 ({grade} - {grade_text})

---

## Executive Summary

"""

    # Add success highlights
    if recommendations['successes']:
        md += "### ✅ What's Working Well\n\n"
        for success in recommendations['successes'][:5]:
            md += f"- {success}\n"
        md += "\n"

    # Add critical issues
    if recommendations['critical']:
        md += "### 🚨 Critical Issues (Fix Immediately)\n\n"
        for issue in recommendations['critical']:
            md += f"- {issue}\n"
        md += "\n"

    # Add high priority
    if recommendations['high_priority']:
        md += "### ⚠️ High Priority Issues\n\n"
        for issue in recommendations['high_priority'][:10]:
            md += f"- {issue}\n"
        md += "\n"

    # Metadata Section
    md += "---\n\n## Metadata Validation\n\n"
    if 'metadata_validation' in audit_results:
        meta = audit_results['metadata_validation']
        if 'summary' in meta:
            summary = meta['summary']
            md += f"**Score**: {summary.get('overall_score', 0)}/100 ({summary.get('grade', 'Unknown')})\n\n"
            md += f"- Critical Issues: {summary.get('critical_issues', 0)}\n"
            md += f"- Total Issues: {summary.get('total_issues', 0)}\n"
            md += f"- Recommendations: {summary.get('recommendations', 0)}\n\n"

        # Meta title
        if 'meta_title' in meta:
            title = meta['meta_title']
            md += f"### Meta Title\n"
            md += f"- **Title**: {title.get('title', 'Missing')}\n"
            md += f"- **Length**: {title.get('length', 0)} characters\n"
            md += f"- **Score**: {title.get('score', 0)}/100\n\n"

        # Meta description
        if 'meta_description' in meta:
            desc = meta['meta_description']
            md += f"### Meta Description\n"
            md += f"- **Length**: {desc.get('length', 0)} characters\n"
            md += f"- **Score**: {desc.get('score', 0)}/100\n\n"

    # Keywords Section
    md += "---\n\n## Keyword Analysis\n\n"
    if 'keyword_analysis' in audit_results:
        kw = audit_results['keyword_analysis']
        if 'summary' in kw:
            summary = kw['summary']
            md += f"- Total Words: {summary.get('total_words', 0)}\n"
            md += f"- Primary Keywords: {summary.get('primary_keywords', 0)}\n"
            md += f"- Semantic Keywords: {summary.get('semantic_keywords', 0)}\n"
            md += f"- Long-tail Keywords: {summary.get('longtail_keywords', 0)}\n"
            md += f"- Question Keywords: {summary.get('question_keywords', 0)}\n"
            md += f"- Voice Search Ready: {summary.get('voice_search_questions', 0)} questions\n\n"

        # Top primary keywords
        if 'primary_keywords' in kw and kw['primary_keywords']:
            md += "### Top Primary Keywords\n\n"
            md += "| Keyword | Type | Frequency | Density |\n"
            md += "|---------|------|-----------|----------|\n"
            for keyword in kw['primary_keywords'][:10]:
                md += f"| {keyword['keyword']} | {keyword['type']} | {keyword['frequency']} | {keyword.get('density', 0)}% |\n"
            md += "\n"

    # Entity Section
    md += "---\n\n## Entity Analysis\n\n"
    if 'entity_analysis' in audit_results:
        ent = audit_results['entity_analysis']
        if 'summary' in ent:
            summary = ent['summary']
            md += f"- Total Persons: {summary.get('total_persons', 0)}\n"
            md += f"- Persons with Credentials: {summary.get('persons_with_credentials', 0)}\n"
            md += f"- Total Organizations: {summary.get('total_organizations', 0)}\n"
            md += f"- Total Places: {summary.get('total_places', 0)}\n"
            md += f"- Knowledge Graph Ready: {'✅ Yes' if summary.get('knowledge_graph_ready') else '❌ No'}\n\n"

        # Persons
        if 'persons' in ent and ent['persons']:
            md += "### Persons Identified\n\n"
            for person in ent['persons'][:5]:
                md += f"- **{person.get('full_name', person.get('name'))}**"
                if person.get('credentials'):
                    md += f" ({', '.join(person['credentials'])})"
                md += f" - {person.get('context', 'unknown')}\n"
            md += "\n"

        # Organizations
        if 'organizations' in ent and ent['organizations']:
            md += "### Organizations Identified\n\n"
            for org in ent['organizations'][:5]:
                md += f"- **{org['name']}** - {org.get('context', 'unknown')}\n"
            md += "\n"

    # Schema Section
    md += "---\n\n## Schema Markup\n\n"
    if 'content_analysis' in audit_results:
        content = audit_results['content_analysis']
        if 'schema' in content and content['schema']:
            md += f"**Found**: {len(content['schema'])} schema(s)\n\n"
            for i, schema in enumerate(content['schema'], 1):
                schema_type = schema.get('@type', 'Unknown') if isinstance(schema, dict) else 'Unknown'
                md += f"{i}. {schema_type}\n"
        else:
            md += "**Status**: ❌ No JSON-LD schema found\n\n"
            md += "**Recommendation**: Add FAQ schema (highest AI citation probability)\n\n"

    # Action Items
    md += "---\n\n## Priority Action Items\n\n"

    if recommendations['critical']:
        md += "### 🚨 Critical (Do Now)\n\n"
        for i, issue in enumerate(recommendations['critical'], 1):
            md += f"{i}. {issue}\n"
        md += "\n"

    if recommendations['high_priority']:
        md += "### ⚠️ High Priority (This Week)\n\n"
        for i, issue in enumerate(recommendations['high_priority'][:5], 1):
            md += f"{i}. {issue}\n"
        md += "\n"

    if recommendations['medium_priority']:
        md += "### 📋 Medium Priority (This Month)\n\n"
        for i, issue in enumerate(recommendations['medium_priority'][:5], 1):
            md += f"{i}. {issue}\n"
        md += "\n"

    md += "---\n\n"
    md += "*Report generated by SEO/GEO Optimizer*\n"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md)

    return output_file


def generate_html_report(audit_results: Dict, output_dir: Path) -> Path:
    """Generate HTML visual dashboard"""

    output_file = output_dir / 'audit_report.html'

    # Calculate overall score
    overall_score = calculate_overall_score(audit_results)
    grade, grade_text, color = get_score_grade(overall_score)

    # Aggregate recommendations
    recommendations = aggregate_recommendations(audit_results)

    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO/GEO Audit Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #1f2937;
            background: #f9fafb;
            padding: 24px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            padding: 40px;
        }}

        header {{
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 24px;
            margin-bottom: 32px;
        }}

        h1 {{
            font-size: 32px;
            font-weight: 700;
            color: #111827;
            margin-bottom: 8px;
        }}

        .meta {{
            color: #6b7280;
            font-size: 14px;
        }}

        .score-card {{
            display: grid;
            grid-template-columns: 200px 1fr;
            gap: 32px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 32px;
            border-radius: 12px;
            margin-bottom: 32px;
        }}

        .score-circle {{
            width: 160px;
            height: 160px;
            border-radius: 50%;
            background: white;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .score-number {{
            font-size: 48px;
            font-weight: 700;
            color: {color};
        }}

        .score-grade {{
            font-size: 18px;
            color: #6b7280;
            margin-top: 4px;
        }}

        .score-details {{
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}

        .score-details h2 {{
            font-size: 24px;
            margin-bottom: 8px;
        }}

        .score-details p {{
            font-size: 16px;
            opacity: 0.9;
        }}

        .section {{
            margin-bottom: 32px;
        }}

        h2 {{
            font-size: 24px;
            font-weight: 600;
            color: #111827;
            margin-bottom: 16px;
            padding-bottom: 8px;
            border-bottom: 2px solid #e5e7eb;
        }}

        h3 {{
            font-size: 18px;
            font-weight: 600;
            color: #374151;
            margin-top: 24px;
            margin-bottom: 12px;
        }}

        .card {{
            background: #f9fafb;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 16px;
        }}

        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }}

        .card-title {{
            font-size: 16px;
            font-weight: 600;
            color: #111827;
        }}

        .card-score {{
            font-size: 18px;
            font-weight: 700;
            padding: 4px 12px;
            border-radius: 6px;
            background: white;
        }}

        .score-excellent {{ color: #10b981; }}
        .score-good {{ color: #22c55e; }}
        .score-fair {{ color: #eab308; }}
        .score-poor {{ color: #f97316; }}
        .score-critical {{ color: #ef4444; }}

        ul {{
            list-style: none;
            padding-left: 0;
        }}

        li {{
            padding: 8px 0;
            padding-left: 24px;
            position: relative;
        }}

        li:before {{
            content: "•";
            position: absolute;
            left: 8px;
            color: #6b7280;
        }}

        .success-item:before {{ content: "✅"; }}
        .critical-item:before {{ content: "🚨"; color: #ef4444; }}
        .high-item:before {{ content: "⚠️"; color: #f97316; }}
        .medium-item:before {{ content: "📋"; color: #eab308; }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
        }}

        th, td {{
            text-align: left;
            padding: 12px;
            border-bottom: 1px solid #e5e7eb;
        }}

        th {{
            background: #f9fafb;
            font-weight: 600;
            color: #374151;
        }}

        .badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
        }}

        .badge-success {{ background: #d1fae5; color: #065f46; }}
        .badge-warning {{ background: #fef3c7; color: #92400e; }}
        .badge-danger {{ background: #fee2e2; color: #991b1b; }}

        footer {{
            margin-top: 48px;
            padding-top: 24px;
            border-top: 2px solid #e5e7eb;
            text-align: center;
            color: #6b7280;
            font-size: 14px;
        }}

        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>SEO/GEO Audit Report</h1>
            <div class="meta">
                <strong>File:</strong> {audit_results['file']}<br>
                <strong>Generated:</strong> {audit_results['timestamp']}
            </div>
        </header>

        <div class="score-card">
            <div class="score-circle">
                <div class="score-number">{overall_score}</div>
                <div class="score-grade">{grade}</div>
            </div>
            <div class="score-details">
                <h2>{grade_text} SEO/GEO Performance</h2>
                <p>Your content has been analyzed across metadata, keywords, entities, and schema markup. Review the recommendations below to improve visibility in traditional search engines and AI platforms.</p>
            </div>
        </div>
"""

    # Success highlights
    if recommendations['successes']:
        html += """
        <div class="section">
            <h2>✅ What's Working Well</h2>
            <ul>
"""
        for success in recommendations['successes'][:8]:
            html += f"                <li class='success-item'>{success}</li>\n"
        html += """            </ul>
        </div>
"""

    # Critical issues
    if recommendations['critical']:
        html += """
        <div class="section">
            <h2>🚨 Critical Issues (Fix Immediately)</h2>
            <ul>
"""
        for issue in recommendations['critical']:
            html += f"                <li class='critical-item'>{issue}</li>\n"
        html += """            </ul>
        </div>
"""

    # High priority
    if recommendations['high_priority']:
        html += """
        <div class="section">
            <h2>⚠️ High Priority Issues</h2>
            <ul>
"""
        for issue in recommendations['high_priority'][:10]:
            html += f"                <li class='high-item'>{issue}</li>\n"
        html += """            </ul>
        </div>
"""

    # Metadata section
    html += """
        <div class="section">
            <h2>Metadata Validation</h2>
"""

    if 'metadata_validation' in audit_results:
        meta = audit_results['metadata_validation']
        if 'summary' in meta:
            summary = meta['summary']
            score = summary.get('overall_score', 0)
            score_class = 'score-excellent' if score >= 90 else 'score-good' if score >= 80 else 'score-fair' if score >= 70 else 'score-poor' if score >= 60 else 'score-critical'

            html += f"""
            <div class="card">
                <div class="card-header">
                    <div class="card-title">Overall Metadata Score</div>
                    <div class="card-score {score_class}">{score}/100</div>
                </div>
                <p>Critical Issues: {summary.get('critical_issues', 0)} | Total Issues: {summary.get('total_issues', 0)} | Recommendations: {summary.get('recommendations', 0)}</p>
            </div>
"""

        # Meta title
        if 'meta_title' in meta:
            title = meta['meta_title']
            score = title.get('score', 0)
            score_class = 'score-excellent' if score >= 90 else 'score-good' if score >= 80 else 'score-fair' if score >= 70 else 'score-poor'

            html += f"""
            <div class="card">
                <div class="card-header">
                    <div class="card-title">Meta Title</div>
                    <div class="card-score {score_class}">{score}/100</div>
                </div>
                <p><strong>Title:</strong> {title.get('title', 'Missing')}<br>
                <strong>Length:</strong> {title.get('length', 0)} characters (optimal: 50-60)</p>
            </div>
"""

        # Meta description
        if 'meta_description' in meta:
            desc = meta['meta_description']
            score = desc.get('score', 0)
            score_class = 'score-excellent' if score >= 90 else 'score-good' if score >= 80 else 'score-fair' if score >= 70 else 'score-poor'

            html += f"""
            <div class="card">
                <div class="card-header">
                    <div class="card-title">Meta Description</div>
                    <div class="card-score {score_class}">{score}/100</div>
                </div>
                <p><strong>Length:</strong> {desc.get('length', 0)} characters (optimal: 150-160)</p>
            </div>
"""

    html += "        </div>\n"

    # Keywords section
    html += """
        <div class="section">
            <h2>Keyword Analysis</h2>
"""

    if 'keyword_analysis' in audit_results:
        kw = audit_results['keyword_analysis']
        if 'summary' in kw:
            summary = kw['summary']
            html += f"""
            <div class="card">
                <p>
                    <strong>Total Words:</strong> {summary.get('total_words', 0)} |
                    <strong>Primary Keywords:</strong> {summary.get('primary_keywords', 0)} |
                    <strong>Long-tail:</strong> {summary.get('longtail_keywords', 0)} |
                    <strong>Questions:</strong> {summary.get('question_keywords', 0)} |
                    <strong>Voice Ready:</strong> {summary.get('voice_search_questions', 0)}
                </p>
            </div>
"""

        # Top keywords table
        if 'primary_keywords' in kw and kw['primary_keywords']:
            html += """
            <h3>Top Primary Keywords</h3>
            <table>
                <thead>
                    <tr>
                        <th>Keyword</th>
                        <th>Type</th>
                        <th>Frequency</th>
                        <th>Density</th>
                    </tr>
                </thead>
                <tbody>
"""
            for keyword in kw['primary_keywords'][:10]:
                html += f"""                    <tr>
                        <td><strong>{keyword['keyword']}</strong></td>
                        <td><span class="badge badge-success">{keyword['type']}</span></td>
                        <td>{keyword['frequency']}</td>
                        <td>{keyword.get('density', 0)}%</td>
                    </tr>
"""
            html += """                </tbody>
            </table>
"""

    html += "        </div>\n"

    # Entity section
    html += """
        <div class="section">
            <h2>Entity Analysis (Knowledge Graph)</h2>
"""

    if 'entity_analysis' in audit_results:
        ent = audit_results['entity_analysis']
        if 'summary' in ent:
            summary = ent['summary']
            kg_ready = summary.get('knowledge_graph_ready', False)
            kg_badge = 'badge-success' if kg_ready else 'badge-danger'

            html += f"""
            <div class="card">
                <p>
                    <strong>Persons:</strong> {summary.get('total_persons', 0)} ({summary.get('persons_with_credentials', 0)} with credentials) |
                    <strong>Organizations:</strong> {summary.get('total_organizations', 0)} |
                    <strong>Places:</strong> {summary.get('total_places', 0)} |
                    <span class="badge {kg_badge}">Knowledge Graph: {'Ready' if kg_ready else 'Not Ready'}</span>
                </p>
            </div>
"""

        # Persons
        if 'persons' in ent and ent['persons']:
            html += "<h3>Persons Identified</h3><ul>"
            for person in ent['persons'][:5]:
                creds = f" ({', '.join(person['credentials'])})" if person.get('credentials') else ''
                html += f"<li><strong>{person.get('full_name', person.get('name'))}{creds}</strong> - {person.get('context', 'unknown')}</li>"
            html += "</ul>"

        # Organizations
        if 'organizations' in ent and ent['organizations']:
            html += "<h3>Organizations Identified</h3><ul>"
            for org in ent['organizations'][:5]:
                html += f"<li><strong>{org['name']}</strong> - {org.get('context', 'unknown')}</li>"
            html += "</ul>"

    html += "        </div>\n"

    # Schema section
    html += """
        <div class="section">
            <h2>Schema Markup</h2>
"""

    if 'content_analysis' in audit_results:
        content = audit_results['content_analysis']
        if 'schema' in content and content['schema']:
            html += f"""
            <div class="card">
                <p><span class="badge badge-success">Found: {len(content['schema'])} schema(s)</span></p>
                <ul>
"""
            for schema in content['schema']:
                schema_type = schema.get('@type', 'Unknown') if isinstance(schema, dict) else 'Unknown'
                html += f"                    <li>{schema_type}</li>\n"
            html += """                </ul>
            </div>
"""
        else:
            html += """
            <div class="card">
                <p><span class="badge badge-danger">No JSON-LD schema found</span></p>
                <p><strong>Recommendation:</strong> Add FAQ schema (highest AI citation probability)</p>
            </div>
"""

    html += "        </div>\n"

    # Action items
    html += """
        <div class="section">
            <h2>Priority Action Items</h2>
"""

    if recommendations['critical']:
        html += "<h3>🚨 Critical (Do Now)</h3><ul>"
        for issue in recommendations['critical']:
            html += f"<li class='critical-item'>{issue}</li>"
        html += "</ul>"

    if recommendations['high_priority']:
        html += "<h3>⚠️ High Priority (This Week)</h3><ul>"
        for issue in recommendations['high_priority'][:5]:
            html += f"<li class='high-item'>{issue}</li>"
        html += "</ul>"

    if recommendations['medium_priority']:
        html += "<h3>📋 Medium Priority (This Month)</h3><ul>"
        for issue in recommendations['medium_priority'][:5]:
            html += f"<li class='medium-item'>{issue}</li>"
        html += "</ul>"

    html += """        </div>

        <footer>
            <p>Report generated by <strong>SEO/GEO Optimizer</strong> • Claude Skills</p>
        </footer>
    </div>
</body>
</html>
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    return output_file


def main():
    """Main entry point"""

    # Parse arguments
    if len(sys.argv) < 2 or '--help' in sys.argv or '-h' in sys.argv:
        print(__doc__)
        sys.exit(0 if len(sys.argv) >= 2 else 1)

    file_path = sys.argv[1]

    # Options
    format_type = 'all'  # Default to all formats
    auto_open = False
    output_dir = None

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--format' and i + 1 < len(sys.argv):
            format_type = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--open':
            auto_open = True
            i += 1
        elif sys.argv[i] == '--output-dir' and i + 1 < len(sys.argv):
            output_dir = Path(sys.argv[i + 1])
            i += 2
        else:
            i += 1

    # Validate file
    if not Path(file_path).exists():
        print(json.dumps({
            'error': f'File not found: {file_path}'
        }, indent=2), file=sys.stderr)
        sys.exit(1)

    # Run audit
    try:
        print("\n" + "=" * 60)
        print("SEO/GEO COMPREHENSIVE AUDIT")
        print("=" * 60 + "\n")

        audit_results = run_full_audit(file_path)

        # Calculate overall score
        overall_score = calculate_overall_score(audit_results)
        audit_results['overall_score'] = overall_score
        grade, grade_text, _ = get_score_grade(overall_score)
        audit_results['grade'] = grade
        audit_results['grade_text'] = grade_text

        # Aggregate recommendations
        audit_results['aggregated_recommendations'] = aggregate_recommendations(audit_results)

        # Create output directory
        if output_dir is None:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            output_dir = Path.home() / 'Documents' / f'SEO_Audit_{timestamp}'

        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n📁 Saving reports to: {output_dir}")
        print("-" * 60)

        # Generate reports
        generated_files = []

        if format_type in ['json', 'all']:
            json_file = generate_json_report(audit_results, output_dir)
            generated_files.append(str(json_file))
            print(f"✅ JSON report: {json_file.name}")

        if format_type in ['md', 'all']:
            md_file = generate_markdown_report(audit_results, output_dir)
            generated_files.append(str(md_file))
            print(f"✅ Markdown report: {md_file.name}")

        if format_type in ['html', 'all']:
            html_file = generate_html_report(audit_results, output_dir)
            generated_files.append(str(html_file))
            print(f"✅ HTML report: {html_file.name}")

            # Auto-open HTML
            if auto_open:
                print(f"\n🌐 Opening HTML report in browser...")
                webbrowser.open(f'file://{html_file}')

        print("-" * 60)
        print(f"\n📊 Overall Score: {overall_score}/100 ({grade} - {grade_text})")
        print(f"📁 Reports saved to: {output_dir}\n")

        # Return success
        sys.exit(0)

    except Exception as e:
        print(json.dumps({
            'error': str(e),
            'file': file_path
        }, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
