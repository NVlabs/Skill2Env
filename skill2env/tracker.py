# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Durable, thread-safe generation run tracking."""

from __future__ import annotations

import json
import os
import secrets
import shutil
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, Optional


TERMINAL_JOB_STATUSES = {"succeeded", "failed", "skipped", "cancelled"}
TERMINAL_RUN_STATUSES = {"succeeded", "failed", "cancelled"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def new_run_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{stamp}-{secrets.token_hex(3)}"


def default_runs_root(cwd: Optional[Path] = None) -> Path:
    return (cwd or Path.cwd()) / ".skill2env" / "runs"


def make_job_id(skill_key: str, phase: str, variant: Optional[int] = None) -> str:
    if variant is None:
        raise ValueError("creator jobs require a variant index")
    return f"{skill_key}:{phase}:{variant:03d}"


def job_log_name(job_id: str) -> str:
    return job_id.replace(":", "-").replace("/", "-")


class RunTracker:
    """Append status events and atomically maintain a monitor-friendly snapshot."""

    schema_version = "1.0"

    def __init__(self, root: Path, manifest: Dict[str, Any]):
        self.root = root.expanduser().resolve()
        self.manifest = manifest
        self.run_id = str(manifest["run_id"])
        self._lock = threading.RLock()
        self._sequence = 0
        self._jobs: Dict[str, Dict[str, Any]] = {
            str(job["id"]): {
                "status": "queued",
                "stage": "queued",
                "message": "",
                "updated_at": manifest["started_at"],
            }
            for job in manifest["jobs"]
        }
        self._job_lookup = {
            (
                str(Path(job["state_dir"]).expanduser().resolve()),
                str(job["phase"]),
                job.get("variant"),
            ): str(job["id"])
            for job in manifest["jobs"]
        }
        self._run_status = "running"
        self._run_message = ""
        self._cancelled = threading.Event()
        # Optional observer invoked with each status snapshot (e.g. CLI progress).
        self.on_status: Optional[Callable[[Dict[str, Any]], None]] = None

    @classmethod
    def create(
        cls,
        root: Path,
        *,
        run_id: str,
        kind: str,
        config: Dict[str, Any],
        jobs: Iterable[Dict[str, Any]],
    ) -> "RunTracker":
        resolved_root = root.expanduser().resolve()
        resolved_root.mkdir(parents=True, exist_ok=True)
        for name in ("manifest.json", "events.jsonl", "status.json", "summary.json"):
            (resolved_root / name).unlink(missing_ok=True)
        shutil.rmtree(resolved_root / "jobs", ignore_errors=True)
        jobs_list = [dict(job) for job in jobs]
        started_at = utc_now()
        for job in jobs_list:
            job_id = str(job["id"])
            logs = resolved_root / "jobs" / job_log_name(job_id)
            logs.mkdir(parents=True, exist_ok=True)
            job["stdout_path"] = str(logs / "stdout.jsonl")
            job["stderr_path"] = str(logs / "stderr.log")
        manifest = {
            "schema_version": cls.schema_version,
            "run_id": run_id,
            "kind": kind,
            "started_at": started_at,
            "cwd": str(Path.cwd().resolve()),
            "config": config,
            "jobs": jobs_list,
        }
        _write_json_atomic(resolved_root / "manifest.json", manifest)
        tracker = cls(resolved_root, manifest)
        tracker._write_status()
        return tracker

    def job_id_for(
        self, state_dir: Path, phase: str, variant: Optional[int] = None
    ) -> Optional[str]:
        key = (str(state_dir.expanduser().resolve()), phase, variant)
        return self._job_lookup.get(key)

    def log_paths(self, job_id: str) -> tuple[Path, Path]:
        job = self.job_definition(job_id)
        return Path(job["stdout_path"]), Path(job["stderr_path"])

    def job_definition(self, job_id: str) -> Dict[str, Any]:
        for job in self.manifest["jobs"]:
            if job["id"] == job_id:
                return job
        raise KeyError(job_id)

    def job_status(self, job_id: str) -> str:
        with self._lock:
            return str(self._jobs[job_id]["status"])

    @property
    def cancelled(self) -> bool:
        return self._cancelled.is_set()

    def update_job(
        self,
        job_id: str,
        *,
        status: str,
        stage: str,
        message: str = "",
    ) -> None:
        if status not in {"queued", "running", *TERMINAL_JOB_STATUSES}:
            raise ValueError(f"invalid job status: {status}")
        with self._lock:
            current = self._jobs[job_id]["status"]
            if current in TERMINAL_JOB_STATUSES:
                return
            now = utc_now()
            self._jobs[job_id] = {
                "status": status,
                "stage": stage,
                "message": message,
                "updated_at": now,
            }
            self._append_event(
                {
                    "type": "job_status",
                    "job_id": job_id,
                    "status": status,
                    "stage": stage,
                    "message": message,
                    "timestamp": now,
                }
            )
            self._write_status()

    def update_run(self, message: str) -> None:
        with self._lock:
            if self._run_status in TERMINAL_RUN_STATUSES:
                return
            self._run_message = message
            now = utc_now()
            self._append_event(
                {
                    "type": "run_status",
                    "status": "running",
                    "message": message,
                    "timestamp": now,
                }
            )
            self._write_status()

    def finish(self, status: str, *, message: str = "", summary: Any = None) -> None:
        if status not in TERMINAL_RUN_STATUSES:
            raise ValueError(f"invalid terminal run status: {status}")
        with self._lock:
            if self._run_status in TERMINAL_RUN_STATUSES:
                return
            self._run_status = status
            self._run_message = message
            now = utc_now()
            self._append_event(
                {
                    "type": "run_status",
                    "status": status,
                    "message": message,
                    "timestamp": now,
                }
            )
            self._write_status()
            if summary is not None:
                _write_json_atomic(self.root / "summary.json", summary)

    def cancel_nonterminal(self, message: str) -> None:
        self._cancelled.set()
        with self._lock:
            for job_id, state in self._jobs.items():
                if state["status"] not in TERMINAL_JOB_STATUSES:
                    self.update_job(
                        job_id,
                        status="cancelled",
                        stage="cancelled",
                        message=message,
                    )

    def _append_event(self, payload: Dict[str, Any]) -> None:
        self._sequence += 1
        event = {
            "schema_version": self.schema_version,
            "run_id": self.run_id,
            "sequence": self._sequence,
            **payload,
        }
        events = self.root / "events.jsonl"
        with events.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
            handle.flush()
            os.fsync(handle.fileno())

    def _write_status(self) -> None:
        counts: Dict[str, int] = {}
        for state in self._jobs.values():
            status = str(state["status"])
            counts[status] = counts.get(status, 0) + 1
        payload = {
            "schema_version": self.schema_version,
            "run_id": self.run_id,
            "status": self._run_status,
            "message": self._run_message,
            "updated_at": utc_now(),
            "total_jobs": len(self._jobs),
            "terminal_jobs": sum(
                count for name, count in counts.items() if name in TERMINAL_JOB_STATUSES
            ),
            "counts": counts,
            "jobs": self._jobs,
        }
        _write_json_atomic(self.root / "status.json", payload)
        observer = self.on_status
        if observer is not None:
            try:
                observer(payload)
            except Exception:  # noqa: BLE001 - progress display must never break a run
                pass


def _write_json_atomic(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{secrets.token_hex(4)}.tmp")
    temporary.write_text(
        json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)
