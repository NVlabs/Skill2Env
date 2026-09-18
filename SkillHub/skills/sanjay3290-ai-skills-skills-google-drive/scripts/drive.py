#!/usr/bin/env python3
"""
Google Drive API operations.
Lightweight alternative to the full Google Workspace MCP server.
"""

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
import urllib.parse
from typing import Optional

from auth import get_valid_access_token

DRIVE_API_BASE = "https://www.googleapis.com/drive/v3"

# Google Drive URL patterns for extracting file/folder IDs
URL_PATTERNS = [
    (r'/folders/([a-zA-Z0-9-_]+)', 'folder'),
    (r'/file/d/([a-zA-Z0-9-_]+)', 'file'),
    (r'/document/d/([a-zA-Z0-9-_]+)', 'file'),
    (r'/spreadsheets/d/([a-zA-Z0-9-_]+)', 'file'),
    (r'/presentation/d/([a-zA-Z0-9-_]+)', 'file'),
    (r'/forms/d/([a-zA-Z0-9-_]+)', 'file'),
    (r'[?&]id=([a-zA-Z0-9-_]+)', 'unknown'),
]

MIN_DRIVE_ID_LENGTH = 25


def escape_query_string(s: str) -> str:
    """Escape special characters in Drive query strings."""
    return s.replace("\\", "\\\\").replace("'", "\\'")


def api_request(method: str, endpoint: str, params: Optional[dict] = None,
                stream: bool = False) -> dict | bytes:
    """Make an authenticated request to the Google Drive API."""
    token = get_valid_access_token()
    if not token:
        return {"error": "Failed to get access token"}

    url = f"{DRIVE_API_BASE}/{endpoint}"
    if params:
        url += "?" + urllib.parse.urlencode(params)

    headers = {
        "Authorization": f"Bearer {token}",
    }

    try:
        req = urllib.request.Request(url, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=60) as response:
            if stream:
                return response.read()
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else str(e)
        return {"error": f"HTTP {e.code}: {error_body}"}
    except urllib.error.URLError as e:
        return {"error": f"Request failed: {e.reason}"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response"}


def extract_id_from_url(url: str) -> tuple[Optional[str], str]:
    """Extract file/folder ID from a Google Drive URL."""
    for pattern, id_type in URL_PATTERNS:
        match = re.search(pattern, url)
        if match:
            return match.group(1), id_type
    return None, 'unknown'


def is_drive_url(query: str) -> bool:
    """Check if query looks like a Google Drive URL."""
    return 'drive.google.com' in query or 'docs.google.com' in query


def is_drive_id(query: str) -> bool:
    """Check if query looks like a Drive file/folder ID."""
    if len(query) < MIN_DRIVE_ID_LENGTH:
        return False
    return bool(re.match(r'^[a-zA-Z0-9-_]+$', query)) and ' ' not in query


def search(query: Optional[str] = None, page_size: int = 10,
           page_token: Optional[str] = None, shared_with_me: bool = False) -> dict:
    """
    Search for files and folders in Google Drive.

    Supports:
    - Full-text search: "quarterly report"
    - Title search: "title:budget"
    - Google Drive URLs: extracts file/folder ID automatically
    - Folder ID: lists contents if query looks like an ID
    - Native query syntax: "mimeType='application/pdf'"
    """
    q = None

    # Handle Google Drive URLs
    if query and is_drive_url(query):
        file_id, id_type = extract_id_from_url(query)

        if not file_id:
            return {"error": "Could not extract file/folder ID from URL"}

        # Determine if it's a folder
        if id_type == 'folder':
            q = f"'{file_id}' in parents"
        elif id_type == 'unknown':
            # Check the file type via API
            result = api_request("GET", f"files/{file_id}", {"fields": "mimeType"})
            if isinstance(result, dict) and "error" not in result:
                if result.get("mimeType") == "application/vnd.google-apps.folder":
                    q = f"'{file_id}' in parents"
                else:
                    # Return just this file
                    file_result = api_request("GET", f"files/{file_id}", {
                        "fields": "id, name, modifiedTime, viewedByMeTime, mimeType, parents"
                    })
                    if isinstance(file_result, dict) and "error" not in file_result:
                        return {"files": [file_result], "nextPageToken": None}
                    return file_result
        else:
            # It's a file, get its details
            file_result = api_request("GET", f"files/{file_id}", {
                "fields": "id, name, modifiedTime, viewedByMeTime, mimeType, parents"
            })
            if isinstance(file_result, dict) and "error" not in file_result:
                return {"files": [file_result], "nextPageToken": None}
            return file_result

    # Handle other query types
    elif query:
        query = query.strip()

        # Title search prefix
        if query.lower().startswith("title:"):
            search_term = query[6:].strip()
            # Remove quotes if present
            if (search_term.startswith("'") and search_term.endswith("'")) or \
               (search_term.startswith('"') and search_term.endswith('"')):
                search_term = search_term[1:-1]
            q = f"name contains '{escape_query_string(search_term)}'"

        # Check if it's a Drive ID (list folder contents)
        elif is_drive_id(query):
            q = f"'{query}' in parents"

        # Check if it's already a Drive query syntax
        elif re.search(r'( and | or | not | contains | in |=)', query):
            q = query

        # Default to full-text search
        else:
            q = f"fullText contains '{escape_query_string(query)}'"

    # Add sharedWithMe filter
    if shared_with_me:
        if q:
            q += " and sharedWithMe"
        else:
            q = "sharedWithMe"

    params = {
        "pageSize": page_size,
        "fields": "nextPageToken, files(id, name, modifiedTime, viewedByMeTime, mimeType, parents)"
    }

    if q:
        params["q"] = q

    if page_token:
        params["pageToken"] = page_token

    result = api_request("GET", "files", params)

    if isinstance(result, dict) and "error" not in result:
        return {
            "files": result.get("files", []),
            "nextPageToken": result.get("nextPageToken")
        }

    return result


def find_folder(folder_name: str) -> dict:
    """Find a folder by its exact name."""
    escaped_name = escape_query_string(folder_name)
    q = f"mimeType='application/vnd.google-apps.folder' and name = '{escaped_name}'"

    params = {
        "q": q,
        "fields": "files(id, name)",
        "spaces": "drive"
    }

    result = api_request("GET", "files", params)

    if isinstance(result, dict) and "error" not in result:
        return {"folders": result.get("files", [])}

    return result


def list_files(folder_id: Optional[str] = None, page_size: int = 10,
               page_token: Optional[str] = None) -> dict:
    """List files in a folder or root."""
    params = {
        "pageSize": page_size,
        "fields": "nextPageToken, files(id, name, modifiedTime, mimeType, parents)"
    }

    if folder_id:
        params["q"] = f"'{folder_id}' in parents"

    if page_token:
        params["pageToken"] = page_token

    result = api_request("GET", "files", params)

    if isinstance(result, dict) and "error" not in result:
        return {
            "files": result.get("files", []),
            "nextPageToken": result.get("nextPageToken")
        }

    return result


def download(file_id: str, local_path: str) -> dict:
    """
    Download a file from Google Drive.

    Note: Google Workspace files (Docs, Sheets, Slides) cannot be downloaded
    directly. Use the appropriate export format or getText tools instead.
    """
    # First get file metadata to check type
    metadata = api_request("GET", f"files/{file_id}", {"fields": "id, name, mimeType"})

    if isinstance(metadata, dict) and "error" in metadata:
        return metadata

    mime_type = metadata.get("mimeType", "")
    file_name = metadata.get("name", "unknown")

    # Handle Google Workspace files
    google_workspace_types = {
        "application/vnd.google-apps.document": ("Google Doc", "docs.getText"),
        "application/vnd.google-apps.spreadsheet": ("Google Sheet", "sheets.getText"),
        "application/vnd.google-apps.presentation": ("Google Slides", "slides.getText"),
    }

    if mime_type in google_workspace_types:
        file_type, tool = google_workspace_types[mime_type]
        return {
            "error": f"This is a {file_type}. Direct download not supported.",
            "suggestion": f"Use the '{tool}' tool with ID: {file_id}",
            "fileId": file_id,
            "fileName": file_name
        }

    if mime_type.startswith("application/vnd.google-apps."):
        return {
            "error": f"Google Workspace file type ({mime_type}) cannot be downloaded directly.",
            "suggestion": "Export the file manually or use specific tools.",
            "fileId": file_id,
            "fileName": file_name
        }

    # Download the file
    file_content = api_request("GET", f"files/{file_id}", {"alt": "media"}, stream=True)

    if isinstance(file_content, dict) and "error" in file_content:
        return file_content

    # Resolve path
    abs_path = os.path.abspath(os.path.expanduser(local_path))

    # Create directory if needed
    dir_path = os.path.dirname(abs_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    # Write file
    try:
        with open(abs_path, 'wb') as f:
            f.write(file_content)

        return {
            "success": True,
            "message": f"Downloaded '{file_name}' to {abs_path}",
            "localPath": abs_path,
            "fileName": file_name,
            "fileId": file_id
        }
    except IOError as e:
        return {"error": f"Failed to write file: {e}"}


def api_write_request(method: str, endpoint: str, data: Optional[dict] = None,
                      params: Optional[dict] = None) -> dict:
    """Make an authenticated write request (POST/PATCH) to the Google Drive API."""
    token = get_valid_access_token()
    if not token:
        return {"error": "Failed to get access token"}

    url = f"{DRIVE_API_BASE}/{endpoint}"
    if params:
        url += "?" + urllib.parse.urlencode(params)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    body = json.dumps(data).encode('utf-8') if data else None

    try:
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=60) as response:
            response_data = response.read().decode('utf-8')
            return json.loads(response_data) if response_data else {"success": True}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else str(e)
        return {"error": f"HTTP {e.code}: {error_body}"}
    except urllib.error.URLError as e:
        return {"error": f"Request failed: {e.reason}"}
    except json.JSONDecodeError:
        return {"success": True}


def upload(local_path: str, folder_id: Optional[str] = None, name: Optional[str] = None) -> dict:
    """
    Upload a file to Google Drive.

    Args:
        local_path: Path to the local file to upload
        folder_id: Target folder ID (uploads to root if not specified)
        name: Name for the file in Drive (uses local filename if not specified)
    """
    import mimetypes

    abs_path = os.path.abspath(os.path.expanduser(local_path))

    if not os.path.exists(abs_path):
        return {"error": f"File not found: {abs_path}"}

    file_name = name or os.path.basename(abs_path)
    mime_type = mimetypes.guess_type(abs_path)[0] or "application/octet-stream"

    # Read file content
    try:
        with open(abs_path, 'rb') as f:
            file_content = f.read()
    except IOError as e:
        return {"error": f"Failed to read file: {e}"}

    # Build metadata
    metadata = {"name": file_name}
    if folder_id:
        metadata["parents"] = [folder_id]

    # Use multipart upload
    token = get_valid_access_token()
    if not token:
        return {"error": "Failed to get access token"}

    boundary = "skill_upload_boundary"
    body = (
        f"--{boundary}\r\n"
        f"Content-Type: application/json; charset=UTF-8\r\n\r\n"
        f"{json.dumps(metadata)}\r\n"
        f"--{boundary}\r\n"
        f"Content-Type: {mime_type}\r\n\r\n"
    ).encode('utf-8') + file_content + f"\r\n--{boundary}--".encode('utf-8')

    url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": f"multipart/related; boundary={boundary}",
    }

    try:
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            return {
                "success": True,
                "fileId": result.get("id"),
                "name": result.get("name"),
                "mimeType": result.get("mimeType")
            }
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else str(e)
        return {"error": f"HTTP {e.code}: {error_body}"}
    except urllib.error.URLError as e:
        return {"error": f"Upload failed: {e.reason}"}


def create_folder(folder_name: str, parent_id: Optional[str] = None) -> dict:
    """
    Create a new folder in Google Drive.

    Args:
        folder_name: Name of the new folder
        parent_id: Parent folder ID (creates in root if not specified)
    """
    metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder"
    }
    if parent_id:
        metadata["parents"] = [parent_id]

    return api_write_request("POST", "files", data=metadata)


def move_file(file_id: str, new_parent_id: str) -> dict:
    """
    Move a file to a different folder.

    Args:
        file_id: ID of the file to move
        new_parent_id: ID of the destination folder
    """
    # Get current parents
    current = api_request("GET", f"files/{file_id}", {"fields": "parents"})
    if isinstance(current, dict) and "error" in current:
        return current

    old_parents = ",".join(current.get("parents", []))

    params = {
        "addParents": new_parent_id,
        "removeParents": old_parents,
        "fields": "id, name, parents"
    }

    return api_write_request("PATCH", f"files/{file_id}", params=params)


def copy_file(file_id: str, new_name: Optional[str] = None, folder_id: Optional[str] = None) -> dict:
    """
    Copy a file.

    Args:
        file_id: ID of the file to copy
        new_name: Name for the copy (defaults to "Copy of <original>")
        folder_id: Destination folder ID (same folder if not specified)
    """
    data = {}
    if new_name:
        data["name"] = new_name
    if folder_id:
        data["parents"] = [folder_id]

    return api_write_request("POST", f"files/{file_id}/copy", data=data)


def rename_file(file_id: str, new_name: str) -> dict:
    """
    Rename a file or folder.

    Args:
        file_id: ID of the file/folder to rename
        new_name: New name
    """
    return api_write_request("PATCH", f"files/{file_id}", data={"name": new_name},
                             params={"fields": "id, name"})


def trash_file(file_id: str) -> dict:
    """
    Move a file or folder to trash.

    Args:
        file_id: ID of the file/folder to trash
    """
    return api_write_request("PATCH", f"files/{file_id}", data={"trashed": True},
                             params={"fields": "id, name, trashed"})


def main():
    parser = argparse.ArgumentParser(description="Google Drive API operations")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # search
    search_parser = subparsers.add_parser("search", help="Search for files and folders")
    search_parser.add_argument("query", nargs="?", help="Search query, URL, or folder ID")
    search_parser.add_argument("--limit", type=int, default=10, help="Max results (default: 10)")
    search_parser.add_argument("--page-token", help="Pagination token")
    search_parser.add_argument("--shared-with-me", action="store_true", help="Only shared files")

    # find-folder
    find_folder_parser = subparsers.add_parser("find-folder", help="Find folder by name")
    find_folder_parser.add_argument("name", help="Folder name to find")

    # list
    list_parser = subparsers.add_parser("list", help="List files in a folder")
    list_parser.add_argument("folder_id", nargs="?", help="Folder ID (root if not specified)")
    list_parser.add_argument("--limit", type=int, default=10, help="Max results (default: 10)")
    list_parser.add_argument("--page-token", help="Pagination token")

    # download
    download_parser = subparsers.add_parser("download", help="Download a file")
    download_parser.add_argument("file_id", help="File ID to download")
    download_parser.add_argument("local_path", help="Local path to save file")

    # upload
    upload_parser = subparsers.add_parser("upload", help="Upload a file to Drive")
    upload_parser.add_argument("local_path", help="Path to local file")
    upload_parser.add_argument("--folder", help="Target folder ID")
    upload_parser.add_argument("--name", help="Name for file in Drive (default: local filename)")

    # create-folder
    create_folder_parser = subparsers.add_parser("create-folder", help="Create a new folder")
    create_folder_parser.add_argument("name", help="Folder name")
    create_folder_parser.add_argument("--parent", help="Parent folder ID")

    # move
    move_parser = subparsers.add_parser("move", help="Move a file to another folder")
    move_parser.add_argument("file_id", help="File ID to move")
    move_parser.add_argument("folder_id", help="Destination folder ID")

    # copy
    copy_parser = subparsers.add_parser("copy", help="Copy a file")
    copy_parser.add_argument("file_id", help="File ID to copy")
    copy_parser.add_argument("--name", help="Name for the copy")
    copy_parser.add_argument("--folder", help="Destination folder ID")

    # rename
    rename_parser = subparsers.add_parser("rename", help="Rename a file or folder")
    rename_parser.add_argument("file_id", help="File/folder ID")
    rename_parser.add_argument("new_name", help="New name")

    # trash
    trash_parser = subparsers.add_parser("trash", help="Move a file to trash")
    trash_parser.add_argument("file_id", help="File/folder ID to trash")

    args = parser.parse_args()

    if args.command == "search":
        result = search(args.query, args.limit, args.page_token, args.shared_with_me)
    elif args.command == "find-folder":
        result = find_folder(args.name)
    elif args.command == "list":
        result = list_files(args.folder_id, args.limit, args.page_token)
    elif args.command == "download":
        result = download(args.file_id, args.local_path)
    elif args.command == "upload":
        result = upload(args.local_path, args.folder, args.name)
    elif args.command == "create-folder":
        result = create_folder(args.name, args.parent)
    elif args.command == "move":
        result = move_file(args.file_id, args.folder_id)
    elif args.command == "copy":
        result = copy_file(args.file_id, args.name, args.folder)
    elif args.command == "rename":
        result = rename_file(args.file_id, args.new_name)
    elif args.command == "trash":
        result = trash_file(args.file_id)
    else:
        result = {"error": f"Unknown command: {args.command}"}

    print(json.dumps(result, indent=2))

    if isinstance(result, dict) and "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()
