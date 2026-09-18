#!/usr/bin/env python3
"""
Voice Search Optimizer

Optimizes content for voice search assistants (Google Assistant, Siri, Alexa).
Generates featured snippet content, Speakable schema, and validates voice-readiness.

Key optimizations:
- Featured snippet extraction (30-40 words)
- Speakable schema for voice assistants
- Question-answer pattern detection
- Speaking time validation (20-30 second segments)

Usage:
    python voice_optimizer.py <file_path>
    python voice_optimizer.py <file_path> --json
    python voice_optimizer.py --help

Requirements:
    Python 3.7+ (stdlib only)

Output:
    Optimized HTML file with Speakable schema, or JSON analysis
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Import shared utilities
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))
from shared import LIMITS, PATTERNS, count_words, extract_sentences, has_question_pattern


def generate_featured_snippet(text: str, max_words: int = 40) -> Dict:
    """
    Extract optimal featured snippet content (30-40 words).

    Google's featured snippets typically use 40-50 words,
    but voice answers are shorter (29 words average).

    Args:
        text: Source text content
        max_words: Maximum words for snippet

    Returns:
        Dict with snippet text and metadata
    """
    sentences = extract_sentences(text)
    words = []
    used_sentences = []

    for sentence in sentences:
        sentence_words = sentence.split()
        if len(words) + len(sentence_words) <= max_words:
            words.extend(sentence_words)
            used_sentences.append(sentence)
        if len(words) >= 30:  # Minimum threshold
            break

    snippet_text = ' '.join(words[:max_words])
    word_count = count_words(snippet_text)

    # Estimate speaking time (150 wpm average)
    speaking_seconds = int((word_count / 150) * 60)

    return {
        'text': snippet_text,
        'word_count': word_count,
        'sentence_count': len(used_sentences),
        'speaking_time_seconds': speaking_seconds,
        'optimal': 30 <= word_count <= 40
    }


def analyze_voice_readiness(html: str) -> Dict:
    """
    Analyze content for voice search optimization.

    Checks for:
    - Question-answer patterns
    - Speakable content segments
    - Sentence length (ideal: 15-20 words)
    - FAQ sections

    Args:
        html: HTML content

    Returns:
        Analysis results dict
    """
    # Remove HTML tags for text analysis
    text = PATTERNS['script_tags'].sub('', html)
    text = PATTERNS['style_tags'].sub('', text)
    text = PATTERNS['html_tags'].sub(' ', text)
    text = PATTERNS['whitespace'].sub(' ', text).strip()

    sentences = extract_sentences(text)
    issues = []
    strengths = []

    # Analyze sentence lengths
    long_sentences = []
    short_sentences = []
    ideal_sentences = []

    for sentence in sentences:
        word_count = count_words(sentence)
        if word_count > 25:
            long_sentences.append(sentence[:50] + '...')
        elif word_count < 10:
            short_sentences.append(sentence)
        elif 15 <= word_count <= 20:
            ideal_sentences.append(sentence)

    if long_sentences:
        issues.append(f"{len(long_sentences)} sentences too long for voice (>25 words)")
    if len(ideal_sentences) >= 3:
        strengths.append(f"{len(ideal_sentences)} sentences at ideal length (15-20 words)")

    # Check for question patterns
    questions = [s for s in sentences if has_question_pattern(s)]
    if questions:
        strengths.append(f"{len(questions)} question patterns found (voice search friendly)")
    else:
        issues.append("No question patterns found - add FAQ content")

    # Check for FAQ section
    has_faq = bool(PATTERNS['faq_heading'].search(html))
    if has_faq:
        strengths.append("FAQ section present (highest voice search compatibility)")
    else:
        issues.append("Missing FAQ section (recommended for voice search)")

    # Check for existing Speakable schema
    has_speakable = 'speakable' in html.lower()
    if has_speakable:
        strengths.append("Speakable schema already present")
    else:
        issues.append("Missing Speakable schema")

    # Generate featured snippet
    snippet = generate_featured_snippet(text)

    # Calculate voice readiness score
    score = 100
    score -= len(issues) * 15
    score += len(strengths) * 5
    score = max(0, min(100, score))

    return {
        'score': score,
        'total_sentences': len(sentences),
        'ideal_length_sentences': len(ideal_sentences),
        'long_sentences': len(long_sentences),
        'questions_found': len(questions),
        'has_faq': has_faq,
        'has_speakable': has_speakable,
        'featured_snippet': snippet,
        'issues': issues,
        'strengths': strengths
    }


def generate_speakable_schema(
    selectors: Optional[List[str]] = None,
    xpaths: Optional[List[str]] = None
) -> Dict:
    """
    Generate Speakable schema specification.

    Speakable identifies content suitable for text-to-speech.

    Args:
        selectors: CSS selectors for speakable content
        xpaths: XPath expressions for speakable content

    Returns:
        Speakable schema dict
    """
    schema = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "speakable": {
            "@type": "SpeakableSpecification"
        }
    }

    if selectors:
        schema["speakable"]["cssSelector"] = selectors
    else:
        # Default selectors for common speakable content
        schema["speakable"]["cssSelector"] = [
            ".tldr",
            ".summary",
            ".featured-snippet",
            "article > p:first-of-type",
            "h1",
            "h2"
        ]

    if xpaths:
        schema["speakable"]["xpath"] = xpaths

    return schema


def add_speakable_to_html(html: str, selectors: Optional[List[str]] = None) -> str:
    """
    Add Speakable schema to HTML content.

    Args:
        html: HTML content
        selectors: CSS selectors for speakable content

    Returns:
        HTML with Speakable schema added
    """
    # Check if already has speakable
    if 'SpeakableSpecification' in html:
        return html

    schema = generate_speakable_schema(selectors)
    schema_json = json.dumps(schema, indent=2)
    script_tag = f'<script type="application/ld+json">\n{schema_json}\n</script>\n'

    # Insert before </head>
    if '</head>' in html:
        html = html.replace('</head>', f'{script_tag}</head>')
    elif '<body' in html:
        # Insert before body if no head
        html = html.replace('<body', f'{script_tag}<body')
    else:
        # Prepend if no structure
        html = script_tag + html

    return html


def optimize_for_voice(file_path: str, output_path: Optional[str] = None) -> Dict:
    """
    Optimize HTML file for voice search.

    Args:
        file_path: Input HTML file path
        output_path: Output file path (auto-generated if None)

    Returns:
        Optimization results dict
    """
    path = Path(file_path)

    if not path.exists():
        return {
            'success': False,
            'error': f'File not found: {file_path}'
        }

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    # Analyze current state
    analysis = analyze_voice_readiness(html)

    # Apply optimizations
    changes = []

    # Add Speakable schema if missing
    if not analysis['has_speakable']:
        html = add_speakable_to_html(html)
        changes.append("Added Speakable schema")

    # Determine output path
    if output_path is None:
        output_path = str(path.parent / f"{path.stem}-voice{path.suffix}")

    # Write optimized file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return {
        'success': True,
        'input_file': file_path,
        'output_file': output_path,
        'analysis': analysis,
        'changes': changes,
        'timestamp': datetime.now().isoformat()
    }


def main():
    """Main entry point"""

    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h']:
        print(__doc__)
        print("\nExamples:")
        print("  python voice_optimizer.py page.html")
        print("  python voice_optimizer.py page.html --json")
        print("  python voice_optimizer.py page.html --output optimized.html")
        sys.exit(0 if '--help' in sys.argv else 1)

    file_path = sys.argv[1]
    json_output = '--json' in sys.argv

    # Parse output path
    output_path = None
    if '--output' in sys.argv:
        idx = sys.argv.index('--output')
        if idx + 1 < len(sys.argv):
            output_path = sys.argv[idx + 1]

    try:
        result = optimize_for_voice(file_path, output_path)

        if json_output:
            print(json.dumps(result, indent=2))
        else:
            if result['success']:
                print(f"✓ Voice optimization complete: {result['output_file']}")
                print(f"  Voice readiness score: {result['analysis']['score']}/100")
                print(f"  Questions found: {result['analysis']['questions_found']}")
                if result['changes']:
                    print("  Changes applied:")
                    for change in result['changes']:
                        print(f"    - {change}")
                if result['analysis']['issues']:
                    print("  Remaining issues:")
                    for issue in result['analysis']['issues'][:3]:
                        print(f"    - {issue}")
            else:
                print(f"✗ Error: {result.get('error', 'Unknown error')}")
                sys.exit(1)

        sys.exit(0 if result['success'] else 1)

    except Exception as e:
        if json_output:
            print(json.dumps({'success': False, 'error': str(e)}, indent=2))
        else:
            print(f"✗ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
