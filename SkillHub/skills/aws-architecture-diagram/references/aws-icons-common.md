# AWS Icons: General, Groups & Arrows

## General Resources (standalone shapes)
fillColor: `#232F3D` | strokeColor: `none`

| shape suffix | Display Name |
|-------------|-------------|
| `client` | Client / Browser |
| `traditional_server` | Traditional Server |
| `generic_firewall` | Firewall |
| `users` | Users |
| `user` | User |
| `mobile_client` | Mobile Client |
| `disk` | Disk |
| `document` | Document |
| `documents` | Documents |
| `email_2` | Email |
| `forums` | Forums |
| `gear` | Gear |
| `internet` | Internet |
| `internet_alt1` | Internet (alt) |
| `internet_alt2` | Internet Globe |
| `multimedia` | Multimedia |
| `office_building` | Office Building |
| `saml_token` | SAML Token |
| `sdk` | SDK |
| `servers` | Servers |
| `source_code` | Source Code |
| `tape` | Tape |
| `thumbs_up` | Thumbs Up |
| `thumbs_down` | Thumbs Down |

## Group Containers
All groups: `fillColor=none` | Use with `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.<grIcon>`

| grIcon | strokeColor | fontColor | Display Name |
|--------|-------------|-----------|-------------|
| `group_aws_cloud_alt` | `#232F3E` | `#232F3E` | AWS Cloud |
| `group_aws_cloud` | `#232F3E` | `#232F3E` | AWS Cloud (alt) |
| `group_region` | `#00A4A6` | `#147EBA` | Region |
| `group_availability_zone` | `#007FAA` | `#007FAA` | Availability Zone |
| `group_security_group` | `#DD344C` | `#DD344C` | Security Group |
| `group_vpc` | `#8C4FFF` | `#8C4FFF` | VPC |
| `group_private_subnet` | `#147EBA` | `#147EBA` | Private Subnet |
| `group_public_subnet` | `#248814` | `#248814` | Public Subnet |
| `group_account` | `#CD2264` | `#CD2264` | AWS Account |
| `group_corporate_data_center` | `#7D8998` | `#5A6C86` | Corporate DC |
| `group_on_premise` | `#5A6C86` | `#5A6C86` | On-Premise |
| `group_elastic_beanstalk` | `#D86613` | `#D86613` | Elastic Beanstalk |
| `group_ec2_instance_contents` | `#D86613` | `#D86613` | EC2 Instance |
| `group_spot_fleet` | `#D86613` | `#D86613` | Spot Fleet |
| `group_aws_step_functions_workflow` | `#CD2264` | `#CD2264` | Step Functions |
| `group_iot_greengrass` | `#7AA116` | `#3F8624` | IoT Greengrass |

## Generic Groups (no grIcon)
```
fillColor=none;strokeColor=#5A6C86;dashed=1;verticalAlign=top;fontStyle=0;fontColor=#5A6C86;whiteSpace=wrap;html=1;
```

## Edge Styles
```
edgeStyle=orthogonalEdgeStyle;html=1;endArrow=block;elbow=vertical;startArrow=none;endFill=1;strokeColor=#545B64;rounded=0;
```

## Two Icon Patterns — CRITICAL RULE

### Pattern 1: Service-level (resourceIcon)
- Uses `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.<name>`
- **MUST have `strokeColor=#ffffff`** — without it, the white glyph won't show
- Size: 78x78

### Pattern 2: Resource-level (standalone shape)
- Uses `shape=mxgraph.aws4.<name>` directly
- **MUST have `strokeColor=none`** — using #ffffff breaks these
- Size: 78x78 or 48x48

**Confusing these two patterns guarantees broken icons.**

## PNG Export Background Fix
Place a light gray rectangle covering the entire diagram as background layer:
```
rounded=1;whiteSpace=wrap;fillColor=#F5F5F5;strokeColor=#E0E0E0;arcSize=2;
```
This prevents black background on areas outside groups when exporting to PNG.

## Base Template
```xml
<mxfile host="app.diagrams.net">
  <diagram id="diagram-1" name="Architecture">
    <mxGraphModel dx="2800" dy="1600" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="2400" pageHeight="1400" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```
