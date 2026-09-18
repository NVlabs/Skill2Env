#!/usr/bin/env python3
"""
wiki_graph_extract.py — Compile the markdown wiki into a queryable graph.

Markdown remains canonical. This script reads every wiki page, derives nodes
and edges (typed semantic edges from `graph.relationships`, plus implicit
`mentions`, `sourced_from`, `summarizes_raw` edges), and emits artifacts under
`<wiki>/graph/` that can be deleted and rebuilt at any time.

Requires PyYAML (`pip install pyyaml`) — the new graph layer uses real YAML
parsing for its nested frontmatter, unlike the stdlib-only lint/search/stats
scripts.

Usage:
    python wiki_graph_extract.py <wiki-dir> [options]

Options:
    --out <dir>                  Output directory (default: <wiki-dir>/graph)
    --formats jsonl,sqlite,...   Comma-list of formats to emit
                                 (jsonl, sqlite, graphml; default: all three)
    --ontology <path>            Override ontology path
                                 (default: <wiki-dir>/graph/ontology.yaml)

Examples:
    python wiki_graph_extract.py wiki/
    python wiki_graph_extract.py wiki/ --out wiki/graph --formats jsonl,sqlite
"""

import argparse
import hashlib
import json
import re
import sqlite3
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:
    print(
        "wiki_graph_extract.py requires PyYAML.\n"
        "Install with:  pip install pyyaml",
        file=sys.stderr,
    )
    sys.exit(2)


WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

SKIP_TOP_LEVEL_FILES = {"SCHEMA.md", "index.md", "log.md", "README.md"}
SKIP_TOP_LEVEL_DIRS = {"indexes", "graph"}

DEFAULT_FORMATS = ["jsonl", "sqlite", "graphml"]


# ---------------------------------------------------------------------------
# Page collection
# ---------------------------------------------------------------------------


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Extract YAML frontmatter using PyYAML. Returns (meta, body)."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    fm_text = m.group(1)
    body = text[m.end():]
    try:
        meta = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        meta = {}
    if not isinstance(meta, dict):
        meta = {}
    return meta, body


def collect_pages(wiki_root: Path) -> list[dict]:
    pages = []
    for md_path in sorted(wiki_root.rglob("*.md")):
        rel = md_path.relative_to(wiki_root)
        if rel.parts[0] in SKIP_TOP_LEVEL_FILES or rel.parts[0] in SKIP_TOP_LEVEL_DIRS:
            continue
        if rel.name.startswith("."):
            continue
        try:
            text = md_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        meta, body = parse_frontmatter(text)
        links = [m.group(1).strip() for m in WIKILINK_RE.finditer(body)]
        pages.append({
            "path": str(md_path),
            "rel_path": str(rel).replace("\\", "/"),
            "slug": md_path.stem,
            "meta": meta,
            "body": body,
            "links": links,
        })
    return pages


# ---------------------------------------------------------------------------
# Ontology
# ---------------------------------------------------------------------------


def load_ontology(path: Path) -> dict:
    if not path.exists():
        return {"node_types": {}, "predicates": {}}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        print(f"Ontology parse error ({path}): {e}", file=sys.stderr)
        sys.exit(2)
    data.setdefault("node_types", {})
    data.setdefault("predicates", {})
    return data


def derive_node_type(meta: dict, ontology: dict) -> str | None:
    """Map a page's frontmatter to a node_type using ontology[node_types][*].maps_from."""
    page_type = meta.get("type")
    page_kind = meta.get("kind")
    explicit = (meta.get("graph") or {}).get("node_type") if isinstance(meta.get("graph"), dict) else None
    if explicit:
        return explicit
    # Try (type, kind) match first, then type-only.
    type_kind_match = None
    type_only_match = None
    for nt_name, nt_def in ontology["node_types"].items():
        maps = (nt_def or {}).get("maps_from") or {}
        m_type = maps.get("type")
        m_kind = maps.get("kind")
        if m_type and m_type == page_type:
            if m_kind and m_kind == page_kind:
                type_kind_match = nt_name
                break
            if not m_kind and type_only_match is None:
                type_only_match = nt_name
    return type_kind_match or type_only_match


# ---------------------------------------------------------------------------
# Node + edge construction
# ---------------------------------------------------------------------------


def build_nodes(pages: list[dict], ontology: dict) -> tuple[list[dict], dict, list[dict]]:
    """Build the node list + slug→node_id index + alias rows. Returns (nodes, slug_to_id, aliases)."""
    nodes: list[dict] = []
    slug_to_id: dict[str, str] = {}
    aliases: list[dict] = []
    seen_ids: set[str] = set()

    for p in pages:
        meta = p["meta"]
        graph_meta = meta.get("graph") if isinstance(meta.get("graph"), dict) else {}
        node_type = derive_node_type(meta, ontology) or "concept"
        explicit_id = graph_meta.get("node_id")
        node_id = explicit_id or f"{node_type}:{p['slug']}"

        # Skip duplicates — first one wins; lint will flag this.
        if node_id in seen_ids:
            continue
        seen_ids.add(node_id)

        node = {
            "id": node_id,
            "slug": p["slug"],
            "title": meta.get("title") or p["slug"],
            "page_type": meta.get("type") or "",
            "node_type": node_type,
            "kind": meta.get("kind") or "",
            "tags": list(meta.get("tags") or []),
            "aliases": list(graph_meta.get("aliases") or []),
            "path": p["rel_path"],
            "created": meta.get("created") or "",
            "updated": meta.get("updated") or "",
            "canonical": bool(graph_meta.get("canonical", False)),
        }
        nodes.append(node)
        slug_to_id[p["slug"]] = node_id
        for alias in node["aliases"]:
            aliases.append({"alias": str(alias), "node_id": node_id})

    return nodes, slug_to_id, aliases


def edge_id(subject: str, predicate: str, obj: str, source: str | None, evidence: str | None) -> str:
    # Truncated to 96 bits — collision risk is negligible at any plausible
    # wiki scale and shorter ids keep the JSONL/sqlite/graphml outputs readable.
    h = hashlib.sha256()
    parts = [subject or "", predicate or "", obj or "", source or "", evidence or ""]
    h.update("\x1f".join(parts).encode("utf-8"))
    return h.hexdigest()[:24]


def make_edge(*, subject, predicate, obj, source, evidence, confidence, status,
              extraction_method, page, extras: dict | None = None) -> dict:
    return {
        "id": edge_id(subject, predicate, obj, source, evidence),
        "subject": subject,
        "predicate": predicate,
        "object": obj,
        "source": source or "",
        "evidence": evidence or "",
        "confidence": confidence or "",
        "status": status or "",
        "extraction_method": extraction_method,
        "page": page,
        "extras": extras or {},
    }


def build_edges(pages: list[dict], slug_to_id: dict[str, str]) -> list[dict]:
    edges: list[dict] = []
    seen_ids: set[str] = set()

    def push(edge: dict) -> None:
        if edge["id"] in seen_ids:
            return
        seen_ids.add(edge["id"])
        edges.append(edge)

    for p in pages:
        slug = p["slug"]
        subject_id = slug_to_id.get(slug)
        if not subject_id:
            continue
        meta = p["meta"]
        graph_meta = meta.get("graph") if isinstance(meta.get("graph"), dict) else {}

        # 1. Typed semantic edges from graph.relationships[].
        for rel in graph_meta.get("relationships") or []:
            if not isinstance(rel, dict):
                continue
            obj = rel.get("object")
            predicate = rel.get("predicate")
            if not (obj and predicate):
                continue
            extras = {
                k: rel[k] for k in ("valid_from", "valid_to", "notes", "raw_ref",
                                    "contradicts", "supersedes")
                if k in rel and rel[k] is not None
            }
            push(make_edge(
                subject=subject_id,
                predicate=str(predicate),
                obj=str(obj),
                source=rel.get("source"),
                evidence=rel.get("evidence"),
                confidence=rel.get("confidence"),
                status=rel.get("status"),
                extraction_method="explicit_graph_frontmatter",
                page=p["rel_path"],
                extras=extras,
            ))

        # 2. Mentions edges from body wikilinks.
        seen_targets: set[str] = set()
        for link in p["links"]:
            target_slug = link.split("#")[0].strip()
            if not target_slug or target_slug == slug:
                continue
            target_id = slug_to_id.get(target_slug)
            if not target_id or target_id in seen_targets:
                continue
            seen_targets.add(target_id)
            push(make_edge(
                subject=subject_id,
                predicate="mentions",
                obj=target_id,
                source=None,
                evidence=None,
                confidence="low",
                status="current",
                extraction_method="body_wikilink",
                page=p["rel_path"],
            ))

        # 3. sourced_from edges from frontmatter `sources:` (skip on source pages themselves).
        if meta.get("type") != "source":
            for src_slug in meta.get("sources") or []:
                src_id = slug_to_id.get(str(src_slug))
                if not src_id:
                    continue
                push(make_edge(
                    subject=subject_id,
                    predicate="sourced_from",
                    obj=src_id,
                    source=str(src_slug),
                    evidence=None,
                    confidence="high",
                    status="current",
                    extraction_method="frontmatter_sources",
                    page=p["rel_path"],
                ))

        # 4. summarizes_raw edges from source pages' raw: field.
        if meta.get("type") == "source":
            raw_path = meta.get("raw")
            if raw_path:
                push(make_edge(
                    subject=subject_id,
                    predicate="summarizes_raw",
                    obj=f"raw:{raw_path}",
                    source=None,
                    evidence=None,
                    confidence="high",
                    status="current",
                    extraction_method="frontmatter_raw",
                    page=p["rel_path"],
                ))

    return edges


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------


def _normalize_for_json(value):
    if hasattr(value, "isoformat"):
        return value.isoformat()
    if isinstance(value, list):
        return [_normalize_for_json(v) for v in value]
    if isinstance(value, dict):
        return {k: _normalize_for_json(v) for k, v in value.items()}
    return value


def write_jsonl(out_dir: Path, nodes: list[dict], edges: list[dict]) -> None:
    nodes_sorted = sorted(nodes, key=lambda n: n["id"])
    edges_sorted = sorted(edges, key=lambda e: e["id"])
    with (out_dir / "nodes.jsonl").open("w", encoding="utf-8") as f:
        for n in nodes_sorted:
            f.write(json.dumps(_normalize_for_json(n), sort_keys=True, ensure_ascii=False))
            f.write("\n")
    with (out_dir / "edges.jsonl").open("w", encoding="utf-8") as f:
        for e in edges_sorted:
            f.write(json.dumps(_normalize_for_json(e), sort_keys=True, ensure_ascii=False))
            f.write("\n")


def write_sqlite(out_dir: Path, nodes: list[dict], aliases: list[dict], edges: list[dict]) -> None:
    db_path = out_dir / "graph.sqlite"
    if db_path.exists():
        db_path.unlink()
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript("""
            CREATE TABLE nodes (
              id TEXT PRIMARY KEY,
              slug TEXT NOT NULL UNIQUE,
              title TEXT NOT NULL,
              page_type TEXT NOT NULL,
              node_type TEXT NOT NULL,
              kind TEXT,
              path TEXT NOT NULL,
              created TEXT,
              updated TEXT,
              metadata_json TEXT NOT NULL
            );
            CREATE TABLE aliases (
              alias TEXT NOT NULL,
              node_id TEXT NOT NULL,
              PRIMARY KEY (alias, node_id),
              FOREIGN KEY (node_id) REFERENCES nodes(id)
            );
            CREATE TABLE edges (
              id TEXT PRIMARY KEY,
              subject TEXT NOT NULL,
              predicate TEXT NOT NULL,
              object TEXT NOT NULL,
              source TEXT,
              evidence TEXT,
              confidence TEXT,
              status TEXT,
              extraction_method TEXT NOT NULL,
              page TEXT NOT NULL,
              metadata_json TEXT NOT NULL
            );
            CREATE INDEX idx_edges_subject ON edges(subject);
            CREATE INDEX idx_edges_object ON edges(object);
            CREATE INDEX idx_edges_predicate ON edges(predicate);
            CREATE INDEX idx_edges_source ON edges(source);
        """)

        for n in sorted(nodes, key=lambda n: n["id"]):
            metadata_json = json.dumps(_normalize_for_json({
                "tags": n.get("tags", []),
                "aliases": n.get("aliases", []),
                "canonical": n.get("canonical", False),
            }), sort_keys=True, ensure_ascii=False)
            conn.execute(
                "INSERT INTO nodes (id, slug, title, page_type, node_type, kind, path, created, updated, metadata_json) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    n["id"], n["slug"], n["title"], n["page_type"], n["node_type"],
                    n.get("kind") or None, n["path"],
                    str(n.get("created") or "") or None,
                    str(n.get("updated") or "") or None,
                    metadata_json,
                ),
            )

        for a in sorted(aliases, key=lambda a: (a["alias"], a["node_id"])):
            conn.execute(
                "INSERT OR IGNORE INTO aliases (alias, node_id) VALUES (?, ?)",
                (a["alias"], a["node_id"]),
            )

        for e in sorted(edges, key=lambda e: e["id"]):
            metadata_json = json.dumps(_normalize_for_json(e.get("extras") or {}),
                                       sort_keys=True, ensure_ascii=False)
            conn.execute(
                "INSERT INTO edges (id, subject, predicate, object, source, evidence, "
                "confidence, status, extraction_method, page, metadata_json) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    e["id"], e["subject"], e["predicate"], e["object"],
                    e.get("source") or None, e.get("evidence") or None,
                    e.get("confidence") or None, e.get("status") or None,
                    e["extraction_method"], e["page"], metadata_json,
                ),
            )
        conn.commit()
    finally:
        conn.close()


def write_graphml(out_dir: Path, nodes: list[dict], edges: list[dict]) -> None:
    ns = "http://graphml.graphdrawing.org/xmlns"
    ET.register_namespace("", ns)
    root = ET.Element(f"{{{ns}}}graphml")

    keys = [
        ("d_title", "node", "title", "string"),
        ("d_node_type", "node", "node_type", "string"),
        ("d_page_type", "node", "page_type", "string"),
        ("d_path", "node", "path", "string"),
        ("d_predicate", "edge", "predicate", "string"),
        ("d_confidence", "edge", "confidence", "string"),
        ("d_status", "edge", "status", "string"),
        ("d_source", "edge", "source", "string"),
    ]
    for kid, kfor, kname, ktype in keys:
        k = ET.SubElement(root, f"{{{ns}}}key")
        k.set("id", kid)
        k.set("for", kfor)
        k.set("attr.name", kname)
        k.set("attr.type", ktype)

    graph = ET.SubElement(root, f"{{{ns}}}graph")
    graph.set("id", "wiki")
    graph.set("edgedefault", "directed")

    for n in sorted(nodes, key=lambda n: n["id"]):
        node_el = ET.SubElement(graph, f"{{{ns}}}node")
        node_el.set("id", n["id"])
        for kid, kfor, kname, _ in keys:
            if kfor != "node":
                continue
            data = ET.SubElement(node_el, f"{{{ns}}}data")
            data.set("key", kid)
            data.text = str(n.get(kname) or "")

    for e in sorted(edges, key=lambda e: e["id"]):
        edge_el = ET.SubElement(graph, f"{{{ns}}}edge")
        edge_el.set("id", e["id"])
        edge_el.set("source", e["subject"])
        edge_el.set("target", e["object"])
        for kid, kfor, kname, _ in keys:
            if kfor != "edge":
                continue
            data = ET.SubElement(edge_el, f"{{{ns}}}data")
            data.set("key", kid)
            data.text = str(e.get(kname) or "")

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(out_dir / "graph.graphml", encoding="utf-8", xml_declaration=True)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("wiki", type=Path, help="Wiki directory.")
    parser.add_argument("--out", type=Path, help="Output directory (default: <wiki>/graph)")
    parser.add_argument("--formats", default=",".join(DEFAULT_FORMATS),
                        help="Comma-list: jsonl, sqlite, graphml")
    parser.add_argument("--ontology", type=Path, help="Ontology file (default: <wiki>/graph/ontology.yaml)")
    args = parser.parse_args()

    if not args.wiki.exists():
        print(f"Wiki directory not found: {args.wiki}", file=sys.stderr)
        sys.exit(1)

    out_dir = args.out or (args.wiki / "graph")
    out_dir.mkdir(parents=True, exist_ok=True)
    ontology_path = args.ontology or (args.wiki / "graph" / "ontology.yaml")
    ontology = load_ontology(ontology_path)
    formats = [f.strip().lower() for f in args.formats.split(",") if f.strip()]
    unknown = [f for f in formats if f not in DEFAULT_FORMATS]
    if unknown:
        print(f"Unknown formats: {unknown}. Allowed: {DEFAULT_FORMATS}", file=sys.stderr)
        sys.exit(1)

    pages = collect_pages(args.wiki)
    nodes, slug_to_id, aliases = build_nodes(pages, ontology)
    edges = build_edges(pages, slug_to_id)

    if "jsonl" in formats:
        write_jsonl(out_dir, nodes, edges)
    if "sqlite" in formats:
        write_sqlite(out_dir, nodes, aliases, edges)
    if "graphml" in formats:
        write_graphml(out_dir, nodes, edges)

    print(f"Extracted {len(nodes)} nodes, {len(edges)} edges → {out_dir}")
    breakdown = defaultdict(int)
    for e in edges:
        breakdown[e["predicate"]] += 1
    for pred, count in sorted(breakdown.items(), key=lambda x: (-x[1], x[0])):
        print(f"  {pred:20s} {count}")


if __name__ == "__main__":
    main()
