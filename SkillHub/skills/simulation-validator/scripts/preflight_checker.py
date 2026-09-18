#!/usr/bin/env python3
import argparse
import json
import math
import os
import re
import sys
from typing import Dict, List, Optional, Tuple

# Allowlist for --required parameter names: letters, digits, underscore, dot, hyphen.
REQUIRED_NAME_RE = re.compile(r"^[A-Za-z0-9_.-]+$")


def positive_finite_float(raw: str) -> float:
    """argparse type: accept only finite, strictly-positive floats."""
    try:
        value = float(raw)
    except (TypeError, ValueError):
        raise argparse.ArgumentTypeError(f"not a number: {raw!r}")
    if not math.isfinite(value) or value <= 0:
        raise argparse.ArgumentTypeError(
            f"must be a finite positive number, got {raw!r}"
        )
    return value


def get_free_disk_space_gb(path: str) -> Optional[float]:
    """Get free disk space in GB. Cross-platform (Windows, Linux, macOS)."""
    try:
        if sys.platform == "win32":
            # Windows: use ctypes to call GetDiskFreeSpaceExW
            import ctypes

            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                ctypes.c_wchar_p(os.path.abspath(path)),
                None,
                None,
                ctypes.pointer(free_bytes),
            )
            return free_bytes.value / (1024**3)
        else:
            # Unix-like: use os.statvfs
            stat = os.statvfs(path)
            return (stat.f_bavail * stat.f_frsize) / (1024**3)
    except (OSError, AttributeError):
        return None


def load_config(path: str) -> Dict[str, object]:
    if not os.path.exists(path):
        raise ValueError(f"Config not found: {path}")
    if path.endswith(".json"):
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    # Minimal YAML-like fallback: key: value per line
    config: Dict[str, object] = {}
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            try:
                if "." in value or "e" in value.lower():
                    parsed = float(value)
                else:
                    parsed = int(value)
            except ValueError:
                parsed = value
            config[key] = parsed
    return config


def parse_list(raw: Optional[str]) -> List[str]:
    if not raw:
        return []
    names = [p.strip() for p in raw.split(",") if p.strip()]
    for name in names:
        if not REQUIRED_NAME_RE.match(name):
            raise ValueError(
                f"Invalid parameter name {name!r}; allowed characters are "
                "letters, digits, underscore, dot, and hyphen."
            )
    return names


def parse_ranges(raw: Optional[str]) -> Dict[str, Tuple[float, float]]:
    ranges: Dict[str, Tuple[float, float]] = {}
    if not raw:
        return ranges
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    for part in parts:
        if ":" not in part:
            raise ValueError("range entries must be name:min:max")
        name, min_val, max_val = part.split(":", 2)
        try:
            lo = float(min_val)
            hi = float(max_val)
        except ValueError:
            raise ValueError(f"range bounds for {name.strip()!r} must be numeric.")
        if not math.isfinite(lo) or not math.isfinite(hi):
            raise ValueError(f"range bounds for {name.strip()!r} must be finite.")
        if hi <= lo:
            raise ValueError(
                f"range max ({hi}) must be greater than min ({lo}) for "
                f"{name.strip()!r}."
            )
        ranges[name.strip()] = (lo, hi)
    return ranges


def _nearest_existing_ancestor(path: str) -> str:
    """Walk up from path until an existing directory is found (for disk probe)."""
    current = os.path.abspath(path)
    while current and not os.path.exists(current):
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    return current or "."


def preflight_check(
    config: Dict[str, object],
    required: List[str],
    ranges: Dict[str, Tuple[float, float]],
    output_dir: Optional[str],
    min_free_gb: float,
    config_dir: Optional[str] = None,
) -> Dict[str, object]:
    blockers: List[str] = []
    warnings: List[str] = []

    params = config.get("parameters", {})
    if not isinstance(params, dict):
        params = {}

    for key in required:
        if key not in config and key not in params:
            blockers.append(f"Missing required parameter: {key}")

    for key, (min_val, max_val) in ranges.items():
        value = config.get(key, params.get(key))
        if value is None:
            warnings.append(f"Range check skipped; missing {key}.")
            continue
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            blockers.append(f"Non-numeric value for {key}.")
            continue
        if numeric < min_val or numeric > max_val:
            blockers.append(f"{key} out of range [{min_val}, {max_val}].")

    # Resolve the output target. A CLI --output-dir override stays CWD-relative;
    # an output_dir from the config file is resolved relative to the config file's
    # directory (config-relative), since on HPC the launch CWD often differs from
    # where the config lives.
    cli_override = output_dir is not None
    if output_dir is None:
        config_output = config.get("output_dir")
        output_dir = config_output if isinstance(config_output, str) else None

    resolved_output: Optional[str] = None
    if output_dir:
        if os.path.isabs(output_dir):
            resolved_output = output_dir
        elif cli_override or not config_dir:
            resolved_output = os.path.abspath(output_dir)
        else:
            resolved_output = os.path.join(config_dir, output_dir)

        if not os.path.exists(resolved_output):
            warnings.append("Output directory does not exist; will be created.")
        else:
            if not os.access(resolved_output, os.W_OK):
                blockers.append("Output directory not writable.")
    else:
        warnings.append("No output directory specified.")

    if min_free_gb > 0:
        # Measure the volume that will actually hold the output. If the output
        # dir does not exist yet, probe its nearest existing ancestor. Fall back
        # to CWD only when no output_dir is configured.
        if resolved_output:
            probe_path = _nearest_existing_ancestor(resolved_output)
        else:
            probe_path = "."
        free_gb = get_free_disk_space_gb(probe_path)
        if free_gb is not None and free_gb < min_free_gb:
            blockers.append(
                f"Insufficient disk space at {probe_path}: {free_gb:.2f} GB free."
            )
        elif free_gb is None:
            warnings.append("Could not determine free disk space.")

    if "material_source" not in config and "materials_source" not in config:
        warnings.append("Material property source not specified.")

    status = "PASS"
    if blockers:
        status = "BLOCK"
    elif warnings:
        status = "WARN"

    return {
        "status": status,
        "blockers": blockers,
        "warnings": warnings,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Pre-flight simulation validation checks.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--config", required=True, help="Path to simulation config (JSON)")
    parser.add_argument(
        "--required",
        default=None,
        help="Comma-separated required parameters",
    )
    parser.add_argument(
        "--ranges",
        default=None,
        help="Range checks name:min:max (comma-separated)",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Override output directory for checks",
    )
    parser.add_argument(
        "--min-free-gb",
        type=positive_finite_float,
        default=0.1,
        help="Minimum free disk space (GB)",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        config = load_config(args.config)
        config_dir = os.path.dirname(os.path.abspath(args.config))
        report = preflight_check(
            config=config,
            required=parse_list(args.required),
            ranges=parse_ranges(args.ranges),
            output_dir=args.output_dir,
            min_free_gb=args.min_free_gb,
            config_dir=config_dir,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)

    payload = {
        "inputs": {
            "config": args.config,
            "required": parse_list(args.required),
            "ranges": args.ranges,
            "output_dir": args.output_dir,
            "min_free_gb": args.min_free_gb,
        },
        "report": report,
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return

    print("Preflight report")
    print(f"  status: {report['status']}")
    for item in report["blockers"]:
        print(f"  blocker: {item}")
    for item in report["warnings"]:
        print(f"  warning: {item}")


if __name__ == "__main__":
    main()
