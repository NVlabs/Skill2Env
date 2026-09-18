"""
Shared utilities for SEO/GEO/AEO Optimizer scripts.

Provides common functions for schema validation, text processing,
and configuration constants.
"""

from .config import LIMITS, SCORES, PATTERNS, STOP_WORDS, FRESHNESS, INDEXNOW, PLATFORMS
from .schema_utils import has_schema_type, get_schema_by_type, validate_schema_structure
from .text_utils import (
    count_words,
    tokenize,
    extract_sentences,
    extract_ngrams,
    clean_html_text,
    has_question_pattern,
    extract_statistics,
    has_credentials,
)

__all__ = [
    # Config
    'LIMITS',
    'SCORES',
    'PATTERNS',
    'STOP_WORDS',
    'FRESHNESS',
    'INDEXNOW',
    'PLATFORMS',
    # Schema utils
    'has_schema_type',
    'get_schema_by_type',
    'validate_schema_structure',
    # Text utils
    'count_words',
    'tokenize',
    'extract_sentences',
    'extract_ngrams',
    'clean_html_text',
    'has_question_pattern',
    'extract_statistics',
    'has_credentials',
]
