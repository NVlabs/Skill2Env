# Discourse Analysis and Conversation Analysis

## Discourse Analysis

Discourse analysis is not a single method but a family of approaches that examine how language constructs social reality. The two most influential traditions in social science are Fairclough's Critical Discourse Analysis and Gee's discourse analysis.

### Fairclough's Critical Discourse Analysis (CDA)

Norman Fairclough's CDA examines the relationship between language, power, and ideology through a three-dimensional framework:

**Dimension 1: Text analysis (description)**
- Vocabulary choices (overwording, rewording, ideologically contested terms)
- Grammar (transitivity, modality, agency, nominalization)
- Text structure and cohesion
- Turn-taking and interactional control

**Dimension 2: Discursive practice (interpretation)**
- Production (who created the text, under what institutional conditions)
- Distribution (how the text circulates and to whom)
- Consumption (how audiences interpret and use the text)
- Intertextuality (how the text draws on and transforms other texts)
- Interdiscursivity (how the text mixes different discourses, genres, styles)

**Dimension 3: Social practice (explanation)**
- Situational context (immediate social situation)
- Institutional context (organizational norms and power relations)
- Societal context (broader political, economic, cultural structures)

**Example: CDA analysis of a university policy document**

```
Text: "Students are expected to demonstrate professional behaviors
consistent with the values of the institution."

Text analysis:
- Passive voice ("are expected") obscures who does the expecting
- Nominalization ("behaviors") converts actions into countable objects
- "Professional" is an ideologically loaded term that normalizes
  particular class and cultural norms
- "Values of the institution" presupposes shared values and
  positions the institution as a moral agent

Discursive practice:
- Genre: institutional policy (authoritative, impersonal)
- Intertextuality: draws on corporate/professional discourse,
  displacing educational discourse
- Production: likely written by administrators, not faculty or students

Social practice:
- Reflects neoliberal governance of higher education
- Constructs students as future workers rather than learners
- Power asymmetry: institution defines "professional" without
  student input
```

### Gee's Discourse Analysis

James Paul Gee distinguishes between discourse (language-in-use) and Discourse (with a capital D) -- ways of being in the world that integrate language with action, interaction, values, beliefs, symbols, objects, tools, and places.

**Gee's seven building tasks of language:**

1. **Significance** -- How does this language make certain things significant or insignificant?
2. **Activities** -- What activity is this language enacting?
3. **Identities** -- What identity is the speaker/writer taking on?
4. **Relationships** -- What relationships is this language building or assuming?
5. **Politics** -- What is being treated as normal, appropriate, or valued?
6. **Connections** -- How does this language connect or disconnect things?
7. **Sign systems and knowledge** -- What sign systems (language, images, statistics) are privileged?

**Gee's analytical tools:**

- Situated meaning (context-dependent word meaning)
- Social languages (varieties associated with social groups/activities)
- Figured worlds (taken-for-granted stories or theories)
- Intertextuality (references to other texts)
- Conversations (societal-level debates indexed by the text)

> For a framework selection matrix (including Foucauldian DA, discursive psychology, multimodal CDA, corpus-assisted DA) and a full CDA analytical checklist, see `references/social-science-frameworks.md`.

## Conversation Analysis

Conversation analysis (CA), developed by Harvey Sacks, Emanuel Schegloff, and Gail Jefferson, studies the sequential organization of naturally occurring talk-in-interaction. CA is fundamentally empirical and data-driven -- it examines what participants actually do in conversation rather than imposing external categories.

**Core principles of CA:**

1. **Sequential organization** -- Utterances are understood in relation to what comes before and after
2. **Turn-taking system** -- Participants coordinate who speaks when through recognizable rules
3. **Preference organization** -- Some responses are structurally "preferred" (e.g., acceptance over rejection)
4. **Repair** -- Participants have systematic practices for dealing with troubles in speaking, hearing, or understanding
5. **Recipient design** -- Talk is designed for specific recipients and their knowledge

**Transcription conventions (Jefferson system):**

```
Symbol    Meaning
(0.5)     Pause in seconds
(.)       Micro-pause (less than 0.2 seconds)
=         Latching (no gap between speakers)
[         Start of overlapping talk
]         End of overlapping talk
word      Emphasis (underline)
WORD      Loud speech
.hh       In-breath
hh        Out-breath
wo::rd    Sound stretching
wo-       Cut-off
>word<    Faster speech
<word>    Slower speech
.         Falling intonation
?         Rising intonation
,         Continuing intonation
((nods))  Analyst description
```

**Example: CA analysis of a doctor-patient interaction**

```
01 DOC:  So how are you feeling today.
02       (0.8)
03 PAT:  Well (.) I'm okay I gu:ess.
04 DOC:  Mm hm,
05       (0.3)
06 PAT:  But my knee's been bothering me quite a bi:t.
07 DOC:  Your knee.
08 PAT:  Yeah the left one.=It's been (0.4) kind of
09       sti::ff in the mornings.

Analysis:
- Line 02: The 0.8 second pause before the patient's response
  suggests a dispreferred response is coming
- Line 03: "Well" is a discourse marker that prefigures disagreement
  or qualification. "I guess" hedges the assessment.
- Line 06: "But" introduces the actual reason for the visit,
  delivered as a contrast to "okay"
- Line 07: The doctor's partial repeat ("Your knee.") functions as
  a go-ahead / continuer, inviting elaboration
```

## Quantitative Content Analysis

Quantitative content analysis systematically codes textual, visual, or audio content into categories and analyzes the resulting data statistically. Unlike discourse analysis, it prioritizes reliability and generalizability over interpretive depth.

**Steps in quantitative content analysis:**

1. **Define the research question** -- What content features are you examining and why?
2. **Define the population and sampling frame** -- What is the universe of relevant content?
3. **Select a sample** -- Random, stratified, or purposive sampling of content units
4. **Define units of analysis** -- What gets coded? (article, paragraph, sentence, image, scene)
5. **Develop the coding scheme** -- Create exhaustive, mutually exclusive categories with clear decision rules
6. **Pilot test and train coders** -- Code a sample, discuss disagreements, refine the scheme
7. **Assess intercoder reliability** -- Calculate agreement statistics before proceeding
8. **Code the full sample** -- Apply the scheme systematically
9. **Analyze** -- Descriptive statistics, chi-square tests, logistic regression, etc.
10. **Report** -- Include reliability statistics, codebook, and examples

**Intercoder reliability metrics:**

| Metric | When to Use | Acceptable Threshold |
|--------|------------|---------------------|
| Percent agreement | Never alone (does not account for chance) | N/A |
| Cohen's kappa | Two coders, nominal categories | > 0.80 (good), > 0.67 (acceptable) |
| Krippendorff's alpha | Any number of coders, any measurement level | > 0.80 (good), > 0.667 (acceptable) |
| Scott's pi | Two coders, nominal categories | > 0.80 |
| ICC (intraclass correlation) | Continuous/ordinal ratings | > 0.75 (good) |
