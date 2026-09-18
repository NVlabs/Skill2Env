"""
Configuration constants for SEO/GEO/AEO Optimizer.

Centralizes all magic numbers, thresholds, and pre-compiled patterns.
"""

import re
from typing import Dict, Pattern

# =============================================================================
# CHARACTER/WORD LIMITS
# =============================================================================

LIMITS: Dict[str, Dict[str, int]] = {
    'meta_title': {
        'min': 30,
        'optimal_min': 50,
        'optimal_max': 60,
        'max': 70,
    },
    'meta_description': {
        'min': 100,
        'optimal_min': 150,
        'optimal_max': 160,
        'max': 170,
    },
    'og_title': {
        'max': 88,
    },
    'og_description': {
        'max': 200,
    },
    'tldr_words': {
        'min': 40,
        'max': 60,
    },
    'paragraph_words': {
        'min': 60,
        'max': 100,
    },
    'sentence_words': {
        'max': 20,
    },
    'faq_answer_words': {
        'min': 40,
        'max': 60,
    },
    'voice_snippet_words': {
        'min': 30,
        'max': 40,
    },
    'content': {
        'min_words': 300,
        'optimal_words': 800,
        'min_h2': 2,
        'optimal_h2': 3,
    },
}

# =============================================================================
# SCORING CONFIGURATION
# =============================================================================

SCORES: Dict[str, Dict] = {
    'thresholds': {
        'excellent': 90,
        'good': 80,
        'fair': 70,
        'poor': 60,
        'critical': 0,
    },
    'weights': {
        'meta_title': 0.15,
        'meta_description': 0.15,
        'open_graph': 0.20,
        'twitter_cards': 0.15,
        'schema': 0.20,
        'content_structure': 0.15,
    },
    'deductions': {
        'critical_issue': 15,
        'regular_issue': 3,
    },
    'bonuses': {
        'has_tldr': 5,
        'has_faq': 5,
        'has_credentials': 10,
        'single_h1': 5,
        'good_h2_count': 5,
        'faq_schema': 10,
        'article_schema': 10,
        'complete_og': 5,
    },
    'citation_boosts': {
        'tldr': 35,           # 35% citation boost
        'credentials': 40,    # 40% citation boost
        'faq_schema': 35,     # 35% citation boost
        'statistics': 41,     # +41% with statistics
        'quotations': 28,     # +28% with quotations
    },
}

# =============================================================================
# PRE-COMPILED REGEX PATTERNS
# =============================================================================

PATTERNS: Dict[str, Pattern] = {
    # Credentials detection
    'credentials': re.compile(
        r'\b(MD|PhD|Ph\.D\.|M\.D\.|MBA|MSc|MPH|DDS|DMD|JD|RN|DO|DPM|OD|PharmD|DVM|EdD|PsyD)\b'
    ),

    # TL;DR detection
    'tldr': re.compile(r'TL;?DR:?\s*', re.IGNORECASE),

    # FAQ heading detection
    'faq_heading': re.compile(
        r'<h[1-3][^>]*>.*?(?:FAQ|Frequently\s+Asked\s+Questions).*?</h[1-3]>',
        re.IGNORECASE | re.DOTALL
    ),

    # ISO date format
    'date_iso': re.compile(r'\d{4}-\d{2}-\d{2}'),

    # dateModified in JSON-LD
    'date_modified': re.compile(r'"dateModified":\s*"([^"]+)"'),

    # Statistics patterns
    'statistics': re.compile(
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(%|percent|years?|months?|patients?|people|users?|cases?)',
        re.IGNORECASE
    ),

    # Year mentions (for freshness). Wide range so freshness checks don't go
    # silent at decade boundaries.
    'year': re.compile(r'\b(19\d{2}|20\d{2}|21\d{2})\b'),

    # Author patterns
    'author': re.compile(r'(?:author|by\s+[A-Z]|written\s+by)', re.IGNORECASE),

    # HTML tag removal
    'html_tags': re.compile(r'<[^>]+>'),

    # Script/style removal
    'script_tags': re.compile(r'<script[^>]*>.*?</script>', re.IGNORECASE | re.DOTALL),
    'style_tags': re.compile(r'<style[^>]*>.*?</style>', re.IGNORECASE | re.DOTALL),

    # Whitespace normalization
    'whitespace': re.compile(r'\s+'),

    # Sentence splitting
    'sentence_end': re.compile(r'(?<=[.!?])\s+'),

    # Heading extraction
    'h1': re.compile(r'<h1[^>]*>(.*?)</h1>', re.IGNORECASE | re.DOTALL),
    'h2': re.compile(r'<h2[^>]*>(.*?)</h2>', re.IGNORECASE | re.DOTALL),
    'h3': re.compile(r'<h3[^>]*>(.*?)</h3>', re.IGNORECASE | re.DOTALL),

    # Markdown headings
    'md_h1': re.compile(r'^#\s+(.+)$', re.MULTILINE),
    'md_h2': re.compile(r'^##\s+(.+)$', re.MULTILINE),
    'md_h3': re.compile(r'^###\s+(.+)$', re.MULTILINE),

    # Word boundary for counting
    'word': re.compile(r'\b\w+\b'),
}

# =============================================================================
# STOP WORDS
# =============================================================================

STOP_WORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and',
    'any', 'are', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below',
    'between', 'both', 'but', 'by', 'can', 'did', 'do', 'does', 'doing', 'don',
    'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'has',
    'have', 'having', 'he', 'her', 'here', 'hers', 'herself', 'him', 'himself',
    'his', 'how', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'itself', 'just',
    'me', 'might', 'more', 'most', 'my', 'myself', 'no', 'nor', 'not', 'now',
    'of', 'off', 'on', 'once', 'only', 'or', 'other', 'our', 'ours', 'ourselves',
    'out', 'over', 'own', 's', 'same', 'she', 'should', 'so', 'some', 'such',
    't', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then',
    'there', 'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under',
    'until', 'up', 'very', 'was', 'we', 'were', 'what', 'when', 'where', 'which',
    'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'you', 'your',
    'yours', 'yourself', 'yourselves'
}

# =============================================================================
# INDEXNOW CONFIGURATION
# =============================================================================

INDEXNOW = {
    # Endpoints sourced from indexnow.org/searchengines.json — each engine's
    # `meta.json` resolves to the `api` URL below. Refresh by running:
    #   curl -s https://www.indexnow.org/searchengines.json
    # and chasing each `meta.json` for its current `api` field.
    'endpoints': {
        'bing': 'https://www.bing.com/indexnow',
        'yandex': 'https://yandex.com/indexnow',
        'seznam': 'https://search.seznam.cz/indexnow',
        'naver': 'https://searchadvisor.naver.com/indexnow',
        'yep': 'https://indexnow.yep.com/indexnow',
        'internetarchive': 'https://internetarchive.indexnow.org/indexnow',
        'amazonbot': 'https://indexnow.amazonbot.amazon/indexnow',
    },
    'key_length': 32,
    'max_batch_urls': 10000,
    'timeout': {
        'single': 10,
        'batch': 30,
    },
}

# =============================================================================
# PLATFORM-SPECIFIC CONFIGURATION
# =============================================================================

PLATFORMS = {
    'chatgpt': {
        'name': 'ChatGPT',
        'priorities': ['credentials', 'tldr', 'article_schema'],
    },
    'perplexity': {
        'name': 'Perplexity',
        'priorities': ['freshness', 'citations', 'date_modified'],
    },
    'claude': {
        'name': 'Claude',
        'priorities': ['structure', 'faq_schema', 'evidence'],
    },
    'gemini': {
        'name': 'Gemini',
        'priorities': ['entity_markup', 'knowledge_graph', 'schema'],
    },
    'grokipedia': {
        'name': 'Grokipedia',
        'priorities': ['realtime', 'social_signals', 'freshness'],
    },
}

# =============================================================================
# FRESHNESS THRESHOLDS
# =============================================================================

FRESHNESS = {
    'max_days_optimal': 30,
    'citation_penalty_multiplier': 3.2,  # 3.2x fewer citations after 30 days
    'update_frequency_days': 3,  # Recommended update frequency for Perplexity
    'stale_year_threshold': 2,  # Years before content is considered stale
}
