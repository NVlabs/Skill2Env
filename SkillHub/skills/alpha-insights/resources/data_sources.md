# Data Sources

> **Purpose**: **Curated data source checklist** for the AI Business Analyst Skill
>
> **Usage principles**:
> 1. This is not an exhaustive list, but a **curated collection of high-quality sources**
> 2. When the research topic matches, the AI **must** prioritize searching these data sources
> 3. Relying solely on generic Google search results is prohibited; original authoritative sources must be traced
> 4. Follow the **Triangulation method**: core data requires 2-3 independent sources for cross-validation

---

## Data Source Selection Strategy

### Priority Principles

| Priority | Source Type | Reliability | Use Case |
|----------|-----------|-------------|----------|
| **P0** | Official data (government/regulatory) | Highest | Macro data, policies & regulations, industry statistics |
| **P1** | Authoritative third-party (brokerages/consulting) | High | Market size, competitive landscape, trend analysis |
| **P2** | Vertical data platforms (QuestMobile, etc.) | Medium-High | User behavior, App data, niche segments |
| **P3** | Corporate official disclosures (earnings/filings) | High | Company data, operating metrics |
| **P4** | Media/self-media | Medium-Low | Use as leads only, must verify |

### Data Verification Rules

> Complete definitions and verification methods for validation levels (A/B/C/D) are in [`triangulation.md`](../methodology/triangulation.md).
> Key numbers, chart data, due-diligence entity facts, and evidence supporting strategic recommendations must also follow the Evidence Claim Ledger fields and gate rules in [`evidence_integrity.md`](evidence_integrity.md).

**Execution rules for this checklist**:
- Core data (market size, growth rate, competitor data, user data) **must** achieve B-level or above
- D-level data is **prohibited** as supporting evidence for key conclusions
- C-level data should be annotated with "recommend supplementary verification"
- Headline numbers, chart data, and recommendation-support evidence must register `claim_id`, `source_date`, `retrieved_at`, and `used_in`
- In due diligence / M&A / target-screening work, entity status, ownership / parent relationships, officers, regulatory filings, licenses, major litigation, and filings must have `primary` / `official` / `company_disclosure` source types
- Aggregators, media, and report aggregators are leads only; if used for A/B-level cross-validation, fill `origin_id` to prove they are not repeating the same original source

### Information Type Annotation Standards (Important)

> Data varies not only in "reliability" but also in "type." Different types of information require different handling.

| Label | Information Type | Definition | Handling |
|-------|-----------------|------------|----------|
| 📊 | **Factual Data** | Market size, earnings figures, user counts, transaction volumes, and other quantifiable facts | Can be directly cited; annotate Confidence Level as A/B/C/D |
| 💡 | **Opinions/Intentions** | Strategic positioning, team judgments, management statements, directional descriptions in internal documents | **Must** annotate as "internal opinion," with critical analysis (reasonableness / alternatives / risks) |
| 📰 | **Media Reports** | News articles, industry reports, self-media analysis | Requires cross-validation; trace to original data source |

**Key rules**:
- Strategic intentions/opinions from internal documents (e.g., knowledge base) are **prohibited** from being used directly as analytical conclusions
- Must distinguish between "the team chose to do X" (💡 opinion) and "X's market size is Y" (📊 fact)
- Example: Knowledge base document states "only do platform model" -> annotate as 💡 internal opinion; analyze: why the platform model? are there alternatives? what are the risks?

### ⛔ Prohibited Behaviors

❌ Relying solely on generic Google search results without tracing original sources
❌ Using single-source core data without annotating verification level
❌ Presenting corporate self-reported data (official website/PR releases) as facts in the report
❌ Using D-level data to support key conclusions
❌ Not explaining or addressing data contradictions

---

## ⚡ Data Routing Table (for Stage 4 Quick Decisions)

> **Usage**: At the start of Stage 4, match rows sequentially by research needs to determine which tool to use, what to query, and fallback options.
> **Multi-source coverage principle**: For the same data need, don't stop after finding one source -- cover as many independent sources as possible per the "Data Source Combination Strategy by Topic" below, cross-validate before determining which to trust. Fallback options aren't "backups" -- they're "second perspectives."

| Data Need | Primary Capability | Query Template | Fallback |
|-----------|--------------------|----------------|----------|
| **Macroeconomic data** (GDP/CPI/population/investment) | Search engine | `{indicator} {year} site:stats.gov.cn` | `{indicator} National Bureau of Statistics {year}` -> Wind |
| **Industry market size** | Search engine | `{industry} market size {year}` + restrict to trusted domains | Broker research reports -> Statista |
| **Competitor company data** (earnings/funding/products) | Web scraping | Directly scrape cninfo.com.cn / SEC EDGAR in-site search page | Search engine `{company} annual report {year}` -> enterprise data platforms |
| **User behavior/App data** | Search engine | `{App} MAU DAU QuestMobile {year}` | Qimai Data -> SimilarWeb |
| **Policies & regulations** | Search engine | `{keywords} site:gov.cn` | PKU Law / public legal databases; use LegalSearch if configured |
| **Consumer insights/user voices** | Public web search or optional private social-media adapter | `{product} review Xiaohongshu` / `{product} user feedback RedNote` | User-provided screenshots, links, or exported notes |
| **Internal data/business docs** | Knowledge base search | Search via the current environment's available knowledge-base tools | Ask user directly |
| **Structured business data** | Database query | Query via the current environment's available database/data-processing tools | Degrade to public data estimation |
| **Expert opinions/deep information** | Interview (Track C) | Stage 3.5 generates guide -> user executes | Industry KOL public statements -> broker conference call transcripts |
| **International market data** | Search engine | `{industry} market size {year} report` | Statista -> World Bank -> OECD |
| **⚠️ Data does not exist** | -- | All above paths yield no results | Bottom-up estimation (decompose variables for step-by-step derivation) -> annotate as C-level + note estimation method |

### Tool Availability Assessment

> The AI should automatically detect available tools in the current environment. The table below lists **common tool names** for each capability (examples only; actual names vary by environment).

| Capability | Common Tool Examples | Notes |
|------------|---------------------|-------|
| **Search engine** | Codex native web, browser search, platform search tools, etc. | Prefer available search capability in the environment |
| **Web scraping** | Codex native web, browser/web reading tools, etc. | Retrieve search result pages or specified URL content |
| **Knowledge base search** | Knowledge-base CLI, Notion/Confluence connectors, or other knowledge-base tools | Search via user-configured knowledge base capability |
| **Database query** | SQL warehouse, BigQuery, Snowflake, or other database tools | Query via user-configured database capability |
| **Xiaohongshu / RedNote** | Public search, browser reading, or a separately installed private adapter | The public GitHub package does not bundle provider-specific collection scripts |

```
Decision logic:
1. Detect available tools in the current environment
2. Match capabilities to the table above -> use corresponding tool
3. If a capability has no available tool -> inform user of the gap -> suggest manual retrieval -> degrade annotation to C/D level
```

---

## External Public Data Sources

### I. China Government Official Data (P0 Level)

| Data Source | URL | Coverage | Use Case |
|-------------|-----|----------|----------|
| **National Bureau of Statistics** | https://data.stats.gov.cn/ | GDP, population, consumption, investment, industry, and other macroeconomic data | Macro environment analysis, market size estimation |
| **National Data Administration** | https://www.nda.gov.cn/ | Data elements, digital economy policies | Digital economy, AI, big data industries |
| **Ministry of Industry and Information Technology** | https://www.miit.gov.cn/ | Industrial, communications, software services data | Manufacturing, TMT industry research |
| **People's Bank of China** | http://www.pbc.gov.cn/ | Finance, credit, payment data | Finance, payments, credit industries |
| **Ministry of Commerce** | http://www.mofcom.gov.cn/ | Commerce circulation, e-commerce, foreign investment data | Retail, e-commerce, consumer industries |
| **China Internet Network Information Center (CNNIC)** | https://www.cnnic.net.cn/ | Internet development statistical reports | Internet industry foundational data |

---

### II. Domestic Authoritative Third-Party Institutions (P1 Level)

| Data Source | URL | Specialty | Use Case |
|-------------|-----|-----------|----------|
| **iResearch** | https://report.iresearch.cn/ | Internet, new economy, consumption | Internet industry, new business models |
| **Analysys (incl. Analysys Qianfan)** | https://www.analysys.cn/ | Digital user analysis, industry digitalization, App active users/usage duration | User profiling, digital transformation, competitor analysis |
| **LeadLeo** | https://www.leadleo.com/ | Emerging industries, niche segments | Quick scanning of emerging industries |
| **CIC Consulting** | https://www.cninsights.com/ | Consumer, healthcare, TMT | Consumer industry, healthcare |
| **IDC China** | https://www.idc.com/ | IT, cloud services, digital transformation | Enterprise software, cloud computing, AI |
| **Gartner China** | https://www.gartner.com/ | Technology trends, IT strategy | Technology selection, IT investment decisions |

---

### III. Broker Reports, Corporate Disclosures & Business Data Platforms (P1/P2/P3 Level)

| Data Source | URL | Characteristics | Use Case |
|-------------|-----|-----------------|----------|
| **Hibor** | https://www.hibor.com.cn/ | Free research report aggregation platform | Quick retrieval of in-depth industry reports |
| **DJYanbao** | https://www.djyanbao.com/ | Report downloads, keyword search (⚠️ unofficial channel with compliance risks, use for lead search only) | Competitive analysis leads, company research (citations must trace to original report source) |
| **East Money Choice** | https://data.eastmoney.com/ | Financial data terminal | Listed company financial data, industry data |
| **Wind Financial Terminal** | https://www.wind.com.cn/ | Authoritative financial data (subscription required) | In-depth financial analysis (if authorized) |
| **CNINFO** | https://www.cninfo.com.cn/ | A-share listed company announcements/earnings originals | Company research, financial analysis (P3 corporate disclosure) |
| **SEC EDGAR** | https://www.sec.gov/cgi-bin/browse-edgar | US-listed company filing originals | ADR/US-listed company research (P3 corporate disclosure) |
| **Qichacha** | https://www.qcc.com/ | Enterprise registration info, equity structure, funding history, legal risks | Competitor background investigation, equity tracing, risk screening (P2) |
| **Tianyancha** | https://www.tianyancha.com/ | Enterprise registration info, relationship graphs, operational risks | Competitor due diligence, supplier/partner background checks (P2) |
| **IT Juzi** | https://www.itjuzi.com/ | VC/PE database, funding events, M&A records | Emerging segment investment analysis, competitor funding round tracking (P2) |

---

### IV. Mobile Internet Data Platforms (P2 Level)

| Data Source | URL | Core Capability | Use Case |
|-------------|-----|-----------------|----------|
| **QuestMobile** | https://www.questmobile.com.cn/ | App user behavior, DAU/MAU, usage duration | Internet product analysis, user behavior |
| **Aurora Mobile** | https://www.jiguang.cn/ | Mobile developer data, user profiling | App user analysis, industry trends |
| **TalkingData** | https://www.talkingdata.com/ | Mobile data monitoring, user insights | User behavior analysis, marketing effectiveness |

---

### V. International Authoritative Data Sources (P1/P2 Level, for global perspective)

| Data Source | URL | Coverage | Use Case |
|-------------|-----|----------|----------|
| **Statista** | https://www.statista.com/ | Global statistics, market forecasts | International benchmarking, global markets (P1 📊) |
| **IBISWorld** | https://www.ibisworld.com/ | Global industry reports, market research | Industry entry assessment, international benchmarking (P1 📊) |
| **Euromonitor** | https://www.euromonitor.com/ | Consumer markets, retail data | Consumer goods, retail industry (P1 📊) |
| **McKinsey Insights** | https://www.mckinsey.com/featured-insights | Thought leadership articles, unstructured data | Strategic perspective reference, qualitative trend assessment (P2 💡, prohibited as quantitative data source) |
| **BCG Insights** | https://www.bcg.com/publications | Thought leadership articles, unstructured data | Strategic framework reference, innovation model inspiration (P2 💡, prohibited as quantitative data source) |
| **Bain Insights** | https://www.bain.com/insights/ | Thought leadership articles, unstructured data | M&A/strategy perspective reference (P2 💡, prohibited as quantitative data source) |

---

### VI. Internet Tech Company Research Institutes (P2 Level)

| Data Source | URL | Specialty | Use Case |
|-------------|-----|-----------|----------|
| **Alibaba Research Institute** | https://www.aliresearch.com/ | E-commerce, digital economy, SMEs | E-commerce, platform economy, industrial clusters |
| **Tencent Research Institute** | https://tisi.org/ | Internet+, AI, digital content | Digital content, AI applications |

---

### VII. Industry Associations & Organizations (P1 Level)

| Data Source | Domain | Use Case |
|-------------|--------|----------|
| **China Banking Association** | Banking | Banking data, industry standards |
| **Insurance Association of China** | Insurance | Insurance statistics, product data |
| **National Financial Regulatory Administration** | Financial regulation | Banking/insurance/non-bank regulatory data (formerly CBIRC, reorganized 2023) |
| **Payment & Clearing Association of China** | Payments industry | Payment transaction data, industry reports |
| **Internet Society of China** | Internet industry | Industry development reports, self-regulatory standards |
| **China Chain Store & Franchise Association** | Retail | Chain retail data, consumption trends |

---

## Data Source Combination Strategy by Topic

### Internet/Digital Economy

```
Required combination:
1. CNNIC (foundational user data)
2. QuestMobile (App behavior data)
3. iResearch/Analysys (industry analysis reports)
4. National Bureau of Statistics (digital economy macro data)

Optional supplements:
- Alibaba Research Institute/Tencent Research Institute (ecosystem perspective)
- IDC (enterprise IT/cloud data)
```

### Consumer Industry

```
Required combination:
1. National Bureau of Statistics (retail sales data, consumption macro)
2. CIC Consulting (consumer industry reports)
3. Broker consumer industry reports (Hibor search)

Optional supplements:
- Euromonitor (international benchmarking)
- China Chain Store & Franchise Association (channel data)
```

### Finance/Payments Industry

```
Required combination:
1. People's Bank of China (official financial data)
2. Payment & Clearing Association of China (payment data)
3. National Financial Regulatory Administration/Banking Association (banking data)
4. Broker finance industry reports

Optional supplements:
- iResearch (payments industry reports)
- IDC (fintech IT spending)
```

### TMT/Technology Industry

```
Required combination:
1. Ministry of Industry and Information Technology (industry statistics)
2. IDC/Gartner (technology trends, market data)
3. Broker TMT industry reports

Optional supplements:
- Tencent/Alibaba Research Institutes (AI/cloud data)
- Statista (global benchmarking)
```

### Emerging Industries/Niche Segments

```
Required combination:
1. LeadLeo (quick scanning)
2. Broker in-depth reports (Hibor search)
3. Business registration/Qichacha (enterprise data)

Optional supplements:
- Expert interviews (validating non-public information)
- Media report cross-validation
```

---

## Internal Specialty Data Sources

### VIII. Knowledge Base Search (Specialty Data Source)

> **Purpose**: Search user knowledge bases (Notion, Confluence, local knowledge bases, etc.) for historical research reports, industry notes, methodology resources
>
> **Prerequisite**: User must have configured a knowledge base MCP tool

**Required capabilities** (AI auto-matches available tools in the environment):

| Capability | Description | Use Case |
|------------|-------------|----------|
| **Keyword search** | Search documents in the knowledge base | Quick retrieval of historical research, industry notes |
| **Document detail** | Get full document content | Deep reading of specific documents |
| **Knowledge base browsing** | List knowledge bases or document lists | Browse documents by knowledge base |

**When to use**:
- Stage 3 pre-scan: Quick check for relevant historical research
- Stage 4 Research Execution: Supplement internal perspective, historical data
- Stage 5 Insight Synthesis: Reference historical Insight frameworks

**Usage rules**:
1. Search user's personal knowledge base first, then team knowledge base
2. After finding relevant documents, use document detail tool for full content
3. When citing knowledge base content, annotate source: `📄 Source: Knowledge Base - [Document Title]`
4. Knowledge base content serves as internal perspective; cross-validate with public data

**Search strategy**:
```
Step 1: Search keywords using knowledge base search tool
Step 2: Select most relevant documents from results
Step 3: Use document detail tool to get full text
Step 4: Extract useful information, annotate source
```

---

### IX. Internal Database (Specialty Data Source)

> **Purpose**: Company internal business data, user behavior data, transaction records, and other core data assets
>
> **Prerequisite**: User must have configured a database or data warehouse tool (e.g., BigQuery, Snowflake, Postgres, DuckDB, or another environment-specific connector) with appropriate access permissions

**Required capabilities** (AI auto-matches available tools in the environment):

| Capability | Description | Use Case |
|------------|-------------|----------|
| **Table search** | Search related tables by natural language description | Find target data tables |
| **Table detail** | Get table details (fields, descriptions, size) | Understand table structure and content |
| **SQL query** | Execute SQL queries | Extract specific data |
| **Field search** | Search field names | Find tables containing specific fields |

**When to use**:
- Stage 3 pre-scan: Quick check for relevant internal data
- Stage 4 Research Execution: Extract internal business data, user behavior data
- Data validation: Cross-validate with public data to improve Confidence Level

**Execution flow**:
```
Step 1: Table Discovery
   - Search keywords using table search tool (e.g., "user transactions", "product details")
   - Or search field names using field search tool (e.g., "user_id", "gmv")

Step 2: Table Understanding
   - Use table detail tool to get table details
   - Review field definitions, table descriptions, data volume

Step 3: Data Extraction
   - Write SQL query statements
   - Execute using SQL query tool
   - Note: Only SELECT statements are allowed

Step 4: Result Processing
   - Parse returned data
   - Annotate source: 📄 Source: {database} - [table name] - [query time]
```

**SQL coding standards**:
```sql
-- ✅ Recommended: explicit fields, add conditions, limit rows
SELECT
    user_id,
    SUM(gmv) AS total_gmv,
    COUNT(*) AS order_count
FROM {project}.{table_name}
WHERE dt = '2024-01-01'
    AND user_type = 'active'
GROUP BY user_id
LIMIT 1000;

-- ❌ Prohibited: SELECT * full scan on large tables
SELECT * FROM huge_table;
```

**Notes**:
1. **Only execute SELECT statements**: INSERT/UPDATE/DELETE/DROP prohibited
2. **Limit query rows**: Large table queries must include LIMIT
3. **Partition filtering**: Prefer partition fields (e.g., dt) for filtering, reducing scan volume
4. **Data masking**: User privacy data requires masking
5. **Source annotation**: All data must annotate source table and query time

**Data verification levels**:
| Source Type | Verification Level | Notes |
|-------------|-------------------|-------|
| Official data tables (approved) | A Level | Trustworthy |
| Business data tables (regular) | B Level | Need to understand data definitions |
| Temporary/intermediate tables | C Level | Need to trace upstream for validation |

---

### X. Xiaohongshu / RedNote Data (Optional Social-Media Source)

> **Purpose**: Consumer sentiment, product feedback, trend insights, brand reputation
>
> **Public package boundary**: The GitHub package does not bundle provider-specific collection scripts. Use public search, browser-readable pages, user-provided links/screenshots, or a separately installed private adapter if the user's environment provides one.

**Collection options**:

| Option | Use Case | Evidence Grade |
|--------|----------|----------------|
| Public web search (`site:xiaohongshu.com` + keywords) | Lightweight trend scan and quote discovery | Usually C unless original page is accessible |
| Browser-readable note pages or share links provided by the user | Direct inspection of specific notes or comments | B/C depending on visibility and timestamp |
| User-provided screenshots or exported notes | Private or login-gated content that the AI cannot access directly | C unless source metadata is complete |
| Separately installed private adapter | High-volume collection in environments where the user has configured one | Grade by adapter reliability and source traceability |

**When to use**:
- Stage 3 pre-scan: Understanding consumer sentiment, product reputation
- Stage 4 Research Execution: Collecting authentic consumer feedback, competitor sentiment
- Stage 5 Insight Synthesis: Extracting Insights from user perspective

**Execution flow**:
```
Step 1: Search publicly visible pages
   - Query examples: "{brand} review Xiaohongshu", "{category} RedNote user feedback", "site:xiaohongshu.com {keyword}"

Step 2: Capture traceable evidence
   - Preserve title, author/account, visible date, link or screenshot reference, engagement if visible
   - Do not treat copied snippets without source metadata as high-confidence evidence

Step 3: Ask for manual evidence when access is gated
   - Request links, screenshots, exports, or a configured private adapter only when Track E is material to the research question

Step 4: Synthesize cautiously
   - Use social media as directional signal unless sample size, timestamps, and source traceability are strong
```

**Search guidance**:

| Search Need | Query Pattern |
|-------------|---------------|
| Product sentiment | `{product} review Xiaohongshu` / `{product} RedNote feedback` |
| Competitor comparison | `{brand A} {brand B} Xiaohongshu comparison` |
| Pain points | `{category} pain point Xiaohongshu` / `{product} complaint RedNote` |
| Trend signal | `{topic} Xiaohongshu trend` / `{topic} RedNote creator discussion` |

**Value assessment criteria**:

| Type | Characteristics | Handling |
|------|-----------------|----------|
| **Worth noting** | In-depth reviews, industry trends, KOL opinions, competitor dynamics, user pain points, high engagement | Focus analysis |
| **Regular content** | Reposts, sponsored content, low engagement, low relevance | Brief note or skip |

**Output format**:
```
Xiaohongshu / RedNote intelligence scan complete

Notable content:

1. @AuthorName - 2026-02-24
   Title: In-depth Comparison of AI Programming Tools
   Engagement: likes/saves/comments if visible
   Link or screenshot: https://www.xiaohongshu.com/explore/...
   Evidence grade: C (publicly discovered, limited sample)

2. @AnotherAuthor - 2026-02-24
   Title: One Month Real Experience with Cursor
   Engagement: 3456 likes / 2100 saves / 89 comments if visible
   Link or screenshot: user-provided screenshot
   Evidence grade: C

Other content: 8 regular notes (omitted)
```

**Data verification levels**:
| Source Type | Verification Level | Notes |
|-------------|-------------------|-------|
| High-engagement notes (10K+) | B Level | Reflects genuine user interest |
| KOL/KOC original content | B Level | Professional perspective, needs cross-validation |
| Regular user notes | C Level | Individual cases, need multi-sample validation |
| Sponsored content | D Level | Prohibited as key evidence |

**Applicability assessment**:

| Topic Type | Applicable? | Reason |
|------------|-------------|--------|
| Consumer insights | ✅ Strongly recommended | Direct access to authentic user feedback |
| C-end product research | ✅ Recommended | Understanding user reviews and pain points |
| Brand sentiment monitoring | ✅ Recommended | Real-time brand reputation tracking |
| B-end business research | ⚠️ Use with caution | Limited content, supplement with other channels |
| Industry macro research | ⚠️ Supplementary | Adding consumer perspective |

---

### XI. User Feedback Data (Specialty Data Source)

> **Purpose**: Authentic user feedback, experience issues, complaint pain points, satisfaction insights
>
> **Prerequisite**: User must have configured a database MCP tool with access to user feedback/customer service ticket data tables

**Required capabilities** (AI auto-matches available tools in the environment):

| Capability | Description | Use Case |
|------------|-------------|----------|
| **Table search** | Search user feedback/customer service related data tables | Find target table |
| **Table detail** | Get table structure and field definitions | Understand data definitions |
| **SQL query** | Execute aggregate/detail queries | Extract feedback data |

**Typical table structure** (actual fields depend on user environment):

| Field Type | Typical Field Names | Analysis Value |
|------------|---------------------|----------------|
| Issue category (multi-level) | `category_l1`, `category_l2`, `category_l3`, etc. | Issue distribution, pain point clustering |
| Issue content | `question_text`, `feedback_content`, etc. | Pain point mining, sentiment analysis |
| Product dimension | `product`, `sub_product`, etc. | Product dimension analysis |
| Time partition | `dt`, `create_date`, etc. | Trend analysis |

**Typical analysis dimensions**:

| Analysis Type | SQL Approach | Output |
|---------------|-------------|--------|
| **Issue distribution** | GROUP BY level-1/level-2 category + COUNT | Which categories have the most issues |
| **Pain point clustering** | GROUP BY finest category + COUNT + ORDER BY DESC | TOP N high-frequency pain points |
| **Product experience** | WHERE product = 'X' + GROUP BY sub_product | Specific product's experience shortcomings |
| **Trend analysis** | GROUP BY date + COUNT | Issue volume change over time |
| **Deep dive** | WHERE category condition + content field | Specific user verbatims and attitudes |

**Example SQL** (field names need to be replaced with actual table fields):

```sql
-- Issue distribution: issue volume by level-1 category
SELECT category_l1, COUNT(*) AS cnt
FROM {project}.{feedback_table}
WHERE dt >= '{start_date}'
GROUP BY category_l1
ORDER BY cnt DESC
LIMIT 20;

-- Pain point clustering: TOP frequent issues under a category
SELECT category_l3, COUNT(*) AS cnt
FROM {project}.{feedback_table}
WHERE category_l1 = '{target_category}'
  AND dt >= '{start_date}'
  AND category_l3 IS NOT NULL
GROUP BY category_l3
ORDER BY cnt DESC
LIMIT 30;

-- User verbatims: get specific issue details
SELECT category_l1, category_l2, feedback_content, dt
FROM {project}.{feedback_table}
WHERE category_l1 IN ('{category1}', '{category2}')
  AND dt >= '{start_date}'
LIMIT 100;
```

**Execution flow**:
```
Step 1: Search for "user feedback", "customer service tickets", "user complaints" using table search tool
Step 2: Use table detail tool to view field definitions, understand the classification system and data definitions
Step 3: Write SQL based on actual fields, ensure partition filtering and LIMIT
Step 4: Parse results, annotate source
```

**Notes**:
1. **Partition filtering required**: Date partition field must have conditions to avoid full table scans
2. **LIMIT required**: Default LIMIT 1000, can increase moderately for deep analysis
3. **Field adaptation**: Classification systems differ across companies; check table structure before writing SQL
4. **Content fields**: User feedback content fields may contain multi-part structures (issue+solution+attitude); parse carefully

**Data verification levels**:

| Source Type | Verification Level | Notes |
|-------------|-------------------|-------|
| Issue volume statistics (aggregate) | A Level | Official system data, directly trustworthy |
| Individual user verbatim | B Level | Authentic feedback, but individual case |
| Trend assessment (needs multi-period comparison) | B Level | Need to verify sufficient time span |

**Applicability assessment**:

| Topic Type | Applicable? | Reason |
|------------|-------------|--------|
| Product optimization | ✅ Strongly recommended | Directly identify user pain points and experience gaps |
| Consumer insights | ✅ Recommended | Access to authentic user feedback and attitudes |
| Competitive analysis | ⚠️ Supplementary | Can identify own weaknesses, but no competitor data |
| Industry research | ❌ Not applicable | Only covers own products |
| Business model analysis | ⚠️ Supplementary | Can discover unmet user needs |

---

## Data Source Integration Status

> Specialty data sources require user configuration of the corresponding tools or connectors. The AI auto-detects available capabilities at Stage 4 start; unconfigured data sources are automatically skipped with user notification.
>
> | Data Source | Required Configuration | Status |
> |------------|----------------------|--------|
> | Knowledge base search | Knowledge-base CLI, Notion/Confluence connectors, or other knowledge-base tools | Auto-detected |
> | Internal database | SQL warehouse, BigQuery, Snowflake, or other database tools | Auto-detected |
> | Xiaohongshu / RedNote data | Public search/browser access or optional private adapter | Auto-detected when available |
> | User feedback data | Database/data-processing tool + feedback data table | Auto-detected |

---

## Appendix: Data Verification Checklist Template

> The complete verification checklist template is in the "Output Format" section of [`triangulation.md`](../methodology/triangulation.md). Every report must include this checklist at the end.
