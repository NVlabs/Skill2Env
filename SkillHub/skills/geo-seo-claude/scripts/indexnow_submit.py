#!/usr/bin/env python3
"""
IndexNow URL Submission Tool

Submit URLs to search engines instantly via the IndexNow protocol.
Supports the current IndexNow participants: Bing, Yandex, Seznam,
Naver, Yep, Internet Archive, and Amazon Bot.

No API key registration required - just generate a key and host it.

Usage:
    python indexnow_submit.py <url> [--key KEY]
    python indexnow_submit.py --batch <file> [--key KEY]
    python indexnow_submit.py --generate-key
    python indexnow_submit.py --help

Requirements:
    Python 3.7+ (stdlib only)

Output:
    JSON with submission status for each search engine
"""

import json
import sys
import secrets
import string
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse, urljoin, quote
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# Import shared configuration
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))
from shared import INDEXNOW

# Use shared config for endpoints and settings
INDEXNOW_ENDPOINTS = INDEXNOW['endpoints']
DEFAULT_KEY_LENGTH = INDEXNOW['key_length']


def generate_key(length: int = DEFAULT_KEY_LENGTH) -> str:
    """
    Generate a random IndexNow key.

    Key requirements:
    - Minimum 8 characters
    - Only lowercase a-z and digits 0-9
    - Must be unique to your site
    """
    alphabet = string.ascii_lowercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def validate_url(url: str) -> bool:
    """Validate URL format"""
    try:
        result = urlparse(url)
        return all([result.scheme in ('http', 'https'), result.netloc])
    except Exception:
        return False


def extract_host(url: str) -> str:
    """Extract host from URL"""
    parsed = urlparse(url)
    return parsed.netloc


def submit_single_url(
    url: str,
    key: str,
    endpoint: str = 'bing',
    timeout: int = None
) -> Dict:
    """
    Submit a single URL to IndexNow.

    Args:
        url: The URL to submit
        key: Your IndexNow key
        endpoint: Which search engine to submit to
        timeout: Request timeout in seconds

    Returns:
        Dict with status and response info
    """
    if timeout is None:
        timeout = INDEXNOW['timeout']['single']

    if endpoint not in INDEXNOW_ENDPOINTS:
        return {
            'success': False,
            'error': f'Unknown endpoint: {endpoint}',
            'endpoint': endpoint
        }

    host = extract_host(url)

    # Build IndexNow URL
    # Format: https://www.bing.com/indexnow?url=URL&key=KEY
    # Percent-encode the URL so query, fragment, and reserved characters
    # in the target URL don't corrupt the IndexNow request.
    indexnow_url = f"{INDEXNOW_ENDPOINTS[endpoint]}?url={quote(url, safe='')}&key={key}"

    try:
        request = Request(
            indexnow_url,
            headers={
                'User-Agent': 'SEO-GEO-Optimizer/1.0 (IndexNow)',
                'Accept': 'application/json'
            }
        )

        with urlopen(request, timeout=timeout) as response:
            status_code = response.getcode()

            return {
                'success': status_code in (200, 202),
                'status_code': status_code,
                'endpoint': endpoint,
                'url': url,
                'message': get_status_message(status_code)
            }

    except HTTPError as e:
        return {
            'success': False,
            'status_code': e.code,
            'endpoint': endpoint,
            'url': url,
            'error': get_status_message(e.code)
        }
    except URLError as e:
        return {
            'success': False,
            'endpoint': endpoint,
            'url': url,
            'error': str(e.reason)
        }
    except Exception as e:
        return {
            'success': False,
            'endpoint': endpoint,
            'url': url,
            'error': str(e)
        }


def submit_batch_urls(
    urls: List[str],
    key: str,
    host: str,
    endpoint: str = 'bing',
    timeout: int = None
) -> Dict:
    """
    Submit multiple URLs via IndexNow batch API.

    Batch API is more efficient for >1 URL (max 10,000 per request).

    Args:
        urls: List of URLs to submit (must be same host)
        key: Your IndexNow key
        host: The host for all URLs
        endpoint: Which search engine to submit to
        timeout: Request timeout in seconds

    Returns:
        Dict with batch submission status
    """
    if timeout is None:
        timeout = INDEXNOW['timeout']['batch']

    if endpoint not in INDEXNOW_ENDPOINTS:
        return {
            'success': False,
            'error': f'Unknown endpoint: {endpoint}'
        }

    if len(urls) > 10000:
        return {
            'success': False,
            'error': 'Maximum 10,000 URLs per batch request'
        }

    # Build batch request body
    payload = {
        'host': host,
        'key': key,
        'urlList': urls
    }

    batch_url = INDEXNOW_ENDPOINTS[endpoint]

    try:
        data = json.dumps(payload).encode('utf-8')
        request = Request(
            batch_url,
            data=data,
            headers={
                'Content-Type': 'application/json; charset=utf-8',
                'User-Agent': 'SEO-GEO-Optimizer/1.0 (IndexNow)',
                'Accept': 'application/json'
            },
            method='POST'
        )

        with urlopen(request, timeout=timeout) as response:
            status_code = response.getcode()

            return {
                'success': status_code in (200, 202),
                'status_code': status_code,
                'endpoint': endpoint,
                'urls_submitted': len(urls),
                'message': get_status_message(status_code)
            }

    except HTTPError as e:
        return {
            'success': False,
            'status_code': e.code,
            'endpoint': endpoint,
            'urls_submitted': 0,
            'error': get_status_message(e.code)
        }
    except URLError as e:
        return {
            'success': False,
            'endpoint': endpoint,
            'urls_submitted': 0,
            'error': str(e.reason)
        }
    except Exception as e:
        return {
            'success': False,
            'endpoint': endpoint,
            'urls_submitted': 0,
            'error': str(e)
        }


def get_status_message(status_code: int) -> str:
    """Get human-readable message for IndexNow status codes"""
    messages = {
        200: 'URL submitted successfully',
        202: 'URL accepted for processing',
        400: 'Invalid request (check URL format)',
        403: 'Key not valid or not found at expected location',
        422: 'URLs do not belong to the host',
        429: 'Too many requests (rate limited)',
        500: 'IndexNow server error'
    }
    return messages.get(status_code, f'Unknown status: {status_code}')


def submit_to_all_engines(
    urls: List[str],
    key: str,
    host: Optional[str] = None
) -> Dict:
    """
    Submit URLs to all IndexNow partner search engines.

    Note: IndexNow partners share submissions, so submitting to one
    is usually sufficient. This submits to all for redundancy.

    Args:
        urls: List of URLs to submit
        key: Your IndexNow key
        host: Host for batch requests (auto-detected if single URL)

    Returns:
        Dict with results from each endpoint
    """
    results = {
        'urls': urls,
        'total_urls': len(urls),
        'endpoints': {}
    }

    # Auto-detect host from first URL
    if not host and urls:
        host = extract_host(urls[0])

    # Single URL uses GET, multiple uses POST batch
    if len(urls) == 1:
        for endpoint in INDEXNOW_ENDPOINTS:
            results['endpoints'][endpoint] = submit_single_url(
                urls[0], key, endpoint
            )
    else:
        for endpoint in INDEXNOW_ENDPOINTS:
            results['endpoints'][endpoint] = submit_batch_urls(
                urls, key, host, endpoint
            )

    # Summary
    successful = sum(
        1 for r in results['endpoints'].values() if r.get('success')
    )
    results['summary'] = {
        'successful_endpoints': successful,
        'total_endpoints': len(INDEXNOW_ENDPOINTS),
        'all_successful': successful == len(INDEXNOW_ENDPOINTS)
    }

    return results


def generate_key_file(key: str, output_dir: str = '.') -> Dict:
    """
    Generate the key verification file.

    IndexNow requires a text file at /{key}.txt containing the key.
    Host this file at your site root.

    Args:
        key: Your IndexNow key
        output_dir: Directory to save the key file

    Returns:
        Dict with file path and hosting instructions
    """
    output_path = Path(output_dir) / f'{key}.txt'

    with open(output_path, 'w') as f:
        f.write(key)

    return {
        'key': key,
        'file_path': str(output_path),
        'file_name': f'{key}.txt',
        'instructions': [
            f'1. Upload {key}.txt to your website root',
            f'2. Verify it\'s accessible at https://yoursite.com/{key}.txt',
            '3. The file must contain only the key (no extra characters)',
            '4. Keep the file hosted permanently for ongoing submissions'
        ],
        'example_url': f'https://example.com/{key}.txt'
    }


def load_urls_from_file(file_path: str) -> List[str]:
    """Load URLs from a text file (one URL per line)"""
    urls = []
    with open(file_path, 'r') as f:
        for line in f:
            url = line.strip()
            if url and not url.startswith('#') and validate_url(url):
                urls.append(url)
    return urls


def main():
    """Main entry point"""

    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h']:
        print(__doc__)
        print("\nExamples:")
        print("  # Generate a new key")
        print("  python indexnow_submit.py --generate-key")
        print("")
        print("  # Submit a single URL")
        print("  python indexnow_submit.py https://example.com/new-page --key abc123")
        print("")
        print("  # Submit multiple URLs from file")
        print("  python indexnow_submit.py --batch urls.txt --key abc123")
        print("")
        print("  # Generate key file for hosting")
        print("  python indexnow_submit.py --generate-key --output ./public")
        print("")
        print("Options:")
        print("  --key KEY       Your IndexNow key")
        print("  --batch FILE    File with URLs (one per line)")
        print("  --generate-key  Generate a new random key")
        print("  --output DIR    Output directory for key file")
        print("  --endpoint EP   Submit to specific endpoint (bing, yandex, seznam, naver)")
        print("")
        print("Notes:")
        print("  - IndexNow partners share submissions (one submission reaches all)")
        print("  - You must host /{key}.txt at your site root")
        print("  - Maximum 10,000 URLs per batch request")
        print("  - GEO benefit: Bing index feeds AI platforms (ChatGPT, Perplexity)")
        sys.exit(0 if '--help' in sys.argv else 1)

    # Parse arguments
    args = sys.argv[1:]

    # Generate key mode
    if '--generate-key' in args:
        key = generate_key()
        output_dir = '.'

        if '--output' in args:
            idx = args.index('--output')
            if idx + 1 < len(args):
                output_dir = args[idx + 1]

        result = generate_key_file(key, output_dir)
        print(json.dumps(result, indent=2))
        sys.exit(0)

    # Get key
    key = None
    if '--key' in args:
        idx = args.index('--key')
        if idx + 1 < len(args):
            key = args[idx + 1]

    if not key:
        print(json.dumps({
            'error': 'IndexNow key required. Use --key KEY or --generate-key'
        }, indent=2), file=sys.stderr)
        sys.exit(1)

    # Get endpoint (optional)
    endpoint = None
    if '--endpoint' in args:
        idx = args.index('--endpoint')
        if idx + 1 < len(args):
            endpoint = args[idx + 1]

    # Batch mode
    if '--batch' in args:
        idx = args.index('--batch')
        if idx + 1 >= len(args):
            print(json.dumps({
                'error': 'Batch file path required after --batch'
            }, indent=2), file=sys.stderr)
            sys.exit(1)

        file_path = args[idx + 1]
        urls = load_urls_from_file(file_path)

        if not urls:
            print(json.dumps({
                'error': f'No valid URLs found in {file_path}'
            }, indent=2), file=sys.stderr)
            sys.exit(1)

        if endpoint:
            host = extract_host(urls[0])
            result = submit_batch_urls(urls, key, host, endpoint)
        else:
            result = submit_to_all_engines(urls, key)

        print(json.dumps(result, indent=2))
        sys.exit(0 if result.get('summary', {}).get('all_successful') else 1)

    # Single URL mode
    url = None
    for arg in args:
        if validate_url(arg):
            url = arg
            break

    if not url:
        print(json.dumps({
            'error': 'Valid URL required'
        }, indent=2), file=sys.stderr)
        sys.exit(1)

    if endpoint:
        result = submit_single_url(url, key, endpoint)
    else:
        result = submit_to_all_engines([url], key)

    print(json.dumps(result, indent=2))

    if endpoint:
        sys.exit(0 if result.get('success') else 1)
    else:
        sys.exit(0 if result.get('summary', {}).get('all_successful') else 1)


if __name__ == '__main__':
    main()
