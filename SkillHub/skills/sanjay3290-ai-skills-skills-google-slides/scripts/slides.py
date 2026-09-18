#!/usr/bin/env python3
"""
Google Slides API operations.
Lightweight alternative to the full Google Workspace MCP server.
"""

import argparse
import json
import re
import sys
import urllib.request
import urllib.error
import urllib.parse
from typing import Optional

from auth import get_valid_access_token

SLIDES_API_BASE = "https://slides.googleapis.com/v1"
DRIVE_API_BASE = "https://www.googleapis.com/drive/v3"


def extract_presentation_id(presentation_id_or_url: str) -> str:
    """Extract presentation ID from URL or return as-is if already an ID."""
    # Match Google Slides URL patterns
    patterns = [
        r'docs\.google\.com/presentation/d/([a-zA-Z0-9_-]+)',
        r'drive\.google\.com/.*?/d/([a-zA-Z0-9_-]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, presentation_id_or_url)
        if match:
            return match.group(1)
    return presentation_id_or_url


def api_request(method: str, url: str, data: Optional[dict] = None, params: Optional[dict] = None) -> dict:
    """Make an authenticated request to a Google API."""
    token = get_valid_access_token()
    if not token:
        return {"error": "Failed to get access token"}

    if params:
        url += "?" + urllib.parse.urlencode(params)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    body = json.dumps(data).encode('utf-8') if data else None

    try:
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else str(e)
        return {"error": f"HTTP {e.code}: {error_body}"}
    except urllib.error.URLError as e:
        return {"error": f"Request failed: {e.reason}"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response"}


def extract_text_from_text_content(text_content: dict) -> str:
    """Extract plain text from a Slides text content object."""
    text = ''
    text_elements = text_content.get('textElements', [])
    for element in text_elements:
        if 'textRun' in element and element['textRun'].get('content'):
            text += element['textRun']['content']
        elif 'paragraphMarker' in element:
            text += '\n'
    return text


def get_text(presentation_id: str) -> dict:
    """Get all text content from a presentation."""
    pid = extract_presentation_id(presentation_id)

    params = {
        "fields": "title,slides(pageElements(shape(text,shapeProperties),table(tableRows(tableCells(text)))))"
    }

    result = api_request("GET", f"{SLIDES_API_BASE}/presentations/{pid}", params=params)

    if "error" in result:
        return result

    content = ''

    # Add presentation title
    if result.get('title'):
        content += f"Presentation Title: {result['title']}\n\n"

    # Process each slide
    slides = result.get('slides', [])
    for slide_index, slide in enumerate(slides):
        content += f"\n--- Slide {slide_index + 1} ---\n"

        page_elements = slide.get('pageElements', [])
        for element in page_elements:
            # Extract text from shapes
            if 'shape' in element and 'text' in element['shape']:
                shape_text = extract_text_from_text_content(element['shape']['text'])
                if shape_text.strip():
                    content += shape_text + '\n'

            # Extract text from tables
            if 'table' in element and 'tableRows' in element['table']:
                content += '\n--- Table Data ---\n'
                for row in element['table']['tableRows']:
                    row_text = []
                    for cell in row.get('tableCells', []):
                        if 'text' in cell:
                            cell_text = extract_text_from_text_content(cell['text'])
                            row_text.append(cell_text.strip())
                        else:
                            row_text.append('')
                    content += ' | '.join(row_text) + '\n'
                content += '--- End Table Data ---\n'

        content += '\n'

    return {"text": content.strip()}


def find_presentations(query: str, page_size: int = 10, page_token: Optional[str] = None) -> dict:
    """Find presentations by search query using Drive API."""
    # Build Drive search query for presentations
    mime_type = "application/vnd.google-apps.presentation"
    drive_query = f"mimeType='{mime_type}' and trashed=false"

    if query:
        # Escape single quotes in query
        escaped_query = query.replace("'", "\\'")
        drive_query += f" and (name contains '{escaped_query}' or fullText contains '{escaped_query}')"

    params = {
        "pageSize": page_size,
        "fields": "nextPageToken,files(id,name,modifiedTime,owners)",
        "q": drive_query
    }

    if page_token:
        params["pageToken"] = page_token

    result = api_request("GET", f"{DRIVE_API_BASE}/files", params=params)

    if "error" in result:
        return result

    return {
        "presentations": result.get("files", []),
        "nextPageToken": result.get("nextPageToken")
    }


def get_metadata(presentation_id: str) -> dict:
    """Get presentation metadata."""
    pid = extract_presentation_id(presentation_id)

    params = {
        "fields": "presentationId,title,slides(objectId),pageSize,notesMaster,masters,layouts"
    }

    result = api_request("GET", f"{SLIDES_API_BASE}/presentations/{pid}", params=params)

    if "error" in result:
        return result

    metadata = {
        "presentationId": result.get("presentationId"),
        "title": result.get("title"),
        "slideCount": len(result.get("slides", [])),
        "pageSize": result.get("pageSize"),
        "hasMasters": bool(result.get("masters")),
        "hasLayouts": bool(result.get("layouts")),
        "hasNotesMaster": bool(result.get("notesMaster"))
    }

    return metadata


def create_presentation(title: str) -> dict:
    """Create a new empty presentation."""
    data = {"title": title}
    return api_request("POST", f"{SLIDES_API_BASE}/presentations", data=data)


def add_slide(presentation_id: str, layout: str = "BLANK", insert_at: Optional[int] = None) -> dict:
    """
    Add a new slide to a presentation.

    Args:
        presentation_id: Presentation ID or URL
        layout: Predefined layout - BLANK, TITLE, TITLE_AND_BODY, TITLE_AND_TWO_COLUMNS,
                TITLE_ONLY, SECTION_HEADER, SECTION_TITLE_AND_DESCRIPTION, ONE_COLUMN_TEXT,
                MAIN_POINT, BIG_NUMBER
        insert_at: 0-based index to insert slide at (appends if not specified)
    """
    pid = extract_presentation_id(presentation_id)

    request = {
        "createSlide": {
            "slideLayoutReference": {
                "predefinedLayout": layout
            }
        }
    }

    if insert_at is not None:
        request["createSlide"]["insertionIndex"] = insert_at

    return api_request("POST", f"{SLIDES_API_BASE}/presentations/{pid}:batchUpdate",
                       data={"requests": [request]})


def replace_text(presentation_id: str, find_text: str, replace_with: str, match_case: bool = False) -> dict:
    """
    Find and replace text across all slides.

    Args:
        presentation_id: Presentation ID or URL
        find_text: Text to search for
        replace_with: Replacement text
        match_case: Whether the search is case-sensitive
    """
    pid = extract_presentation_id(presentation_id)

    request = {
        "replaceAllText": {
            "containsText": {
                "text": find_text,
                "matchCase": match_case
            },
            "replaceText": replace_with
        }
    }

    return api_request("POST", f"{SLIDES_API_BASE}/presentations/{pid}:batchUpdate",
                       data={"requests": [request]})


def delete_slide(presentation_id: str, slide_object_id: str) -> dict:
    """
    Delete a slide by its object ID.

    Use get-metadata to find slide object IDs.
    """
    pid = extract_presentation_id(presentation_id)

    request = {
        "deleteObject": {
            "objectId": slide_object_id
        }
    }

    return api_request("POST", f"{SLIDES_API_BASE}/presentations/{pid}:batchUpdate",
                       data={"requests": [request]})


def batch_update(presentation_id: str, requests: list) -> dict:
    """
    Execute batch update requests for advanced operations.

    Args:
        presentation_id: Presentation ID or URL
        requests: List of request objects (see Google Slides API batchUpdate docs)
    """
    pid = extract_presentation_id(presentation_id)
    return api_request("POST", f"{SLIDES_API_BASE}/presentations/{pid}:batchUpdate",
                       data={"requests": requests})


def main():
    parser = argparse.ArgumentParser(description="Google Slides API operations")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # get-text
    get_text_parser = subparsers.add_parser("get-text", help="Get text content from a presentation")
    get_text_parser.add_argument("presentation", help="Presentation ID or URL")

    # find
    find_parser = subparsers.add_parser("find", help="Find presentations by search query")
    find_parser.add_argument("query", help="Search query")
    find_parser.add_argument("--limit", type=int, default=10, help="Max results to return")
    find_parser.add_argument("--page-token", help="Pagination token")

    # get-metadata
    get_metadata_parser = subparsers.add_parser("get-metadata", help="Get presentation metadata")
    get_metadata_parser.add_argument("presentation", help="Presentation ID or URL")

    # create
    create_parser = subparsers.add_parser("create", help="Create a new presentation")
    create_parser.add_argument("title", help="Presentation title")

    # add-slide
    add_slide_parser = subparsers.add_parser("add-slide", help="Add a slide to a presentation")
    add_slide_parser.add_argument("presentation", help="Presentation ID or URL")
    add_slide_parser.add_argument("--layout", default="BLANK",
                                  help="Slide layout (BLANK, TITLE, TITLE_AND_BODY, TITLE_ONLY, SECTION_HEADER, etc.)")
    add_slide_parser.add_argument("--at", type=int, default=None, help="Insert position (0-based index)")

    # replace-text
    replace_text_parser = subparsers.add_parser("replace-text", help="Find and replace text across all slides")
    replace_text_parser.add_argument("presentation", help="Presentation ID or URL")
    replace_text_parser.add_argument("find", help="Text to find")
    replace_text_parser.add_argument("replace", help="Replacement text")
    replace_text_parser.add_argument("--match-case", action="store_true", help="Case-sensitive search")

    # delete-slide
    delete_slide_parser = subparsers.add_parser("delete-slide", help="Delete a slide by object ID")
    delete_slide_parser.add_argument("presentation", help="Presentation ID or URL")
    delete_slide_parser.add_argument("slide_id", help="Slide object ID (from get-metadata)")

    # batch-update
    batch_parser = subparsers.add_parser("batch-update", help="Execute batch update requests")
    batch_parser.add_argument("presentation", help="Presentation ID or URL")
    batch_parser.add_argument("requests", help="JSON array of batch update request objects")

    args = parser.parse_args()

    if args.command == "get-text":
        result = get_text(args.presentation)
    elif args.command == "find":
        result = find_presentations(args.query, args.limit, args.page_token)
    elif args.command == "get-metadata":
        result = get_metadata(args.presentation)
    elif args.command == "create":
        result = create_presentation(args.title)
    elif args.command == "add-slide":
        result = add_slide(args.presentation, args.layout, args.at)
    elif args.command == "replace-text":
        result = replace_text(args.presentation, args.find, args.replace, args.match_case)
    elif args.command == "delete-slide":
        result = delete_slide(args.presentation, args.slide_id)
    elif args.command == "batch-update":
        requests_data = json.loads(args.requests)
        result = batch_update(args.presentation, requests_data)
    else:
        result = {"error": f"Unknown command: {args.command}"}

    print(json.dumps(result, indent=2))

    if isinstance(result, dict) and "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()
