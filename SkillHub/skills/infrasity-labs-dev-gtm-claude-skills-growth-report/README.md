# Growth Report

Generates a comprehensive 3-month SEO performance HTML report for any domain using live DataForSEO data. Covers traffic trends, keyword rankings, top content clusters, competitive positioning, strategic priorities, and an executive summary — delivered as a dark-theme executive-ready HTML file.

---

## What this skill does

You provide a target domain and a list of competitors. The skill pulls live data from DataForSEO — baseline vs current traffic, keyword ranking distributions, top content pages, and historical trend data for every competitor — then compiles it into a polished HTML report you can share directly with leadership or clients.

Every number in the report comes from a real API response. No placeholder text, no estimates.

Built for:
- **SEO teams** delivering monthly or quarterly performance briefings
- **Agencies** producing client-facing SEO reports at scale
- **Developer marketing and growth teams** tracking competitive SEO positioning

---

## Installation

### Claude Code (Recommended)

Clone the repo — the skill activates automatically when you open it in Claude Code:

```bash
git clone https://github.com/Infrasity-Labs/dev-gtm-claude-skills.git
cd dev-gtm-claude-skills
claude
```

Then trigger it with:

```
/dev-gtm growth-report firefly.ai spacelift.io env0.com terraform.io
```

### Claude Web (Free / Pro)

1. Go to **[Settings → Capabilities](https://claude.ai/settings/capabilities)** and enable **Code execution and file creation**
2. Go to **[Customize → Skills](https://claude.ai/customize/skills)**
3. Click **+** → **Create skill** → **Upload a skill**
4. Zip this skill folder and upload it:

```bash
cd dev-gtm-claude-skills/skills
zip -r growth-report.zip growth-report/
```

Upload `growth-report.zip` and toggle it on.

---

## DataForSEO Setup (Required)

This skill requires a [DataForSEO](https://dataforseo.com) account. All traffic, keyword, and competitive data is fetched live from their API.

### Claude Code

Open `.claude/settings.json` in the cloned repo and replace the placeholder credentials:

```json
{
  "mcpServers": {
    "dataforseo": {
      "command": "npx",
      "args": ["-y", "@dataforseo/mcp-server"],
      "env": {
        "DATAFORSEO_USERNAME": "your-dataforseo-username",
        "DATAFORSEO_PASSWORD": "your-dataforseo-password"
      }
    }
  }
}
```

### Claude Web (Free / Pro)

Go to **[Settings → Integrations](https://claude.ai/settings/integrations)**, find **DataForSEO**, and connect your account with your API credentials.

---

## How to use

```
Generate SEO report for firefly.ai vs spacelift.io, env0.com, terraform.io
```

```
/dev-gtm growth-report stripe.com braintree.com adyen.com
```

The skill asks for any missing inputs in a single message — target domain, competitors (up to 6), date range, and location. It comes with sensible defaults so you can confirm and proceed immediately.

### Inputs

| Input | Required | Default |
|-------|----------|---------|
| Target domain | ✅ | — |
| Competitor domains | ✅ Min 2, max 6 | — |
| Date range | ⬜ | Last 3 months |
| Location | ⬜ | United States |

---

## What the report covers

**Timeline cards** — traffic, keyword count, and top-3 ranking changes over the date range with delta badges (percentage growth or decline vs baseline).

**Traffic trend bars** — monthly ETV snapshots across the date window, showing the trajectory visually.

**Competitive landscape table** — all domains ranked by current traffic with each competitor's trend badge (growing / stable / declining) derived from real historical data.

**Top content clusters** — the 3 highest-traffic pages on the target domain with their ETV and keyword counts.

**Q2 targets card** — automatically derived traffic, keyword, and top-3 goals based on the current trajectory.

**6 strategic priority cards** — data-driven actions: gap to next competitor, threats from rising competitors, traffic recovery or scale path, content cluster opportunities, keyword coverage recovery, and top-10-to-top-3 conversion.

**Executive summary** — 4 paragraphs written from the data: overall result, content concentration analysis, keyword trend, and Q2 strategy. All numbers are real API values.

---

## Output

An HTML file saved to `/mnt/user-data/outputs/<domain>_seo_report.html`, delivered via `present_files`.

The report is fully self-contained — no external dependencies, no CDN links. Open it in a browser or attach it directly to a Slack message or email.

---

## File structure

```
growth-report/
├── SKILL.md               # Skill instructions Claude follows
├── README.md              # This file
└── references/
    └── html-template.md   # Full HTML/CSS report template with variable map
```
