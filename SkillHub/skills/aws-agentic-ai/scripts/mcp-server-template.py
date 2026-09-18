#!/usr/bin/env python3
"""AgentCore MCP Server Template.

Deploys as an MCP protocol Runtime on AgentCore.
Port 8000, endpoint /mcp, Streamable HTTP transport.

Note: FastMCP handles the /mcp endpoint and MCP protocol automatically.
AgentCore's /ping health check is expected on port 8000 — verify that
FastMCP serves it, or add a custom health endpoint if needed.

Usage:
    # Local development
    python mcp-server-template.py

    # Deploy to AgentCore
    agentcore configure -e mcp-server-template.py --protocol MCP
    agentcore deploy
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(host="0.0.0.0", stateless_http=True)


@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


@mcp.tool()
def greet_user(name: str) -> str:
    """Greet a user by name."""
    return f"Hello, {name}!"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
