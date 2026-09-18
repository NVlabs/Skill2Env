---
name: c-tracking
description: Track packages across UPS, FedEx, USPS, and DHL using the `ordercli` CLI. Look up tracking numbers, get current status, estimated delivery dates, and shipment history without visiting carrier websites.
tags: [tracking, shipping, packages, ups, fedex, usps, dhl, delivery]
---

## What This Skill Does

Uses `ordercli` to look up package tracking information across all major carriers. Returns current status, location, and estimated delivery without opening a browser.

## CLI Tool: `ordercli`

### Common Commands

```bash
# Track a package (carrier auto-detected)
ordercli track 1Z999AA10123456784

# Specify carrier explicitly
ordercli track --carrier ups 1Z999AA10123456784
ordercli track --carrier fedex 123456789012
ordercli track --carrier usps 9400111899223397623472
ordercli track --carrier dhl 1234567890

# Get full shipment history/events
ordercli track --history 1Z999AA10123456784

# Track multiple packages
ordercli track 1Z999AA10123456784 9400111899223397623472
```

### Supported Carriers

`ups`, `fedex`, `usps`, `dhl`

## Usage Guidelines

1. If the user provides a tracking number, attempt auto-detection first before specifying a carrier.
2. Show: current status, last known location, and estimated delivery date.
3. If tracking fails or carrier is unrecognized, ask the user to confirm the carrier name.
4. Use `--history` when the user asks for a full timeline of events.

## Notes

- Tracking numbers must be exact — no spaces or dashes unless the carrier format requires them.
- Some carriers have delayed updates; results reflect the last carrier scan.
