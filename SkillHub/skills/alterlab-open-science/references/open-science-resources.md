# Open Science Resources -- Reference Guide

## Preregistration Templates and Platforms

### OSF Preregistration Templates

**Standard OSF Preregistration (van 't Veer & Giner-Sorolla, 2016)**

This is the most comprehensive template and works across disciplines:

```
Section 1: Study Information
  - Title
  - Authors
  - Research questions
  - Hypotheses (numbered, directional)

Section 2: Design Plan
  - Study type (experiment, survey, observational, archival, other)
  - Blinding (no blinding, single, double, triple)
  - Study design (between, within, mixed)
  - Randomization

Section 3: Sampling Plan
  - Existing data (registration prior to creation, prior to access, prior to analysis)
  - Explanation of existing data
  - Data collection procedures
  - Sample size and rationale
  - Stopping rule

Section 4: Variables
  - Manipulated variables
  - Measured variables
  - Indices (composite measures)

Section 5: Analysis Plan
  - Statistical models
  - Transformations
  - Inference criteria
  - Data exclusion
  - Missing data handling
  - Exploratory analyses
```

**AsPredicted Template (8 Questions)**

```
1. Have any data been collected for this study already?
2. What is the main question being asked or hypothesis being tested?
3. Describe the key dependent variable(s).
4. How many and which conditions will participants be assigned to?
5. Specify exactly which analyses you will conduct to examine the main question/hypothesis.
6. Any secondary analyses?
7. How many observations will be collected or what will determine sample size?
8. Anything else you would like to pre-register?
```

### Registered Report Journals by Discipline

| Discipline | Journals Accepting Registered Reports |
|-----------|--------------------------------------|
| Psychology | Cortex, PLOS ONE, Royal Society Open Science, Psychological Science, JEP:General |
| Neuroscience | eLife, Nature Human Behaviour, Cortex, NeuroImage |
| Education | AERA Open, Journal of Educational Psychology |
| Political Science | Journal of Politics, Political Analysis, BJPS |
| Economics | Journal of Development Economics, Experimental Economics |
| Biology | PLOS Biology, BMC Biology, PeerJ |
| Medicine | BMJ, The Lancet (pilot), BMJ Open |
| Environmental Science | Nature Ecology & Evolution, PeerJ |

## FAIR Data Implementation Guide

### Metadata Standards by Discipline

| Discipline | Standard | Description |
|-----------|----------|-------------|
| General | Dublin Core | 15-element descriptive metadata standard |
| Social Science | DDI (Data Documentation Initiative) | Comprehensive social/behavioral science metadata |
| Geospatial | ISO 19115 | Geographic information metadata |
| Biology | MIAME, MINSEQE | Microarray and sequencing experiment metadata |
| Climate | CF Conventions | Climate and forecast metadata |
| Humanities | TEI Header | Text Encoding Initiative metadata for texts |
| Health | FHIR | Fast Healthcare Interoperability Resources |

### Data Format Recommendations

**Preferred open formats:**

| Data Type | Preferred Format | Avoid |
|----------|-----------------|-------|
| Tabular data | CSV, TSV | XLS/XLSX (proprietary), SAV (SPSS binary) |
| Text | Plain text, Markdown, XML | DOCX (complex), PDF (not machine-readable) |
| Images | TIFF, PNG | BMP (uncompressed, huge) |
| Audio | WAV, FLAC | MP3 (lossy) |
| Video | MP4 (H.264) | WMV (proprietary) |
| Geospatial | GeoJSON, GeoTIFF, Shapefile | Proprietary GIS formats |
| Statistical | R (.rds), Parquet | Stata (.dta) if long-term preservation |

### Data Dictionary Template

```
Variable Name: participant_id
  Type: Integer
  Description: Unique participant identifier assigned at enrollment
  Range: 1001-9999
  Missing values: None expected

Variable Name: condition
  Type: Categorical
  Description: Experimental condition assignment
  Values: 1 = spaced practice, 2 = massed practice, 3 = control
  Missing values: NA = participant withdrew before assignment

Variable Name: retention_score
  Type: Continuous (float)
  Description: Score on delayed retention test, percentage correct
  Range: 0.0-100.0
  Units: Percentage
  Missing values: NA = participant did not complete test
  Notes: Calculated as (correct items / total items) * 100
```

## Open Access Decision Flowchart

```
Is your funder Plan S / cOAlition S compliant?
  YES --> You must publish OA with CC-BY
    --> Option 1: Gold OA journal (check DOAJ)
    --> Option 2: Use Rights Retention Strategy + Green OA
  NO --> Continue to next question

Does your institution have OA mandates?
  YES --> Check specific requirements (may allow Green OA with embargo)
  NO --> Continue to next question

Do you have APC funding?
  YES --> Gold OA is straightforward
    --> Check journal is in DOAJ (not predatory)
    --> Verify APC is reasonable for your field
  NO --> Green OA is your best option
    --> Post preprint on discipline server
    --> Deposit accepted manuscript in institutional repository
    --> Check Sherpa Romeo for publisher embargo policy
```

## Reproducibility Toolkit

### Makefile for Research Pipeline

```makefile
# Makefile for reproducible research pipeline

.PHONY: all clean data analysis figures paper

all: paper

data: data/processed/clean_data.csv

data/processed/clean_data.csv: data/raw/survey_responses.csv scripts/01_clean_data.R
	Rscript scripts/01_clean_data.R

analysis: output/models/main_results.rds

output/models/main_results.rds: data/processed/clean_data.csv scripts/02_analysis.R
	Rscript scripts/02_analysis.R

figures: output/figures/figure1.pdf output/figures/figure2.pdf

output/figures/%.pdf: output/models/main_results.rds scripts/03_figures.R
	Rscript scripts/03_figures.R

paper: manuscript/manuscript.pdf

manuscript/manuscript.pdf: manuscript/manuscript.Rmd analysis figures
	Rscript -e "rmarkdown::render('manuscript/manuscript.Rmd')"

clean:
	rm -f data/processed/*.csv
	rm -f output/models/*.rds
	rm -f output/figures/*.pdf
	rm -f manuscript/manuscript.pdf
```

### Project Directory Structure

```
my-research-project/
  README.md                 # Project overview and instructions
  LICENSE                   # Data/code license
  CITATION.cff             # How to cite this project
  Makefile                 # Automated pipeline
  environment.yml          # Python environment (or renv.lock for R)
  Dockerfile               # Full environment specification
  .gitignore              # Files not tracked by git
  
  data/
    raw/                   # Original, immutable data
      README.md           # Data provenance documentation
    processed/            # Cleaned, analysis-ready data
    
  scripts/
    01_clean_data.R       # Data cleaning
    02_analysis.R         # Main analyses
    03_figures.R          # Visualization
    utils/                # Helper functions
    
  output/
    models/               # Saved model objects
    figures/              # Generated figures
    tables/               # Generated tables
    
  manuscript/
    manuscript.Rmd        # Paper source
    references.bib        # Bibliography
    
  docs/
    preregistration.md    # Link to OSF preregistration
    codebook.md           # Variable definitions
    analysis_log.md       # Decision log during analysis
```

## Repository Comparison and Selection Guide

### Decision Matrix

| Factor | Zenodo | Dryad | Figshare | OSF | ICPSR |
|--------|--------|-------|----------|-----|-------|
| Cost | Free | $150+ per submission | Free (basic) | Free | Free (depositor) |
| Curation | Minimal | Full curation | Minimal | Minimal | Full curation |
| Max size | 50 GB | No limit | 5 GB (free) | 50 GB | No limit |
| Versioning | Yes | Yes | Yes | Yes | Limited |
| Embargo | Yes | Yes | Yes | Yes | Yes |
| Access control | No | No | No | Yes | Yes |
| GitHub integration | Yes (automatic DOI) | No | Yes | Yes | No |
| Best for | Code + data bundles | Curated datasets | Mixed media | Collaborative projects | Social science |

### Repository Selection by Funder

| Funder | Accepted/Required Repositories |
|--------|-------------------------------|
| NIH | Domain-specific (GenBank, dbGaP, etc.) or generalist with DOI |
| NSF | Any repository meeting FAIR principles |
| ERC / Horizon Europe | OpenAIRE-compatible (Zenodo recommended) |
| UKRI | UKRI-approved repositories |
| Wellcome Trust | Europe PMC + approved data repositories |
| Gates Foundation | Immediate open access + approved data repository |

## License Selection Quick Reference

### For Publications

| Situation | Recommended License | Reason |
|-----------|-------------------|--------|
| Plan S funded research | CC-BY 4.0 | Required by policy |
| Want maximum dissemination | CC-BY 4.0 | Most permissive with attribution |
| Concerned about commercial misuse | CC-BY-NC 4.0 | Restricts commercial use |
| Want to prevent modifications | CC-BY-ND 4.0 | Prevents derivative works |

### For Data

| Situation | Recommended License | Reason |
|-----------|-------------------|--------|
| Maximum reusability | CC0 | No restrictions, broadest adoption |
| Want attribution | CC-BY 4.0 | Attribution required |
| Sensitive data | Custom DUA | Data Use Agreement with specific terms |

### For Software

| Situation | Recommended License | Reason |
|-----------|-------------------|--------|
| Maximum adoption | MIT | Simple, permissive |
| Patent protection | Apache 2.0 | Explicit patent grant |
| Want derivatives open | GPL v3 | Copyleft ensures openness |
| Academic use only | Not recommended | OSI-approved licenses preferred |

## Further Reading

### Essential Books
- Fogel, K. (2005). *Producing Open Source Software*. O'Reilly Media. (Free online)
- Stodden, V., Leisch, F., & Peng, R. D. (2014). *Implementing Reproducible Research*. CRC Press.
- Suber, P. (2012). *Open Access*. MIT Press. (Free online)
- Wilson, G., et al. (2017). Good enough practices in scientific computing. *PLOS Computational Biology*, 13(6), e1005510.

### Key Policy Documents
- cOAlition S Plan S: https://www.coalition-s.org/
- NIH Data Management and Sharing Policy: https://sharing.nih.gov/
- NSF Public Access Plan: https://new.nsf.gov/public-access
- UKRI Open Access Policy: https://www.ukri.org/publications/ukri-open-access-policy/

### Training Resources
- FOSTER Open Science Training: https://web.archive.org/web/2019/https://www.fosteropenscience.eu/
- The Turing Way: https://the-turing-way.netlify.app/
- Software Carpentry: https://software-carpentry.org/
- Library Carpentry: https://librarycarpentry.org/
- Center for Open Science Ambassador Program: https://www.cos.io/communities/ambassadors
