#!/usr/bin/env python3
"""
init_wiki.py — Bootstrap or upgrade an LLM Wiki structure in a project.

Plain init creates the directory layout and drops in templates for SCHEMA.md,
index.md, log.md, the page template, and the optional graph layer
(graph/ontology.yaml, graph/README.md, graph/.gitignore). It is idempotent:
re-running won't clobber existing files.

`--upgrade` mode is for wikis bootstrapped under an older plugin version. It
does the same idempotent file creation, then inspects the existing SCHEMA.md
for sections introduced in newer versions and prints clear instructions for
what to merge by hand. It never overwrites SCHEMA.md — the schema is
co-evolved with the user.

Usage:
    python init_wiki.py <project-root> [--wiki-dir wiki] [--raw-dir raw] [--upgrade]

Examples:
    python init_wiki.py .
    python init_wiki.py . --upgrade
    python init_wiki.py ~/research --wiki-dir kb --raw-dir sources
"""

import argparse
import sys
from pathlib import Path
from datetime import date


SKILL_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = SKILL_ROOT / "assets"


SUBDIRS = ["sources", "entities", "concepts", "synthesis", "graph"]

# Markers used by --upgrade to detect SCHEMA.md sections introduced in
# specific plugin versions. Each entry: (heading_marker, version_label,
# template_anchor, blurb).
SCHEMA_SECTION_MARKERS = [
    {
        "marker": "## Optional graph metadata",
        "version": "0.3.0",
        "anchor": "## Optional graph metadata",
        "label": "Optional graph metadata (Frontmatter section)",
    },
    {
        "marker": "## Graph layer",
        "version": "0.3.0",
        "anchor": "## Graph layer",
        "label": "Graph layer (canonical-vs-generated artifact policy)",
    },
    {
        "marker": "Graph lint + extract",
        "version": "0.3.0",
        "anchor": "- Graph lint + extract: after every ingest that adds typed `graph.relationships`.",
        "label": "Graph lint + extract cadence (Lint cadence section)",
    },
]


def copy_template(src: Path, dst: Path, substitutions: dict | None = None) -> bool:
    """Copy a template file to dst. Returns True if file was created, False if it already existed."""
    if dst.exists():
        return False
    text = src.read_text()
    if substitutions:
        for key, value in substitutions.items():
            text = text.replace(key, value)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text)
    return True


def detect_schema_gaps(schema_path: Path) -> list[dict]:
    """Return the SCHEMA_SECTION_MARKERS entries missing from the user's SCHEMA.md."""
    if not schema_path.exists():
        return []
    text = schema_path.read_text(encoding="utf-8")
    return [m for m in SCHEMA_SECTION_MARKERS if m["marker"] not in text]


def print_schema_upgrade_guidance(schema_path: Path, gaps: list[dict]) -> None:
    template_path = TEMPLATES / "SCHEMA.md.template"
    print()
    print("=" * 64)
    print(f"Upgrade required: {schema_path}")
    print("=" * 64)
    print(
        "Your SCHEMA.md predates one or more sections introduced by newer\n"
        "plugin versions. The graph layer itself is opt-in, but to make Claude\n"
        "aware of it, merge the sections below by hand. SCHEMA.md is co-evolved\n"
        "with you — this script never overwrites it."
    )
    print()
    print("Missing sections:")
    for m in gaps:
        print(f"  - [{m['version']}] {m['label']}")
    print()
    print(f"Reference template: {template_path}")
    print(
        "Diff your SCHEMA.md against the template and copy the missing\n"
        "sections in. Or run /wiki:upgrade and Claude will propose the edits\n"
        "interactively (one section at a time, never silent)."
    )


def init_wiki(project_root: Path, wiki_dir: str, raw_dir: str, upgrade: bool = False) -> None:
    project_root = project_root.resolve()
    if not project_root.exists():
        print(f"Error: project root does not exist: {project_root}", file=sys.stderr)
        sys.exit(1)

    wiki = project_root / wiki_dir
    raw = project_root / raw_dir

    mode = "Upgrading" if upgrade else "Initializing"
    print(f"{mode} LLM Wiki in: {project_root}")
    print(f"  Wiki directory: {wiki}")
    print(f"  Raw directory:  {raw}")
    print()

    created = []
    skipped = []

    # Create wiki subdirs
    for subdir in SUBDIRS:
        d = wiki / subdir
        if not d.exists():
            d.mkdir(parents=True)
            created.append(f"{wiki_dir}/{subdir}/")
        else:
            skipped.append(f"{wiki_dir}/{subdir}/")

    # Create raw + raw/assets
    for d, label in [(raw, raw_dir), (raw / "assets", f"{raw_dir}/assets")]:
        if not d.exists():
            d.mkdir(parents=True)
            created.append(f"{label}/")
        else:
            skipped.append(f"{label}/")

    # Copy templates
    template_map = [
        ("SCHEMA.md.template", wiki / "SCHEMA.md"),
        ("index.md.template", wiki / "index.md"),
        ("log.md.template", wiki / "log.md"),
        ("page.md.template", wiki / ".page-template.md"),
        ("ontology.yaml.template", wiki / "graph" / "ontology.yaml"),
        ("graph_README.md.template", wiki / "graph" / "README.md"),
        ("graph_gitignore.template", wiki / "graph" / ".gitignore"),
    ]
    for src_name, dst in template_map:
        src = TEMPLATES / src_name
        if not src.exists():
            print(f"Warning: template missing: {src}", file=sys.stderr)
            continue
        if copy_template(src, dst):
            created.append(str(dst.relative_to(project_root)))
        else:
            skipped.append(str(dst.relative_to(project_root)))

    # Report
    if created:
        print("Created:")
        for path in created:
            print(f"  + {path}")
    if skipped:
        print("Already existed (skipped):")
        for path in skipped:
            print(f"  = {path}")

    if upgrade:
        gaps = detect_schema_gaps(wiki / "SCHEMA.md")
        if gaps:
            print_schema_upgrade_guidance(wiki / "SCHEMA.md", gaps)
        else:
            print()
            print("SCHEMA.md is up to date with the current template — no manual merge needed.")
        return

    print()
    print("Next steps:")
    print(f"  1. Read {wiki_dir}/SCHEMA.md and customize it for your domain.")
    print(f"  2. (Optional) Edit {wiki_dir}/graph/ontology.yaml to add domain-specific predicates.")
    print(f"  3. Drop your first source into {raw_dir}/.")
    print(f"  4. Ask Claude to ingest it.")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("project_root", type=Path, help="Project root directory.")
    parser.add_argument("--wiki-dir", default="wiki", help="Name of the wiki subdirectory (default: wiki).")
    parser.add_argument("--raw-dir", default="raw", help="Name of the raw sources subdirectory (default: raw).")
    parser.add_argument("--upgrade", action="store_true",
                        help="Upgrade an existing wiki: add missing files idempotently and surface SCHEMA.md sections to merge by hand.")
    args = parser.parse_args()
    init_wiki(args.project_root, args.wiki_dir, args.raw_dir, upgrade=args.upgrade)


if __name__ == "__main__":
    main()
