---
name: aws-architecture-diagram
description: Always use when user asks to create, generate, or build an AWS architecture diagram, cloud infrastructure diagram, or system diagram with AWS services. Also activates for draw.io diagrams mentioning AWS services like Lambda, DynamoDB, S3, API Gateway, etc.
---

# AWS Architecture Diagram Skill

Generate AWS architecture diagrams as native `.drawio` files using official AWS Architecture Icons. Optionally export to PNG, SVG, or PDF with embedded XML (so exported files remain editable in draw.io).

## How to create a diagram

1. **Generate draw.io XML** in mxGraphModel format following the rules below
2. **Write the XML** to a `.drawio` file using the Write tool
3. **If the user requested an export format** (png, svg, pdf), export using the draw.io CLI (see Export section)
4. **Open the result** with `open` (macOS), `xdg-open` (Linux), or print the path

## Layout Rules

- **Left-to-right flow** for data/request path
- **UI/Frontend on the LEFT** (users access from left side)
- **Data sources / external systems on the RIGHT**
- Use horizontal lanes for parallel paths (top lane, bottom lane)
- **Minimum 220px horizontal spacing** between icons (room for edge labels)
- **Minimum 250px vertical spacing** between lanes
- Secondary/auxiliary services (monitoring, DLQ) go BELOW main flow with 280px+ gap
- Canvas: `pageWidth="2400" pageHeight="1400"`, viewport `dx="2800" dy="1600"`
- Always include a title block after the background rectangle:
```xml
<mxCell value="&lt;b&gt;Diagram Title&lt;/b&gt;&lt;br&gt;Author | Date | Version" style="text;html=1;align=left;verticalAlign=top;whiteSpace=wrap;rounded=0;fontSize=14;spacing=8;" vertex="1" parent="1">
  <mxGeometry x="40" y="30" width="420" height="60" as="geometry" />
</mxCell>
```

## Icon Style

- Icons are from draw.io's built-in `mxgraph.aws4` stencil library — the **official AWS Architecture Icons** (https://aws.amazon.com/architecture/icons/)
- Icon size: **78x78px** for main services, **65x65px** for secondary
- Use `sketch=0` on all icons
- Use `strokeColor=#ffffff` on all AWS service icons
- Font size: **12px** for labels
- **NO colored backgrounds** on group boxes — always `fillColor=none`

## Edge Style — CRITICAL FOR CLEAN DIAGRAMS

**Base edge style:**
```
edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;
```

**Edge label rules:**
- Keep labels SHORT (1-2 words max). Detail goes in icon labels, not edge labels.
- Always add `labelBackgroundColor=#F5F5F5;fontSize=11;` to edges with labels
- For edges WITHOUT labels: omit `value` entirely
- When NOT to label: if the flow is obvious (Lambda → DynamoDB doesn't need "Write")

**For edges to services ABOVE or BELOW main flow, use explicit exit/entry points:**
- Exit bottom: `exitX=0.5;exitY=1;exitDx=0;exitDy=0;`
- Enter top: `entryX=0.5;entryY=0;entryDx=0;entryDy=0;`
- This prevents draw.io from routing lines through other icons

**Edge types:**
- Solid (`strokeWidth=2`): primary data flow
- Dashed (`strokeWidth=2;dashed=1;`): optional/async
- Red dashed (`strokeWidth=2;dashed=1;strokeColor=#DD344C;`): error path

**Edge attachment (CRITICAL — fixes "green cross" problem):**
- Every edge MUST have both `source="<cell-id>"` and `target="<cell-id>"` attributes referencing valid cell IDs
- NEVER create floating/unattached edges — all edges must be bound to shapes at both ends
- Always include `exitX/exitY` and `entryX/entryY` to define exact connection points on the shape perimeter
- **Cross-container edges:** When source and target are in different containers, set the edge's `parent="1"`

## PNG Export Background
First element after root cells (lowest z-order):
```xml
<mxCell value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="2400" height="1400" as="geometry" />
</mxCell>
```

## AWS Icon Patterns (VERIFIED WORKING)

### resourceIcon (78x78, colored square frame)

| Service | resIcon | fillColor |
|---------|---------|-----------|
| Lambda | `mxgraph.aws4.lambda` | `#ED7100` |
| API Gateway | `mxgraph.aws4.api_gateway` | `#E7157B` |
| EventBridge | `mxgraph.aws4.eventbridge` | `#E7157B` |
| SNS | `mxgraph.aws4.sns` | `#E7157B` |
| SES | `mxgraph.aws4.simple_email_service` | `#DD344C` |
| Step Functions | `mxgraph.aws4.step_functions` | `#E7157B` |
| DynamoDB | `mxgraph.aws4.dynamodb` | `#C925D1` |
| RDS | `mxgraph.aws4.rds` | `#C925D1` |
| S3 | `mxgraph.aws4.s3` | `#7AA116` |
| CloudFront | `mxgraph.aws4.cloudfront` | `#8C4FFF` |
| Route 53 | `mxgraph.aws4.route_53` | `#8C4FFF` |
| ECS | `mxgraph.aws4.ecs` | `#ED7100` |
| EC2 | `mxgraph.aws4.ec2` | `#ED7100` |

Style template:
```
sketch=0;points=[[0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0],[0,1,0],[0.25,1,0],[0.5,1,0],[0.75,1,0],[1,1,0],[0,0.25,0],[0,0.5,0],[0,0.75,0],[1,0.25,0],[1,0.5,0],[1,0.75,0]];outlineConnect=0;fontColor=#232F3E;fillColor=<COLOR>;strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.<SERVICE>
```

### productIcon (70x100, taller with service header bar)

| Service | prIcon |
|---------|--------|
| SQS | `mxgraph.aws4.sqs` |

Style template:
```
sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;strokeColor=#ffffff;fillColor=#232F3E;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;whiteSpace=wrap;fontSize=12;fontStyle=0;shape=mxgraph.aws4.productIcon;prIcon=mxgraph.aws4.<SERVICE>
```

### Standalone shapes (no resIcon needed)

| Shape | shape value | fillColor |
|-------|-------------|-----------|
| Client/Browser | `mxgraph.aws4.client` | `#232F3D` |
| Traditional Server | `mxgraph.aws4.traditional_server` | `#232F3D` |
| Firewall | `mxgraph.aws4.generic_firewall` | `#232F3D` |
| ALB | `mxgraph.aws4.application_load_balancer` | `#8C4FFF` |
| NLB | `mxgraph.aws4.network_load_balancer` | `#8C4FFF` |
| VPC Endpoint | `mxgraph.aws4.endpoints` | `#8C4FFF` |

### Group boundaries

| Group | grIcon | strokeColor |
|-------|--------|-------------|
| AWS Cloud | `mxgraph.aws4.group_aws_cloud_alt` | `#232F3E` |
| Account | `mxgraph.aws4.group_account` | `#CD2264` |
| On-premise | `mxgraph.aws4.group_on_premise` | `#5A6C86` |
| Corporate DC | `mxgraph.aws4.group_corporate_data_center` | `#388E3C` |
| VPC | `mxgraph.aws4.group_vpc2` | `#8C4FFF` |
| Subnet (public) | `mxgraph.aws4.group_security_group` | `#7AA116` |
| Subnet (private) | `mxgraph.aws4.group_security_group` | `#147EBA` |

**Container nesting (CRITICAL for grouping):**
- ALL group/boundary shapes MUST include `container=1;dropTarget=1;` in their style
- Child cells inside a boundary MUST set `parent="<boundary-cell-id>"` instead of `parent="1"`
- This ensures moving a boundary moves all its children together
- Child geometry coordinates are **relative to the parent container**, not the canvas
- **Cross-container edges:** When source and target are in different containers, set the edge's `parent="1"`

## BROKEN Icons — DO NOT USE

- `resIcon=mxgraph.aws4.dynamodb_table` — renders as empty colored square
- `resIcon=mxgraph.aws4.dynamodb_stream` — renders as empty colored square
- `resIcon=mxgraph.aws4.general_saml_token` — renders as black square
- `resIcon=mxgraph.aws4.endpoint` — may not render
- `resIcon=mxgraph.aws4.kinesis_data_streams` — unreliable

**Alternatives:**
- DynamoDB tables/streams → use `resIcon=mxgraph.aws4.dynamodb` with descriptive labels
- External systems → use `shape=mxgraph.aws4.traditional_server`
- Browsers/clients → use `shape=mxgraph.aws4.client`

## Audience Mode

Before generating, assess the target audience:
- **Technical**: Use service names, protocol labels (HTTPS, gRPC), CIDR blocks, instance types
- **Non-technical**: Use action labels ("Store Data", "Send Notification"), hide implementation details, use numbered flow (① ② ③)

If unclear, ask: "Technical audience or executive/non-technical?"

### Numbered flow edges (for non-technical mode)
Instead of technical labels, show flow order with circled numbers:
- Flow A: ① → ② → ③ → ④ (white circled numbers)
- Flow B: ❶ → ❷ → ❸ → ❹ (black circled numbers for second flow)

Use edge labels: `value="①"` with `fontSize=14;fontStyle=1;labelBackgroundColor=#ffffff;`

## Companion Guide

After generating the .drawio file, also generate a markdown guide:
- Same filename with `.md` extension
- Contents: diagram title, flow description (numbered steps), service list with purpose, key design decisions

## Two-Step Edit Approach
After generating the initial .drawio file:
1. **Export to PNG** using the draw.io CLI (see Export section)
2. **Review the PNG** visually — check for empty/broken icons, overlapping edges, misaligned labels
3. **Fix issues** in the .drawio XML and re-export

This catches rendering problems (wrong stencil names, broken styles) that are invisible in raw XML.

## Icon Name Gotchas — CRITICAL
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

**Fallback for unmapped services:** If a service is NOT found in any reference file, use this generic AWS cloud icon with the service name as label:
```
sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor=#232F3E;strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.general_AWScloud
```
Never render an unknown service as a plain colored rectangle with no label.

## Validation Step

After generating XML, verify:
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

## Export

For PNG/SVG/PDF export using draw.io Desktop CLI:

### Multi-page Diagrams
For complex architectures, use multiple pages in one .drawio file:
```xml
<mxfile>
  <diagram id="overview" name="Overview">...</diagram>
  <diagram id="networking" name="Networking Detail">...</diagram>
  <diagram id="data-flow" name="Data Flow">...</diagram>
</mxfile>
```
- Page 1: High-level overview (service-level icons only)
- Page 2+: Detail views (resource-level icons, subnet layouts, etc.)

### Legend / Title Block
Place in top-left corner, inside the background rectangle:
```xml
<mxCell value="&lt;b&gt;Diagram Title&lt;/b&gt;&lt;br&gt;Author | Date | Version" style="text;html=1;align=left;verticalAlign=top;whiteSpace=wrap;rounded=0;fontSize=14;spacing=8;" vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="300" height="50" as="geometry" />
</mxCell>
```

### PNG Export Background Fix
Place a `#F5F5F5` rectangle covering the entire diagram as the bottom-most element to prevent black background on export.

### Export CLI

| Platform | CLI Path |
|----------|----------|
| macOS | `/Applications/draw.io.app/Contents/MacOS/draw.io` |
| Linux | `drawio` (on PATH via snap/apt) |
| Windows | `"C:\Program Files\draw.io\draw.io.exe"` |

```bash
<CLI> -x -f <format> -e -b 10 -o <output> <input>
```

Flags: `-x` export, `-f` format (png/svg/pdf), `-e` embed diagram XML, `-b 10` border

Exported files use double extension: `name.drawio.png` — signals embedded XML, re-editable in draw.io.

## XML Well-formedness (CRITICAL)

- **NEVER include XML comments (`<!-- -->`)** — they cause parse errors
- Escape special characters: `&amp;` `&lt;` `&gt;` `&quot;`
- Always use unique `id` values for each mxCell
- Every edge MUST have `<mxGeometry relative="1" as="geometry" />` as child
- Root structure requires cells `id="0"` (root) and `id="1"` (default layer, parent="0")

## Official Reference

- XML reference: https://raw.githubusercontent.com/jgraph/drawio-mcp/main/shared/xml-reference.md
- Style reference: https://raw.githubusercontent.com/jgraph/drawio-mcp/main/shared/style-reference.md
