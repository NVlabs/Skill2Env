#!/usr/bin/env python3
"""
Memory Profiler - Estimate memory requirements from simulation parameters.
"""
import argparse
import json
import math
import os
import sys
from typing import Dict, Optional

# Security limits
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB


def load_parameters(path: str) -> Dict:
    """
    Load simulation parameters from JSON file with validation.

    Args:
        path: Path to JSON file with parameters

    Returns:
        Parameter dictionary
    """
    try:
        file_size = os.path.getsize(path)
        if file_size > MAX_FILE_SIZE:
            raise ValueError(f"File exceeds size limit ({file_size} > {MAX_FILE_SIZE}): {path}")
        with open(path, 'r', encoding='utf-8') as f:
            params = json.load(f)
        if not isinstance(params, dict):
            raise ValueError(f"JSON root must be an object: {path}")
        
        # Validate required fields
        missing = []
        if 'mesh' not in params:
            missing.append('mesh')
        if 'fields' not in params:
            missing.append('fields')
        
        if missing:
            raise ValueError(f"Missing required parameters: {', '.join(missing)}")
        
        return params
    
    except FileNotFoundError:
        raise FileNotFoundError(f"Parameters file not found: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")


def estimate_field_memory(mesh: Dict, fields: Dict) -> float:
    """
    Estimate memory for field variables.

    Args:
        mesh: Mesh parameters (nx, ny, nz)
        fields: Field definitions

    Returns:
        Memory in GB
    """
    # Calculate total mesh points
    nx = mesh.get('nx', 1)
    ny = mesh.get('ny', 1)
    nz = mesh.get('nz', 1)
    # Validate mesh dimensions
    for name, val in [('nx', nx), ('ny', ny), ('nz', nz)]:
        if not isinstance(val, int) or val <= 0:
            raise ValueError(f"Mesh dimension '{name}' must be a positive integer, got {val}")
    mesh_points = nx * ny * nz

    # Calculate memory for all fields
    total_bytes = 0
    for field_name, field_spec in fields.items():
        components = field_spec.get('components', 1)
        bytes_per_value = field_spec.get('bytes_per_value', 8)  # default: double precision
        if not isinstance(components, int) or components <= 0:
            raise ValueError(f"Field '{field_name}' components must be a positive integer, got {components}")
        if not isinstance(bytes_per_value, (int, float)) or bytes_per_value <= 0:
            raise ValueError(f"Field '{field_name}' bytes_per_value must be positive, got {bytes_per_value}")
        total_bytes += mesh_points * components * bytes_per_value
    
    # Convert to GB
    return total_bytes / (1024 ** 3)


def _count_field_components(fields: Dict) -> int:
    """Count total degrees of freedom per mesh point across all fields."""
    total = 0
    for field_spec in fields.values():
        components = field_spec.get('components', 1)
        if isinstance(components, int) and components > 0:
            total += components
    return max(total, 1)


# Default sparse-matrix stencil (non-zeros per row). 7 is the canonical
# 3D finite-difference 7-point stencil. Configurable via solver['stencil_nnz'].
DEFAULT_STENCIL_NNZ = 7
# Bytes for a column index in a sparse matrix (int32 by default).
DEFAULT_INDEX_BYTES = 4
# Conservative fill-in factor for direct-solver factorization. Direct solvers
# grow like O(N^1.3); this multiplies the assembled sparse-operator cost to
# reflect factorization fill-in (see optimization_strategies.md Case Study 3,
# where a 256^3 direct solve uses ~9x the iterative footprint).
DEFAULT_DIRECT_FILLIN_FACTOR = 10.0


def estimate_solver_memory(mesh: Dict, solver: Dict, fields: Optional[Dict] = None) -> Dict:
    """
    Estimate memory for solver workspace and matrix storage.

    Implements the three-term formula from references/profiling_guide.md:
    the solver contribution is the matrix storage plus iterative workspace
    vectors, and it depends on the solver type:

      - ``matrix-free``: no assembled matrix, workspace vectors only.
      - ``iterative`` (default): sparse matrix storage + workspace vectors.
      - ``direct``: sparse matrix storage scaled by a conservative fill-in
        factor to reflect factorization fill-in (Case Study 3: ~18 GB direct
        vs ~2 GB iterative for the same mesh).

    The sparse-matrix estimate assumes a documented stencil (default 7,
    the 3D 7-point finite-difference stencil; override via
    ``solver['stencil_nnz']``) and is intentionally conservative so that a
    "will it fit in RAM?" decision does not silently under-estimate.

    Args:
        mesh: Mesh parameters
        solver: Solver configuration
        fields: Field definitions (used to size matrix degrees of freedom)

    Returns:
        Dict with 'workspace_gb' and 'matrix_storage_gb' (both in GB)
    """
    # Calculate total mesh points
    nx = mesh.get('nx', 1)
    ny = mesh.get('ny', 1)
    nz = mesh.get('nz', 1)
    mesh_points = nx * ny * nz

    # Get workspace multiplier and solver type
    solver_type = str(solver.get('type', 'iterative')).lower()
    workspace_multiplier = solver.get('workspace_multiplier', 5)
    if not isinstance(workspace_multiplier, (int, float)) or workspace_multiplier < 0:
        raise ValueError(
            f"solver workspace_multiplier must be a non-negative number, got {workspace_multiplier}"
        )

    stencil_nnz = solver.get('stencil_nnz', DEFAULT_STENCIL_NNZ)
    if not isinstance(stencil_nnz, (int, float)) or stencil_nnz < 0:
        raise ValueError(f"solver stencil_nnz must be a non-negative number, got {stencil_nnz}")
    index_bytes = solver.get('index_bytes', DEFAULT_INDEX_BYTES)
    if not isinstance(index_bytes, (int, float)) or index_bytes < 0:
        raise ValueError(f"solver index_bytes must be a non-negative number, got {index_bytes}")

    bytes_per_value = 8  # double precision
    n_dofs = mesh_points * _count_field_components(fields or {})

    # Iterative workspace vectors (size n_dofs each).
    workspace_bytes = n_dofs * workspace_multiplier * bytes_per_value

    # Assembled sparse matrix: each stored non-zero costs one value + one index.
    sparse_matrix_bytes = n_dofs * stencil_nnz * (bytes_per_value + index_bytes)

    if solver_type == 'matrix-free':
        matrix_bytes = 0.0
    elif solver_type == 'direct':
        fillin = solver.get('fillin_factor', DEFAULT_DIRECT_FILLIN_FACTOR)
        if not isinstance(fillin, (int, float)) or fillin <= 0:
            raise ValueError(f"solver fillin_factor must be a positive number, got {fillin}")
        # Direct factorization fill-in scales the sparse-operator cost; the
        # workspace vectors are not needed for a direct solve.
        matrix_bytes = sparse_matrix_bytes * fillin
        workspace_bytes = 0.0
    else:  # iterative (default) and any unknown type fall back to iterative
        matrix_bytes = sparse_matrix_bytes

    return {
        'workspace_gb': workspace_bytes / (1024 ** 3),
        'matrix_storage_gb': matrix_bytes / (1024 ** 3),
    }


def compute_total_memory(params: Dict, available_gb: Optional[float] = None) -> Dict:
    """
    Compute total memory requirements.
    
    Args:
        params: Simulation parameters
        available_gb: Available system memory (optional)
    
    Returns:
        Memory profile dictionary
    """
    mesh = params['mesh']
    fields = params['fields']
    solver = params.get('solver', {'type': 'iterative', 'workspace_multiplier': 5})
    processors = params.get('processors', 1)
    if not isinstance(processors, int) or processors <= 0:
        raise ValueError(f"processors must be a positive integer, got {processors}")
    if available_gb is not None:
        if not isinstance(available_gb, (int, float)) or not math.isfinite(available_gb) or available_gb <= 0:
            raise ValueError(f"available_gb must be a positive finite number, got {available_gb}")
    
    # Calculate mesh points
    nx = mesh.get('nx', 1)
    ny = mesh.get('ny', 1)
    nz = mesh.get('nz', 1)
    mesh_points = nx * ny * nz
    
    # Estimate memory components (three-term formula: field + solver workspace
    # + matrix storage, per references/profiling_guide.md).
    field_memory_gb = estimate_field_memory(mesh, fields)
    solver_mem = estimate_solver_memory(mesh, solver, fields)
    solver_workspace_gb = solver_mem['workspace_gb']
    matrix_storage_gb = solver_mem['matrix_storage_gb']
    total_memory_gb = field_memory_gb + solver_workspace_gb + matrix_storage_gb
    per_process_gb = total_memory_gb / processors
    
    # Generate warnings
    warnings = []
    if available_gb is not None:
        if total_memory_gb > available_gb:
            warnings.append(f"Total memory ({total_memory_gb:.2f} GB) exceeds available memory ({available_gb:.2f} GB)")
        elif total_memory_gb > 0.8 * available_gb:
            warnings.append(f"Memory usage ({total_memory_gb:.2f} GB) is high (>80% of available {available_gb:.2f} GB)")
    
    return {
        'mesh_points': mesh_points,
        'field_memory_gb': field_memory_gb,
        'solver_workspace_gb': solver_workspace_gb,
        'matrix_storage_gb': matrix_storage_gb,
        'total_memory_gb': total_memory_gb,
        'per_process_gb': per_process_gb,
        'warnings': warnings
    }


def main():
    parser = argparse.ArgumentParser(
        description='Estimate memory requirements from simulation parameters'
    )
    parser.add_argument('--params', required=True, help='Path to JSON file with simulation parameters')
    parser.add_argument('--available-gb', type=float, help='Available system memory in GB')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')
    
    args = parser.parse_args()
    
    try:
        # Load parameters
        params = load_parameters(args.params)
        
        # Compute memory profile
        profile = compute_total_memory(params, args.available_gb)
        
        # Format output
        if args.json:
            output = {
                'inputs': {
                    'params_file': args.params,
                    'available_gb': args.available_gb
                },
                'results': profile
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"Memory Profile")
            print(f"=" * 60)
            print(f"Mesh points: {profile['mesh_points']:,}")
            print(f"Field memory: {profile['field_memory_gb']:.3f} GB")
            print(f"Solver workspace: {profile['solver_workspace_gb']:.3f} GB")
            print(f"Matrix storage: {profile['matrix_storage_gb']:.3f} GB")
            print(f"Total memory: {profile['total_memory_gb']:.3f} GB")
            print(f"Per-process memory: {profile['per_process_gb']:.3f} GB")
            
            if profile['warnings']:
                print(f"\nWarnings:")
                for warning in profile['warnings']:
                    print(f"  - {warning}")
    
    except (FileNotFoundError, ValueError) as e:
        if args.json:
            print(json.dumps({'error': str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        if args.json:
            print(json.dumps({'error': f'Unexpected error: {e}'}))
        else:
            print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
