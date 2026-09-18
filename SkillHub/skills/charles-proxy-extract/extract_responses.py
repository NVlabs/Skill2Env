#!/usr/bin/env python3
"""
Charles Proxy Response Extractor

Usage:
    python extract_responses.py <file.chlsj> <path_pattern> [options]

Examples:
    # Extract all /today responses
    python extract_responses.py file.chlsj "/today"

    # Extract all /items responses
    python extract_responses.py file.chlsj "/items"

    # Filter by HTTP method (shows request body for POST/PUT/PATCH)
    python extract_responses.py file.chlsj "/logs" --method POST

    # Extract and save to file
    python extract_responses.py file.chlsj "/logs-by-day" --output logs_responses.json

    # Pretty print first response only
    python extract_responses.py file.chlsj "/users" --first-only

    # Show summary only (no response bodies)
    python extract_responses.py file.chlsj "/today" --summary-only
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional


def load_charles_session(file_path: str) -> List[Dict[str, Any]]:
    """Load Charles session file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"❌ Error: File not found: {file_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in file: {e}")
        sys.exit(1)


def filter_requests(requests: List[Dict], path_pattern: str, method_filter: Optional[str] = None) -> List[Dict]:
    """Filter requests by path pattern (contains) and optionally by HTTP method."""
    filtered = [req for req in requests if path_pattern in req.get('path', '')]

    if method_filter:
        method_upper = method_filter.upper()
        filtered = [req for req in filtered if req.get('method', '').upper() == method_upper]

    return filtered


def extract_response_body(request: Dict) -> Any:
    """Extract and parse response body."""
    response = request.get('response', {})
    body = response.get('body', {})
    text = body.get('text', '')

    if not text:
        return None

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text  # Return raw text if not JSON


def extract_request_body(request: Dict) -> Any:
    """Extract and parse request body."""
    req = request.get('request', {})
    body = req.get('body', {})
    text = body.get('text', '')

    if not text:
        return None

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text  # Return raw text if not JSON


def print_summary(requests: List[Dict], path_pattern: str):
    """Print summary of filtered requests."""
    print(f"\n{'='*80}")
    print("CHARLES SESSION ANALYSIS")
    print(f"{'='*80}")
    print(f"Pattern: '{path_pattern}'")
    print(f"Matching requests: {len(requests)}")
    print(f"{'='*80}\n")

    if not requests:
        print("❌ No matching requests found.")
        return

    # Group by path
    path_counts = {}
    for req in requests:
        path = req.get('path', 'unknown')
        path_counts[path] = path_counts.get(path, 0) + 1

    print("📊 Paths found:")
    for path, count in sorted(path_counts.items()):
        print(f"  {path} ({count} request{'s' if count > 1 else ''})")
    print()


def print_request_details(request: Dict, index: int, total: int, show_request_body: bool = False):
    """Print detailed information about a single request."""
    path = request.get('path', 'unknown')
    method = request.get('method', 'GET')
    status = request.get('response', {}).get('status', 'N/A')

    # Get timing info
    times = request.get('times', {})
    start_time = times.get('start', 'N/A')

    print(f"\n{'─'*80}")
    print(f"REQUEST {index + 1}/{total}")
    print(f"{'─'*80}")
    print(f"Method:    {method}")
    print(f"Path:      {path}")
    print(f"Status:    {status}")
    print(f"Time:      {start_time}")
    print(f"{'─'*80}")

    # Show request body for mutation operations
    if show_request_body and method.upper() in ['POST', 'PUT', 'PATCH']:
        request_body = extract_request_body(request)
        if request_body:
            print("\nRequest Body:")
            if isinstance(request_body, str):
                print(request_body[:500])
                if len(request_body) > 500:
                    print(f"... ({len(request_body) - 500} more characters)")
            else:
                print(json.dumps(request_body, indent=2))
            print(f"{'─'*80}")


def print_response_body(body: Any, pretty: bool = True):
    """Print response body."""
    if body is None:
        print("⚠️  No response body")
        return

    if isinstance(body, str):
        print("\nResponse (text):")
        print(body[:500])  # Limit text responses
        if len(body) > 500:
            print(f"... ({len(body) - 500} more characters)")
    else:
        print("\nResponse (JSON):")
        if pretty:
            print(json.dumps(body, indent=2))
        else:
            print(json.dumps(body))


def save_responses(requests: List[Dict], output_file: str, path_pattern: str):
    """Save all responses to a file."""
    results = {
        'pattern': path_pattern,
        'total_requests': len(requests),
        'extracted_at': datetime.now().isoformat(),
        'requests': []
    }

    for req in requests:
        body = extract_response_body(req)
        results['requests'].append({
            'path': req.get('path'),
            'method': req.get('method'),
            'status': req.get('response', {}).get('status'),
            'response': body
        })

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"✅ Saved {len(requests)} responses to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description='Extract responses from Charles Proxy session files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument('file', help='Charles session file (.chlsj)')
    parser.add_argument('pattern', help='Path pattern to match (contains)')
    parser.add_argument('-o', '--output', help='Output file to save responses')
    parser.add_argument('-m', '--method', help='Filter by HTTP method (GET, POST, PUT, PATCH, DELETE)')
    parser.add_argument('-f', '--first-only', action='store_true',
                       help='Show only the first matching request')
    parser.add_argument('-s', '--summary-only', action='store_true',
                       help='Show summary only, no response bodies')
    parser.add_argument('--no-pretty', action='store_true',
                       help='Disable pretty printing of JSON')

    args = parser.parse_args()

    # Load and filter requests
    all_requests = load_charles_session(args.file)
    filtered_requests = filter_requests(all_requests, args.pattern, args.method)

    # Determine if we should show request bodies (for POST/PUT/PATCH)
    show_request_body = args.method and args.method.upper() in ['POST', 'PUT', 'PATCH']

    # Print summary
    print_summary(filtered_requests, args.pattern)

    if not filtered_requests:
        sys.exit(1)

    # Save to file if requested
    if args.output:
        save_responses(filtered_requests, args.output, args.pattern)
        if args.summary_only:
            return

    # Print responses
    if not args.summary_only:
        requests_to_show = [filtered_requests[0]] if args.first_only else filtered_requests

        for i, req in enumerate(requests_to_show):
            print_request_details(req, i, len(requests_to_show), show_request_body=show_request_body)
            body = extract_response_body(req)
            print_response_body(body, pretty=not args.no_pretty)

        if args.first_only and len(filtered_requests) > 1:
            print(f"\n💡 Showing 1 of {len(filtered_requests)} matching requests.")
            print("   Remove --first-only to see all responses.")


if __name__ == '__main__':
    main()
