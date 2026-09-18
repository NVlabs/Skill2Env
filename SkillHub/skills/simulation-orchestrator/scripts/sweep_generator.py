#!/usr/bin/env python3
"""Generate parameter sweep configurations for multi-simulation campaigns.

This script creates multiple configuration files by varying parameters across
specified ranges. Supports grid (full factorial), linspace (uniform), and
LHS (Latin Hypercube Sampling) methods.

Swept parameter names may use dot notation (e.g. ``parameters.kappa``) to
target nested keys in the base config. ``merge_config`` walks/creates the
nested dict path and assigns the value there. A bare name (e.g. ``kappa``)
sets/overwrites a top-level key. This mirrors the dot-notation reads used by
result_aggregator.py, so a sweep on ``parameters.kappa`` actually changes the
value a solver reads from ``parameters.kappa`` (instead of silently leaving the
base value in place while adding an unused top-level ``kappa``).

Usage:
    python sweep_generator.py --base-config sim.json --params "dt:1e-4:1e-2:5" --method linspace --output-dir ./sweep
    python sweep_generator.py --base-config sim.json --params "parameters.kappa:0.1:1.0:4" --method linspace --output-dir ./sweep

Output (JSON):
    {
        "configs": ["config_0000.json", "config_0001.json", ...],
        "parameter_space": {"dt": [0.0001, 0.002575, 0.00505, 0.007525, 0.01]},
        "sweep_method": "linspace",
        "total_runs": 5
    }
"""

import argparse
import copy
import itertools
import json
import math
import os
import random
import re
import sys
from typing import Any, Dict, List, Tuple

# Security limits
MAX_PARAM_SPECS = 32  # maximum number of parameters in one --params string
MAX_COUNT = 100_000  # maximum points per parameter (linspace/grid)
MAX_SAMPLES = 1_000_000  # maximum LHS samples
MAX_NESTED_DEPTH = 10  # maximum dot-notation depth for an override key
# Parameter names: identifier segments separated by dots (mirrors the metric
# allowlist used by result_aggregator.py), e.g. "dt" or "parameters.kappa".
PARAM_NAME_PATTERN = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z_][a-zA-Z0-9_]*)*$")


def parse_param_spec(spec: str) -> Tuple[str, float, float, int]:
    """Parse parameter specification string.

    Formats:
        name:min:max:count  -> linspace/grid with count points
        name:min:max        -> for LHS, just bounds (count from --samples)

    Returns:
        (name, min_val, max_val, count) where count=-1 if not specified
    """
    parts = spec.strip().split(":")
    if len(parts) == 4:
        name, min_val, max_val, count = parts
        _validate_param_name(name)
        fmin, fmax = _parse_finite_float(name, min_val), _parse_finite_float(name, max_val)
        if fmin >= fmax:
            raise ValueError(
                f"Invalid range for '{name}': min ({fmin}) must be less than max ({fmax})"
            )
        icount = _parse_count(name, count)
        return name, fmin, fmax, icount
    elif len(parts) == 3:
        name, min_val, max_val = parts
        _validate_param_name(name)
        fmin, fmax = _parse_finite_float(name, min_val), _parse_finite_float(name, max_val)
        if fmin >= fmax:
            raise ValueError(
                f"Invalid range for '{name}': min ({fmin}) must be less than max ({fmax})"
            )
        return name, fmin, fmax, -1
    else:
        raise ValueError(
            f"Invalid param spec: {spec}. Use 'name:min:max:count' or 'name:min:max'"
        )


def _validate_param_name(name: str) -> None:
    """Validate a swept parameter name (allows dot notation for nested keys)."""
    if not PARAM_NAME_PATTERN.match(name):
        raise ValueError(
            f"Invalid parameter name '{name}'. "
            "Must match [a-zA-Z_][a-zA-Z0-9_]*(.[a-zA-Z_][a-zA-Z0-9_]*)* "
            "(e.g. 'dt' or 'parameters.kappa')"
        )
    if name.count(".") + 1 > MAX_NESTED_DEPTH:
        raise ValueError(
            f"Parameter name '{name}' exceeds maximum nesting depth {MAX_NESTED_DEPTH}"
        )


def _parse_finite_float(name: str, raw: str) -> float:
    """Parse a bound as a finite float, rejecting NaN/Inf."""
    try:
        val = float(raw)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid numeric bound for '{name}': {raw!r}")
    if not math.isfinite(val):
        raise ValueError(
            f"Bound for '{name}' must be finite, got {raw!r} (NaN/Inf not allowed)"
        )
    return val


def _parse_count(name: str, raw: str) -> int:
    """Parse a point count as a positive integer within the allowed bound."""
    try:
        icount = int(raw)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid count for '{name}': {raw!r} (must be an integer)")
    if icount <= 0:
        raise ValueError(f"Count for '{name}' must be a positive integer, got {icount}")
    if icount > MAX_COUNT:
        raise ValueError(
            f"Count for '{name}' ({icount}) exceeds maximum {MAX_COUNT}"
        )
    return icount


def parse_params(params_str: str) -> List[Tuple[str, float, float, int]]:
    """Parse comma-separated parameter specifications."""
    specs = [s.strip() for s in params_str.split(",") if s.strip()]
    if len(specs) > MAX_PARAM_SPECS:
        raise ValueError(
            f"Too many parameters ({len(specs)}); maximum is {MAX_PARAM_SPECS}"
        )
    return [parse_param_spec(s) for s in specs]


def linspace(start: float, stop: float, count: int) -> List[float]:
    """Generate linearly spaced values."""
    if count <= 1:
        return [start]
    step = (stop - start) / (count - 1)
    return [start + i * step for i in range(count)]


def generate_grid(params: List[Tuple[str, float, float, int]]) -> List[Dict[str, float]]:
    """Generate full factorial grid of parameter combinations."""
    param_names = [p[0] for p in params]
    param_values = [linspace(p[1], p[2], p[3]) for p in params]

    configs = []
    for combo in itertools.product(*param_values):
        configs.append(dict(zip(param_names, combo)))

    return configs


def generate_linspace(
    params: List[Tuple[str, float, float, int]]
) -> Tuple[List[Dict[str, float]], Dict[str, List[float]]]:
    """Generate grid sweep using linspace for each parameter."""
    configs = generate_grid(params)
    param_space = {p[0]: linspace(p[1], p[2], p[3]) for p in params}
    return configs, param_space


def generate_lhs(
    params: List[Tuple[str, float, float, int]], samples: int, seed: int = 42
) -> Tuple[List[Dict[str, float]], Dict[str, List[float]]]:
    """Generate Latin Hypercube Sampling configurations."""
    random.seed(seed)
    n_params = len(params)

    # Create intervals for each dimension
    configs = []
    param_space: Dict[str, List[float]] = {p[0]: [] for p in params}

    # Generate LHS: each parameter range divided into n intervals,
    # one sample per interval, randomly ordered
    for i in range(n_params):
        name, min_val, max_val, _ = params[i]
        interval_size = (max_val - min_val) / samples
        # Create one point per interval
        points = []
        for j in range(samples):
            low = min_val + j * interval_size
            high = low + interval_size
            points.append(random.uniform(low, high))
        random.shuffle(points)
        param_space[name] = points

    # Combine into configs
    for i in range(samples):
        config = {}
        for name in param_space:
            config[name] = param_space[name][i]
        configs.append(config)

    return configs, param_space


def load_base_config(path: str) -> Dict[str, Any]:
    """Load base configuration file."""
    with open(path, "r") as f:
        return json.load(f)


def _set_nested(target: Dict[str, Any], dotted_key: str, value: Any) -> None:
    """Set ``value`` at the dot-notation path ``dotted_key`` inside ``target``.

    Intermediate dicts are created as needed. If an intermediate path element
    exists but is not a dict, it is replaced with a dict so the override can be
    applied (the swept parameter always wins). A bare key (no dot) sets a
    top-level key.
    """
    keys = dotted_key.split(".")
    node = target
    for key in keys[:-1]:
        child = node.get(key)
        if not isinstance(child, dict):
            child = {}
            node[key] = child
        node = child
    node[keys[-1]] = value


def merge_config(base: Dict[str, Any], overrides: Dict[str, float]) -> Dict[str, Any]:
    """Merge override parameters into a deep copy of the base config.

    Override keys may use dot notation (e.g. ``parameters.kappa``) to target
    nested locations; ``merge_config`` walks/creates the nested dict path and
    assigns there. Bare keys set top-level values. This ensures a sweep on a
    nested parameter actually overwrites the value a solver reads, rather than
    silently adding an unused duplicate top-level key.
    """
    result = copy.deepcopy(base)
    for key, value in overrides.items():
        _set_nested(result, key, value)
    return result


def write_configs(
    base_config: Dict[str, Any],
    param_configs: List[Dict[str, float]],
    output_dir: str,
) -> List[str]:
    """Write configuration files to output directory."""
    os.makedirs(output_dir, exist_ok=True)
    written = []

    for i, params in enumerate(param_configs):
        merged = merge_config(base_config, params)
        filename = f"config_{i:04d}.json"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w") as f:
            json.dump(merged, f, indent=2)
        written.append(filename)

    return written


def generate_sweep(
    base_config_path: str,
    params_str: str,
    method: str,
    output_dir: str,
    samples: int = 10,
    seed: int = 42,
    force: bool = False,
) -> Dict[str, Any]:
    """Generate parameter sweep configurations.

    Args:
        base_config_path: Path to base configuration JSON
        params_str: Comma-separated parameter specifications
        method: Sweep method (grid, linspace, lhs)
        output_dir: Directory to write configurations
        samples: Number of samples for LHS method
        seed: Random seed for reproducibility
        force: Overwrite existing output directory

    Returns:
        Dictionary with configs, parameter_space, sweep_method, total_runs
    """
    # Validate inputs
    if not os.path.exists(base_config_path):
        raise ValueError(f"Base config not found: {base_config_path}")

    if os.path.exists(output_dir) and not force:
        raise ValueError(
            f"Output directory exists: {output_dir}. Use --force to overwrite."
        )

    # Parse parameters
    params = parse_params(params_str)
    if not params:
        raise ValueError("No parameters specified")

    # Load base config
    base_config = load_base_config(base_config_path)

    # Generate parameter combinations
    if method == "grid":
        for p in params:
            if p[3] <= 0:
                raise ValueError(f"Grid method requires count for parameter {p[0]}")
        configs, param_space = generate_linspace(params)
    elif method == "linspace":
        for p in params:
            if p[3] <= 0:
                raise ValueError(f"Linspace method requires count for parameter {p[0]}")
        configs, param_space = generate_linspace(params)
    elif method == "lhs":
        if samples <= 0:
            raise ValueError(f"--samples must be a positive integer, got {samples}")
        if samples > MAX_SAMPLES:
            raise ValueError(f"--samples ({samples}) exceeds maximum {MAX_SAMPLES}")
        configs, param_space = generate_lhs(params, samples, seed)
    else:
        raise ValueError(f"Unknown method: {method}. Use grid, linspace, or lhs.")

    # Write configuration files
    written = write_configs(base_config, configs, output_dir)

    # Write manifest
    manifest = {
        "configs": written,
        "parameter_space": param_space,
        "sweep_method": method,
        "total_runs": len(configs),
        "base_config": os.path.basename(base_config_path),
        "parameters": [{"name": p[0], "min": p[1], "max": p[2]} for p in params],
    }

    manifest_path = os.path.join(output_dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate parameter sweep configurations.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--base-config",
        required=True,
        help="Path to base configuration JSON file",
    )
    parser.add_argument(
        "--params",
        required=True,
        help="Parameter specs: 'name:min:max:count,...' or 'name:min:max,...' for LHS",
    )
    parser.add_argument(
        "--method",
        choices=["grid", "linspace", "lhs"],
        default="linspace",
        help="Sweep method",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory to write configuration files",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=10,
        help=f"Number of samples for LHS method (positive, max {MAX_SAMPLES})",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing output directory",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    try:
        result = generate_sweep(
            base_config_path=args.base_config,
            params_str=args.params,
            method=args.method,
            output_dir=args.output_dir,
            samples=args.samples,
            seed=args.seed,
            force=args.force,
        )
    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(2)

    if args.json:
        # Output subset for JSON (exclude full param_space for brevity)
        output = {
            "configs": result["configs"],
            "parameter_space": {
                k: [round(v, 8) for v in vals]
                for k, vals in result["parameter_space"].items()
            },
            "sweep_method": result["sweep_method"],
            "total_runs": result["total_runs"],
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"Generated {result['total_runs']} configurations")
        print(f"Method: {result['sweep_method']}")
        print(f"Output directory: {args.output_dir}")
        print(f"Configs: {', '.join(result['configs'][:5])}...")


if __name__ == "__main__":
    main()
