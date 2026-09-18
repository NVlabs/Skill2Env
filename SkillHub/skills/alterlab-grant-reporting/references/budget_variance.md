# Budget-vs-Actual (Variance) Narratives

A variance narrative explains, category by category, why spending differs from the
approved budget. Funders read it to decide whether the award is on track, whether
a rebudgeting/virement is needed, and whether unspent funds justify a no-cost
extension. This file gives a reusable structure and worked examples. All amounts
and reasons must come from the user's own records — never invent figures.

## What a variance narrative must answer

For each budget category that is materially off plan:

1. **Planned vs actual** — the approved amount and the spent (or committed) amount.
2. **Variance** — absolute and percentage difference, and its direction
   (under-spend / over-spend).
3. **Reason** — the *programmatic* cause (a hire slipped, equipment came in under
   quote, a site visit was deferred, a subaward started late).
4. **Effect on the work** — did it delay or change any aim, milestone, or
   deliverable? If not, say so.
5. **Action** — what happens to the variance: absorbed within the category,
   moved via rebudgeting, or rolled forward (which may motivate an NCE — see
   `nce_rebudget.md`).

## Standard cost categories

Use the categories from the award's own budget. Common ones:

- **Personnel / Salaries & Wages** (and effort, in person-months)
- **Fringe benefits**
- **Equipment** (often a capitalization threshold applies)
- **Travel** (domestic / international)
- **Materials & Supplies / Consumables**
- **Subawards / Subcontracts**
- **Participant / trainee costs**
- **Other Direct Costs** (publication, computing, services)
- **Indirect / F&A (facilities & administrative) costs**

## Template (per category)

```
### {Category}
- Approved (this period): {amount}
- Actual / committed:    {amount}
- Variance:              {amount} ({+/- %}) — {under-/over-spend}
- Reason: {programmatic cause}
- Effect on aims/milestones: {none | which aim/milestone and how}
- Action: {absorb | rebudget to {category} | carry forward / request NCE}
```

## Worked example (illustrative — figures are placeholders)

> ### Personnel
> - Approved (Year 1): `[TODO: approved $]`
> - Actual: `[TODO: actual $]`
> - Variance: under-spend, because the postdoctoral researcher started in month 4
>   rather than month 1 (visa processing).
> - Effect on aims: Aim 2 data collection shifted by ~3 months; no aim dropped.
> - Action: the unspent salary is requested to carry forward to Year 2 to fund the
>   delayed data-collection period; this motivates a no-cost extension request
>   (see `nce_rebudget.md`).
>
> ### Equipment
> - Approved: `[TODO]` / Actual: `[TODO]`
> - Variance: under-spend; the flow cytometer was procured below the quoted price.
> - Effect on aims: none.
> - Action: residual reallocated to Materials & Supplies (within the funder's
>   rebudgeting authority — confirm threshold below).

## Funder-specific framing

- **NIH** — significant rebudgeting and changes in scope are reported in the RPPR
  **Section F (Changes)**; carryover and prior-approval requirements depend on
  whether the award is under expanded authorities / SNAP. Confirm against the
  Notice of Award.
- **NSF** — narrative belongs in the annual/final project report; certain
  reallocations and a single one-year NCE fall under the awardee's authority, with
  larger changes requiring NSF prior approval (confirm against PAPPG and the award
  conditions).
- **Horizon Europe / ERC** — actual costs are declared in the **Financial
  Statements**; deviations from the planned budget and use of resources are
  explained in the **Technical Report Part B**. Budget transfers between
  beneficiaries/categories are generally allowed if the action is carried out as
  described — confirm against the Grant Agreement.

> The exact prior-approval thresholds and rebudgeting authority differ per award
> and per program. State the rule generically and tell the user to confirm against
> their Notice of Award / Grant Agreement; do not assert a specific percentage
> threshold unless the user's award documents supply it.

## Self-check

- Does every off-plan category have a *reason*, not just a number?
- Is each variance tied to an effect (or an explicit "no effect") on the aims?
- Are all amounts the user's real figures or clearly-marked `[TODO]` placeholders?
- Do carry-forwards that need an extension cross-reference the NCE request?
