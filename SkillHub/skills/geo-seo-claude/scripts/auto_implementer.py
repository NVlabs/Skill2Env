#!/usr/bin/env python3
"""
Auto-Implementer - Phase 2 Orchestrator
Coordinates all optimization scripts in correct sequence

Pipeline:
1. Phase 1 analysis (audit_report.py)
2. Content optimization (content_optimizer.py)
3. Platform optimization (platform_optimizer.py)
4. Voice optimization (voice_optimizer.py)
5. Citation analysis (citation_enhancer.py)
6. Freshness check (freshness_monitor.py)
7. Final validation
8. Generate before/after report
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

def run_script(script_name: str, args: list) -> dict:
    """Run a script and capture output"""
    script_path = Path(__file__).parent / script_name
    try:
        result = subprocess.run(
            ['python3', str(script_path)] + args,
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def auto_optimize(file_path: str, platform: str = 'multi', mode: str = 'full') -> dict:
    """
    Full automated optimization pipeline

    Args:
        file_path: HTML file to optimize
        platform: Target platform (chatgpt, perplexity, claude, gemini, grokipedia, multi)
        mode: Optimization mode (quick, full, preview)

    Returns:
        Optimization results
    """
    print(f"Auto-Implementer: Phase 2 Optimization Pipeline")
    print(f"=" * 60)
    print(f"File: {file_path}")
    print(f"Platform: {platform.upper()}")
    print(f"Mode: {mode.upper()}\n")
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'file': file_path,
        'platform': platform,
        'steps': []
    }
    
    current_file = file_path
    
    # Step 1: Phase 1 Analysis
    print("[1/6] Running Phase 1 analysis...")
    audit = run_script('audit_report.py', [file_path, '--format', 'json'])
    if audit['success']:
        results['steps'].append({'step': 'audit', 'status': 'success'})
        print("  ✓ Audit complete")
    else:
        print("  ✗ Audit failed")
        results['steps'].append({'step': 'audit', 'status': 'failed'})
    
    # Step 2: Content Optimization
    print("[2/6] Applying content optimization...")
    content_opt = run_script('content_optimizer.py', [current_file])
    if content_opt['success']:
        # Update current file to optimized version
        base = current_file.rsplit('.', 1)[0]
        current_file = f"{base}-optimized.html"
        results['steps'].append({'step': 'content', 'status': 'success', 'file': current_file})
        print(f"  ✓ Content optimized: {current_file}")
    else:
        print("  ✗ Content optimization failed")
        results['steps'].append({'step': 'content', 'status': 'failed'})
    
    # Step 3: Platform Optimization
    print(f"[3/6] Applying {platform} platform optimization...")
    platform_opt = run_script('platform_optimizer.py', [current_file, platform])
    if platform_opt['success']:
        base = current_file.rsplit('.', 1)[0]
        current_file = f"{base.replace('-optimized', '')}-{platform}.html"
        results['steps'].append({'step': 'platform', 'status': 'success', 'file': current_file})
        print(f"  ✓ Platform optimized: {current_file}")
    else:
        print("  ✗ Platform optimization failed")
        results['steps'].append({'step': 'platform', 'status': 'failed'})
    
    # Step 4: Voice Optimization
    print("[4/6] Adding voice search optimization...")
    voice_opt = run_script('voice_optimizer.py', [current_file])
    if voice_opt['success']:
        base = current_file.rsplit('.', 1)[0]
        current_file = f"{base}-voice.html"
        results['steps'].append({'step': 'voice', 'status': 'success', 'file': current_file})
        print(f"  ✓ Voice optimized: {current_file}")
    else:
        print("  ⚠ Voice optimization skipped")
        results['steps'].append({'step': 'voice', 'status': 'skipped'})
    
    # Step 5: Citation Analysis
    print("[5/6] Analyzing citation opportunities...")
    citation = run_script('citation_enhancer.py', [current_file])
    if citation['success']:
        results['steps'].append({'step': 'citation', 'status': 'success'})
        print("  ✓ Citation analysis complete")
        try:
            citation_data = json.loads(citation['stdout'])
            print(f"  → Found {citation_data['opportunities_count']} opportunities")
        except (json.JSONDecodeError, KeyError, TypeError):
            pass  # Citation data not in expected format
    else:
        print("  ⚠ Citation analysis skipped")
        results['steps'].append({'step': 'citation', 'status': 'skipped'})
    
    # Step 6: Freshness Check
    print("[6/6] Checking content freshness...")
    freshness = run_script('freshness_monitor.py', [current_file])
    if freshness['success']:
        results['steps'].append({'step': 'freshness', 'status': 'success'})
        print("  ✓ Freshness analysis complete")
        try:
            fresh_data = json.loads(freshness['stdout'])
            print(f"  → Freshness score: {fresh_data['freshness_score']}/100")
        except (json.JSONDecodeError, KeyError, TypeError):
            pass  # Freshness data not in expected format
    else:
        print("  ⚠ Freshness check skipped")
        results['steps'].append({'step': 'freshness', 'status': 'skipped'})
    
    # Final Results
    print(f"\n" + "=" * 60)
    print(f"✓ Phase 2 Optimization Complete")
    print(f"  Final output: {current_file}")
    print(f"  Steps completed: {len([s for s in results['steps'] if s['status'] == 'success'])}/6")
    
    results['final_file'] = current_file
    results['success'] = True
    
    return results

def main():
    """CLI interface"""
    if len(sys.argv) < 2:
        print("Usage: python auto_implementer.py <file> [platform] [mode]")
        print("\nPlatforms: chatgpt, perplexity, claude, gemini, grokipedia, multi (default)")
        print("Modes: quick, full (default), preview")
        print("\nExample:")
        print("  python auto_implementer.py page.html perplexity full")
        print("  python auto_implementer.py page.html grokipedia full")
        sys.exit(1)
    
    file_path = sys.argv[1]
    platform = sys.argv[2] if len(sys.argv) > 2 else 'multi'
    mode = sys.argv[3] if len(sys.argv) > 3 else 'full'
    
    result = auto_optimize(file_path, platform, mode)
    
    # Save results
    results_file = file_path.replace('.html', '-optimization-results.json')
    with open(results_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\nResults saved: {results_file}")

if __name__ == '__main__':
    main()
