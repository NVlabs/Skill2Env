# Prerequisites by Skill

Check that required data files exist before proceeding. If any required file is missing, show the failure message and stop.

## Required Files

| File | setup | job-search | tailor-resume | cover-letter | network-scan | apply |
|------|:-----:|:----------:|:------------:|:------------:|:------------:|:-----:|
| `DATA_DIR/resume/*` | — | Required | Required | Required | Required | Required |
| `DATA_DIR/preferences.md` | — | Required | — | — | Required | — |
| `DATA_DIR/profile.md` | — | — | Recommended | Recommended | — | — |
| `DATA_DIR/linkedin-contacts.csv` | — | — | — | — | Required | — |
| `DATA_DIR/application-data.md` | — | — | — | — | — | Created if missing |

## Failure Messages

- **Resume missing**: "Run `/proficiently:setup` first to upload your resume."
- **Preferences missing**: "Run `/proficiently:setup` first to configure your resume and preferences."
- **LinkedIn contacts missing**: "No LinkedIn contacts found. Run `/proficiently:setup` and import your contacts first."
- **Profile missing (tailor-resume)**: Warn that the resume will be based only on resume text and may require more corrections. Recommend running `/proficiently:setup interview` first. Allow the user to proceed if they choose.
- **Profile missing (cover-letter)**: Warn that the cover letter will be based only on the resume. Recommend running `/proficiently:setup interview` first. Proceed anyway.
