"""Evidence and numeric integrity checks shared by stage validators."""

import os
import re
from html import unescape
from datetime import date


STALE_SOURCE_DAYS = 730

DUE_DILIGENCE_TERMS = (
    "due diligence",
    "m&a",
    "merger",
    "acquisition",
    "target screening",
    "corporate screening",
    "company background",
    "target company",
    "supplier screening",
    "supplier background",
    "\u5c3d\u8c03",
    "\u5c3d\u804c\u8c03\u67e5",
    "\u4f01\u4e1a\u5c3d\u8c03",
    "\u5e76\u8d2d",
    "\u6536\u8d2d",
    "\u6807\u7684\u7b5b\u9009",
    "\u6807\u7684\u7814\u7a76",
    "\u6807\u7684\u516c\u53f8",
    "\u516c\u53f8\u80cc\u8c03",
    "\u4f9b\u5e94\u5546\u80cc\u8c03",
    "\u4f9b\u5e94\u5546\u5ba1\u67e5",
)

PRIMARY_PLAN_LABEL_TERMS = (
    "primary-source plan",
    "primary source plan",
    "primary_source_plan",
    "\u4e00\u624b\u6e90\u8ba1\u5212",
    "\u4e00\u624b\u6765\u6e90\u8ba1\u5212",
)

PRIMARY_PATH_TERMS = (
    "primary source",
    "primary-source",
    "primary_source",
    "official registry",
    "official register",
    "national register",
    "company registry",
    "regulatory filing",
    "regulatory record",
    "company disclosure",
    "court record",
    "sec filing",
    "\u4e00\u624b\u6e90",
    "\u4e00\u624b\u6765\u6e90",
    "\u5b98\u65b9\u767b\u8bb0\u6e90",
    "\u5b98\u65b9\u6765\u6e90",
    "\u5de5\u5546\u767b\u8bb0",
    "\u76d1\u7ba1\u5907\u6848",
    "\u76d1\u7ba1\u8bb0\u5f55",
    "\u4f01\u4e1a\u516c\u544a",
    "\u516c\u53f8\u62ab\u9732",
    "\u6cd5\u9662\u8bb0\u5f55",
    "\u539f\u59cb\u5907\u6848",
)

PRIMARY_CONCRETE_PATH_TERMS = tuple(
    term for term in PRIMARY_PATH_TERMS
    if term not in {"primary source", "primary-source", "primary_source", "\u4e00\u624b\u6e90", "\u4e00\u624b\u6765\u6e90"}
)

PRIMARY_NEGATION_PATTERN = re.compile(
    r"(no|without|missing|lack(?:ing)?|unavailable)\s+.{0,40}primary[- ]source|"
    r"primary[- ]source\s+.{0,40}(missing|unavailable|not found|absent)|"
    r"(\u65e0|\u6ca1\u6709|\u7f3a\u5c11|\u672a\u627e\u5230).{0,20}(\u4e00\u624b\u6e90|\u4e00\u624b\u6765\u6e90|\u5b98\u65b9\u6765\u6e90|\u5b98\u65b9\u767b\u8bb0\u6e90|\u76d1\u7ba1\u5907\u6848|\u516c\u53f8\u62ab\u9732)",
    re.IGNORECASE,
)

PRIMARY_SOURCE_TYPES = {
    "primary",
    "official",
    "official registry",
    "official_registry",
    "regulator",
    "regulatory",
    "regulatory_filing",
    "regulatory_record",
    "company_disclosure",
    "company disclosure",
    "company_registry",
    "filing",
    "court",
    "court_record",
}

AGGREGATED_SOURCE_TYPES = {
    "aggregator",
    "media",
    "third_party_summary",
    "third-party summary",
    "third party summary",
    "report_aggregator",
    "report aggregator",
    "summary",
}

ENTITY_CLAIM_TYPES = {
    "entity",
    "relationship",
    "filing",
    "litigation",
    "license",
    "officer",
    "ownership",
    "parent_status",
}


def _read(workspace, filename):
    path = os.path.join(workspace, filename)
    if not os.path.isfile(path):
        return ""
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def _lower(value):
    return (value or "").strip().lower()


def _truthy(value):
    return _lower(value) in {"true", "yes", "y", "1", "present", "\u662f", "\u6709"}


def _has_any(text, terms):
    lowered = text.lower()
    return any(term.lower() in lowered for term in terms)


def _has_primary_source_plan(text):
    has_label = _has_any(text, PRIMARY_PLAN_LABEL_TERMS)
    if not has_label:
        return False
    if _has_any(text, PRIMARY_CONCRETE_PATH_TERMS):
        return True
    if PRIMARY_NEGATION_PATTERN.search(text):
        return False
    return _has_any(text, PRIMARY_PATH_TERMS)


def _field_map(block):
    fields = {}
    for match in re.finditer(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*?)\s*$", block, re.MULTILINE):
        fields[match.group(1).lower()] = match.group(2).strip()
    return fields


def _claim_blocks(text):
    blocks = []
    for match in re.finditer(r"(?ms)^\s*claim_id\s*:\s*.*?(?=^\s*claim_id\s*:|\Z)", text):
        fields = _field_map(match.group(0))
        if fields:
            blocks.append(fields)
    return blocks


def _parse_iso_date(value):
    try:
        return date.fromisoformat((value or "").strip()[:10])
    except (TypeError, ValueError):
        return None


def _source_age_days(source_date):
    parsed = _parse_iso_date(source_date)
    if parsed is None:
        return None
    return (date.today() - parsed).days


def _report_id_refs(text, keys):
    refs = set()
    key_pattern = "|".join(re.escape(key) for key in keys)
    pattern = re.compile(
        rf"(?is)(?:{key_pattern})\s*(?:=|:)\s*(\"[^\"]+\"|'[^']+'|\[[^\]]+\]|[A-Za-z0-9_.:-]+)"
    )
    for match in pattern.finditer(text):
        snippet = match.group(1)
        refs.update(re.findall(r"\b[A-Za-z][A-Za-z0-9_]*-\d{2,}\b", snippet))
    return refs


def _html_attrs(tag):
    attrs = {}
    for match in re.finditer(r"([A-Za-z_:][-A-Za-z0-9_:.]*)\s*=\s*(\"[^\"]*\"|'[^']*')", tag):
        attrs[match.group(1).lower()] = unescape(match.group(2)[1:-1]).strip()
    return attrs


def _claim_refs(value):
    return set(re.findall(r"\b[A-Za-z][A-Za-z0-9_]*-\d{2,}\b", value or ""))


def _normalize_number(value):
    text = (value or "").strip().replace(",", "")
    match = re.search(r"[-+]?\d+(?:\.\d+)?", text)
    if not match:
        return None
    try:
        return float(match.group(0))
    except ValueError:
        return None


def _numbers_match(left, right):
    left_num = _normalize_number(left)
    right_num = _normalize_number(right)
    if left_num is None or right_num is None:
        return False
    tolerance = max(1e-9, abs(left_num) * 1e-6)
    return abs(left_num - right_num) <= tolerance


def _normalize_dimension(value):
    return re.sub(r"\s+", " ", (value or "").strip().lower())


def _chart_tags(text):
    for match in re.finditer(r"(?is)<[A-Za-z][^>]*\bdata-claim-id\s*=\s*(?:\"[^\"]*\"|'[^']*')[^>]*>", text):
        tag = match.group(0)
        attrs = _html_attrs(tag)
        chart_id = attrs.get("id", "")
        class_name = attrs.get("class", "")
        if chart_id and (
            "chart" in chart_id.lower()
            or "chart" in class_name.lower()
            or re.search(rf"getElementById\((?:'|\"){re.escape(chart_id)}(?:'|\")\)", text)
        ):
            yield attrs


def _chart_data_numbers(text, chart_id):
    if not chart_id:
        return []
    id_pattern = rf"getElementById\((?:'|\"){re.escape(chart_id)}(?:'|\")\)"
    match = re.search(id_pattern, text)
    if not match:
        return []
    snippet = text[match.end():]
    next_chart = re.search(r"echarts\.init\s*\(", snippet)
    if next_chart:
        snippet = snippet[: next_chart.start()]
    end_script = snippet.find("</script>")
    if end_script >= 0:
        snippet = snippet[:end_script]

    numbers = []
    for data_match in re.finditer(r"(?is)(?:\"data\"|(?<!\")\bdata)\s*:\s*\[([^\]]*)\]", snippet):
        values = data_match.group(1)
        numbers.extend(re.findall(r"[-+]?\d+(?:\.\d+)?", values.replace(",", "")))
    return numbers


def _validate_chart_claim_consistency(r, report_text, claims):
    claim_by_id = {fields.get("claim_id"): fields for fields in claims if fields.get("claim_id")}
    for attrs in _chart_tags(report_text):
        chart_id = attrs.get("id", "<unknown-chart>")
        chart_numbers = _chart_data_numbers(report_text, chart_id)
        for claim_id in sorted(_claim_refs(attrs.get("data-claim-id", ""))):
            fields = claim_by_id.get(claim_id)
            if not fields or not _is_numeric_claim(fields):
                continue

            ledger_value = fields.get("value")
            if ledger_value:
                explicit_value = attrs.get("data-value") or attrs.get("data-claim-value")
                if explicit_value and not _numbers_match(explicit_value, ledger_value):
                    r.fail(f"Chart {chart_id} claim {claim_id} value mismatch: report={explicit_value}, ledger={ledger_value}")
                elif not explicit_value and chart_numbers and not any(_numbers_match(num, ledger_value) for num in chart_numbers):
                    r.fail(f"Chart {chart_id} claim {claim_id} value missing from chart data: ledger={ledger_value}")

            for field_name, attr_name in (
                ("unit", "data-unit"),
                ("currency", "data-currency"),
                ("period", "data-period"),
            ):
                ledger_value = fields.get(field_name)
                report_value = attrs.get(attr_name)
                if ledger_value and report_value and _normalize_dimension(report_value) != _normalize_dimension(ledger_value):
                    r.fail(
                        f"Chart {chart_id} claim {claim_id} {field_name} mismatch: "
                        f"report={report_value}, ledger={ledger_value}"
                    )


def _used_in(fields, target):
    return target in _lower(fields.get("used_in"))


def _is_numeric_claim(fields):
    claim_type = _lower(fields.get("claim_type"))
    return claim_type == "numeric" or bool(fields.get("value"))


def _is_primary_source_type(source_type):
    normalized = _lower(source_type).replace("-", "_")
    return normalized in PRIMARY_SOURCE_TYPES or source_type in PRIMARY_SOURCE_TYPES


def _is_aggregated_source_type(source_type):
    normalized = _lower(source_type).replace("-", "_")
    return normalized in AGGREGATED_SOURCE_TYPES or source_type in AGGREGATED_SOURCE_TYPES


def validate_stage3_plan(r, workspace, filename="research_plan.md"):
    text = _read(workspace, filename)
    if not text or not _has_any(text, DUE_DILIGENCE_TERMS):
        return
    if _has_primary_source_plan(text):
        r.pass_check("due-diligence/target-screening primary-source plan declared")
    else:
        r.fail("due-diligence/target-screening lacks a primary-source plan; declare official registry/regulatory filing/company disclosure paths")


def validate_evidence_base(r, workspace, filename="evidence_base.md"):
    text = _read(workspace, filename)
    if not text:
        return

    claims = _claim_blocks(text)
    has_key_claim_signal = bool(re.search(
        r"headline|chart|\u5173\u952e\u6570\u5b57|\u56fe\u8868|\u5e02\u573a\u89c4\u6a21|market size|\u589e\u957f\u7387|growth rate|"
        r"\u4efd\u989d|share|\u6536\u5165|revenue|gmv|\u4ebf\u5143|\u4ebf|billion|million|%|"
        r"recommendation|strategic recommendation|\u5173\u952e\u5efa\u8bae|\u6218\u7565\u5efa\u8bae|\u884c\u52a8\u5efa\u8bae|\u5efa\u8bae\u652f\u6491",
        text,
        re.IGNORECASE,
    ))

    if "Evidence Claim Ledger" in text and not claims:
        r.fail("Evidence Claim Ledger heading detected but no claim_id field found")
        return
    if not claims and has_key_claim_signal:
        r.fail("key numbers/charts/recommendation evidence lacks Evidence Claim Ledger claim_id fields")
        return
    if not claims:
        r.warn("Evidence Claim Ledger claim_id fields not detected; register core numeric/entity claims structurally")
        return

    r.pass_check(f"Evidence Claim Ledger entries: {len(claims)}")

    claim_origin_groups = {}
    for fields in claims:
        claim_id = fields.get("claim_id", "<unknown>")
        claim_type = _lower(fields.get("claim_type"))
        source_type = _lower(fields.get("source_type"))
        source_grade = _lower(fields.get("source_grade"))
        primary_required = _truthy(fields.get("primary_source_required"))
        primary_present = _truthy(fields.get("primary_source_present")) or _is_primary_source_type(source_type)
        used_for_headline_or_chart = _used_in(fields, "headline") or _used_in(fields, "chart")

        if primary_required and not primary_present:
            r.fail(f"{claim_id} requires primary source but primary_source_present is false")

        if claim_type in ENTITY_CLAIM_TYPES and _is_aggregated_source_type(source_type) and not primary_present:
            r.fail(f"{claim_id} entity/filing claim uses aggregated source without primary source")

        if (_is_numeric_claim(fields) or used_for_headline_or_chart) and used_for_headline_or_chart:
            if not fields.get("source_date"):
                r.fail(f"{claim_id} headline/chart claim missing source_date")
            if not fields.get("retrieved_at"):
                r.warn(f"{claim_id} headline/chart claim missing retrieved_at")
            age_days = _source_age_days(fields.get("source_date"))
            if age_days is not None and age_days > STALE_SOURCE_DAYS:
                r.warn(f"{claim_id} headline/chart claim source_date is stale ({age_days} days old)")

        if _is_numeric_claim(fields):
            missing = [name for name in ("unit", "period") if not fields.get(name)]
            value_text = " ".join([fields.get("value", ""), fields.get("claim_text", "")]).lower()
            if any(token in value_text for token in ("rmb", "usd", "$", "¥", "RMB", "USD")) and not fields.get("currency"):
                missing.append("currency")
            if missing:
                r.warn(f"{claim_id} numeric claim missing {', '.join(missing)}")

        if source_grade in {"a", "b"} and _is_aggregated_source_type(source_type) and not fields.get("origin_id"):
            r.warn(f"{claim_id} A/B graded aggregated source lacks origin_id — source laundering risk")

        key = re.sub(r"\s+", " ", _lower(fields.get("claim_text")))
        origin = _lower(fields.get("origin_id"))
        if key and _is_aggregated_source_type(source_type):
            claim_origin_groups.setdefault(key, []).append((claim_id, origin))

    for claim_text, entries in claim_origin_groups.items():
        origins = [origin for _, origin in entries if origin]
        if len(entries) >= 2 and (not origins or len(set(origins)) < len(entries)):
            ids = ", ".join(claim_id for claim_id, _ in entries)
            r.fail(f"source laundering risk: {ids} repeat the same or missing origin for '{claim_text[:60]}'")


def validate_insight_confidence(r, workspace, filename="insights.md"):
    text = _read(workspace, filename)
    if not text:
        return

    strong_recommendation = re.search(
        r"strong recommendation|strongly recommend|must acquire|immediately|\u660e\u786e\u5efa\u8bae|\u5f3a\u70c8\u5efa\u8bae|\u5fc5\u987b\u8fdb\u5165|\u7acb\u5373\u6536\u8d2d|\u660e\u786e\u8fdb\u5165",
        text,
        re.IGNORECASE,
    )
    weak_only = re.search(
        r"source grades?\s*C\s*/\s*D\s*only|C/D\s*only|\u4ec5\u7531\s*[CD]\s*\u7ea7|\u53ea[\u7531\u6709].*[CD]\s*\u7ea7",
        text,
        re.IGNORECASE,
    )
    explicit_high_grade = re.search(r"\bsource[_ ]?grades?\s*[:：]?\s*[AB]\b|[AB]\s*\u7ea7", text, re.IGNORECASE)

    if strong_recommendation and (weak_only or not explicit_high_grade):
        r.fail("Strong recommendation backed only by weak sources — downgrade confidence or add A/B evidence")


def validate_report_links(r, workspace, filename="report.html"):
    text = _read(workspace, filename)
    if not text:
        return

    evidence_text = _read(workspace, "evidence_base.md")
    claims = _claim_blocks(evidence_text)
    claim_ids = {fields.get("claim_id") for fields in claims if fields.get("claim_id")}
    source_ids = {fields.get("source_id") for fields in claims if fields.get("source_id")}

    report_claim_refs = _report_id_refs(text, (
        "data-claim-id",
        "data-evidence-id",
        "claim_id",
        "claimId",
        "claimIds",
        "claim_ids",
        "evidence_id",
        "evidenceId",
        "evidenceIds",
    ))
    report_source_refs = _report_id_refs(text, (
        "data-source-id",
        "source_id",
        "sourceId",
        "sourceIds",
    ))

    if claim_ids:
        unknown_claims = sorted(ref for ref in report_claim_refs if ref not in claim_ids)
        if unknown_claims:
            r.fail(f"Report references unknown claim_id(s): {', '.join(unknown_claims)}")
    if source_ids:
        unknown_sources = sorted(ref for ref in report_source_refs if ref not in source_ids)
        if unknown_sources:
            r.fail(f"Report references unknown source_id(s): {', '.join(unknown_sources)}")
    _validate_chart_claim_consistency(r, text, claims)

    evidence_link_pattern = re.compile(
        r"claim[_-]?id|evidence[_-]?id|data-claim-id|data-evidence-id|source[_-]?id|evidence-ref|claimIds",
        re.IGNORECASE,
    )
    has_evidence_link = bool(evidence_link_pattern.search(text))

    headline_number = re.search(
        r"(headline|executive|summary|market size|\u6838\u5fc3data|\u5173\u952e\u6570\u5b57)[\s\S]{0,240}"
        r"(\d+(?:\.\d+)?\s*(?:%|bn|billion|million|rmb|usd|\u4ebf\u5143|\u4ebf|\u4e07|USD|RMB))",
        text,
        re.IGNORECASE,
    )
    if headline_number and not has_evidence_link:
        r.fail("Headline number lacks evidence link — add claim_id/evidence_id/source_id")

    chart_data = "echarts.init" in text and re.search(r"(?i)(?:\"data\"|(?<!\")\bdata)\s*[:\[]", text)
    chart_level_link = re.search(
        r"data-(?:claim|evidence|source)-id|claimIds|claim_ids|evidenceIds|sourceIds|chartClaim",
        text,
        re.IGNORECASE,
    )
    if chart_data and not chart_level_link:
        r.fail("Chart data lacks chart-level evidence link — bind chart series to claim_id/evidence_id/source_id")
