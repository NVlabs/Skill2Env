from __future__ import annotations
from typing import Any


def _session_label(agent_id: str) -> str:
    return 'main' if str(agent_id).strip().lower() == 'main' else f"agent-{agent_id}"


def cmd_list(args, *, deps: Any):
    """List all agents (configured and running)."""
    list_all_agents = deps.list_all_agents
    list_sessions = deps.list_sessions
    get_agent_id = deps.get_agent_id
    get_session_info = deps.get_session_info

    all_agents = list_all_agents()
    running_sessions = set(list_sessions())

    print("📋 Agents:")
    print()

    if not all_agents:
        print("  No agents configured in agents/")
        return

    for file_id, config in sorted(all_agents.items(), key=lambda item: item[0]):
        agent_name = config.get('name') or file_id
        agent_id = get_agent_id(config)
        is_running = agent_id in running_sessions
        is_enabled = config.get('enabled', True)
        session_label = _session_label(agent_id)

        if args.running and not is_running:
            continue

        if is_running:
            status = "✅ Running"
            session_info = get_session_info(agent_id)
            if session_info:
                print(f"{status} {session_info['session']}({agent_name})")
            else:
                print(f"{status} {session_label}({agent_name})")
        elif not is_enabled:
            status = "⛔ Disabled"
            print(f"{status} {session_label}({agent_name})")
            print(f"   Description: {config.get('description', 'No description')}")
            print(f"   Working Dir: {config.get('working_directory', 'N/A')}")
            print()
            continue
        else:
            status = "⭕ Stopped"
            print(f"{status} {session_label}({agent_name})")

        print(f"   Description: {config.get('description', 'No description')}")
        print(f"   Working Dir: {config.get('working_directory', 'N/A')}")

        skills = config.get('skills', [])
        if skills:
            print(f"   Skills: {', '.join(skills)}")

        print()
