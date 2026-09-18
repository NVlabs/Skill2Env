#!/usr/bin/env python3
"""
wiki_graph_query.py — Query the compiled wiki graph (graph.sqlite).

Use this to accelerate navigation: find what's connected to a node, list
typed edges around a subject, find a path between two nodes, or dump every
fact about a node. The graph is a navigation index — for high-stakes
claims, follow the `source` field back to the wiki page and the raw file.

Subcommands:
    neighbors --node <id>            List nodes one hop away from <id>
    edges    --subject <id>          List all outbound edges from <id>
             [--predicate <p>]        Filter by predicate
    path     --from <id> --to <id>   Shortest directed path (BFS, max depth 6)
             [--max-depth N]
    facts    --about <id>            Outbound + inbound edges for <id>

Common options:
    --db <path>           Path to graph.sqlite (default: <wiki>/graph/graph.sqlite)
    --json                Emit JSON instead of text

Examples:
    python wiki_graph_query.py wiki/ neighbors --node product:konvy
    python wiki_graph_query.py wiki/ edges    --subject person:stephanie-emmanouel
    python wiki_graph_query.py wiki/ path     --from person:praney-behl --to product:konvy
    python wiki_graph_query.py wiki/ facts    --about product:konvy
"""

import argparse
import json
import sqlite3
import sys
from collections import deque
from pathlib import Path


EVIDENCE_SNIPPET_LEN = 140


def open_db(path: Path) -> sqlite3.Connection:
    if not path.exists():
        print(f"graph.sqlite not found at {path}.", file=sys.stderr)
        print("Run wiki_graph_extract.py first.", file=sys.stderr)
        sys.exit(1)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def fetch_node(conn: sqlite3.Connection, node_id: str) -> dict | None:
    row = conn.execute("SELECT * FROM nodes WHERE id = ?", (node_id,)).fetchone()
    return dict(row) if row else None


def edges_from(conn: sqlite3.Connection, subject: str, predicate: str | None = None) -> list[dict]:
    q = "SELECT * FROM edges WHERE subject = ?"
    params: list = [subject]
    if predicate:
        q += " AND predicate = ?"
        params.append(predicate)
    q += " ORDER BY predicate, object"
    return [dict(r) for r in conn.execute(q, params).fetchall()]


def edges_to(conn: sqlite3.Connection, obj: str, predicate: str | None = None) -> list[dict]:
    q = "SELECT * FROM edges WHERE object = ?"
    params: list = [obj]
    if predicate:
        q += " AND predicate = ?"
        params.append(predicate)
    q += " ORDER BY predicate, subject"
    return [dict(r) for r in conn.execute(q, params).fetchall()]


def truncate(text: str | None) -> str:
    if not text:
        return ""
    if len(text) <= EVIDENCE_SNIPPET_LEN:
        return text
    return text[: EVIDENCE_SNIPPET_LEN - 1].rstrip() + "…"


def render_edge_row(e: dict) -> str:
    pieces = [
        f"  {e['subject']} --[{e['predicate']}]--> {e['object']}",
    ]
    confidence = e.get("confidence") or "-"
    status = e.get("status") or "-"
    src = e.get("source") or "-"
    pieces.append(f"      via {src}  conf={confidence}  status={status}")
    if e.get("evidence"):
        pieces.append(f"      evidence: {truncate(e['evidence'])}")
    pieces.append(f"      (page: {e['page']})")
    return "\n".join(pieces)


def cmd_neighbors(conn: sqlite3.Connection, args) -> dict:
    node = fetch_node(conn, args.node)
    if not node:
        print(f"node not found: {args.node}", file=sys.stderr)
        sys.exit(1)
    out_edges = edges_from(conn, args.node)
    in_edges = edges_to(conn, args.node)

    neighbors: dict[str, dict] = {}
    for e in out_edges:
        neighbors.setdefault(e["object"], {"node_id": e["object"], "out": [], "in": []})
        neighbors[e["object"]]["out"].append(e)
    for e in in_edges:
        neighbors.setdefault(e["subject"], {"node_id": e["subject"], "out": [], "in": []})
        neighbors[e["subject"]]["in"].append(e)

    # Resolve neighbor titles where possible
    for nid, slot in neighbors.items():
        target = fetch_node(conn, nid)
        slot["title"] = target["title"] if target else nid
        slot["path"] = target["path"] if target else None

    return {
        "node": node,
        "neighbors": sorted(neighbors.values(), key=lambda n: n["node_id"]),
    }


def cmd_edges(conn: sqlite3.Connection, args) -> dict:
    es = edges_from(conn, args.subject, args.predicate)
    return {"subject": args.subject, "predicate": args.predicate, "edges": es}


def cmd_facts(conn: sqlite3.Connection, args) -> dict:
    node = fetch_node(conn, args.about)
    if not node:
        print(f"node not found: {args.about}", file=sys.stderr)
        sys.exit(1)
    return {
        "node": node,
        "outbound": edges_from(conn, args.about),
        "inbound": edges_to(conn, args.about),
    }


def cmd_path(conn: sqlite3.Connection, args) -> dict:
    src = fetch_node(conn, getattr(args, "from"))
    dst = fetch_node(conn, args.to)
    if not src:
        print(f"from-node not found: {getattr(args, 'from')}", file=sys.stderr)
        sys.exit(1)
    if not dst:
        print(f"to-node not found: {args.to}", file=sys.stderr)
        sys.exit(1)

    start, goal = getattr(args, "from"), args.to
    queue = deque([(start, [start], [])])
    visited = {start}
    while queue:
        node, node_path, edge_path = queue.popleft()
        if node == goal:
            return {"from": start, "to": goal, "path_nodes": node_path, "path_edges": edge_path}
        if len(node_path) - 1 >= args.max_depth:
            continue
        for e in edges_from(conn, node):
            nxt = e["object"]
            if nxt in visited:
                continue
            visited.add(nxt)
            queue.append((nxt, node_path + [nxt], edge_path + [e]))
    return {"from": start, "to": goal, "path_nodes": [], "path_edges": []}


def render(result: dict, command: str) -> str:
    out: list[str] = []
    if command == "neighbors":
        n = result["node"]
        out.append(f"Node: {n['id']}  ({n['title']})  {n['node_type']}  [{n['path']}]")
        out.append(f"Neighbors: {len(result['neighbors'])}")
        for nb in result["neighbors"]:
            out.append("")
            out.append(f"  → {nb['node_id']}  ({nb['title']})")
            for e in nb.get("out", []):
                out.append(f"      out  [{e['predicate']}]  conf={e.get('confidence') or '-'}  src={e.get('source') or '-'}")
            for e in nb.get("in", []):
                out.append(f"      in   [{e['predicate']}]  from {e['subject']}  src={e.get('source') or '-'}")
    elif command == "edges":
        out.append(f"Edges from {result['subject']}"
                   + (f" with predicate {result['predicate']}" if result['predicate'] else ""))
        for e in result["edges"]:
            out.append("")
            out.append(render_edge_row(e))
    elif command == "facts":
        n = result["node"]
        out.append(f"Facts about {n['id']}  ({n['title']})  [{n['path']}]")
        out.append("")
        out.append(f"Outbound ({len(result['outbound'])}):")
        for e in result["outbound"]:
            out.append(render_edge_row(e))
        out.append("")
        out.append(f"Inbound ({len(result['inbound'])}):")
        for e in result["inbound"]:
            out.append(render_edge_row(e))
    elif command == "path":
        if not result["path_nodes"]:
            out.append(f"No path found from {result['from']} to {result['to']} within depth limit.")
        else:
            out.append(f"Path from {result['from']} to {result['to']} ({len(result['path_edges'])} hops):")
            for e in result["path_edges"]:
                out.append("")
                out.append(render_edge_row(e))
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("wiki", type=Path, help="Wiki directory.")
    parser.add_argument("--db", type=Path, help="Path to graph.sqlite (default: <wiki>/graph/graph.sqlite)")
    parser.add_argument("--json", action="store_true")

    sub = parser.add_subparsers(dest="command", required=True)

    p_n = sub.add_parser("neighbors")
    p_n.add_argument("--node", required=True)

    p_e = sub.add_parser("edges")
    p_e.add_argument("--subject", required=True)
    p_e.add_argument("--predicate")

    p_p = sub.add_parser("path")
    p_p.add_argument("--from", dest="from", required=True)
    p_p.add_argument("--to", required=True)
    p_p.add_argument("--max-depth", type=int, default=6)

    p_f = sub.add_parser("facts")
    p_f.add_argument("--about", required=True)

    args = parser.parse_args()

    if not args.wiki.exists():
        print(f"Wiki directory not found: {args.wiki}", file=sys.stderr)
        sys.exit(1)
    db_path = args.db or (args.wiki / "graph" / "graph.sqlite")
    conn = open_db(db_path)
    try:
        if args.command == "neighbors":
            result = cmd_neighbors(conn, args)
        elif args.command == "edges":
            result = cmd_edges(conn, args)
        elif args.command == "path":
            result = cmd_path(conn, args)
        elif args.command == "facts":
            result = cmd_facts(conn, args)
        else:
            parser.print_help()
            sys.exit(1)
    finally:
        conn.close()

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print(render(result, args.command))


if __name__ == "__main__":
    main()
