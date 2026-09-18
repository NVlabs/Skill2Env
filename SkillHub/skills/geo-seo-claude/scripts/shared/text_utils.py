"""
Text processing utilities for SEO/GEO/AEO Optimizer.

Provides common functions for word counting, tokenization,
sentence extraction, and HTML text cleaning.
"""

import re
from typing import List, Tuple
from .config import PATTERNS, STOP_WORDS


def count_words(text: str) -> int:
    """
    Count words in text.

    Uses word boundary regex for accurate counting.

    Args:
        text: Text to count words in

    Returns:
        Number of words

    Examples:
        >>> count_words("Hello world!")
        2
        >>> count_words("This is a test sentence.")
        5
    """
    if not text:
        return 0
    return len(PATTERNS['word'].findall(text))


def tokenize(text: str, remove_stop_words: bool = True, min_length: int = 3) -> List[str]:
    """
    Tokenize text into words.

    Converts to lowercase, removes punctuation, optionally removes stop words.

    Args:
        text: Text to tokenize
        remove_stop_words: Whether to remove common stop words
        min_length: Minimum word length to include

    Returns:
        List of word tokens

    Examples:
        >>> tokenize("The quick brown fox")
        ['quick', 'brown', 'fox']
        >>> tokenize("Hello world!", remove_stop_words=False)
        ['hello', 'world']
    """
    if not text:
        return []

    # Convert to lowercase
    text = text.lower()

    # Remove punctuation except hyphens in words
    text = re.sub(r'[^\w\s-]', ' ', text)

    # Split into words
    words = text.split()

    # Filter
    result = []
    for word in words:
        if len(word) < min_length:
            continue
        if remove_stop_words and word in STOP_WORDS:
            continue
        result.append(word)

    return result


def extract_sentences(text: str) -> List[str]:
    """
    Split text into sentences.

    Uses sentence-ending punctuation (.!?) for splitting.

    Args:
        text: Text to split

    Returns:
        List of sentence strings

    Examples:
        >>> extract_sentences("Hello. World!")
        ['Hello', 'World!']
    """
    if not text:
        return []

    sentences = PATTERNS['sentence_end'].split(text)
    return [s.strip() for s in sentences if s.strip()]


def clean_html_text(html: str) -> str:
    """
    Extract clean text from HTML content.

    Removes script, style, and all HTML tags.

    Args:
        html: HTML content string

    Returns:
        Clean text without HTML markup

    Examples:
        >>> clean_html_text("<p>Hello <b>world</b>!</p>")
        'Hello world!'
    """
    if not html:
        return ""

    # Remove script tags
    text = PATTERNS['script_tags'].sub('', html)

    # Remove style tags
    text = PATTERNS['style_tags'].sub('', text)

    # Remove all HTML tags
    text = PATTERNS['html_tags'].sub(' ', text)

    # Normalize whitespace
    text = PATTERNS['whitespace'].sub(' ', text).strip()

    return text


def extract_ngrams(words: List[str], n: int) -> List[str]:
    """
    Extract n-grams from word list.

    Args:
        words: List of word tokens
        n: N-gram size (2 for bigrams, 3 for trigrams, etc.)

    Returns:
        List of n-gram strings

    Examples:
        >>> extract_ngrams(['quick', 'brown', 'fox'], 2)
        ['quick brown', 'brown fox']
    """
    if len(words) < n:
        return []

    ngrams = []
    for i in range(len(words) - n + 1):
        ngram = ' '.join(words[i:i+n])
        ngrams.append(ngram)

    return ngrams


def extract_first_n_words(text: str, n: int) -> str:
    """
    Extract first N words from text.

    Args:
        text: Source text
        n: Number of words to extract

    Returns:
        String with first N words

    Examples:
        >>> extract_first_n_words("The quick brown fox jumps", 3)
        'The quick brown'
    """
    if not text:
        return ""

    words = text.split()
    return ' '.join(words[:n])


def estimate_reading_time(text: str, wpm: int = 200) -> Tuple[int, int]:
    """
    Estimate reading time for text.

    Args:
        text: Text to estimate
        wpm: Words per minute (default 200, average adult)

    Returns:
        Tuple of (minutes, seconds)

    Examples:
        >>> estimate_reading_time("..." * 400)  # 400 words
        (2, 0)
    """
    words = count_words(text)
    total_seconds = int((words / wpm) * 60)
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return (minutes, seconds)


def estimate_speaking_time(text: str, wpm: int = 150) -> Tuple[int, int]:
    """
    Estimate speaking time for text.

    Args:
        text: Text to estimate
        wpm: Words per minute (default 150, average speaking rate)

    Returns:
        Tuple of (minutes, seconds)

    Examples:
        >>> estimate_speaking_time("..." * 150)  # 150 words
        (1, 0)
    """
    words = count_words(text)
    total_seconds = int((words / wpm) * 60)
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return (minutes, seconds)


def has_question_pattern(text: str) -> bool:
    """
    Check if text contains question patterns.

    Detects question words (what, how, why, etc.) and question marks.

    Args:
        text: Text to check

    Returns:
        True if question pattern found
    """
    question_words = ['what', 'how', 'why', 'when', 'where', 'who', 'which', 'can', 'does', 'is', 'are']

    text_lower = text.lower()
    first_word = text_lower.split()[0] if text_lower.split() else ''

    return first_word in question_words or '?' in text


def extract_statistics(text: str) -> List[dict]:
    """
    Extract statistics and numbers from text.

    Finds patterns like "95%", "10,000 users", "5 years".

    Args:
        text: Text to analyze

    Returns:
        List of dicts with 'value' and 'context' keys
    """
    statistics = []
    matches = PATTERNS['statistics'].finditer(text)

    for match in matches:
        start = max(0, match.start() - 50)
        end = min(len(text), match.end() + 50)
        context = text[start:end].strip()

        statistics.append({
            'value': match.group(0),
            'context': context
        })

    return statistics


def has_credentials(text: str) -> bool:
    """
    Check if text contains professional credentials.

    Detects patterns like MD, PhD, MBA, etc.

    Args:
        text: Text to check

    Returns:
        True if credentials found
    """
    return bool(PATTERNS['credentials'].search(text))


def extract_credentials(text: str) -> List[str]:
    """
    Extract all credentials from text.

    Args:
        text: Text to search

    Returns:
        List of credential strings found
    """
    return PATTERNS['credentials'].findall(text)
