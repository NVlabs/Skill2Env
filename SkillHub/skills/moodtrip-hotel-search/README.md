# MoodTrip Hotel Search Skill

A Claude AI skill for searching, comparing, evaluating, and booking hotels through the [MoodTrip.ai](https://moodtrip.ai) MCP server.

## What It Does

This skill connects to `https://api.moodtrip.ai/api/mcp-http` and gives Claude (or any MCP-compatible agent) the ability to:

- **Search hotels** by destination, dates, budget, and natural language ("romantic getaway with rooftop bar")
- **Compare** hotels side-by-side with ratings, prices, and amenities
- **View reviews** with AI-powered sentiment analysis
- **Explore rooms** by description or photo upload
- **Track pricing trends** for cities and specific hotels
- **Hand off booking** via direct booking links to moodtrip.ai

## Tools Covered

| Tool | Purpose |
|------|---------|
| `searchHotelsWithRates` | Search with real-time pricing |
| `searchHotelsSemanticQuery` | AI-powered natural language search |
| `quickHotelSearch` | Simplified single-room search |
| `findHotels` | Browse hotels without pricing |
| `getHotelDetails` | Full hotel info + optional pricing |
| `getHotelReviews` | Guest reviews + sentiment analysis |
| `askHotelQuestion` | AI Q&A about a specific hotel |
| `searchRooms` | Visual/text room search |
| `summarizeResults` | AI summary of search results |
| `getHotelPriceIndex` | Hotel price trends |
| `getCityPriceIndex` | City-level price trends |
| `relaxConstraints` | Broaden a failed search |

Plus 3 optional Agent Builder tools (`build_booking_link`, `search`, `fetch`).

## Installation

### Option 1: ClawHub
Import directly from [ClawHub](https://clawhub.com) — search for `moodtrip-hotel-search`.

### Option 2: Claude Project
Copy the contents of `SKILL.md` into your Claude Project's custom instructions.

### Option 3: .skill file
Download `moodtrip-hotel-search.skill` from [Releases](../../releases) and import it into Claude.

## MCP Server

- **Endpoint**: `https://api.moodtrip.ai/api/mcp-http`
- **Protocol**: MCP Streamable HTTP (JSON-RPC 2.0)
- **Auth**: Public for search (no API key needed). OAuth 2.1 optional for session tracking.
- **Booking**: Link-based handoff — user completes booking on moodtrip.ai

## Quick Start

No setup needed. The MCP server is live and free to call for search operations.

To connect from Claude Desktop, add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "moodtrip": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://api.moodtrip.ai/api/mcp-http"]
    }
  }
}
```

## Example Interactions

**Search with pricing:**
> "Find me hotels in Paris for May 1-4, under $200/night"

**Semantic search:**
> "Romantic boutique hotel with rooftop bar in Tel Aviv"

**Hotel deep-dive:**
> "Tell me more about the second hotel — reviews, photos, and is breakfast included?"

**Price intelligence:**
> "When is the cheapest time to visit London?"

## Data Source

Hotel inventory, pricing, and reviews are provided by [LiteAPI](https://www.liteapi.travel/).

## License

MIT-0 (No Attribution Required)

## Links

- [MoodTrip.ai](https://moodtrip.ai)
- [MCP Protocol](https://modelcontextprotocol.io)
- [ClawHub](https://clawhub.com)
