# Public Google Drive

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Public Google Drive is an agent skill that lets LLM coding agents create and edit Google Docs and Sheets hosted on Memyard — no Google sign-in required. Documents are viewable at shareable links; registration is automatic on first use.

## Installation

Copy the repo into your agent's skills folder, then restart (or start a new session).

| Agent | Command |
|-------|--------|
| **Claude Code** | `git clone https://github.com/zagmoai/public-google-drive.git ~/.claude/skills/public-google-drive` |
| **Cursor** | `git clone https://github.com/zagmoai/public-google-drive.git ~/.cursor/skills/public-google-drive` |
| **Codex** | `git clone https://github.com/zagmoai/public-google-drive.git ~/.codex/skills/public-google-drive` |
| **OpenClaw** | `git clone https://github.com/zagmoai/public-google-drive.git ~/.openclaw/workspace/skills/public-google-drive` |

## What you can do

- **Create** new Google Docs or Sheets in Memyard's workspace.
- **Append or insert** text into docs you created, or **append rows** to sheets you created.
- **View** your documents at a public link (e.g. `https://app.memyard.com/share/<id>`). Anyone with the link can view; only you (your agent) can edit.
- **List** and **get metadata** for your own documents (no plan needed).

Everything lives in Memyard's Google Workspace, not in a personal Drive. You never sign in with a Google account.

## Get started

**You don't need to do anything special.** The first time you create or edit a document through Public Google Drive, the tool will register you automatically and store credentials in `<HOME>/.memyard/agent_config.json` (where `<HOME>` is `$HOME` on macOS/Linux or `%USERPROFILE%` on Windows). After that, it reuses the same credentials so you can keep creating and editing. There is no separate "sign up" step and no URLs or keys to copy.

## How writing works: plan then execute

For **creating** or **updating** a doc or sheet, you use two steps. This lets the server check scope, size, and content before any write happens.

1. **Plan (propose)**
   Tell the server what you want to do: create a doc or sheet, or append/insert into an existing one. Include a short **content summary** (e.g. "Meeting notes and action items"). You don't send the full content yet.

2. **Server response**
   - **Approved:** You get a **plan ID** and a short time window (e.g. 10 minutes). You also get **constraints** (e.g. max characters or rows) so you know the limits for your payload.
   - **Rejected:** You get **reasons** (e.g. content policy) and optional **adjusted constraints**. Don't call execute; fix the proposal or content and try plan again if appropriate.

3. **Execute (do the write)**
   Send the **plan ID** plus the actual **payload** (title, content, rows, etc.). The server performs the write and returns the result (e.g. resource ID, view URL). Each plan ID works **once**; for another write, get a new plan.

So: **propose → get approved or rejected → if approved, send content once**.
Full request/response shapes and examples are in **[SKILL.md](SKILL.md)**.

## When something goes wrong

- **Plan rejected**
  You'll see `rejected_plan` with `reasons`. Don't call execute. Change your summary or title and try plan again, or skip the write.

- **"Plan expired or invalid" (400)**
  The plan ID is no longer valid (used already or timed out). Request a new plan and call execute within the time window.

- **Rate limited (429)**
  You've hit a limit (registrations per IP, or creates/writes per agent per hour). The response includes when to retry. Use the same agent key and try again later.

- **Size limits**
  The approved plan's **constraints** tell you the max characters (docs) or rows (sheets) per request. Stay under those when building your execute payload.

## Documentation

- **[SKILL.md](SKILL.md)** — Full API reference, plan/execute flow, and curl examples.

## License

MIT. See [LICENSE](LICENSE).
