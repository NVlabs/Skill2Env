# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Batch orchestration for monitored skill generation runs."""

from __future__ import annotations

import json
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from .buildaudit import BuildAuditor
from .generator import MAX_WORKFLOWS, ContainerizedCodexRunner
from .output import safe_name, write_corpus_manifest
from .pipeline import PipelineConfig, SkillPipeline
from .tracker import RunTracker, make_job_id, utc_now
from .validation import DEFAULT_MAX_TASK_SIZE_MIB, TaskPostChecker


DONE_MARKER = ".skill2env_done.json"
FINISHED_STATUSES = {"retained", "retained_partial", "skipped"}


@dataclass(frozen=True)
class BatchConfig:
    input_root: Path
    output_root: Path
    run_dir: Path
    model: str
    reasoning_effort: str
    codex_version: str
    generator_image: str
    max_tasks_per_skill: Optional[int] = None
    max_parallel_workers: int = 4
    max_task_size_mib: int = DEFAULT_MAX_TASK_SIZE_MIB
    resume: bool = False

    def task_slots(self) -> int:
        """Tracker slots pre-registered per skill (planner decides actual count)."""
        if self.max_tasks_per_skill is None:
            return MAX_WORKFLOWS
        return min(MAX_WORKFLOWS, self.max_tasks_per_skill)


@dataclass(frozen=True)
class SkillSpec:
    key: str
    source: Path
    output: Path
    state: Path
    relative: str


def discover_skills(input_root: Path, output_root: Path, run_dir: Path) -> List[SkillSpec]:
    input_root = input_root.expanduser().resolve()
    output_root = output_root.expanduser().resolve()
    run_dir = run_dir.expanduser().resolve()
    skill_files = sorted(input_root.rglob("SKILL.md"), key=lambda path: path.as_posix())
    specs = []
    for index, skill_file in enumerate(skill_files):
        source = skill_file.parent.resolve()
        relative_path = source.relative_to(input_root)
        relative = relative_path.as_posix() if relative_path.parts else "."
        key_part = "root" if relative == "." else safe_name(relative)
        key = f"{index:04d}-{key_part}"
        output = output_root if relative == "." else output_root / relative_path
        specs.append(
            SkillSpec(
                key=key,
                source=source,
                output=output,
                state=run_dir / "skills" / key,
                relative=relative,
            )
        )
    return specs


def create_batch_tracker(config: BatchConfig, specs: List[SkillSpec]) -> RunTracker:
    slots = config.task_slots()
    jobs = []
    for spec in specs:
        common = {
            "skill_key": spec.key,
            "skill_id": spec.source.name,
            "skill_path": str(spec.source),
            "relative_path": spec.relative,
            "state_dir": str(spec.state),
        }
        for variant in range(slots):
            jobs.append(
                {
                    **common,
                    "id": make_job_id(spec.key, "creator", variant),
                    "phase": "creator",
                    "variant": variant,
                }
            )
    return RunTracker.create(
        config.run_dir,
        run_id=config.run_dir.name,
        kind="batch",
        config={
            "input_root": str(config.input_root),
            "output_root": str(config.output_root),
            "model": config.model,
            "reasoning_effort": config.reasoning_effort,
            "codex_version": config.codex_version,
            "generator_image": config.generator_image,
            "max_tasks_per_skill": config.max_tasks_per_skill,
            "max_parallel_workers": config.max_parallel_workers,
            "max_task_size_mib": config.max_task_size_mib,
            "resume": config.resume,
        },
        jobs=jobs,
    )


class BatchRunner:
    def __init__(
        self,
        config: BatchConfig,
        specs: List[SkillSpec],
        runner: ContainerizedCodexRunner,
        tracker: RunTracker,
    ):
        self.config = config
        self.specs = specs
        self.runner = runner
        self.tracker = tracker
        self.auditor = BuildAuditor()

    def run(self) -> Dict[str, object]:
        summaries: Dict[str, Dict[str, object]] = {}
        pending: List[SkillSpec] = []
        if self.config.resume:
            for spec in self.specs:
                finished = _load_finished_state(spec)
                if finished is None:
                    pending.append(spec)
                    continue
                self._mark_skill_resumed(spec, finished)
                summaries[spec.key] = _resumed_summary(finished)
        else:
            pending = list(self.specs)
        # Pools are sized to the worker budget; the runner's global semaphore is
        # the true cap on concurrent Codex containers across skills and variants.
        executor = ThreadPoolExecutor(
            max_workers=min(self.config.max_parallel_workers, max(len(pending), 1)),
            thread_name_prefix="skill2env-skill",
        )
        futures: Dict[Future[Dict[str, object]], SkillSpec] = {}
        interrupted = False
        try:
            for spec in pending:
                futures[executor.submit(self._run_skill, spec)] = spec
            for future in as_completed(futures):
                spec = futures[future]
                try:
                    summaries[spec.key] = future.result()
                except Exception as exc:  # Last-resort isolation between skills.
                    self._mark_skill_failed(spec, str(exc))
                    summaries[spec.key] = _failed_summary()
        except KeyboardInterrupt:
            interrupted = True
            self.runner.cancel_all()
            for future in futures:
                future.cancel()
            self.tracker.cancel_nonterminal("Batch generation interrupted")
        finally:
            executor.shutdown(wait=True, cancel_futures=True)

        if interrupted:
            summary = _aggregate_summaries(summaries, requested=len(self.specs))
            unfinished = len(self.specs) - len(summaries)
            if unfinished:
                status_counts = summary["status_counts"]
                status_counts["cancelled"] = status_counts.get("cancelled", 0) + unfinished
                summary["terminal_records"] = len(self.specs)
            summary["interrupted"] = True
            self.tracker.finish("cancelled", message="Batch generation interrupted", summary=summary)
            raise KeyboardInterrupt

        summary = _aggregate_summaries(summaries, requested=len(self.specs))
        self.config.output_root.mkdir(parents=True, exist_ok=True)
        manifest_attempts = list(summary["attempts"])
        if self.config.resume:
            manifest_attempts = _merge_prior_manifest(
                self.config.output_root, manifest_attempts
            )
        write_corpus_manifest(self.config.output_root, manifest_attempts)
        passed = bool(summary["acceptance_gate"]["passed"])
        self.tracker.finish(
            "succeeded" if passed else "failed",
            message="Batch generation completed" if passed else "Batch generation had failures",
            summary=summary,
        )
        return summary

    def _run_skill(self, spec: SkillSpec) -> Dict[str, object]:
        pipeline_config = PipelineConfig(
            skill_path=spec.source,
            output_dir=spec.output,
            state_dir=spec.state,
            model=self.runner.model,
            reasoning_effort=self.runner.reasoning_effort,
            codex_version=self.runner.codex_version,
            generator_image=self.runner.image,
            max_tasks_per_skill=self.config.max_tasks_per_skill,
            max_parallel_workers=self.config.max_parallel_workers,
            max_task_size_mib=self.config.max_task_size_mib,
            write_manifest=False,
        )
        summary = SkillPipeline(
            pipeline_config,
            self.runner,
            auditor=self.auditor,
            post_checker=TaskPostChecker(),
            tracker=self.tracker,
            show_progress=False,
        ).run()
        self._write_done_marker(spec, summary)
        return summary

    def _write_done_marker(self, spec: SkillSpec, summary: Dict[str, object]) -> None:
        """Record durable per-skill completion so later runs can resume past it."""
        counts = dict(summary.get("status_counts", {}))
        status = next(iter(counts)) if len(counts) == 1 else None
        if status not in FINISHED_STATUSES:
            return
        spec.output.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": "1.0",
            "skill": spec.relative,
            "status": status,
            "retained_tasks": int(summary.get("retained_tasks", 0)),
            "run_id": self.config.run_dir.name,
            "completed_at": utc_now(),
        }
        (spec.output / DONE_MARKER).write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

    def _mark_skill_resumed(self, spec: SkillSpec, finished: Dict[str, Any]) -> None:
        status = finished.get("status", "retained")
        for variant in range(self.config.task_slots()):
            job_id = make_job_id(spec.key, "creator", variant)
            self.tracker.update_job(
                job_id,
                status="skipped",
                stage="resumed",
                message=f"Finished in a previous run ({status})",
            )

    def _mark_skill_failed(self, spec: SkillSpec, message: str) -> None:
        job_ids = [
            make_job_id(spec.key, "creator", variant)
            for variant in range(self.config.task_slots())
        ]
        for job_id in job_ids:
            self.tracker.update_job(
                job_id,
                status="failed",
                stage="failed",
                message=message,
            )


def _aggregate_summaries(
    summaries: Dict[str, Dict[str, object]], *, requested: int
) -> Dict[str, object]:
    counts: Dict[str, int] = {}
    retained = 0
    invocations = 0
    terminal = 0
    failed = False
    attempts: list[dict[str, object]] = []
    for summary in summaries.values():
        terminal += int(summary.get("terminal_records", 0))
        retained += int(summary.get("retained_tasks", 0))
        invocations += int(summary.get("generator_invocations", 0))
        attempts.extend(list(summary.get("attempts", [])))
        for status, count in dict(summary.get("status_counts", {})).items():
            counts[str(status)] = counts.get(str(status), 0) + int(count)
        gate = summary.get("acceptance_gate", {})
        if not isinstance(gate, dict) or not gate.get("no_generation_failures", False):
            failed = True
    if len(summaries) != requested:
        failed = True
    passed = retained > 0 and not failed
    return {
        "schema_version": "3.0",
        "requested_skills": requested,
        "terminal_records": terminal,
        "status_counts": counts,
        "retained_tasks": retained,
        "generator_invocations": invocations,
        "attempts": attempts,
        "acceptance_gate": {
            "all_retained_tasks_host_accepted": retained > 0,
            "no_generation_failures": not failed,
            "passed": passed,
        },
    }


def _load_finished_state(spec: SkillSpec) -> Optional[Dict[str, Any]]:
    """Return the prior completion state for a skill, or None if it must run.

    Prefers the durable done marker; falls back to detecting published tasks so
    runs that predate markers still resume past their retained skills.
    """
    marker = spec.output / DONE_MARKER
    if marker.is_file():
        try:
            data = json.loads(marker.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            data = None
        if isinstance(data, dict) and data.get("status") in FINISHED_STATUSES:
            return data
    published = sorted(spec.output.glob("task_*/task.toml"))
    if published:
        return {"status": "retained", "retained_tasks": len(published), "legacy": True}
    return None


def _resumed_summary(finished: Dict[str, Any]) -> Dict[str, object]:
    retained = int(finished.get("retained_tasks", 0) or 0)
    return {
        "schema_version": "3.0",
        "requested_skills": 1,
        "terminal_records": 1,
        "status_counts": {"resumed": 1},
        "retained_tasks": retained,
        "generator_invocations": 0,
        "attempts": [],
        "acceptance_gate": {
            "all_retained_tasks_host_accepted": retained > 0,
            "no_generation_failures": True,
            "passed": retained > 0,
        },
    }


def _merge_prior_manifest(
    output_root: Path, attempts: List[Dict[str, object]]
) -> List[Dict[str, object]]:
    """Keep prior manifest entries whose published tasks still exist on disk.

    Without this, a resumed run would overwrite _corpus_manifest.json with only
    the newly generated attempts and drop the record of earlier retained tasks.
    """
    manifest_path = output_root / "_corpus_manifest.json"
    try:
        prior = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return attempts
    new_names = {
        str(attempt.get("task_name")) for attempt in attempts if attempt.get("task_name")
    }
    merged: List[Dict[str, object]] = []
    for entry in prior.get("attempts", []) if isinstance(prior, dict) else []:
        if not isinstance(entry, dict):
            continue
        name = entry.get("task_name")
        relative = entry.get("path")
        if not name or name in new_names or not isinstance(relative, str):
            continue
        absolute = output_root / relative
        if not (absolute / "task.toml").is_file():
            continue
        merged.append({**entry, "path": str(absolute)})
    merged.extend(attempts)
    return merged


def _failed_summary() -> Dict[str, object]:
    return {
        "schema_version": "3.0",
        "requested_skills": 1,
        "terminal_records": 1,
        "status_counts": {"failed": 1},
        "retained_tasks": 0,
        "generator_invocations": 0,
        "attempts": [],
        "acceptance_gate": {
            "all_retained_tasks_host_accepted": False,
            "no_generation_failures": False,
            "passed": False,
        },
    }
