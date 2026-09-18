#!/usr/bin/env python3
"""check_artifact.py — Inspect a QIIME 2 .qza/.qzv WITHOUT a QIIME 2 install.

A QIIME 2 artifact (.qza) or visualization (.qzv) is just a ZIP whose single
top-level directory is the artifact's UUID. Inside that directory:

    <uuid>/metadata.yaml     # 'uuid:', 'type:' (semantic type), 'format:'
    <uuid>/data/...          # the payload
    <uuid>/provenance/       # recorded actions, parameters, plugin versions

This reads those without importing qiime2, so you can sanity-check that an artifact is
the SEMANTIC TYPE a downstream step expects (e.g. FeatureTable[Frequency],
SampleData[PairedEndSequencesWithQuality]) before wiring it into the next command, and
list the provenance actions that produced it. Pure standard library (zipfile + a tiny
line parser for the handful of metadata.yaml keys) — no PyYAML, no qiime2, runs under a
bare ``uv run python``.

Usage:
  uv run python check_artifact.py ARTIFACT.qza [--provenance] [--json]
  uv run python check_artifact.py table.qza                 # type + uuid + format
  uv run python check_artifact.py table.qza --provenance     # + action list
  uv run python check_artifact.py table.qza --json           # machine-readable

Exit codes: 0 = parsed; 2 = not a readable QIIME 2 zip / missing metadata.yaml.
"""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import PurePosixPath


def _scalar(line: str, key: str) -> str | None:
    """Extract 'key: value' from a flat metadata.yaml line (no PyYAML needed)."""
    stripped = line.strip()
    if stripped.startswith(key + ":"):
        return stripped[len(key) + 1 :].strip().strip("'\"")
    return None


def read_metadata(zf: zipfile.ZipFile) -> dict:
    # The single top-level dir is the artifact UUID.
    roots = {PurePosixPath(n).parts[0] for n in zf.namelist() if n.strip("/")}
    if len(roots) != 1:
        raise SystemExit(f"ERROR: expected one top-level dir (UUID), found {sorted(roots)}")
    root = roots.pop()
    meta_path = f"{root}/metadata.yaml"
    if meta_path not in zf.namelist():
        raise SystemExit(f"ERROR: no metadata.yaml at {meta_path} — not a QIIME 2 artifact?")
    text = zf.read(meta_path).decode("utf-8", "replace")
    info = {"root_uuid": root, "uuid": None, "type": None, "format": None}
    for line in text.splitlines():
        for key in ("uuid", "type", "format"):
            val = _scalar(line, key)
            if val is not None and info[key] is None:
                info[key] = val
    return info


def list_provenance_actions(zf: zipfile.ZipFile, root: str) -> list[str]:
    """List provenance action.yaml entries (one per recorded action)."""
    prefix = f"{root}/provenance/"
    actions = sorted(
        n for n in zf.namelist()
        if n.startswith(prefix) and n.endswith("/action/action.yaml")
    )
    out: list[str] = []
    for n in actions:
        plugin = act = None
        for line in zf.read(n).decode("utf-8", "replace").splitlines():
            plugin = plugin or _scalar(line, "plugin")
            act = act or _scalar(line, "action")
        label = "/".join(p for p in (plugin, act) if p) or n
        out.append(label)
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("artifact", help="Path to a .qza or .qzv file")
    ap.add_argument("--provenance", action="store_true", help="List provenance actions")
    ap.add_argument("--json", action="store_true", help="Emit JSON")
    args = ap.parse_args(argv)

    try:
        zf = zipfile.ZipFile(args.artifact)
    except (FileNotFoundError, zipfile.BadZipFile) as exc:
        print(f"ERROR: cannot open as zip: {exc}", file=sys.stderr)
        return 2

    with zf:
        info = read_metadata(zf)
        prov: list[str] = []
        if args.provenance:
            prov = list_provenance_actions(zf, info["root_uuid"])

    if args.json:
        payload = {"uuid": info["uuid"] or info["root_uuid"],
                   "type": info["type"], "format": info["format"]}
        if args.provenance:
            payload["provenance_actions"] = prov
        print(json.dumps(payload, indent=2))
    else:
        print(f"uuid:   {info['uuid'] or info['root_uuid']}")
        print(f"type:   {info['type']}")
        print(f"format: {info['format']}")
        if args.provenance:
            print("provenance actions ({}):".format(len(prov)))
            for a in prov:
                print(f"  - {a}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
