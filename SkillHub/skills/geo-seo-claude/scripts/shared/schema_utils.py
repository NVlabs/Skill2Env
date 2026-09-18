"""
Schema utilities for JSON-LD validation and detection.

Provides common functions for checking and extracting schema markup
across SEO/GEO/AEO optimizer scripts.
"""

from typing import Dict, List, Optional, Any, Union


def has_schema_type(schemas: List[Any], schema_type: str) -> bool:
    """
    Check if a specific schema type exists in JSON-LD array.

    Handles both single schemas and arrays of schemas, including
    nested @graph structures.

    Args:
        schemas: List of JSON-LD schema objects
        schema_type: The @type to search for (e.g., 'FAQPage', 'Article')

    Returns:
        True if schema type exists, False otherwise

    Examples:
        >>> schemas = [{'@type': 'FAQPage', 'mainEntity': [...]}]
        >>> has_schema_type(schemas, 'FAQPage')
        True

        >>> schemas = [{'@graph': [{'@type': 'Article'}]}]
        >>> has_schema_type(schemas, 'Article')
        True
    """
    if not schemas:
        return False

    for schema in schemas:
        if _check_schema_type(schema, schema_type):
            return True

    return False


def _check_schema_type(schema: Any, schema_type: str) -> bool:
    """Recursively check schema for type match."""
    if not isinstance(schema, (dict, list)):
        return False

    if isinstance(schema, list):
        return any(_check_schema_type(item, schema_type) for item in schema)

    # Direct type match
    if schema.get('@type') == schema_type:
        return True

    # Handle array @type (e.g., ["Article", "NewsArticle"])
    schema_types = schema.get('@type', [])
    if isinstance(schema_types, list) and schema_type in schema_types:
        return True

    # Check @graph structure
    if '@graph' in schema:
        return _check_schema_type(schema['@graph'], schema_type)

    return False


def get_schema_by_type(schemas: List[Any], schema_type: str) -> Optional[Dict]:
    """
    Get first schema matching the specified type.

    Args:
        schemas: List of JSON-LD schema objects
        schema_type: The @type to search for

    Returns:
        The matching schema dict, or None if not found

    Examples:
        >>> schemas = [{'@type': 'FAQPage', 'mainEntity': [...]}]
        >>> get_schema_by_type(schemas, 'FAQPage')
        {'@type': 'FAQPage', 'mainEntity': [...]}
    """
    if not schemas:
        return None

    for schema in schemas:
        result = _find_schema_by_type(schema, schema_type)
        if result:
            return result

    return None


def _find_schema_by_type(schema: Any, schema_type: str) -> Optional[Dict]:
    """Recursively find schema by type."""
    if not isinstance(schema, (dict, list)):
        return None

    if isinstance(schema, list):
        for item in schema:
            result = _find_schema_by_type(item, schema_type)
            if result:
                return result
        return None

    # Direct type match
    if schema.get('@type') == schema_type:
        return schema

    # Handle array @type
    schema_types = schema.get('@type', [])
    if isinstance(schema_types, list) and schema_type in schema_types:
        return schema

    # Check @graph structure
    if '@graph' in schema:
        return _find_schema_by_type(schema['@graph'], schema_type)

    return None


def get_all_schemas_by_type(schemas: List[Any], schema_type: str) -> List[Dict]:
    """
    Get all schemas matching the specified type.

    Args:
        schemas: List of JSON-LD schema objects
        schema_type: The @type to search for

    Returns:
        List of matching schema dicts
    """
    results = []

    for schema in schemas:
        _collect_schemas_by_type(schema, schema_type, results)

    return results


def _collect_schemas_by_type(schema: Any, schema_type: str, results: List[Dict]) -> None:
    """Recursively collect all schemas by type."""
    if not isinstance(schema, (dict, list)):
        return

    if isinstance(schema, list):
        for item in schema:
            _collect_schemas_by_type(item, schema_type, results)
        return

    # Direct type match
    if schema.get('@type') == schema_type:
        results.append(schema)

    # Handle array @type
    schema_types = schema.get('@type', [])
    if isinstance(schema_types, list) and schema_type in schema_types:
        if schema not in results:
            results.append(schema)

    # Check @graph structure
    if '@graph' in schema:
        _collect_schemas_by_type(schema['@graph'], schema_type, results)


def validate_schema_structure(schema: Dict) -> Dict[str, Any]:
    """
    Validate JSON-LD schema structure.

    Checks for required fields and common issues.

    Args:
        schema: JSON-LD schema object

    Returns:
        Dict with 'valid' bool, 'issues' list, and 'warnings' list

    Examples:
        >>> validate_schema_structure({'@type': 'Article'})
        {'valid': False, 'issues': ['Missing @context'], 'warnings': []}
    """
    issues = []
    warnings = []

    if not isinstance(schema, dict):
        return {
            'valid': False,
            'issues': ['Schema must be a dictionary'],
            'warnings': []
        }

    # Check @context
    if '@context' not in schema:
        issues.append('Missing @context (should be "https://schema.org")')

    # Check @type
    if '@type' not in schema:
        issues.append('Missing @type')

    # Validate @context value
    context = schema.get('@context')
    if context and context not in ['https://schema.org', 'http://schema.org']:
        warnings.append(f'Non-standard @context: {context}')

    # Type-specific validation
    schema_type = schema.get('@type')

    if schema_type == 'FAQPage':
        if 'mainEntity' not in schema:
            issues.append('FAQPage missing mainEntity (list of Questions)')
        elif isinstance(schema.get('mainEntity'), list):
            for i, q in enumerate(schema['mainEntity']):
                if not isinstance(q, dict):
                    continue
                if q.get('@type') != 'Question':
                    warnings.append(f'FAQ item {i+1}: Expected @type "Question"')
                if 'name' not in q:
                    warnings.append(f'FAQ item {i+1}: Missing question text (name)')
                if 'acceptedAnswer' not in q:
                    warnings.append(f'FAQ item {i+1}: Missing acceptedAnswer')

    elif schema_type == 'Article':
        required = ['headline', 'datePublished']
        for field in required:
            if field not in schema:
                issues.append(f'Article missing {field}')

        if 'author' not in schema:
            warnings.append('Article missing author (reduces E-E-A-T)')
        if 'dateModified' not in schema:
            warnings.append('Article missing dateModified (important for Perplexity)')

    elif schema_type == 'HowTo':
        if 'step' not in schema:
            issues.append('HowTo missing step array')
        if 'name' not in schema:
            issues.append('HowTo missing name')

    elif schema_type in ['Organization', 'LocalBusiness', 'MedicalBusiness']:
        if 'name' not in schema:
            issues.append(f'{schema_type} missing name')
        if 'url' not in schema:
            warnings.append(f'{schema_type} missing url')

    elif schema_type == 'Person':
        if 'name' not in schema:
            issues.append('Person missing name')

    return {
        'valid': len(issues) == 0,
        'issues': issues,
        'warnings': warnings
    }


def extract_author_credentials(schema: Dict) -> Optional[str]:
    """
    Extract author credentials from Article schema.

    Args:
        schema: Article schema dict

    Returns:
        Credentials string (e.g., "MD, PhD") or None
    """
    author = schema.get('author')
    if not author:
        return None

    if isinstance(author, dict):
        return author.get('honorificSuffix')

    if isinstance(author, list) and author:
        first_author = author[0]
        if isinstance(first_author, dict):
            return first_author.get('honorificSuffix')

    return None


def has_speakable_schema(schemas: List[Any]) -> bool:
    """
    Check if any schema contains speakable specification.

    Args:
        schemas: List of JSON-LD schema objects

    Returns:
        True if speakable found, False otherwise
    """
    for schema in schemas:
        if _has_speakable(schema):
            return True
    return False


def _has_speakable(schema: Any) -> bool:
    """Recursively check for speakable property."""
    if not isinstance(schema, (dict, list)):
        return False

    if isinstance(schema, list):
        return any(_has_speakable(item) for item in schema)

    if 'speakable' in schema:
        return True

    if '@graph' in schema:
        return _has_speakable(schema['@graph'])

    return False
