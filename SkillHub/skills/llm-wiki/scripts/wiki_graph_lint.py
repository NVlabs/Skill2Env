#!/usr/bin/env python3
"""
wiki_graph_lint.py — Validate the typed graph metadata in a wiki.

Reads every page's `graph:` frontmatter, cross-checks against the ontology
(`wiki/graph/ontology.yaml`), and reports problems. Conservative by design:
reports only, never edits.

Requires PyYAML (`pip install pyyaml`).

Checks:
- Unique `graph.node_id` values across pages.
- All relationship `object` ids resolve to known nodes (or are allowed
  string-literal targets for predicates whose object_types include "*").
- All predicates exist in `graph/ontology.yaml`.
- Predicate subject/object types match ontology.
- Typed semantic edges (anything except mentions/sourced_from/summarizes_raw
  and predicates with `requires_evidence: false`) carry `source` and
  `evidence`.
- `source` references resolve to an existing source page.
- `confidence` is one of high|medium|low; `status` is one of
  current|historical|proposed|disputed|superseded.
- No duplicate canonical nodes for the same node id.
- Aliases do not collide across distinct canonical nodes.
- `contradicts` / `supersedes` references resolve to known node/edge ids.
- Generated graph has no orphan typed nodes (nodes with no inbound or
  outbound typed edges) except for `source` nodes (allowed source-only).

Usage:
    python wiki_graph_lint.py [<wiki-dir>] [--json]
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:
    print(
        "wiki_graph_lint.py requires PyYAML.\n"
        "Install with:  pip install pyyaml",
        file=sys.stderr,
    )
    sys.exit(2)

# Same module is imported by extract; we re-use its build_nodes/build_edges to
# guarantee lint sees exactly what extract would emit.
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import wiki_graph_extract as _extract  # noqa: E402


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")

SKIP_TOP_LEVEL_FILES = {"SCHEMA.md", "index.md", "log.md", "README.md"}
SKIP_TOP_LEVEL_DIRS = {"indexes", "graph"}

ALLOWED_CONFIDENCE = {"high", "medium", "low"}
ALLOWED_STATUS = {"current", "historical", "proposed", "disputed", "superseded"}
IMPLICIT_PREDICATES = {"mentions", "sourced_from", "summarizes_raw"}


def parse_frontmatter(text: str) -> tuple[dict, str]:
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
        pages.append({
            "path": str(md_path),
            "rel_path": str(rel).replace("\\", "/"),
            "slug": md_path.stem,
            "meta": meta,
            "body": body,
            "links": [m.group(1).strip() for m in WIKILINK_RE.finditer(body)],
        })
    return pages


def derive_node_type(meta: dict, ontology: dict) -> str | None:
    page_type = meta.get("type")
    page_kind = meta.get("kind")
    explicit = (meta.get("graph") or {}).get("node_type") if isinstance(meta.get("graph"), dict) else None
    if explicit:
        return explicit
    type_kind_match = None
    type_only_match = None
    for nt_name, nt_def in ontology.get("node_types", {}).items():
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


def derive_node_id(meta: dict, slug: str, ontology: dict) -> str:
    graph_meta = meta.get("graph") if isinstance(meta.get("graph"), dict) else {}
    explicit = graph_meta.get("node_id")
    if explicit:
        return str(explicit)
    node_type = derive_node_type(meta, ontology) or "concept"
    return f"{node_type}:{slug}"


def types_match(allowed: list[str] | None, actual: str | None) -> bool:
    if not allowed:
        return True
    if "*" in allowed:
        return True
    return actual in allowed


def lint(pages: list[dict], ontology: dict) -> dict:
    findings = {
        "duplicate_node_ids": [],
        "unknown_predicates": [],
        "broken_object_refs": [],
        "subject_type_mismatch": [],
        "object_type_mismatch": [],
        "missing_evidence": [],
        "missing_source_field": [],
        "broken_source_refs": [],
        "invalid_confidence": [],
        "invalid_status": [],
        "duplicate_canonical": [],
        "alias_collisions": [],
        "broken_contradicts": [],
        "broken_supersedes": [],
        "orphan_typed_nodes": [],
        "summary": {},
    }

    predicates = ontology.get("predicates", {})
    node_types = ontology.get("node_types", {})

    # Build node index
    node_by_id: dict[str, dict] = {}
    duplicates: dict[str, list[str]] = defaultdict(list)
    for p in pages:
        nid = derive_node_id(p["meta"], p["slug"], ontology)
        if nid in node_by_id:
            duplicates[nid].append(p["rel_path"])
            duplicates[nid].append(node_by_id[nid]["rel_path"])
            continue
        node_type = derive_node_type(p["meta"], ontology) or "concept"
        graph_meta = p["meta"].get("graph") if isinstance(p["meta"].get("graph"), dict) else {}
        node_by_id[nid] = {
            "id": nid,
            "node_type": node_type,
            "rel_path": p["rel_path"],
            "slug": p["slug"],
            "page_type": p["meta"].get("type"),
            "canonical": bool(graph_meta.get("canonical", False)),
            "aliases": list(graph_meta.get("aliases") or []),
            "graph": graph_meta,
        }

    for nid, paths in duplicates.items():
        findings["duplicate_node_ids"].append({"node_id": nid, "paths": sorted(set(paths))})

    # Source pages by slug — used to validate `source:` refs on edges.
    source_slugs = {p["slug"] for p in pages if p["meta"].get("type") == "source"}

    # Aliases
    alias_to_canonicals: dict[str, set[str]] = defaultdict(set)
    canonical_by_id: dict[str, list[str]] = defaultdict(list)
    for n in node_by_id.values():
        if n["canonical"]:
            canonical_by_id[n["id"]].append(n["rel_path"])
        for alias in n["aliases"]:
            alias_to_canonicals[str(alias)].add(n["id"])

    for nid, paths in canonical_by_id.items():
        if len(paths) > 1:
            findings["duplicate_canonical"].append({"node_id": nid, "paths": paths})

    for alias, owners in alias_to_canonicals.items():
        if len(owners) > 1:
            findings["alias_collisions"].append({"alias": alias, "owners": sorted(owners)})

    # Walk relationships
    for p in pages:
        graph_meta = p["meta"].get("graph") if isinstance(p["meta"].get("graph"), dict) else {}
        subject_id = derive_node_id(p["meta"], p["slug"], ontology)
        subject_type = node_by_id.get(subject_id, {}).get("node_type")

        for idx, rel in enumerate(graph_meta.get("relationships") or []):
            if not isinstance(rel, dict):
                continue
            predicate = rel.get("predicate")
            obj = rel.get("object")
            here = {"page": p["rel_path"], "predicate": predicate,
                    "object": obj, "index": idx}

            if not predicate or predicate not in predicates:
                findings["unknown_predicates"].append({**here})
                continue
            pdef = predicates[predicate] or {}

            # Object resolution. Allow string-literal objects only when
            # ontology lists "*" in object_types (e.g. summarizes_raw).
            object_types = pdef.get("object_types") or []
            allows_wildcard_obj = "*" in object_types
            if obj and obj not in node_by_id:
                if not allows_wildcard_obj:
                    findings["broken_object_refs"].append({**here})

            # Subject type check
            if not types_match(pdef.get("subject_types"), subject_type):
                findings["subject_type_mismatch"].append({
                    **here,
                    "subject": subject_id,
                    "subject_type": subject_type,
                    "allowed": pdef.get("subject_types"),
                })
            # Object type check (only if object resolves to a node)
            obj_node = node_by_id.get(obj) if obj else None
            obj_type = obj_node["node_type"] if obj_node else None
            if obj_node and not types_match(pdef.get("object_types"), obj_type):
                findings["object_type_mismatch"].append({
                    **here,
                    "object_type": obj_type,
                    "allowed": pdef.get("object_types"),
                })

            requires_evidence = pdef.get("requires_evidence", True)
            if requires_evidence:
                if not rel.get("evidence"):
                    findings["missing_evidence"].append({**here})
                if not rel.get("source"):
                    findings["missing_source_field"].append({**here})

            # source field must reference an existing source page slug
            src = rel.get("source")
            if src and str(src) not in source_slugs:
                findings["broken_source_refs"].append({**here, "source": src})

            confidence = rel.get("confidence")
            if confidence and confidence not in ALLOWED_CONFIDENCE:
                findings["invalid_confidence"].append({**here, "confidence": confidence})

            status = rel.get("status")
            if status and status not in ALLOWED_STATUS:
                findings["invalid_status"].append({**here, "status": status})

            # contradicts / supersedes resolution
            for ref_field, bucket in (("contradicts", "broken_contradicts"),
                                       ("supersedes", "broken_supersedes")):
                ref = rel.get(ref_field)
                if ref:
                    ref_str = str(ref)
                    if ref_str not in node_by_id and ref_str not in source_slugs:
                        findings[bucket].append({**here, ref_field: ref_str})

    # Orphan typed nodes — pages that declared `graph:` frontmatter but end
    # up with no typed (non-implicit) edge touching them after extraction.
    # Source nodes are exempt (they participate via implicit edges).
    extracted_edges = _extract.build_edges(pages, {n["slug"]: n["id"] for n in node_by_id.values()})
    typed_node_refs: set[str] = set()
    for e in extracted_edges:
        if e["predicate"] in IMPLICIT_PREDICATES:
            continue
        typed_node_refs.add(e["subject"])
        if e["object"] in node_by_id:
            typed_node_refs.add(e["object"])

    for n in node_by_id.values():
        if n["node_type"] == "source":
            continue
        graph_meta = n.get("graph") or {}
        if not graph_meta:
            continue  # Pages without graph metadata are valid; they're text-only nodes.
        if n["id"] in typed_node_refs:
            continue
        findings["orphan_typed_nodes"].append({
            "node_id": n["id"],
            "path": n["rel_path"],
        })

    # Summary
    findings["summary"] = {
        "pages_scanned": len(pages),
        "nodes": len(node_by_id),
        **{k: len(v) for k, v in findings.items() if isinstance(v, list)},
    }
    return findings


def render_text(findings: dict) -> str:
    out = []
    s = findings["summary"]
    out.append("=" * 60)
    out.append("Wiki Graph Lint Report")
    out.append("=" * 60)
    out.append(f"Pages scanned: {s['pages_scanned']}    Nodes: {s['nodes']}")
    out.append("")

    sections = [
        ("duplicate_node_ids", "Duplicate node ids",
         lambda f: f"  - {f['node_id']}: {', '.join(f['paths'])}"),
        ("unknown_predicates", "Unknown predicates (not in ontology)",
         lambda f: f"  - {f['page']}#rel[{f['index']}]  predicate={f['predicate']!r}"),
        ("broken_object_refs", "Broken object references",
         lambda f: f"  - {f['page']}#rel[{f['index']}]  {f['predicate']} → {f['object']!r}"),
        ("subject_type_mismatch", "Subject type does not match ontology",
         lambda f: f"  - {f['page']}#rel[{f['index']}]  {f['predicate']}: subject={f['subject_type']} (allowed: {f['allowed']})"),
        ("object_type_mismatch", "Object type does not match ontology",
         lambda f: f"  - {f['page']}#rel[{f['index']}]  {f['predicate']}: object={f['object_type']} (allowed: {f['allowed']})"),
        ("missing_evidence", "Missing evidence on typed edge",
         lambda f: f"  - {f['page']}#rel[{f['index']}]  {f['predicate']} → {f['object']}"),
        ("missing_source_field", "Missing source on typed edge",
         lambda f: f"  - {f['page']}#rel[{f['index']}]  {f['predicate']} → {f['object']}"),
        ("broken_source_refs", "source: does not match any source page",
         lambda f: f"  - {f['page']}#rel[{f['index']}]  source={f['source']!r}"),
        ("invalid_confidence", "Invalid confidence value",
         lambda f: f"  - {f['page']}#rel[{f['index']}]  confidence={f['confidence']!r}"),
        ("invalid_status", "Invalid status value",
         lambda f: f"  - {f['page']}#rel[{f['index']}]  status={f['status']!r}"),
        ("duplicate_canonical", "Duplicate canonical nodes",
         lambda f: f"  - {f['node_id']}: {', '.join(f['paths'])}"),
        ("alias_collisions", "Alias used by multiple canonical nodes",
         lambda f: f"  - {f['alias']!r}: {', '.join(f['owners'])}"),
        ("broken_contradicts", "Broken contradicts reference",
         lambda f: f"  - {f['page']}#rel[{f['index']}]  contradicts={f.get('contradicts')}"),
        ("broken_supersedes", "Broken supersedes reference",
         lambda f: f"  - {f['page']}#rel[{f['index']}]  supersedes={f.get('supersedes')}"),
        ("orphan_typed_nodes", "Orphan typed nodes (no inbound or outbound typed edges)",
         lambda f: f"  - {f['node_id']}  ({f['path']})"),
    ]

    healthy = True
    for key, label, formatter in sections:
        items = findings[key]
        if not items:
            continue
        healthy = False
        out.append(f"{label} ({len(items)}):")
        for item in items[:50]:
            out.append(formatter(item))
        if len(items) > 50:
            out.append(f"  ... and {len(items) - 50} more")
        out.append("")

    if healthy:
        out.append("No graph issues found.")
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("wiki", nargs="?", type=Path, default=Path("wiki"))
    parser.add_argument("--ontology", type=Path, help="Ontology file (default: <wiki>/graph/ontology.yaml)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.wiki.exists():
        print(f"Wiki directory not found: {args.wiki}", file=sys.stderr)
        sys.exit(1)

    ontology_path = args.ontology or (args.wiki / "graph" / "ontology.yaml")
    if not ontology_path.exists():
        print(f"Ontology not found: {ontology_path}", file=sys.stderr)
        print("Did you forget to seed wiki/graph/ontology.yaml? See assets/ontology.yaml.template.",
              file=sys.stderr)
        sys.exit(1)
    try:
        ontology = yaml.safe_load(ontology_path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        print(f"Ontology parse error: {e}", file=sys.stderr)
        sys.exit(2)

    pages = collect_pages(args.wiki)
    findings = lint(pages, ontology)

    if args.json:
        print(json.dumps(findings, indent=2, default=str))
    else:
        print(render_text(findings))


if __name__ == "__main__":
    main()
