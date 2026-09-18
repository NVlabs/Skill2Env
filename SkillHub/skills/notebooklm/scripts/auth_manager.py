#!/usr/bin/env python3
"""
NotebookLM authentication manager using a persistent Playwright profile.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from pathlib import Path
from typing import Dict, List

from playwright.sync_api import sync_playwright

from common import (
    NOTEBOOKLM_AUTH_URL,
    NOTEBOOKLM_HOME_URL,
    ensure_data_dirs,
    get_data_dir,
    get_profile_dir,
    launch_persistent_context,
    sanitize_profile_name,
)

CRITICAL_COOKIE_NAMES = {
    "SID",
    "HSID",
    "SSID",
    "APISID",
    "SAPISID",
    "__Secure-1PSID",
    "__Secure-3PSID",
}

DEFAULT_AUTH_TIMEOUT_SEC = 600


def _auth_status(profile: str) -> Dict:
    ensure_data_dirs()
    with sync_playwright() as p:
        context = launch_persistent_context(p, headless=True, profile=profile)
        page = context.new_page()
        try:
            page.goto(NOTEBOOKLM_HOME_URL, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(1500)
            cookies = context.cookies()
            critical = [c for c in cookies if c.get("name") in CRITICAL_COOKIE_NAMES]
            current_url = page.url
            authenticated = len(critical) > 0 and "accounts.google.com" not in current_url
            return {
                "authenticated": authenticated,
                "profile": profile,
                "profileDir": str(get_profile_dir(profile)),
                "criticalCookieCount": len(critical),
                "currentUrl": current_url,
            }
        finally:
            context.close()


def _setup_auth(timeout_seconds: int, profile: str) -> Dict:
    ensure_data_dirs()
    with sync_playwright() as p:
        context = launch_persistent_context(p, headless=False, profile=profile)
        page = context.new_page()
        try:
            page.goto(NOTEBOOKLM_AUTH_URL, wait_until="domcontentloaded", timeout=60000)
            start = time.time()
            while time.time() - start < timeout_seconds:
                url = page.url
                if url.startswith("https://notebooklm.google.com/") and "accounts.google.com" not in url:
                    page.wait_for_timeout(1500)
                    cookies = context.cookies()
                    critical = [c for c in cookies if c.get("name") in CRITICAL_COOKIE_NAMES]
                    return {
                        "authenticated": len(critical) > 0,
                        "profile": profile,
                        "profileDir": str(get_profile_dir(profile)),
                        "criticalCookieCount": len(critical),
                        "currentUrl": url,
                        "message": "Authentication appears complete.",
                    }
                page.wait_for_timeout(1000)

            return {
                "authenticated": False,
                "message": (
                    f"Timed out waiting for login after {timeout_seconds}s. "
                    "Run setup again and complete login in the opened browser."
                ),
                "profile": profile,
                "profileDir": str(get_profile_dir(profile)),
            }
        finally:
            context.close()


def _discover_profiles() -> List[Dict]:
    ensure_data_dirs()
    profiles: List[Dict] = []

    default_dir = get_profile_dir("default")
    profiles.append(
        {
            "profile": "default",
            "profileDir": str(default_dir),
            "exists": default_dir.exists(),
        }
    )

    profiles_dir = get_data_dir() / "profiles"
    if profiles_dir.exists():
        for child in sorted(profiles_dir.iterdir()):
            if not child.is_dir():
                continue
            profile_name = sanitize_profile_name(child.name)
            profiles.append(
                {
                    "profile": profile_name,
                    "profileDir": str(child),
                    "exists": True,
                }
            )
    return profiles


def _clear_auth(profile: str, all_profiles: bool = False) -> Dict:
    ensure_data_dirs()
    cleared_profiles: List[str] = []

    if all_profiles:
        profiles_to_clear = _discover_profiles()
    else:
        profiles_to_clear = [
            {
                "profile": profile,
                "profileDir": str(get_profile_dir(profile)),
                "exists": get_profile_dir(profile).exists(),
            }
        ]

    for entry in profiles_to_clear:
        profile_dir = Path(entry["profileDir"])
        if profile_dir.exists():
            shutil.rmtree(profile_dir, ignore_errors=True)
            cleared_profiles.append(entry["profile"])

    ensure_data_dirs()
    return {
        "success": True,
        "clearedProfiles": sorted(set(cleared_profiles)),
        "allProfiles": all_profiles,
    }


def _list_profiles() -> Dict:
    return {"profiles": _discover_profiles(), "count": len(_discover_profiles())}


def _resolve_profile(raw_profile: str) -> str:
    return sanitize_profile_name(raw_profile)


def _clear_auth_legacy_compat() -> Dict:
    # Kept for safety if any external callers rely on legacy behavior.
    return _clear_auth(profile="default", all_profiles=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="NotebookLM auth management")
    subparsers = parser.add_subparsers(dest="command", required=True)

    setup_parser = subparsers.add_parser("setup", help="Open browser and perform manual Google login")
    setup_parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_AUTH_TIMEOUT_SEC,
        help=f"Max seconds to wait for login (default: {DEFAULT_AUTH_TIMEOUT_SEC})",
    )
    setup_parser.add_argument(
        "--profile",
        default="default",
        help="Profile name for auth session (default: default)",
    )

    status_parser = subparsers.add_parser("status", help="Check if auth profile appears valid")
    status_parser.add_argument(
        "--profile",
        default="default",
        help="Profile name for auth session (default: default)",
    )

    clear_parser = subparsers.add_parser("clear", help="Clear local browser auth profile")
    clear_parser.add_argument(
        "--profile",
        default="default",
        help="Profile name for auth session (default: default)",
    )
    clear_parser.add_argument(
        "--all-profiles",
        action="store_true",
        help="Clear all known profiles",
    )

    subparsers.add_parser("profiles", help="List auth profiles")

    reauth_parser = subparsers.add_parser("reauth", help="Clear auth profile and run setup")
    reauth_parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_AUTH_TIMEOUT_SEC,
        help=f"Max seconds to wait for login (default: {DEFAULT_AUTH_TIMEOUT_SEC})",
    )
    reauth_parser.add_argument(
        "--profile",
        default="default",
        help="Profile name for auth session (default: default)",
    )

    args = parser.parse_args()

    try:
        if args.command == "setup":
            profile = _resolve_profile(args.profile)
            result = _setup_auth(args.timeout, profile)
        elif args.command == "status":
            profile = _resolve_profile(args.profile)
            result = _auth_status(profile)
        elif args.command == "clear":
            profile = _resolve_profile(args.profile)
            result = _clear_auth(profile=profile, all_profiles=bool(args.all_profiles))
        elif args.command == "profiles":
            result = _list_profiles()
        elif args.command == "reauth":
            profile = _resolve_profile(args.profile)
            _clear_auth(profile=profile, all_profiles=False)
            result = _setup_auth(args.timeout, profile)
        else:
            result = {"error": f"Unknown command: {args.command}"}
    except Exception as exc:  # noqa: BLE001
        result = {"error": str(exc)}

    print(json.dumps(result, indent=2))
    if isinstance(result, dict) and result.get("error"):
        sys.exit(1)


if __name__ == "__main__":
    main()
