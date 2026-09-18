"""
Schedule helper for agent-manager skill.

Manages crontab entries for scheduled agent jobs.
"""

from __future__ import annotations
import shlex
import subprocess
from pathlib import Path
from typing import List, Optional

from agent_config import list_all_schedules, list_all_heartbeats, resolve_agent, get_schedule_task, parse_duration
from repo_root import get_repo_root


# Markers for our crontab section
CRONTAB_START_MARKER = "# === agent-manager schedules (auto-generated) ==="
CRONTAB_END_MARKER = "# === end agent-manager schedules ==="


def _get_agent_manager_section(crontab: str) -> str:
    """Extract the agent-manager section (including markers) from a crontab."""
    lines = crontab.splitlines()
    in_section = False
    section_lines: List[str] = []

    for line in lines:
        if CRONTAB_START_MARKER in line:
            in_section = True
        if in_section:
            section_lines.append(line)
        if CRONTAB_END_MARKER in line and in_section:
            break

    return "\n".join(section_lines)


def _count_cron_entries(section: str) -> int:
    """Count cron entry lines (non-empty, non-comment) inside a section."""
    if not section:
        return 0
    count = 0
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith('#'):
            continue
        count += 1
    return count


def get_current_crontab() -> str:
    """Get current user's crontab content."""
    try:
        result = subprocess.run(
            ['crontab', '-l'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout
        return ""
    except Exception:
        return ""


def set_crontab(content: str) -> bool:
    """Set user's crontab content."""
    try:
        result = subprocess.run(
            ['crontab', '-'],
            input=content,
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception:
        return False


def remove_agent_manager_section(crontab: str) -> str:
    """Remove agent-manager section from crontab content."""
    lines = crontab.split('\n')
    result = []
    in_section = False

    for line in lines:
        if CRONTAB_START_MARKER in line:
            in_section = True
            continue
        if CRONTAB_END_MARKER in line:
            in_section = False
            continue
        if not in_section:
            result.append(line)

    # Remove trailing empty lines
    while result and not result[-1].strip():
        result.pop()

    return '\n'.join(result)


def generate_crontab_entries(repo_root: Optional[Path] = None) -> str:
    """
    Generate crontab entries for all scheduled agent jobs and heartbeats.

    Returns:
        Crontab section with all agent schedules and heartbeats
    """
    if repo_root is None:
        repo_root = get_repo_root()

    schedules = list_all_schedules()
    heartbeats = list_all_heartbeats()

    if not schedules and not heartbeats:
        return ""

    lines = [CRONTAB_START_MARKER]

    # Add PATH environment variable for crontab execution
    # This ensures commands like tmux can be found when running via cron
    lines.append("# Set PATH for cron jobs (include user-local bins for CLIs like codex)")
    lines.append('PATH=$HOME/.local/bin:$HOME/bin:/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin')
    lines.append("")

    # Group by agent file_id for readability (names may not be unique)
    current_agent_file_id = None

    # Add schedules first
    for sched in schedules:
        # Skip if schedule is disabled
        if not sched.get('enabled', True):
            continue

        # Skip if agent is disabled
        agent_config = resolve_agent(sched['file_id'])
        if agent_config and not agent_config.get('enabled', True):
            continue

        cron = sched.get('cron', '')
        if not cron:
            continue

        agent_name = sched['agent_name']
        file_id = sched['file_id']
        agent_display = sched.get('agent_display') or f"{agent_name} ({file_id})"
        job_name = sched['job_name']
        max_runtime = sched.get('max_runtime', '')

        # Add agent header comment
        if file_id != current_agent_file_id:
            if current_agent_file_id is not None:
                lines.append("")  # Blank line between agents
            lines.append(f"# {agent_display}")
            current_agent_file_id = file_id

        # Build command.
        # Use the installed location of this skill (works for OpenSkills global/project installs).
        main_script = Path(__file__).resolve().parent / 'main.py'
        log_dir = repo_root / '.crontab_logs'
        log_file = str(log_dir / f"agent-{sched['agent_id']}-{job_name}.log")

        repo_root_q = shlex.quote(str(repo_root))
        main_script_q = shlex.quote(str(main_script))
        log_dir_q = shlex.quote(str(log_dir))
        log_file_q = shlex.quote(log_file)
        file_id_q = shlex.quote(str(file_id))
        job_name_q = shlex.quote(str(job_name))

        cmd_parts = [
            f"cd {repo_root_q}",
            f"mkdir -p {log_dir_q}",
            f"python3 {main_script_q} schedule run {file_id_q} --job {job_name_q}",
        ]

        if max_runtime:
            cmd_parts[-1] += f" --timeout {max_runtime}"

        cmd = " && ".join(cmd_parts)
        cmd += f" >> {log_file_q} 2>&1"

        # Add crontab entry
        lines.append(f"# {job_name}")
        lines.append(f"{cron} {cmd}")

    # Add heartbeats (use a different comment style to distinguish)
    for hb in heartbeats:
        # Skip if heartbeat is disabled
        if not hb.get('enabled', True):
            continue

        # Skip if agent is disabled
        agent_config = resolve_agent(hb['file_id'])
        if agent_config and not agent_config.get('enabled', True):
            continue

        cron = hb.get('cron', '')
        if not cron:
            continue

        agent_name = hb['agent_name']
        file_id = hb['file_id']
        agent_display = hb.get('agent_display') or f"{agent_name} ({file_id})"
        max_runtime = hb.get('max_runtime', '')

        # Add agent header comment if not already added
        if file_id != current_agent_file_id:
            if current_agent_file_id is not None:
                lines.append("")  # Blank line between agents
            lines.append(f"# {agent_display}")
            current_agent_file_id = file_id

        # Build command for heartbeat
        main_script = Path(__file__).resolve().parent / 'main.py'
        log_dir = repo_root / '.crontab_logs'
        log_file = str(log_dir / f"agent-{hb['agent_id']}-heartbeat.log")

        repo_root_q = shlex.quote(str(repo_root))
        main_script_q = shlex.quote(str(main_script))
        log_dir_q = shlex.quote(str(log_dir))
        log_file_q = shlex.quote(log_file)
        file_id_q = shlex.quote(str(file_id))

        cmd_parts = [
            f"cd {repo_root_q}",
            f"mkdir -p {log_dir_q}",
            f"python3 {main_script_q} start {file_id_q} --restore",
            f"python3 {main_script_q} heartbeat run {file_id_q}",
        ]

        if max_runtime:
            cmd_parts[-1] += f" --timeout {max_runtime}"

        cmd = " && ".join(cmd_parts)
        cmd += f" >> {log_file_q} 2>&1"

        # Add crontab entry (heartbeat marked with [HB])
        lines.append(f"# heartbeat [HB]")
        lines.append(f"{cron} {cmd}")

    lines.append(CRONTAB_END_MARKER)

    return '\n'.join(lines)


def sync_crontab(dry_run: bool = False) -> dict:
    """
    Sync agent schedules to crontab.

    Args:
        dry_run: If True, only show what would be done

    Returns:
        Dict with 'success', 'added', 'removed', 'content'
    """
    current = get_current_crontab()
    cleaned = remove_agent_manager_section(current)
    new_section = generate_crontab_entries()

    # Build new crontab
    if cleaned and new_section:
        new_crontab = cleaned + '\n\n' + new_section + '\n'
    elif new_section:
        new_crontab = new_section + '\n'
    else:
        new_crontab = cleaned + '\n' if cleaned else ""

    # Count cron entries within our managed section.
    old_section = _get_agent_manager_section(current)
    old_entries = _count_cron_entries(old_section)
    new_entries = _count_cron_entries(new_section)

    result = {
        'success': True,
        'entries': new_entries,
        'previous_entries': old_entries,
        'added': max(new_entries - old_entries, 0),
        'removed': max(old_entries - new_entries, 0),
        'content': new_section,
        'dry_run': dry_run,
    }

    if not dry_run:
        result['success'] = set_crontab(new_crontab)

    return result


def list_schedules_formatted() -> str:
    """Get formatted list of all schedules for display."""
    schedules = list_all_schedules()

    if not schedules:
        return "No scheduled jobs configured."

    lines = ["📅 Scheduled Jobs:", ""]

    current_agent_file_id = None
    for sched in schedules:
        agent_name = sched['agent_name']
        file_id = sched['file_id']
        agent_display = sched.get('agent_display') or f"{agent_name} ({file_id})"

        if file_id != current_agent_file_id:
            if current_agent_file_id is not None:
                lines.append("")
            lines.append(f"{agent_display}:")
            current_agent_file_id = file_id

        enabled = sched.get('enabled', True)
        status = "✓" if enabled else "✗"
        job_name = sched['job_name']
        cron = sched.get('cron', 'N/A')
        max_runtime = sched.get('max_runtime', '')
        runtime_str = f"({max_runtime})" if max_runtime else ""

        lines.append(f"  {status} {job_name:20} {cron:20} {runtime_str}")

    return '\n'.join(lines)


def list_heartbeats_formatted() -> str:
    """Get formatted list of all heartbeats for display."""
    heartbeats = list_all_heartbeats()

    if not heartbeats:
        return "No heartbeat jobs configured."

    lines = ["💓 Heartbeats:", ""]

    current_agent_file_id = None
    for hb in heartbeats:
        agent_name = hb['agent_name']
        file_id = hb['file_id']
        agent_display = hb.get('agent_display') or f"{agent_name} ({file_id})"

        if file_id != current_agent_file_id:
            if current_agent_file_id is not None:
                lines.append("")
            lines.append(f"{agent_display}:")
            current_agent_file_id = file_id

        enabled = hb.get('enabled', True)
        status = "✓" if enabled else "✗"
        cron = hb.get('cron', 'N/A')
        max_runtime = hb.get('max_runtime', '')
        session_mode = str(hb.get('session_mode', 'restore') or 'restore').strip().lower()
        heartbeat_mode = str(hb.get('mode', 'normal') or 'normal').strip().lower()
        details = []
        if max_runtime:
            details.append(max_runtime)
        details.append(f"session:{session_mode}")
        if heartbeat_mode != 'normal':
            details.append(f"heartbeat:{heartbeat_mode}")

        schedule = hb.get('schedule')
        if schedule:
            from services.work_schedule import format_schedule_summary
            sched_summary = format_schedule_summary(schedule)
            if sched_summary:
                details.append(f"sched:{sched_summary}")

        dream = hb.get('dream')
        if isinstance(dream, dict) and dream.get('enabled', False):
            from services.dream_window import normalize_dream_fixed_windows
            fixed_windows = normalize_dream_fixed_windows(dream)
            if fixed_windows:
                details.append(f"dream:{len(fixed_windows)}fixed")

        runtime_str = f"({' '.join(details)})" if details else ""

        lines.append(f"  {status} heartbeat           {cron:20} {runtime_str}")

    return '\n'.join(lines)
