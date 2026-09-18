#!/usr/bin/env python3
"""
Google Sheets API operations.
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

SHEETS_API_BASE = "https://sheets.googleapis.com/v4"
DRIVE_API_BASE = "https://www.googleapis.com/drive/v3"

# MIME type for Google Sheets
SHEETS_MIME_TYPE = "application/vnd.google-apps.spreadsheet"


def api_write_request(base_url: str, endpoint: str, data: dict, method: str = "PUT", params: Optional[dict] = None) -> dict:
    """Make an authenticated write request (PUT/POST) to a Google API."""
    token = get_valid_access_token()
    if not token:
        return {"error": "Failed to get access token"}

    url = f"{base_url}/{endpoint}"
    if params:
        url += "?" + urllib.parse.urlencode(params)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        body = json.dumps(data).encode('utf-8')
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


def extract_spreadsheet_id(spreadsheet_id_or_url: str) -> str:
    """
    Extract spreadsheet ID from a URL or return the ID as-is.

    Handles URLs like:
    - https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit
    - https://docs.google.com/spreadsheets/d/SPREADSHEET_ID
    """
    # Pattern to match Google Sheets URLs
    url_pattern = r'docs\.google\.com/spreadsheets/d/([a-zA-Z0-9_-]+)'
    match = re.search(url_pattern, spreadsheet_id_or_url)
    if match:
        return match.group(1)
    return spreadsheet_id_or_url


def api_request(base_url: str, endpoint: str, params: Optional[dict] = None) -> dict:
    """Make an authenticated GET request to a Google API."""
    token = get_valid_access_token()
    if not token:
        return {"error": "Failed to get access token"}

    url = f"{base_url}/{endpoint}"
    if params:
        url += "?" + urllib.parse.urlencode(params)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        req = urllib.request.Request(url, headers=headers, method="GET")
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else str(e)
        return {"error": f"HTTP {e.code}: {error_body}"}
    except urllib.error.URLError as e:
        return {"error": f"Request failed: {e.reason}"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response"}


def get_text(spreadsheet_id: str, output_format: str = "text") -> dict:
    """
    Get spreadsheet content in various formats.

    Args:
        spreadsheet_id: Spreadsheet ID or URL
        output_format: 'text', 'csv', or 'json'
    """
    sheet_id = extract_spreadsheet_id(spreadsheet_id)

    # First, get spreadsheet metadata
    metadata = api_request(SHEETS_API_BASE, f"spreadsheets/{sheet_id}", {
        "includeGridData": "false"
    })

    if "error" in metadata:
        return metadata

    title = metadata.get("properties", {}).get("title", "Untitled")
    sheets = metadata.get("sheets", [])

    content = ""
    json_data = {}

    if output_format != "json":
        content += f"Spreadsheet Title: {title}\n\n"

    # Get data from each sheet
    for sheet in sheets:
        sheet_name = sheet.get("properties", {}).get("title", "")
        if not sheet_name:
            continue

        # Get values for this sheet
        values_result = api_request(SHEETS_API_BASE, f"spreadsheets/{sheet_id}/values/{urllib.parse.quote(sheet_name)}")

        if "error" in values_result:
            if output_format == "json":
                continue
            content += f"Sheet Name: {sheet_name}\n(Error reading sheet)\n\n"
            continue

        values = values_result.get("values", [])

        if output_format == "json":
            json_data[sheet_name] = values
        else:
            content += f"Sheet Name: {sheet_name}\n"

            if not values:
                content += "(Empty sheet)\n"
            else:
                for row in values:
                    if output_format == "csv":
                        # Convert to CSV format
                        csv_row = []
                        for cell in row:
                            cell_str = str(cell) if cell else ""
                            if "," in cell_str or '"' in cell_str or "\n" in cell_str:
                                csv_row.append(f'"{cell_str.replace(chr(34), chr(34)+chr(34))}"')
                            else:
                                csv_row.append(cell_str)
                        content += ",".join(csv_row) + "\n"
                    else:
                        # Plain text format with pipe separators
                        content += " | ".join(str(cell) if cell else "" for cell in row) + "\n"

            content += "\n"

    if output_format == "json":
        return {"data": json_data}

    return {"content": content.strip()}


def get_range(spreadsheet_id: str, range_notation: str) -> dict:
    """
    Get values from a specific range.

    Args:
        spreadsheet_id: Spreadsheet ID or URL
        range_notation: A1 notation (e.g., 'Sheet1!A1:B10', 'A1:C5')
    """
    sheet_id = extract_spreadsheet_id(spreadsheet_id)

    result = api_request(SHEETS_API_BASE, f"spreadsheets/{sheet_id}/values/{urllib.parse.quote(range_notation)}")

    if "error" in result:
        return result

    return {
        "range": result.get("range"),
        "values": result.get("values", [])
    }


def find_spreadsheets(query: str, page_size: int = 10, page_token: Optional[str] = None) -> dict:
    """
    Find spreadsheets by search query.

    Args:
        query: Search query (searches name and content)
        page_size: Number of results to return
        page_token: Pagination token
    """
    # Build Drive API search query
    # Search for spreadsheets matching the query in name or fullText
    search_query = f"mimeType='{SHEETS_MIME_TYPE}' and (name contains '{query}' or fullText contains '{query}')"

    params = {
        "q": search_query,
        "pageSize": str(page_size),
        "fields": "nextPageToken, files(id, name, createdTime, modifiedTime, webViewLink)"
    }

    if page_token:
        params["pageToken"] = page_token

    result = api_request(DRIVE_API_BASE, "files", params)

    if "error" in result:
        return result

    return {
        "files": result.get("files", []),
        "nextPageToken": result.get("nextPageToken")
    }


def get_metadata(spreadsheet_id: str) -> dict:
    """
    Get spreadsheet metadata.

    Args:
        spreadsheet_id: Spreadsheet ID or URL
    """
    sheet_id = extract_spreadsheet_id(spreadsheet_id)

    result = api_request(SHEETS_API_BASE, f"spreadsheets/{sheet_id}", {
        "includeGridData": "false"
    })

    if "error" in result:
        return result

    metadata = {
        "spreadsheetId": result.get("spreadsheetId"),
        "title": result.get("properties", {}).get("title"),
        "locale": result.get("properties", {}).get("locale"),
        "timeZone": result.get("properties", {}).get("timeZone"),
        "sheets": []
    }

    for sheet in result.get("sheets", []):
        props = sheet.get("properties", {})
        grid_props = props.get("gridProperties", {})
        metadata["sheets"].append({
            "sheetId": props.get("sheetId"),
            "title": props.get("title"),
            "index": props.get("index"),
            "rowCount": grid_props.get("rowCount"),
            "columnCount": grid_props.get("columnCount")
        })

    return metadata


def quote_range(range_notation: str) -> str:
    """URL-encode a range notation, matching the read API encoding."""
    return urllib.parse.quote(range_notation)


def update_range(spreadsheet_id: str, range_notation: str, values: list, value_input_option: str = "USER_ENTERED") -> dict:
    """
    Update a range of cells with new values.

    Args:
        spreadsheet_id: Spreadsheet ID or URL
        range_notation: A1 notation (e.g., 'Sheet1!A1:B10')
        values: 2D list of values, e.g. [["A1","B1"],["A2","B2"]]
        value_input_option: USER_ENTERED (parses formulas/numbers) or RAW
    """
    sheet_id = extract_spreadsheet_id(spreadsheet_id)
    data = {
        "range": range_notation,
        "majorDimension": "ROWS",
        "values": values
    }
    return api_write_request(
        SHEETS_API_BASE,
        f"spreadsheets/{sheet_id}/values/{quote_range(range_notation)}",
        data,
        method="PUT",
        params={"valueInputOption": value_input_option}
    )


def append_rows(spreadsheet_id: str, range_notation: str, values: list, value_input_option: str = "USER_ENTERED") -> dict:
    """
    Append rows after the last row with data in a sheet.

    Args:
        spreadsheet_id: Spreadsheet ID or URL
        range_notation: A1 notation for the target sheet/range (e.g., 'Sheet1!A:Z')
        values: 2D list of row values to append
        value_input_option: USER_ENTERED or RAW
    """
    sheet_id = extract_spreadsheet_id(spreadsheet_id)
    data = {
        "range": range_notation,
        "majorDimension": "ROWS",
        "values": values
    }
    return api_write_request(
        SHEETS_API_BASE,
        f"spreadsheets/{sheet_id}/values/{quote_range(range_notation)}:append",
        data,
        method="POST",
        params={
            "valueInputOption": value_input_option,
            "insertDataOption": "INSERT_ROWS"
        }
    )


def clear_range(spreadsheet_id: str, range_notation: str) -> dict:
    """
    Clear values from a range of cells.

    Args:
        spreadsheet_id: Spreadsheet ID or URL
        range_notation: A1 notation (e.g., 'Sheet1!A1:B10')
    """
    sheet_id = extract_spreadsheet_id(spreadsheet_id)
    return api_write_request(
        SHEETS_API_BASE,
        f"spreadsheets/{sheet_id}/values/{quote_range(range_notation)}:clear",
        {},
        method="POST"
    )


def batch_update(spreadsheet_id: str, requests: list) -> dict:
    """
    Execute batch update requests for advanced operations.

    Args:
        spreadsheet_id: Spreadsheet ID or URL
        requests: List of request objects (see Google Sheets API batchUpdate docs)
    """
    sheet_id = extract_spreadsheet_id(spreadsheet_id)
    return api_write_request(
        SHEETS_API_BASE,
        f"spreadsheets/{sheet_id}:batchUpdate",
        {"requests": requests},
        method="POST"
    )


def main():
    parser = argparse.ArgumentParser(description="Google Sheets API operations")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # get-text
    get_text_parser = subparsers.add_parser("get-text", help="Get spreadsheet content")
    get_text_parser.add_argument("spreadsheet_id", help="Spreadsheet ID or URL")
    get_text_parser.add_argument("--format", choices=["text", "csv", "json"], default="text",
                                  help="Output format (default: text)")

    # get-range
    get_range_parser = subparsers.add_parser("get-range", help="Get values from a specific range")
    get_range_parser.add_argument("spreadsheet_id", help="Spreadsheet ID or URL")
    get_range_parser.add_argument("range", help="A1 notation range (e.g., 'Sheet1!A1:B10')")

    # find
    find_parser = subparsers.add_parser("find", help="Find spreadsheets by search query")
    find_parser.add_argument("query", help="Search query")
    find_parser.add_argument("--limit", type=int, default=10, help="Max results (default: 10)")
    find_parser.add_argument("--page-token", help="Pagination token")

    # get-metadata
    get_metadata_parser = subparsers.add_parser("get-metadata", help="Get spreadsheet metadata")
    get_metadata_parser.add_argument("spreadsheet_id", help="Spreadsheet ID or URL")

    # update-range
    update_range_parser = subparsers.add_parser("update-range", help="Update a range of cells")
    update_range_parser.add_argument("spreadsheet_id", help="Spreadsheet ID or URL")
    update_range_parser.add_argument("range", help="A1 notation range (e.g., 'Sheet1!A1:B2')")
    update_range_parser.add_argument("values", help="JSON 2D array of values (e.g., '[[\"A1\",\"B1\"],[\"A2\",\"B2\"]]')")
    update_range_parser.add_argument("--raw", action="store_true", help="Use RAW input (no formula parsing)")

    # append-rows
    append_parser = subparsers.add_parser("append-rows", help="Append rows to a sheet")
    append_parser.add_argument("spreadsheet_id", help="Spreadsheet ID or URL")
    append_parser.add_argument("range", help="Target sheet range (e.g., 'Sheet1!A:Z')")
    append_parser.add_argument("values", help="JSON 2D array of row values")
    append_parser.add_argument("--raw", action="store_true", help="Use RAW input (no formula parsing)")

    # clear-range
    clear_parser = subparsers.add_parser("clear-range", help="Clear values from a range")
    clear_parser.add_argument("spreadsheet_id", help="Spreadsheet ID or URL")
    clear_parser.add_argument("range", help="A1 notation range to clear")

    # batch-update
    batch_parser = subparsers.add_parser("batch-update", help="Execute batch update requests")
    batch_parser.add_argument("spreadsheet_id", help="Spreadsheet ID or URL")
    batch_parser.add_argument("requests", help="JSON array of batch update request objects")

    args = parser.parse_args()

    if args.command == "get-text":
        result = get_text(args.spreadsheet_id, args.format)
    elif args.command == "get-range":
        result = get_range(args.spreadsheet_id, args.range)
    elif args.command == "find":
        result = find_spreadsheets(args.query, args.limit, args.page_token)
    elif args.command == "get-metadata":
        result = get_metadata(args.spreadsheet_id)
    elif args.command == "update-range":
        values = json.loads(args.values)
        input_option = "RAW" if args.raw else "USER_ENTERED"
        result = update_range(args.spreadsheet_id, args.range, values, input_option)
    elif args.command == "append-rows":
        values = json.loads(args.values)
        input_option = "RAW" if args.raw else "USER_ENTERED"
        result = append_rows(args.spreadsheet_id, args.range, values, input_option)
    elif args.command == "clear-range":
        result = clear_range(args.spreadsheet_id, args.range)
    elif args.command == "batch-update":
        requests_data = json.loads(args.requests)
        result = batch_update(args.spreadsheet_id, requests_data)
    else:
        result = {"error": f"Unknown command: {args.command}"}

    print(json.dumps(result, indent=2))

    if isinstance(result, dict) and "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()
