# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""One creator call per task followed by host-owned acceptance."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import shutil
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional

from .axes import AxisPreference, TaskAxes, sample_axes
from .buildaudit import TaskAuditor
from .bundle import BundleError, load_skill_bundle
from .generator import AgentRunner, GeneratorError
from .models import ContractError, GenerationRecord
from .output import (
    append_jsonl,
    format_task_name,
    publish_task,
    write_corpus_manifest,
    write_creator_state,
)
from .task_config import write_authoritative_task_toml
from .tracker import RunTracker
from .validation import (
    DEFAULT_MAX_TASK_SIZE_MIB,
    MIB_BYTES,
    TaskPostChecker,
    completed_task_size_bytes,
)


@dataclass
class PipelineConfig:
    skill_path: Path
    output_dir: Path
    state_dir: Path
    model: str
    reasoning_effort: str
    codex_version: str
    generator_image: str
    max_tasks_per_skill: Optional[int] = None
    max_parallel_workers: int = 1
    max_task_size_mib: int = DEFAULT_MAX_TASK_SIZE_MIB
    write_manifest: bool = True
    decompose_workflows: bool = True


class SkillPipeline:
    def __init__(
        self,
        config: PipelineConfig,
        runner: AgentRunner,
        *,
        auditor: TaskAuditor,
        post_checker: Optional[TaskPostChecker] = None,
        tracker: Optional[RunTracker] = None,
        show_progress: bool = True,
    ):
        self.config = config
        self.runner = runner
        self.auditor = auditor
        self.post_checker = post_checker or TaskPostChecker()
        self.tracker = tracker
        self.show_progress = show_progress

    def run(self) -> Dict[str, object]:
        cfg = self.config
        cfg.output_dir.mkdir(parents=True, exist_ok=True)
        cfg.state_dir.mkdir(parents=True, exist_ok=True)
        records_path = cfg.state_dir / "records.jsonl"
        records_path.unlink(missing_ok=True)
        _write_run_config(cfg)

        if self.show_progress:
            print(f"[1/1] {cfg.skill_path}: planning workflows and creating tasks")
        record = self._run_skill()
        append_jsonl(records_path, record.to_dict())
        detail = f" ({record.reason_code}: {record.reason})" if record.reason else ""
        if self.show_progress:
            print(f"  -> {record.status}{detail}")

        summary = summarize_records([record], requested=1)
        _write_json(cfg.state_dir / "summary.json", summary)
        if cfg.write_manifest:
            write_corpus_manifest(cfg.output_dir, record.attempts)
        return summary

    def _run_skill(self) -> GenerationRecord:
        started = time.monotonic()
        source_path = self.config.skill_path.expanduser().resolve()
        record = GenerationRecord(
            skill_id=source_path.name or "skill",
            provider="local",
            source_path=str(source_path),
            status="failed",
            stage="ingest",
        )
        try:
            bundle = load_skill_bundle(source_path)
            record.skill_id = bundle.id
            record.provider = bundle.provider
            record.source_path = bundle.source_path
            record.bundle_digest = bundle.digest
        except BundleError as exc:
            record.reason_code = exc.code
            record.reason = str(exc)
            self._finish_all_jobs("failed", "ingest", str(exc))
            return self._finish_record(record, started)

        workflows = self._analyze_workflows(bundle)
        if workflows:
            _write_json(
                self.config.state_dir / "workflows.json",
                [workflow.to_dict() for workflow in workflows],
            )
        # The planner's workflow count decides how many creators run; the user
        # cap only trims it. Planner failure degrades to a single task.
        count = max(1, len(workflows))
        if self.config.max_tasks_per_skill is not None:
            count = min(count, self.config.max_tasks_per_skill)
        self._skip_surplus_jobs(count)
        workers = min(self.config.max_parallel_workers, count)
        record.generator_invocations = count
        attempts: Dict[int, Dict[str, object]] = {}
        if self.show_progress:
            detail = f", {len(workflows)} workflow(s)" if workflows else ""
            print(f"  -> running {count} creator(s) with up to {workers} worker(s){detail}")

        executor = ThreadPoolExecutor(
            max_workers=workers,
            thread_name_prefix="skill2env-creator",
        )
        futures = {}
        task_names: Dict[int, str] = {}
        try:
            for variant in range(count):
                task_name = format_task_name(bundle.id)
                task_names[variant] = task_name
                futures[
                    executor.submit(
                        self._run_variant,
                        variant=variant,
                        bundle=bundle,
                        workflows=workflows,
                        task_name=task_name,
                    )
                ] = variant
            for future in as_completed(futures):
                variant = futures[future]
                try:
                    attempt = future.result()
                except (GeneratorError, ContractError, RuntimeError, OSError, ValueError) as exc:
                    code = exc.code if isinstance(exc, GeneratorError) else "creation_failed"
                    attempt = {
                        "task_name": task_names[variant],
                        "variant": variant,
                        "status": "failed",
                        "reason_code": code,
                        "reason": str(exc),
                        "path": None,
                        "digest": None,
                    }
                    self._update_job(variant, "failed", "failed", str(exc))
                attempts[variant] = attempt
                if self.show_progress:
                    print(f"  -> variant {variant:03d} {attempt['status']}")
        except KeyboardInterrupt:
            cancel_all = getattr(self.runner, "cancel_all", None)
            if callable(cancel_all):
                cancel_all()
            for future in futures:
                future.cancel()
            if self.tracker is not None:
                self.tracker.cancel_nonterminal("Generation interrupted")
            raise
        finally:
            executor.shutdown(wait=True, cancel_futures=True)

        record.attempts = [attempts[index] for index in sorted(attempts)]
        record.task_dirs = [
            str(attempt["path"])
            for attempt in record.attempts
            if attempt["status"] == "retained"
        ]
        statuses = [str(attempt["status"]) for attempt in record.attempts]
        failures = [
            f"variant {attempt['variant']} [{attempt['reason_code']}]: {attempt['reason']}"
            for attempt in record.attempts
            if attempt["status"] not in {"retained", "skipped"}
        ]
        if statuses and all(status == "retained" for status in statuses):
            record.status = "retained"
            record.stage = "complete"
        elif "retained" in statuses:
            record.status = "retained_partial"
            record.stage = "complete"
            record.reason_code = "attempt_not_retained"
            record.reason = "; ".join(failures) or "one or more attempts were skipped"
        elif statuses and all(status == "skipped" for status in statuses):
            record.status = "skipped"
            record.stage = "complete"
            record.reason_code = str(record.attempts[0]["reason_code"])
            record.reason = str(record.attempts[0]["reason"])
        elif statuses and all(status == "infra_failed" for status in statuses):
            record.status = "infra_failed"
            record.reason_code = "registry_unavailable"
            record.reason = "; ".join(failures)
        else:
            record.status = "failed"
            record.reason_code = "generation_failed"
            record.reason = "; ".join(failures) or "no task was retained"
        return self._finish_record(record, started)

    def _analyze_workflows(self, bundle) -> List:
        """Identify distinct Skill workflows once per skill; degrade to none on failure."""
        if not self.config.decompose_workflows:
            return []
        analyze = getattr(self.runner, "analyze", None)
        if not callable(analyze):
            return []
        try:
            return list(analyze(bundle, state_dir=self.config.state_dir) or [])
        except (GeneratorError, ContractError, OSError, ValueError):
            return []

    def _run_variant(
        self,
        *,
        variant: int,
        bundle,
        workflows: Optional[List] = None,
        task_name: Optional[str] = None,
    ) -> Dict[str, object]:
        if self.tracker is not None and self.tracker.cancelled:
            raise GeneratorError("cancelled", "Batch generation was interrupted")
        if task_name is None:
            task_name = format_task_name(bundle.id)
        workflow = workflows[variant % len(workflows)] if workflows else None
        axes = sample_axes(bundle, variant, workflow=workflow)
        focus = f", {workflow.name}" if workflow is not None else ""
        self._update_job(
            variant,
            "running",
            "creating",
            f"Creator started ({axes.primary}{focus})",
        )
        run = self.runner.create(
            bundle,
            task_name=task_name,
            variant_index=variant,
            state_dir=self.config.state_dir,
            axes=axes,
            workflow=workflow,
        )
        private_dir = write_creator_state(
            self.config.state_dir,
            task_name=task_name,
            result=run.result,
            transcript=run.transcript,
            prompt=run.prompt,
            axes=axes,
        )
        try:
            if run.result.status == "skipped":
                self._update_job(
                    variant,
                    "skipped",
                    "skipped",
                    run.result.skip_reason or "Creator skipped the Skill",
                )
                return {
                    "task_name": task_name,
                    "variant": variant,
                    "status": "skipped",
                    "reason_code": run.result.skip_reason_code,
                    "reason": run.result.skip_reason,
                    "path": None,
                    "digest": None,
                    "axes": axes.to_dict(),
                }

            assert run.task_dir is not None
            effective_axes = _effective_axes(axes, run.result)
            self._update_job(variant, "running", "validating", "Static host checks")
            write_authoritative_task_toml(
                run.task_dir,
                task_name=task_name,
                bundle=bundle,
                creator_result=run.result,
                axes=effective_axes,
            )
            size_bytes = completed_task_size_bytes(run.task_dir)
            limit_bytes = self.config.max_task_size_mib * MIB_BYTES
            _write_json(
                private_dir / "task-size.json",
                {
                    "size_bytes": size_bytes,
                    "limit_bytes": limit_bytes,
                    "passed": size_bytes <= limit_bytes,
                },
            )
            if size_bytes > limit_bytes:
                self._retain_rejected_candidate(run.task_dir, private_dir)
                reason = (
                    f"completed task size {size_bytes} bytes exceeds "
                    f"{self.config.max_task_size_mib} MiB limit ({limit_bytes} bytes)"
                )
                self._update_job(variant, "failed", "task_too_large", reason)
                return {
                    "task_name": task_name,
                    "variant": variant,
                    "status": "failed",
                    "reason_code": "task_too_large",
                    "reason": reason,
                    "path": None,
                    "digest": None,
                    "axes": effective_axes.to_dict(),
                }
            post_check = self.post_checker.check(
                run.task_dir,
                expected_name=task_name,
                bundle=bundle,
                creator_result=run.result,
                axes=effective_axes,
            )
            _write_json(private_dir / "post-check.json", post_check.to_dict())
            if not post_check.ok:
                self._retain_rejected_candidate(run.task_dir, private_dir)
                reason = "; ".join(post_check.errors)
                self._update_job(variant, "failed", "static_validation_failed", reason)
                return {
                    "task_name": task_name,
                    "variant": variant,
                    "status": "failed",
                    "reason_code": "static_validation_failed",
                    "reason": reason,
                    "path": None,
                    "digest": None,
                    "axes": effective_axes.to_dict(),
                }

            self._update_job(variant, "running", "accepting", "Harbor Oracle and NOP")
            audit = self.auditor.audit(
                run.task_dir,
                audit_dir=private_dir / "acceptance",
            )
            _write_json(private_dir / "audit.json", audit.to_dict())
            if not audit.ok:
                self._retain_rejected_candidate(run.task_dir, private_dir)
                reason = "; ".join(audit.errors)
                tracker_status = "failed"
                self._update_job(variant, tracker_status, audit.status, reason)
                return {
                    "task_name": task_name,
                    "variant": variant,
                    "status": "infra_failed" if audit.status == "infra_failed" else "failed",
                    "reason_code": audit.reason_code,
                    "reason": reason,
                    "path": None,
                    "digest": audit.task_digest,
                    "axes": effective_axes.to_dict(),
                }

            self._update_job(variant, "running", "publishing", "Publishing retained task")
            published = publish_task(
                candidate=run.task_dir,
                output_dir=self.config.output_dir,
                task_name=task_name,
            )
            self._update_job(variant, "succeeded", "complete", str(published))
            return {
                "task_name": task_name,
                "variant": variant,
                "status": "retained",
                "reason_code": None,
                "reason": None,
                "path": str(published),
                "digest": audit.task_digest,
                "axes": effective_axes.to_dict(),
            }
        finally:
            shutil.rmtree(run.workspace, ignore_errors=True)

    @staticmethod
    def _retain_rejected_candidate(task_dir: Path, private_dir: Path) -> None:
        destination = private_dir / "candidate"
        if destination.exists():
            shutil.rmtree(destination)
        shutil.move(str(task_dir), destination)

    @staticmethod
    def _finish_record(record: GenerationRecord, started: float) -> GenerationRecord:
        record.elapsed_seconds = round(time.monotonic() - started, 3)
        return record

    def _job_id(self, variant: int) -> Optional[str]:
        if self.tracker is None:
            return None
        return self.tracker.job_id_for(self.config.state_dir, "creator", variant)

    def _update_job(
        self, variant: int, status: str, stage: str, message: str
    ) -> None:
        job_id = self._job_id(variant)
        if self.tracker is not None and job_id is not None:
            self.tracker.update_job(job_id, status=status, stage=stage, message=message)

    def _skip_surplus_jobs(self, count: int) -> None:
        """Retire pre-registered creator slots beyond the resolved task count (auto mode)."""
        if self.tracker is None:
            return
        variant = count
        while True:
            job_id = self.tracker.job_id_for(self.config.state_dir, "creator", variant)
            if job_id is None:
                return
            self.tracker.update_job(
                job_id,
                status="skipped",
                stage="skipped",
                message="No workflow for this slot",
            )
            variant += 1

    def _finish_all_jobs(self, status: str, stage: str, message: str) -> None:
        if self.tracker is None:
            return
        variant = 0
        while True:
            job_id = self.tracker.job_id_for(self.config.state_dir, "creator", variant)
            if job_id is None:
                return
            self.tracker.update_job(job_id, status=status, stage=stage, message=message)
            variant += 1


def summarize_records(records: List[GenerationRecord], *, requested: int) -> Dict[str, object]:
    counts: Dict[str, int] = {}
    attempts: List[Dict[str, object]] = []
    invocations = 0
    for record in records:
        counts[record.status] = counts.get(record.status, 0) + 1
        attempts.extend(record.attempts)
        invocations += record.generator_invocations
    retained = sum(1 for attempt in attempts if attempt.get("status") == "retained")
    failed = sum(
        1
        for attempt in attempts
        if attempt.get("status") in {"failed", "infra_failed"}
    )
    return {
        "schema_version": "3.0",
        "requested_skills": requested,
        "terminal_records": len(records),
        "status_counts": counts,
        "retained_tasks": retained,
        "generator_invocations": invocations,
        "attempts": attempts,
        "acceptance_gate": {
            "all_retained_tasks_host_accepted": retained > 0,
            "no_generation_failures": failed == 0,
            "passed": retained > 0 and failed == 0,
        },
    }


def _effective_axes(axes: AxisPreference, result) -> TaskAxes:
    _validate_realized_axes(axes, result)
    return TaskAxes(
        archetype=result.realized_axes["archetype"],
        primary_verifier_pattern=result.realized_axes["primary_verifier_pattern"],
        complexity=axes.complexity,
        persona=axes.persona,
        tone=axes.tone,
        expertise=axes.expertise,
    )


def _validate_realized_axes(axes: AxisPreference, result) -> None:
    realized = result.realized_axes
    if realized.get("archetype") not in axes.allowed_archetypes():
        raise ContractError(
            "creator realized archetype must be the sampled primary archetype "
            "or one of its ordered fallbacks"
        )
    if realized.get("primary_verifier_pattern") not in axes.allowed_verifier_patterns():
        raise ContractError(
            "creator realized primary_verifier_pattern must be the sampled primary pattern "
            "or one of its ordered fallbacks"
        )


def _write_run_config(config: PipelineConfig) -> None:
    payload = {
        **asdict(config),
        "skill_path": str(config.skill_path),
        "output_dir": str(config.output_dir),
        "state_dir": str(config.state_dir),
    }
    _write_json(config.state_dir / "run_config.json", payload)


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
