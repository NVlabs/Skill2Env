#!/usr/bin/env python3
"""
SEO/GEO/AEO Keyword Analyzer

Extracts and analyzes keywords from content files for SEO/GEO/AEO optimization.
Identifies primary, semantic, LSI, long-tail, and question-based keywords.
Includes keyword clustering for semantic grouping.

Usage:
    python keyword_analyzer.py <file_path>
    python keyword_analyzer.py <file_path> --clusters
    python keyword_analyzer.py --help

Requirements:
    Python 3.7+ (stdlib only)

Output:
    JSON with categorized keywords, density analysis, and semantic clusters
"""

import json
import sys
import re
import math
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import Counter, defaultdict

# Import shared utilities and analyze_content functions
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))
from shared import STOP_WORDS, tokenize, extract_ngrams
from analyze_content import analyze_file, extract_html_content, extract_markdown_frontmatter


def extract_text_content(file_path: str) -> Dict:
    """Extract clean text content from file"""

    path = Path(file_path)
    suffix = path.suffix.lower()

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    text = ""
    title = ""
    headings = []

    if suffix in ['.html', '.htm']:
        # Extract title
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        if title_match:
            title = title_match.group(1).strip()

        # Extract all headings
        for level in range(1, 7):
            matches = re.findall(rf'<h{level}[^>]*>(.*?)</h{level}>', content, re.IGNORECASE | re.DOTALL)
            headings.extend([re.sub(r'<[^>]+>', '', h).strip() for h in matches])

        # Extract clean text
        html_analysis = extract_html_content(content)
        text = html_analysis['full_text']

    elif suffix in ['.md', '.mdx', '.markdown']:
        # Extract frontmatter
        frontmatter, body = extract_markdown_frontmatter(content)
        title = frontmatter.get('title', '')

        # Extract headings
        headings = re.findall(r'^#{1,6}\s+(.+)$', body, re.MULTILINE)

        # Clean text
        text = re.sub(r'```.*?```', '', body, flags=re.DOTALL)
        text = re.sub(r'`[^`]+`', '', text)
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        text = re.sub(r'[#*_`]', '', text)

    elif suffix in ['.jsx', '.tsx', '.js', '.ts']:
        # Extract from JSX/TSX
        title_match = re.search(r'title:\s*["\']([^"\']+)["\']', content)
        if title_match:
            title = title_match.group(1)

        # Extract headings from JSX
        for level in range(1, 7):
            matches = re.findall(rf'<h{level}[^>]*>([^<]+)</h{level}>', content)
            headings.extend(matches)

        # Extract text
        text = re.sub(r'import\s+.*?from\s+["\'].*?["\'];?', '', content)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\{[^\}]+\}', ' ', text)

    # Clean text
    text = re.sub(r'\s+', ' ', text).strip()

    return {
        'title': title,
        'headings': headings,
        'text': text,
        'word_count': len(text.split())
    }


# tokenize_text replaced by shared.tokenize
# extract_ngrams replaced by shared.extract_ngrams


def extract_primary_keywords(content: Dict, top_n: int = 10) -> List[Dict]:
    """
    Extract primary keywords from title, H1, H2, and first 100 words
    These are the main topic keywords
    """
    # Combine high-priority text
    priority_text = ' '.join([
        content['title'],
        ' '.join(content['headings'][:3]),  # First 3 headings
        ' '.join(content['text'].split()[:100])  # First 100 words
    ])

    words = tokenize(priority_text)

    # Count single words
    word_counts = Counter(words)

    # Count 2-grams
    bigrams = extract_ngrams(words, 2)
    bigram_counts = Counter(bigrams)

    # Combine and rank
    keywords = []

    # Top single words
    for word, count in word_counts.most_common(top_n):
        keywords.append({
            'keyword': word,
            'type': '1-gram',
            'frequency': count,
            'score': count
        })

    # Top 2-grams
    for bigram, count in bigram_counts.most_common(top_n // 2):
        keywords.append({
            'keyword': bigram,
            'type': '2-gram',
            'frequency': count,
            'score': count * 1.5  # Boost multi-word keywords
        })

    # Sort by score
    keywords.sort(key=lambda x: x['score'], reverse=True)

    return keywords[:top_n]


def extract_semantic_keywords(content: Dict, primary: List[Dict], top_n: int = 15) -> List[Dict]:
    """
    Extract semantic keywords (related terms)
    Found in H2/H3 headings and body content
    """
    # Extract from H2/H3 and body
    semantic_text = ' '.join([
        ' '.join(content['headings'][1:]),  # All headings except H1
        content['text']
    ])

    words = tokenize(semantic_text)

    # Remove primary keywords to avoid duplication
    primary_words = set()
    for kw in primary:
        primary_words.update(kw['keyword'].split())

    words = [w for w in words if w not in primary_words]

    # Count words
    word_counts = Counter(words)

    # Count 2-grams
    bigrams = extract_ngrams(words, 2)
    bigram_counts = Counter(bigrams)

    keywords = []

    # Top single words
    for word, count in word_counts.most_common(top_n):
        keywords.append({
            'keyword': word,
            'type': '1-gram',
            'frequency': count,
            'context': 'semantic'
        })

    # Top 2-grams
    for bigram, count in bigram_counts.most_common(top_n // 2):
        keywords.append({
            'keyword': bigram,
            'type': '2-gram',
            'frequency': count,
            'context': 'semantic'
        })

    return keywords[:top_n]


def extract_longtail_keywords(content: Dict, top_n: int = 10) -> List[Dict]:
    """
    Extract long-tail keywords (3-8 word phrases)
    Found in FAQ sections and H3 headings
    """
    words = tokenize(content['text'])

    longtail = []

    # Extract 3-grams
    trigrams = extract_ngrams(words, 3)
    trigram_counts = Counter(trigrams)

    for trigram, count in trigram_counts.most_common(top_n):
        if count >= 2:  # Must appear at least twice
            longtail.append({
                'keyword': trigram,
                'type': '3-gram',
                'frequency': count,
                'length': 'long-tail'
            })

    # Extract 4-grams
    fourgrams = extract_ngrams(words, 4)
    fourgram_counts = Counter(fourgrams)

    for fourgram, count in fourgram_counts.most_common(top_n // 2):
        if count >= 2:
            longtail.append({
                'keyword': fourgram,
                'type': '4-gram',
                'frequency': count,
                'length': 'long-tail'
            })

    return longtail[:top_n]


def extract_question_keywords(content: Dict) -> List[Dict]:
    """
    Extract question-based keywords
    Critical for voice search and FAQ schema
    """
    questions = []

    # Question patterns
    question_words = ['what', 'how', 'why', 'when', 'where', 'who', 'which', 'whose', 'can', 'does', 'is', 'are']

    # Extract from text
    sentences = re.split(r'[.!?]', content['text'])

    for sentence in sentences:
        sentence = sentence.strip()
        first_word = sentence.lower().split()[0] if sentence else ''

        if first_word in question_words or sentence.endswith('?'):
            if len(sentence.split()) >= 3:  # Minimum 3 words
                questions.append({
                    'question': sentence,
                    'type': 'natural',
                    'word_count': len(sentence.split()),
                    'voice_search_optimized': len(sentence.split()) <= 10
                })

    # Extract from headings
    for heading in content['headings']:
        first_word = heading.lower().split()[0] if heading else ''
        if first_word in question_words or '?' in heading:
            questions.append({
                'question': heading,
                'type': 'heading',
                'word_count': len(heading.split()),
                'voice_search_optimized': len(heading.split()) <= 10
            })

    return questions


def calculate_keyword_density(content: Dict, keywords: List[Dict]) -> List[Dict]:
    """Calculate keyword density percentage"""
    total_words = content['word_count']

    for keyword in keywords:
        frequency = keyword.get('frequency', 0)
        word_count = len(keyword['keyword'].split())
        # Density = (keyword frequency * word count) / total words * 100
        density = (frequency * word_count) / total_words * 100 if total_words > 0 else 0
        keyword['density'] = round(density, 2)

    return keywords


# =============================================================================
# KEYWORD CLUSTERING (TF-IDF + Cosine Similarity)
# =============================================================================

def build_vocabulary(keywords: List[str]) -> Dict[str, int]:
    """Build vocabulary from all keyword terms"""
    vocab = {}
    idx = 0
    for kw in keywords:
        for word in kw.lower().split():
            if word not in vocab:
                vocab[word] = idx
                idx += 1
    return vocab


def calculate_tf(keyword: str, vocab: Dict[str, int]) -> List[float]:
    """Calculate term frequency vector for a keyword"""
    words = keyword.lower().split()
    word_count = Counter(words)
    total = len(words)

    vector = [0.0] * len(vocab)
    for word, count in word_count.items():
        if word in vocab:
            vector[vocab[word]] = count / total if total > 0 else 0
    return vector


def calculate_idf(keywords: List[str], vocab: Dict[str, int]) -> List[float]:
    """Calculate inverse document frequency for vocabulary"""
    n_docs = len(keywords)
    doc_freq = [0] * len(vocab)

    for kw in keywords:
        words = set(kw.lower().split())
        for word in words:
            if word in vocab:
                doc_freq[vocab[word]] += 1

    # IDF = log(N / (df + 1)) + 1 (smoothed)
    idf = [math.log(n_docs / (df + 1)) + 1 for df in doc_freq]
    return idf


def calculate_tfidf(keyword: str, vocab: Dict[str, int], idf: List[float]) -> List[float]:
    """Calculate TF-IDF vector for a keyword"""
    tf = calculate_tf(keyword, vocab)
    return [tf[i] * idf[i] for i in range(len(vocab))]


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors"""
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))

    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_product / (norm1 * norm2)


def cluster_keywords(keywords: List[Dict], similarity_threshold: float = 0.3) -> List[Dict]:
    """
    Cluster keywords based on TF-IDF cosine similarity.

    Uses a simple agglomerative approach:
    1. Calculate TF-IDF vectors for all keywords
    2. Group keywords with similarity above threshold
    3. Name clusters by most frequent/important keyword

    Args:
        keywords: List of keyword dicts with 'keyword' field
        similarity_threshold: Min similarity to group (0.0-1.0)

    Returns:
        List of cluster dicts with name, keywords, and topic
    """
    if not keywords:
        return []

    # Extract keyword strings
    kw_strings = [kw['keyword'] for kw in keywords]

    if len(kw_strings) < 2:
        return [{
            'name': kw_strings[0] if kw_strings else 'unknown',
            'keywords': kw_strings,
            'size': len(kw_strings),
            'topic': 'primary'
        }]

    # Build vocabulary and calculate IDF
    vocab = build_vocabulary(kw_strings)
    if not vocab:
        return []

    idf = calculate_idf(kw_strings, vocab)

    # Calculate TF-IDF vectors
    vectors = [calculate_tfidf(kw, vocab, idf) for kw in kw_strings]

    # Track which keywords are assigned to clusters
    assigned = [False] * len(kw_strings)
    clusters = []

    for i, kw in enumerate(kw_strings):
        if assigned[i]:
            continue

        # Start new cluster with this keyword
        cluster_keywords = [kw]
        assigned[i] = True

        # Find similar keywords
        for j in range(i + 1, len(kw_strings)):
            if assigned[j]:
                continue

            similarity = cosine_similarity(vectors[i], vectors[j])
            if similarity >= similarity_threshold:
                cluster_keywords.append(kw_strings[j])
                assigned[j] = True

        # Also check word overlap for short keywords
        for j in range(i + 1, len(kw_strings)):
            if assigned[j]:
                continue

            words_i = set(kw.lower().split())
            words_j = set(kw_strings[j].lower().split())
            overlap = len(words_i & words_j)

            # If significant word overlap, add to cluster
            if overlap > 0 and overlap >= min(len(words_i), len(words_j)) * 0.5:
                cluster_keywords.append(kw_strings[j])
                assigned[j] = True

        # Determine cluster topic based on common words
        all_words = []
        for ckw in cluster_keywords:
            all_words.extend(ckw.lower().split())
        word_freq = Counter(all_words)

        # Filter out stop words for topic
        topic_words = [w for w, _ in word_freq.most_common(3) if w not in STOP_WORDS]
        topic = ' '.join(topic_words[:2]) if topic_words else cluster_keywords[0]

        clusters.append({
            'name': cluster_keywords[0],  # First keyword as cluster name
            'topic': topic,
            'keywords': cluster_keywords,
            'size': len(cluster_keywords)
        })

    # Sort clusters by size (largest first)
    clusters.sort(key=lambda x: x['size'], reverse=True)

    return clusters


def generate_cluster_recommendations(clusters: List[Dict]) -> List[str]:
    """Generate SEO recommendations based on keyword clusters"""
    recommendations = []

    if not clusters:
        recommendations.append("No keyword clusters found - add more varied content")
        return recommendations

    # Check cluster distribution
    total_keywords = sum(c['size'] for c in clusters)
    largest_cluster = clusters[0] if clusters else None

    if largest_cluster and largest_cluster['size'] > total_keywords * 0.6:
        recommendations.append(
            f"Topic concentration: {largest_cluster['size']}/{total_keywords} keywords in '{largest_cluster['topic']}' cluster. "
            "Consider diversifying content topics."
        )

    # Check for single-keyword clusters (orphan topics)
    orphans = [c for c in clusters if c['size'] == 1]
    if len(orphans) > len(clusters) * 0.5:
        recommendations.append(
            f"{len(orphans)} orphan keywords without related terms. "
            "Add supporting content for these topics."
        )

    # Recommend content for top clusters
    if len(clusters) >= 2:
        top_topics = [c['topic'] for c in clusters[:3]]
        recommendations.append(
            f"Top topic clusters: {', '.join(top_topics)}. "
            "Create pillar content for each cluster."
        )

    # Check cluster count
    if len(clusters) < 3:
        recommendations.append(
            "Limited topic diversity. Add content covering 3-5 distinct topic clusters "
            "for better topical authority."
        )
    elif len(clusters) > 10:
        recommendations.append(
            f"{len(clusters)} topic clusters detected. Consider consolidating into "
            "5-7 main topic pillars for clearer site structure."
        )

    return recommendations


def analyze_keywords(file_path: str, include_clusters: bool = True) -> Dict:
    """Main keyword analysis function"""

    # Extract content
    content = extract_text_content(file_path)

    if content['word_count'] == 0:
        return {
            'error': 'No text content found in file',
            'file': file_path
        }

    # Extract different keyword types
    primary = extract_primary_keywords(content, top_n=10)
    semantic = extract_semantic_keywords(content, primary, top_n=15)
    longtail = extract_longtail_keywords(content, top_n=10)
    questions = extract_question_keywords(content)

    # Calculate densities
    primary = calculate_keyword_density(content, primary)
    semantic = calculate_keyword_density(content, semantic)
    longtail = calculate_keyword_density(content, longtail)

    # Analysis summary
    summary = {
        'total_words': content['word_count'],
        'unique_words': len(set(tokenize(content['text']))),
        'primary_keywords': len(primary),
        'semantic_keywords': len(semantic),
        'longtail_keywords': len(longtail),
        'question_keywords': len(questions),
        'voice_search_questions': len([q for q in questions if q.get('voice_search_optimized')])
    }

    # Recommendations
    recommendations = []

    if len(questions) == 0:
        recommendations.append("Add question-based content for voice search optimization")
    elif len(questions) < 3:
        recommendations.append(f"Add more FAQ content ({len(questions)} questions found, 5+ recommended)")
    else:
        recommendations.append(f"Good FAQ coverage ({len(questions)} questions found)")

    if len(longtail) < 5:
        recommendations.append("Add more long-tail keyword phrases (3-5 word combinations)")

    # Check keyword density (should be 1-3% for primary keywords)
    if primary:
        top_keyword = primary[0]
        if top_keyword['density'] > 3:
            recommendations.append(f"Primary keyword '{top_keyword['keyword']}' density too high ({top_keyword['density']}%), risk of keyword stuffing")
        elif top_keyword['density'] < 0.5:
            recommendations.append(f"Primary keyword '{top_keyword['keyword']}' density too low ({top_keyword['density']}%), increase usage")

    result = {
        'file': file_path,
        'summary': summary,
        'primary_keywords': primary,
        'semantic_keywords': semantic,
        'longtail_keywords': longtail,
        'question_keywords': questions,
        'recommendations': recommendations
    }

    # Add keyword clustering if requested
    if include_clusters:
        # Combine all keywords for clustering
        all_keywords = primary + semantic + longtail
        clusters = cluster_keywords(all_keywords, similarity_threshold=0.3)

        result['keyword_clusters'] = clusters
        result['summary']['cluster_count'] = len(clusters)

        # Add cluster-specific recommendations
        cluster_recs = generate_cluster_recommendations(clusters)
        result['cluster_recommendations'] = cluster_recs

    return result


def main():
    """Main entry point"""

    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h']:
        print(__doc__)
        print("\nExamples:")
        print("  python keyword_analyzer.py ~/project/about.html")
        print("  python keyword_analyzer.py ~/blog/post.md")
        print("  python keyword_analyzer.py ~/blog/post.md --clusters")
        print("  python keyword_analyzer.py ~/blog/post.md --no-clusters")
        print("\nOptions:")
        print("  --clusters     Include keyword clustering (default)")
        print("  --no-clusters  Disable keyword clustering for faster analysis")
        sys.exit(0 if len(sys.argv) >= 2 else 1)

    file_path = sys.argv[1]

    # Parse options
    include_clusters = True
    if '--no-clusters' in sys.argv:
        include_clusters = False

    try:
        analysis = analyze_keywords(file_path, include_clusters=include_clusters)

        # Pretty print JSON
        print(json.dumps(analysis, indent=2, ensure_ascii=False))

        # Exit code
        if 'error' in analysis:
            sys.exit(1)
        else:
            sys.exit(0)

    except Exception as e:
        print(json.dumps({
            'error': str(e),
            'file': file_path
        }, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
