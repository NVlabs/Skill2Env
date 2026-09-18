# Research Workflow Example

Use this when the user is collecting papers, articles, books, datasets, slide decks, screenshots, or other mixed research sources into one vault.

## Commands

```bash
swarmvault init
swarmvault add https://arxiv.org/abs/2401.12345
swarmvault add 10.1145/1234567.1234568
swarmvault ingest ./paper.pdf
swarmvault ingest ./interview.mp3
swarmvault ingest https://www.youtube.com/watch?v=dQw4w9WgXcQ
swarmvault ingest ./book.epub
swarmvault ingest ./results.csv
swarmvault ingest ./analysis.xlsx
swarmvault ingest ./deck.pptx
swarmvault inbox import ./capture-bundle
swarmvault compile
swarmvault doctor
swarmvault query "What are the main claims and conflicts?"
swarmvault chat "What should I read next?"
swarmvault context build "Review the main claims and conflicts" --target "main claims" --budget 8000
swarmvault export ai --out ./exports/ai
swarmvault explore "What should I read next?" --steps 3
```

## What To Check

- `raw/sources/` contains normalized markdown captures for `add`
- `state/extracts/` contains PDF, DOCX, EPUB, CSV/TSV, XLSX, PPTX, audio, video, YouTube, or image extraction sidecars when relevant
- `wiki/graph/report.md` surfaces contradictions, surprise links, and benchmark data
- `swarmvault doctor` reports whether graph and retrieval artifacts are ready for query or handoff
- `wiki/outputs/` contains saved query and explore outputs
- `wiki/outputs/chat-sessions/` and `state/chat-sessions/` contain saved conversation state when multi-turn research questions should persist
- `wiki/context/` and `state/context-packs/` contain saved review packs when `context build` is used
- `wiki/exports/ai/` or the chosen export path contains static handoff files when `export ai` is used

## Guidance

- Use `swarmvault add` for research URLs and `swarmvault ingest` for direct local files.
- If image extraction is weak, verify that a real `visionProvider` is configured.
- If audio or video extraction is missing, verify that `tasks.audioProvider` points at a provider with `audio` capability. Local video also needs `ffmpeg`; public video URLs with `--video` need `yt-dlp`.
- Use `swarmvault context build` when another agent or future session needs a bounded evidence bundle for review.
- Use `swarmvault chat --resume <id>` when research follow-ups should keep their prior turns and citations together.
- Use `swarmvault export ai --out <dir>` when another static tool should read the compiled research wiki.
- Use `lint --conflicts` when the user specifically wants contradiction review.
