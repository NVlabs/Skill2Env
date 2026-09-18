# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Authoritative Harbor task configuration generation and validation."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Mapping

from harbor.models.task.config import (
    AgentConfig,
    Author,
    EnvironmentConfig,
    PackageInfo,
    SolutionConfig,
    TaskConfig,
    VerifierConfig,
)
from pydantic import ValidationError

from .axes import TaskAxes
from .models import ContractError, CreatorResult, SkillBundle


TASK_SCHEMA_VERSION = "1.3"
TASK_PACKAGE_ORG = "skill2env"
TASK_AUTHOR_NAME = "skill2env"

AGENT_TIMEOUT_SEC = 1800.0
VERIFIER_TIMEOUT_SEC = 600.0
ENVIRONMENT_BUILD_TIMEOUT_SEC = 1200.0
ENVIRONMENT_CPUS = 2
ENVIRONMENT_MEMORY_MB = 4096
ENVIRONMENT_STORAGE_MB = 4096
TASK_NETWORK_MODE = "no-network"


class HarborTaskConfigError(ContractError):
    """Raised when Harbor rejects a task configuration."""


def authoritative_task_name(task_name: str) -> str:
    """Return the deterministic Harbor package name for an output directory."""
    return f"{TASK_PACKAGE_ORG}/{task_name}"


def build_authoritative_task_config(
    *,
    task_name: str,
    bundle: SkillBundle,
    creator_result: CreatorResult,
    axes: TaskAxes | None = None,
    base_image_pins: Mapping[str, str] | None = None,
) -> TaskConfig:
    """Build task.toml from the bundle and validated private creator result."""
    if creator_result.status != "created":
        raise HarborTaskConfigError("task config requires a created result")

    metadata = {
        "source_skill": f"{bundle.provider}/{bundle.id}",
        "source_bundle_digest": bundle.digest,
    }
    if axes is not None:
        metadata.update(axes.to_dict())
    if base_image_pins is not None:
        metadata["base_image_pins"] = dict(base_image_pins)

    config = TaskConfig(
        schema_version=TASK_SCHEMA_VERSION,
        task=PackageInfo(
            name=authoritative_task_name(task_name),
            description=creator_result.description,
            keywords=_task_keywords(bundle, creator_result, axes),
            authors=[Author(name=TASK_AUTHOR_NAME)],
        ),
        metadata=metadata,
        agent=AgentConfig(
            timeout_sec=AGENT_TIMEOUT_SEC,
            network_mode=TASK_NETWORK_MODE,
            allowed_hosts=[],
        ),
        verifier=VerifierConfig(
            timeout_sec=VERIFIER_TIMEOUT_SEC,
            network_mode=TASK_NETWORK_MODE,
            allowed_hosts=[],
        ),
        environment=EnvironmentConfig(
            build_timeout_sec=ENVIRONMENT_BUILD_TIMEOUT_SEC,
            cpus=ENVIRONMENT_CPUS,
            memory_mb=ENVIRONMENT_MEMORY_MB,
            storage_mb=ENVIRONMENT_STORAGE_MB,
            network_mode=TASK_NETWORK_MODE,
            allowed_hosts=[],
        ),
        solution=SolutionConfig(),
        artifacts=list(creator_result.expected_artifacts),
    )
    # Validate the serialized representation too; this is the exact form written to disk.
    validate_harbor_task_toml(config.model_dump_toml())
    return config


def write_authoritative_task_toml(
    task_dir: Path,
    *,
    task_name: str,
    bundle: SkillBundle,
    creator_result: CreatorResult,
    axes: TaskAxes | None = None,
    base_image_pins: Mapping[str, str] | None = None,
) -> Path:
    """Replace any agent-authored task.toml with the authoritative host version."""
    config = build_authoritative_task_config(
        task_name=task_name,
        bundle=bundle,
        creator_result=creator_result,
        axes=axes,
        base_image_pins=base_image_pins,
    )
    text = config.model_dump_toml().rstrip() + "\n"
    validate_harbor_task_toml(text)
    path = task_dir / "task.toml"
    path.write_text(text, encoding="utf-8")
    return path


def validate_harbor_task_toml(text: str) -> TaskConfig:
    """Parse task TOML with Harbor's real TaskConfig model."""
    try:
        return TaskConfig.model_validate_toml(text)
    except (ValidationError, ValueError, TypeError) as exc:
        detail = " | ".join(part.strip() for part in str(exc).splitlines() if part.strip())
        raise HarborTaskConfigError(f"Harbor TaskConfig rejected task.toml: {detail}") from exc


def _task_keywords(
    bundle: SkillBundle, creator_result: CreatorResult, axes: TaskAxes | None
) -> list[str]:
    axis_keywords = [axes.archetype, axes.complexity] if axes is not None else []
    return _unique_nonempty([bundle.id, *axis_keywords, *creator_result.required_tools]) or [
        "skill2env"
    ]


def _unique_nonempty(values: Iterable[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        normalized = value.strip()
        key = normalized.casefold()
        if normalized and key not in seen:
            result.append(normalized)
            seen.add(key)
    return result
