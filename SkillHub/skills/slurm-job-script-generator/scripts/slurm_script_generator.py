#!/usr/bin/env python3
"""Generate a SLURM sbatch script from resource and launch parameters."""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import sys
from typing import Dict, List, Optional, Sequence, Tuple, TypedDict


_JOB_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
_WALLTIME_RE = re.compile(r"^(?:(?P<days>[0-9]+)-)?(?P<hours>[0-9]{1,3}):(?P<mins>[0-9]{2}):(?P<secs>[0-9]{2})$")
# Slurm memory flags (--mem, --mem-per-cpu) accept integer MB by default, or an
# integer with a suffix in [K|M|G|T]. Keep validation strict to avoid generating
# scripts that Slurm rejects. (This describes Slurm's format convention; only
# --mem and --mem-per-cpu are exposed as CLI flags.)
_MEM_RE = re.compile(r"^[0-9]+(?:[KMGT])?$", re.IGNORECASE)
_ENV_KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
# Safe-character allowlist for SLURM identifier-style fields (partition, account,
# qos, constraint, reservation). These are emitted unquoted into #SBATCH lines,
# so we forbid shell metacharacters and whitespace.
_IDENT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:,+-]{0,127}$")
# Module specs may include a slash for version (e.g. openmpi/4.1). Forbid shell
# metacharacters that could escape the `module load` directive.
_MODULE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/+-]{0,127}$")

# Launcher basenames that already establish an MPI launch context. If the user's
# run command starts with one of these, the generator must not wrap it in srun.
_NESTED_LAUNCHERS = frozenset(
    {"srun", "mpirun", "mpiexec", "mpiexec.hydra", "orterun", "aprun", "jsrun"}
)

# Upper bounds for integer resource requests. These guard against typos /
# pathological requests; they are generous enough for any real cluster.
_MAX_NODES = 100_000
_MAX_NTASKS = 10_000_000
_MAX_CPUS_PER_TASK = 4_096
_MAX_GPUS_PER_NODE = 64
_MAX_CORES_PER_NODE = 4_096

class SlurmResources(TypedDict):
    nodes: int
    ntasks: int
    ntasks_per_node: Optional[int]
    cpus_per_task: int
    mem: Optional[str]
    mem_per_cpu: Optional[str]
    gpus_per_node: Optional[int]
    gpu_type: Optional[str]


def _validate_job_name(name: str) -> str:
    if not name or not _JOB_NAME_RE.match(name):
        raise ValueError(
            "job-name must match /^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$/ (no spaces)"
        )
    return name


def _normalize_walltime(value: str) -> str:
    m = _WALLTIME_RE.match(value.strip())
    if not m:
        raise ValueError("time must be HH:MM:SS or D-HH:MM:SS")
    days = int(m.group("days") or "0")
    hours = int(m.group("hours"))
    mins = int(m.group("mins"))
    secs = int(m.group("secs"))
    if days < 0 or hours < 0:
        raise ValueError("time must be non-negative")
    if not (0 <= mins <= 59) or not (0 <= secs <= 59):
        raise ValueError("time minutes/seconds must be in [00,59]")
    if days > 0:
        return f"{days}-{hours:02d}:{mins:02d}:{secs:02d}"
    return f"{hours:02d}:{mins:02d}:{secs:02d}"


def _validate_positive_int(name: str, value: int, upper: Optional[int] = None) -> int:
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    if upper is not None and value > upper:
        raise ValueError(f"{name} must be <= {upper} (got {value})")
    return value


def _validate_identifier(flag: str, value: Optional[str]) -> Optional[str]:
    """Validate a SLURM identifier-style field against a safe-character allowlist.

    These values are emitted unquoted into #SBATCH directives, so they must not
    contain shell metacharacters or whitespace.
    """
    if value is None:
        return None
    v = value.strip()
    if not v:
        raise ValueError(f"{flag} must be non-empty when provided")
    if not _IDENT_RE.match(v):
        raise ValueError(
            f"{flag} must match /^[A-Za-z0-9][A-Za-z0-9._:,+-]{{0,127}}$/ "
            "(no spaces or shell metacharacters)"
        )
    return v


def _validate_modules(modules: Sequence[str]) -> List[str]:
    out: List[str] = []
    for mod in modules:
        m = mod.strip()
        if not m or not _MODULE_RE.match(m):
            raise ValueError(
                f"module must match /^[A-Za-z0-9][A-Za-z0-9._/+-]{{0,127}}$/ "
                f"(no shell metacharacters); got {mod!r}"
            )
        out.append(m)
    return out


def _validate_mem_spec(flag: str, value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    v = value.strip()
    if not v:
        raise ValueError(f"{flag} must be non-empty when provided")
    if not _MEM_RE.match(v):
        raise ValueError(
            f"{flag} must be an integer (MB) or an integer with suffix in [K|M|G|T] (e.g. 16000M, 16G)"
        )
    return v


def _validate_env_kv(pairs: Sequence[str]) -> List[Tuple[str, str]]:
    out: List[Tuple[str, str]] = []
    for item in pairs:
        if "=" not in item:
            raise ValueError(f"env must be KEY=VALUE (got {item!r})")
        key, value = item.split("=", 1)
        key = key.strip()
        if not _ENV_KEY_RE.match(key):
            raise ValueError(f"env key must be a valid identifier (got {key!r})")
        out.append((key, value))
    return out


def build_resources(
    *,
    nodes: int,
    ntasks: Optional[int],
    ntasks_per_node: Optional[int],
    cpus_per_task: int,
    mem: Optional[str],
    mem_per_cpu: Optional[str],
    gpus_per_node: Optional[int],
    gpu_type: Optional[str],
) -> SlurmResources:
    """Pure function: validate and normalize resource request."""
    nodes = _validate_positive_int("nodes", nodes, _MAX_NODES)
    cpus_per_task = _validate_positive_int(
        "cpus-per-task", cpus_per_task, _MAX_CPUS_PER_TASK
    )

    if ntasks is not None and ntasks_per_node is not None:
        raise ValueError("Provide either --ntasks or --ntasks-per-node, not both")

    if ntasks_per_node is not None:
        ntasks_per_node = _validate_positive_int(
            "ntasks-per-node", ntasks_per_node, _MAX_NTASKS
        )
        derived_ntasks = nodes * ntasks_per_node
        ntasks = _validate_positive_int("ntasks", derived_ntasks, _MAX_NTASKS)
    else:
        ntasks = _validate_positive_int("ntasks", ntasks or 1, _MAX_NTASKS)

    mem = _validate_mem_spec("--mem", mem)
    mem_per_cpu = _validate_mem_spec("--mem-per-cpu", mem_per_cpu)
    if mem is not None and mem_per_cpu is not None:
        raise ValueError("Provide either --mem or --mem-per-cpu, not both")

    if gpus_per_node is not None:
        gpus_per_node = _validate_positive_int(
            "gpus-per-node", gpus_per_node, _MAX_GPUS_PER_NODE
        )
        if gpu_type is not None:
            gpu_type = _validate_identifier("gpu-type", gpu_type)

    return {
        "nodes": nodes,
        "ntasks": ntasks,
        "ntasks_per_node": ntasks_per_node,
        "cpus_per_task": cpus_per_task,
        "mem": mem,
        "mem_per_cpu": mem_per_cpu,
        "gpus_per_node": gpus_per_node,
        "gpu_type": gpu_type,
    }


def generate_sbatch_script(
    *,
    job_name: str,
    time_limit: str,
    partition: Optional[str],
    account: Optional[str],
    qos: Optional[str],
    constraint: Optional[str],
    reservation: Optional[str],
    exclusive: bool,
    output: Optional[str],
    error: Optional[str],
    mail_user: Optional[str],
    mail_type: Optional[str],
    workdir: Optional[str],
    modules: Sequence[str],
    env: Sequence[str],
    launcher: str,
    srun_extra: Optional[str],
    command: Sequence[str],
    resources: SlurmResources,
    cores_per_node: Optional[int] = None,
) -> Dict[str, object]:
    """Pure function: return JSON payload with the generated sbatch script."""
    job_name = _validate_job_name(job_name)
    time_limit = _normalize_walltime(time_limit)
    if not command:
        raise ValueError("Provide a run command after --")

    # Validate identifier-style fields against a safe-character allowlist before
    # they are emitted unquoted into #SBATCH directives.
    partition = _validate_identifier("--partition", partition)
    account = _validate_identifier("--account", account)
    qos = _validate_identifier("--qos", qos)
    constraint = _validate_identifier("--constraint", constraint)
    reservation = _validate_identifier("--reservation", reservation)
    modules = _validate_modules(modules)

    if launcher not in ("srun", "none"):
        raise ValueError("launcher must be one of: srun, none")

    directives: List[str] = []
    directives.append(f"#SBATCH --job-name={job_name}")
    directives.append(f"#SBATCH --time={time_limit}")
    directives.append(f"#SBATCH --nodes={resources['nodes']}")

    if partition:
        directives.append(f"#SBATCH --partition={partition}")
    if account:
        directives.append(f"#SBATCH --account={account}")
    if qos:
        directives.append(f"#SBATCH --qos={qos}")

    if resources["ntasks_per_node"] is not None:
        directives.append(f"#SBATCH --ntasks-per-node={resources['ntasks_per_node']}")
    else:
        directives.append(f"#SBATCH --ntasks={resources['ntasks']}")
    directives.append(f"#SBATCH --cpus-per-task={resources['cpus_per_task']}")

    if resources["mem"] is not None:
        directives.append(f"#SBATCH --mem={resources['mem']}")
    if resources["mem_per_cpu"] is not None:
        directives.append(f"#SBATCH --mem-per-cpu={resources['mem_per_cpu']}")

    if resources["gpus_per_node"] is not None:
        if resources["gpu_type"]:
            directives.append(
                f"#SBATCH --gres=gpu:{resources['gpu_type']}:{resources['gpus_per_node']}"
            )
        else:
            directives.append(f"#SBATCH --gres=gpu:{resources['gpus_per_node']}")

    if output:
        directives.append(f"#SBATCH --output={output}")
    if error:
        directives.append(f"#SBATCH --error={error}")

    if mail_user:
        directives.append(f"#SBATCH --mail-user={mail_user}")
        if mail_type:
            directives.append(f"#SBATCH --mail-type={mail_type}")

    if constraint:
        directives.append(f"#SBATCH --constraint={constraint}")
    if reservation:
        directives.append(f"#SBATCH --reservation={reservation}")
    if exclusive:
        directives.append("#SBATCH --exclusive")

    warnings: List[str] = []
    derived: Dict[str, object] = {
        "ntasks": resources["ntasks"],
        "ntasks_per_node": resources["ntasks_per_node"],
        "cpus_total_requested": resources["ntasks"] * resources["cpus_per_task"],
    }

    if cores_per_node is not None:
        cores_per_node = _validate_positive_int(
            "cores-per-node", cores_per_node, _MAX_CORES_PER_NODE
        )
        derived["cores_per_node"] = cores_per_node
        if resources["ntasks_per_node"] is not None:
            per_node = resources["ntasks_per_node"] * resources["cpus_per_task"]
            derived["cpus_per_node_requested"] = per_node
            if per_node > cores_per_node:
                warnings.append(
                    f"Oversubscription risk: ntasks-per-node*cpus-per-task={per_node} > cores-per-node={cores_per_node}"
                )

    # GPU layout sanity check: when GPUs are requested, derive the rank-to-GPU
    # mapping and warn if ranks do not divide evenly across the allocated GPUs.
    if resources["gpus_per_node"] is not None:
        total_gpus = resources["nodes"] * resources["gpus_per_node"]
        derived["total_gpus"] = total_gpus
        ranks_per_gpu = resources["ntasks"] / total_gpus
        derived["ranks_per_gpu"] = ranks_per_gpu
        if resources["ntasks"] % total_gpus != 0:
            warnings.append(
                f"Task-to-GPU ratio is not an integer: ntasks={resources['ntasks']} "
                f"is not divisible by total GPUs={total_gpus} "
                f"(nodes={resources['nodes']} * gpus-per-node={resources['gpus_per_node']}). "
                "Ranks will not map evenly to devices; consider --gpu-bind or "
                "intentional MPS sharing."
            )

    env_pairs = _validate_env_kv(env)

    cmd_str = " ".join(shlex.quote(x) for x in command)
    effective_launcher = launcher
    if launcher == "srun":
        first_tok = os.path.basename(command[0]) if command else ""
        if first_tok in _NESTED_LAUNCHERS:
            # The run command already starts with a launcher (e.g. mpirun, srun).
            # Wrapping it in another srun would spawn N independent copies of the
            # inner launcher (each starting its own MPI world) or nest srun
            # invocations, which is malformed. Treat as launcher='none' and warn.
            effective_launcher = "none"
            warnings.append(
                f"Run command already starts with a launcher ({first_tok!r}); "
                "skipping the automatic 'srun' wrap (equivalent to --launcher none). "
                "Pass --launcher none explicitly to silence this warning."
            )

    if effective_launcher == "srun":
        srun_bits = [
            "srun",
            f"--ntasks={resources['ntasks']}",
            f"--cpus-per-task={resources['cpus_per_task']}",
        ]
        if srun_extra:
            # Tokenize honoring existing quoting, then re-quote each token so no
            # shell metacharacter (;, |, &, $, backticks, ...) can inject a live
            # command into the run line.
            try:
                srun_tokens = shlex.split(srun_extra.strip())
            except ValueError as exc:
                raise ValueError(f"--srun-extra is not valid shell syntax: {exc}")
            srun_bits.extend(shlex.quote(tok) for tok in srun_tokens)
        run_line = " ".join(srun_bits + [cmd_str])
    elif effective_launcher == "none":
        run_line = cmd_str
    else:
        raise ValueError("launcher must be one of: srun, none")

    lines: List[str] = []
    # Per SchedMD's sbatch spec, once the first non-comment, non-whitespace line
    # is reached, no further #SBATCH directives are processed. Therefore all
    # directives must immediately follow the shebang and precede any executable
    # command (such as `set -euo pipefail`).
    lines.append("#!/usr/bin/env bash")
    lines.extend(directives)
    lines.append("")
    lines.append("set -euo pipefail")
    lines.append("")

    lines.append('echo "job_id=${SLURM_JOB_ID:-unknown} start=$(date)"')
    lines.append('echo "node_list=${SLURM_JOB_NODELIST:-unknown}"')

    # Working directory
    if workdir:
        lines.append(f"cd {shlex.quote(workdir)}")
    else:
        lines.append('cd "${SLURM_SUBMIT_DIR:-$PWD}"')
    lines.append('echo "pwd=$(pwd)"')
    lines.append("")

    # Optional module loading
    if modules:
        lines.append("if command -v module >/dev/null 2>&1; then")
        lines.append("  module purge || true")
        for mod in modules:
            lines.append(f"  module load {shlex.quote(mod)}")
        lines.append("else")
        lines.append('  echo "warning: environment modules not available; skipping module load" >&2')
        lines.append("fi")
        lines.append("")

    # Threading environment
    lines.append(f"export OMP_NUM_THREADS={resources['cpus_per_task']}")
    lines.append("export OMP_PLACES=cores")
    lines.append("export OMP_PROC_BIND=close")
    for key, value in env_pairs:
        lines.append(f"export {key}={shlex.quote(value)}")
    lines.append("")

    lines.append(run_line)
    lines.append("")
    lines.append('echo "job_id=${SLURM_JOB_ID:-unknown} end=$(date)"')

    script = "\n".join(lines) + "\n"

    return {
        "inputs": {
            "job_name": job_name,
            "time": time_limit,
            "partition": partition,
            "account": account,
            "nodes": resources["nodes"],
            "ntasks": resources["ntasks"],
            "ntasks_per_node": resources["ntasks_per_node"],
            "cpus_per_task": resources["cpus_per_task"],
            "mem": resources["mem"],
            "mem_per_cpu": resources["mem_per_cpu"],
            "gpus_per_node": resources["gpus_per_node"],
            "gpu_type": resources["gpu_type"],
            "workdir": workdir,
            "modules": list(modules),
            "env": list(env),
            "launcher": launcher,
            "srun_extra": srun_extra,
            "command": list(command),
        },
        "results": {
            "directives": directives,
            "derived": derived,
            "warnings": warnings,
            "run_line": run_line,
            "script": script,
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a SLURM sbatch script from resource and launch parameters.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("--job-name", required=True, help="SLURM job name (no spaces)")
    parser.add_argument(
        "--time",
        required=True,
        help="Walltime limit (HH:MM:SS or D-HH:MM:SS)",
    )
    parser.add_argument("--partition", default=None, help="SLURM partition")
    parser.add_argument("--account", default=None, help="SLURM account/project")
    parser.add_argument("--qos", default=None, help="SLURM QoS")
    parser.add_argument("--constraint", default=None, help="SLURM constraint")
    parser.add_argument("--reservation", default=None, help="SLURM reservation")
    parser.add_argument("--exclusive", action="store_true", help="Request exclusive node access")

    parser.add_argument("--nodes", type=int, default=1, help="Number of nodes")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--ntasks", type=int, default=None, help="Total MPI tasks/ranks")
    group.add_argument(
        "--ntasks-per-node",
        type=int,
        default=None,
        help="MPI tasks/ranks per node",
    )
    parser.add_argument(
        "--cpus-per-task",
        type=int,
        default=1,
        help="CPU cores per task (OpenMP threads)",
    )

    parser.add_argument("--mem", default=None, help="Memory per node (e.g. 32G)")
    parser.add_argument(
        "--mem-per-cpu",
        default=None,
        help="Memory per CPU core (e.g. 2G)",
    )
    parser.add_argument("--gpus-per-node", type=int, default=None, help="GPUs per node")
    parser.add_argument("--gpu-type", default=None, help="GPU type for --gres (optional)")

    parser.add_argument("--output", default=None, help="Stdout file pattern (e.g. slurm-%%j.out)")
    parser.add_argument("--error", default=None, help="Stderr file pattern (e.g. slurm-%%j.err)")
    parser.add_argument("--mail-user", default=None, help="Email address for notifications")
    parser.add_argument("--mail-type", default=None, help="Mail types (e.g. END,FAIL)")

    parser.add_argument(
        "--workdir",
        default=None,
        help="Working directory (default: SLURM_SUBMIT_DIR)",
    )
    parser.add_argument(
        "--module",
        action="append",
        default=[],
        help="Module to load (repeatable)",
    )
    parser.add_argument(
        "--env",
        action="append",
        default=[],
        help="Environment variable KEY=VALUE (repeatable)",
    )

    parser.add_argument(
        "--launcher",
        choices=["srun", "none"],
        default="srun",
        help="How to launch the command inside the allocation",
    )
    parser.add_argument(
        "--srun-extra",
        default=None,
        help="Extra text appended to the srun invocation (advanced)",
    )

    parser.add_argument(
        "--cores-per-node",
        type=int,
        default=None,
        help="Optional sanity-check: physical cores per node for oversubscription warnings",
    )
    parser.add_argument("--out", default=None, help="Write the script to this path")
    parser.add_argument("--json", action="store_true", help="Emit JSON payload")

    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="Command to run after `--` (e.g. -- ./simulate --config cfg.json)",
    )
    return parser.parse_args()


def _write_text(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    with open(path, "w", newline="\n") as f:
        f.write(text)


def main() -> None:
    args = parse_args()
    # argparse includes the `--` separator only as an option terminator, not in the remainder
    command = [c for c in args.command if c != "--"]

    try:
        resources = build_resources(
            nodes=args.nodes,
            ntasks=args.ntasks,
            ntasks_per_node=args.ntasks_per_node,
            cpus_per_task=args.cpus_per_task,
            mem=args.mem,
            mem_per_cpu=args.mem_per_cpu,
            gpus_per_node=args.gpus_per_node,
            gpu_type=args.gpu_type,
        )
        payload = generate_sbatch_script(
            job_name=args.job_name,
            time_limit=args.time,
            partition=args.partition,
            account=args.account,
            qos=args.qos,
            constraint=args.constraint,
            reservation=args.reservation,
            exclusive=args.exclusive,
            output=args.output,
            error=args.error,
            mail_user=args.mail_user,
            mail_type=args.mail_type,
            workdir=args.workdir,
            modules=args.module,
            env=args.env,
            launcher=args.launcher,
            srun_extra=args.srun_extra,
            command=command,
            resources=resources,
            cores_per_node=args.cores_per_node,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)

    script = str(payload["results"]["script"])
    if args.out:
        try:
            _write_text(args.out, script)
        except OSError as exc:
            print(f"Failed to write {args.out}: {exc}", file=sys.stderr)
            sys.exit(1)

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return

    if args.out:
        print(f"Wrote {args.out}")
        return

    print(script, end="")


if __name__ == "__main__":
    main()
