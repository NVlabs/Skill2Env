# Deploying Filesystem-Based Agent Frameworks with S3 Files and AgentCore

**Applies to**: Runtime, S3 Files, Claude Agent SDK, OpenClaw, Strands Agents

## Core Insight

Modern agent frameworks discover capabilities by reading configuration files from the working directory at startup:

| Framework | Key Config Files | Discovery Mechanism |
|-----------|-----------------|---------------------|
| **Claude Agent SDK** | `CLAUDE.md`, `.claude/skills/*/SKILL.md`, `.claude/commands/*.md`, `.claude/output-styles/*.md` | `cwd` + `setting_sources=["project"]` |
| **OpenClaw** | `.openclaw/`, `.agents/`, `skills/`, `.codex`, `.env` | Gateway working directory |
| **Strands Agents** | Agent code, `requirements.txt`, tool definitions | Python module loading |

Modify a `SKILL.md` → agent gains new capabilities. Update `CLAUDE.md` → agent follows new guidelines. No redeployment.

**S3 Files** mounts an S3 bucket as a shared NFS filesystem. All agent instances see identical configuration files. Update once in S3 → every instance picks it up on the next file access.

## Architecture

```
┌────────────────────────────────────────────────────┐
│  S3 Bucket (agent configuration source of truth)    │
│                                                     │
│  ├── CLAUDE.md                                      │
│  ├── .claude/skills/*/SKILL.md                      │
│  ├── .claude/commands/*.md                          │
│  ├── .openclaw/skills/                              │
│  └── shared-knowledge/                              │
└─────────────┬───────────────────────────────────────┘
              │ S3 Files NFS (auto bidirectional sync)
              ▼
┌─────────────────┐  ┌──────────────────┐  ┌──────────────┐
│ EC2 / EKS / ECS │  │ EC2 / EKS / ECS  │  │ Lambda       │
│ /mnt/s3-config/ │  │ /mnt/s3-config/  │  │ /mnt/s3/     │
│ (Claude Agent)  │  │ (OpenClaw)       │  │ (Strands)    │
└─────────────────┘  └──────────────────┘  └──────────────┘
```

**AgentCore Runtime** microVMs cannot mount S3 Files directly. For AgentCore deployments, pull shared config from S3 via API at session start, or use Session Storage for per-session file persistence.

## Claude Agent SDK Deployment

### With S3 Files (EC2/EKS)

Point `cwd` to the S3 Files mount. The SDK reads `CLAUDE.md`, skills, commands, and output styles transparently:

```python
from claude_agent_sdk import query, ClaudeAgentOptions

S3_MOUNT = "/mnt/s3-config"  # S3 Files mount point

async def handle_request(prompt: str, session_id: str = None):
    options = ClaudeAgentOptions(
        cwd=S3_MOUNT,
        setting_sources=["project"],
        allowed_tools=["Skill", "Read", "Write", "Edit", "Bash", "Glob", "Grep"],
    )
    if session_id:
        options.resume = session_id

    async for message in query(prompt=prompt, options=options):
        if hasattr(message, "result"):
            yield message.result
```

Enable Bedrock model access (no Anthropic API key required):

```bash
export CLAUDE_CODE_USE_BEDROCK=1
# AWS credentials from instance role
```

### Zero-Downtime Skill Updates

Upload a new skill to S3 — all running instances discover it on next invocation without restart:

```bash
aws s3 cp ./api-testing/SKILL.md \
  s3://agent-configs/.claude/skills/api-testing/SKILL.md
```

### On AgentCore Runtime (S3 API Sync)

Pull shared config from S3 to Session Storage at session start:

```python
import boto3, os
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from claude_agent_sdk import query, ClaudeAgentOptions
import asyncio

app = BedrockAgentCoreApp()
s3 = boto3.client("s3")
WORKSPACE = "/mnt/workspace"

def sync_config():
    """Pull shared agent config from S3 to local workspace."""
    for prefix in ["CLAUDE.md", ".claude/skills/", ".claude/commands/"]:
        if "/" not in prefix:
            obj = s3.get_object(Bucket="agent-configs", Key=prefix)
            path = f"{WORKSPACE}/{prefix}"
            with open(path, "w") as f:
                f.write(obj["Body"].read().decode())
        else:
            resp = s3.list_objects_v2(Bucket="agent-configs", Prefix=prefix)
            for item in resp.get("Contents", []):
                local = f"{WORKSPACE}/{item['Key']}"
                os.makedirs(os.path.dirname(local), exist_ok=True)
                obj = s3.get_object(Bucket="agent-configs", Key=item["Key"])
                with open(local, "w") as f:
                    f.write(obj["Body"].read().decode())

@app.entrypoint
def handler(payload):
    sync_config()
    async def run():
        options = ClaudeAgentOptions(
            cwd=WORKSPACE, setting_sources=["project"],
            allowed_tools=["Skill", "Read", "Write", "Bash"],
        )
        result = None
        async for msg in query(prompt=payload["prompt"], options=options):
            if hasattr(msg, "result"):
                result = msg.result
        return result
    return {"response": asyncio.run(run())}
```

## OpenClaw Deployment

### With S3 Files (EKS)

Mount two S3 file systems — shared config (read-only across pods) and per-user workspaces:

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: openclaw
        volumeMounts:
        - name: shared-config
          mountPath: /mnt/config    # Shared skills, prompts, templates
          readOnly: true
        - name: user-data
          mountPath: /mnt/users     # Per-user workspaces
      volumes:
      - name: shared-config
        nfs:
          server: <fs-config>.s3-fs.<region>.amazonaws.com
          path: /
      - name: user-data
        nfs:
          server: <fs-users>.s3-fs.<region>.amazonaws.com
          path: /
```

S3 Files provides automatic bidirectional sync — workspace writes propagate to S3 transparently. Per-user isolation is achieved through path-based separation (`/mnt/users/<user-id>/`).

### On AgentCore Runtime

Use Session Storage (`filesystemConfigurations`) for per-user workspace persistence. The Router maps each user to a stable `runtimeSessionId`, so the same user always resumes from the same filesystem state.

## Strands Agents Deployment

### With S3 Files (EC2/EKS) — Shared Knowledge Base

```python
from strands import Agent, tool
from strands.models import BedrockModel
from strands.session.s3_session_manager import S3SessionManager

KNOWLEDGE = "/mnt/s3-knowledge"  # S3 Files mount

@tool
def search_docs(query: str, directory: str = "") -> str:
    """Search shared reference documents.

    Args:
        query: Search term
        directory: Subdirectory to scope search (e.g., 'policies')
    """
    import subprocess
    path = f"{KNOWLEDGE}/{directory}" if directory else KNOWLEDGE
    result = subprocess.run(
        ["grep", "-rl", query, path, "--include=*.md"],
        capture_output=True, text=True
    )
    return result.stdout or "No matching documents found."

agent = Agent(
    model=BedrockModel(model_id="us.anthropic.claude-sonnet-4-20250514-v1:0"),
    tools=[search_docs],
    session_manager=S3SessionManager(
        session_id="user-123", bucket="agent-sessions", prefix="strands/"
    ),
)
```

### On AgentCore Runtime

Use `S3SessionManager` for conversation persistence and Session Storage for file workspace:

```bash
aws bedrock-agentcore-control create-agent-runtime \
  --agent-runtime-name "strands-agent" \
  --filesystem-configurations '[{"sessionStorage": {"mountPath": "/mnt/workspace"}}]' \
  ...
```

## Decision Matrix

| Factor | S3 Files (EC2/EKS/ECS) | AgentCore + S3 API | AgentCore + Session Storage |
|--------|------------------------|--------------------|-----------------------------|
| **Shared config sync** | Native — update S3 once, all see it | Manual sync code at session start | Not shared (per-session) |
| **Multi-instance sharing** | Native NFS | Not supported (per-microVM) | Not supported (per-session) |
| **Per-user isolation** | Path-based (`/users/<id>/`) | Native (per-microVM) | Native (per-session) |
| **File latency** | Sub-millisecond (small files) | 10-100ms (S3 API) | Sub-millisecond (local) |
| **Ops complexity** | Medium (VPC, mount targets) | Low (fully managed) | Low (fully managed) |
| **Claude Agent SDK** | `cwd` → mount point | Sync to Session Storage | `cwd` → Session Storage |
| **Cost** | S3 + performance storage + access | Runtime + S3 API calls | Included in Runtime |

### Recommended Deployments

| Scenario | Target |
|----------|--------|
| Multi-instance shared skills/config | EC2/EKS + **S3 Files** |
| Serverless per-user agent | **AgentCore Runtime** + Session Storage |
| Claude Agent SDK production service | EC2/EKS + **S3 Files** (shared CLAUDE.md + skills) |
| Large shared knowledge base | EC2/EKS + **S3 Files** (NFS access) |

## S3 Files Setup

```bash
# 1. Create file system
aws s3files create-file-system --bucket <bucket-arn> --role-arn <iam-role-arn> --region <region>

# 2. Create mount target (one per AZ)
aws s3files create-mount-target \
  --file-system-id <fs-id> \
  --subnet-id <subnet> \
  --security-groups <sg>

# 3. Mount on compute
sudo mount -t nfs4 <fs-id>.s3-fs.<region>.amazonaws.com:/ /mnt/s3-config

# 4. Upload agent config
aws s3 sync ./agent-config/ s3://<bucket>/

# 5. Verify
ls /mnt/s3-config/CLAUDE.md
ls /mnt/s3-config/.claude/skills/
```

### IAM Requirements

Compute role needs:
- `s3:GetObject`, `s3:PutObject`, `s3:ListBucket` on the config bucket (for S3 intelligent read routing)
- `s3files:ClientMount`, `s3files:ClientWrite` on the file system (for NFS client access)

### Security

- S3 Files encrypts all data at rest (AWS KMS) and in transit (TLS)
- Restrict NFS access to agent compute via VPC security groups
- For multi-tenant deployments, use separate S3 prefixes per tenant

## Related

- [Runtime Service](../services/runtime/README.md) — Session Storage for AgentCore
- [Memory Service](../services/memory/README.md) — AgentCore Memory for long-term recall
- [Credential Management](credential-management.md) — IAM roles for S3/S3 Files access
- [S3 Files Documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-files.html)
- [Claude Agent SDK — Skills](https://code.claude.com/docs/en/agent-sdk/skills)
- [Claude Agent SDK — CLAUDE.md](https://code.claude.com/docs/en/agent-sdk/modifying-system-prompts)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Strands Session Management](https://strandsagents.com/docs/user-guide/concepts/agents/session-management/)
