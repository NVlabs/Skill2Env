#!/usr/bin/env python3
"""Plan molecular dynamics trajectory analysis tasks."""
from __future__ import annotations

import argparse
import json
import math
import sys
from typing import Dict, List


GOAL_MAP = {
    "rdf": ("radial distribution function", ["positions", "cell", "species"]),
    "coordination": ("coordination number", ["positions", "cell", "species", "cutoff rule"]),
    "bond-angle": ("bond-angle distribution", ["positions", "neighbor list", "species"]),
    "diffusion": ("MSD and diffusion coefficient", ["unwrapped positions", "time axis"]),
    "msd": ("MSD and diffusion coefficient", ["unwrapped positions", "time axis"]),
    "vacf": ("velocity autocorrelation", ["velocities", "time axis"]),
    "vdos": ("vibrational density of states", ["velocities", "time axis"]),
    "stress-strain": ("stress-strain curve", ["stress or virial", "strain history"]),
    "equilibration": ("equilibration diagnostics", ["thermo history", "time axis"]),
}


# Ordering of analysis-plan statuses from most to least severe. A more-severe
# status must never be silently demoted to a less-severe one (e.g. a VACF/VDOS
# goal that is "blocked" because no velocities are stored must stay "blocked"
# even when the timestep is also missing).
SEVERITY = {"blocked": 3, "needs time axis": 2, "needs review": 1, "ready": 0}

# Lightweight input caps so a planning helper never has to materialise pathological
# input. These mirror the safeguards advertised in SKILL.md "## Security".
MAX_GOALS = 64
MAX_SYSTEM_LEN = 256
MAX_FIELD_LEN = 256


def _escalate(current: str, candidate: str) -> str:
    """Return the more-severe of two statuses (never demote)."""
    return max(current, candidate, key=lambda s: SEVERITY[s])


def _split_goals(value: str) -> List[str]:
    return [item.strip().lower() for item in value.split(",") if item.strip()]


def plan_md_analysis(
    system: str,
    goals: List[str],
    trajectory_format: str,
    has_velocities: bool,
    has_stress: bool,
    unwrap_needed: bool,
    timestep_fs: float | None,
) -> Dict:
    if not system.strip():
        raise ValueError("system must not be empty")
    if len(system) > MAX_SYSTEM_LEN:
        raise ValueError(f"system must be at most {MAX_SYSTEM_LEN} characters")
    if not goals:
        raise ValueError("at least one goal is required")
    if len(goals) > MAX_GOALS:
        raise ValueError(f"at most {MAX_GOALS} goals are allowed")
    for goal in goals:
        if len(goal) > MAX_FIELD_LEN:
            raise ValueError(f"goal must be at most {MAX_FIELD_LEN} characters")
    if len(trajectory_format) > MAX_FIELD_LEN:
        raise ValueError(f"trajectory_format must be at most {MAX_FIELD_LEN} characters")
    if timestep_fs is not None and (not math.isfinite(timestep_fs) or timestep_fs <= 0):
        raise ValueError("timestep_fs must be a positive finite number")

    analyses = []
    required_data = set()
    warnings: List[str] = []
    for goal in goals:
        if goal not in GOAL_MAP:
            warnings.append(f"Unknown goal {goal!r}; add a custom analysis note.")
            analyses.append({"goal": goal, "method": "custom analysis", "status": "needs review"})
            continue
        method, requirements = GOAL_MAP[goal]
        status = "ready"
        if goal in {"vacf", "vdos"} and not has_velocities:
            status = _escalate(status, "blocked")
            warnings.append(f"{goal} needs velocities or a defensible finite-difference velocity estimate.")
        if goal == "stress-strain" and not has_stress:
            status = _escalate(status, "blocked")
            warnings.append("stress-strain analysis needs stress/virial output and strain history.")
        if goal in {"diffusion", "msd"}:
            if unwrap_needed:
                warnings.append("Diffusion analysis requires unwrapped trajectories before fitting MSD.")
                # Performing the unwrap (as opposed to consuming already-unwrapped
                # positions) needs the simulation cell and per-atom image flags.
                required_data.update({"cell", "image flags"})
            warnings.append(
                "Verify the diffusive regime: MSD vs time should be linear "
                "(log-log slope ~1) before fitting D = lim MSD/(2*d*t); "
                "exclude ballistic and sub-diffusive transients."
            )
            warnings.append(
                "Apply a finite-size correction to D (Yeh-Hummer 1/L): "
                "D_0 = D_PBC + k_B*T*xi/(6*pi*eta*L), xi~=2.837 for a cubic box; "
                "needs box length L and shear viscosity eta."
            )
        if goal in {"diffusion", "msd", "vacf", "vdos", "equilibration"} and timestep_fs is None:
            status = _escalate(status, "needs time axis")
            warnings.append(f"{goal} needs timestep or saved-frame spacing.")
        required_data.update(requirements)
        analyses.append({"goal": goal, "method": method, "status": status})

    return {
        "analysis_plan": analyses,
        "required_data": sorted(required_data),
        "equilibration_checks": [
            "discard startup transient before property fits",
            "check temperature and pressure plateaus",
            "compare first-half and second-half property estimates",
            "use block averaging for uncertainty",
        ],
        "pbc_handling": {
            "unwrap_needed": unwrap_needed,
            "minimum_action": "unwrap before displacement-based analysis" if unwrap_needed else "confirm wrapping convention",
            "format_note": f"Check image flags or cell metadata for {trajectory_format}",
        },
        "warnings": warnings,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--system", required=True)
    parser.add_argument("--goals", required=True, help="Comma-separated goals")
    parser.add_argument("--trajectory-format", default="unknown")
    parser.add_argument("--has-velocities", action="store_true")
    parser.add_argument("--has-stress", action="store_true")
    parser.add_argument("--unwrap-needed", action="store_true")
    parser.add_argument("--timestep-fs", type=float)
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        results = plan_md_analysis(
            system=args.system,
            goals=_split_goals(args.goals),
            trajectory_format=args.trajectory_format,
            has_velocities=args.has_velocities,
            has_stress=args.has_stress,
            unwrap_needed=args.unwrap_needed,
            timestep_fs=args.timestep_fs,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    payload = {
        "inputs": {
            "system": args.system,
            "goals": _split_goals(args.goals),
            "trajectory_format": args.trajectory_format,
            "has_velocities": args.has_velocities,
            "has_stress": args.has_stress,
            "unwrap_needed": args.unwrap_needed,
            "timestep_fs": args.timestep_fs,
        },
        "results": results,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print("Analysis plan:")
        for item in results["analysis_plan"]:
            print(f"- {item['goal']}: {item['method']} ({item['status']})")
        if results["required_data"]:
            print("Required data:")
            for item in results["required_data"]:
                print(f"- {item}")
        print(f"PBC: {results['pbc_handling']['minimum_action']}")
        if results["warnings"]:
            # Safety-critical content: print to both stdout and stderr so it
            # stays visible even when stdout is piped elsewhere.
            print("Warnings:")
            for warning in results["warnings"]:
                print(f"- {warning}")
            print("Warnings:", file=sys.stderr)
            for warning in results["warnings"]:
                print(f"- {warning}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
