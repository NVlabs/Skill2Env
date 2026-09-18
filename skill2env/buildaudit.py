# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Host-owned base-image checks and Harbor Oracle/NOP acceptance."""

from __future__ import annotations

import asyncio
import hashlib
import importlib.metadata
import json
import os
import re
import subprocess
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from threading import Lock
from typing import Any, Mapping, Protocol, Sequence

from harbor.job import Job
from harbor.models.job.config import DatasetConfig, JobConfig
from harbor.models.trial.config import AgentConfig, EnvironmentConfig

from .task_config import validate_harbor_task_toml
from .validation import reward_mean, reward_passes


_FROM = re.compile(
    r"^\s*FROM\s+(?:--platform=\S+\s+)?(\S+)(?:\s+AS\s+(\S+))?\s*$",
    re.IGNORECASE,
)
_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
_HEREDOC = re.compile(r"<<-?\s*(?P<quote>['\"]?)(?P<word>[A-Za-z0-9_.-]+)(?P=quote)")
APPROVED_REGISTRIES = {
    "docker.io",
    "ghcr.io",
    "mcr.microsoft.com",
    "public.ecr.aws",
    "quay.io",
}


class BuildAuditError(RuntimeError):
    """Raised when a candidate violates a deterministic host policy."""


class RegistryResolutionError(RuntimeError):
    """Raised after transient image resolution retries are exhausted."""


@dataclass
class BuildAuditReport:
    status: str
    reason_code: str | None = None
    errors: list[str] = field(default_factory=list)
    task_digest: str | None = None
    harbor_version: str | None = None
    base_image_digests: dict[str, str] = field(default_factory=dict)
    oracle_reward: dict[str, float | int] | None = None
    nop_reward: dict[str, float | int] | None = None

    @property
    def ok(self) -> bool:
        return self.status == "accepted"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class TaskAuditor(Protocol):
    def audit(self, task_dir: Path, *, audit_dir: Path) -> BuildAuditReport: ...


class TrialRunner(Protocol):
    def run(self, task_dir: Path, *, agent: str, jobs_dir: Path) -> dict[str, float | int]: ...


def external_base_images(dockerfile: str) -> list[str]:
    """Return static external FROM references, excluding scratch and prior stages."""
    aliases: set[str] = set()
    bases: list[str] = []
    seen: set[str] = set()
    for line in _dockerfile_instructions(dockerfile):
        if not re.match(r"^\s*FROM\b", line, re.IGNORECASE):
            continue
        match = _FROM.match(line)
        if match is None:
            raise BuildAuditError(f"unsupported FROM instruction: {line.strip()}")
        reference, alias = match.group(1), match.group(2)
        if "$" in reference:
            raise BuildAuditError(f"non-static FROM cannot be audited: {line.strip()}")
        key = reference.casefold()
        if key != "scratch" and key not in aliases and key not in seen:
            bases.append(reference)
            seen.add(key)
        if alias:
            aliases.add(alias.casefold())
    return bases


def _dockerfile_instructions(dockerfile: str) -> list[str]:
    instructions: list[str] = []
    current = ""
    heredoc_terminators: list[str] = []
    for raw_line in dockerfile.splitlines():
        if heredoc_terminators:
            if raw_line.strip() == heredoc_terminators[0]:
                heredoc_terminators.pop(0)
            continue
        stripped = raw_line.rstrip()
        current += stripped[:-1] + " " if stripped.endswith("\\") else stripped
        if stripped.endswith("\\"):
            continue
        instructions.append(current)
        heredoc_terminators = [
            match.group("word") for match in _HEREDOC.finditer(current)
        ]
        current = ""
    if current:
        instructions.append(current)
    if heredoc_terminators:
        raise BuildAuditError(f"unterminated Dockerfile heredoc: {heredoc_terminators[0]}")
    return instructions


class HarborTrialRunner:
    """Execute one local task with a built-in Harbor agent."""

    def run(
        self,
        task_dir: Path,
        *,
        agent: str,
        jobs_dir: Path,
    ) -> dict[str, float | int]:
        async def execute() -> dict[str, float | int]:
            config = JobConfig(
                job_name=agent,
                jobs_dir=jobs_dir,
                n_attempts=1,
                n_concurrent_trials=1,
                quiet=True,
                agents=[AgentConfig(name=agent)],
                datasets=[
                    DatasetConfig(
                        path=task_dir.parent,
                        task_names=[task_dir.name],
                    )
                ],
                environment=EnvironmentConfig(force_build=True, delete=True),
            )
            job = await Job.create(config)
            result = await job.run()
            if len(result.trial_results) != 1:
                raise BuildAuditError(
                    f"Harbor {agent} produced {len(result.trial_results)} trials"
                )
            trial = result.trial_results[0]
            if trial.exception_info is not None:
                raise BuildAuditError(
                    f"Harbor {agent} failed: {trial.exception_info.exception_type}: "
                    f"{trial.exception_info.exception_message}"
                )
            if trial.verifier_result is None or trial.verifier_result.rewards is None:
                raise BuildAuditError(f"Harbor {agent} produced no verifier reward")
            return trial.verifier_result.rewards

        return asyncio.run(execute())


class BuildAuditor:
    """Resolve public bases, then require Oracle pass and NOP fail in Harbor."""

    def __init__(
        self,
        *,
        trial_runner: TrialRunner | None = None,
        registry_attempts: int = 5,
        registry_timeout_sec: float = 120.0,
        retry_backoff_sec: float = 5.0,
        retry_max_backoff_sec: float = 120.0,
        nop_reward_threshold: float = 0.0,
    ):
        self.trial_runner = trial_runner or HarborTrialRunner()
        self.registry_attempts = registry_attempts
        self.registry_timeout_sec = registry_timeout_sec
        self.retry_backoff_sec = retry_backoff_sec
        self.retry_max_backoff_sec = retry_max_backoff_sec
        # Graded verifiers must not hand the pristine state free partial credit:
        # the mean NOP reward may not exceed this threshold.
        self.nop_reward_threshold = nop_reward_threshold
        # A batch shares one auditor across its workers. Cache only successfully
        # resolved immutable digests so repeated candidates do not exhaust the
        # registry while still requiring an initial authoritative resolution.
        self._base_image_cache: dict[str, str] = {}
        self._base_image_cache_lock = Lock()

    def audit(self, task_dir: Path, *, audit_dir: Path) -> BuildAuditReport:
        task_dir = task_dir.resolve()
        audit_dir.mkdir(parents=True, exist_ok=True)
        report = BuildAuditReport(
            status="rejected",
            task_digest=task_digest(task_dir),
            harbor_version=importlib.metadata.version("harbor"),
        )
        try:
            dockerfile = (task_dir / "environment" / "Dockerfile").read_text(
                encoding="utf-8"
            )
            bases = external_base_images(dockerfile)
            self._check_base_policy(bases)
        except (BuildAuditError, OSError, UnicodeDecodeError) as exc:
            report.reason_code = "base_image_policy"
            report.errors.append(str(exc))
            return report

        try:
            report.base_image_digests = self._resolve_bases(bases)
        except RegistryResolutionError as exc:
            report.status = "infra_failed"
            report.reason_code = "registry_unavailable"
            report.errors.append(str(exc))
            return report

        try:
            pin_dockerfile_digests(
                task_dir / "environment" / "Dockerfile", report.base_image_digests
            )
            record_task_base_image_pins(
                task_dir / "task.toml", report.base_image_digests
            )
            report.task_digest = task_digest(task_dir)
        except (BuildAuditError, OSError, UnicodeDecodeError, ValueError, TypeError) as exc:
            report.reason_code = "base_image_policy"
            report.errors.append(str(exc))
            return report

        try:
            report.oracle_reward = self.trial_runner.run(
                task_dir,
                agent="oracle",
                jobs_dir=audit_dir / "harbor",
            )
            if not reward_passes(report.oracle_reward):
                raise BuildAuditError("Harbor Oracle reward did not pass")
        except (BuildAuditError, OSError, RuntimeError, ValueError) as exc:
            report.reason_code = "oracle_failed"
            report.errors.append(str(exc))
            return report

        try:
            report.nop_reward = self.trial_runner.run(
                task_dir,
                agent="nop",
                jobs_dir=audit_dir / "harbor",
            )
            nop_mean = reward_mean(report.nop_reward)
            if nop_mean > self.nop_reward_threshold:
                raise BuildAuditError(
                    f"Harbor NOP earned reward on pristine state "
                    f"(mean {nop_mean:g} > threshold {self.nop_reward_threshold:g})"
                )
        except (BuildAuditError, OSError, RuntimeError, ValueError) as exc:
            report.reason_code = "nop_failed"
            report.errors.append(str(exc))
            return report

        report.status = "accepted"
        report.reason_code = None
        return report

    @staticmethod
    def _check_base_policy(bases: Sequence[str]) -> None:
        if not bases:
            raise BuildAuditError("Dockerfile must use at least one public base image")
        for reference in bases:
            registry = _registry_for(reference)
            if registry not in APPROVED_REGISTRIES:
                raise BuildAuditError(f"base image registry is not approved: {reference}")
            lowered = reference.casefold()
            if "skill2env" in lowered or any(
                part.startswith("task_") for part in lowered.split("/")
            ):
                raise BuildAuditError(f"local/generated base image is forbidden: {reference}")

    def _resolve_bases(self, bases: Sequence[str]) -> dict[str, str]:
        resolved: dict[str, str] = {}
        for base in bases:
            cache_key = base.casefold()
            with self._base_image_cache_lock:
                digest = self._base_image_cache.get(cache_key)
                if digest is None:
                    digest = self._resolve_base(base)
                    self._base_image_cache[cache_key] = digest
            resolved[base] = digest
        return resolved

    def _resolve_base(self, base: str) -> str:
        last_error = "no output"
        for attempt in range(1, self.registry_attempts + 1):
            try:
                result = _docker(
                    ["manifest", "inspect", "--verbose", base],
                    timeout=self.registry_timeout_sec,
                )
            except RegistryResolutionError as exc:
                last_error = str(exc)
            else:
                digest = _manifest_digest(result.stdout or "")
                if result.returncode == 0 and digest is not None:
                    return digest
                last_error = _tail(result)
            if attempt < self.registry_attempts:
                # Exponential backoff: Docker Hub's unauthenticated pull
                # limit needs far longer pauses than a linear ramp gives.
                time.sleep(
                    min(
                        self.retry_backoff_sec * (2 ** (attempt - 1)),
                        self.retry_max_backoff_sec,
                    )
                )
        raise RegistryResolutionError(
            f"registry resolution failed after "
            f"{self.registry_attempts} attempts for {base}: {last_error}"
        )


def _manifest_digest(value: str) -> str | None:
    """Extract one runnable Linux manifest digest from Docker's verbose JSON."""
    try:
        payload = json.loads(value)
    except json.JSONDecodeError:
        return None
    entries = payload if isinstance(payload, list) else [payload]
    fallback: str | None = None
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        descriptor = entry.get("Descriptor")
        if not isinstance(descriptor, dict):
            continue
        digest = descriptor.get("digest")
        if not isinstance(digest, str) or _DIGEST.fullmatch(digest) is None:
            continue
        fallback = fallback or digest
        target = descriptor.get("platform")
        if isinstance(target, dict) and target.get("os") == "linux":
            architecture = target.get("architecture")
            if isinstance(architecture, str) and architecture != "unknown":
                return digest
    return fallback


def pin_dockerfile_digests(path: Path, digests: dict[str, str]) -> None:
    """Rewrite external FROM references to include resolved content digests."""
    lines = path.read_text(encoding="utf-8").splitlines()
    aliases: set[str] = set()
    for index, line in enumerate(lines):
        match = _FROM.match(line)
        if match is None:
            continue
        reference, alias = match.group(1), match.group(2)
        key = reference.casefold()
        if key != "scratch" and key not in aliases and reference in digests and "@sha256:" not in reference:
            lines[index] = line.replace(reference, f"{reference}@{digests[reference]}", 1)
        if alias:
            aliases.add(alias.casefold())
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def record_task_base_image_pins(path: Path, digests: dict[str, str]) -> None:
    """Record resolved base image pins in host-authored task.toml metadata."""
    if not path.is_file():
        return
    config = validate_harbor_task_toml(path.read_text(encoding="utf-8"))
    metadata = dict(config.metadata or {})
    metadata["base_image_pins"] = dict(digests)
    updated = config.model_copy(update={"metadata": metadata})
    text = updated.model_dump_toml().rstrip() + "\n"
    validate_harbor_task_toml(text)
    path.write_text(text, encoding="utf-8")


def task_digest(task_dir: Path) -> str:
    """Hash a task tree deterministically, including paths and symlink targets."""
    digest = hashlib.sha256()
    root = task_dir.resolve()
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            digest.update(f"L\0{relative}\0{os.readlink(path)}\0".encode())
        elif path.is_file():
            digest.update(f"F\0{relative}\0".encode())
            with path.open("rb") as handle:
                while chunk := handle.read(1024 * 1024):
                    digest.update(chunk)
            digest.update(b"\0")
        elif path.is_dir():
            digest.update(f"D\0{relative}\0".encode())
    return digest.hexdigest()


def _registry_for(reference: str) -> str:
    without_digest = reference.split("@", 1)[0]
    if "/" not in without_digest:
        return "docker.io"
    first = without_digest.split("/", 1)[0]
    if "." in first or ":" in first or first == "localhost":
        return first.casefold()
    return "docker.io"


def _docker(
    args: Sequence[str],
    *,
    timeout: float,
    env: Mapping[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            ["docker", *args],
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
    except subprocess.TimeoutExpired as exc:
        raise RegistryResolutionError(
            f"docker {args[0]} timed out after {timeout:g}s"
        ) from exc
    except OSError as exc:
        raise RegistryResolutionError(f"docker {args[0]} failed: {exc}") from exc


def _tail(result: subprocess.CompletedProcess[str], limit: int = 4000) -> str:
    value = ((result.stdout or "") + (result.stderr or "")).strip()
    return value[-limit:] or f"docker exited {result.returncode} without output"
