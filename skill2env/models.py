# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Serializable contracts for task creation and run bookkeeping."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any, Dict, List, Optional

from .axes import validate_axis_values


CREATOR_STATUSES = {"created", "skipped"}
NETWORK_MODES = {"no-network"}
SKIP_REASON_CODES = {
    "external_account",
    "live_network",
    "physical_hardware",
    "gui_only",
    "proprietary_infra",
    "privileged_host",
    "human_approval",
    "non_terminal",
    "unsafe",
    "insufficient_instruction",
    "pure_knowledge",
    "unknown",
}
class ContractError(ValueError):
    """Raised when generated data violates a skill2env contract."""


@dataclass(frozen=True)
class FileRecord:
    path: str
    size: int
    sha256: str
    kind: str
    line_count: int = 0


@dataclass
class SkillBundle:
    id: str
    provider: str
    source_path: str
    root: Path
    entry_document: str
    name: str
    description: str
    license: str
    files: List[FileRecord]
    digest: str

    def provenance(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "provider": self.provider,
            "path": self.source_path,
            "entry_document": self.entry_document,
            "license": self.license,
            "bundle_digest": self.digest,
            "files": [asdict(item) for item in self.files],
        }


@dataclass(frozen=True)
class AssetSource:
    """One public or Skill-bundled source suggested by the planner."""

    description: str
    url: Optional[str] = None
    path: Optional[str] = None
    revision: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        value: Dict[str, Any] = {"description": self.description}
        if self.url is not None:
            value["url"] = self.url
        if self.path is not None:
            value["path"] = self.path
        if self.revision is not None:
            value["revision"] = self.revision
        return value


@dataclass(frozen=True)
class AssetRecommendation:
    """Planner guidance for constructing a workflow's realistic initial world."""

    purpose: str
    kind: str
    sources: tuple[AssetSource, ...]
    composition: str
    fallback: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "purpose": self.purpose,
            "kind": self.kind,
            "sources": [source.to_dict() for source in self.sources],
            "composition": self.composition,
            "fallback": self.fallback,
        }


@dataclass(frozen=True)
class Workflow:
    """One distinct instructed workflow identified by the planner pass.

    ``plan`` is free-form planner-owned metadata (scenario, world inventory,
    planted defects, solution sketch, verifier strategy, ...); the host passes
    it through to the creator without enforcing a field set.
    ``asset_recommendations`` is structured but advisory source/composition
    guidance. ``axis_pool`` is the planner's ranked list of suitable axis combos.
    """

    name: str
    summary: str
    plan: Dict[str, Any] = field(default_factory=dict)
    asset_recommendations: tuple[AssetRecommendation, ...] = ()
    axis_pool: tuple = ()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "summary": self.summary,
            "plan": dict(self.plan),
            "asset_recommendations": [
                recommendation.to_dict() for recommendation in self.asset_recommendations
            ],
            "axis_pool": [dict(combo) for combo in self.axis_pool],
        }


@dataclass(frozen=True)
class CreatorResult:
    """Private result written by the single creator invocation."""

    status: str
    skip_reason_code: Optional[str]
    skip_reason: Optional[str]
    description: str
    required_tools: List[str]
    expected_artifacts: List[str]
    network_mode: str
    allowed_hosts: List[str]
    realized_axes: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CreatorResult":
        if not isinstance(data, dict):
            raise ContractError("creator result must be an object")
        expected_fields = {
            "status",
            "skip_reason_code",
            "skip_reason",
            "description",
            "required_tools",
            "expected_artifacts",
            "network_mode",
            "allowed_hosts",
            "realized_axes",
        }
        unknown = set(data) - expected_fields
        missing = expected_fields - set(data)
        if unknown:
            raise ContractError(f"creator result has unknown fields: {sorted(unknown)!r}")
        if missing:
            raise ContractError(f"creator result is missing fields: {sorted(missing)!r}")

        status = _required_string(data, "status")
        if status not in CREATOR_STATUSES:
            raise ContractError(f"invalid creator status: {status!r}")
        reason_code = _optional_string(data.get("skip_reason_code"))
        reason = _optional_string(data.get("skip_reason"))
        description = _string(data.get("description"), "description")
        required_tools = _string_list(data, "required_tools")
        expected_artifacts = _string_list(data, "expected_artifacts")
        network_mode = _required_string(data, "network_mode")
        allowed_hosts = _string_list(data, "allowed_hosts")
        realized_axes = _string_dict(data, "realized_axes")
        axis_errors = validate_axis_values(realized_axes)
        if axis_errors:
            raise ContractError("; ".join(axis_errors))

        if network_mode not in NETWORK_MODES:
            raise ContractError("generated tasks must use network_mode 'no-network'")
        if allowed_hosts:
            raise ContractError("generated tasks cannot include allowed hosts")

        if status == "created":
            if reason_code is not None or reason is not None:
                raise ContractError("created result cannot have a skip reason")
            if not description:
                raise ContractError("created result requires a description")
            if not expected_artifacts:
                raise ContractError("created result requires expected artifacts")
            for key in ("archetype", "primary_verifier_pattern"):
                if key not in realized_axes:
                    raise ContractError(f"created result requires realized_axes.{key}")
            if any(
                not PurePosixPath(artifact).is_absolute()
                or ".." in PurePosixPath(artifact).parts
                for artifact in expected_artifacts
            ):
                raise ContractError("expected artifacts must be absolute environment paths")
        else:
            if reason_code not in SKIP_REASON_CODES:
                raise ContractError(f"invalid skip_reason_code: {reason_code!r}")
            if reason is None:
                raise ContractError("skipped result requires skip_reason")
            if description or required_tools or expected_artifacts:
                raise ContractError("skipped result cannot describe a task")
            if network_mode != "no-network" or allowed_hosts:
                raise ContractError("skipped result must use no-network")
            if realized_axes:
                raise ContractError("skipped result cannot include realized axes")

        return cls(
            status=status,
            skip_reason_code=reason_code,
            skip_reason=reason,
            description=description,
            required_tools=required_tools,
            expected_artifacts=expected_artifacts,
            network_mode=network_mode,
            allowed_hosts=allowed_hosts,
            realized_axes=realized_axes,
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class GenerationRecord:
    skill_id: str
    provider: str
    source_path: str
    status: str
    stage: str
    reason_code: Optional[str] = None
    reason: Optional[str] = None
    bundle_digest: Optional[str] = None
    task_dirs: List[str] = field(default_factory=list)
    attempts: List[Dict[str, Any]] = field(default_factory=list)
    generator_invocations: int = 0
    elapsed_seconds: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _required_string(data: Dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{key} must be a non-empty string")
    return value.strip()


def _string(value: Any, key: str) -> str:
    if not isinstance(value, str):
        raise ContractError(f"{key} must be a string")
    return value.strip()


def _optional_string(value: Any) -> Optional[str]:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ContractError("optional strings must be null or non-empty")
    return value.strip()


def _string_list(data: Dict[str, Any], key: str) -> List[str]:
    value = data.get(key)
    if not isinstance(value, list):
        raise ContractError(f"{key} must be a list")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise ContractError(f"{key} must contain only non-empty strings")
    result = [item.strip() for item in value]
    if len(result) != len(set(result)):
        raise ContractError(f"{key} must not contain duplicates")
    return result


def _string_dict(data: Dict[str, Any], key: str) -> Dict[str, str]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise ContractError(f"{key} must be an object")
    result: Dict[str, str] = {}
    for raw_key, raw_value in value.items():
        if not isinstance(raw_key, str) or not raw_key.strip():
            raise ContractError(f"{key} keys must be non-empty strings")
        if not isinstance(raw_value, str) or not raw_value.strip():
            raise ContractError(f"{key}.{raw_key} must be a non-empty string")
        result[raw_key.strip()] = raw_value.strip()
    return result
