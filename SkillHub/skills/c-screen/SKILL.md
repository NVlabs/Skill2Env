---
name: c-screen
description: Capture screenshots and extract text via OCR using `peekaboo`, and capture webcam images using `camsnap`. Enables visual analysis of screen content and camera input.
tags: [screenshot, ocr, webcam, peekaboo, camsnap, vision]
---

## What This Skill Does

Enables Claude to take screenshots, extract text from the screen via OCR, and capture webcam images for visual analysis using `peekaboo` and `camsnap`.

## Available CLI Tools

### `peekaboo` — Screenshots & OCR

```bash
# Take a full screenshot and save to file
peekaboo screenshot --output ~/Desktop/screen.png

# Take screenshot and extract all text via OCR
peekaboo ocr

# OCR a specific region (x, y, width, height)
peekaboo ocr --region 0,0,1280,720

# Screenshot a specific window by app name
peekaboo screenshot --app "Safari" --output window.png

# Screenshot and pipe to stdout for immediate analysis
peekaboo screenshot --stdout
```

### `camsnap` — Webcam Capture

```bash
# Capture a single webcam frame
camsnap --output ~/Desktop/photo.jpg

# Capture with a specific camera device
camsnap --device 0 --output shot.jpg

# Capture and print file path
camsnap --output /tmp/cam.jpg && echo "Saved"
```

## Usage Guidelines

- Use `peekaboo ocr` when the user wants text extracted from the screen
- Use `camsnap` only when the user explicitly wants a webcam image
- After capturing, read the image file to analyze its contents visually

## Notes

- macOS screen recording permission required for `peekaboo`
- Camera permission required for `camsnap`
- OCR accuracy depends on font size and screen resolution
