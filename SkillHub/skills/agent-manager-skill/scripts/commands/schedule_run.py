from __future__ import annotations
import argparse
import time
from pathlib import Path
from typing import Any, Callable, Optional


def _resolve_schedule_task_path(schedule: dict, repo_root: Path, *, expand_env_vars: Callable[[str], str]) -> Optional[Path]:
    if str(schedule.get('task') or '').strip():
        return None

    raw_task_file = str(schedule.get('task_file') or '').strip()
    if not raw_task_file:
        return None

    expanded = expand_env_vars(raw_task_file)
    path = Path(expanded)
    if not path.is_absolute():
        path = repo_root / path
    if path.exists():
        return path
    return None


def _decide_runtime_action(
    *,
    state: str,
    elapsed: Any,
    timeout_seconds: Optional[int],
    reason: str,
) -> tuple[str, str]:
    if state == 'blocked':
        return 'skip', 'blocked'

    if state == 'error':
        return 'restart', f"error:{reason}"

    if state == 'stuck':
        restart_threshold = timeout_seconds if timeout_seconds else 900
        if isinstance(elapsed, int) and elapsed >= restart_threshold:
            return 'restart', f"stuck>{restart_threshold}s"
        return 'skip', 'stuck_below_threshold'

    if state == 'busy':
        if timeout_seconds and isinstance(elapsed, int) and elapsed >= timeout_seconds:
            return 'restart', f"busy>{timeout_seconds}s"
        return 'skip', 'busy'

    return 'continue', ''


def _print_runtime_skip_message(skip_reason: str) -> None:
    if skip_reason == 'blocked':
        print("⏭️  Agent is blocked, skipping scheduled task")
        print("   Will retry on next cron execution")
        return

    if skip_reason == 'stuck_below_threshold':
        print("⏭️  Agent appears stuck but below restart threshold; skipping scheduled task")
        print("   Will retry on next cron execution")
        return

    if skip_reason == 'busy':
        print("⏭️  Agent is busy, skipping scheduled task")
        print("   Will retry on next cron execution")


def _build_task_message_for_provider(
    *,
    provider_key: str,
    task: str,
    schedule_task_path: Optional[Path],
    repo_root: Path,
    agent_id: str,
    job_name: str,
    deps: Any,
) -> str:
    if provider_key != 'codex':
        return task

    if schedule_task_path is not None:
        return f"Run scheduled job '{job_name}'. Read and follow instructions from file: {schedule_task_path}"

    if deps._should_use_codex_file_pointer(task):
        task_file = deps.write_scheduled_task_file(repo_root, agent_id, job_name, task)
        return f"Run scheduled job '{job_name}'. Read and follow instructions from file: {task_file}"

    return task


def cmd_schedule_run(args, *, deps: Any, start_handler: Callable):
    """Run a scheduled job for an agent."""
    if not deps.check_tmux():
        print("❌ tmux is not installed")
        return 1

    schedule = deps.get_agent_schedule(args.agent, args.job)
    if not schedule:
        print(f"❌ Schedule '{args.job}' not found for agent '{args.agent}'")
        return 1

    agent_config = schedule['_agent_config']
    agent_name = agent_config['name']
    agent_id = deps.get_agent_id(agent_config)

    if not agent_config.get('enabled', True):
        agent_file_id = agent_config.get('file_id', args.agent)
        agent_file_path = agent_config.get('_file_path', f'agents/{agent_file_id}.md')
        print(f"⏭️  Agent '{agent_name}' is disabled - skipping scheduled job '{args.job}'")
        print(f"   Config: {agent_file_path}")
        return 0

    if not schedule.get('enabled', True):
        print(f"⏭️  Schedule '{args.job}' is disabled for agent '{agent_name}'")
        return 0

    repo_root = deps.get_repo_root()

    removed = deps.cleanup_old_logs(repo_root, days=7)
    if removed > 0:
        print(f"   🗑️  Cleaned up {removed} old log file(s)")

    task = deps.get_schedule_task(schedule, repo_root)
    if not task:
        print(f"❌ No task content for schedule '{args.job}'")
        return 1

    schedule_task_path = _resolve_schedule_task_path(
        schedule,
        repo_root,
        expand_env_vars=deps.expand_env_vars,
    )

    print(f"🚀 Running scheduled job: {agent_name}/{args.job}")
    print(f"   Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    timeout_seconds = None
    timeout_str = args.timeout or schedule.get('max_runtime', '')
    if timeout_str:
        timeout_seconds = deps.parse_duration(timeout_str)
        if timeout_seconds:
            print(f"   Max runtime: {timeout_str}")

    was_started = False
    if not deps.session_exists(agent_id):
        print("   Starting agent...")

        start_args = argparse.Namespace(
            agent=args.agent,
            working_dir=None,
            restore=False,
        )

        if start_handler(start_args) != 0:
            print("❌ Failed to start agent")
            return 1

        was_started = True
        time.sleep(2)

    launcher = deps.resolve_launcher_command(agent_config.get('launcher', ''))
    runtime = deps.get_agent_runtime_state(agent_id, launcher=launcher)
    state = str(runtime.get('state', 'unknown'))
    elapsed = runtime.get('elapsed_seconds')
    runtime_reason = str(runtime.get('reason', 'unknown'))
    did_restart = False

    def _restart_agent(restart_reason: str) -> bool:
        nonlocal did_restart
        print(f"♻️  Restarting agent (reason: {restart_reason})")
        deps.stop_session(agent_id)
        time.sleep(1)
        restart_args = argparse.Namespace(agent=args.agent, working_dir=None)
        if start_handler(restart_args) != 0:
            print("❌ Failed to restart agent")
            return False
        time.sleep(2)
        did_restart = True
        return True

    runtime_action, runtime_action_reason = _decide_runtime_action(
        state=state,
        elapsed=elapsed,
        timeout_seconds=timeout_seconds,
        reason=runtime_reason,
    )

    if runtime_action == 'skip':
        _print_runtime_skip_message(runtime_action_reason)
        return 0

    if runtime_action == 'restart':
        if not _restart_agent(runtime_action_reason):
            return 1

    clear_context = bool(schedule.get('clear_context', False))
    if clear_context and not was_started and not did_restart:
        runtime_after = deps.get_agent_runtime_state(agent_id, launcher=launcher)
        state_after = str(runtime_after.get('state', 'unknown'))
        if state_after == 'idle':
            if not _restart_agent('clear_context'):
                return 1

    if not was_started and not did_restart:
        idle_wait_seconds = 5
        deadline = time.time() + idle_wait_seconds
        while time.time() < deadline:
            runtime_check = deps.get_agent_runtime_state(agent_id, launcher=launcher)
            if str(runtime_check.get('state', 'unknown')) == 'idle':
                break
            time.sleep(0.5)

    provider_key = deps.get_provider_key(launcher)
    task_message = _build_task_message_for_provider(
        provider_key=provider_key,
        task=task,
        schedule_task_path=schedule_task_path,
        repo_root=repo_root,
        agent_id=agent_id,
        job_name=args.job,
        deps=deps,
    )

    is_codex = provider_key == 'codex'
    if not deps.send_keys(
        agent_id,
        task_message,
        send_enter=True,
        clear_input=is_codex,
        escape_first=is_codex,
        enter_via_key=is_codex,
    ):
        print("❌ Failed to send task to agent")
        return 1

    print(f"✅ Task sent to {agent_name}")

    wait_seconds = timeout_seconds if timeout_seconds else 600
    if wait_seconds and wait_seconds > 0:
        start_time = time.time()
        last_state: Optional[str] = None
        poll_seconds = 2

        start_deadline = min(30, int(wait_seconds))
        while (time.time() - start_time) < start_deadline:
            runtime = deps.get_agent_runtime_state(agent_id, launcher=launcher)
            last_state = str(runtime.get('state', 'unknown'))
            if last_state != 'idle':
                break
            time.sleep(1)

        print(f"   Waiting for completion (up to {int(wait_seconds)}s)...")
        while (time.time() - start_time) < wait_seconds:
            runtime = deps.get_agent_runtime_state(agent_id, launcher=launcher)
            last_state = str(runtime.get('state', 'unknown'))

            if last_state == 'idle':
                break

            if last_state in ('blocked', 'error', 'stuck'):
                break

            time.sleep(poll_seconds)

        time.sleep(1)
        tail = deps.capture_output(agent_id, lines=200)
        if tail:
            print("----- Agent Output (tail) -----")
            print(tail.rstrip())
            print("----- End Agent Output -----")
        else:
            print("⚠️  Could not capture agent output")

        if last_state and last_state != 'idle':
            print(f"⚠️  Agent state after wait: {last_state}")

    if timeout_seconds and was_started:
        print(f"   Will auto-stop after {timeout_str}")

    return 0
