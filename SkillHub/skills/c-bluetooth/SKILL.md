---
name: c-bluetooth
description: Manage Bluetooth devices on macOS using the blucli (`blu`) CLI. List paired and available devices, connect to headphones/speakers/keyboards, and disconnect devices by name or MAC address.
tags: [bluetooth, hardware, macos, devices, audio]
---

## What This Skill Does

Manages Bluetooth device connections on macOS using `blu` (blucli). You can list available devices, connect to a device by name or MAC address, and disconnect active devices.

## CLI Tool: `blu`

### Common Commands

```bash
# List all paired/known devices
blu list

# Connect to a device (by name or MAC)
blu connect "AirPods Pro"
blu connect AA:BB:CC:DD:EE:FF

# Disconnect a device
blu disconnect "AirPods Pro"
blu disconnect AA:BB:CC:DD:EE:FF

# Check connection status
blu status
```

## Usage Guidelines

1. Run `blu list` first to identify the exact device name or MAC address.
2. Device names are case-sensitive — use the exact name from `blu list`.
3. If connecting by name fails, fall back to MAC address.
4. After connecting, confirm success by checking for a non-error exit code or running `blu status`.

## Notes

- `blu` only manages already-paired devices. New device pairing must be done via macOS System Settings.
- Some commands may require Bluetooth to be enabled in macOS before running.
- If `blu` is not installed: `brew install blucli`
