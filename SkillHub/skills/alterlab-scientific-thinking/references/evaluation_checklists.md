# Detailed Evaluation Checklists

Operational, question-form review checklists relocated from SKILL.md for the Bias Detection, Statistical Analysis Evaluation, Evidence Quality Assessment, and Logical Fallacy Identification capabilities; consult the section matching the capability you are applying.

## Bias Detection — Systematic Bias Review

**Systematic bias review:**

1. **Cognitive Biases (Researcher)**
   - **Confirmation bias:** Are only supporting findings highlighted?
   - **HARKing:** Were hypotheses stated a priori or formed after seeing results?
   - **Publication bias:** Are negative results missing from literature?
   - **Cherry-picking:** Is evidence selectively reported?
   - Check for preregistration and analysis plan transparency

2. **Selection Biases**
   - **Sampling bias:** Is sample representative of target population?
   - **Volunteer bias:** Do participants self-select in systematic ways?
   - **Attrition bias:** Is dropout differential between groups?
   - **Survivorship bias:** Are only "survivors" visible in sample?
   - Examine participant flow diagrams and compare baseline characteristics

3. **Measurement Biases**
   - **Observer bias:** Could expectations influence observations?
   - **Recall bias:** Are retrospective reports systematically inaccurate?
   - **Social desirability:** Are responses biased toward acceptability?
   - **Instrument bias:** Do measurement tools systematically err?
   - Evaluate blinding, validation, and measurement objectivity

4. **Analysis Biases**
   - **P-hacking:** Were multiple analyses conducted until significance emerged?
   - **Outcome switching:** Were non-significant outcomes replaced with significant ones?
   - **Selective reporting:** Are all planned analyses reported?
   - **Subgroup fishing:** Were subgroup analyses conducted without correction?
   - Check for study registration and compare to published outcomes

5. **Confounding**
   - What variables could affect both exposure and outcome?
   - Were confounders measured and controlled (statistically or by design)?
   - Could unmeasured confounding explain findings?
   - Are there plausible alternative explanations?

## Statistical Analysis Evaluation — Statistical Review Checklist

**Statistical review checklist:**

1. **Sample Size and Power**
   - Was a priori power analysis conducted?
   - Is sample adequate for detecting meaningful effects?
   - Is the study underpowered (common problem)?
   - Do significant results from small samples raise flags for inflated effect sizes?

2. **Statistical Tests**
   - Are tests appropriate for data type and distribution?
   - Were test assumptions checked and met?
   - Are parametric tests justified, or should non-parametric alternatives be used?
   - Is the analysis matched to study design (e.g., paired vs. independent)?

3. **Multiple Comparisons**
   - Were multiple hypotheses tested?
   - Was correction applied (Bonferroni, FDR, other)?
   - Are primary outcomes distinguished from secondary/exploratory?
   - Could findings be false positives from multiple testing?

4. **P-Value Interpretation**
   - Are p-values interpreted correctly (probability of data if null is true)?
   - Is non-significance incorrectly interpreted as "no effect"?
   - Is statistical significance conflated with practical importance?
   - Are exact p-values reported, or only "p < .05"?
   - Is there suspicious clustering just below .05?

5. **Effect Sizes and Confidence Intervals**
   - Are effect sizes reported alongside significance?
   - Are confidence intervals provided to show precision?
   - Is the effect size meaningful in practical terms?
   - Are standardized effect sizes interpreted with field-specific context?

6. **Missing Data**
   - How much data is missing?
   - Is missing data mechanism considered (MCAR, MAR, MNAR)?
   - How is missing data handled (deletion, imputation, maximum likelihood)?
   - Could missing data bias results?

7. **Regression and Modeling**
   - Is the model overfitted (too many predictors, no cross-validation)?
   - Are predictions made outside the data range (extrapolation)?
   - Are multicollinearity issues addressed?
   - Are model assumptions checked?

8. **Common Pitfalls**
   - Correlation treated as causation
   - Ignoring regression to the mean
   - Base rate neglect
   - Texas sharpshooter fallacy (pattern finding in noise)
   - Simpson's paradox (confounding by subgroups)

## Evidence Quality Assessment — Evidence Evaluation Framework

**Evidence evaluation framework:**

1. **Study Design Hierarchy**
   - Systematic reviews/meta-analyses (highest for intervention effects)
   - Randomized controlled trials
   - Cohort studies
   - Case-control studies
   - Cross-sectional studies
   - Case series/reports
   - Expert opinion (lowest)

   **Important:** Higher-level designs aren't always better quality. A well-designed observational study can be stronger than a poorly-conducted RCT.

2. **Quality Within Design Type**
   - Risk of bias assessment (use appropriate tool: Cochrane ROB, Newcastle-Ottawa, etc.)
   - Methodological rigor
   - Transparency and reporting completeness
   - Conflicts of interest

3. **GRADE Considerations (if applicable)**
   - Start with design type (RCT = high, observational = low)
   - **Downgrade for:**
     - Risk of bias
     - Inconsistency across studies
     - Indirectness (wrong population/intervention/outcome)
     - Imprecision (wide confidence intervals, small samples)
     - Publication bias
   - **Upgrade for:**
     - Large effect sizes
     - Dose-response relationships
     - Confounders would reduce (not increase) effect

4. **Convergence of Evidence**
   - **Stronger when:**
     - Multiple independent replications
     - Different research groups and settings
     - Different methodologies converge on same conclusion
     - Mechanistic and empirical evidence align
   - **Weaker when:**
     - Single study or research group
     - Contradictory findings in literature
     - Publication bias evident
     - No replication attempts

5. **Contextual Factors**
   - Biological/theoretical plausibility
   - Consistency with established knowledge
   - Temporality (cause precedes effect)
   - Specificity of relationship
   - Strength of association

## Logical Fallacy Identification — Common Fallacies in Science

**Common fallacies in science:**

1. **Causation Fallacies**
   - **Post hoc ergo propter hoc:** "B followed A, so A caused B"
   - **Correlation = causation:** Confusing association with causality
   - **Reverse causation:** Mistaking cause for effect
   - **Single cause fallacy:** Attributing complex outcomes to one factor

2. **Generalization Fallacies**
   - **Hasty generalization:** Broad conclusions from small samples
   - **Anecdotal fallacy:** Personal stories as proof
   - **Cherry-picking:** Selecting only supporting evidence
   - **Ecological fallacy:** Group patterns applied to individuals

3. **Authority and Source Fallacies**
   - **Appeal to authority:** "Expert said it, so it's true" (without evidence)
   - **Ad hominem:** Attacking person, not argument
   - **Genetic fallacy:** Judging by origin, not merits
   - **Appeal to nature:** "Natural = good/safe"

4. **Statistical Fallacies**
   - **Base rate neglect:** Ignoring prior probability
   - **Texas sharpshooter:** Finding patterns in random data
   - **Multiple comparisons:** Not correcting for multiple tests
   - **Prosecutor's fallacy:** Confusing P(E|H) with P(H|E)

5. **Structural Fallacies**
   - **False dichotomy:** "Either A or B" when more options exist
   - **Moving goalposts:** Changing evidence standards after they're met
   - **Begging the question:** Circular reasoning
   - **Straw man:** Misrepresenting arguments to attack them

6. **Science-Specific Fallacies**
   - **Galileo gambit:** "They laughed at Galileo, so my fringe idea is correct"
   - **Argument from ignorance:** "Not proven false, so true"
   - **Nirvana fallacy:** Rejecting imperfect solutions
   - **Unfalsifiability:** Making untestable claims
