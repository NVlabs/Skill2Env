#!/usr/bin/env python3
"""
SEO/GEO Content Analyzer

Analyzes content files (HTML, Markdown, React/JSX) for SEO/GEO optimization.
Extracts metadata, schema, content structure, and generates recommendations.

Usage:
    python analyze_content.py <file_path>
    python analyze_content.py --help

Requirements:
    Python 3.7+ (stdlib only, no external dependencies)

Output:
    JSON with analysis results, issues, recommendations, and SEO score
"""

import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from html.parser import HTMLParser

# Import shared utilities
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))
from shared import has_schema_type, PATTERNS, LIMITS, SCORES


class MetaTagsParser(HTMLParser):
    """HTML parser to extract meta tags"""

    def __init__(self):
        super().__init__()
        self.meta_tags = {}
        self.open_graph = {}
        self.twitter_cards = {}
        self.title = None
        self.in_title = False
        self.json_ld_schemas = []
        self.in_script = False
        self.script_content = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag == 'title':
            self.in_title = True

        elif tag == 'meta':
            # Standard meta tags
            if 'name' in attrs_dict and 'content' in attrs_dict:
                name = attrs_dict['name'].lower()
                content = attrs_dict['content']

                if name in ['description', 'keywords', 'author']:
                    self.meta_tags[name] = content

                # Twitter Cards
                elif name.startswith('twitter:'):
                    key = name.replace('twitter:', '')
                    self.twitter_cards[key] = content

            # Open Graph tags
            elif 'property' in attrs_dict and 'content' in attrs_dict:
                prop = attrs_dict['property'].lower()
                content = attrs_dict['content']

                if prop.startswith('og:'):
                    key = prop.replace('og:', '')
                    self.open_graph[key] = content

        elif tag == 'script':
            # Check for JSON-LD schema
            if attrs_dict.get('type') == 'application/ld+json':
                self.in_script = True
                self.script_content = ""

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        elif tag == 'script' and self.in_script:
            self.in_script = False
            try:
                schema = json.loads(self.script_content)
                self.json_ld_schemas.append(schema)
            except json.JSONDecodeError:
                pass
            self.script_content = ""

    def handle_data(self, data):
        if self.in_title and data.strip():
            self.title = data.strip()
        elif self.in_script:
            self.script_content += data


def analyze_position_bias(text: str) -> Dict:
    """
    Check whether high-leverage content sits in the first ~30% of the body.

    Why: 2026 studies (iPullRank, AIBoost) measured that the first ~30%
    of a page captures ~44% of AI-search citations. If the TL;DR, the
    first statistic, or the first credential mention land below that
    mark, AI platforms see less of the signal.
    """
    words = text.split()
    total = len(words)
    if total == 0:
        return {'total_words': 0, 'warnings': []}

    def word_offset(pattern) -> Optional[int]:
        m = pattern.search(text)
        if not m:
            return None
        return len(text[:m.start()].split())

    def pct(offset: Optional[int]) -> Optional[float]:
        if offset is None:
            return None
        return round(100 * offset / total, 1)

    tldr_off = word_offset(PATTERNS['tldr'])
    stat_off = word_offset(PATTERNS['statistics'])
    cred_off = word_offset(PATTERNS['credentials'])

    warnings = []
    if tldr_off is not None and pct(tldr_off) > 10:
        warnings.append(
            f"TL;DR appears at {pct(tldr_off)}% of body; move it into the "
            f"first 10% so AI platforms catch it in the citation window"
        )
    if stat_off is not None and pct(stat_off) > 30:
        warnings.append(
            f"First statistic appears at {pct(stat_off)}% of body; front-load "
            f"citation-worthy numbers in the first 30%"
        )
    elif stat_off is None and total >= 200:
        warnings.append(
            "No statistics detected; named numerical claims are a strong "
            "AI-citation signal (Princeton GEO tactic, replicated in 2026 studies)"
        )

    return {
        'total_words': total,
        'tldr_position_pct': pct(tldr_off),
        'first_stat_position_pct': pct(stat_off),
        'first_credential_position_pct': pct(cred_off),
        'warnings': warnings,
    }


def extract_html_content(html: str) -> Dict:
    """Extract content elements from HTML"""

    # Remove HTML tags for text analysis
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text_content = re.sub(r'<[^>]+>', ' ', text)
    text_content = re.sub(r'\s+', ' ', text_content).strip()

    # Extract headings
    h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE | re.DOTALL)
    h2_matches = re.findall(r'<h2[^>]*>(.*?)</h2>', html, re.IGNORECASE | re.DOTALL)
    h3_matches = re.findall(r'<h3[^>]*>(.*?)</h3>', html, re.IGNORECASE | re.DOTALL)

    # Clean heading tags
    h1_list = [re.sub(r'<[^>]+>', '', h).strip() for h in h1_matches]
    h2_list = [re.sub(r'<[^>]+>', '', h).strip() for h in h2_matches]
    h3_list = [re.sub(r'<[^>]+>', '', h).strip() for h in h3_matches]

    # Check for TL;DR pattern
    has_tldr = bool(re.search(r'TL;?DR:?\s*', html, re.IGNORECASE))

    # Count words in first 150 words
    words = text_content.split()
    first_150_words = ' '.join(words[:150])
    first_60_words = ' '.join(words[:60])

    # Check for FAQ section
    has_faq = bool(re.search(r'<h[1-3][^>]*>.*?FAQ.*?</h[1-3]>', html, re.IGNORECASE))

    # Check for author info
    has_author = bool(re.search(r'(?:author|by\s+[A-Z]|written\s+by)', html, re.IGNORECASE))

    # Check for credentials (MD, PhD, etc.)
    has_credentials = bool(PATTERNS['credentials'].search(html))

    return {
        'word_count': len(words),
        'h1': h1_list,
        'h2': h2_list,
        'h3': h3_list,
        'h1_count': len(h1_list),
        'h2_count': len(h2_list),
        'h3_count': len(h3_list),
        'has_tldr': has_tldr,
        'has_faq': has_faq,
        'has_author': has_author,
        'has_credentials': has_credentials,
        'first_150_words': first_150_words,
        'first_60_words': first_60_words,
        'full_text': text_content
    }


def analyze_html_file(file_path: str) -> Dict:
    """Analyze HTML file for SEO elements"""

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Parse meta tags and schema
    parser = MetaTagsParser()
    parser.feed(content)

    # Extract content structure
    content_analysis = extract_html_content(content)

    analysis = {
        'file': file_path,
        'file_type': 'html',
        'meta': {
            'title': parser.title,
            'description': parser.meta_tags.get('description'),
            'keywords': parser.meta_tags.get('keywords'),
            'author': parser.meta_tags.get('author')
        },
        'open_graph': parser.open_graph,
        'twitter_cards': parser.twitter_cards,
        'schema': parser.json_ld_schemas,
        'content': content_analysis,
        'position_bias': analyze_position_bias(content_analysis['full_text']),
        'issues': [],
        'recommendations': [],
        'score': 0
    }

    # Validate and score
    analysis['issues'] = validate_metadata(analysis) + analysis['position_bias']['warnings']
    analysis['recommendations'] = generate_recommendations(analysis)
    analysis['score'] = calculate_seo_score(analysis)

    return analysis


def extract_markdown_frontmatter(content: str) -> Tuple[Dict, str]:
    """Extract YAML frontmatter from Markdown"""

    frontmatter = {}
    body = content

    # Check for YAML frontmatter (--- ... ---)
    frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)

    if frontmatter_match:
        yaml_content = frontmatter_match.group(1)
        body = content[frontmatter_match.end():]

        # Simple YAML parser (key: value)
        for line in yaml_content.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip().strip('"\'')

    return frontmatter, body


def analyze_markdown_file(file_path: str) -> Dict:
    """Analyze Markdown file for SEO elements"""

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Extract frontmatter
    frontmatter, body = extract_markdown_frontmatter(content)

    # Extract headings
    h1_matches = re.findall(r'^#\s+(.+)$', body, re.MULTILINE)
    h2_matches = re.findall(r'^##\s+(.+)$', body, re.MULTILINE)
    h3_matches = re.findall(r'^###\s+(.+)$', body, re.MULTILINE)

    # Count words
    text_content = re.sub(r'```.*?```', '', body, flags=re.DOTALL)  # Remove code blocks
    text_content = re.sub(r'`[^`]+`', '', text_content)  # Remove inline code
    text_content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text_content)  # Remove links
    words = text_content.split()

    # Check for TL;DR
    has_tldr = bool(re.search(r'(?:^|\n)(?:\*\*)?TL;?DR(?:\*\*)?:?\s*', body, re.IGNORECASE))

    # Check for FAQ section
    has_faq = bool(re.search(r'^##?\s+(?:FAQ|Frequently Asked Questions)', body, re.MULTILINE | re.IGNORECASE))

    # Check for author
    has_author = bool(
        'author' in frontmatter or
        re.search(r'(?:author|by\s+[A-Z]|written\s+by)', body, re.IGNORECASE)
    )

    # Check for credentials
    has_credentials = bool(PATTERNS['credentials'].search(body))

    first_150_words = ' '.join(words[:150])
    first_60_words = ' '.join(words[:60])

    analysis = {
        'file': file_path,
        'file_type': 'markdown',
        'meta': {
            'title': frontmatter.get('title'),
            'description': frontmatter.get('description'),
            'keywords': frontmatter.get('keywords'),
            'author': frontmatter.get('author')
        },
        'open_graph': {
            'title': frontmatter.get('og:title') or frontmatter.get('title'),
            'description': frontmatter.get('og:description') or frontmatter.get('description'),
            'image': frontmatter.get('og:image')
        },
        'twitter_cards': {
            'card': frontmatter.get('twitter:card'),
            'title': frontmatter.get('twitter:title') or frontmatter.get('title'),
            'description': frontmatter.get('twitter:description') or frontmatter.get('description'),
            'image': frontmatter.get('twitter:image')
        },
        'schema': [],  # Markdown typically doesn't have embedded schema
        'content': {
            'word_count': len(words),
            'h1': h1_matches,
            'h2': h2_matches,
            'h3': h3_matches,
            'h1_count': len(h1_matches),
            'h2_count': len(h2_matches),
            'h3_count': len(h3_matches),
            'has_tldr': has_tldr,
            'has_faq': has_faq,
            'has_author': has_author,
            'has_credentials': has_credentials,
            'first_150_words': first_150_words,
            'first_60_words': first_60_words,
            'full_text': ' '.join(words)
        },
        'frontmatter': frontmatter,
        'position_bias': analyze_position_bias(' '.join(words)),
        'issues': [],
        'recommendations': [],
        'score': 0
    }

    # Validate and score
    analysis['issues'] = validate_metadata(analysis) + analysis['position_bias']['warnings']
    analysis['recommendations'] = generate_recommendations(analysis)
    analysis['score'] = calculate_seo_score(analysis)

    return analysis


def analyze_jsx_file(file_path: str) -> Dict:
    """Analyze React/JSX file for SEO elements"""

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Extract metadata from JSX (Head component, meta tags, etc.)
    meta_title = None
    meta_description = None

    # Check for Next.js metadata
    title_match = re.search(r'title:\s*["\']([^"\']+)["\']', content)
    if title_match:
        meta_title = title_match.group(1)

    desc_match = re.search(r'description:\s*["\']([^"\']+)["\']', content)
    if desc_match:
        meta_description = desc_match.group(1)

    # Extract JSX content (rough approximation)
    jsx_content = re.sub(r'import\s+.*?from\s+["\'].*?["\'];?', '', content)
    jsx_content = re.sub(r'export\s+.*?{', '', jsx_content)

    # Extract headings from JSX
    h1_matches = re.findall(r'<h1[^>]*>([^<]+)</h1>', jsx_content)
    h2_matches = re.findall(r'<h2[^>]*>([^<]+)</h2>', jsx_content)
    h3_matches = re.findall(r'<h3[^>]*>([^<]+)</h3>', jsx_content)

    # Count words in JSX content
    text_content = re.sub(r'<[^>]+>', ' ', jsx_content)
    text_content = re.sub(r'\{[^\}]+\}', ' ', text_content)
    text_content = re.sub(r'\s+', ' ', text_content).strip()
    words = text_content.split()

    # Check patterns
    has_tldr = bool(re.search(r'TL;?DR:?\s*', jsx_content, re.IGNORECASE))
    has_faq = bool(re.search(r'FAQ|Frequently Asked Questions', jsx_content, re.IGNORECASE))
    has_author = bool(re.search(r'author|by\s+[A-Z]', jsx_content, re.IGNORECASE))
    has_credentials = bool(PATTERNS['credentials'].search(jsx_content))

    first_150_words = ' '.join(words[:150])
    first_60_words = ' '.join(words[:60])

    analysis = {
        'file': file_path,
        'file_type': 'jsx/tsx',
        'meta': {
            'title': meta_title,
            'description': meta_description,
            'keywords': None,
            'author': None
        },
        'open_graph': {},
        'twitter_cards': {},
        'schema': [],
        'content': {
            'word_count': len(words),
            'h1': h1_matches,
            'h2': h2_matches,
            'h3': h3_matches,
            'h1_count': len(h1_matches),
            'h2_count': len(h2_matches),
            'h3_count': len(h3_matches),
            'has_tldr': has_tldr,
            'has_faq': has_faq,
            'has_author': has_author,
            'has_credentials': has_credentials,
            'first_150_words': first_150_words,
            'first_60_words': first_60_words,
            'full_text': text_content
        },
        'position_bias': analyze_position_bias(text_content),
        'issues': [],
        'recommendations': [],
        'score': 0
    }

    # Validate and score
    analysis['issues'] = validate_metadata(analysis) + analysis['position_bias']['warnings']
    analysis['recommendations'] = generate_recommendations(analysis)
    analysis['score'] = calculate_seo_score(analysis)

    return analysis


def validate_metadata(analysis: Dict) -> List[str]:
    """Validate metadata completeness"""
    issues = []

    meta = analysis['meta']
    og = analysis['open_graph']
    twitter = analysis['twitter_cards']
    schemas = analysis['schema']
    content = analysis['content']

    # Meta title checks
    if not meta.get('title'):
        issues.append("CRITICAL: Missing meta title (essential for SEO)")
    elif len(meta['title']) > 60:
        issues.append(f"Meta title too long ({len(meta['title'])} chars, should be 50-60)")
    elif len(meta['title']) < 30:
        issues.append(f"Meta title too short ({len(meta['title'])} chars, should be 50-60)")

    # Meta description checks
    if not meta.get('description'):
        issues.append("CRITICAL: Missing meta description (essential for SEO)")
    elif len(meta['description']) > 160:
        issues.append(f"Meta description too long ({len(meta['description'])} chars, should be 150-160)")
    elif len(meta['description']) < 100:
        issues.append(f"Meta description too short ({len(meta['description'])} chars, should be 150-160)")

    # Open Graph checks
    if not og.get('title'):
        issues.append("Missing og:title (poor social media preview)")
    if not og.get('description'):
        issues.append("Missing og:description (poor social media preview)")
    if not og.get('image'):
        issues.append("Missing og:image (no preview image on Facebook/LinkedIn/WhatsApp)")

    # Twitter Cards checks
    if not twitter.get('card'):
        issues.append("Missing twitter:card (poor Twitter/X preview)")
    if not twitter.get('image'):
        issues.append("Missing twitter:image (no preview image on Twitter/X)")

    # Schema checks
    has_faq_schema = has_schema_type(schemas, 'FAQPage')
    has_article_schema = has_schema_type(schemas, 'Article')

    if not has_faq_schema and content['has_faq']:
        issues.append("Missing FAQ schema (highest AI citation probability for FAQ content)")
    if not has_article_schema:
        issues.append("Missing Article schema (E-E-A-T signals for AI citation)")

    # Content structure checks
    if not content['has_tldr']:
        issues.append("Missing TL;DR in first 60 words (35% citation boost for AI search)")
    if content['h1_count'] == 0:
        issues.append("CRITICAL: Missing H1 heading (essential for SEO)")
    elif content['h1_count'] > 1:
        issues.append(f"Multiple H1 headings found ({content['h1_count']}), should have exactly 1")
    if content['h2_count'] < 2:
        issues.append("Should have at least 2 H2 headings for proper structure")
    if content['has_faq'] and not has_faq_schema:
        issues.append("FAQ section found but missing FAQ schema markup")
    if not content['has_author']:
        issues.append("Missing author attribution (40% citation boost with credentials)")
    if not content['has_credentials'] and content['has_author']:
        issues.append("Author found but no credentials (MD, PhD) - add for 40% citation boost")
    if content['word_count'] < 300:
        issues.append(f"Content too short ({content['word_count']} words, minimum 300 recommended)")

    return issues


def generate_recommendations(analysis: Dict) -> List[str]:
    """Generate SEO recommendations"""
    recommendations = []

    content = analysis['content']
    schemas = analysis['schema']

    # AI citation optimization
    if not content['has_tldr']:
        recommendations.append("Add TL;DR in first 40-60 words (35% citation boost for ChatGPT/Perplexity)")

    if not has_schema_type(schemas, 'FAQPage'):
        recommendations.append("Add FAQ schema (highest LLM citation probability - use schema_generator.py)")

    if not has_schema_type(schemas, 'Article'):
        recommendations.append("Add Article schema with author credentials (40% citation boost)")

    # Voice search optimization
    has_speakable = any(
        'speakable' in str(s).lower()
        for s in schemas
    )
    if not has_speakable:
        recommendations.append("Add Speakable schema for voice search optimization (Google Assistant, Siri, Alexa)")

    if content['has_faq'] and not has_faq_schema:
        recommendations.append("Add FAQ section with 29-word answers for voice search (80% of answers from top 3)")

    # Social preview optimization
    og = analysis['open_graph']
    if not og.get('image'):
        recommendations.append("Add Open Graph image (1200×630px for Facebook/LinkedIn/WhatsApp previews)")

    # Content structure recommendations
    if content['h2_count'] < 3:
        recommendations.append(f"Add more H2 headings ({content['h2_count']} found, 3-5 recommended for AI scan-ability)")

    if not content['has_author']:
        recommendations.append("Add author attribution with credentials (MD, PhD, etc.) - 40% citation boost")

    if content['word_count'] < 800:
        recommendations.append(f"Expand content ({content['word_count']} words, 800-1500 recommended for comprehensive coverage)")

    # Platform-specific recommendations
    if content['has_credentials']:
        recommendations.append("✅ STRENGTH: Author credentials present - excellent for ChatGPT citation")
    if content['h1_count'] == 1 and content['h2_count'] >= 2:
        recommendations.append("✅ STRENGTH: Proper heading hierarchy - excellent for AI parsing")

    return recommendations


def calculate_seo_score(analysis: Dict) -> int:
    """Calculate overall SEO score (0-100)"""
    score = 100

    issues = analysis['issues']
    content = analysis['content']
    schemas = analysis['schema']

    # Deduct points for critical issues
    critical_issues = [i for i in issues if 'CRITICAL' in i]
    score -= len(critical_issues) * 15

    # Deduct points for regular issues
    regular_issues = [i for i in issues if 'CRITICAL' not in i]
    score -= len(regular_issues) * 3

    # Bonus points for best practices
    if content['has_tldr']:
        score += 5
    if content['has_faq']:
        score += 5
    if content['has_credentials']:
        score += 10
    if content['h1_count'] == 1:
        score += 5
    if content['h2_count'] >= 3:
        score += 5

    # Bonus for schema markup
    if has_schema_type(schemas, 'FAQPage'):
        score += SCORES['bonuses']['faq_schema']

    if has_schema_type(schemas, 'Article'):
        score += SCORES['bonuses']['article_schema']

    # Bonus for Open Graph
    og = analysis['open_graph']
    if og.get('title') and og.get('description') and og.get('image'):
        score += 5

    return max(0, min(100, score))


def analyze_file(file_path: str) -> Dict:
    """Analyze file based on type"""

    path = Path(file_path)

    if not path.exists():
        return {
            'error': f'File not found: {file_path}',
            'file': file_path,
            'score': 0
        }

    suffix = path.suffix.lower()

    if suffix in ['.html', '.htm']:
        return analyze_html_file(file_path)
    elif suffix in ['.md', '.mdx', '.markdown']:
        return analyze_markdown_file(file_path)
    elif suffix in ['.jsx', '.tsx', '.js', '.ts']:
        return analyze_jsx_file(file_path)
    else:
        return {
            'error': f'Unsupported file type: {suffix}',
            'file': file_path,
            'score': 0,
            'supported_types': ['.html', '.htm', '.md', '.mdx', '.markdown', '.jsx', '.tsx', '.js', '.ts']
        }


def main():
    """Main entry point"""

    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h']:
        print(__doc__)
        print("\nExamples:")
        print("  python analyze_content.py ~/project/about.html")
        print("  python analyze_content.py ~/blog/post.md")
        print("  python analyze_content.py ~/app/pages/index.tsx")
        sys.exit(0 if len(sys.argv) >= 2 else 1)

    file_path = sys.argv[1]

    try:
        analysis = analyze_file(file_path)

        # Pretty print JSON
        print(json.dumps(analysis, indent=2, ensure_ascii=False))

        # Exit code based on score
        if 'error' in analysis:
            sys.exit(1)
        elif analysis['score'] < 60:
            sys.exit(2)  # Poor SEO
        else:
            sys.exit(0)  # Good SEO

    except Exception as e:
        print(json.dumps({
            'error': str(e),
            'file': file_path,
            'score': 0
        }, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
