# Data Directory Resolution

All user data lives in a `.proficiently/` folder. Follow these steps to find it:

## Resolution Algorithm

1. Check the current working directory for `.proficiently/` — use it if found
2. Check `~/.proficiently/` — use it if found
3. If neither exists:
   - **setup skill**: this is a fresh setup — create it in Step 1
   - **all other skills**: tell the user to run `/proficiently:setup` first, then stop

## Ephemeral Session Warning

If no folder is selected (i.e. the working directory looks like an ephemeral session path such as `/sessions/...`), stop and tell the user:

> "Before we start, you need to select a folder so your data persists between sessions. Click 'Work in a folder' and select your home directory, then try again."

Do NOT proceed without a persistent folder.

## DATA_DIR Tree

All paths in skill instructions use `DATA_DIR` to mean whichever `.proficiently/` directory was found or created.

```
DATA_DIR/
  resume/              # Your resume PDF/DOCX
  preferences.md       # Job matching rules
  profile.md           # Work history from interview
  linkedin-contacts.csv # LinkedIn connections (optional)
  jobs/                # Per-job application folders
  job-history.md       # Running log from job-search
```
