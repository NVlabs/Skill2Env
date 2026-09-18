from __future__ import annotations
from typing import Any


def cmd_doctor(args, *, deps: Any):
    """Run basic environment checks for agent-manager."""
    get_repo_root = deps.get_repo_root
    check_tmux = deps.check_tmux
    list_all_agents = deps.list_all_agents
    get_agent_id = deps.get_agent_id
    resolve_launcher_command = deps.resolve_launcher_command
    Path = deps.Path
    sys = deps.sys
    subprocess = deps.subprocess

    repo_root = get_repo_root()
    agents_dir = repo_root / 'agents'
    skills_dir = repo_root / '.agent' / 'skills'
    claude_dir = repo_root / '.claude'

    problems = 0

    print("🩺 agent-manager doctor")
    print()
    print(f"Repo root: {repo_root}")
    print(f"Python: {sys.version.split()[0]} ({sys.executable})")
    print(f"Platform: {sys.platform}")
    print()

    if check_tmux():
        print("✅ tmux: found")
    else:
        problems += 1
        print("❌ tmux: missing")
        print(f"   Fix: {deps._tmux_install_hint()}")

    if agents_dir.exists() and agents_dir.is_dir():
        agents = list_all_agents(agents_dir)
        print(f"✅ agents/: found ({len(agents)} configured)")
    else:
        problems += 1
        print("❌ agents/: missing")
        print(f"   Expected at: {agents_dir}")

    if skills_dir.exists() and skills_dir.is_dir():
        print("✅ .agent/skills/: found")
    else:
        print("⚠️  .agent/skills/: missing")
        print(f"   Expected at: {skills_dir}")

    if claude_dir.exists() and claude_dir.is_dir():
        print("✅ .claude/: found")
    else:
        print("⚠️  .claude/: missing")
        print(f"   Expected at: {claude_dir}")

    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ crontab: readable")
        else:
            print("⚠️  crontab: not set (or not readable)")
    except FileNotFoundError:
        problems += 1
        print("❌ crontab: command not found")

    if args.deep and agents_dir.exists() and agents_dir.is_dir():
        print()
        print("🔎 Deep checks:")
        agents = list_all_agents(agents_dir)
        for file_id, config in sorted(agents.items(), key=lambda item: item[0]):
            agent_id = get_agent_id(config)
            working_dir = config.get('working_directory')
            launcher = resolve_launcher_command(config.get('launcher', ''))
            enabled = config.get('enabled', True)

            status = "✅" if enabled else "⛔"
            print(f"{status} {file_id} (agent-{agent_id})")
            if working_dir:
                wd_ok = Path(working_dir).exists()
                print(f"   Working dir: {working_dir} ({'ok' if wd_ok else 'missing'})")
                if not wd_ok and enabled:
                    problems += 1
            else:
                print("   Working dir: (not set)")
                if enabled:
                    problems += 1

            if launcher:
                print(f"   Launcher: {launcher}")
            else:
                print("   Launcher: (not set)")

    print()
    if problems:
        print(f"❌ Doctor found {problems} problem(s)")
        return 1
    print("✅ Doctor checks passed")
    return 0
