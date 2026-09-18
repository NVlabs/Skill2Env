#!/usr/bin/env python3
"""Create a FAIR-minded simulation reproducibility manifest."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List


MAX_FILE_SIZE = 500 * 1024 * 1024
MAX_ENTRIES = 1000
MAX_FIELD_LEN = 4096
SAFE_FIELD = re.compile(r"^[A-Za-z0-9_.:/@+-]+$")


def _split_csv(value: str, name: str = "list") -> List[str]:
    if not value:
        return []
    items = [item.strip() for item in value.split(",") if item.strip()]
    if len(items) > MAX_ENTRIES:
        raise ValueError(f"{name} has too many entries ({len(items)} > {MAX_ENTRIES})")
    return items


def _reject_control(value: str, name: str) -> None:
    if len(value) > MAX_FIELD_LEN:
        raise ValueError(f"{name} exceeds maximum length ({len(value)} > {MAX_FIELD_LEN})")
    if any(ord(ch) < 32 for ch in value):
        raise ValueError(f"{name} contains control characters")


def parse_units(value: str) -> Dict[str, str]:
    units: Dict[str, str] = {}
    for item in _split_csv(value, "units"):
        if "=" not in item:
            raise ValueError("units must use key=value entries")
        key, unit = [part.strip() for part in item.split("=", 1)]
        if not SAFE_FIELD.match(key) or not SAFE_FIELD.match(unit):
            raise ValueError("unit keys and values must use safe field characters")
        units[key] = unit
    return units


def file_record(path_value: str) -> Dict:
    _reject_control(path_value, "path")
    path = Path(path_value)
    record = {"path": path_value, "exists": path.exists()}
    if not path.exists():
        return record
    size = path.stat().st_size
    if size > MAX_FILE_SIZE:
        raise ValueError(f"file exceeds size limit ({size} > {MAX_FILE_SIZE}): {path_value}")
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    record.update({"size_bytes": size, "sha256": digest.hexdigest()})
    return record


def build_manifest(
    project_name: str,
    engine: str,
    inputs: List[str],
    outputs: List[str],
    units: Dict[str, str],
    structure_id: str | None,
    engine_version: str | None,
) -> Dict:
    if not project_name.strip():
        raise ValueError("project_name must not be empty")
    if not engine.strip():
        raise ValueError("engine must not be empty")
    _reject_control(project_name, "project_name")
    _reject_control(engine, "engine")
    if structure_id:
        _reject_control(structure_id, "structure_id")

    input_records = [file_record(path) for path in inputs]
    output_records = [file_record(path) for path in outputs]
    missing = [record["path"] for record in input_records + output_records if not record["exists"]]
    existing_records = [
        record for record in input_records + output_records if record["exists"]
    ]
    has_hashes = (
        all("sha256" in record for record in existing_records)
        if existing_records
        else None
    )
    manifest = {
        "project_name": project_name,
        "engine": engine,
        "engine_version": engine_version or "unknown",
        "structure_id": structure_id,
        "units": units,
        "file_inventory": {"inputs": input_records, "outputs": output_records},
        "missing_files": missing,
        "provenance": {
            "working_directory": os.getcwd(),
            "manifest_schema": "materials-simulation-skills.fair-manifest.v1",
        },
        "fair_checks": {
            "has_inputs": bool(inputs),
            "has_outputs": bool(outputs),
            "has_units": bool(units),
            "has_engine_version": bool(engine_version),
            "has_hashes_for_existing_files": has_hashes,
        },
        "recommended_next_steps": [
            "add code commit or container image digest",
            "add parser versions for derived quantities",
            "store README or notes describing the scientific intent",
        ],
    }
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-name", required=True)
    parser.add_argument("--engine", required=True)
    parser.add_argument("--engine-version")
    parser.add_argument("--inputs", default="", help="Comma-separated input files")
    parser.add_argument("--outputs", default="", help="Comma-separated output files")
    parser.add_argument("--units", default="", help="Comma-separated key=value units")
    parser.add_argument("--structure-id")
    parser.add_argument("--out", help="Optional manifest JSON output path")
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        manifest = build_manifest(
            project_name=args.project_name,
            engine=args.engine,
            inputs=_split_csv(args.inputs, "inputs"),
            outputs=_split_csv(args.outputs, "outputs"),
            units=parse_units(args.units),
            structure_id=args.structure_id,
            engine_version=args.engine_version,
        )
        if args.out:
            out_path = Path(args.out)
            _reject_control(str(out_path), "out")
            out_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    payload = {"inputs": vars(args), "results": {"manifest": manifest}}
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"Manifest for {manifest['project_name']} ({manifest['engine']})")
        if manifest["missing_files"]:
            print(f"Missing files: {', '.join(manifest['missing_files'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
