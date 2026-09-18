#!/usr/bin/env python3
"""AgentCore HTTP Runtime Template (FastAPI).

A minimal FastAPI-based AgentCore Runtime with:
- /invocations endpoint (SSE streaming)
- /ping health check
- MCPClient lifecycle management (startup/shutdown)
- Per-request Agent creation

Environment Variables:
    MODEL_ID: Bedrock model identifier (default: us.anthropic.claude-sonnet-4-5-20250929-v1:0)
    MCP_SERVER_URL: Streamable HTTP URL for MCP server (optional, empty = no MCP tools)
    SYSTEM_PROMPT: Agent system prompt (default: "You are a helpful AI assistant.")
    AWS_REGION: AWS region for Bedrock and CORS (default: us-east-1)

Usage:
    # Local development (rename file to use underscores for Python import)
    cp runtime-fastapi-template.py runtime_fastapi_template.py
    uvicorn runtime_fastapi_template:app --host 0.0.0.0 --port 8080 --reload

    # Deploy to AgentCore via CDK (see agentcore-runtime-deploy.md)
"""

import json
import logging
import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from strands import Agent
from strands.models.bedrock import BedrockModel
from strands.tools.mcp import MCPClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Configuration ---
MODEL_ID = os.environ.get("MODEL_ID", "us.anthropic.claude-sonnet-4-5-20250929-v1:0")
MCP_SERVER_URL = os.environ.get("MCP_SERVER_URL", "")
SYSTEM_PROMPT = os.environ.get("SYSTEM_PROMPT", "You are a helpful AI assistant.")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")


# --- Request Models ---
class MessagePart(BaseModel):
    type: str = "text"
    text: str


class Message(BaseModel):
    id: str = ""
    role: str
    content: str
    parts: list[MessagePart] = []


class ChatRequest(BaseModel):
    id: str  # Session ID
    user_id: str = ""
    messages: list[Message] = []


# --- Module-level singletons (created once, reused across requests) ---
model = BedrockModel(model_id=MODEL_ID, region_name=AWS_REGION)
_mcp_client: MCPClient | None = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Initialize MCPClient at startup, close on shutdown."""
    global _mcp_client
    if MCP_SERVER_URL:
        try:
            from mcp.client.streamable_http import streamable_http_client

            _mcp_client = MCPClient(lambda: streamable_http_client(url=MCP_SERVER_URL))
            logger.info(f"MCPClient initialized for {MCP_SERVER_URL}")
        except ImportError:
            logger.error("mcp package not installed. Install with: pip install mcp")
            raise
        except Exception:
            logger.exception(f"Failed to initialize MCPClient for URL: {MCP_SERVER_URL}")
            raise
    yield
    if _mcp_client:
        try:
            await _mcp_client.close()
        except Exception:
            logger.exception("Error closing MCPClient")


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"https://bedrock-agentcore.{AWS_REGION}.amazonaws.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
def ping():
    return {"status": "Healthy"}


@app.post("/invocations")
async def invocations(request: ChatRequest):
    """Create a per-request Agent and stream SSE response."""
    user_message = request.messages[-1].content if request.messages else ""

    tools: list = [_mcp_client] if _mcp_client else []
    agent = Agent(
        system_prompt=SYSTEM_PROMPT,
        model=model,
        tools=tools,
    )

    async def event_generator():
        yield f"data: {json.dumps({'type': 'start', 'session_id': request.id})}\n\n"
        try:
            async for event in agent.stream_async(user_message):
                if "data" in event:
                    text = event.get("data", "")
                    if text:
                        yield f"data: {json.dumps({'type': 'text-delta', 'delta': text})}\n\n"
            yield f"data: {json.dumps({'type': 'finish', 'session_id': request.id})}\n\n"
        except Exception as e:
            logger.exception(f"Streaming error for session {request.id}")
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
