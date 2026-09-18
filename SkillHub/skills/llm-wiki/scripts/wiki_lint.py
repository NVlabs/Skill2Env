#!/usr/bin/env python3
"""
wiki_lint.py — Structural health check for an LLM Wiki.

Reports orphan pages, broken wikilinks, oversized pages, frontmatter issues,
stale pages, duplicate slugs, and (with --suggest-pages) terms that appear in
many pages without their own page.

Conservative by design: reports findings, never edits.

Usage:
    python wiki_lint.py [<wiki-dir>] [options]

Options:
    --soft-cap N        Page-size soft cap in lines (default: 400)
    --hard-cap N        Page-size hard cap in lines (default: 800)
    --required-fm a,b   Required frontmatter fields (default: type,title,tags,created,updated)
    --suggest-pages     Surface terms appearing in many pages without a page
    --suggest-min N     Minimum occurrences for --suggest-pages (default: 5)
    --json              Emit JSON instead of text

Examples:
    python wiki_lint.py wiki/
    python wiki_lint.py wiki/ --suggest-pages
    python wiki_lint.py wiki/ --json > lint.json
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path


WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
CAPITALIZED_PHRASE_RE = re.compile(r"\b([A-Z][a-zA-Z0-9]+(?:\s+[A-Z][a-zA-Z0-9]+){0,3})\b")


SKIP_TOP_LEVEL_FILES = {"SCHEMA.md", "index.md", "log.md", "README.md"}
SKIP_TOP_LEVEL_DIRS = {"indexes", "graph"}


def parse_frontmatter(text: str) -> tuple[dict, str, bool]:
    """Returns (metadata, body, malformed). malformed=True if frontmatter was attempted but unparseable."""
    if not text.startswith("---"):
        return {}, text, False
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text, True
    fm_text = m.group(1)
    body = text[m.end():]
    meta = {}
    current_key = None
    for line in fm_text.split("\n"):
        if not line.strip():
            continue
        kv = re.match(r"^([a-zA-Z_]+):\s*(.*)$", line)
        if kv:
            key, value = kv.group(1), kv.group(2).strip()
            if value.startswith("[") and value.endswith("]"):
                items = [x.strip().strip('"').strip("'") for x in value[1:-1].split(",") if x.strip()]
                meta[key] = items
            elif value:
                meta[key] = value.strip('"').strip("'")
            else:
                meta[key] = []
                current_key = key
        elif line.startswith("  - ") and current_key:
            meta[current_key].append(line[4:].strip().strip('"').strip("'"))
    return meta, body, False


def collect_pages(wiki_root: Path) -> list[dict]:
    pages = []
    for md_path in wiki_root.rglob("*.md"):
        rel = md_path.relative_to(wiki_root)
        if rel.parts[0] in SKIP_TOP_LEVEL_FILES or rel.parts[0] in SKIP_TOP_LEVEL_DIRS:
            continue
        if rel.name.startswith("."):
            continue
        try:
            text = md_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as e:
            pages.append({
                "path": str(md_path),
                "rel_path": str(rel),
                "slug": md_path.stem,
                "read_error": str(e),
            })
            continue
        meta, body, malformed = parse_frontmatter(text)
        line_count = text.count("\n") + 1
        links = [m.group(1).strip() for m in WIKILINK_RE.finditer(body)]
        pages.append({
            "path": str(md_path),
            "rel_path": str(rel),
            "slug": md_path.stem,
            "meta": meta,
            "body": body,
            "line_count": line_count,
            "links": links,
            "malformed_fm": malformed,
        })
    return pages


def parse_date(s):
    if not s or not isinstance(s, str):
        return None
    try:
        return datetime.strptime(s[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def lint(pages: list[dict], soft_cap: int, hard_cap: int, required_fm: list[str], suggest_pages: bool, suggest_min: int) -> dict:
    findings = {
        "orphans": [],
        "broken_links": [],
        "oversized_hard": [],
        "oversized_soft": [],
        "missing_frontmatter": [],
        "malformed_frontmatter": [],
        "duplicate_slugs": [],
        "stale_pages": [],
        "read_errors": [],
        "suggested_pages": [],
        "summary": {},
    }

    # Read errors
    for p in pages:
        if "read_error" in p:
            findings["read_errors"].append({"path": p["rel_path"], "error": p["read_error"]})

    pages = [p for p in pages if "read_error" not in p]

    # Slugs
    slug_to_pages = defaultdict(list)
    for p in pages:
        slug_to_pages[p["slug"]].append(p["rel_path"])
    for slug, paths in slug_to_pages.items():
        if len(paths) > 1:
            findings["duplicate_slugs"].append({"slug": slug, "paths": paths})

    # Inbound link map
    inbound = defaultdict(set)
    all_slugs = set(slug_to_pages.keys())
    for p in pages:
        for link in p["links"]:
            inbound[link].add(p["slug"])

    # Orphans, broken links, oversize, frontmatter, staleness
    for p in pages:
        # Orphans
        if not inbound.get(p["slug"]):
            findings["orphans"].append({"slug": p["slug"], "path": p["rel_path"]})

        # Broken links
        for link in p["links"]:
            if link not in all_slugs:
                findings["broken_links"].append({
                    "from": p["slug"],
                    "from_path": p["rel_path"],
                    "to": link,
                })

        # Oversize
        if p["line_count"] > hard_cap:
            findings["oversized_hard"].append({"path": p["rel_path"], "lines": p["line_count"]})
        elif p["line_count"] > soft_cap:
            findings["oversized_soft"].append({"path": p["rel_path"], "lines": p["line_count"]})

        # Frontmatter
        if p["malformed_fm"]:
            findings["malformed_frontmatter"].append({"path": p["rel_path"]})
        else:
            missing = [field for field in required_fm if field not in p["meta"] or p["meta"].get(field) in ("", None, [])]
            if missing:
                findings["missing_frontmatter"].append({"path": p["rel_path"], "missing": missing})

        # Staleness: heuristic — page hasn't been updated in 90 days AND has been touched by recent ingests.
        # Approximate: if updated > 90d ago and the page is well-linked (a hub), flag it.
        updated = parse_date(p["meta"].get("updated"))
        if updated:
            age_days = (date.today() - updated).days
            if age_days > 90 and len(inbound.get(p["slug"], [])) >= 3:
                findings["stale_pages"].append({
                    "path": p["rel_path"],
                    "updated": p["meta"].get("updated"),
                    "age_days": age_days,
                    "inbound_count": len(inbound.get(p["slug"], [])),
                })

    # Suggested pages: capitalized multi-word phrases appearing in many pages without a page
    if suggest_pages:
        phrase_pages = defaultdict(set)
        for p in pages:
            seen = set()
            for m in CAPITALIZED_PHRASE_RE.finditer(p["body"]):
                phrase = m.group(1).strip()
                seen.add(phrase)
            for phrase in seen:
                phrase_pages[phrase].add(p["slug"])

        # Title set for filtering
        existing_titles = {p["meta"].get("title", "").lower() for p in pages}
        existing_slugs_normalized = {s.lower().replace("-", " ") for s in all_slugs}

        candidates = []
        for phrase, page_set in phrase_pages.items():
            if len(page_set) < suggest_min:
                continue
            if phrase.lower() in existing_titles:
                continue
            if phrase.lower() in existing_slugs_normalized:
                continue
            # Filter out section header garbage
            if phrase.split()[0] in {"Section", "Where", "Sources", "Tags", "Type", "Title"}:
                continue
            candidates.append({"phrase": phrase, "page_count": len(page_set), "pages": sorted(page_set)[:5]})
        candidates.sort(key=lambda x: -x["page_count"])
        findings["suggested_pages"] = candidates[:30]

    findings["summary"] = {
        "total_pages": len(pages),
        "orphans": len(findings["orphans"]),
        "broken_links": len(findings["broken_links"]),
        "oversized_hard": len(findings["oversized_hard"]),
        "oversized_soft": len(findings["oversized_soft"]),
        "missing_frontmatter": len(findings["missing_frontmatter"]),
        "malformed_frontmatter": len(findings["malformed_frontmatter"]),
        "duplicate_slugs": len(findings["duplicate_slugs"]),
        "stale_pages": len(findings["stale_pages"]),
        "read_errors": len(findings["read_errors"]),
        "suggested_pages": len(findings["suggested_pages"]),
    }
    return findings


def render_text(findings: dict) -> str:
    out = []
    s = findings["summary"]
    out.append("=" * 60)
    out.append("Wiki Lint Report")
    out.append("=" * 60)
    out.append(f"Total pages scanned: {s['total_pages']}")
    out.append("")

    sections = [
        ("orphans", "Orphan pages (no inbound links)", lambda f: f"  - {f['slug']}  ({f['path']})"),
        ("broken_links", "Broken wikilinks", lambda f: f"  - [[{f['to']}]] referenced from {f['from_path']}"),
        ("oversized_hard", "OVERSIZE (over hard cap — must split)", lambda f: f"  - {f['path']}  ({f['lines']} lines)"),
        ("oversized_soft", "Oversize (over soft cap — consider splitting)", lambda f: f"  - {f['path']}  ({f['lines']} lines)"),
        ("missing_frontmatter", "Missing frontmatter fields", lambda f: f"  - {f['path']}  missing: {', '.join(f['missing'])}"),
        ("malformed_frontmatter", "Malformed frontmatter", lambda f: f"  - {f['path']}"),
        ("duplicate_slugs", "Duplicate slugs", lambda f: f"  - {f['slug']}: {', '.join(f['paths'])}"),
        ("stale_pages", "Stale pages (well-linked but not updated in 90+ days)", lambda f: f"  - {f['path']}  (updated {f['updated']}, {f['age_days']}d ago, {f['inbound_count']} inbound)"),
        ("read_errors", "Read errors", lambda f: f"  - {f['path']}: {f['error']}"),
    ]

    for key, label, formatter in sections:
        items = findings[key]
        if not items:
            continue
        out.append(f"{label} ({len(items)}):")
        for item in items[:50]:
            out.append(formatter(item))
        if len(items) > 50:
            out.append(f"  ... and {len(items) - 50} more")
        out.append("")

    if findings["suggested_pages"]:
        out.append(f"Suggested page candidates ({len(findings['suggested_pages'])}):")
        out.append("  Phrases appearing in many pages without a dedicated page:")
        for item in findings["suggested_pages"]:
            out.append(f"  - \"{item['phrase']}\"  ({item['page_count']} pages)")
        out.append("")

    if all(v == 0 for k, v in s.items() if k != "total_pages"):
        out.append("No issues found. Wiki is healthy.")

    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("wiki", nargs="?", type=Path, default=Path("wiki"), help="Wiki directory (default: ./wiki).")
    parser.add_argument("--soft-cap", type=int, default=400, help="Page-size soft cap (lines).")
    parser.add_argument("--hard-cap", type=int, default=800, help="Page-size hard cap (lines).")
    parser.add_argument("--required-fm", default="type,title,tags,created,updated", help="Required frontmatter fields, comma-separated.")
    parser.add_argument("--suggest-pages", action="store_true", help="Surface page candidates.")
    parser.add_argument("--suggest-min", type=int, default=5, help="Minimum page count for suggestions.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args()

    if not args.wiki.exists():
        print(f"Wiki directory not found: {args.wiki}", file=sys.stderr)
        sys.exit(1)

    pages = collect_pages(args.wiki)
    required_fm = [f.strip() for f in args.required_fm.split(",") if f.strip()]
    findings = lint(pages, args.soft_cap, args.hard_cap, required_fm, args.suggest_pages, args.suggest_min)

    if args.json:
        print(json.dumps(findings, indent=2, default=str))
    else:
        print(render_text(findings))


if __name__ == "__main__":
    main()
