"""Agent configuration parser for agent-manager skill.

Supports two agent profile layouts under `agents/`:
1) File-based: `agents/EMP_0001.md`
2) Folder-based: `agents/EMP_0001/AGENTS.md`
"""

from __future__ import annotations
import os
import re
import shlex
from pathlib import Path
from typing import Optional, Dict, Any, List, Iterable, Union

from repo_root import find_repo_root, get_repo_root, get_skill_search_dirs


# =============================================================================
# Stdlib-only YAML Frontmatter Parser
# =============================================================================

class _YAMLParseError(Exception):
    """Raised when YAML parsing fails."""
    pass


def _parse_yaml_value(value: str) -> Any:
    """
    Parse a YAML value string into appropriate Python type.

    Supports:
    - Strings (unquoted or quoted)
    - Booleans: true, false, yes, no (case-insensitive)
    - None/null: ~, null, None (case-insensitive)
    - Integers and floats
    - Lists: [item1, item2]
    - Nested dicts via indentation (handled by _parse_yaml_dict)
    """
    value = value.strip()

    # None/null
    if value.lower() in ('~', 'null', 'none'):
        return None

    # Booleans
    if value.lower() in ('true', 'yes'):
        return True
    if value.lower() in ('false', 'no'):
        return False

    # Empty string
    if not value:
        return ''

    # List syntax: [item1, item2, "quoted item"]
    if value.startswith('[') and value.endswith(']'):
        return _parse_yaml_list(value[1:-1])

    # Try parsing as number
    try:
        if '.' in value:
            return float(value)
        return int(value)
    except ValueError:
        pass

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or \
       (value.startswith("'") and value.endswith("'")):
        return value[1:-1]

    # Return as string
    return value


def _parse_yaml_list(list_str: str) -> List[Any]:
    """Parse a YAML list string into Python list."""
    items = []
    current = []
    in_quotes = False
    quote_char = None

    i = 0
    while i < len(list_str):
        char = list_str[i]

        # Handle quoted strings
        if char in ('"', "'") and (i == 0 or list_str[i-1] != '\\'):
            if not in_quotes:
                in_quotes = True
                quote_char = char
            elif char == quote_char:
                in_quotes = False
                quote_char = None
            current.append(char)
        elif in_quotes:
            current.append(char)
        # Handle list separator
        elif char == ',':
            items.append(''.join(current).strip())
            current = []
        # Handle whitespace (skip between items)
        elif char.isspace() and not current:
            pass
        else:
            current.append(char)

        i += 1

    # Add last item
    if current or items:
        items.append(''.join(current).strip())

    return [_parse_yaml_value(item) for item in items if item]


def _looks_like_mapping_entry(text: str) -> bool:
    """
    Best-effort check whether a list item is a mapping entry (e.g. `name: value`).

    Keeps URL-like values (e.g. `https://...`) as scalars.
    """
    stripped = text.strip()
    if "://" in stripped:
        return False
    return bool(re.match(r'^[A-Za-z_][A-Za-z0-9_-]*\s*:', stripped))


def _parse_yaml_block_list(lines: List[str], parent_indent: int) -> List[Any]:
    """
    Parse YAML block-style lists:

    key:
      - item
      - key: value
        nested: value
    """
    items: List[Any] = []
    i = 0

    while i < len(lines):
        line = lines[i]

        if not line.strip() or line.strip().startswith('#'):
            i += 1
            continue

        stripped = line.lstrip()
        current_indent = len(line) - len(stripped)

        if current_indent <= parent_indent or not stripped.startswith('-'):
            i += 1
            continue

        item_indent = current_indent
        item_value = stripped[1:].strip()  # support "-" and "- value"

        i += 1
        continuation: List[str] = []
        while i < len(lines):
            next_line = lines[i]
            if not next_line.strip():
                continuation.append(next_line)
                i += 1
                continue

            next_stripped = next_line.lstrip()
            next_indent = len(next_line) - len(next_stripped)

            if next_indent == item_indent and next_stripped.startswith('-'):
                break
            if next_indent <= parent_indent:
                break

            continuation.append(next_line)
            i += 1

        if not item_value:
            if continuation:
                parsed = _parse_yaml_dict(continuation, item_indent + 2)
                items.append(parsed if parsed else None)
            else:
                items.append(None)
            continue

        if _looks_like_mapping_entry(item_value):
            first_line = f"{' ' * (item_indent + 2)}{item_value}"
            parsed = _parse_yaml_dict([first_line] + continuation, item_indent + 2)
            items.append(parsed)
            continue

        items.append(_parse_yaml_value(item_value))

    return items


def _parse_yaml_dict(lines: List[str], indent_level: int = 0) -> Dict[str, Any]:
    """
    Parse YAML dict from lines, handling nested structures via indentation.

    Args:
        lines: List of YAML lines (without --- markers)
        indent_level: Current indentation level for nested structures

    Returns:
        Parsed dictionary
    """
    result = {}
    i = 0

    while i < len(lines):
        line = lines[i]

        # Skip empty lines and comments
        if not line.strip() or line.strip().startswith('#'):
            i += 1
            continue

        # Count indentation
        stripped = line.lstrip()
        current_indent = len(line) - len(stripped)

        # End of current dict level (less indented or same level but we're nested)
        if current_indent < indent_level:
            break

        # Check for nested dict (more indented)
        if current_indent > indent_level:
            # Collect all lines at this indentation level
            nested_lines = [lines[i]]
            i += 1
            while i < len(lines):
                next_line = lines[i]
                if not next_line.strip():
                    nested_lines.append(next_line)
                    i += 1
                    continue
                next_indent = len(next_line) - len(next_line.lstrip())
                if next_indent <= indent_level:
                    break
                nested_lines.append(next_line)
                i += 1

            # Parse nested dict and assign to last key
            if result:
                last_key = list(result.keys())[-1]
                first_meaningful = next(
                    (ln.lstrip() for ln in nested_lines if ln.strip() and not ln.strip().startswith('#')),
                    ""
                )
                if first_meaningful.startswith('-'):
                    result[last_key] = _parse_yaml_block_list(nested_lines, indent_level)
                else:
                    result[last_key] = _parse_yaml_dict(nested_lines, current_indent)
            continue

        # Parse key: value pair
        if ':' in stripped:
            key_part, value_part = stripped.split(':', 1)
            key = key_part.strip()
            value_str = value_part.strip()

            if value_str:
                # Inline value
                result[key] = _parse_yaml_value(value_str)
            else:
                # Check if next lines are nested (more indented)
                i += 1
                if i < len(lines):
                    next_line = lines[i]
                    next_indent = len(next_line) - len(next_line.lstrip()) if next_line.strip() else 0

                    if next_indent > indent_level:
                        # Nested dict or block list
                        nested_lines = [next_line]
                        i += 1
                        while i < len(lines):
                            next_line = lines[i]
                            if not next_line.strip():
                                nested_lines.append(next_line)
                                i += 1
                                continue
                            next_indent2 = len(next_line) - len(next_line.lstrip())
                            if next_indent2 <= indent_level:
                                break
                            nested_lines.append(next_line)
                            i += 1

                        first_meaningful = next(
                            (ln.lstrip() for ln in nested_lines if ln.strip() and not ln.strip().startswith('#')),
                            ""
                        )
                        if first_meaningful.startswith('-'):
                            result[key] = _parse_yaml_block_list(nested_lines, current_indent)
                        else:
                            # Parse nested mapping at its own indentation level.
                            result[key] = _parse_yaml_dict(nested_lines, next_indent)
                        continue

                # Empty value
                result[key] = None
        else:
            # Malformed line, skip
            pass

        i += 1

    return result


def _parse_yaml_frontmatter(content: str) -> Dict[str, Any]:
    """
    Parse YAML frontmatter from markdown file content.

    Supports a subset of YAML sufficient for agent config files:
    - String values (quoted or unquoted)
    - Boolean values (true/false, yes/no)
    - None/null values (~, null, None)
    - Integer and float values
    - Lists: [item1, item2, "quoted item"]
    - Nested dicts (for schedules, heartbeat, tmux, etc.)

    Args:
        content: Full file content with YAML frontmatter between --- markers

    Returns:
        Parsed configuration dictionary
    """
    # Extract YAML frontmatter (between --- markers)
    frontmatter_match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if not frontmatter_match:
        return {}

    yaml_content = frontmatter_match.group(1)

    if not yaml_content.strip():
        return {}

    # Split into lines and parse
    lines = yaml_content.split('\n')
    return _parse_yaml_dict(lines, indent_level=0)


AGENT_DIR_PROFILE_FILENAME = "AGENTS.md"
MAIN_AGENT_NAME = "main"
MAIN_AGENT_FILE_ID = "main"
MAIN_AGENT_WORKSPACE_ENV = "AGENT_MANAGER_MAIN_WORKSPACE"
MAIN_AGENT_LAUNCHER_ENV = "AGENT_MANAGER_MAIN_LAUNCHER"
MAIN_AGENT_LAUNCHER_ARGS_ENV = "AGENT_MANAGER_MAIN_LAUNCHER_ARGS"


def _bundled_main_codex_model_file() -> Optional[Path]:
    candidate = Path(__file__).resolve().parents[1] / '.codex' / 'main-codex-model.md'
    if candidate.exists() and candidate.is_file():
        return candidate
    return None


def _is_main_agent_query(name_or_id: str) -> bool:
    return str(name_or_id or '').strip().lower() == MAIN_AGENT_NAME


def _path_is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except Exception:
        return False


def _resolve_workspace_root(repo_root: Path) -> Path:
    for candidate in [repo_root] + list(repo_root.parents):
        projects_dir = candidate / 'projects'
        if projects_dir.is_dir() and _path_is_within(repo_root, projects_dir):
            return candidate
    return repo_root


def _build_main_agent_config(
    *,
    repo_root: Optional[Path] = None,
    env_vars: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    if repo_root is None:
        repo_root = get_repo_root()
    if env_vars is None:
        env_vars = dict(os.environ)

    workspace_override = str(env_vars.get(MAIN_AGENT_WORKSPACE_ENV, '') or '').strip()
    if workspace_override:
        workspace_root = Path(expand_env_vars(workspace_override, env_vars=env_vars))
    else:
        workspace_root = _resolve_workspace_root(repo_root)

    launcher = str(env_vars.get(MAIN_AGENT_LAUNCHER_ENV, 'codex') or '').strip() or 'codex'
    launcher_args_raw = str(env_vars.get(MAIN_AGENT_LAUNCHER_ARGS_ENV, '') or '').strip()
    launcher_args = shlex.split(launcher_args_raw) if launcher_args_raw else []

    base = {
        'name': MAIN_AGENT_NAME,
        'description': 'Reserved main agent (default workspace root routing)',
        'file_id': MAIN_AGENT_FILE_ID,
        'working_directory': str(workspace_root),
        'launcher': launcher,
        'launcher_args': launcher_args,
        'launcher_config': {},
        'skills': [],
        'schedules': [],
        'mcps': {},
        'enabled': True,
        'heartbeat': None,
        'role_definition': '',
        '_reserved_main': True,
    }

    bundled_main_model = _bundled_main_codex_model_file()
    if launcher.lower() == 'codex' and bundled_main_model is not None:
        base['launcher_config'] = {
            'model_instructions_file': str(bundled_main_model),
        }

    # Merge overrides from root AGENTS.md or agents/main.md if present.
    agents_dir = repo_root / 'agents'
    for candidate in [
        repo_root / AGENT_DIR_PROFILE_FILENAME,       # root AGENTS.md
        agents_dir / f'{MAIN_AGENT_NAME}.md',          # agents/main.md
        agents_dir / MAIN_AGENT_NAME / AGENT_DIR_PROFILE_FILENAME,  # agents/main/AGENTS.md
    ]:
        if candidate.exists() and candidate.is_file():
            try:
                override = parse_agent_file(candidate)
                override = expand_config_env_vars(override)
                for key in ('heartbeat', 'schedules', 'skills', 'mcps', 'description', 'role_definition',
                            'launcher', 'launcher_args', 'launcher_config', 'working_directory'):
                    val = override.get(key)
                    if val is not None:
                        base[key] = val
                break  # first match wins
            except Exception:
                continue

    return base


def _file_id_from_profile_path(profile_path: Path) -> str:
    """Derive EMP_* file_id from a profile file path."""
    if profile_path.name == AGENT_DIR_PROFILE_FILENAME:
        return profile_path.parent.name
    return profile_path.stem


def _iter_agent_profile_paths(agents_dir: Path) -> Iterable[Path]:
    """Yield agent profile file paths, preferring folder-based profiles when both exist."""
    profiles_by_file_id: dict[str, Path] = {}

    # Legacy file-based profiles.
    for path in sorted(agents_dir.glob('EMP_*.md')):
        profiles_by_file_id[path.stem] = path

    # Folder-based profiles override legacy file profiles if both exist.
    for path in sorted(agents_dir.glob('EMP_*')):
        if not path.is_dir():
            continue
        candidate = path / AGENT_DIR_PROFILE_FILENAME
        if candidate.exists() and candidate.is_file():
            profiles_by_file_id[path.name] = candidate

    yield from sorted(profiles_by_file_id.values())


def parse_agent_file(agent_path: Path) -> Dict[str, Any]:
    """
    Parse agent file extracting YAML frontmatter and markdown content.

    Args:
        agent_path: Path to agent profile file (e.g., agents/EMP_0001.md or agents/EMP_0001/AGENTS.md)

    Returns:
        Dictionary with keys:
        - name: str
        - description: str
        - working_directory: str
        - launcher: str
        - launcher_args: List[str]
        - skills: List[str] (optional)
        - role_definition: str (markdown content after YAML)

    Raises:
        ValueError: If file format is invalid
    """
    content = agent_path.read_text()

    # Extract YAML frontmatter (between --- markers)
    frontmatter_match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if not frontmatter_match:
        raise ValueError(f"Invalid agent file format: {agent_path}")

    yaml_content = frontmatter_match.group(1)
    markdown_content = frontmatter_match.group(2)

    config = _parse_yaml_frontmatter(content)
    config['role_definition'] = markdown_content.strip()

    # Extract file ID from path (e.g., EMP_0001 from EMP_0001.md; EMP_0001 from EMP_0001/AGENTS.md)
    file_id = _file_id_from_profile_path(agent_path)
    config['file_id'] = file_id

    # Set defaults for optional fields
    config.setdefault('launcher_args', [])
    config.setdefault('skills', [])
    config.setdefault('schedules', [])
    # Optional MCP server configuration (provider-dependent).
    # Expected shape: mapping of server_name -> server_config (dict)
    config.setdefault('mcps', {})
    # Optional provider/launcher-specific startup configuration.
    # Current shape: {'key': value}
    config.setdefault('launcher_config', {})
    config.setdefault('enabled', True)  # Agents are enabled by default
    # Heartbeat configuration (optional dict or None)
    config.setdefault('heartbeat', None)

    return config


def expand_env_vars(value: str, env_vars: Optional[Dict[str, str]] = None) -> str:
    """
    Expand ${VAR_NAME} style environment variables.

    Args:
        value: String possibly containing ${VAR_NAME}
        env_vars: Optional dict of env vars (defaults to os.environ)

    Returns:
        Expanded string with ${VAR_NAME} replaced
    """
    if env_vars is None:
        env_vars = dict(os.environ)

    # Set REPO_ROOT default if not in environment.
    # Use git-based detection so configs work from subdirectories/submodules.
    if 'REPO_ROOT' not in env_vars:
        env_vars['REPO_ROOT'] = str(find_repo_root(Path.cwd()))

    # Replace ${VAR_NAME} patterns
    pattern = re.compile(r'\$\{([^}]+)\}')

    def replacer(match):
        var_name = match.group(1)
        return env_vars.get(var_name, match.group(0))

    return pattern.sub(replacer, value)


def expand_config_env_vars(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively expand env vars in all string values.

    Args:
        config: Configuration dictionary possibly containing ${VAR}

    Returns:
        Configuration with expanded environment variables
    """
    expanded = {}

    for key, value in config.items():
        if isinstance(value, str):
            expanded[key] = expand_env_vars(value)
        elif isinstance(value, list):
            expanded[key] = [
                expand_env_vars(item) if isinstance(item, str) else item
                for item in value
            ]
        elif isinstance(value, dict):
            expanded[key] = expand_config_env_vars(value)
        else:
            expanded[key] = value

    return expanded


def resolve_agent(name_or_id: str, agents_dir: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    """
    Resolve agent name or ID to configuration.

    Args:
        name_or_id: Agent name (e.g., "dev") or file ID (e.g., "EMP_0001")
        agents_dir: Directory containing agent files (default: cwd/agents/)

    Returns:
        Parsed agent configuration, or None if not found
    """
    query = str(name_or_id or '').strip()
    if _is_main_agent_query(query):
        return _build_main_agent_config(repo_root=get_repo_root())

    # Accept direct paths (absolute or relative) for convenience, e.g.:
    #   agents/EMP_0008.md
    #   agents/EMP_0008/AGENTS.md
    #   agents/EMP_0008
    candidate_path = Path(name_or_id)

    # 1) If caller provided an existing path, use it.
    if candidate_path.exists():
        profile_path: Optional[Path] = None
        if candidate_path.is_file() and candidate_path.suffix.lower() == '.md':
            profile_path = candidate_path
        elif candidate_path.is_dir():
            candidate_profile = candidate_path / AGENT_DIR_PROFILE_FILENAME
            if candidate_profile.exists() and candidate_profile.is_file():
                profile_path = candidate_profile

        if profile_path is not None:
            try:
                config = parse_agent_file(profile_path)
                config['_file_path'] = profile_path
                return expand_config_env_vars(config)
            except (ValueError, _YAMLParseError):
                return None

    # 2) If it's a bare filename, try resolving it inside agents_dir.
    if name_or_id.endswith('.md'):
        if agents_dir is None:
            agents_dir = get_repo_root() / 'agents'
        agent_file = agents_dir / candidate_path.name
        if agent_file.exists() and agent_file.is_file():
            try:
                config = parse_agent_file(agent_file)
                config['_file_path'] = agent_file
                return expand_config_env_vars(config)
            except (ValueError, _YAMLParseError):
                return None

    if agents_dir is None:
        agents_dir = get_repo_root() / 'agents'

    if not agents_dir.exists():
        return None

    # Try by name (from profile contents)
    for agent_file in _iter_agent_profile_paths(agents_dir):
        try:
            config = parse_agent_file(agent_file)
            if config.get('name') == name_or_id:
                # Add file path to config
                config['_file_path'] = agent_file
                return expand_config_env_vars(config)
        except (ValueError, _YAMLParseError):
            continue

    # Try by file ID
    agent_file = agents_dir / f"{name_or_id}.md"
    if agent_file.exists() and agent_file.is_file():
        try:
            config = parse_agent_file(agent_file)
            config['_file_path'] = agent_file
            return expand_config_env_vars(config)
        except (ValueError, _YAMLParseError):
            return None

    agent_dir_profile = agents_dir / name_or_id / AGENT_DIR_PROFILE_FILENAME
    if agent_dir_profile.exists() and agent_dir_profile.is_file():
        try:
            config = parse_agent_file(agent_dir_profile)
            config['_file_path'] = agent_dir_profile
            return expand_config_env_vars(config)
        except (ValueError, _YAMLParseError):
            return None

    return None


def list_all_agents(agents_dir: Optional[Path] = None) -> Dict[str, Dict[str, Any]]:
    """
    List all configured agents.

    Args:
        agents_dir: Directory containing agent files (default: cwd/agents/)

    Returns:
        Dict mapping agent file_id (e.g. EMP_0001) to configuration.
        (File IDs are stable and avoid collisions when multiple agents share the same `name`.)
    """
    if agents_dir is None:
        repo_root = get_repo_root()
        agents_dir = repo_root / 'agents'
    else:
        repo_root = agents_dir.parent if agents_dir.name == 'agents' else get_repo_root()

    agents: Dict[str, Dict[str, Any]] = {}

    if agents_dir.exists():
        for agent_file in _iter_agent_profile_paths(agents_dir):
            try:
                config = parse_agent_file(agent_file)
                config['_file_path'] = agent_file
                config = expand_config_env_vars(config)
                file_id = config.get('file_id')
                if file_id:
                    agents[file_id] = config
            except (ValueError, _YAMLParseError):
                continue

    agents.setdefault(MAIN_AGENT_FILE_ID, _build_main_agent_config(repo_root=repo_root))
    return agents


def _dedupe_paths(paths: List[Path]) -> List[Path]:
    seen: set[str] = set()
    deduped: List[Path] = []
    for path in paths:
        key = str(path)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(path)
    return deduped


def _find_skill_file(skill_name: str, roots: List[Path]) -> Optional[Path]:
    for root in roots:
        candidate = root / skill_name / 'SKILL.md'
        if candidate.exists() and candidate.is_file():
            return candidate
    return None


def load_skills(
    config: Dict[str, Any],
    *,
    repo_root: Optional[Path] = None,
    skills_dir: Optional[Path] = None,
) -> str:
    """
    Load skill contents from .agent/skills/ and format as system prompt.

    Args:
        config: Agent configuration (must have 'skills' key)
        skills_dir: Directory containing skills (default: cwd/.agent/skills/)

    Returns:
        Formatted string with all skills as system prompt
    """
    skills = config.get('skills', [])
    if not skills:
        return ""

    if repo_root is None:
        repo_root = get_repo_root()

    search_dirs: List[Path] = []
    if skills_dir is not None:
        search_dirs.append(skills_dir)
    search_dirs.extend(get_skill_search_dirs(repo_root))
    search_dirs = _dedupe_paths(search_dirs)

    skill_contents = []

    for skill_name in skills:
        skill_file = _find_skill_file(skill_name, search_dirs)
        if not skill_file:
            continue
        try:
            content = skill_file.read_text(encoding='utf-8')
            # Extract YAML frontmatter for description
            frontmatter_match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
            if frontmatter_match:
                skill_meta = _parse_yaml_frontmatter(content)
                description = skill_meta.get('description', 'No description')
            else:
                description = 'No description'

            skill_contents.append(f"### {skill_name}\n\n{description}\n")
        except Exception:
            # Skip skills that can't be loaded
            continue

    if not skill_contents:
        return ""

    return "## Available Skills\n\n" + "\n\n".join(skill_contents)


def build_system_prompt(
    config: Dict[str, Any],
    *,
    repo_root: Optional[Path] = None,
    skills_dir: Optional[Path] = None,
) -> str:
    """
    Build complete system prompt from agent role definition and skills.

    Args:
        config: Agent configuration (with 'role_definition' and 'skills' keys)
        skills_dir: Directory containing skills (default: cwd/.agent/skills/)

    Returns:
        Complete system prompt string
    """
    parts = []

    # 1. Agent role definition (from markdown body)
    role_definition = config.get('role_definition', '')
    if role_definition:
        parts.append(f"# {config.get('name', 'Agent').upper()} ROLE\n\n{role_definition}")

    # 2. Skills
    skills_content = load_skills(config, repo_root=repo_root, skills_dir=skills_dir)
    if skills_content:
        parts.append(skills_content)

        parts.append(
            "## Workspace Preflight\n\n"
            "If `openskills` can't find skills when you're working inside a subdirectory or git submodule, "
            "first `cd` to the superproject (repo root) and retry:\n\n"
            "```bash\n"
            "cd \"$(git rev-parse --show-superproject-working-tree 2>/dev/null || git rev-parse --show-toplevel 2>/dev/null)\"\n"
            "```\n"
        )

    # Combine all parts
    if not parts:
        return ""

    return "\n\n---\n\n".join(parts)


def get_launcher_command(config: Dict[str, Any]) -> str:
    """
    Build launcher command from config.

    Args:
        config: Agent configuration with 'launcher' and 'launcher_args'

    Returns:
        Full command string to execute
    """
    launcher = config.get('launcher', '')
    args = config.get('launcher_args', [])

    if args:
        args_str = ' '.join(args)
        return f"{launcher} {args_str}"
    return launcher


def parse_duration(duration_str: str) -> Optional[int]:
    """
    Parse duration string to seconds.

    Args:
        duration_str: Duration like '30m', '2h', '1d'

    Returns:
        Duration in seconds, or None if invalid
    """
    if not duration_str:
        return None

    match = re.match(r'^(\d+)([smhd])$', duration_str.strip().lower())
    if not match:
        return None

    value = int(match.group(1))
    unit = match.group(2)

    multipliers = {
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 86400,
    }

    return value * multipliers.get(unit, 1)


def get_schedule_task(schedule: Dict[str, Any], repo_root: Optional[Path] = None) -> str:
    """
    Get task content from a schedule entry.

    Args:
        schedule: Schedule dict with 'task' or 'task_file'
        repo_root: Repository root for resolving task_file paths

    Returns:
        Task content string
    """
    # Inline task takes priority
    if 'task' in schedule and schedule['task']:
        return schedule['task'].strip()

    # Load from task_file
    task_file = schedule.get('task_file', '')
    if task_file:
        if repo_root is None:
            repo_root = Path.cwd()

        # Expand env vars in path
        task_file = expand_env_vars(task_file)
        task_path = Path(task_file)

        # Handle relative paths
        if not task_path.is_absolute():
            task_path = repo_root / task_path

        if task_path.exists():
            return task_path.read_text().strip()

    return ""


def list_all_schedules(agents_dir: Optional[Path] = None) -> List[Dict[str, Any]]:
    """
    List all scheduled jobs across all agents.

    Args:
        agents_dir: Directory containing agent files

    Returns:
        List of dicts with agent info and schedule details
    """
    all_agents = list_all_agents(agents_dir)
    all_schedules = []

    for file_id, config in all_agents.items():
        schedules = config.get('schedules', [])
        for schedule in schedules:
            agent_name = config.get('name') or file_id
            all_schedules.append({
                'agent_name': agent_name,
                'agent_display': f"{agent_name} ({file_id})",
                'agent_id': config.get('file_id', '').lower().replace('_', '-'),
                'file_id': config.get('file_id', ''),
                'job_name': schedule.get('name', 'unnamed'),
                'cron': schedule.get('cron', ''),
                'max_runtime': schedule.get('max_runtime', ''),
                'enabled': schedule.get('enabled', True),
                'task': schedule.get('task', ''),
                'task_file': schedule.get('task_file', ''),
            })

    return all_schedules


def get_agent_schedule(agent_name: str, job_name: str, agents_dir: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    """
    Get a specific schedule from an agent.

    Args:
        agent_name: Agent name or file ID
        job_name: Schedule job name
        agents_dir: Directory containing agent files

    Returns:
        Schedule dict or None if not found
    """
    config = resolve_agent(agent_name, agents_dir)
    if not config:
        return None

    schedules = config.get('schedules', [])
    for schedule in schedules:
        if schedule.get('name') == job_name:
            return {
                **schedule,
                '_agent_config': config,
            }

    return None


def list_all_heartbeats(agents_dir: Optional[Path] = None) -> List[Dict[str, Any]]:
    """
    List all heartbeat configurations across all agents.

    Args:
        agents_dir: Directory containing agent files

    Returns:
        List of dicts with agent info and heartbeat details
    """
    all_agents = list_all_agents(agents_dir)
    all_heartbeats = []

    for file_id, config in all_agents.items():
        heartbeat = config.get('heartbeat')
        if not heartbeat or not isinstance(heartbeat, dict):
            continue

        agent_name = config.get('name') or file_id
        all_heartbeats.append({
            'agent_name': agent_name,
            'agent_display': f"{agent_name} ({file_id})",
            'agent_id': config.get('file_id', '').lower().replace('_', '-'),
            'file_id': config.get('file_id', ''),
            'cron': heartbeat.get('cron', ''),
            'max_runtime': heartbeat.get('max_runtime', ''),
            'session_mode': heartbeat.get('session_mode', 'restore'),
            'mode': heartbeat.get('mode', 'normal'),
            'enabled': heartbeat.get('enabled', True),
            'schedule': heartbeat.get('schedule'),
            'dream': heartbeat.get('dream'),
        })

    return all_heartbeats
