---
name: alterlab-open-science
description: "Guidance for open science practices — preregistration (OSF Registries, AsPredicted, PROSPERO, ClinicalTrials.gov), open data and FAIR principles, repository choice (Zenodo, Dryad, Figshare), open access routes (Green/Gold/Diamond), Creative Commons licensing, reproducible computational workflows (Docker, Binder, Code Ocean), registered reports, open peer review, and TOP Guidelines. Use when preregistering a study, writing the FAIR data-sharing and repository section of a grant data management plan (NSF, NIH, ERC, UKRI), choosing a data repository, navigating open access, or building reproducible analyses. For human-subjects ethics, IRB applications, informed consent, or GDPR/HIPAA compliance, defer to alterlab-research-ethics. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read WebFetch WebSearch Bash(python:*)
compatibility: No API key required. Guidance-focused skill; uses WebFetch/WebSearch and optional Python helpers via `uv run python`.
metadata:
  skill-author: AlterLab
  version: "1.0.0"
  last_updated: "2026-03-18"
---

# Open Science Practices

## Overview

Open science represents a fundamental shift in how research is conducted, shared, and evaluated. Rather than treating the scientific process as a series of private activities culminating in a polished publication, open science makes the entire research lifecycle transparent -- from the initial hypothesis through data collection, analysis, and dissemination. This transparency serves multiple purposes: it increases trust in research findings, accelerates scientific progress by enabling reuse and replication, reduces waste by making negative results visible, and democratizes access to knowledge.

The open science movement encompasses a wide range of practices: preregistration of study designs and analyses, registered reports that receive peer review before data collection, open sharing of data and materials under FAIR principles (Findable, Accessible, Interoperable, Reusable), open access publishing through various routes (Green, Gold, Diamond), reproducible computational workflows using containers and notebooks, open peer review, and the use of persistent repositories for long-term data preservation.

This skill provides practical guidance for implementing each of these practices. It is not an advocacy document -- it acknowledges the real tensions between openness and privacy, the costs of open access publishing, and the career incentives that sometimes conflict with open practices. The goal is to equip researchers with the knowledge to make informed decisions about which open science practices to adopt, when, and how.

## When to Use This Skill

Use this skill when you need to:

- Preregister a study on the Open Science Framework (OSF) or AsPredicted
- Prepare a registered report submission for a journal
- Create a data management plan for a grant application (NSF, NIH, ERC, UKRI)
- Share research data in compliance with FAIR principles
- Choose an appropriate data repository (Zenodo, Dryad, Figshare, domain-specific)
- Navigate open access publishing options and costs
- Select Creative Commons licenses for research outputs
- Build reproducible computational analyses using Docker, Binder, or Code Ocean
- Create computational notebooks that others can execute and verify
- Participate in or set up open peer review processes
- Plan and conduct replication studies
- Develop or contribute to open source research software
- Comply with funder mandates for data sharing and open access
- Understand and implement the TOP Guidelines (Transparency and Openness Promotion)

## Core Capabilities

### Preregistration

Preregistration involves publicly recording your research plan -- hypotheses, methods, sample size, and analysis strategy -- before collecting or analyzing data. It distinguishes confirmatory analyses (hypothesis-testing) from exploratory analyses (hypothesis-generating), reducing the risk of p-hacking, HARKing (Hypothesizing After Results are Known), and other questionable research practices.

**Key preregistration platforms:**

| Platform | Best For | Features |
|----------|----------|----------|
| OSF Registries | All disciplines | Multiple templates, embargo options, DOI, integrates with OSF projects |
| AsPredicted | Quick preregistration | 8-question template, simple, generates PDF |
| ClinicalTrials.gov | Clinical trials | Legally required for most interventional trials in the US |
| PROSPERO | Systematic reviews | Specific to health-related systematic reviews |
| EGAP | Political science / governance | Designed for experimental governance research |

**What to include in a preregistration:**

1. **Research questions and hypotheses** -- State specific, testable predictions
2. **Design** -- Experimental, quasi-experimental, observational, survey
3. **Variables** -- Independent, dependent, covariates, moderators, mediators
4. **Sample** -- Target population, sampling strategy, inclusion/exclusion criteria
5. **Sample size justification** -- Power analysis or resource constraints with rationale
6. **Measurement** -- Instruments, scales, operationalization of constructs
7. **Analysis plan** -- Statistical tests, model specifications, assumption checks
8. **Inference criteria** -- Alpha level, correction for multiple comparisons
9. **Exclusion criteria** -- Rules for removing data points or participants
10. **Exploratory analyses** -- Planned but not confirmatory

A worked preregistration excerpt (hypothesis, analysis plan, power analysis) and the common misconceptions about what preregistration does *not* require (exploratory analyses, deviations, qualitative work) are collected in `references/preregistration_guide.md`. Reusable OSF and AsPredicted templates live in `references/open-science-resources.md`.

### Registered Reports

Registered reports take preregistration further by embedding it in the peer review process. The study is reviewed in two stages:

**Stage 1: Before data collection**
- Introduction, hypotheses, methods, and analysis plan are peer-reviewed
- If accepted, the journal issues an In-Principle Acceptance (IPA)
- The study will be published regardless of results, provided the protocol is followed

**Stage 2: After data collection**
- Results and discussion are added to the accepted protocol
- Reviewed only for adherence to the plan and quality of interpretation
- Published regardless of whether results are statistically significant

**Benefits of registered reports:**
- Eliminates publication bias (null results get published)
- Peer review improves methods before costly data collection
- Removes incentive for p-hacking since results do not determine publication
- Provides a clear commitment device for confirmatory research

**Journals offering registered reports:** Over 300 journals across disciplines now accept registered reports. The Center for Open Science maintains the complete list at cos.io/rr.

A full annotated Stage 1 submission structure (introduction, methods, layered analysis plan, exclusion criteria, timeline) is in `references/preregistration_guide.md`; a discipline-by-discipline list of registered-report journals is in `references/open-science-resources.md`.

### Open Data and FAIR Principles

The FAIR principles provide a framework for making data maximally useful for both humans and machines:

**Findable:**
- Assign a persistent identifier (DOI) to every dataset
- Describe data with rich metadata
- Register the dataset in a searchable resource
- Include the identifier in the metadata

**Accessible:**
- Store data in a trusted repository with long-term preservation
- Use standardized, open protocols for data retrieval
- Provide metadata even when the data itself cannot be shared
- Implement authentication where necessary (not all data can be open)

**Interoperable:**
- Use formal, accessible, shared language for knowledge representation
- Use vocabularies that follow FAIR principles
- Include qualified references to other data

**Reusable:**
- Describe data with accurate and relevant attributes
- Release with clear, accessible data usage licenses
- Associate data with detailed provenance
- Meet domain-relevant community standards

**Practical data sharing checklist:** A full three-phase checklist (before sharing, preparing the deposit, depositing) covering de-identification, codebooks, formats, licensing, DOIs, and data availability statements is in `references/data_sharing_and_dmp.md`. Metadata standards and preferred open file formats by discipline are in `references/open-science-resources.md`.

### Data Management Plans

Most major funders now require a data management plan (DMP) as part of grant applications. A DMP describes how data will be collected, organized, stored, shared, and preserved.

**NSF DMP requirements (2 pages):**
1. Types of data produced
2. Data and metadata standards
3. Policies for access and sharing
4. Policies for re-use and redistribution
5. Plans for archiving and preservation

**NIH Data Management and Sharing Plan (post-2023):**
1. Data type
2. Related tools, software, and code
3. Standards
4. Data preservation, access, and associated timelines
5. Access, distribution, and reuse considerations
6. Oversight of data management and sharing

A worked DMP excerpt (data types, sharing plan, standards) and the list of DMP authoring tools (DMPTool, DMPonline, ARGOS) are in `references/data_sharing_and_dmp.md`.

### Open Access Publishing

Open access (OA) removes paywalls so that anyone can read research without a subscription. There are several routes to OA:

**Gold OA:** Published in a fully open access journal. The author (or their funder/institution) pays an Article Processing Charge (APC). Examples: PLOS ONE, eLife, BMJ Open.

**Green OA:** The author deposits a version of the paper (preprint or accepted manuscript) in a repository. The journal may impose an embargo period (typically 6-12 months). No APC required. Repositories include institutional repositories, PubMed Central, arXiv, and SSRN.

**Diamond OA (Platinum OA):** The journal is open access with no APC -- costs are covered by institutions, scholarly societies, or grants. Examples include many humanities journals, the Journal of Machine Learning Research, and some society journals.

**Hybrid OA:** The journal is subscription-based but offers an OA option for individual articles (for an APC). Controversial because institutions pay twice (subscription + APC). Some funders (e.g., cOAlition S / Plan S) no longer fund hybrid OA.

**Bronze OA:** Free to read on the publisher website but without an open license. The publisher can remove access at any time. Not true OA.

**APC cost ranges (2025-2026):**

| Publisher Tier | Typical APC |
|---------------|-------------|
| Mega journals (PLOS ONE) | $1,500-$2,000 |
| Mid-tier specialty journals | $2,000-$4,000 |
| High-impact journals (Nature, Science OA options) | $5,000-$11,000 |
| Diamond OA journals | $0 |

**Rights retention strategy:** Many funders (including cOAlition S members) now support a Rights Retention Strategy where authors retain a CC-BY license on the Author Accepted Manuscript, regardless of publisher policy. This enables Green OA deposit immediately upon acceptance.

**Preprint servers by discipline:**

| Server | Disciplines |
|--------|------------|
| arXiv | Physics, mathematics, computer science, quantitative biology |
| bioRxiv | Biology |
| medRxiv | Health sciences (not peer-reviewed clinical findings) |
| SSRN | Social sciences, economics, law |
| PsyArXiv | Psychology |
| SocArXiv | Sociology, political science |
| EdArXiv | Education |
| EarthArXiv | Earth sciences |
| ChemRxiv | Chemistry |
| OSF Preprints | All disciplines |

### Creative Commons Licenses for Research

Creative Commons (CC) licenses provide standardized terms for sharing research outputs. Understanding them is essential for open science.

**License options (most to least permissive):**

| License | Allows | Requires | Restrictions |
|---------|--------|----------|-------------|
| CC0 (Public Domain) | Anything | Nothing | None |
| CC-BY | Anything | Attribution | None |
| CC-BY-SA | Anything | Attribution, share-alike | Derivatives must use same license |
| CC-BY-NC | Non-commercial use | Attribution | No commercial use |
| CC-BY-NC-SA | Non-commercial use | Attribution, share-alike | No commercial use, same license |
| CC-BY-ND | Sharing only | Attribution | No derivatives |
| CC-BY-NC-ND | Non-commercial sharing | Attribution | No commercial use, no derivatives |

**Recommendations:**
- **Data:** CC0 or CC-BY 4.0 (most reusable; databases have separate legal protections)
- **Publications:** CC-BY 4.0 (required by many funders including Plan S)
- **Software:** Use OSI-approved licenses (MIT, Apache 2.0, GPL) -- CC licenses are not designed for software
- **Educational materials:** CC-BY or CC-BY-SA (enables OER use)

### Reproducible Analysis

Reproducibility means that another researcher can take your data and code and obtain the same results. Computational reproducibility is the minimum standard; replicability (obtaining similar results with new data) is the aspirational goal.

**Levels of reproducibility:**

1. **Documentation** -- Describe your analysis steps in sufficient detail that someone could in principle reproduce them
2. **Code sharing** -- Share the actual analysis scripts used
3. **Environment capture** -- Record the software versions, packages, and operating system used
4. **Containerization** -- Package the complete computational environment (Docker, Singularity)
5. **Executable environment** -- Provide a one-click way to run the analysis (Binder, Code Ocean)

**Tooling for each level:** *Docker/Singularity* package the complete environment; *Binder* (mybinder.org) turns a GitHub repo with an `environment.yml` or `install.R` into a live interactive Jupyter/RStudio session with zero local install; *Code Ocean* provides guaranteed reproducibility with a published DOI per "compute capsule" (used by Nature and others for results verification). Always pin exact package versions so environments rebuild identically.

Copy-ready recipes -- a Dockerfile for an R analysis, an annotated Binder `environment.yml`, a CITATION.cff software-citation file, and the eight core rules for reproducible code (relative paths, random seeds, package managers, session info, pipeline automation, version control, README, clean-machine testing) -- are in `references/reproducible_workflows.md`. A Makefile pipeline and a full project directory layout are in `references/open-science-resources.md`.

### Computational Notebooks

Jupyter notebooks, R Markdown, and Quarto documents combine code, text, and results in a single document. They are powerful tools for reproducible research when used well.

**Jupyter notebooks (.ipynb):**
- Best for Python, Julia, R
- Interactive exploration and visualization
- Runs in browser, shareable via GitHub, Binder, Google Colab
- Risk: non-linear execution order can break reproducibility

**R Markdown (.Rmd) / Quarto (.qmd):**
- Best for R (also supports Python, Julia)
- Produces polished documents (PDF, HTML, Word)
- Linear execution model (more reproducible than notebooks)
- papaja package creates APA-formatted manuscripts directly

**Best practices for notebooks:**
- Restart and run all cells before sharing (ensures linear execution)
- Use meaningful cell ordering (do not rely on out-of-order execution)
- Clear all outputs before committing to version control
- Use nbstripout or similar to prevent bloated diffs
- Pair notebooks with standalone scripts for production analyses

### Open Peer Review

Open peer review encompasses several practices that increase transparency in the review process:

**Models of open peer review:**

1. **Open identities** -- Reviewer names are disclosed to authors (and sometimes publicly)
2. **Open reports** -- Review text is published alongside the paper
3. **Open participation** -- Anyone can submit reviews or comments (not just invited reviewers)
4. **Open interaction** -- Authors and reviewers engage in dialogue during review
5. **Open pre-review manuscripts** -- Preprints allow public comment before formal review

**Journals practicing open peer review:**

| Journal/Platform | Model |
|-----------------|-------|
| eLife | Published reviews with author responses |
| BMJ | Open identities, open reports |
| F1000Research | Post-publication open review |
| PLOS ONE (optional) | Authors can opt for open reports |
| PeerJ | Authors can publish review history |
| Frontiers | Open identities, structured reports |

### Data Repositories

Choosing the right repository depends on your discipline, data type, and funder requirements.

**General-purpose repositories:**

| Repository | Max File Size | License | DOI | Preservation |
|-----------|--------------|---------|-----|-------------|
| Zenodo | 50 GB per dataset | Flexible | Yes | CERN long-term |
| Dryad | No hard limit | CC0 required | Yes | Curated, long-term |
| Figshare | 5 GB free, 20 GB institutional | Flexible | Yes | Long-term |
| OSF | 5 GB per file, 50 GB per project | Flexible | Yes | Long-term |
| Harvard Dataverse | 2.5 GB per file | Flexible | Yes | Long-term |

**Domain-specific repositories (selected):**

| Repository | Domain | Notes |
|-----------|--------|-------|
| GenBank / SRA | Genomics | Required for sequence data |
| PDB | Protein structures | Required for structural biology |
| ICPSR | Social science | Curated, access-controlled options |
| PANGAEA | Earth sciences | Georeferenced data |
| Qualitative Data Repository | Qualitative research | Specialized for interview/ethnographic data |
| UK Data Archive | Social science (UK) | Long-term preservation |
| Archaeology Data Service | Archaeology | UK-based, international scope |

### Replication Studies

Replication studies attempt to reproduce the findings of a previous study. They are essential for scientific self-correction but historically undervalued.

**Types of replication:**

1. **Direct replication** -- Same methods, same population, same analysis
2. **Conceptual replication** -- Different methods testing the same theoretical prediction
3. **Systematic replication** -- Planned variation across conditions, populations, or contexts

**Planning a replication study:**

- Obtain original materials from the authors (required for direct replication)
- Preregister your replication plan on OSF or AsPredicted
- Power the study to detect the original effect size (not just "significance")
- Use the "small telescopes" approach (Simonsohn, 2015) to determine the minimum detectable effect
- Report results relative to both the original effect and your smallest effect of interest
- Submit to a journal that publishes replications (e.g., PLOS ONE replication collection)

**Key considerations:**

- Contact the original authors early -- they may share materials, data, or analysis code
- Pre-specify your criteria for what counts as a "successful" replication
- Consider multi-site replications for greater generalizability
- Publish regardless of outcome -- negative replications are scientifically valuable

### Open Source Research Software

Research software is increasingly recognized as a first-class scholarly output. Making it open source enhances reproducibility and enables community contributions.

**Best practices for research software:**

1. **Choose an appropriate license** -- MIT (permissive), Apache 2.0 (permissive with patent protection), GPL (copyleft)
2. **Use version control** -- Git with a public repository on GitHub/GitLab
3. **Write documentation** -- README, installation instructions, usage examples, API reference
4. **Add tests** -- Unit tests, integration tests, and regression tests
5. **Use continuous integration** -- GitHub Actions, Travis CI, or similar
6. **Create releases with semantic versioning** -- v1.2.3 (major.minor.patch)
7. **Publish a DOI** -- Zenodo-GitHub integration mints DOIs for each release
8. **Write a software paper** -- Journal of Open Source Software (JOSS) publishes peer-reviewed software papers
9. **Add a CITATION.cff file** -- Machine-readable citation metadata

A ready-to-adapt CITATION.cff example (authors, ORCID, version, DOI, license) is in `references/reproducible_workflows.md`.

## Best Practices

### Getting Started with Open Science

1. **Start with preregistration** -- It is free, it improves your research design, and it takes only an hour. Use the AsPredicted template for your next confirmatory study.
2. **Share your data with your next paper** -- Choose Zenodo or a domain-specific repository. Write a codebook. It gets easier every time.
3. **Post preprints** -- Upload to the appropriate preprint server before or at submission. It increases visibility and establishes priority.
4. **Use version control** -- If you write any code for your research, use git. This is non-negotiable for reproducibility.
5. **Document as you go** -- Writing README files, codebooks, and analysis logs during the project is far easier than reconstructing them later.

### Navigating Institutional and Funder Requirements

1. **Know your funder mandate** -- NIH, NSF, ERC, UKRI, and many others now require data sharing plans and open access. Read the specific policy for your grant.
2. **Use your institutional repository** -- Many universities operate institutional repositories that meet Green OA requirements.
3. **Check publisher policies** -- Sherpa Romeo (sherpa.ac.uk/romeo) catalogs publisher self-archiving policies.
4. **Budget for APCs** -- Include open access publication costs in your grant budget. Most funders allow this.
5. **Negotiate with publishers** -- Use rights retention language in your cover letter if your funder requires it.

### Balancing Openness with Constraints

1. **Sensitive data** -- Not all data can or should be shared openly. Human subjects data with re-identification risk, Indigenous data sovereignty concerns, and proprietary data all require careful handling. Share metadata and analysis code even when raw data cannot be shared.
2. **Scooping concerns** -- Preregistration and preprints actually protect against scooping by establishing a timestamped public record of your work.
3. **Career incentives** -- Some tenure committees undervalue open science contributions. Document the impact of your open resources (downloads, citations, reuse).
4. **Time costs** -- Open science practices take time to learn and implement. Start with one or two practices and build incrementally.

### Building an Open Science Lab Culture

1. **Model the behavior** -- If you are a PI, preregister your own studies and share your own data before expecting trainees to do so.
2. **Provide training** -- Allocate lab meeting time for open science skills (git, OSF, Docker, data management).
3. **Reward open practices** -- Recognize and celebrate when lab members share data, post preprints, or contribute to open source tools.
4. **Create templates** -- Develop lab-specific preregistration templates, data management plans, and README templates that lower the barrier to adoption.
5. **Budget for it** -- Include data management, APC costs, and open science infrastructure in grant applications.

## Common Pitfalls

### Preregistration Pitfalls

- **Over-specifying the plan** -- A preregistration that is too rigid leaves no room for sensible methodological decisions during data collection. Include decision rules for anticipated contingencies.
- **Under-specifying the plan** -- A vague preregistration provides little protection against researcher degrees of freedom. Be specific about analysis decisions.
- **Preregistering after peeking at data** -- This defeats the purpose. Even preliminary looks at the data compromise the confirmatory status of your analyses.
- **Treating deviations as failures** -- Deviations from the plan are fine if transparently reported and justified. Science is messy.

### Data Sharing Pitfalls

- **Sharing data without a license** -- Data without a license defaults to "all rights reserved" in many jurisdictions. Always include a license (CC0 or CC-BY).
- **Insufficient de-identification** -- Removing names is not enough. Combinations of demographic variables can re-identify individuals. Use formal anonymization methods and consult your IRB.
- **No documentation** -- Data without a codebook is useless to others. Variable names like "Q4_rev_3" mean nothing without definitions.
- **Forgetting to cite data** -- Published datasets should be cited like papers. Use the DOI.

### Reproducibility Pitfalls

- **"Works on my machine" syndrome** -- Code that depends on your local setup will break elsewhere. Use containers or virtual environments.
- **Non-linear notebook execution** -- Running Jupyter cells out of order creates hidden state. Always restart-and-run-all before sharing.
- **Hardcoded paths** -- /Users/martinez/Desktop/project/data.csv will not work on anyone else's machine. Use relative paths.
- **Missing random seeds** -- Stochastic analyses without set seeds produce different results each run.
- **Outdated dependencies** -- Recording package versions with a lockfile prevents future breakage.

### Open Access Pitfalls

- **Predatory publishers** -- Predatory journals charge APCs but provide no real peer review. Check DOAJ, and publisher reputation before submitting.
- **Double-dipping publishers** -- Some hybrid journals charge both subscriptions and APCs. Many funders now refuse to pay hybrid APCs.
- **Losing copyright** -- Read the publishing agreement carefully. Many publishers require copyright transfer, which limits your ability to share your own work.
- **Ignoring embargoes** -- If you signed a publishing agreement with a 12-month embargo, respect it or negotiate before signing.

## References

- Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). The preregistration revolution. *Proceedings of the National Academy of Sciences*, 115(11), 2600-2606.
- Wilkinson, M. D., Dumontier, M., Aalbersberg, I. J., et al. (2016). The FAIR Guiding Principles for scientific data management and stewardship. *Scientific Data*, 3, 160018.
- Chambers, C. D. (2013). Registered Reports: A new publishing initiative at Cortex. *Cortex*, 49(3), 609-610.
- Simonsohn, U. (2015). Small telescopes: Detectability and the evaluation of replication results. *Psychological Science*, 26(5), 559-569.
- Open Science Collaboration. (2015). Estimating the reproducibility of psychological science. *Science*, 349(6251), aac4716.
- Suber, P. (2012). *Open Access*. MIT Press.
- Stodden, V., Leisch, F., & Peng, R. D. (Eds.). (2014). *Implementing Reproducible Research*. CRC Press.
- Center for Open Science. (2026). *TOP Guidelines*. https://www.cos.io/initiatives/top-guidelines
- Creative Commons. (2026). *About CC Licenses*. https://creativecommons.org/licenses/
- FOSTER Open Science. (2026). *Open Science Training Handbook*. https://web.archive.org/web/2019/https://book.fosteropenscience.eu

Part of the AlterLab Academic Skills suite.
