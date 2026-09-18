"""Stage 7: Iteration & Closure Validator

Stage 7 is terminal but still gated. Its core responsibility is cascade integrity: when a key deliverable changes during iteration, downstream deliverables must be refreshed in order. Broken critical chains block; ordinary close-out quality issues remain warnings.
"""

import os

from .common import ValidationResult, file_exists, file_size_bytes, load_state


CASCADE_CHAIN = [
    ("research_plan.md", 3, "research_definition.md", 2),
    ("evidence_base.md", 4, "research_plan.md", 3),
    ("insights.md", 5, "evidence_base.md", 4),
    ("report.html", 6, "insights.md", 5),
]

MTIME_TOLERANCE = 60


def _get_mtime(workspace, filename):
    path = os.path.join(workspace, filename)
    if os.path.isfile(path):
        return os.path.getmtime(path)
    return None


def validate(workspace):
    r = ValidationResult(7)

    if not file_exists(workspace, "report.html"):
        r.fail("report.html missing; Stage 7 cannot pass without final report")
        return r
    r.pass_check("report.html exists")

    if not file_exists(workspace, "insights.md"):
        r.warn("insights.md missing; iteration may lack insight context")
    else:
        r.pass_check("insights.md exists")

    if not file_exists(workspace, "evidence_base.md"):
        r.warn("evidence_base.md missing; iteration may lack evidence context")
    else:
        r.pass_check("evidence_base.md exists")

    size = file_size_bytes(workspace, "report.html")
    if size < 5000:
        r.warn(f"report.html is only {size} bytes; iterated report may be incomplete")
    else:
        r.pass_check(f"report.html size: {size} bytes")

    state = load_state(workspace)
    if state is None:
        r.warn("cannot read _state.json; skipping cascade integrity check")
        return r

    current_stage = state.get("current_stage")
    if current_stage != 7:
        r.pass_check(f"current Stage {current_stage}; cascade integrity check runs only in Stage 7")
        return r

    r.pass_check("_state.json confirms Stage 7; running cascade integrity check")

    upstream_updates = []
    chain_intact = True

    for downstream, ds_stage, upstream, us_stage in CASCADE_CHAIN:
        downstream_mtime = _get_mtime(workspace, downstream)
        upstream_mtime = _get_mtime(workspace, upstream)

        if downstream_mtime is None:
            r.fail(f"cascade chain broken: stage {ds_stage} deliverable {downstream} missing (upstream stage {us_stage} deliverable {upstream} exists)")
            chain_intact = False
            continue

        if upstream_mtime is None:
            r.fail(f"cascade chain anomaly: upstream stage {us_stage} deliverable {upstream} missing, but downstream {downstream} exists")
            chain_intact = False
            continue

        if upstream_mtime > downstream_mtime + MTIME_TOLERANCE:
            gap_sec = int(upstream_mtime - downstream_mtime)
            upstream_updates.append(f"stage {us_stage} deliverable {upstream} is newer than stage {ds_stage} deliverable {downstream} by {gap_sec}s")
            chain_intact = False
        else:
            r.pass_check(f"cascade intact: {upstream} → {downstream}")

    if upstream_updates:
        for issue in upstream_updates:
            r.fail(f"cascade incomplete: {issue}")
        r.warn("Cascade rule: after an upstream deliverable changes, rerun downstream stages in order (data update S4->S5->S6 / insight update S5->S6 / direction update S2->...->S6)")
    elif chain_intact:
        r.pass_check("Cascade integrity passed: all upstream deliverable timestamps are <= downstream deliverables")

    disclosure_log = state.get("disclosure_log", [])
    stage7_writes = [e for e in disclosure_log if e.get("stage") == 7 and e.get("type") == "file_load"]
    if stage7_writes:
        r.pass_check(f"Stage 7 iteration file-load records: {len(stage7_writes)} file loads")

    return r
