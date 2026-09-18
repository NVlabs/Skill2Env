# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Containerized Codex runner for one-call task creation."""

from __future__ import annotations

import json
import os
import random
import re
import shutil
import subprocess
import tempfile
import threading
import time
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Callable, Optional, Protocol, TypeVar

from .axes import AxisPreference, valid_axis_label
from .models import (
    AssetRecommendation,
    AssetSource,
    ContractError,
    CreatorResult,
    SkillBundle,
    Workflow,
)
from .prompts import creator_prompt, workflow_analysis_prompt
from .tracker import RunTracker


DEFAULT_CODEX_VERSION = "0.146.0"
DEFAULT_MODEL = "gpt-5.6-sol"
DEFAULT_REASONING_EFFORT = "xhigh"
REASONING_EFFORTS = ("low", "medium", "high", "xhigh", "max")
MAX_WORKFLOWS = 8
DEFAULT_MAX_CODEX_ATTEMPTS = 5
DEFAULT_RETRY_BASE_DELAY_SEC = 15.0
RETRY_MAX_DELAY_SEC = 300.0
GENERATOR_IMAGE_REVISION = "assets1"

# CODEX_HOME lives at a fixed container path outside the bind-mounted workspace
# so the workspace-write sandbox cannot touch shared authentication/config state.
CONTAINER_CODEX_HOME = PurePosixPath("/skill2env-codex-home")

# Transient upstream failures worth retrying with backoff. The auth-refresh
# patterns cover the rotation race between concurrent containers sharing one
# auth.json: the loser fails once, then succeeds after re-reading the file the
# winner just rewrote.
_RETRYABLE_OUTPUT = re.compile(
    r"rate limit"
    r"|too many requests"
    r"|\b429\b"
    r"|usage limit"
    r"|refresh token was already used"
    r"|token could not be refreshed"
    r"|internal server error"
    r"|bad gateway"
    r"|service unavailable"
    r"|gateway timeout"
    r"|\boverloaded\b"
    r"|connection reset by peer"
    r"|stream disconnected",
    re.IGNORECASE,
)
_RETRYABLE_CODES = {"codex_failed"}

_T = TypeVar("_T")


def retryable_codex_error(exc: "GeneratorError") -> bool:
    return exc.code in _RETRYABLE_CODES and bool(_RETRYABLE_OUTPUT.search(str(exc)))


def default_generator_image(codex_version: str) -> str:
    """Return a cache-busting tag for the bundled generator toolset."""
    return f"skill2env-codex:{codex_version}-{GENERATOR_IMAGE_REVISION}"


class GeneratorError(RuntimeError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class CreationRun:
    workspace: Path
    task_dir: Optional[Path]
    result: CreatorResult
    transcript: str
    prompt: str


class AgentRunner(Protocol):
    model: str
    reasoning_effort: str
    codex_version: str
    image: str

    def prepare(self) -> None: ...

    def analyze(
        self,
        bundle: SkillBundle,
        *,
        state_dir: Path,
        max_workflows: int = MAX_WORKFLOWS,
    ) -> list[Workflow]: ...

    def create(
        self,
        bundle: SkillBundle,
        *,
        task_name: str,
        variant_index: int,
        state_dir: Path,
        axes: AxisPreference,
        workflow: Workflow | None = None,
    ) -> CreationRun: ...


class ContainerizedCodexRunner:
    """Run one isolated creator per task without exposing the host Docker daemon."""

    def __init__(
        self,
        *,
        auth_json: Optional[Path] = None,
        model: str = DEFAULT_MODEL,
        reasoning_effort: str = DEFAULT_REASONING_EFFORT,
        codex_version: str = DEFAULT_CODEX_VERSION,
        image: Optional[str] = None,
        creator_timeout_sec: int = 3600,
        tracker: Optional[RunTracker] = None,
        max_parallel_workers: Optional[int] = None,
        max_codex_attempts: int = DEFAULT_MAX_CODEX_ATTEMPTS,
        retry_base_delay_sec: float = DEFAULT_RETRY_BASE_DELAY_SEC,
    ):
        if not model.strip():
            raise ValueError("a pinned Codex model is required")
        if reasoning_effort not in REASONING_EFFORTS:
            raise ValueError(f"reasoning effort must be one of {REASONING_EFFORTS!r}")
        if not codex_version.strip():
            raise ValueError("a pinned Codex CLI version is required")
        if max_parallel_workers is not None and max_parallel_workers < 1:
            raise ValueError("max_parallel_workers must be positive")
        if max_codex_attempts < 1:
            raise ValueError("max_codex_attempts must be positive")
        if retry_base_delay_sec <= 0:
            raise ValueError("retry_base_delay_sec must be positive")
        if auth_json is None:
            raise ValueError("auth_json is required")
        self.model = model.strip()
        self.reasoning_effort = reasoning_effort
        self.auth_json = auth_json.expanduser().resolve()
        self.codex_version = codex_version.strip()
        self.image = image or default_generator_image(self.codex_version)
        self._external_image = image is not None
        self.creator_timeout_sec = creator_timeout_sec
        self.tracker = tracker
        self.max_codex_attempts = max_codex_attempts
        self.retry_base_delay_sec = retry_base_delay_sec
        self._shared_codex_home: Optional[Path] = None
        self._shared_home_lock = threading.Lock()
        # Global cap on concurrent Codex agent containers (planner + creators),
        # regardless of how the calling thread pools are shaped.
        self._worker_slots = (
            threading.BoundedSemaphore(max_parallel_workers)
            if max_parallel_workers is not None
            else None
        )
        self._prepared = False
        self._active_processes: set[subprocess.Popen[str]] = set()
        self._active_lock = threading.Lock()

    def cancel_all(self) -> None:
        with self._active_lock:
            processes = list(self._active_processes)
        for process in processes:
            if process.poll() is None:
                process.terminate()

    def prepare(self) -> None:
        if self._prepared:
            return
        if shutil.which("docker") is None:
            raise GeneratorError("docker_unavailable", "docker is not on PATH")
        if not self.auth_json.is_file():
            raise GeneratorError("auth_missing", f"Codex auth file not found: {self.auth_json}")

        inspect = _host_command(["docker", "image", "inspect", self.image], timeout=60)
        if inspect.returncode != 0:
            if self._external_image:
                pull = _host_command(["docker", "pull", self.image], timeout=900)
                if pull.returncode != 0:
                    raise GeneratorError(
                        "generator_image_pull_failed", _bounded_output(pull, 8000)
                    )
            else:
                dockerfile = Path(__file__).with_name("generator.Dockerfile")
                build = _host_command(
                    [
                        "docker",
                        "build",
                        "--build-arg",
                        f"CODEX_VERSION={self.codex_version}",
                        "--tag",
                        self.image,
                        "--file",
                        str(dockerfile),
                        str(dockerfile.parent),
                    ],
                    timeout=900,
                )
                if build.returncode != 0:
                    raise GeneratorError(
                        "generator_image_build_failed", _bounded_output(build, 12000)
                    )

        version = _host_command(
            ["docker", "run", "--rm", "--entrypoint", "codex", self.image, "--version"],
            timeout=60,
        )
        if version.returncode != 0:
            raise GeneratorError("codex_unavailable", _bounded_output(version, 4000))
        reported = (version.stdout or version.stderr).strip()
        if not self._external_image and self.codex_version not in reported:
            raise GeneratorError(
                "codex_version_mismatch",
                f"generator image reports {reported!r}, expected {self.codex_version!r}",
            )
        if self._external_image:
            self.codex_version = reported or self.codex_version
        self._ensure_shared_codex_home()
        self._prepared = True

    def _ensure_shared_codex_home(self) -> Path:
        """One host-owned CODEX_HOME shared by every container.

        It holds static approval rules and Codex's ephemeral state; auth.json is
        bind-mounted separately.
        """
        with self._shared_home_lock:
            if self._shared_codex_home is None:
                shared_home = Path(tempfile.mkdtemp(prefix="skill2env-codex-home-"))
                rules_dir = shared_home / "rules"
                rules_dir.mkdir(parents=True, exist_ok=True)
                (rules_dir / "skill2env.rules").write_text(
                    'prefix_rule(pattern=["/bin/bash", "-lc"], decision="allow")\n'
                    'prefix_rule(pattern=["/bin/bash", "-c"], decision="allow")\n',
                    encoding="utf-8",
                )
                self._shared_codex_home = shared_home
            return self._shared_codex_home

    def analyze(
        self,
        bundle: SkillBundle,
        *,
        state_dir: Path,
        max_workflows: int = MAX_WORKFLOWS,
    ) -> list[Workflow]:
        """Identify the distinct instructed workflows in a Skill (host-owned pre-pass)."""
        self.prepare()
        return self._retry_codex(
            lambda: self._analyze_once(
                bundle, state_dir=state_dir, max_workflows=max_workflows
            ),
            state_dir=state_dir,
            phase="analyst",
            variant_index=0,
        )

    def _analyze_once(
        self,
        bundle: SkillBundle,
        *,
        state_dir: Path,
        max_workflows: int,
    ) -> list[Workflow]:
        workspace = _new_workspace(state_dir, f"analyze-{_safe_name(bundle.id)}-")
        try:
            _stage_bundle(bundle, workspace / "source")
            prompt = workflow_analysis_prompt(bundle=bundle, max_workflows=max_workflows)
            result_path = workspace / "workflows.json"
            self._run_codex(
                workspace=workspace,
                prompt=prompt,
                transcript_path=workspace / "analyst-transcript.jsonl",
                output_path=workspace / "analyst-last-message.txt",
                timeout=self.creator_timeout_sec,
                state_dir=state_dir,
                variant_index=0,
                phase="analyst",
            )
            try:
                data = json.loads(result_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise GeneratorError("workflow_contract_failed", str(exc)) from exc
            return _parse_workflows(data, limit=max_workflows)
        finally:
            shutil.rmtree(workspace, ignore_errors=True)

    def create(
        self,
        bundle: SkillBundle,
        *,
        task_name: str,
        variant_index: int,
        state_dir: Path,
        axes: AxisPreference,
        workflow: Workflow | None = None,
    ) -> CreationRun:
        self.prepare()
        return self._retry_codex(
            lambda: self._create_once(
                bundle,
                task_name=task_name,
                variant_index=variant_index,
                state_dir=state_dir,
                axes=axes,
                workflow=workflow,
            ),
            state_dir=state_dir,
            phase="creator",
            variant_index=variant_index,
        )

    def _retry_codex(
        self,
        attempt_fn: Callable[[], _T],
        *,
        state_dir: Path,
        phase: str,
        variant_index: int,
    ) -> _T:
        """Run one Codex call, retrying provider failures or transient upstream errors.

        Each retry starts from a fresh workspace (the failed one is discarded),
        so a partially written task tree never leaks into the next attempt.
        """
        delay = self.retry_base_delay_sec
        for attempt in range(1, self.max_codex_attempts + 1):
            try:
                return attempt_fn()
            except GeneratorError as exc:
                cancelled = self.tracker is not None and self.tracker.cancelled
                retryable = retryable_codex_error(exc)
                if (
                    cancelled
                    or attempt >= self.max_codex_attempts
                    or not retryable
                ):
                    raise
                failed_workspace = getattr(exc, "workspace", None)
                if failed_workspace is not None:
                    shutil.rmtree(failed_workspace, ignore_errors=True)
                sleep_for = min(delay, RETRY_MAX_DELAY_SEC) * random.uniform(0.5, 1.5)
                self._note_retry(
                    state_dir=state_dir,
                    phase=phase,
                    variant_index=variant_index,
                    attempt=attempt,
                    sleep_for=sleep_for,
                    exc=exc,
                )
                if self._sleep_unless_cancelled(sleep_for):
                    raise
                delay *= 2
        raise AssertionError("unreachable")

    def _sleep_unless_cancelled(self, seconds: float) -> bool:
        """Sleep in small slices; return True if the run was cancelled meanwhile."""
        deadline = time.monotonic() + seconds
        while True:
            if self.tracker is not None and self.tracker.cancelled:
                return True
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return False
            time.sleep(min(remaining, 2.0))

    def _note_retry(
        self,
        *,
        state_dir: Path,
        phase: str,
        variant_index: int,
        attempt: int,
        sleep_for: float,
        exc: GeneratorError,
    ) -> None:
        if self.tracker is None:
            return
        job_id = self.tracker.job_id_for(state_dir, phase, variant_index)
        if job_id is None:
            return
        detail = " ".join(str(exc).split())[:200]
        self.tracker.update_job(
            job_id,
            status="running",
            stage="retrying",
            message=(
                f"[{exc.code}] retry {attempt}/{self.max_codex_attempts - 1} "
                f"in {sleep_for:.0f}s: {detail}"
            ),
        )

    def _create_once(
        self,
        bundle: SkillBundle,
        *,
        task_name: str,
        variant_index: int,
        state_dir: Path,
        axes: AxisPreference,
        workflow: Workflow | None = None,
    ) -> CreationRun:
        workspace = _new_workspace(state_dir, f"create-{_safe_name(bundle.id)}-")
        _stage_bundle(bundle, workspace / "source")
        task_dir = workspace / task_name
        for relative in ("environment", "tests", "solution"):
            (task_dir / relative).mkdir(parents=True, exist_ok=True)
        prompt = creator_prompt(
            bundle=bundle,
            task_name=task_name,
            variant_index=variant_index,
            axes=axes,
            workflow=workflow,
        )
        transcript_path = workspace / "creator-transcript.jsonl"
        output_path = workspace / "creator-last-message.txt"
        result_path = workspace / "creator-result.json"
        try:
            transcript = self._run_codex(
                workspace=workspace,
                prompt=prompt,
                transcript_path=transcript_path,
                output_path=output_path,
                timeout=self.creator_timeout_sec,
                state_dir=state_dir,
                variant_index=variant_index,
            )
            try:
                result = CreatorResult.from_dict(
                    json.loads(result_path.read_text(encoding="utf-8"))
                )
            except (OSError, json.JSONDecodeError, ContractError, TypeError) as exc:
                raise GeneratorError("creator_contract_failed", str(exc)) from exc

            if result.status == "created" and not task_dir.is_dir():
                raise GeneratorError(
                    "task_missing", f"creator did not create expected directory {task_name!r}"
                )
            if result.status == "skipped":
                if any(path.is_file() or path.is_symlink() for path in task_dir.rglob("*")):
                    raise GeneratorError(
                        "skip_left_task", "skipped creator result left task files"
                    )
                shutil.rmtree(task_dir, ignore_errors=True)
            return CreationRun(
                workspace=workspace,
                task_dir=task_dir if result.status == "created" else None,
                result=result,
                transcript=transcript,
                prompt=prompt,
            )
        except GeneratorError as exc:
            wrapped = GeneratorError(
                exc.code, f"{exc} (diagnostic workspace: {workspace})"
            )
            # Let the retry loop discard this workspace before re-attempting.
            wrapped.workspace = workspace
            raise wrapped from exc

    def _run_codex(
        self,
        *,
        workspace: Path,
        prompt: str,
        transcript_path: Path,
        output_path: Path,
        timeout: int,
        state_dir: Path,
        variant_index: int,
        phase: str = "creator",
    ) -> str:
        if self._worker_slots is None:
            return self._execute_codex(
                workspace=workspace,
                prompt=prompt,
                transcript_path=transcript_path,
                output_path=output_path,
                timeout=timeout,
                state_dir=state_dir,
                variant_index=variant_index,
                phase=phase,
            )
        with self._worker_slots:
            return self._execute_codex(
                workspace=workspace,
                prompt=prompt,
                transcript_path=transcript_path,
                output_path=output_path,
                timeout=timeout,
                state_dir=state_dir,
                variant_index=variant_index,
                phase=phase,
            )

    def _execute_codex(
        self,
        *,
        workspace: Path,
        prompt: str,
        transcript_path: Path,
        output_path: Path,
        timeout: int,
        state_dir: Path,
        variant_index: int,
        phase: str = "creator",
    ) -> str:
        workspace = workspace.resolve()
        # Host-owned HOME inside the bind mount so a non-root container user
        # can write ephemeral state, and so created task files stay writable
        # by the host process that authors task.toml afterward.
        home_dir = workspace / ".codex-home"
        home_dir.mkdir(parents=True, exist_ok=True)
        shared_codex_home = self._ensure_shared_codex_home()
        command = [
            "docker",
            "run",
            "--rm",
            "--interactive",
            # Codex's managed workspace-write sandbox uses a nested user
            # namespace on Linux. Docker's default seccomp profile blocks the
            # required unshare syscall, so allow the inner bwrap sandbox to
            # establish its own restrictions. The container still runs as the
            # host uid/gid and receives only the workspace and Codex state
            # mounts below.
            "--security-opt",
            "seccomp=unconfined",
            "--security-opt",
            "apparmor=unconfined",
            *_docker_user_args(),
            "--mount",
            f"type=bind,src={workspace},dst={workspace}",
            "--mount",
            f"type=bind,src={shared_codex_home},dst={CONTAINER_CODEX_HOME}",
            # auth.json is mounted read-write and shared so Codex can safely
            # persist rotated refresh tokens. CODEX_HOME remains beyond the
            # workspace-write sandbox.
            "--mount",
            f"type=bind,src={self.auth_json},dst={CONTAINER_CODEX_HOME / 'auth.json'}",
            "--workdir",
            str(workspace),
            "--env",
            f"HOME={home_dir}",
            "--env",
            f"CODEX_HOME={CONTAINER_CODEX_HOME}",
            self.image,
            "--sandbox",
            "workspace-write",
            "--search",
            "exec",
            "--model",
            self.model,
            "--config",
            f'model_reasoning_effort="{self.reasoning_effort}"',
            "--config",
            'service_tier="fast"',
            "--config",
            "features.fast_mode=true",
            "--config",
            "sandbox_workspace_write.network_access=true",
            "--ephemeral",
            "--skip-git-repo-check",
            "--json",
            "--output-last-message",
            str(output_path),
            "-",
        ]
        durable_stdout = None
        durable_stderr = None
        if self.tracker is not None:
            job_id = self.tracker.job_id_for(state_dir, phase, variant_index)
            if job_id is not None:
                durable_stdout, durable_stderr = self.tracker.log_paths(job_id)

        transcript_parts: list[str] = []
        stderr_parts: list[str] = []
        try:
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )
        except OSError as exc:
            raise GeneratorError("docker_execution_failed", str(exc)) from exc

        with self._active_lock:
            self._active_processes.add(process)

        stdout_targets = [transcript_path]
        if durable_stdout is not None and durable_stdout != transcript_path:
            stdout_targets.append(durable_stdout)
        stderr_targets = [durable_stderr] if durable_stderr is not None else []
        drain_threads = [
            threading.Thread(
                target=_drain_stream,
                args=(process.stdout, stdout_targets, transcript_parts),
                name="skill2env-creator-stdout",
                daemon=True,
            ),
            threading.Thread(
                target=_drain_stream,
                args=(process.stderr, stderr_targets, stderr_parts),
                name="skill2env-creator-stderr",
                daemon=True,
            ),
        ]
        for thread in drain_threads:
            thread.start()

        try:
            if process.stdin is not None:
                process.stdin.write(prompt)
                process.stdin.close()
            returncode = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            raise GeneratorError("codex_timeout", f"Codex timed out after {timeout}s") from exc
        except KeyboardInterrupt:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            raise
        except OSError as exc:
            process.kill()
            process.wait()
            raise GeneratorError("docker_execution_failed", str(exc)) from exc
        finally:
            for thread in drain_threads:
                thread.join(timeout=5)
            with self._active_lock:
                self._active_processes.discard(process)

        transcript = "".join(transcript_parts)
        stderr = "".join(stderr_parts)
        if returncode != 0:
            completed = subprocess.CompletedProcess(command, returncode, transcript, stderr)
            failure = _bounded_output(completed, 12000)
            raise GeneratorError("codex_failed", failure)
        if not output_path.is_file():
            raise GeneratorError("codex_output_missing", "Codex produced no final response file")
        return transcript


MAX_AXIS_POOL_COMBOS = 5


def _parse_workflows(data: object, *, limit: int) -> list[Workflow]:
    """Leniently parse the planner's workflows.json into a bounded Workflow list.

    ``name``/``summary`` are required; ``plan``, ``asset_recommendations``, and
    ``axis_pool`` are optional planner enrichments that degrade to empty values,
    never to a failed run.
    """
    raw = data.get("workflows", []) if isinstance(data, dict) else data
    if not isinstance(raw, list):
        return []
    workflows: list[Workflow] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name", "")).strip()
        summary = str(item.get("summary", "")).strip()
        if name and summary:
            workflows.append(
                Workflow(
                    name=name,
                    summary=summary,
                    plan=_parse_plan(item.get("plan")),
                    asset_recommendations=_parse_asset_recommendations(
                        item.get("asset_recommendations")
                    ),
                    axis_pool=_parse_axis_pool(item.get("axis_pool")),
                )
            )
        if len(workflows) >= limit:
            break
    return workflows


def _parse_plan(value: object) -> dict:
    if not isinstance(value, dict):
        return {}
    return {str(key): item for key, item in value.items() if str(key).strip()}


def _parse_asset_recommendations(value: object) -> tuple[AssetRecommendation, ...]:
    """Keep well-shaped planner guidance without validating remote availability."""
    if not isinstance(value, list):
        return ()
    recommendations: list[AssetRecommendation] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        purpose = _nonempty_text(item.get("purpose"))
        kind = _nonempty_text(item.get("kind"))
        composition = _nonempty_text(item.get("composition"))
        fallback = _nonempty_text(item.get("fallback"))
        if not all((purpose, kind, composition, fallback)):
            continue
        recommendations.append(
            AssetRecommendation(
                purpose=purpose,
                kind=kind,
                sources=_parse_asset_sources(item.get("sources")),
                composition=composition,
                fallback=fallback,
            )
        )
    return tuple(recommendations)


def _parse_asset_sources(value: object) -> tuple[AssetSource, ...]:
    if not isinstance(value, list):
        return ()
    sources: list[AssetSource] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        description = _nonempty_text(item.get("description"))
        url = _nonempty_text(item.get("url"))
        path = _nonempty_text(item.get("path"))
        revision = _nonempty_text(item.get("revision"))
        if description and (url or path):
            sources.append(
                AssetSource(
                    description=description,
                    url=url or None,
                    path=path or None,
                    revision=revision or None,
                )
            )
    return tuple(sources)


def _nonempty_text(value: object) -> str:
    return value.strip() if isinstance(value, str) and value.strip() else ""


def _parse_axis_pool(value: object) -> tuple:
    if not isinstance(value, list):
        return ()
    combos: list[dict[str, str]] = []
    for item in value:
        if not isinstance(item, dict) or not valid_axis_label(item.get("archetype")):
            continue
        combo = {"archetype": item["archetype"]}
        for key in ("primary_verifier_pattern", "persona"):
            if valid_axis_label(item.get(key)):
                combo[key] = item[key]
        combos.append(combo)
        if len(combos) >= MAX_AXIS_POOL_COMBOS:
            break
    return tuple(combos)


def _drain_stream(
    stream: Optional[object], targets: list[Optional[Path]], capture: list[str]
) -> None:
    if stream is None:
        return
    handles = []
    try:
        for path in targets:
            if path is None:
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            handles.append(path.open("a", encoding="utf-8"))
        for line in iter(stream.readline, ""):
            capture.append(line)
            for handle in handles:
                handle.write(line)
                handle.flush()
    finally:
        for handle in handles:
            handle.close()
        stream.close()


def _stage_bundle(bundle: SkillBundle, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    root = bundle.root.resolve()

    for current, directories, _ in os.walk(root, followlinks=False):
        current_path = Path(current)
        relative_dir = current_path.relative_to(root)
        (destination / relative_dir).mkdir(parents=True, exist_ok=True)
        for name in directories:
            source = current_path / name
            target = destination / relative_dir / name
            if source.is_symlink():
                _stage_internal_symlink(source, target, root, destination)
            else:
                target.mkdir(parents=True, exist_ok=True)

    for record in bundle.files:
        source_path = root / record.path
        source = source_path.resolve()
        try:
            source.relative_to(root)
        except ValueError as exc:
            raise GeneratorError(
                "source_escape", f"bundle file escaped source root: {record.path}"
            ) from exc
        target = destination / record.path
        target.parent.mkdir(parents=True, exist_ok=True)
        if source_path.is_symlink():
            _stage_internal_symlink(source_path, target, root, destination)
        else:
            shutil.copy2(source, target)


def _stage_internal_symlink(
    source: Path, target: Path, source_root: Path, destination_root: Path
) -> None:
    resolved = source.resolve()
    try:
        resolved_relative = resolved.relative_to(source_root)
    except ValueError as exc:
        raise GeneratorError(
            "source_escape", f"bundle symlink escaped source root: {source}"
        ) from exc
    staged_target = destination_root / resolved_relative
    relative_target = os.path.relpath(staged_target, start=target.parent)
    target.symlink_to(relative_target, target_is_directory=resolved.is_dir())


def _new_workspace(state_dir: Path, prefix: str) -> Path:
    workspaces = state_dir / "workspaces"
    workspaces.mkdir(parents=True, exist_ok=True)
    return Path(tempfile.mkdtemp(prefix=prefix, dir=workspaces)).resolve()


def _docker_user_args() -> list[str]:
    """Run the creator as the host user so bind-mounted files stay host-owned.

    Without this, the container defaults to root and leaves root-owned task
    trees that the host cannot rewrite (e.g. when authoring task.toml).
    """
    getuid = getattr(os, "getuid", None)
    getgid = getattr(os, "getgid", None)
    if getuid is None or getgid is None:
        return []
    return ["--user", f"{getuid()}:{getgid()}"]


def _safe_name(value: str) -> str:
    cleaned = "".join(char if char.isalnum() or char in "-_" else "-" for char in value)
    return cleaned.strip("-") or "skill"


def _bounded_output(result: subprocess.CompletedProcess[str], limit: int) -> str:
    value = (result.stdout or "") + (result.stderr or "")
    return value[-limit:] or f"command exited {result.returncode} without output"


def _host_command(command: list[str], *, timeout: int) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(command, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        raise GeneratorError(
            "docker_timeout", f"Docker command timed out after {timeout}s: {command[:3]!r}"
        ) from exc
    except OSError as exc:
        raise GeneratorError("docker_execution_failed", str(exc)) from exc
