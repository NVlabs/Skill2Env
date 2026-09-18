---
name: aws-architecture-diagram
description: Generate AWS architecture diagrams in draw.io format. Activates when the user asks to create, generate, or build an architecture diagram, system diagram, or draw.io diagram for AWS services.
---

## Instructions

Generate a draw.io (.drawio) XML file representing an AWS architecture diagram.

### Layout
- **Left-to-right flow** for data/request path
- **UI/Frontend on the LEFT** (users access from left side)
- **Data sources / external systems on the RIGHT**
- Use horizontal lanes for parallel paths (top lane, bottom lane)
- **Minimum 220px horizontal spacing** between icons (to leave room for edge labels)
- **Minimum 250px vertical spacing** between lanes (so vertical edges don't crowd)
- Secondary/auxiliary services (monitoring, DLQ, error paths) go BELOW the main flow with 280px+ vertical gap

### Canvas
- Large canvas: `pageWidth="2400" pageHeight="1400"` minimum
- Set `dx="2800" dy="1600"` for proper viewport
- Always include a title block as the first element after the background:
```xml
<mxCell value="&lt;b&gt;Diagram Title&lt;/b&gt;&lt;br&gt;Author | Date | Version" style="text;html=1;align=left;verticalAlign=top;whiteSpace=wrap;rounded=0;fontSize=14;spacing=8;" vertex="1" parent="1">
  <mxGeometry x="40" y="30" width="420" height="60" as="geometry" />
</mxCell>
```

### Icon Style
- Icons are from draw.io's built-in `mxgraph.aws4` stencil library — the **official AWS Architecture Icons** (https://aws.amazon.com/architecture/icons/, updated quarterly)
- Icon size: **78x78px** for main services, **65x65px** for secondary
- Use `sketch=0;outlineConnect=0;` on all icons
- Use `strokeColor=#ffffff` on all AWS service icons
- **MUST include `fillColor`** — without it, icons render as invisible/white in PNG export
- Font size: **12px** for labels
- Always include: `fontColor=#232F3E;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;aspect=fixed;`

**fillColor by AWS service category:**
| Category | fillColor | Services |
|----------|-----------|----------|
| Compute | `#ED7100` | Lambda, EC2, ECS, EKS, Fargate |
| Networking | `#8C4FFF` | VPC, ELB, CloudFront, Route 53, API Gateway |
| Database | `#C925D1` | RDS, DynamoDB, Aurora, ElastiCache |
| Storage | `#3F8624` | S3, EFS, EBS |
| Security | `#DD344C` | IAM, Cognito, KMS, WAF |
| Integration | `#E7157B` | SQS, SNS, EventBridge, Step Functions |
| Analytics | `#8C4FFF` | Kinesis, Athena, Redshift |
| Management | `#E7157B` | CloudWatch, CloudTrail |
| AI/ML | `#01A88D` | Bedrock, SageMaker |

### Edge Style — CRITICAL FOR CLEAN DIAGRAMS

**Base edge style (all edges):**
```
edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;
```

**Rules for edge labels:**
- Keep labels SHORT (1-2 words max). Use icon labels for detail, not edge labels.
- On horizontal edges: position label ABOVE the line using `verticalAlign=bottom;` in the edge style
- On vertical edges: position label to the LEFT using `align=right;` in the edge style
- Always add `labelBackgroundColor=#F5F5F5;` so labels don't overlap lines
- For edges WITHOUT labels: omit the `value` attribute entirely (don't use `value=""`)

**Edge label positioning (prevents overlap with icons):**
```xml
<mxCell value="Label" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;labelBackgroundColor=#F5F5F5;fontSize=11;" edge="1" source="a" target="b" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

**For edges that go to services ABOVE or BELOW the main flow:**
- Use explicit exit/entry points to control routing:
  - Exit bottom: `exitX=0.5;exitY=1;exitDx=0;exitDy=0;`
  - Enter top: `entryX=0.5;entryY=0;entryDx=0;entryDy=0;`
  - Exit top: `exitX=0.5;exitY=0;exitDx=0;exitDy=0;`
  - Enter bottom: `entryX=0.5;entryY=1;entryDx=0;entryDy=0;`
- This prevents draw.io from routing lines through other icons

**Edge types:**
- Solid black (`strokeWidth=2`): primary data flow
- Dashed black (`strokeWidth=2;dashed=1;`): optional/async path
- Dashed red (`strokeWidth=2;dashed=1;strokeColor=#DD344C;`): error path

**Edge attachment (CRITICAL — fixes "green cross" problem):**
- Every edge MUST have both `source="<cell-id>"` and `target="<cell-id>"` attributes referencing valid cell IDs
- NEVER create floating/unattached edges — all edges must be bound to shapes at both ends
- Always include `exitX/exitY` and `entryX/entryY` to define exact connection points on the shape perimeter
- In draw.io, properly attached edges show a "blue dot" anchor; unattached edges show a "green cross"
- If an edge connects to a child inside a container, reference the child's ID directly (not the container)
- **Cross-container edges:** When source and target are in different containers, set the edge's `parent="1"` (root layer) so draw.io can route it across boundaries

**When NOT to label edges:**
- If the flow is obvious from context (e.g., Lambda → DynamoDB doesn't need "Write")
- If the icon labels already explain the relationship
- Prefer fewer, more meaningful labels over labeling every edge

### Two Icon Patterns — CRITICAL

**Pattern 1: Service-level (resourceIcon frame)**
- Style: `sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor=<CATEGORY_COLOR>;strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.<name>`
- **MUST use `strokeColor=#ffffff`** — without it, the white glyph disappears
- **MUST use `fillColor=<color>`** — without it, icon renders as white/invisible square in PNG export
- Size: 78x78

**Pattern 2: Resource-level (standalone shape)**
- Style: `sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor=<CATEGORY_COLOR>;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.<name>`
- **MUST use `strokeColor=none`** — using #ffffff breaks these
- **MUST use `fillColor=<color>`** — same reason as above
- Size: 78x78 or 48x48

**Confusing these patterns guarantees broken icons.**

### Icon Reference Files (load by category as needed)
- `references/aws-icons-compute.md` — Lambda, EC2, ECS, EKS, Fargate
- `references/aws-icons-database.md` — DynamoDB, RDS, Aurora, ElastiCache
- `references/aws-icons-integration.md` — API Gateway, SQS, SNS, EventBridge, Step Functions
- `references/aws-icons-networking.md` — CloudFront, Route 53, VPC, ELB
- `references/aws-icons-storage.md` — S3, EFS, EBS, Glacier, Backup
- `references/aws-icons-security.md` — IAM, Cognito, KMS, WAF, Shield
- `references/aws-icons-analytics-ml.md` — Kinesis, Athena, Bedrock, SageMaker
- `references/aws-icons-common.md` — Groups, general resources, edge styles, base template

**Always look up icons from reference files. Never guess icon names.**

**Fallback for unmapped services:** If a service is NOT found in any reference file, use this generic AWS cloud icon with the service name as label:
```
sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor=#232F3E;strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.general_AWScloud
```
Never render an unknown service as a plain colored rectangle with no label.

### Group Boundaries
- **AWS Cloud:** `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_aws_cloud_alt;strokeColor=#232F3E;fillColor=none;container=1;dropTarget=1;`
- **Account:** `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_account;strokeColor=#CD2264;fillColor=none;container=1;dropTarget=1;`
- **On-premise:** `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_on_premise;strokeColor=#5A6C86;fillColor=none;container=1;dropTarget=1;`
- **VPC:** `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc2;strokeColor=#8C4FFF;fillColor=none;container=1;dropTarget=1;`
- **Subnet (public):** `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_security_group;strokeColor=#7AA116;fillColor=none;container=1;dropTarget=1;`
- **Subnet (private):** `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_security_group;strokeColor=#147EBA;fillColor=none;container=1;dropTarget=1;`
- **Logical groups:** Simple dashed boxes: `whiteSpace=wrap;html=1;fillColor=none;dashed=1;dashPattern=8 8;container=1;dropTarget=1;`
- **NO colored backgrounds** on group boxes — always `fillColor=none`

**Container nesting (CRITICAL for grouping):**
- ALL boundary/group shapes MUST include `container=1;dropTarget=1;` in their style
- Child cells inside a boundary MUST set `parent="<boundary-cell-id>"` instead of `parent="1"`
- This ensures moving a boundary moves all its children together
- Example:
```xml
<mxCell id="vpc1" value="VPC" style="shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc2;strokeColor=#8C4FFF;fillColor=none;container=1;dropTarget=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="800" height="500" as="geometry" />
</mxCell>
<mxCell id="lambda1" value="Lambda" style="shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;strokeColor=#ffffff;" vertex="1" parent="vpc1">
  <mxGeometry x="50" y="50" width="78" height="78" as="geometry" />
</mxCell>
```
Note: child geometry coordinates are **relative to the parent container**, not the canvas.

### PNG Export Background Fix
Place a full-canvas rectangle as the FIRST element (lowest z-order):
```xml
<mxCell value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="2400" height="1400" as="geometry" />
</mxCell>
```
This prevents black background on PNG export. Use `strokeColor=none` (not E0E0E0).

### Multi-page Diagrams
For complex architectures, use multiple pages (tabs) in one .drawio file:
```xml
<mxfile>
  <diagram id="overview" name="Overview">...</diagram>
  <diagram id="networking" name="Networking Detail">...</diagram>
  <diagram id="data-flow" name="Data Flow">...</diagram>
</mxfile>
```
- Page 1: High-level overview (service-level icons only)
- Page 2+: Detail views (resource-level icons, subnet layouts, etc.)

### Edge Legend (optional, for complex diagrams)
Place below the title block if the diagram has multiple edge types:
- Solid line: primary data flow
- Dashed line: optional/async
- Red dashed: error path

### File Splitting
Since draw.io XML can be large, split creation across multiple tool calls:
1. Header + left side (frontend, delivery layer)
2. Middle (processing lambdas, database)
3. Right side (ingest, messaging, data sources)
4. Bottom (optional/outbound flows) + close XML

### Audience Mode
Before generating, assess the target audience:
- **Technical**: Use service names, protocol labels (HTTPS, gRPC), CIDR blocks, instance types
- **Non-technical**: Use action labels ("Store Data", "Send Notification"), hide implementation details, use numbered flow (① ② ③)

If unclear, ask: "Technical audience or executive/non-technical?"

### Numbered Flow Edges (for non-technical mode)
Instead of technical labels, show flow order with circled numbers:
- Flow A: ① → ② → ③ → ④ (white circled numbers)
- Flow B: ❶ → ❷ → ❸ → ❹ (black circled numbers for second flow)

Use edge labels: `value="①"` with `fontSize=14;fontStyle=1;labelBackgroundColor=#ffffff;`

### Companion Guide
After generating the .drawio file, also generate a markdown guide:
- Same filename with `.md` extension (e.g., `serverless-api.drawio` + `serverless-api.md`)
- Contents: diagram title, flow description (numbered steps matching edge labels), service list with purpose, key design decisions

### Two-Step Edit Approach
After generating the initial .drawio file:
1. **Export to PNG** using the draw.io CLI (see Output section)
2. **Review the PNG** visually — check for empty/broken icons, overlapping edges, misaligned labels
3. **Fix issues** in the .drawio XML and re-export

This catches rendering problems (wrong stencil names, broken styles) that are invisible in raw XML.

### Icon Name Gotchas — CRITICAL
draw.io stencil names do NOT always match current AWS service names. Services that were renamed keep their legacy stencil names:

| AWS Service Name | draw.io resIcon name | Why |
|---|---|---|
| Amazon OpenSearch Service | `elasticsearch_service` | Renamed from Elasticsearch in 2021; `opensearch_service` also works |
| Amazon EventBridge | `eventbridge` | Was CloudWatch Events |
| AWS Fargate | `fargate` | Correct |
| VPC Peering | `peering` | Resource-level: `shape=mxgraph.aws4.peering;strokeColor=none` — NOT `vpc_peering` or `peering_connection` (those render as blank squares) |
| Amazon MSK | `managed_streaming_for_kafka` | NOT `msk` (renders as blank square) |
| IAM Identity Center | `single_sign_on` | NOT `iam_identity_center` (renders as blank square) |

**Rule:** Always verify icon names from the reference files. If a service icon renders as an empty box, the stencil name is wrong. Check the draw.io source at `src/main/webapp/js/diagramly/sidebar/Sidebar-AWS4.js` for the canonical name.

### Validation Step
After generating XML, mentally verify:
1. Every `resIcon=` value exists in the reference files
2. Service-level icons have `strokeColor=#ffffff`
3. Resource-level icons have `strokeColor=none`
4. No XML comments present
5. All cell IDs are unique
6. Every edge has `<mxGeometry relative="1" as="geometry" />`
7. No icon uses a guessed stencil name — all verified against reference files
8. Every edge has both `source` and `target` attributes referencing valid cell IDs (no floating edges)
9. All group/boundary shapes include `container=1;dropTarget=1;` in their style
10. Children inside boundaries use `parent="<boundary-id>"` (not `parent="1"`)

### Output
- Save with descriptive filename ending in `.drawio`
- Open with `open` command (macOS) or `xdg-open` (Linux) after creation
- For PNG/SVG/PDF export, use draw.io CLI:
  - macOS: `/Applications/draw.io.app/Contents/MacOS/draw.io -x -f png -e -b 10 -o output.drawio.png input.drawio`
  - Linux: `drawio -x -f png -e -b 10 -o output.drawio.png input.drawio`
  Flags: `-x` export, `-f` format, `-e` embed diagram XML, `-b 10` border
- Exported files use double extension: `name.drawio.png` (signals embedded XML, re-editable in draw.io)

### XML Well-formedness (CRITICAL)
- **NEVER include XML comments (`<!-- -->`)** — they cause parse errors
- Escape special characters in values: `&amp;` `&lt;` `&gt;` `&quot;`
- Always use unique `id` values for each mxCell
- Every edge MUST have `<mxGeometry relative="1" as="geometry" />` as child element
- Basic structure must include root cells `id="0"` and `id="1"` (parent="0")

### Official Reference
- Full XML/style reference: https://raw.githubusercontent.com/jgraph/drawio-mcp/main/shared/xml-reference.md
- Style properties: https://raw.githubusercontent.com/jgraph/drawio-mcp/main/shared/style-reference.md
