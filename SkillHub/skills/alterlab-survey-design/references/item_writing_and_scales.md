# Item Writing, Scales, and Survey Structure

Detailed templates and rules for construct mapping, question types, Likert scale design, item wording, survey organization, and skip logic. Extracted from the Survey Design skill body.

## Construct Definition and Operationalization

Before writing a single item, define what you are measuring.

**Construct Mapping Template:**

```markdown
## Construct Map

### Construct: [Name]
### Definition: [Precise conceptual definition with citation]

### Dimensions/Facets:
1. [Dimension 1] — [Definition]
   - Indicators: [Observable behaviors or attitudes]
   - Example items: [Draft items]

2. [Dimension 2] — [Definition]
   - Indicators: [Observable behaviors or attitudes]
   - Example items: [Draft items]

3. [Dimension 3] — [Definition]
   - Indicators: [Observable behaviors or attitudes]
   - Example items: [Draft items]

### Related but Distinct Constructs:
- [Construct A] — How it differs from your construct
- [Construct B] — How it differs from your construct

### Nomological Network:
- Should correlate positively with: [Constructs]
- Should correlate negatively with: [Constructs]
- Should be unrelated to: [Constructs]
```

## Item Writing

### Question Types and When to Use Them

| Type | Format | Best For | Example |
|------|--------|----------|---------|
| Closed-ended (single choice) | Radio buttons | Mutually exclusive categories | "What is your highest degree? ( ) Bachelor's ( ) Master's ( ) Doctoral" |
| Closed-ended (multiple choice) | Checkboxes | Non-mutually exclusive categories | "Which tools do you use? [ ] Qualtrics [ ] REDCap [ ] Google Forms" |
| Likert scale | Rating scale | Attitudes, perceptions, frequency | "I feel confident using statistics: Strongly Disagree 1 2 3 4 5 Strongly Agree" |
| Semantic differential | Bipolar scale | Evaluative judgments | "The training was: Useless ___:___:___:___:___ Useful" |
| Ranking | Drag-and-drop or numbered | Forced prioritization | "Rank these factors from most to least important: ___" |
| Matrix/Grid | Likert items in table | Multiple items with same response scale | [See matrix example below] |
| Open-ended | Text box | Exploratory, rich responses | "What challenges do you face in your research?" |
| Numeric | Number input | Precise quantities | "How many publications do you have? ___" |
| Visual analog scale (VAS) | Slider | Continuous measurement | "Rate your pain: No pain |------●------| Worst pain" |

### Likert Scale Design

**Number of Points:**

| Points | Pros | Cons | Use When |
|--------|------|------|----------|
| 4-point | Forces a choice (no midpoint) | May frustrate genuinely neutral respondents | You want to avoid social desirability midpoint clustering |
| 5-point | Most common; well-understood | Central tendency bias; midpoint ambiguity | Standard attitudinal measurement |
| 6-point | Forced choice with more granularity | Less familiar to respondents | You want to force direction with more options |
| 7-point | Greater discrimination; better for factor analysis | May exceed respondents' discriminative capacity | Established psychometric instruments; research contexts |

**Likert Scale Labeling:**

```
FULLY LABELED (recommended for clarity):
Strongly Disagree | Disagree | Neutral | Agree | Strongly Agree

END-ANCHORED ONLY (acceptable for experienced respondents):
Strongly Disagree | 2 | 3 | 4 | Strongly Agree

AGREEMENT:        Strongly Disagree → Strongly Agree
FREQUENCY:        Never → Always
IMPORTANCE:       Not at all Important → Extremely Important
SATISFACTION:     Very Dissatisfied → Very Satisfied
LIKELIHOOD:       Very Unlikely → Very Likely
QUALITY:          Very Poor → Excellent
```

### Item Writing Rules

**DO:**
1. Use simple, clear language (avoid jargon, acronyms, technical terms unless your population uses them)
2. Ask about one thing per item (no double-barreled questions)
3. Use specific time frames ("In the past 30 days..." not "Do you ever...")
4. Match the response scale to the question stem
5. Include both positively and negatively worded items (with caution — see pitfalls)
6. Pilot test items with your target population
7. Write 2-3x more items than you need (expect to cut during validation)

**DO NOT:**
1. Use leading or loaded language ("Don't you agree that...")
2. Use double negatives ("How much do you disagree with not implementing...")
3. Assume knowledge ("Rate the effectiveness of the Delphi method" — respondent may not know it)
4. Use absolutes ("always," "never," "all," "none") unless measuring frequency
5. Create unnecessarily long items (aim for under 20 words per item)
6. Use hypothetical scenarios when asking about actual behavior

**Examples of Item Revisions:**

```
POOR: "How satisfied are you with the quality and timeliness of feedback?"
       (Double-barreled: quality AND timeliness)
FIX:  Item 1: "How satisfied are you with the quality of feedback you receive?"
      Item 2: "How satisfied are you with the timeliness of feedback you receive?"

POOR: "Students should not be required to not attend classes."
       (Double negative)
FIX:  "Class attendance should be mandatory."

POOR: "Do you agree that the new policy is beneficial?"
       (Leading — assumes the policy is beneficial)
FIX:  "The new policy has been beneficial to my work."
       (Neutral stem; let the Likert scale capture agreement/disagreement)

POOR: "Rate your teaching effectiveness." (1-5)
       (Socially desirable response; no reference frame)
FIX:  "In the past semester, how often did you use student feedback
       to modify your teaching?" (Never / Rarely / Sometimes / Often / Always)
```

## Survey Structure and Flow

**Recommended Survey Organization:**

```markdown
## Survey Structure Template

### Page 1: Welcome and Consent
- Study title, purpose, estimated time
- Consent checkbox (mandatory before proceeding)
- Contact information for questions

### Page 2: Screening Questions (if applicable)
- Eligibility criteria
- Route ineligible respondents to end-of-survey message

### Page 3-N: Main Content Sections
- Group by topic/construct
- Progress bar visible
- Section headers with brief context
- Start with engaging, easy questions
- Place sensitive questions in the middle (after rapport, before fatigue)
- Use skip logic to hide irrelevant questions

### Page N+1: Demographics
- Place at the END (reduces dropout from sensitive questions early)
- Include only demographics you will actually analyze
- Provide "Prefer not to answer" option for sensitive items

### Final Page: Thank You
- Thank participant
- Provide debriefing information
- Share contact info for results
- Remind of withdrawal procedure
```

**Skip Logic Design:**

```
Q1: Do you supervise graduate students?
    ( ) Yes → Show Q2-Q5 (supervision questions)
    ( ) No  → Skip to Q6

Q3: How many students do you currently supervise?
    [Number input]
    If Q3 > 5 → Show Q4 (workload management question)
    If Q3 ≤ 5 → Skip to Q5

Q10: Would you like to participate in a follow-up interview?
     ( ) Yes → Show Q11 (contact information)
     ( ) No  → Skip to end
```
