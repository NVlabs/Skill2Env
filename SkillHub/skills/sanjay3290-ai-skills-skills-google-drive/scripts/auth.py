#!/usr/bin/env python3
"""
OAuth token management for Google Drive API.
Standalone authentication - does not require the MCP server.
Cross-platform support using keyring library.
"""

import http.server
import json
import secrets
import socket
import sys
import time
import webbrowser
from base64 import b64encode
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlencode, parse_qs, urlparse
import urllib.request
import urllib.error

import keyring

# OAuth Configuration - uses same cloud function as MCP server
CLIENT_ID = "338689075775-o75k922vn5fdl18qergr96rp8g63e4d7.apps.googleusercontent.com"
CLOUD_FUNCTION_URL = "https://google-workspace-extension.geminicli.com"
REFRESH_ENDPOINT = f"{CLOUD_FUNCTION_URL}/refreshToken"

# Keyring configuration
KEYCHAIN_SERVICE = "google-drive-skill-oauth"
KEYCHAIN_ACCOUNT = "main-account"

# Google Drive requires these scopes (read/write)
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/userinfo.profile",
]

TOKEN_EXPIRY_BUFFER_MS = 5 * 60 * 1000  # 5 minutes


@dataclass
class TokenInfo:
    access_token: str
    refresh_token: Optional[str]
    expires_at: Optional[int]
    scope: Optional[str]


# ==============================================================================
# Cross-platform token storage using keyring
# ==============================================================================

def get_tokens_from_keychain() -> Optional[TokenInfo]:
    """Read OAuth tokens from keyring."""
    try:
        data_str = keyring.get_password(KEYCHAIN_SERVICE, KEYCHAIN_ACCOUNT)
        if not data_str:
            return None
        data = json.loads(data_str)
        token = data.get("token", {})
        return TokenInfo(
            access_token=token.get("accessToken", ""),
            refresh_token=token.get("refreshToken"),
            expires_at=token.get("expiresAt"),
            scope=token.get("scope")
        )
    except (json.JSONDecodeError, keyring.errors.KeyringError):
        return None


def save_tokens_to_keychain(token_info: TokenInfo) -> bool:
    """Save OAuth tokens to keyring."""
    data = {
        "serverName": KEYCHAIN_ACCOUNT,
        "token": {
            "accessToken": token_info.access_token,
            "refreshToken": token_info.refresh_token,
            "tokenType": "Bearer",
            "scope": token_info.scope,
            "expiresAt": token_info.expires_at
        },
        "updatedAt": int(time.time() * 1000)
    }
    try:
        keyring.set_password(KEYCHAIN_SERVICE, KEYCHAIN_ACCOUNT, json.dumps(data))
        return True
    except keyring.errors.KeyringError:
        return False


def clear_tokens_from_keychain() -> bool:
    """Clear OAuth tokens from keyring."""
    try:
        keyring.delete_password(KEYCHAIN_SERVICE, KEYCHAIN_ACCOUNT)
        return True
    except (keyring.errors.PasswordDeleteError, keyring.errors.KeyringError):
        return False


# ==============================================================================
# Utility functions
# ==============================================================================

def get_available_port() -> int:
    """Find an available port for the OAuth callback server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 0))
        return s.getsockname()[1]


def is_token_expired(token_info: TokenInfo) -> bool:
    """Check if the access token is expired or expiring soon."""
    if not token_info.expires_at:
        return False
    current_time_ms = int(time.time() * 1000)
    return token_info.expires_at < (current_time_ms + TOKEN_EXPIRY_BUFFER_MS)


def refresh_access_token(refresh_token: str) -> Optional[dict]:
    """Refresh access token using the cloud function."""
    try:
        data = json.dumps({"refresh_token": refresh_token}).encode('utf-8')
        req = urllib.request.Request(
            REFRESH_ENDPOINT,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as e:
        print(f"Error refreshing token: {e}", file=sys.stderr)
        return None


class OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):
    """HTTP request handler for OAuth callback."""

    token_info: Optional[TokenInfo] = None
    csrf_token: str = ""
    error: Optional[str] = None

    def log_message(self, format: str, *args) -> None:  # noqa: A002
        """Suppress default logging."""
        _ = format, args  # Unused

    def do_GET(self):
        """Handle the OAuth callback."""
        parsed = urlparse(self.path)

        if not parsed.path.startswith("/oauth2callback"):
            self.send_error(404)
            return

        params = parse_qs(parsed.query)

        # Validate CSRF token
        state = params.get("state", [""])[0]
        if state != OAuthCallbackHandler.csrf_token:
            OAuthCallbackHandler.error = "State mismatch - possible CSRF attack"
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Error: State mismatch</h1></body></html>")
            return

        # Check for errors
        if "error" in params:
            OAuthCallbackHandler.error = params.get("error_description", params["error"])[0]
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f"<html><body><h1>Error: {OAuthCallbackHandler.error}</h1></body></html>".encode())
            return

        # Extract tokens
        access_token = params.get("access_token", [""])[0]
        refresh_token = params.get("refresh_token", [""])[0]
        expiry_date = params.get("expiry_date", [""])[0]
        scope = params.get("scope", [""])[0]

        if access_token:
            OAuthCallbackHandler.token_info = TokenInfo(
                access_token=access_token,
                refresh_token=refresh_token or None,
                expires_at=int(expiry_date) if expiry_date else None,
                scope=scope or None
            )

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"""<html><body>
                <h1>Authentication successful!</h1>
                <p>You can close this window and return to the terminal.</p>
                <script>window.close();</script>
            </body></html>""")
        else:
            OAuthCallbackHandler.error = "No access token received"
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Error: No access token received</h1></body></html>")


def perform_oauth_flow() -> Optional[TokenInfo]:
    """Perform the full OAuth flow with browser-based authentication."""
    port = get_available_port()
    redirect_uri = f"http://localhost:{port}/oauth2callback"
    csrf_token = secrets.token_hex(32)

    # Build state payload for cloud function
    state_payload = {
        "uri": redirect_uri,
        "manual": False,
        "csrf": csrf_token
    }
    state = b64encode(json.dumps(state_payload).encode()).decode()

    # Build auth URL
    auth_params = {
        "client_id": CLIENT_ID,
        "redirect_uri": CLOUD_FUNCTION_URL,  # Cloud function handles the secret
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "prompt": "consent",
        "state": state
    }
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(auth_params)}"

    # Set up callback handler
    OAuthCallbackHandler.csrf_token = csrf_token
    OAuthCallbackHandler.token_info = None
    OAuthCallbackHandler.error = None

    # Start local server
    server = http.server.HTTPServer(('localhost', port), OAuthCallbackHandler)
    server.timeout = 300  # 5 minute timeout

    print(f"Opening browser for authentication...", file=sys.stderr)
    print(f"If browser doesn't open, visit: {auth_url}", file=sys.stderr)

    webbrowser.open(auth_url)

    # Wait for callback
    print("Waiting for authentication...", file=sys.stderr)
    while OAuthCallbackHandler.token_info is None and OAuthCallbackHandler.error is None:
        server.handle_request()

    server.server_close()

    if OAuthCallbackHandler.error:
        print(f"Authentication failed: {OAuthCallbackHandler.error}", file=sys.stderr)
        return None

    return OAuthCallbackHandler.token_info


def get_valid_access_token(interactive: bool = True) -> Optional[str]:
    """
    Get a valid access token.

    Args:
        interactive: If True, will prompt for OAuth flow if no tokens exist.
                    If False, will return None if no valid tokens.
    """
    token_info = get_tokens_from_keychain()

    # No tokens - need to authenticate
    if not token_info or not token_info.access_token:
        if not interactive:
            return None

        print("No OAuth tokens found. Starting authentication...", file=sys.stderr)
        token_info = perform_oauth_flow()

        if not token_info:
            return None

        save_tokens_to_keychain(token_info)
        print("Authentication successful!", file=sys.stderr)
        return token_info.access_token

    # Check if token needs refresh
    if is_token_expired(token_info) and token_info.refresh_token:
        print("Access token expired, refreshing...", file=sys.stderr)
        new_tokens = refresh_access_token(token_info.refresh_token)

        if new_tokens:
            token_info.access_token = new_tokens.get("access_token", token_info.access_token)
            token_info.expires_at = new_tokens.get("expiry_date", token_info.expires_at)
            save_tokens_to_keychain(token_info)
            print("Token refreshed successfully.", file=sys.stderr)
        else:
            # Refresh failed - try re-authenticating if interactive
            if interactive:
                print("Token refresh failed. Re-authenticating...", file=sys.stderr)
                token_info = perform_oauth_flow()
                if token_info:
                    save_tokens_to_keychain(token_info)
                else:
                    return None
            else:
                print("Warning: Failed to refresh token.", file=sys.stderr)

    return token_info.access_token if token_info else None


def logout() -> bool:
    """Clear stored OAuth tokens."""
    return clear_tokens_from_keychain()


def main():
    """CLI for auth operations."""
    import argparse

    parser = argparse.ArgumentParser(description="Google Drive OAuth management")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("login", help="Authenticate with Google")
    subparsers.add_parser("logout", help="Clear stored tokens")
    subparsers.add_parser("token", help="Print current access token")
    subparsers.add_parser("status", help="Check authentication status")

    args = parser.parse_args()

    if args.command == "login":
        token_info = perform_oauth_flow()
        if token_info:
            save_tokens_to_keychain(token_info)
            print("Login successful!")
        else:
            print("Login failed.")
            sys.exit(1)

    elif args.command == "logout":
        if logout():
            print("Logged out successfully.")
        else:
            print("No tokens to clear.")

    elif args.command == "token":
        token = get_valid_access_token(interactive=False)
        if token:
            print(token)
        else:
            print("Not authenticated. Run: python auth.py login", file=sys.stderr)
            sys.exit(1)

    elif args.command == "status":
        token_info = get_tokens_from_keychain()
        if token_info and token_info.access_token:
            expired = is_token_expired(token_info)
            print(f"Status: Authenticated")
            print(f"Token expired: {expired}")
            if token_info.expires_at:
                expires_in = (token_info.expires_at - int(time.time() * 1000)) / 1000 / 60
                print(f"Expires in: {expires_in:.1f} minutes")
        else:
            print("Status: Not authenticated")
            print("Run: python auth.py login")
            sys.exit(1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
