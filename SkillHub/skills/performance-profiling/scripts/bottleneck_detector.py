#!/usr/bin/env python3
"""
Bottleneck Detector - Identify performance bottlenecks and recommend optimizations.
"""
import argparse
import json
import os
import re
import sys
from typing import Dict, List, Optional

# Security limits
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB

# Keyword groups used both for per-type thresholds and recommendation routing.
IO_KEYWORDS = ['io', 'i/o', 'write', 'output', 'save']
ASSEMBLY_KEYWORDS = ['assembly', 'assemble', 'build']
SOLVER_KEYWORDS = ['solve', 'linear', 'iteration', 'cg', 'gmres']

# Per-type dominance thresholds (percentage of total runtime) matching the
# documented decision rules in SKILL.md / references/profiling_guide.md.
IO_THRESHOLD = 30.0
DEFAULT_THRESHOLD = 50.0
HIGH_SEVERITY_THRESHOLD = 70.0


def _classify_phase(name: str) -> str:
    """Classify a phase name into 'io', 'assembly', 'solver', or 'general'.

    Normalizes the name by lowercasing and stripping non-alphanumerics so that
    canonical names like 'I/O' (which lowercases to 'i/o') are matched as 'io'.
    """
    lowered = name.lower()
    norm = re.sub(r'[^a-z0-9]', '', lowered)
    if any(k in norm for k in ('io', 'write', 'output', 'save')):
        return 'io'
    if any(k in norm for k in ('assembly', 'assemble', 'build')):
        return 'assembly'
    if any(k in norm for k in ('solve', 'linear', 'iteration', 'cg', 'gmres')):
        return 'solver'
    return 'general'


def _phase_threshold(category: str) -> float:
    """Return the dominance threshold for a phase category."""
    if category == 'io':
        return IO_THRESHOLD
    return DEFAULT_THRESHOLD


def _load_json_safe(path: str, label: str) -> Dict:
    """Load a JSON file with size and structure validation."""
    file_size = os.path.getsize(path)
    if file_size > MAX_FILE_SIZE:
        raise ValueError(f"{label} file exceeds size limit ({file_size} > {MAX_FILE_SIZE}): {path}")
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{label} JSON root must be an object: {path}")
    return data


def load_analysis_results(timing_path: str, scaling_path: Optional[str] = None,
                          memory_path: Optional[str] = None) -> Dict:
    """
    Load analysis results from JSON files with validation.

    Args:
        timing_path: Path to timing analysis JSON
        scaling_path: Path to scaling analysis JSON (optional)
        memory_path: Path to memory profile JSON (optional)

    Returns:
        Combined analysis data
    """
    results = {}

    # Load timing data (required)
    try:
        results['timing'] = _load_json_safe(timing_path, "Timing")
    except FileNotFoundError:
        raise FileNotFoundError(f"Timing analysis file not found: {timing_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid timing JSON: {e}")

    # Load scaling data (optional)
    if scaling_path:
        try:
            results['scaling'] = _load_json_safe(scaling_path, "Scaling")
        except FileNotFoundError:
            print(f"Warning: Scaling file not found: {scaling_path}", file=sys.stderr)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Warning: Invalid scaling file: {e}", file=sys.stderr)

    # Load memory data (optional)
    if memory_path:
        try:
            results['memory'] = _load_json_safe(memory_path, "Memory")
        except FileNotFoundError:
            print(f"Warning: Memory file not found: {memory_path}", file=sys.stderr)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Warning: Invalid memory file: {e}", file=sys.stderr)

    return results


def detect_timing_bottlenecks(timing_data: Dict, threshold: Optional[float] = None) -> List[Dict]:
    """
    Detect timing bottlenecks from timing analysis.

    Reads the timing_analyzer.py output schema, where the payload is nested
    under a top-level 'results' key alongside 'inputs'. A bare payload (phases
    at the top level) is also accepted for backward compatibility.

    Per-type dominance thresholds are applied (matching the documented decision
    rules): I/O phases are flagged above 30%, all other phases above 50%. If an
    explicit ``threshold`` is provided it overrides the per-type defaults for
    every phase.

    Args:
        timing_data: Timing analysis results (analyzer output dict)
        threshold: Optional uniform percentage threshold override

    Returns:
        List of bottleneck dictionaries
    """
    bottlenecks = []

    # Resolve the payload: prefer the nested 'results' envelope, fall back to a
    # bare payload that carries 'phases' directly.
    payload = timing_data.get('results', timing_data)
    phases = payload.get('phases', []) if isinstance(payload, dict) else []

    for phase in phases:
        percentage = phase.get('percentage', 0)
        name = phase.get('name', '')
        category = _classify_phase(name)
        phase_threshold = threshold if threshold is not None else _phase_threshold(category)
        if percentage > phase_threshold:
            severity = 'high' if percentage > HIGH_SEVERITY_THRESHOLD else 'medium'
            bottlenecks.append({
                'type': 'timing',
                'phase': name,
                'category': category,
                'severity': severity,
                'metric': 'percentage',
                'value': percentage,
                'threshold': phase_threshold
            })

    return bottlenecks


def detect_scaling_bottlenecks(scaling_data: Dict, threshold: float = 0.70) -> List[Dict]:
    """
    Detect scaling bottlenecks from scaling analysis.
    
    Args:
        scaling_data: Scaling analysis results
        threshold: Efficiency threshold (default: 0.70)
    
    Returns:
        List of bottleneck dictionaries
    """
    bottlenecks = []

    # Resolve the payload from the scaling_analyzer.py output envelope.
    analysis = scaling_data.get('results', scaling_data)
    if not isinstance(analysis, dict):
        return bottlenecks
    avg_efficiency = analysis.get('average_efficiency', 1.0)
    
    if avg_efficiency < threshold:
        bottlenecks.append({
            'type': 'scaling',
            'phase': 'parallel_efficiency',
            'severity': 'high' if avg_efficiency < 0.5 else 'medium',
            'metric': 'efficiency',
            'value': avg_efficiency,
            'threshold': threshold
        })
    
    return bottlenecks


def detect_memory_bottlenecks(memory_data: Dict, threshold: float = 0.80) -> List[Dict]:
    """
    Detect memory bottlenecks from memory profile.
    
    Args:
        memory_data: Memory profile results
        threshold: Memory usage threshold (default: 0.80 = 80%)
    
    Returns:
        List of bottleneck dictionaries
    """
    bottlenecks = []

    # Resolve the payload from the memory_profiler.py output envelope.
    profile = memory_data.get('results', memory_data)
    if not isinstance(profile, dict):
        return bottlenecks

    # Check if warnings exist (indicates high memory usage)
    if profile.get('warnings'):
        total_memory = profile.get('total_memory_gb', 0)
        bottlenecks.append({
            'type': 'memory',
            'phase': 'memory_usage',
            'severity': 'high',
            'metric': 'total_memory_gb',
            'value': total_memory,
            'threshold': threshold
        })
    
    return bottlenecks


def generate_recommendations(bottlenecks: List[Dict], timing_data: Optional[Dict] = None) -> List[Dict]:
    """
    Generate optimization recommendations based on bottlenecks.
    
    Args:
        bottlenecks: List of detected bottlenecks
        timing_data: Optional timing data for context
    
    Returns:
        List of recommendation dictionaries
    """
    recommendations = []
    
    if not bottlenecks:
        recommendations.append({
            'priority': 'low',
            'category': 'general',
            'issue': 'No significant bottlenecks detected',
            'strategies': ['Performance appears balanced', 'Consider profiling at larger scale']
        })
        return recommendations
    
    # Process timing bottlenecks
    for bottleneck in bottlenecks:
        if bottleneck['type'] == 'timing':
            # Use the category recorded by detect_timing_bottlenecks (which
            # normalizes 'I/O' -> 'io'); fall back to re-classifying for
            # bottlenecks built without a category.
            category = bottleneck.get('category') or _classify_phase(bottleneck['phase'])

            # Solver-related bottlenecks
            if category == 'solver':
                recommendations.append({
                    'priority': 'high',
                    'category': 'solver',
                    'issue': f"{bottleneck['phase']} dominates runtime ({bottleneck['value']:.1f}%)",
                    'strategies': [
                        'Use algebraic multigrid (AMG) preconditioner',
                        'Tighten solver tolerance if over-solving',
                        'Consider direct solver for small problems',
                        'Profile matrix assembly vs solve time'
                    ]
                })
            
            # Assembly bottlenecks
            elif category == 'assembly':
                recommendations.append({
                    'priority': 'high',
                    'category': 'assembly',
                    'issue': f"{bottleneck['phase']} dominates runtime ({bottleneck['value']:.1f}%)",
                    'strategies': [
                        'Cache element matrices if geometry is static',
                        'Use vectorized assembly routines',
                        'Consider matrix-free methods',
                        'Parallelize assembly with coloring'
                    ]
                })
            
            # I/O bottlenecks
            elif category == 'io':
                recommendations.append({
                    'priority': 'medium',
                    'category': 'io',
                    'issue': f"{bottleneck['phase']} dominates runtime ({bottleneck['value']:.1f}%)",
                    'strategies': [
                        'Reduce output frequency',
                        'Use parallel I/O (HDF5, MPI-IO)',
                        'Write to fast scratch storage',
                        'Compress output data'
                    ]
                })
            
            # Generic timing bottleneck
            else:
                recommendations.append({
                    'priority': 'medium',
                    'category': 'general',
                    'issue': f"{bottleneck['phase']} dominates runtime ({bottleneck['value']:.1f}%)",
                    'strategies': [
                        'Profile this phase in detail',
                        'Look for algorithmic improvements',
                        'Consider parallelization opportunities'
                    ]
                })
        
        # Process scaling bottlenecks
        elif bottleneck['type'] == 'scaling':
            recommendations.append({
                'priority': 'high',
                'category': 'parallel',
                'issue': f"Poor parallel efficiency ({bottleneck['value']:.2f})",
                'strategies': [
                    'Investigate communication overhead',
                    'Check for load imbalance',
                    'Reduce synchronization points',
                    'Use asynchronous communication',
                    'Consider hybrid MPI+OpenMP'
                ]
            })
        
        # Process memory bottlenecks
        elif bottleneck['type'] == 'memory':
            recommendations.append({
                'priority': 'high',
                'category': 'memory',
                'issue': f"High memory usage ({bottleneck['value']:.2f} GB)",
                'strategies': [
                    'Reduce mesh resolution',
                    'Use iterative solver (lower memory than direct)',
                    'Enable out-of-core computation',
                    'Increase number of processors',
                    'Use single precision where appropriate'
                ]
            })
    
    return recommendations


def main():
    parser = argparse.ArgumentParser(
        description='Identify performance bottlenecks and recommend optimizations'
    )
    parser.add_argument('--timing', required=True, help='Path to timing analysis JSON')
    parser.add_argument('--scaling', help='Path to scaling analysis JSON (optional)')
    parser.add_argument('--memory', help='Path to memory profile JSON (optional)')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')
    
    args = parser.parse_args()
    
    try:
        # Load analysis results
        results = load_analysis_results(args.timing, args.scaling, args.memory)
        
        # Detect bottlenecks
        bottlenecks = []
        
        if 'timing' in results:
            bottlenecks.extend(detect_timing_bottlenecks(results['timing']))
        
        if 'scaling' in results:
            bottlenecks.extend(detect_scaling_bottlenecks(results['scaling']))
        
        if 'memory' in results:
            bottlenecks.extend(detect_memory_bottlenecks(results['memory']))
        
        # Generate recommendations
        recommendations = generate_recommendations(bottlenecks, results.get('timing'))
        
        # Format output
        if args.json:
            output = {
                'inputs': {
                    'timing_file': args.timing,
                    'scaling_file': args.scaling,
                    'memory_file': args.memory
                },
                'results': {
                    'bottlenecks': bottlenecks,
                    'recommendations': recommendations
                }
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"Bottleneck Analysis")
            print(f"=" * 60)
            
            if bottlenecks:
                print(f"\nDetected Bottlenecks:")
                for bottleneck in bottlenecks:
                    print(f"  [{bottleneck['severity'].upper()}] {bottleneck['phase']}: "
                          f"{bottleneck['metric']} = {bottleneck['value']:.2f}")
            else:
                print("\nNo significant bottlenecks detected")
            
            print(f"\nRecommendations:")
            for rec in recommendations:
                print(f"\n  [{rec['priority'].upper()}] {rec['category'].upper()}")
                print(f"  Issue: {rec['issue']}")
                print(f"  Strategies:")
                for strategy in rec['strategies']:
                    print(f"    - {strategy}")
    
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
        sys.exit(3)


if __name__ == '__main__':
    main()
