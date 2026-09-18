# Data Sharing Checklist and DMP Example

The full practical data-sharing checklist and a worked data management plan (DMP) excerpt, extracted from the Open Science Practices skill body.

## Practical data sharing checklist

```
Before sharing:
[ ] Remove or anonymize personally identifiable information (PII)
[ ] Check IRB/ethics approval covers data sharing
[ ] Verify no proprietary restrictions from data providers
[ ] Clean variable names and remove internal codes
[ ] Create a comprehensive codebook/data dictionary

Preparing the deposit:
[ ] Choose appropriate file formats (CSV over XLSX, open formats preferred)
[ ] Write a README describing the dataset structure
[ ] Create a data dictionary with all variable definitions
[ ] Include analysis scripts that reproduce published results
[ ] Add a LICENSE file (CC-BY 4.0 recommended for data)
[ ] Include the study preregistration link if applicable

Depositing:
[ ] Upload to a persistent repository (Zenodo, Dryad, Figshare, or domain-specific)
[ ] Obtain a DOI
[ ] Set an embargo period if needed (e.g., until publication)
[ ] Link the dataset DOI to the paper DOI
[ ] Add the data availability statement to the manuscript
```

## Example: DMP excerpt

```
Data Types: This project will generate three primary data types:
(1) survey responses from approximately 500 participants (Qualtrics,
exported as CSV), (2) semi-structured interview transcripts from 30
participants (audio recordings transcribed to text), and (3) behavioral
log data from the learning platform (JSON format, approximately 2GB).

Sharing Plan: De-identified survey and behavioral data will be deposited
in the ICPSR data repository within 12 months of the project end date
and assigned a DOI. Interview transcripts will be shared in redacted
form, with participant consent for sharing obtained during recruitment.
Audio recordings will not be shared due to re-identification risk.

Standards: Survey data will follow DDI (Data Documentation Initiative)
metadata standards. Variable names will use the codebook published with
our validated instrument (Martinez et al., 2024). All dates will use
ISO 8601 format.
```

## DMP tools

- DMPTool (dmptool.org) -- US-focused, funder-specific templates
- DMPonline (dmponline.dcc.ac.uk) -- UK/EU-focused
- ARGOS (argos.openaire.eu) -- EU OpenAIRE aligned
