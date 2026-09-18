---
name: security-guide
description: OpenClaw 安全部署指南 / Security deployment guide — help users secure their OpenClaw installation
user-invocable: true
disable-model-invocation: false
---

# ShellWard Security Deployment Guide / 安全部署指南

When the user invokes this skill, provide a complete security deployment checklist based on the following best practices. Check the current system state using available tools and give actionable recommendations.

## Security Checklist

### 1. Network Control / 网络控制
- Check if OpenClaw gateway port (19000/19001) is exposed to public network
- Recommend binding to 127.0.0.1 or using a reverse proxy with authentication
- Suggest firewall rules: `ufw allow from 127.0.0.1 to any port 19000`
- For cloud servers: check security group rules

### 2. Container Isolation / 容器隔离
- Recommend running OpenClaw in Docker with restricted capabilities:
  ```
  docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE \
    --read-only --tmpfs /tmp \
    -u 1000:1000 \
    openclaw
  ```
- Suggest resource limits: `--memory=2g --cpus=1`
- Mount only necessary directories

### 3. Credential Management / 凭证管理
- Scan for plaintext secrets in .env, .bashrc, environment variables
- Recommend using a secret manager (Vault, doppler, etc.)
- Check file permissions on sensitive files (should be 0600)
- Suggest `chmod 600 ~/.env ~/.ssh/* ~/.aws/credentials`

### 4. Audit Logging / 审计日志
- Verify ShellWard audit log is active at ~/.openclaw/shellward/audit.jsonl
- Show recent security events
- Recommend log rotation and backup strategy
- Suggest sending critical events to external SIEM

### 5. Plugin Security / 插件安全
- List all installed plugins and check for known risks
- Disable auto-update for plugins
- Only install from trusted sources
- Scan plugin code for suspicious patterns

### 6. Patch Management / 补丁管理
- Check current OpenClaw version
- Report known vulnerabilities for current version
- Recommend upgrade path
- Check Node.js version (must be >= 22.12)

## Available Commands
Remind the user about ShellWard's quick commands:
- `/security` — Full security status overview
- `/audit [count] [filter]` — View audit log
- `/harden` — Scan for issues, `/harden fix` to auto-fix
- `/scan-plugins` — Scan plugins for security risks
- `/check-updates` — Check versions and vulnerabilities

## Response Style
- Be concise and actionable
- Use the user's language (detect from their message)
- Prioritize critical issues first
- For each issue, provide the exact command to fix it
- Ask for confirmation before executing destructive operations
