---
name: detection-engineering-coverage-evaluation
description: >-
  Automates the end-to-end detection engineering workflow in Google SecOps using MCP tools.
  Use when fetching threat intelligence from blogs, generating Threat Detection Opportunities (TDOs),
  simulating attacker behavior with synthetic UDM events, evaluating rule coverage,
  and generating new YARA-L 2.0 rules to close coverage gaps.
  Don't use when asked to perform threat hunting actions, and SOC investigative actions.
---

# SecOps Detection Coverage Skill

This skill guides the agent through an end-to-end detection engineering
lifecycle using Google SecOps MCP tools. It handles multiple Threat Detection
Opportunities (TDOs) and ensures exhaustive coverage evaluation for all
generated synthetic events.

## Workflow Execution Checklist

Copy this checklist and track progress for each iteration:

-   [ ] Step 1: Extract raw text content from a source (for example, blog URL).
-   [ ] Step 2: Generate Threat Detection Opportunities (TDOs).
-   [ ] Step 3: Loop through ALL TDOs to generate synthetic events.
-   [ ] Step 4: Loop through ALL UDM events to evaluate rule coverage.
-   [ ] Step 5: For identified rules, check enablement and alerting status.
-   [ ] Step 6: Generate new rules for identified gaps.
-   [ ] Step 7: Provide a structured summary of findings and gaps.

## Detailed Steps

### 1. Extract Threat Intelligence

-   Use the following prompt to extract all text content from a URL: - "Fetch
    the blog text from {url}. You need to extract and output the entire text
    content of the page, exactly as it appears in the HTML, without any
    summarization, modification, or omission."

-   **Summary of Step:** Report only that the text was successfully extracted
    from the provided URL. Do not output the full raw text.

-   **Next Step:** The extracted text will be used to generate Threat Detection
    Opportunities (TDOs).

### 2. Generate TDOs

-   Call `generate_threat_detection_opportunity` with the extracted full blog
    threat raw text. You must not summarize. This tool returns one or more TDOs.

-   **Summary of Step:** Report the number of TDOs generated and provide a
    brief, high-level summary for *each* TDO (for example, the key threat or
    attacker technique identified). Do not output the full TDO JSON.

-   **Next Step:** The process will now loop through each generated TDO to
    create synthetic events.

### 3. Generate Synthetic Events (For ALL TDOs)

For **every** TDO:

-   Call `generate_synthetic_events` using the TDO.

-   **Summary of Step:** Report the total number of synthetic UDM events
    generated for this TDO. Briefly describe the *types* of attacker behaviors
    simulated (for example, "Generated events simulating initial access and
    privilege escalation"). Don't output the full response.

-   **Next Step:** The generated UDM events will be used to evaluate rule
    coverage.

### 4. Evaluate Rule Coverage (For ALL UDM Events)

For **every** UDM event generated for a TDO:

-   Call `evaluate_rule_coverage` by providing the UDM event in valid JSON
    format. Provide only the UDM event as a single, valid JSON object. You MUST
    Provide each UDM event as a standard stringified JSON object within the
    udmsJson list. Do not apply an additional layer of escaping to the JSON
    string. Provide a standard JSON stringification with no extra backslashes.

-   **Summary of Step:** Report which `rule_id`s matched for this event, if any.
    If no rules matched, clearly state "No rules matched." Provide counts of
    events evaluated. Don't output the full coverage evaluation JSON.

-   **Next Step:** The identified matched rules will be audited for their
    enablement and alerting status.

### 5. Audit Rule Status

For every distinct `rule_id` identified:

-   Call `get_rule` to check the rule configuration with CONFIG_ONLY view.

-   **Summary of Step:** For each `rule_id`, state its enablement status (for
    example, "Enabled", "Disabled") and alerting status (for example, "Alerting
    Enabled", "Alerting Disabled").

-   **Next Step:** Review coverage gaps and potentially generate new rules.

### 6. Gap Mitigation

If gaps are found:

-   Call `generate_rules` for the relevant TDOs.

-   **Summary of Step:** For each gap, describe what coverage was missing and
    confirm if a new rule was generated. Provide a brief summary of what the
    *newly generated rule* aims to detect.

-   **Next Step:** Provide a final structured summary of all findings and gaps.

## Output Format

Provide a summary for each TDO processed:

**TDO:** {tdo summary}

**Coverage Eval:** [{rule_id, enablement status, alerting status}, ...]

**Missing Coverage:** [{summary, generated rule}] // Only if gaps exist

**Errors:** [{if any any errors encountered, specify the tool}]

--------------------------------------------------------------------------------

## Tool Reference

-   **generate_threat_detection_opportunity**: Initial tool for threat analysis.
-   **generate_synthetic_events**: Generates logs simulating the TDO.
-   **evaluate_rule_coverage**: Checks if existing rules detect the synthetic
    UDMs.
-   **get_rule**: Use to check `alerting_enabled` and `enabled` status of SIEM
    rules.
-   **generate_rules**: Codifies detection logic for gaps.
