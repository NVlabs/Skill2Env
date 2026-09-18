---
name: alterlab-survey-design
description: "Comprehensive survey and instrument design assistant supporting questionnaire construction, Likert scale design, question types (open/closed/matrix), response bias mitigation, sampling strategies (probability/non-probability), pilot testing, instrument validation (Cronbach's alpha, factor analysis), online survey tools (Qualtrics, REDCap, Google Forms), interview protocol development, focus group facilitation, mixed-mode surveys, and cultural adaptation of instruments. Use when designing a survey or questionnaire, building Likert scales, planning a sampling strategy, pilot testing, validating an instrument (Cronbach's alpha, factor analysis), developing an interview protocol, improving response rates, or working in Qualtrics or REDCap. For analyzing interview/focus-group data use alterlab-qualitative-methods; for qual+quant integration alterlab-mixed-methods; for test selection/power analysis alterlab-statistical-analysis; for IRB/consent alterlab-research-ethics. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read WebFetch WebSearch Bash(python:*)
compatibility: No API key required. Guidance-focused skill; uses WebFetch/WebSearch and optional Python helpers via `uv run python`.
metadata:
  skill-author: AlterLab
  version: "1.0.0"
  last_updated: "2026-03-18"
---

# Survey Design — Survey & Instrument Design Agent

A comprehensive survey and instrument design tool for faculty and researchers. Covers the full lifecycle of survey-based research: from construct definition and item writing through pilot testing, validation, deployment, and analysis of survey data.

## Overview

Survey research is one of the most widely used methods across social sciences, health sciences, education, and business. Despite its apparent simplicity, designing a valid and reliable survey instrument requires systematic attention to construct definition, item wording, response format, sampling, bias mitigation, and psychometric validation.

This skill treats survey design as a scientific process, not an art. Every design decision should be justified and documented.

## When to Use This Skill

This skill should be used when:
- Designing a new survey or questionnaire from scratch
- Adapting an existing instrument for a new population or context
- Writing Likert-scale items or other structured response formats
- Developing interview protocols or focus group guides
- Planning sampling strategies for survey research
- Conducting pilot tests and cognitive interviews
- Validating instruments (reliability and validity analysis)
- Selecting online survey platforms (Qualtrics, REDCap, Google Forms)
- Improving response rates and reducing bias
- Conducting cultural adaptation and translation of instruments
- Teaching research methods courses that include survey design

### Does NOT Trigger

| Scenario | Use Instead |
|----------|-------------|
| Qualitative data analysis (coding, themes, focus group/interview analysis) | `alterlab-qualitative-methods` |
| Integrating qual + quant strands (convergent/sequential designs, joint displays) | `alterlab-mixed-methods` |
| Hypothesis-test selection, assumption checks, power analysis beyond validation | `alterlab-statistical-analysis` |
| Specialized social-science methods (Delphi, Q-methodology, QCA) | `alterlab-social-science-methods` |
| Writing the research paper | `alterlab-paper-writer` |
| Ethics/IRB applications, informed consent for survey research | `alterlab-research-ethics` |

---

## Core Capabilities

### 1. Survey Design Process

**The 10-Step Survey Design Framework:**

```
Step 1:  Define research objectives and constructs
         What do you want to measure? What are your research questions?
              │
Step 2:  Review existing instruments
         Has someone already validated an instrument for your construct?
              │
Step 3:  Define the target population and sampling frame
         Who will you survey? How will you reach them?
              │
Step 4:  Choose survey mode
         Online, paper, phone, in-person, mixed-mode?
              │
Step 5:  Write items and response options
         Craft questions that are clear, unambiguous, and aligned to constructs
              │
Step 6:  Design survey structure and flow
         Organize sections, add skip logic, manage survey length
              │
Step 7:  Expert review
         Subject matter experts and methodologists evaluate the instrument
              │
Step 8:  Cognitive interviews and pilot testing
         Test with a small sample from the target population
              │
Step 9:  Psychometric validation
         Reliability analysis, factor analysis, validity assessment
              │
Step 10: Deploy, monitor, and analyze
         Launch survey, track response rates, clean and analyze data
```

### 2. Construct Definition and Operationalization

Before writing a single item, define what you are measuring. Map each construct to its dimensions, indicators, distinct-but-related constructs, and a nomological network so every item traces back to something specific.

Full **Construct Mapping Template**: see `references/item_writing_and_scales.md`.

### 3. Item Writing

#### Question Types and When to Use Them

| Type | Format | Best For |
|------|--------|----------|
| Closed-ended (single choice) | Radio buttons | Mutually exclusive categories |
| Closed-ended (multiple choice) | Checkboxes | Non-mutually exclusive categories |
| Likert scale | Rating scale | Attitudes, perceptions, frequency |
| Semantic differential | Bipolar scale | Evaluative judgments |
| Ranking | Drag-and-drop or numbered | Forced prioritization |
| Matrix/Grid | Likert items in table | Multiple items with same response scale |
| Open-ended | Text box | Exploratory, rich responses |
| Numeric | Number input | Precise quantities |
| Visual analog scale (VAS) | Slider | Continuous measurement |

#### Likert Scale — Number of Points

| Points | Trade-off | Use When |
|--------|-----------|----------|
| 4-point | Forces a choice (no midpoint) | Avoid social desirability midpoint clustering |
| 5-point | Most common, well-understood; central-tendency bias | Standard attitudinal measurement |
| 6-point | Forced choice with more granularity | Force direction with more options |
| 7-point | Greater discrimination; better for factor analysis | Established psychometric instruments |

**Item-writing essentials — DO:** simple/clear language; one concept per item (no double-barreled); specific time frames; match scale to stem; pilot with the target population; over-generate items. **DO NOT:** leading/loaded language; double negatives; assume knowledge; use absolutes; write overly long items; ask about hypotheticals when you mean actual behavior.

Full question-type examples, Likert labeling schemes, the complete DO / DO NOT rules, and worked before/after item revisions: see `references/item_writing_and_scales.md`.

### 4. Survey Structure and Flow

Organize the instrument as: welcome + consent → screening → main content grouped by construct (easy questions first, sensitive items mid-survey) → demographics at the end → thank-you/debrief. Use skip logic to hide irrelevant questions and route ineligible respondents.

Full **Survey Structure Template** and **Skip Logic Design** examples: see `references/item_writing_and_scales.md`.

### 5. Sampling Strategies

**Probability Sampling** (every member has a known, non-zero chance of selection; generalizable):

| Method | How It Works | Trade-off |
|--------|-------------|-----------|
| Simple random | Select randomly from complete list | Unbiased, but needs a complete sampling frame |
| Systematic | Select every kth element | Easy, but periodicity risk if list has a pattern |
| Stratified | Random sample within population strata | Ensures subgroup representation; needs population knowledge |
| Cluster | Randomly select clusters, then sample within | Practical without individual list; higher sampling error |
| Multi-stage | Combine methods (cluster then stratified) | Flexible for large populations; complex to analyze |

**Non-Probability Sampling** (no representativeness guarantee):

| Method | How It Works | Trade-off |
|--------|-------------|-----------|
| Convenience | Recruit whoever is available | Fast/cheap, but strong bias |
| Purposive | Select on specific criteria | Targets relevant subgroups; researcher bias |
| Snowball | Participants recruit others | Reaches hidden populations; biased toward the connected |
| Quota | Convenience sample within subgroup quotas | Ensures diversity; not truly random within quotas |

Size the sample with the proportion formula `n = (Z² × p × (1-p)) / E²` for descriptive surveys (adjusting for finite population and expected response rate), or a power analysis for comparative surveys. Worked sample-size formulas and the Python two-group power-analysis helper: see `references/sampling_and_power.md`.

### 6. Response Bias Mitigation

| Bias Type | Definition | Mitigation Strategies |
|-----------|-----------|----------------------|
| Social desirability | Respondents answer in ways they believe are socially acceptable | Anonymous data collection; indirect questioning; validated social desirability scales (e.g., Marlowe-Crowne) |
| Acquiescence | Tendency to agree with statements regardless of content | Mix positively and negatively worded items; use forced-choice formats |
| Central tendency | Tendency to select middle response options | Use even-point scales (no midpoint); provide behavioral anchors |
| Extreme responding | Tendency to select extreme endpoints | Use more response options (7-point); provide clear anchor descriptions |
| Order effects | Earlier questions influence responses to later questions | Randomize item order within sections; counterbalance across respondents |
| Nonresponse bias | Systematic differences between responders and non-responders | Follow-up reminders; analyze early vs. late responders; compare demographics to population |
| Recall bias | Inaccurate recall of past events | Use shorter recall periods; provide memory aids; use event-specific prompts |
| Common method bias | Inflated correlations due to same measurement method | Use different measurement methods; temporal separation; marker variables |

### 7. Pilot Testing

Run a **three-phase pilot** before full deployment: (1) expert review for content/face validity (CVI thresholds: Item-CVI ≥ 0.78, Scale-CVI/Ave ≥ 0.90); (2) cognitive interviews (n = 5-10) using think-aloud and probing questions; (3) a quantitative pilot (n = 30-50) assessing completion, missing data, distributions, internal consistency, and item-total correlations.

Full phase-by-phase protocol with probe scripts and the quantitative-pilot checklist: see `references/pilot_and_validation.md`.

### 8. Instrument Validation

Assess **reliability** (Cronbach's alpha per subscale, corrected item-total correlations — flag items < 0.30) and **validity** across the evidence types below. Use exploratory factor analysis (Bartlett's test, KMO, eigenvalues, rotated loadings) to check internal structure.

| Type | Question | Method |
|------|----------|--------|
| Content validity | Do items cover the construct adequately? | Expert review, CVI calculation |
| Face validity | Do items appear to measure the construct? | Target population review |
| Construct validity | Does it measure the theoretical construct? | Factor analysis (EFA/CFA) |
| Convergent validity | Does it correlate with similar measures? | Correlation with established instruments (r > 0.50) |
| Discriminant validity | Is it distinct from different constructs? | Low correlation with unrelated measures (r < 0.30) |
| Criterion (concurrent) | Does it correlate with a current criterion? | Correlation with gold standard, measured simultaneously |
| Criterion (predictive) | Does it predict a future outcome? | Correlation with criterion measured later |
| Known-groups | Can it distinguish groups known to differ? | Compare scores between groups that should differ |

Runnable Python for Cronbach's alpha, item-total correlations, EFA, and the three-phase pilot protocol: see `references/pilot_and_validation.md`. For CFA fit indices, measurement invariance, and the broader psychometric framework, see `references/survey-methodology.md`.

### 9. Online Survey Platform Comparison

| Feature | Qualtrics | REDCap | Google Forms | LimeSurvey |
|---------|-----------|--------|--------------|------------|
| Cost | Institutional license (expensive) | Free for institutions | Free | Free (open source) |
| Skip logic | Advanced | Advanced | Basic | Advanced |
| Randomization | Yes (items, blocks) | Limited | No | Yes |
| Piping | Yes | Yes | No | Yes |
| Offline data collection | Yes (app) | Yes (app) | No | Yes |
| HIPAA compliant | Yes (BAA available) | Yes (designed for it) | No | Self-hosted: yes |
| API access | Yes | Yes | Limited | Yes |
| Data export | CSV, SPSS, Excel | CSV, Excel, SPSS, SAS, R, Stata | CSV, Excel | CSV, Excel, SPSS, R |
| Multi-language | Yes | Yes | Manual | Yes |
| Panel integration | Yes (Prolific, MTurk) | No | No | Limited |
| Best for | Complex academic surveys | Clinical and health research | Simple surveys, course evaluations | Budget-conscious complex surveys |

### 10. Interview Protocol Development

Build semi-structured interview guides with a scripted opening/consent, a warm-up question, main-question blocks organized by construct (each with probes), a closing catch-all, and a post-interview field-notes routine.

Full **Semi-Structured Interview Guide Template**: see `references/qualitative_protocols.md`.

### 11. Focus Group Facilitation

Plan groups of 6-10 (4-6 for complex topics), 3-5 groups per segment until saturation, homogeneous within and heterogeneous across. Assign moderator and note-taker roles, prepare a neutral environment, and use funnel-approach facilitation to manage dominant and quiet voices.

Full **Focus Group Design Checklist**: see `references/qualitative_protocols.md`.

### 12. Cultural Adaptation of Instruments

Adapt instruments across languages/cultures using Brislin's (1970) back-translation cycle (forward translation → independent back-translation → reconciliation → cultural review → cognitive interviews → validation) and the 10-step ISPOR cross-cultural adaptation guidelines.

Full back-translation flow diagram and ISPOR step list: see `references/qualitative_protocols.md`.

---

## Best Practices

1. **Start with constructs, not questions.** Define exactly what you are measuring before writing a single item. Each item should trace back to a specific construct or dimension.

2. **Use existing validated instruments when possible.** Do not reinvent the wheel. Search the literature for instruments with established psychometric properties.

3. **Pilot everything.** Every survey should go through cognitive interviews and a quantitative pilot before full deployment. There is no substitute for testing with your target population.

4. **Keep it short.** Every additional item increases dropout risk. Include only items you will actually analyze. A good survey is as short as possible and as long as necessary.

5. **Design for your weakest respondent.** Write at an appropriate reading level. Test on mobile devices. Consider accessibility (screen readers, color contrast). Provide translations if needed.

6. **Randomize item order within sections.** This reduces order effects and helps detect careless responding.

7. **Include attention checks.** Embed 1-2 instructed response items (e.g., "Please select 'Agree' for this item") to identify careless respondents.

8. **Plan your analysis before collecting data.** Every question should have a purpose in your analysis plan. If you cannot say how you will analyze an item, remove it.

9. **Document everything.** Keep a survey design log recording every decision: why items were added, removed, or revised; pilot test results; expert feedback.

10. **Protect respondent data.** Use anonymous links when possible; store data securely; minimize collection of identifiers; comply with IRB requirements.

---

## Common Pitfalls

| Pitfall | Why It Happens | How to Avoid |
|---------|---------------|--------------|
| Double-barreled questions | Trying to be efficient; asking two things at once | Split into separate items; one concept per item |
| Leading questions | Researcher's hypothesis influences wording | Have a colleague blind to your hypothesis review items |
| Response options that do not match the stem | Copy-pasting from another survey | Ensure stem and response scale are grammatically and logically matched |
| Too many open-ended questions | Wanting rich data | Limit to 2-3 open-ended items; save depth for interviews |
| No pilot testing | Time pressure; overconfidence in item clarity | Always pilot — even a quick cognitive interview with 3-5 people helps |
| Ignoring mobile respondents | Designing on desktop | Test on multiple devices; avoid matrix questions on mobile (they break) |
| Low response rate | No follow-up plan; survey too long; no incentive | Pre-notify; send reminders (3-4 contacts); shorten survey; offer incentive |
| Neglecting psychometric validation | Assuming items are valid because they "look right" | Run reliability and factor analysis; report results in your paper |
| Convenience sampling reported as representative | Not understanding sampling limitations | Be honest about sampling method in limitations section |
| Cultural insensitivity | Assuming instruments transfer across cultures | Use formal adaptation procedures (back-translation, cognitive interviews) |

---

## References

- DeVellis, R. F., & Thorpe, C. T. (2022). *Scale development: Theory and applications* (5th ed.). Sage.
- Dillman, D. A., Smyth, J. D., & Christian, L. M. (2014). *Internet, phone, mail, and mixed-mode surveys: The tailored design method* (4th ed.). Wiley.
- Fowler, F. J. (2014). *Survey research methods* (5th ed.). Sage.
- Groves, R. M., Fowler, F. J., Couper, M. P., Lepkowski, J. M., Singer, E., & Tourangeau, R. (2009). *Survey methodology* (2nd ed.). Wiley.
- Krosnick, J. A., & Presser, S. (2010). Question and questionnaire design. In P. V. Marsden & J. D. Wright (Eds.), *Handbook of survey research* (2nd ed., pp. 263-313). Emerald.
- Podsakoff, P. M., MacKenzie, S. B., Lee, J. Y., & Podsakoff, N. P. (2003). Common method biases in behavioral research. *Journal of Applied Psychology*, 88(5), 879-903.
- Willis, G. B. (2005). *Cognitive interviewing: A tool for improving questionnaire design*. Sage.

See also: `references/survey-methodology.md` for expanded methodology details.
