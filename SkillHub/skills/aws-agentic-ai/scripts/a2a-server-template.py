#!/usr/bin/env python3
"""AgentCore A2A Server Template.

Deploys as an A2A protocol Runtime on AgentCore.
Port 9000, root endpoint /, Agent Card at /.well-known/agent-card.json.

Usage:
    # Local development
    python a2a-server-template.py

    # Deploy to AgentCore
    pip install strands-agents[a2a] strands-agents-tools fastapi uvicorn
    agentcore configure -e a2a-server-template.py --protocol A2A
    agentcore deploy
"""

import logging
import os

import uvicorn
from fastapi import FastAPI
from strands import Agent
from strands.multiagent.a2a import A2AServer
from strands_tools.calculator import calculator

logging.basicConfig(level=logging.INFO)

runtime_url = os.environ.get("AGENTCORE_RUNTIME_URL", "http://127.0.0.1:9000/")

strands_agent = Agent(
    name="Calculator Agent",
    description="A calculator agent that can perform basic arithmetic operations.",
    tools=[calculator],
    callback_handler=None,
)

a2a_server = A2AServer(
    agent=strands_agent,
    http_url=runtime_url,
    serve_at_root=True,  # AgentCore A2A contract requires root path /
)

app = FastAPI()


@app.get("/ping")
def ping():
    return {"status": "Healthy"}


app.mount("/", a2a_server.to_fastapi_app())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
