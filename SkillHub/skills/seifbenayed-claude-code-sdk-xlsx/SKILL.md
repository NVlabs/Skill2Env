---
name: xlsx
description: "Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like \"the xlsx in my downloads\") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved."
allowed-tools: Spreadsheet,Read,Write,Glob,Grep
---

# Requirements for Outputs

## All Excel files

### Professional Font
- Use a consistent, professional font (e.g., Arial, Times New Roman) for all deliverables unless otherwise instructed by the user

### Zero Formula Errors
- Every Excel model MUST be delivered with ZERO formula errors (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?)
- **Always verify with**: `Spreadsheet { action: "check_errors", file_path: "output.xlsx" }`

### Preserve Existing Templates (when updating templates)
- Study and EXACTLY match existing format, style, and conventions when modifying files
- Never impose standardized formatting on files with established patterns
- Existing template conventions ALWAYS override these guidelines

## Financial models

### Color Coding Standards
Unless otherwise stated by the user or existing template

#### Industry-Standard Color Conventions
- **Blue text (RGB: 0,0,255)**: Hardcoded inputs, and numbers users will change for scenarios
- **Black text (RGB: 0,0,0)**: ALL formulas and calculations
- **Green text (RGB: 0,128,0)**: Links pulling from other worksheets within same workbook
- **Red text (RGB: 255,0,0)**: External links to other files
- **Yellow background (RGB: 255,255,0)**: Key assumptions needing attention or cells that need to be updated

### Number Formatting Standards

#### Required Format Rules
- **Years**: Format as text strings (e.g., "2024" not "2,024")
- **Currency**: Use $#,##0 format; ALWAYS specify units in headers ("Revenue ($mm)")
- **Zeros**: Use number formatting to make all zeros "-", including percentages (e.g., "$#,##0;($#,##0);-")
- **Percentages**: Default to 0.0% format (one decimal)
- **Multiples**: Format as 0.0x for valuation multiples (EV/EBITDA, P/E)
- **Negative numbers**: Use parentheses (123) not minus -123

### Formula Construction Rules

#### Assumptions Placement
- Place ALL assumptions (growth rates, margins, multiples, etc.) in separate assumption cells
- Use cell references instead of hardcoded values in formulas
- Example: Use =B5*(1+$B$6) instead of =B5*1.05

#### Formula Error Prevention
- Verify all cell references are correct
- Check for off-by-one errors in ranges
- Ensure consistent formulas across all projection periods
- Test with edge cases (zero values, negative numbers)
- Verify no unintended circular references

#### Documentation Requirements for Hardcodes
- Comment or in cells beside (if end of table). Format: "Source: [System/Document], [Date], [Specific Reference], [URL if applicable]"
- Examples:
  - "Source: Company 10-K, FY2024, Page 45, Revenue Note, [SEC EDGAR URL]"
  - "Source: Bloomberg Terminal, 8/15/2025, AAPL US Equity"

# Workflow

## Use the Spreadsheet tool for everything

The `Spreadsheet` tool handles ALL operations natively — no Python, no Bash, no dependencies.

### Available actions
- Reading: `inspect`, `list_sheets`, `get_sheet_info`, `read_range`
- Writing: `write_range`, `append_rows`, `set_cell` (supports formulas: `value: "=SUM(A1:A10)"`)
- Searching: `find_text`
- Validation: `check_errors`, `inspect_formulas`
- Formatting: `format_cells`, `set_column_width`
- Structure: `create`, `add_sheet`
- Export: `export_csv`

Do NOT use Python/Bash for spreadsheet operations. The Spreadsheet tool is the single source of truth.

## Common Workflows

### 1. Inspect an existing file
```
Spreadsheet { action: "inspect", file_path: "data.xlsx" }
Spreadsheet { action: "list_sheets", file_path: "data.xlsx" }
Spreadsheet { action: "read_range", file_path: "data.xlsx", sheet: "Summary", range: "A1:F20" }
```

### 2. Create a new workbook
```
Spreadsheet { action: "create", file_path: "output.xlsx", sheets: ["Summary", "Data", "Assumptions"] }
Spreadsheet { action: "write_range", file_path: "output.xlsx", sheet: "Summary", range: "A1", values: [["Revenue","Q1","Q2","Q3","Q4"],["Product A",100,120,130,150]] }
Spreadsheet { action: "format_cells", file_path: "output.xlsx", sheet: "Summary", range: "A1:E1", format: {"bold": true, "fill": "4472C4", "color": "FFFFFF"} }
Spreadsheet { action: "set_column_width", file_path: "output.xlsx", column: "A", width: 20 }
```

### 3. Edit existing data
```
Spreadsheet { action: "read_range", file_path: "model.xlsx", sheet: "Input" }
Spreadsheet { action: "set_cell", file_path: "model.xlsx", sheet: "Input", cell: "B5", value: "150000" }
Spreadsheet { action: "append_rows", file_path: "model.xlsx", sheet: "Data", rows: [["2026-Q1", 250, 180, 70]] }
```

### 4. Verify and fix errors
```
Spreadsheet { action: "check_errors", file_path: "output.xlsx" }
```

Returns:
```json
{
  "status": "success",
  "totalErrors": 0,
  "formulaCount": 42,
  "errorSummary": {}
}
```

Or if errors found:
```json
{
  "status": "errors_found",
  "totalErrors": 3,
  "formulaCount": 42,
  "errorSummary": {
    "#REF!": { "count": 2, "locations": ["Sheet1!B5", "Sheet1!C10"] },
    "#DIV/0!": { "count": 1, "locations": ["Sheet1!D15"] }
  }
}
```

Fix the identified errors and check again until `status: "success"`.

### 5. Search across sheets
```
Spreadsheet { action: "find_text", file_path: "report.xlsx", query: "revenue" }
```

### 6. Export to CSV
```
Spreadsheet { action: "export_csv", file_path: "data.xlsx", sheet: "Summary" }
```

### 7. Financial model with formulas
```
Spreadsheet { action: "create", file_path: "model.xlsx", sheets: ["Model"] }
Spreadsheet { action: "set_cell", file_path: "model.xlsx", sheet: "Model", cell: "A1", value: "Revenue" }
Spreadsheet { action: "set_cell", file_path: "model.xlsx", sheet: "Model", cell: "B1", value: "Q1" }
Spreadsheet { action: "format_cells", file_path: "model.xlsx", sheet: "Model", range: "A1:B1", format: {"bold": true} }
Spreadsheet { action: "set_cell", file_path: "model.xlsx", sheet: "Model", cell: "B2", value: "100" }
Spreadsheet { action: "set_cell", file_path: "model.xlsx", sheet: "Model", cell: "B3", value: "=B2*1.1" }
Spreadsheet { action: "set_cell", file_path: "model.xlsx", sheet: "Model", cell: "B4", value: "=SUM(B2:B3)" }
Spreadsheet { action: "check_errors", file_path: "model.xlsx" }
```

## Format Reference

### format_cells options
```json
{
  "bold": true,
  "italic": false,
  "color": "FF0000",
  "fill": "FFFF00",
  "numFmt": "$#,##0",
  "alignment": { "horizontal": "center", "vertical": "center" }
}
```

### Financial color coding via format_cells
```
// Blue inputs
Spreadsheet { action: "format_cells", file_path: "model.xlsx", range: "B5:B10", format: {"color": "0000FF"} }
// Yellow assumptions
Spreadsheet { action: "format_cells", file_path: "model.xlsx", range: "B2:B4", format: {"fill": "FFFF00"} }
// Bold headers
Spreadsheet { action: "format_cells", file_path: "model.xlsx", range: "A1:F1", format: {"bold": true, "fill": "4472C4", "color": "FFFFFF"} }
```

## Quick Reference

| Task | Tool |
|------|------|
| Read data | `Spreadsheet { action: "read_range" }` |
| Write values | `Spreadsheet { action: "write_range" }` or `set_cell` |
| Check errors | `Spreadsheet { action: "check_errors" }` |
| Format cells | `Spreadsheet { action: "format_cells" }` |
| Find text | `Spreadsheet { action: "find_text" }` |
| Create file | `Spreadsheet { action: "create" }` |
| Add sheet | `Spreadsheet { action: "add_sheet" }` |
| Column width | `Spreadsheet { action: "set_column_width" }` |
| Export CSV | `Spreadsheet { action: "export_csv" }` |
| See formulas | `Spreadsheet { action: "inspect_formulas" }` |
| Formulas | `Spreadsheet { action: "set_cell", value: "=..." }` |
