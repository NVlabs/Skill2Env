# 🪭 Junshi (军师)

**Your personalized research strategist**

*Not just what's new. What's new for you.*

Junshi is a Claude Code skill for researchers. It reads your papers, builds a profile of your methods and interests, tracks new papers from arXiv and the venues you care about, and proposes 3–5 ranked research directions you can actually test.

The product is **Junshi (军师)**. The Claude Code skill name is **`research-junshi`**.

You stay the researcher. Junshi acts like a daily 军师: it connects your past work to fresh literature, looks for gaps, and turns them into concrete ideas with a first experiment and a main risk.

It works across many fields, including machine learning, statistics, economics, biology, physics, robotics, and more.

## 30-second example

Tell Claude Code your situation in plain language:

```text
I work on causal inference and econometrics. My papers are in ~/papers/.
I'm thinking about better ways to handle high-dimensional confounders.
Run research-junshi.
```

Claude reads your papers, builds a profile, searches today's arXiv and recent venue papers, and saves a digest like this:

```
### [Rank 1] Debiased Lasso Meets Synthetic Control
Score: Novelty 4/5 · Feasibility 5/5 · Impact 4/5 → 4.3/5

The pitch: Synthetic control methods break down when the donor pool is large
relative to the pre-treatment window. Your debiased Lasso work already handles
high-dimensional nuisance estimation — applying it to reweight the donor pool
gives a synthetic control estimator that is valid even when p >> T.

Why now: Arkhangelsky et al. (2021) opened the synthetic DiD direction but left
the high-dimensional donor case open. Two AER papers this month circle the same
gap from different angles.

First experiment: Simulate a panel with n=500 donors, T=50 periods, and sparse
true weights. Compare your debiased estimator against standard synthetic control
and SDID on coverage and RMSE. One afternoon of code.

Main risk: The weights may not sum to 1 after debiasing — need a projection step
whose effect on inference is unclear.
```

## What you get

- **Ideas grounded in your own work** — Claude reads your papers first, so ideas connect to your methods, open problems, and research taste
- **Daily literature coverage** — arXiv + venue papers (NeurIPS, ACL, Nature, ICRA, or whatever you care about), filtered to what actually matters for your problem
- **Bold ideas, not safe summaries** — 军师 mode pushes for cross-pollinated, gap-exploiting directions; each idea comes with a first experiment and main risk
- **A ranked digest you can act on** — saved to `~/.claude/research-junshi/digests/` every morning

## Installation

```bash
git clone https://github.com/junshi-research/research-junshi.git ~/.claude/skills/research-junshi
```

Then reload plugins in Claude Code:

```
/reload-plugins
```

Also install `poppler` for PDF reading (if you haven't already):

```bash
brew install poppler        # macOS
apt install poppler-utils   # Linux
```

## Usage

### First run

Just describe your situation naturally:

```
I'm researching causal inference in economics. My papers are in ~/papers/.
I'm thinking about better ways to handle high-dimensional confounders.
Run research-junshi.
```

Claude will ask a few follow-up questions (which venues to watch, etc.) and make smart guesses if you skip anything. It reads your papers, builds a profile, and generates today's digest.

### Daily digest

```
Give me today's research digest.
```

### Set up automatic daily runs (fully automatic, no Claude Code session needed)

```bash
bash ~/.claude/skills/research-junshi/setup_automation.sh
```

The script asks for your preferred time (e.g. `08:00`) and sets up a cron job. Digests appear in `~/.claude/research-junshi/digests/` each morning with no action required.

> **Note**: Automated runs use `--dangerously-skip-permissions` for headless execution — this bypasses all permission prompts with no technical enforcement of scope. The prompt is designed to only read papers, write digest files, and search the web, but nothing prevents Claude from taking other actions. Review the script before enabling automation, and use only in a trusted local environment.

### Update your profile

```
Update my Junshi profile. I've shifted focus to [new direction].
```

## Output

Each digest is saved to `~/.claude/research-junshi/digests/`:

- **Today's landscape** — what the field is doing right now
- **Top papers** — summaries of the most relevant arXiv + venue papers
- **Ranked ideas** — top 3–5 bold directions with scores, pitch, first experiment, and main risk
- **Raw ideas** — unfiltered brainstorm

## Supported Fields

The skill adapts to any research area. Built-in venue knowledge covers:

| Field | Example venues |
|---|---|
| Machine Learning | NeurIPS, ICML, ICLR, JMLR |
| Computer Vision | CVPR, ICCV, ECCV |
| NLP | ACL, EMNLP, NAACL |
| Robotics | ICRA, RSS, CoRL |
| Biology | Nature, Science, Cell, Bioinformatics |
| Physics | PRL, PRX, Nature Physics |
| Economics / Statistics | Econometrica, AER, Annals of Statistics |
| Systems / HCI | SOSP, OSDI, SIGCHI, UIST |

If your field or venue isn't listed, just tell Claude — it will adapt.

## Files created by the skill

```
~/.claude/research-junshi/
├── profile.md                  ← your research profile (updated on "update my profile")
├── config.md                   ← field, venues, arXiv categories, papers folder
└── digests/
    ├── 2026-03-15.md
    ├── 2026-03-16.md
    ├── ...
    └── cron-junshi.log         ← cron run log (created by setup_automation.sh)
```

These are personal — they are not part of this repo and should not be committed.

## Customization

Edit `SKILL.md` to adjust:
- Idea scoring weights (default: novelty 0.4, feasibility 0.3, impact 0.3)
- Number of ideas per digest
- Digest format and sections
- How aggressively the skill suggests bold vs. conservative ideas

---

Built with the [skill-creator](https://github.com/anthropics/claude-code) plugin for Claude Code.
If you find this useful, feel free to open issues or PRs.
