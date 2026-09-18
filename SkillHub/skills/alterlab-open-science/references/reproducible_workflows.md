# Reproducible Workflows — Containers, Environments, and Software Citation

Container recipes, environment specifications, code best practices, and software-citation metadata, extracted from the Open Science Practices skill body.

## Docker for reproducible research

```dockerfile
# Dockerfile for a reproducible R analysis
FROM rocker/tidyverse:4.3.0

# Install additional R packages
RUN install2.r --error lme4 brms papaja here

# Copy analysis files
COPY . /home/rstudio/project
WORKDIR /home/rstudio/project

# Run the analysis
CMD ["Rscript", "analysis/main.R"]
```

## Binder for interactive reproducibility

Binder (mybinder.org) takes a GitHub repository with an environment.yml (Python) or install.R (R) file and creates a live, interactive Jupyter or RStudio environment that anyone can use without installing anything.

### Example: environment.yml for Binder

```yaml
name: my-research-env
channels:
  - conda-forge
  - nodefaults  # avoid Anaconda's `defaults` channel: its ToS can require a
                # paid license for larger orgs and for mirroring/embedding.
                # conda-forge is community-maintained and free for any use.
dependencies:
  - python=3.11
  - numpy=1.26
  - pandas=2.1
  - scipy=1.11
  - matplotlib=3.8
  - seaborn=0.13
  - statsmodels=0.14
  - jupyterlab=4.0
  - pip:
    - pingouin==0.5.3
```

Pin exact versions (not floating ranges) so the environment rebuilds identically. Generate the file from a working env with `conda env export --from-history -f environment.yml` to avoid OS-specific packages that break on Binder.

**Code Ocean:** A commercial platform that provides guaranteed computational reproducibility with a published DOI for each "compute capsule." Used by journals including Nature for results verification.

## Best practices for reproducible code

1. Use relative paths (never absolute paths like /Users/yourname/data/)
2. Set random seeds for any stochastic process
3. Use a package manager (renv for R, conda/pip for Python)
4. Record the session info (sessionInfo() in R, pip freeze in Python)
5. Automate the entire pipeline (Makefile, Snakemake, targets)
6. Use version control (git) from the start
7. Write a README that explains how to run the analysis
8. Test on a clean machine before sharing

## Example: CITATION.cff

```yaml
cff-version: 1.2.0
message: "If you use this software, please cite it as below."
authors:
  - family-names: "Martinez"
    given-names: "Rosa"
    orcid: "https://orcid.org/0000-0002-1234-5678"
title: "PyRetention: A Python Package for Learning Retention Analysis"
version: 2.1.0
doi: 10.5281/zenodo.1234567
date-released: 2025-09-15
url: "https://github.com/martinez-lab/pyretention"
license: MIT
```
