# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Command-line entry point for skill2env."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from rich.progress import BarColumn, Progress, TextColumn, TimeElapsedColumn

from .batch import BatchConfig, BatchRunner, create_batch_tracker, discover_skills
from .generator import (
    DEFAULT_CODEX_VERSION,
    DEFAULT_MAX_CODEX_ATTEMPTS,
    DEFAULT_MODEL,
    DEFAULT_REASONING_EFFORT,
    DEFAULT_RETRY_BASE_DELAY_SEC,
    MAX_WORKFLOWS,
    REASONING_EFFORTS,
    ContainerizedCodexRunner,
    GeneratorError,
    default_generator_image,
)
from .submit import SubmitError, submit_tasks
from .tracker import RunTracker, default_runs_root, new_run_id
from .validation import DEFAULT_MAX_TASK_SIZE_MIB


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="skill2env")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser(
        "generate",
        description="Generate host-validated Harbor tasks from every SKILL.md below an input root",
    )
    generate.add_argument(
        "--input-root",
        type=Path,
        required=True,
        help="Directory scanned recursively for SKILL.md (a directory with one SKILL.md works too)",
    )
    generate.add_argument("--out", type=Path, required=True)
    generate.add_argument(
        "--run-dir",
        type=Path,
        help="Run state directory (default: .skill2env/runs/<run-id>)",
    )
    generate.add_argument(
        "--max-tasks-per-skill",
        type=int,
        default=None,
        help=(
            "Optional cap on tasks per skill. By default the planner agent decides "
            f"(one task per identified workflow, up to {MAX_WORKFLOWS})"
        ),
    )
    generate.add_argument(
        "--max-parallel-workers",
        type=int,
        default=4,
        help="Maximum Codex agents (planner + creators) running concurrently across the batch",
    )
    generate.add_argument(
        "--max-task-size-mib",
        type=int,
        default=DEFAULT_MAX_TASK_SIZE_MIB,
        help=(
            "Maximum completed public task size before acceptance "
            f"(default: {DEFAULT_MAX_TASK_SIZE_MIB} MiB)"
        ),
    )
    generate.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="Pinned Codex model identifier used by task creators",
    )
    generate.add_argument(
        "--reasoning-effort",
        choices=REASONING_EFFORTS,
        default=DEFAULT_REASONING_EFFORT,
        help="Codex reasoning effort used by task creators",
    )
    generate.add_argument("--codex-version", default=DEFAULT_CODEX_VERSION)
    generate.add_argument(
        "--generator-image",
        help="Prebuilt Codex image (default builds skill2env's pinned image)",
    )
    generate.add_argument(
        "--auth-json",
        type=Path,
        default=Path("~/.codex/auth.json"),
        help="Codex auth file created by 'codex login' (default: ~/.codex/auth.json)",
    )
    generate.add_argument("--creator-timeout-sec", type=int, default=3600)
    generate.add_argument(
        "--codex-max-attempts",
        type=int,
        default=DEFAULT_MAX_CODEX_ATTEMPTS,
        help="Attempts per Codex call before a transient failure (rate limit, auth refresh race) becomes fatal",
    )
    generate.add_argument(
        "--codex-retry-base-sec",
        type=float,
        default=DEFAULT_RETRY_BASE_DELAY_SEC,
        help="First retry delay; doubles per attempt with jitter, capped at 5 minutes",
    )
    generate.add_argument(
        "--resume",
        action="store_true",
        help="Skip skills already finished by a previous run into the same --out root",
    )

    submit = subparsers.add_parser(
        "submit",
        description=(
            "Publish generated tasks to the Harbor hub registry "
            "(https://hub.harborframework.com). Requires 'harbor auth login'."
        ),
    )
    submit.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="Task directories or corpus roots (scanned recursively for task.toml)",
    )
    submit.add_argument(
        "--org",
        help="Rewrite the task package org before publishing (task.name becomes <org>/<task>)",
    )
    submit.add_argument(
        "--tag",
        action="append",
        default=[],
        help="Registry tag to apply (repeatable); 'latest' is always added",
    )
    submit.add_argument(
        "--public",
        action="store_true",
        help="Publish publicly (default: private to the publishing org)",
    )
    submit.add_argument(
        "--concurrency",
        type=int,
        default=None,
        help="Maximum concurrent uploads (harbor publish default: 50)",
    )
    submit.add_argument(
        "--dry-run",
        action="store_true",
        help="List the tasks that would be published and exit",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> None:
    args = build_parser().parse_args(argv)
    if args.command == "generate":
        _validate_generation_args(args)
        _run_generate(args)
        return
    if args.command == "submit":
        _run_submit(args)
        return
    raise SystemExit(f"unknown command: {args.command}")


def _run_generate(args: argparse.Namespace) -> None:
    input_root = args.input_root.expanduser().resolve()
    if not input_root.is_dir():
        raise SystemExit(f"--input-root is not a directory: {input_root}")
    output_root = args.out.expanduser().resolve()
    run_id = new_run_id()
    run_dir = (
        args.run_dir.expanduser().resolve()
        if args.run_dir
        else (default_runs_root() / run_id).resolve()
    )
    if (run_dir / "manifest.json").exists():
        raise SystemExit(f"--run-dir already contains a run: {run_dir}")
    image = args.generator_image or default_generator_image(args.codex_version)
    config = BatchConfig(
        input_root=input_root,
        output_root=output_root,
        run_dir=run_dir,
        model=args.model,
        reasoning_effort=args.reasoning_effort,
        codex_version=args.codex_version,
        generator_image=image,
        max_tasks_per_skill=args.max_tasks_per_skill,
        max_parallel_workers=args.max_parallel_workers,
        max_task_size_mib=args.max_task_size_mib,
        resume=args.resume,
    )
    specs = discover_skills(input_root, output_root, run_dir)
    if not specs:
        raise SystemExit(f"no SKILL.md files found under: {input_root}")
    tracker = create_batch_tracker(config, specs)
    print(f"Run state and creator logs: {run_dir}")
    runner = _make_runner(args, tracker)
    tracker.update_run("Preparing generator image")
    print("Preparing generator image...")
    try:
        runner.prepare()
    except GeneratorError as exc:
        _finish_setup_failure(tracker, f"generator setup failed [{exc.code}]: {exc}")
        raise SystemExit(f"generator setup failed [{exc.code}]: {exc}") from exc
    except KeyboardInterrupt:
        _finish_interrupted(tracker, "Generation interrupted during setup")
        raise SystemExit(130)
    tracker.update_run("Generator ready; starting generation pipeline")
    try:
        summary = _run_batch_with_progress(config, specs, runner, tracker)
    except KeyboardInterrupt:
        raise SystemExit(130)
    print(json.dumps(summary, indent=2, sort_keys=True))
    retained = summary.get("retained_tasks", 0)
    passed = bool(summary.get("acceptance_gate", {}).get("passed", False))
    if not isinstance(retained, int) or retained == 0:
        raise SystemExit(2)
    if not passed:
        raise SystemExit(1)


def _run_batch_with_progress(
    config: BatchConfig,
    specs: List[Any],
    runner: ContainerizedCodexRunner,
    tracker: RunTracker,
) -> Dict[str, object]:
    """Run the batch while rendering one overall progress line from tracker state."""
    progress = Progress(
        TextColumn("[bold cyan]generating[/bold cyan]"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total} creator jobs"),
        TextColumn("[dim]{task.fields[detail]}[/dim]"),
        TimeElapsedColumn(),
    )
    task_id = progress.add_task(
        "generate", total=len(tracker.manifest["jobs"]), detail="starting"
    )

    def on_status(payload: Dict[str, Any]) -> None:
        counts = payload.get("counts", {})
        detail = (
            f"running {counts.get('running', 0)} · "
            f"retained {counts.get('succeeded', 0)} · "
            f"skipped {counts.get('skipped', 0)} · "
            f"failed {counts.get('failed', 0) + counts.get('cancelled', 0)}"
        )
        progress.update(
            task_id,
            completed=int(payload.get("terminal_jobs", 0)),
            detail=detail,
        )

    tracker.on_status = on_status
    try:
        with progress:
            return BatchRunner(config, specs, runner, tracker).run()
    finally:
        tracker.on_status = None


def _run_submit(args: argparse.Namespace) -> None:
    if args.concurrency is not None and args.concurrency < 1:
        raise SystemExit("--concurrency must be positive")
    try:
        returncode = submit_tasks(
            args.paths,
            org=args.org,
            tags=args.tag,
            public=args.public,
            concurrency=args.concurrency,
            dry_run=args.dry_run,
        )
    except SubmitError as exc:
        raise SystemExit(f"submit failed: {exc}") from exc
    if returncode != 0:
        raise SystemExit(returncode)


def _make_runner(args: argparse.Namespace, tracker: RunTracker) -> ContainerizedCodexRunner:
    return ContainerizedCodexRunner(
        model=args.model,
        reasoning_effort=args.reasoning_effort,
        auth_json=args.auth_json,
        codex_version=args.codex_version,
        image=args.generator_image,
        creator_timeout_sec=args.creator_timeout_sec,
        tracker=tracker,
        max_parallel_workers=args.max_parallel_workers,
        max_codex_attempts=args.codex_max_attempts,
        retry_base_delay_sec=args.codex_retry_base_sec,
    )


def _validate_generation_args(args: argparse.Namespace) -> None:
    if args.max_tasks_per_skill is not None and args.max_tasks_per_skill < 1:
        raise SystemExit("--max-tasks-per-skill must be a positive integer")
    if args.max_parallel_workers < 1 or args.creator_timeout_sec < 1:
        raise SystemExit("numeric limits must be positive")
    if args.max_task_size_mib < 1:
        raise SystemExit("--max-task-size-mib must be a positive integer")
    if args.codex_max_attempts < 1 or args.codex_retry_base_sec <= 0:
        raise SystemExit("retry settings must be positive")


def _finish_setup_failure(tracker: RunTracker, message: str) -> None:
    for job in tracker.manifest["jobs"]:
        tracker.update_job(
            str(job["id"]),
            status="failed",
            stage="setup",
            message=message,
        )
    requested = len({str(job["skill_key"]) for job in tracker.manifest["jobs"]})
    tracker.finish(
        "failed",
        message=message,
        summary={
            "schema_version": "3.0",
            "requested_skills": requested,
            "terminal_records": requested,
            "status_counts": {"failed": requested},
            "retained_tasks": 0,
            "generator_invocations": 0,
            "acceptance_gate": {
                "all_retained_tasks_host_accepted": False,
                "no_generation_failures": False,
                "passed": False,
            },
        },
    )


def _finish_interrupted(tracker: RunTracker, message: str) -> None:
    tracker.cancel_nonterminal(message)
    requested = len({str(job["skill_key"]) for job in tracker.manifest["jobs"]})
    tracker.finish(
        "cancelled",
        message=message,
        summary={
            "schema_version": "3.0",
            "requested_skills": requested,
            "terminal_records": requested,
            "status_counts": {"cancelled": requested},
            "retained_tasks": 0,
            "generator_invocations": 0,
            "interrupted": True,
            "acceptance_gate": {
                "all_retained_tasks_host_accepted": False,
                "no_generation_failures": False,
                "passed": False,
            },
        },
    )


if __name__ == "__main__":
    main()
