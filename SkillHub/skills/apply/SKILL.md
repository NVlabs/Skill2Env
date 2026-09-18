---
name: apply
description: Fill out a job application on Greenhouse, Lever, or Workday
argument-hint: "job URL, 'last' to use most recent job, or 'current' to fill the active browser tab"
---

# Apply Skill

> **Priority hierarchy**: See `references/priority-hierarchy.md` for conflict resolution.

Fill out job application forms on Greenhouse, Lever, and Workday using browser automation.

## File Structure

```
scripts/
  fill-page.md              # Form-filling subagent prompt
```

## Data Directory

Resolve the data directory using `references/data-directory.md`.

---

## Workflow

### Step 0: Check Prerequisites

Resolve the data directory, then check prerequisites per `references/prerequisites.md`. Resume file is required. Load `DATA_DIR/application-data.md` if it exists (created in Step 2 if not).

### Step 1: Determine Target Job

Parse `$ARGUMENTS`:

**If a URL:**
- Check if a matching job folder exists in `DATA_DIR/jobs/` (match by company slug in folder name or by URL). If found, load `posting.md`, `resume.md`, `cover-letter.md` from that folder.
- If no match, set up browser per `references/browser-setup.md`, fetch the posting, save it to a new folder at `DATA_DIR/jobs/[company-slug]-[date]/posting.md`.

**If "last" or empty:**
- Find the most recently modified job folder in `DATA_DIR/jobs/`
- Load its `posting.md`, `resume.md`, `cover-letter.md`
- Confirm with the user which job this is for

**If "current":**
- Skip navigation — will use the current browser tab as-is
- Match the tab's URL against saved job folders to load context if possible

Report what's loaded:

```
Applying to [Role] at [Company].
```

### Step 2: Build/Load Application Data

If `DATA_DIR/application-data.md` exists, read it and load the values.

If it does NOT exist:
1. Extract what you can from the resume: name, email, phone, LinkedIn, location
2. Present extracted data to the user. Ask them to confirm and fill in gaps: work authorization, visa sponsorship, EEO preferences (default all EEO to "Decline to self-identify")
3. Save to `DATA_DIR/application-data.md` using this format:

```markdown
# Application Data

## Personal Information
- First Name: ...
- Last Name: ...
- Email: ...
- Phone: ...
- City: ...
- Country: United States

## Online Profiles
- LinkedIn: ...
- GitHub: ...
- Portfolio: ...

## Standard Answers
- How did you hear about us: Job Board
- Previously worked at this company: No
- Authorized to work in the US: Yes
- Requires visa sponsorship: No

## EEO / Voluntary Disclosures
- Gender: Decline to self-identify
- Race/Ethnicity: Decline to self-identify
- Veteran status: I am not a veteran
- Disability: I don't wish to answer
```

### Step 3: Navigate to Application Form and Scout Requirements

Set up browser per `references/browser-setup.md` (`tabs_context` → `tabs_create` → `navigate`).

**If `$ARGUMENTS` is "current"**: Skip navigation. Call `tabs_context_mcp` to get the active tab.

**Otherwise**, detect ATS type from URL patterns (see `references/ats-patterns.md`) and navigate accordingly:

**Lever** (`jobs.lever.co/...`):
- Navigate to the posting URL with `/apply` appended, or navigate to the posting and click "APPLY FOR THIS JOB"

**Greenhouse** (`boards.greenhouse.io/...` or page with `grnhse_iframe`):
- Navigate to the posting URL
- Extract iframe tokens via `javascript_tool`:
  ```javascript
  const iframe = document.getElementById('grnhse_iframe');
  const url = new URL(iframe.src);
  JSON.stringify({
    boardToken: url.searchParams.get('for'),
    jobToken: url.searchParams.get('token')
  });
  ```
- Navigate to direct form URL: `https://job-boards.greenhouse.io/embed/job_app?for={boardToken}&token={jobToken}`

**Workday** (`*.myworkdayjobs.com/...`):
- Navigate to the posting. Click "Apply Now".
- If a landing page appears with Autofill/Manual options, click "Apply Manually".
- If an auth gate appears, **tell the user to sign in, then say "continue" when ready**. Account creation is a prohibited action — the user must handle authentication themselves.

**Unknown ATS**:
- Navigate to the URL, take a screenshot
- Attempt to identify the form. If unrecognizable, tell the user and ask for guidance.

**Scout the form.** Once on the application form, do a quick scan (`read_page(filter="interactive")` or scroll through for Workday) to determine:
- Does the form have a **resume/CV upload** field?
- Does the form have a **cover letter** upload or text field?
- Are there any **unusual required fields** that need special attention?

Record these requirements — they determine what materials to generate in Step 4.

### Step 4: Generate Missing Materials

The goal is to have everything ready before filling, so the user does minimal work.

**Always tailor the resume.** Check if `DATA_DIR/jobs/[job-folder]/resume.md` exists for this job:
- If YES: the resume is already tailored for this role. Skip.
- If NO: Run the tailor-resume skill inline. Follow the workflow in `skills/tailor-resume/SKILL.md` — use the job posting (already loaded), the original resume, and the work history profile to generate a tailored resume. Save to the job folder. Present it to the user for quick review before continuing.

**Generate a cover letter only if the form requires one.** If the scout in Step 3 found a cover letter field:
- Check if `DATA_DIR/jobs/[job-folder]/cover-letter.md` exists
- If YES: already done. Skip.
- If NO: Run the cover-letter skill inline. Follow the workflow in `skills/cover-letter/SKILL.md` — use the posting, tailored resume, and profile. Save to the job folder. Present it for quick review.

**If the form doesn't have a cover letter field**, skip cover letter generation entirely.

Tell the user what was generated:

```
Prepared for [Role] at [Company]:
- Tailored resume: [generated / already existed]
- Cover letter: [generated / already existed / not required by form]

Ready to fill the application. Proceeding...
```

### Step 5: Scan All Fields

Before filling anything, scan the entire form to discover every field. Do NOT fill fields during this step — read only.

**For Lever/Greenhouse (single-page forms):**
- Call `read_page(tabId, filter="interactive")` to get all fields at once

**For Workday (multi-step wizard):**
- Scan the current page by scrolling top-to-bottom, calling `read_page` at each viewport position
- Collect all field labels, types, and whether they're required
- Note: you'll scan each wizard page as you reach it (see Step 7)

**For each field found**, record:
- Field label
- Field type (text, dropdown, radio, checkbox, file upload)
- Whether it's required
- The element ref for later filling

### Step 6: Propose Answers and Get Approval

Generate a proposed answer for every field using this priority:
1. **Application data** — match from `application-data.md` per the Field Matching Reference below
2. **Reasonable defaults** — for common fields not in application data:
   - Legal First/Last Name → same as First/Last Name
   - Electronic signature → full name
   - Arbitration/terms agreements → Accept (note to user)
   - Interview process acknowledgments → Accept
   - AI transcription consent → Accept
   - Contract/temp work questions → "No" (unless application data says otherwise)
3. **Custom Answers** — check the "Custom Answers" section of `application-data.md` for previously cached answers
4. **Best guess** — for any remaining fields, generate a reasonable answer based on the field label and job context
5. **Cannot determine** — only if truly ambiguous and no reasonable default exists

Present ONE consolidated summary to the user:

```
Here's my plan for the [Company] application:

**Auto-fill from your data:**
- First Name: Jane
- Last Name: Doe
- Email: jane@example.com
- Phone: 555-0123
- LinkedIn: https://linkedin.com/in/janedoe
...

**Proposed answers (please review):**
- Legal First Name: Jane (same as first name)
- Electronic signature: Jane Doe
- Arbitration agreement: Accept
- Contract work: No
- [Any other non-obvious fields]: [proposed answer]

**Needs your input:**
- [Only truly ambiguous fields, if any]

**Manual upload needed:**
- Resume: [file path]
- Cover letter: [file path] (if applicable)

Approve and I'll fill everything in. Or tell me what to change.
```

**Key principle:** Ask once, fill once. Do not interrupt with per-field questions. The only user interaction should be this single approval (plus the final submit confirmation in Step 8).

After the user approves (with any edits), cache any new answers in `DATA_DIR/application-data.md` under a "Custom Answers" section so they're reused on future applications.

### Step 7: Fill Form

After approval, fill everything in one pass.

**Delegate to the subagent.** Invoke `scripts/fill-page.md` with:
- ATS type (lever/greenhouse/workday/unknown)
- The approved field→value mapping (all answers, not just application data)
- Tab ID
- File paths for resume and cover letter uploads

The subagent fills all fields on the current page, then returns what was filled and what remains.

**For multi-page forms (Workday):**
1. Fill current page → click "Save and Continue"
2. If validation errors: read the errors, fix the fields, retry
3. On the new page: scan fields (Step 5 logic), match against the approved answers, fill, advance
4. Repeat until reaching the review page

**File upload handling:**
MCP tools can only upload images via `upload_image`. For PDF/DOCX resume and cover letter uploads, tell the user the file path and ask them to upload manually. This is a known limitation — include the path in the Step 6 summary so the user can upload while reviewing.

### Step 8: Review Before Submit

When a review/confirmation page is reached or all fields on a single-page form are filled:

1. Take a screenshot
2. Confirm everything looks correct
3. **Ask the user for explicit confirmation before submitting** — this is a required explicit-permission action per browser automation rules

Do NOT click Submit/Send until the user confirms.

### Step 9: Log the Application

After submission (or if the user decides not to submit):

Create `DATA_DIR/jobs/[company-slug]-[date]/applied.md`:

```markdown
# Application Log

- **Date**: YYYY-MM-DD
- **ATS**: Greenhouse/Lever/Workday
- **Status**: Submitted / Draft (not submitted)
- **Notes**: [any relevant notes]
```

Update `DATA_DIR/job-history.md` — find the entry for this job and append the application status and date.

Present to user:

```
Applied to [Role] at [Company] on [date].
Files saved to: DATA_DIR/jobs/[folder]/

```

---

## Field Matching Reference

Match form field labels (case-insensitive, fuzzy) to application data:

| Label pattern | Data source | Input method |
|---------------|-------------|--------------|
| `first name` | Personal.FirstName | form_input / type |
| `last name` | Personal.LastName | form_input / type |
| `full name` | Personal.FirstName + LastName | form_input / type |
| `email` | Personal.Email | form_input / type |
| `phone` | Personal.Phone | form_input / type |
| `city`, `location`, `current location` | Personal.City | form_input / type / combobox |
| `country` | Personal.Country | dropdown selection |
| `linkedin` | Profiles.LinkedIn | form_input / type |
| `github` | Profiles.GitHub | form_input / type |
| `portfolio`, `website` | Profiles.Portfolio | form_input / type |
| `resume`, `cv` | File upload: resume PDF | file upload |
| `cover letter` | File upload: cover letter | file upload |
| `how did you hear` | StandardAnswers.HowHeard | dropdown: "Job Board" |
| `previously worked` | StandardAnswers.PreviouslyWorked | radio/checkbox: "No" |
| `authorized to work`, `work authorization` | StandardAnswers.WorkAuth | radio/dropdown |
| `sponsorship` | StandardAnswers.Sponsorship | radio/dropdown |
| `gender` | EEO.Gender | dropdown: "Decline" |
| `race`, `ethnicity` | EEO.Race | dropdown: "Decline" |
| `veteran` | EEO.Veteran | dropdown/radio: decline option |
| `disability` | EEO.Disability | dropdown/radio: decline option |

**Unrecognized fields**: Check if required. If required, ask the user. If optional, skip. Cache user answers in `DATA_DIR/application-data.md` under "Custom Answers" for reuse.

---

## ATS-Specific Interaction Notes

**Lever**: `form_input` with value or text works directly for all field types including dropdowns.

**Greenhouse**: `form_input` with value works after navigating to the direct form URL (outside the iframe).

**Workday**:
- `read_page(filter="interactive")` only returns viewport-visible elements. Must scroll top-to-bottom, calling `read_page` at each scroll position.
- Radio buttons are NOT returned by `read_page` — use `find` tool or `computer` click at coordinates.
- Dropdowns are `button` elements that open popup panels. Click the button → use `find` or `read_page` to locate options → click the option. For hierarchical dropdowns (like "How Did You Hear"), search within the popup using the Search textbox.

---

## Response Format

Structure user-facing output with these sections:

1. **Application Status** — what was filled, what was skipped, confirmation of submission
2. **Files Saved** — paths to any saved application logs
3. **Next Steps** — suggest cover letter if missing, or next job search

