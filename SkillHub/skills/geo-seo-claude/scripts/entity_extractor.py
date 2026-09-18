#!/usr/bin/env python3
"""
SEO/GEO Entity Extractor

Extracts entities (people, organizations, places) from content for
Knowledge Graph optimization and E-E-A-T signals.

Usage:
    python entity_extractor.py <file_path>
    python entity_extractor.py --help

Requirements:
    Python 3.7+ (stdlib only)

Output:
    JSON with extracted entities and recommendations
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Set

# Import shared utilities and analyze_content functions
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))
from shared import PATTERNS
from keyword_analyzer import extract_text_content


# Common titles that indicate person entities (kept local - more specific to entity extraction)
PERSON_TITLES = {
    'dr', 'dr.', 'doctor', 'prof', 'prof.', 'professor',
    'md', 'm.d.', 'phd', 'ph.d.', 'mba', 'esq', 'jr', 'sr',
    'mr', 'mrs', 'ms', 'miss', 'dds', 'jd', 'mph', 'msc',
    'rev', 'father', 'sister', 'rabbi', 'imam'
}

# Note: For credential detection, use PATTERNS['credentials'] from shared

# Common organization types
ORG_TYPES = {
    'clinic', 'hospital', 'university', 'college', 'institute', 'foundation',
    'company', 'corporation', 'inc', 'llc', 'ltd', 'corp', 'co',
    'association', 'society', 'federation', 'council', 'committee',
    'department', 'school', 'center', 'centre', 'lab', 'laboratory',
    'group', 'agency', 'bureau', 'office', 'ministry'
}

# Common place indicators
PLACE_INDICATORS = {
    'street', 'st', 'avenue', 'ave', 'road', 'rd', 'boulevard', 'blvd',
    'drive', 'dr', 'lane', 'ln', 'way', 'court', 'ct', 'plaza', 'square',
    'city', 'town', 'village', 'county', 'state', 'province', 'country'
}


def extract_person_entities(text: str) -> List[Dict]:
    """Extract person names with titles and credentials"""
    persons = []
    seen = set()

    # Pattern: Title + Name (Dr. John Smith)
    title_pattern = r'\b(' + '|'.join(re.escape(t) for t in PERSON_TITLES) + r')\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\b'
    matches = re.finditer(title_pattern, text, re.IGNORECASE)

    for match in matches:
        title = match.group(1)
        name = match.group(2)
        full_name = f"{title} {name}"

        if full_name.lower() not in seen:
            seen.add(full_name.lower())

            # Check for credentials after name using shared pattern
            end_pos = match.end()
            following_text = text[end_pos:end_pos+50]
            credentials = PATTERNS['credentials'].findall(following_text)

            persons.append({
                'name': name,
                'title': title,
                'full_name': full_name,
                'credentials': credentials if credentials else None,
                'type': 'person',
                'context': 'titled_professional'
            })

    # Pattern: Capitalized Name (in quotes or after "by")
    author_pattern = r'(?:by|author[:\s]+|written by)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})'
    matches = re.finditer(author_pattern, text, re.IGNORECASE)

    for match in matches:
        name = match.group(1)
        if name.lower() not in seen:
            seen.add(name.lower())
            persons.append({
                'name': name,
                'full_name': name,
                'type': 'person',
                'context': 'author'
            })

    return persons


def extract_organization_entities(text: str) -> List[Dict]:
    """Extract organization names"""
    organizations = []
    seen = set()

    # Pattern: Capitalized Name + Organization Type
    org_pattern = r'\b([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){0,4})\s+(' + '|'.join(ORG_TYPES) + r')\b'
    matches = re.finditer(org_pattern, text, re.IGNORECASE)

    for match in matches:
        name_part = match.group(1)
        type_part = match.group(2)
        full_name = f"{name_part} {type_part}"

        if full_name.lower() not in seen and len(name_part.split()) >= 1:
            seen.add(full_name.lower())
            organizations.append({
                'name': full_name,
                'type': 'organization',
                'org_type': type_part.lower(),
                'context': 'named_organization'
            })

    # Pattern: Quoted organization names
    quoted_pattern = r'"([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){1,4})"'
    matches = re.finditer(quoted_pattern, text)

    for match in matches:
        name = match.group(1)
        if name.lower() not in seen and any(t in name.lower() for t in ORG_TYPES):
            seen.add(name.lower())
            organizations.append({
                'name': name,
                'type': 'organization',
                'context': 'quoted'
            })

    # Pattern: Organization with Inc, LLC, Corp
    corp_pattern = r'\b([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){0,3})\s+(Inc|LLC|Ltd|Corp|Co)\.?\b'
    matches = re.finditer(corp_pattern, text)

    for match in matches:
        name = match.group(1)
        suffix = match.group(2)
        full_name = f"{name} {suffix}"

        if full_name.lower() not in seen:
            seen.add(full_name.lower())
            organizations.append({
                'name': full_name,
                'type': 'organization',
                'org_type': 'business',
                'context': 'corporate'
            })

    return organizations


def extract_place_entities(text: str) -> List[Dict]:
    """Extract place names and addresses"""
    places = []
    seen = set()

    # Pattern: Street addresses
    address_pattern = r'\b(\d+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3}\s+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln))\b'
    matches = re.finditer(address_pattern, text, re.IGNORECASE)

    for match in matches:
        address = match.group(1)
        if address.lower() not in seen:
            seen.add(address.lower())
            places.append({
                'name': address,
                'type': 'place',
                'place_type': 'street_address',
                'context': 'address'
            })

    # Pattern: City, State
    city_state_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),\s+([A-Z]{2})\b'
    matches = re.finditer(city_state_pattern, text)

    for match in matches:
        city = match.group(1)
        state = match.group(2)
        full_name = f"{city}, {state}"

        if full_name.lower() not in seen:
            seen.add(full_name.lower())
            places.append({
                'name': full_name,
                'city': city,
                'state': state,
                'type': 'place',
                'place_type': 'city_state',
                'context': 'location'
            })

    # Pattern: ZIP codes (for address validation)
    zip_pattern = r'\b\d{5}(?:-\d{4})?\b'
    zip_codes = re.findall(zip_pattern, text)

    if zip_codes:
        for i, place in enumerate(places):
            if place.get('place_type') in ['street_address', 'city_state']:
                # Enhance with ZIP if found nearby
                places[i]['has_zip'] = True

    return places


def find_entity_relationships(persons: List[Dict], organizations: List[Dict]) -> List[Dict]:
    """Find relationships between persons and organizations"""
    relationships = []

    for person in persons:
        person_name = person.get('name', person.get('full_name', ''))

        for org in organizations:
            org_name = org.get('name', '')

            # Look for common relationship indicators
            relationship_types = []

            # Check if mentioned together (within 50 characters)
            # This is a simplified heuristic

            if person.get('context') == 'titled_professional':
                # Doctors, professors likely affiliated with clinics, universities
                if 'clinic' in org_name.lower() or 'hospital' in org_name.lower():
                    relationship_types.append('works_for')
                elif 'university' in org_name.lower() or 'college' in org_name.lower():
                    relationship_types.append('affiliated_with')

            if relationship_types:
                relationships.append({
                    'person': person_name,
                    'organization': org_name,
                    'relationships': relationship_types
                })

    return relationships


def generate_entity_schema(entities: Dict) -> Dict:
    """Generate schema markup recommendations for entities"""
    schemas = []

    # Organization schema
    if entities['organizations']:
        primary_org = entities['organizations'][0]
        schemas.append({
            'schema_type': 'Organization',
            'entity': primary_org['name'],
            'recommended_properties': [
                'name',
                'url',
                'logo',
                'description',
                'address' if any(p['type'] == 'place' for p in entities['places']) else None,
                'contactPoint',
                'sameAs'
            ]
        })

    # Person schema
    if entities['persons']:
        for person in entities['persons'][:3]:  # Top 3 persons
            properties = ['name', 'url', 'image', 'jobTitle', 'worksFor']

            if person.get('credentials'):
                properties.append('honorificSuffix')

            schemas.append({
                'schema_type': 'Person',
                'entity': person['name'],
                'recommended_properties': properties
            })

    return schemas


def extract_entities(file_path: str) -> Dict:
    """Main entity extraction function"""

    # Extract content
    content = extract_text_content(file_path)

    if content['word_count'] == 0:
        return {
            'error': 'No text content found in file',
            'file': file_path
        }

    # Extract all text
    full_text = ' '.join([
        content['title'],
        ' '.join(content['headings']),
        content['text']
    ])

    # Extract entities
    persons = extract_person_entities(full_text)
    organizations = extract_organization_entities(full_text)
    places = extract_place_entities(full_text)

    # Find relationships
    relationships = find_entity_relationships(persons, organizations)

    # Generate schema recommendations
    schema_recommendations = generate_entity_schema({
        'persons': persons,
        'organizations': organizations,
        'places': places
    })

    # Generate recommendations
    recommendations = []

    if len(persons) == 0:
        recommendations.append("Add author byline with full name and credentials (40% citation boost)")
    elif not any(p.get('credentials') for p in persons):
        recommendations.append("Add credentials to author name (MD, PhD, etc.) for 40% citation boost")
    else:
        recommendations.append(f"✅ Found {len(persons)} person entities with credentials")

    if len(organizations) == 0:
        recommendations.append("Add organization/institution affiliation for E-E-A-T")
    else:
        recommendations.append(f"✅ Found {len(organizations)} organization entities")

    if len(places) > 0:
        recommendations.append(f"✅ Found {len(places)} place entities (good for local SEO)")

    if len(relationships) > 0:
        recommendations.append(f"✅ Found {len(relationships)} entity relationships (implement in schema)")

    # Summary
    summary = {
        'total_persons': len(persons),
        'total_organizations': len(organizations),
        'total_places': len(places),
        'total_relationships': len(relationships),
        'persons_with_credentials': len([p for p in persons if p.get('credentials')]),
        'knowledge_graph_ready': len(persons) > 0 and len(organizations) > 0
    }

    return {
        'file': file_path,
        'summary': summary,
        'persons': persons,
        'organizations': organizations,
        'places': places,
        'relationships': relationships,
        'schema_recommendations': schema_recommendations,
        'recommendations': recommendations
    }


def main():
    """Main entry point"""

    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h']:
        print(__doc__)
        print("\nExamples:")
        print("  python entity_extractor.py ~/project/about.html")
        print("  python entity_extractor.py ~/blog/post.md")
        sys.exit(0 if len(sys.argv) >= 2 else 1)

    file_path = sys.argv[1]

    try:
        analysis = extract_entities(file_path)

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
