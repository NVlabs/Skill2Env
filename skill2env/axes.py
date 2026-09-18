# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Sampling axes for skill-grounded task generation.

Archetype, primary-verifier-pattern, and persona labels form an OPEN
vocabulary. The catalogs below are examples shipped to the planner agent,
which proposes a ranked per-workflow ``axis_pool`` of combos (and may coin new
labels). The host samples afresh from that pool for every attempt; the keyword
classifier survives only as a fallback for workflows with no usable pool.
"""

from __future__ import annotations

import random
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence


ARCHETYPE_EXAMPLES: Mapping[str, str] = {
    "repair_debug": "diagnose and fix defects in an existing system until behavior is correct",
    "build_to_spec": "build a new artifact, service, or program that satisfies a precise spec",
    "repo_change": "resolve an issue or implement a scoped feature in an existing real repository while preserving its behavior and tests",
    "system_build_repair": "build, compile, install, or repair a system or toolchain under realistic dependency and runtime constraints",
    "service_runtime": "implement or debug a service, CLI, daemon, or protocol including process lifecycle, concurrency, and error paths",
    "interactive_qa": "exercise an existing browser or interactive application through realistic headless flows and verify observable behavior",
    "operate_configure": "configure, deploy, migrate, or operate a seeded local system until it reaches a required state",
    "audit_report": "inspect evidence to diagnose root causes or assess explicit criteria and produce structured findings without necessarily changing the system",
    "transform_convert": "convert data or documents between formats without losing meaning",
    "edit_preserve": "modify an existing document, media, data, or design artifact while preserving unaffected content and fidelity",
    "author_to_constraints": "author a document, design, or artifact satisfying hard constraints",
    "optimize_metric": "improve a measurable metric without breaking functional correctness",
    "data_query": "query or analyze seeded data with reproducible statistics, modeling, or forecasting and report checkable results",
    "investigate_synthesize": "research a seeded local corpus and synthesize a cited, checkable report",
    "plan_decide": "produce a decision memo or deck from messy inputs under reconciliation constraints",
    "harden_secure": "find and fix security weaknesses while keeping behavior intact",
    "author_tests": "write tests, fuzzers, or analysis rules that catch planted defects",
    "creative_build": "build a game, visual, or interactive artifact verified by headless simulation",
}

PRIMARY_VERIFIER_PATTERN_EXAMPLES: Mapping[str, str] = {
    "exact_state": "assert final files, persisted state, and cross-file invariants directly",
    "metric_threshold": "measure a deterministic metric against a documented threshold",
    "protocol_conformance": "exercise schemas, transitions, and error paths against local fixtures",
    "differential_equivalence": "compare behavior against a private reference oracle over many inputs",
    "adversarial_corpus": "ship planted positives and negatives; verify both directions",
    "behavioral_simulation": "drive a program, browser, or interactive artifact headlessly over deterministic scripted inputs and assert its behavior",
    "regression_suite": "ship an executable test suite the solution must make pass without breaking planted guards",
    "rendered_artifact": "render a document, media, or UI artifact and assert its content, geometry, metadata, and fidelity",
    "evidence_traceability": "verify claims and findings trace to seeded sources and cover planted evidence",
    "metamorphic_invariants": "exercise many inputs and assert round-trip, idempotence, monotonicity, or relation-preserving properties",
}

PERSONA_EXAMPLES: Mapping[str, str] = {
    "software_engineer": "an engineer who builds, maintains, and debugs software systems",
    "platform_engineer": "an engineer who develops internal platforms, tooling, and integrations",
    "site_reliability_engineer": "an engineer who operates reliable production services",
    "quality_engineer": "an engineer who designs tests and validates product behavior",
    "performance_engineer": "an engineer who measures and improves system performance",
    "data_engineer": "an engineer who builds and maintains data pipelines and transformations",
    "data_analyst": "an analyst who answers operational and business questions from data",
    "security_engineer": "an engineer who finds and remediates security weaknesses",
    "security_auditor": "an auditor who evaluates systems against security controls",
    "product_designer": "a designer who creates usable visual and interactive artifacts",
    "document_specialist": "a specialist who creates and transforms structured documents",
    "technical_writer": "a writer who produces precise technical documentation",
    "researcher": "a researcher who synthesizes evidence into defensible findings",
    "product_manager": "a manager who turns evidence and constraints into product decisions",
    "executive": "an executive who makes strategic decisions from concise evidence",
    "growth_marketer": "a marketer who measures and improves acquisition or conversion",
    "game_developer": "a developer who builds and tests interactive game systems",
    "compliance_officer": "an officer who evaluates policy and regulatory conformance",
    "support_engineer": "an engineer who reproduces and resolves customer problems",
}

ARCHETYPES = tuple(ARCHETYPE_EXAMPLES)
PRIMARY_VERIFIER_PATTERNS = tuple(PRIMARY_VERIFIER_PATTERN_EXAMPLES)
PERSONAS = tuple(PERSONA_EXAMPLES)

# Complexity is the expected number of tool-calling turns (one shell command or
# file edit per turn) a competent terminal agent needs from the pristine state.
COMPLEXITY_TURNS: Mapping[str, str] = {
    "easy": "3-5",
    "medium": "5-10",
    "hard": "10-20",
    "complex": "20+",
}
COMPLEXITIES = tuple(COMPLEXITY_TURNS)
_COMPLEXITY_WEIGHTS = (2, 3, 3, 2)


def complexity_turns(level: str) -> str | None:
    """Expected solution-turn range for a complexity level, or None if unknown."""
    return COMPLEXITY_TURNS.get(level)


def complexity_label(level: str) -> str:
    """Human-readable tag such as ``hard (solvable in 10-20 turns)``; unknown levels pass through."""
    turns = complexity_turns(level)
    return f"{level} (solvable in {turns} turns)" if turns else level


TONES = ("first_person_ask", "imperative_brief", "ticket_snippet", "example_driven")
EXPERTISE_LEVELS = ("novice", "practitioner", "expert")

AXIS_KEYS = (
    "archetype",
    "primary_verifier_pattern",
    "complexity",
    "persona",
    "tone",
    "expertise",
)
_LABEL_PATTERN = re.compile(r"^[a-z][a-z0-9_-]{0,47}$")

_ARCHETYPE_KEYWORDS: Mapping[str, tuple[str, ...]] = {
    "repair_debug": ("debug", "fix", "repair", "troubleshoot", "diagnose", "bug"),
    "build_to_spec": ("scaffold", "create", "build", "generate", "starter", "template", "mcp"),
    "repo_change": (
        "repository",
        "repo",
        "github",
        "issue",
        "pull request",
        "regression",
        "existing codebase",
        "feature request",
    ),
    "system_build_repair": (
        "compile",
        "compiler",
        "build failure",
        "build system",
        "toolchain",
        "linker",
        "package",
        "install",
        "binary",
        "qemu",
    ),
    "service_runtime": (
        "service",
        "server",
        "daemon",
        "grpc",
        "socket",
        "protocol",
        "endpoint",
        "background process",
        "async",
        "concurrency",
    ),
    "interactive_qa": (
        "browser qa",
        "webapp testing",
        "playwright",
        "selenium",
        "headless browser",
        "end-to-end",
        "e2e",
        "form filling",
    ),
    "operate_configure": (
        "configure",
        "configuration",
        "deploy",
        "deployment",
        "migration",
        "provision",
        "rollout",
        "runbook",
        "backup",
        "restore",
    ),
    "audit_report": (
        "audit",
        "review",
        "best practice",
        "vulnerab",
        "accessibility",
        "compliance",
        "root cause",
        "rca",
        "incident triage",
        "findings",
    ),
    "transform_convert": (
        "convert",
        "transform",
        "extract",
        "parse",
        "format",
        "docx",
        "pdf",
        "xlsx",
        "pptx",
    ),
    "edit_preserve": (
        "edit existing",
        "modify existing",
        "update existing",
        "preserve formatting",
        "preserve layout",
        "existing document",
        "existing spreadsheet",
        "existing presentation",
    ),
    "author_to_constraints": ("author", "write", "design", "presentation", "report", "artifact"),
    "optimize_metric": ("optimize", "performance", "latency", "speed", "memory"),
    "data_query": (
        "sql",
        "duckdb",
        "query",
        "database",
        "dataset",
        "analytics",
        "statistics",
        "statistical",
        "modeling",
        "forecast",
        "simulation",
        "regression",
    ),
    "investigate_synthesize": (
        "research",
        "investigate",
        "sources",
        "citation",
        "literature",
        "dossier",
    ),
    "plan_decide": ("decision", "strategy", "board", "memo", "roadmap", "stakeholder"),
    "harden_secure": ("security", "harden", "exploit", "sanitize", "cve", "injection"),
    "author_tests": ("test", "fuzz", "coverage", "property-based", "semgrep", "mutation"),
    "creative_build": ("game", "animation", "canvas", "art", "interactive", "frontend"),
}

_VERIFIER_PATTERNS_BY_ARCHETYPE: Mapping[str, tuple[str, ...]] = {
    "repair_debug": ("exact_state", "regression_suite", "differential_equivalence"),
    "build_to_spec": ("exact_state", "protocol_conformance", "behavioral_simulation"),
    "repo_change": ("regression_suite", "differential_equivalence", "exact_state"),
    "system_build_repair": ("regression_suite", "exact_state", "metric_threshold"),
    "service_runtime": ("protocol_conformance", "regression_suite", "behavioral_simulation"),
    "interactive_qa": ("behavioral_simulation", "rendered_artifact", "regression_suite"),
    "operate_configure": ("exact_state", "regression_suite", "protocol_conformance"),
    "audit_report": ("adversarial_corpus", "evidence_traceability", "exact_state"),
    "transform_convert": (
        "differential_equivalence",
        "metamorphic_invariants",
        "exact_state",
        "rendered_artifact",
    ),
    "edit_preserve": ("rendered_artifact", "exact_state", "metamorphic_invariants"),
    "author_to_constraints": (
        "exact_state",
        "rendered_artifact",
        "differential_equivalence",
        "metric_threshold",
    ),
    "optimize_metric": ("metric_threshold", "exact_state"),
    "data_query": (
        "exact_state",
        "metamorphic_invariants",
        "differential_equivalence",
        "metric_threshold",
    ),
    "investigate_synthesize": ("evidence_traceability", "exact_state", "adversarial_corpus"),
    "plan_decide": ("exact_state", "metric_threshold"),
    "harden_secure": ("adversarial_corpus", "regression_suite", "exact_state"),
    "author_tests": ("adversarial_corpus", "differential_equivalence"),
    "creative_build": (
        "behavioral_simulation",
        "rendered_artifact",
        "metric_threshold",
        "exact_state",
    ),
}

_PERSONA_BY_ARCHETYPE: Mapping[str, tuple[str, ...]] = {
    "repair_debug": ("software_engineer", "support_engineer", "site_reliability_engineer"),
    "build_to_spec": ("software_engineer", "platform_engineer", "product_designer"),
    "repo_change": ("software_engineer", "quality_engineer", "support_engineer"),
    "system_build_repair": (
        "platform_engineer",
        "software_engineer",
        "performance_engineer",
    ),
    "service_runtime": (
        "platform_engineer",
        "site_reliability_engineer",
        "software_engineer",
    ),
    "interactive_qa": ("quality_engineer", "software_engineer", "product_designer"),
    "operate_configure": (
        "platform_engineer",
        "site_reliability_engineer",
        "software_engineer",
    ),
    "audit_report": ("security_auditor", "compliance_officer", "quality_engineer"),
    "transform_convert": ("data_engineer", "document_specialist", "software_engineer"),
    "edit_preserve": ("document_specialist", "product_designer", "data_engineer"),
    "author_to_constraints": ("technical_writer", "product_designer", "document_specialist"),
    "optimize_metric": (
        "performance_engineer",
        "site_reliability_engineer",
        "growth_marketer",
    ),
    "data_query": ("data_analyst", "data_engineer", "researcher"),
    "investigate_synthesize": ("researcher", "data_analyst", "product_manager"),
    "plan_decide": ("product_manager", "executive", "data_analyst"),
    "harden_secure": ("security_engineer", "software_engineer", "platform_engineer"),
    "author_tests": ("quality_engineer", "software_engineer", "security_engineer"),
    "creative_build": ("game_developer", "product_designer", "software_engineer"),
}


@dataclass(frozen=True)
class TaskAxes:
    archetype: str
    primary_verifier_pattern: str
    complexity: str
    persona: str
    tone: str
    expertise: str

    def to_dict(self) -> dict[str, str]:
        value = asdict(self)
        # Public metadata carries the expected-turn range, e.g. "hard (solvable in 10-20 turns)".
        value["complexity"] = complexity_label(self.complexity)
        return value


@dataclass(frozen=True)
class AxisPreference(TaskAxes):
    """Host-sampled target axes plus ordered fallbacks for creator realization."""

    fallbacks: tuple[str, ...]
    verifier_pattern_fallbacks: tuple[str, ...] = ()

    @property
    def primary(self) -> str:
        return self.archetype

    def allowed_archetypes(self) -> tuple[str, ...]:
        return (self.archetype, *self.fallbacks)

    def allowed_verifier_patterns(self) -> tuple[str, ...]:
        return (self.primary_verifier_pattern, *self.verifier_pattern_fallbacks)

    def to_dict(self) -> dict[str, Any]:
        return {
            **super().to_dict(),
            "primary": self.primary,
            "fallbacks": list(self.fallbacks),
            "verifier_pattern_fallbacks": list(self.verifier_pattern_fallbacks),
        }


def sample_axes(
    bundle: Any,
    variant_index: int,
    workflow: Any = None,
    *,
    rng: random.Random | None = None,
) -> AxisPreference:
    """Sample a fresh target shape, preferring the planner's per-workflow pool."""
    del variant_index  # Variant identity must not make repeated runs deterministic.
    rng = rng if rng is not None else random.SystemRandom()
    pool = _usable_pool(workflow)
    if pool:
        primary_combo, rest = _pick_combo(rng, pool)
        archetype = primary_combo["archetype"]
        primary_verifier_pattern = primary_combo.get("primary_verifier_pattern") or rng.choice(
            _default_verifier_patterns(archetype)
        )
        persona = primary_combo.get("persona") or rng.choice(
            _PERSONA_BY_ARCHETYPE.get(archetype, PERSONAS)
        )
        fallbacks = _unique(
            [combo["archetype"] for combo in rest if combo["archetype"] != archetype]
        )
        verifier_pattern_fallbacks = _unique(
            [
                pattern
                for combo in rest
                if (pattern := combo.get("primary_verifier_pattern"))
                and pattern != primary_verifier_pattern
            ]
        )
    else:
        weights = classify_skill(bundle)
        archetype = _weighted_choice(rng, weights)
        fallbacks = tuple(item for item in _ranked_rest(rng, weights) if item != archetype)
        primary_verifier_pattern = rng.choice(_default_verifier_patterns(archetype))
        verifier_pattern_fallbacks = _unique(
            [
                pattern
                for pattern in _default_verifier_patterns(archetype)
                if pattern != primary_verifier_pattern
            ]
            + [
                pattern
                for pattern in PRIMARY_VERIFIER_PATTERNS
                if pattern != primary_verifier_pattern
            ]
        )
        persona = rng.choice(_PERSONA_BY_ARCHETYPE.get(archetype, PERSONAS))

    complexity = rng.choices(COMPLEXITIES, weights=_COMPLEXITY_WEIGHTS, k=1)[0]
    tone = rng.choices(TONES, weights=(5, 4, 2, 3), k=1)[0]
    expertise = rng.choices(EXPERTISE_LEVELS, weights=(2, 6, 2), k=1)[0]
    return AxisPreference(
        archetype=archetype,
        fallbacks=fallbacks,
        primary_verifier_pattern=primary_verifier_pattern,
        verifier_pattern_fallbacks=verifier_pattern_fallbacks,
        complexity=complexity,
        persona=persona,
        tone=tone,
        expertise=expertise,
    )


def valid_axis_label(value: Any) -> bool:
    return isinstance(value, str) and _LABEL_PATTERN.fullmatch(value) is not None


def validate_axis_values(values: Mapping[str, str]) -> list[str]:
    """Shape-only validation: known keys, open slug-style label vocabulary."""
    errors: list[str] = []
    for key, value in values.items():
        if key not in AXIS_KEYS:
            errors.append(f"unknown realized_axes key: {key}")
        elif not valid_axis_label(value):
            errors.append(
                f"invalid realized_axes.{key}: {value!r} (expected a short lowercase slug)"
            )
    return errors


def classify_skill(bundle: Any) -> dict[str, float]:
    """Keyword fallback used only when a workflow carries no planner axis pool."""
    text = _bundle_text(bundle)
    weights = {name: 1.0 for name in ARCHETYPES}
    for archetype, keywords in _ARCHETYPE_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            score += len(re.findall(re.escape(keyword), text))
        if score:
            weights[archetype] += min(score * 2.0, 12.0)
    return weights


def _usable_pool(workflow: Any) -> list[dict[str, str]]:
    pool = getattr(workflow, "axis_pool", None) or ()
    combos: list[dict[str, str]] = []
    for combo in pool:
        if not isinstance(combo, Mapping) or not valid_axis_label(combo.get("archetype")):
            continue
        cleaned: dict[str, str] = {"archetype": combo["archetype"]}
        for key in ("primary_verifier_pattern", "persona"):
            if valid_axis_label(combo.get(key)):
                cleaned[key] = combo[key]
        combos.append(cleaned)
    return combos


def _pick_combo(
    rng: random.Random, pool: Sequence[dict[str, str]]
) -> tuple[dict[str, str], list[dict[str, str]]]:
    """Rank-weighted primary choice; remaining combos keep their planner order."""
    weights = [len(pool) - index for index in range(len(pool))]
    chosen = rng.choices(range(len(pool)), weights=weights, k=1)[0]
    rest = [combo for index, combo in enumerate(pool) if index != chosen]
    return pool[chosen], rest


def _default_verifier_patterns(archetype: str) -> tuple[str, ...]:
    return _VERIFIER_PATTERNS_BY_ARCHETYPE.get(archetype, ("exact_state",))


def _unique(values: Sequence[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return tuple(result)


def _weighted_choice(rng: random.Random, weights: Mapping[str, float]) -> str:
    names = list(weights)
    values = [max(float(weights[name]), 0.0) for name in names]
    return rng.choices(names, weights=values, k=1)[0]


def _ranked_rest(rng: random.Random, weights: Mapping[str, float]) -> list[str]:
    jittered = [(float(weight) + rng.random() * 0.01, name) for name, weight in weights.items()]
    return [name for _, name in sorted(jittered, reverse=True)]


def _bundle_text(bundle: Any) -> str:
    parts = [
        str(getattr(bundle, "id", "")),
        str(getattr(bundle, "name", "")),
        str(getattr(bundle, "description", "")),
        str(getattr(bundle, "entry_document", "")),
    ]
    root = Path(getattr(bundle, "root", ""))
    for record in getattr(bundle, "files", []):
        path = str(getattr(record, "path", ""))
        parts.append(path)
        if getattr(record, "kind", None) != "text":
            continue
        source = root / path
        if path == getattr(bundle, "entry_document", "") or source.name == "SKILL.md":
            try:
                parts.append(source.read_text(encoding="utf-8")[:20000])
            except (OSError, UnicodeDecodeError):
                pass
    return "\n".join(parts).casefold()
