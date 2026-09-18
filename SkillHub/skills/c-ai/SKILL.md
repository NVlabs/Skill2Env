---
name: c-ai
description: Query LLMs from the CLI — pipe text for summarization, chat interactively, use local or cloud models with llm or aichat.
tags: [ai, llm, summarize, chat]
---

# AI / LLM Tools

## llm (Simon Willison)

```bash
# Quick prompt
llm "What is the capital of France?"

# Pipe text for processing
cat article.txt | llm "Summarize this in 3 bullet points"
git diff | llm "Write a commit message for these changes"
pbpaste | llm "Fix the grammar in this text"

# Interactive chat
llm chat

# Use specific model
llm -m claude-3.5-sonnet "Explain quantum computing"
llm -m gpt-4o "Review this code"

# List available models
llm models

# Install model plugins
llm install llm-claude-3
llm install llm-ollama    # local models

# View prompt/response history
llm logs list
llm logs last
```

## aichat

```bash
# Quick prompt
aichat "Explain Docker in simple terms"

# Pipe input
cat code.py | aichat "Find bugs in this code"

# Interactive REPL
aichat

# Shell assistant (generates and runs commands)
aichat -e "find all files larger than 100MB"

# Specific model
aichat -m claude-3.5-sonnet "Hello"

# List models
aichat --list-models
```

## Guidelines

- Use `llm` for piping text through LLMs (summarize, translate, analyze)
- Use `aichat -e` for generating shell commands from natural language
- Both tools store API keys locally — set up once with auth commands
- `llm` has the richest plugin ecosystem (100+ model providers)
- `aichat` is faster (Rust) and has built-in RAG support
- These tools use separate API keys from Claude Code — user pays per token
