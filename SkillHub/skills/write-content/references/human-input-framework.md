# Technique 17: Human Input Framework -- The Critical Differentiator

## What It Is
A structured system for collecting and integrating human-provided content into AI-assisted articles -- because AI without human input produces high-quality slop. The human's experiences, data, opinions, and case studies are what transform generic AI content into genuinely valuable, ranking-worthy articles.

## Why It Works
Every technique in this research converges on one truth: **AI content that ranks is content that includes things only a human could provide.** Information Gain requires unique data. EEAT requires demonstrated experience. Anti-AI-detection requires genuine opinions and idiosyncratic phrasing. NavBoost requires content that actually satisfies users.

AI alone cannot provide:
- First-party data from your business
- Case studies with real clients, real numbers, real timelines
- Genuine opinions and contrarian perspectives based on experience
- Specific tool interactions, error messages, and unexpected results
- The "what went wrong" stories that build trust

## The Human Input Hierarchy

### Tier 1: Essential (Content won't rank without these)
1. **First-party data**: Numbers from your own business, research, or analysis
2. **Case study details**: Client name (or anonymized), problem, solution, specific results
3. **Genuine opinion**: What the author actually thinks about the topic, including disagreements with conventional wisdom

### Tier 2: High-Value (Significantly improves quality)
4. **Specific experience details**: Tool versions, error messages, unexpected behaviors encountered
5. **Process documentation**: The exact steps the author follows, with reasoning for each
6. **Failure stories**: What was tried and didn't work, and why
7. **Comparisons from actual usage**: "I used tool A and tool B for 3 months each. Here's what I found."

### Tier 3: Enhancing (Adds polish and authenticity)
8. **Analogies and metaphors**: The author's unique way of explaining a concept
9. **Predictions/opinions**: Where the author thinks the industry is heading
10. **Behind-the-scenes context**: Why certain decisions were made, what alternatives were considered
11. **Personal anecdotes**: Brief relevant stories that illustrate points

## Step-by-Step Process

### Step 1: Pre-Writing Interview (5-10 questions)
Before the AI pipeline starts, collect human input via structured questions:

**For blog posts / thought leadership:**
1. "What's YOUR take on [topic]? What do you disagree with that most people believe?"
2. "Can you share a specific example or case study related to [topic]?"
3. "What numbers or data do you have from your own experience?"
4. "What's the most common mistake you see people make with [topic]?"
5. "If you had to give one piece of counterintuitive advice on [topic], what would it be?"

**For how-to guides / tutorials:**
1. "When you do [process], what's the exact sequence of steps?"
2. "What usually goes wrong? What error messages do people see?"
3. "What prerequisite do beginners always forget?"
4. "Is there a shortcut or trick that makes this significantly easier?"
5. "What tools/versions do you use, and does it matter?"

**For product/comparison content:**
1. "Which option do you actually recommend and why?"
2. "What's the biggest hidden drawback that nobody mentions?"
3. "Who should NOT use this product/approach?"
4. "What's changed about this product/market in the last 6 months?"
5. "Can you share specific metrics from your usage?"

### Step 2: Input Integration
6. Map each human input to a specific section of the outline
7. Use direct quotes where the human's phrasing is distinctive
8. Weave data points into arguments (don't dump them in a "data" section)
9. Use case studies as section anchors (start sections with the story)
10. Let opinions drive the article's angle, not just flavor paragraphs

### Step 3: Input Verification
11. If the human provides statistics, verify they're reasonable
12. If the human names tools or products, verify they exist and are current
13. If the human references clients, confirm disclosure is appropriate
14. Flag any claims that need supporting evidence

### Step 4: Quality Gate
15. Before finalizing, check: "What in this article could ONLY come from this specific human?"
16. If the answer is "nothing" or "just the case study in paragraph 7," more human input is needed
17. Target: at least 20% of the article's value should be human-sourced

## The Input Collection Interface (MCP Skill Design)

A well-designed workflow should implement a structured input collection:

```
CONTENT WRITING REQUEST
========================
Topic: [user provides]
Content Type: [user selects from 10 types]
Target Keyword: [user provides]

HUMAN INPUT REQUIRED
========================
DATA: Do you have any data or numbers to include?
   [text input -- first-party data, metrics, percentages]

CASE STUDY: Can you share a specific case study or example?
   [text input -- client story, project outcome, before/after]

OPINION: What's YOUR opinion on this topic? Any disagreements with conventional wisdom?
   [text input -- personal take, contrarian view]

CONTRARIAN: What common advice on this topic do you think is WRONG?
   [text input -- things that don't work, outdated advice]

PROCESS: Any specific tools, processes, or methods you use?
   [text input -- exact steps, tool names, configurations]

FAILURES: What usually goes wrong with this? Any failure stories?
   [text input -- mistakes, unexpected results, lessons learned]

[Optional] Upload voice samples for brand voice matching
[Optional] Paste 2-3 example articles in your style
```

## Tips

- **Audio input is often better than text**: People share more detailed, natural-sounding experiences when speaking vs typing. If possible, accept voice memos and transcribe them.
- **The "why" follow-up**: When the human says "we use tool X," follow up with "why did you choose X over alternatives?" -- the reasoning is the information gain, not the tool name.
- **Anonymization template**: Provide a simple template for case studies that need anonymization: "A [industry] company with [X employees] in [region]..."
- **Capture the messy version**: Raw, unpolished human input often sounds MORE authentic than cleaned-up versions. Preserve the original voice.

## Common Mistakes

1. **Making human input optional**: If the pipeline allows "skip" on all human input fields, users will skip everything -- and the content will be generic
2. **Collecting input after writing**: Human input should shape the OUTLINE and WRITING, not be bolted on as quotes after the fact
3. **Over-processing human input**: Don't AI-rewrite the human's case study. Their natural phrasing is an anti-detection signal.
4. **One input, many articles**: Each article should have UNIQUE human input. Reusing the same case study across 10 articles weakens information gain.
