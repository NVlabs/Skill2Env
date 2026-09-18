# NotebookLM Command Reference

## Authentication

```bash
python scripts/auth_manager.py status --profile default
python scripts/auth_manager.py setup --profile work
python scripts/auth_manager.py reauth --profile work
python scripts/auth_manager.py clear --profile work
python scripts/auth_manager.py clear --all-profiles
python scripts/auth_manager.py profiles
```

## Notebook Library

```bash
python scripts/notebook_manager.py list
python scripts/notebook_manager.py add --url "https://notebooklm.google.com/notebook/..." --name "Notebook Name" --description "What this notebook contains" --topics "topic1,topic2"
python scripts/notebook_manager.py activate --id notebook-id
python scripts/notebook_manager.py search --query "keyword"
python scripts/notebook_manager.py remove --id notebook-id
python scripts/notebook_manager.py stats
```

## Ask NotebookLM

```bash
# Single ask (active notebook)
python scripts/ask_question.py --question "What are the key implementation details?"

# Ask by notebook ID / URL
python scripts/ask_question.py --question "Summarize auth flow" --notebook-id notebook-id
python scripts/ask_question.py --question "What is covered here?" --notebook-url "https://notebooklm.google.com/notebook/..."

# Batch ask
python scripts/ask_question.py --questions "q1||q2||q3" --notebook-id notebook-id
python scripts/ask_question.py --questions-file ./questions.txt --notebook-id notebook-id

# Compare one question across notebooks
python scripts/ask_question.py --question "What changed this week?" --compare-notebook-ids "notebook-a,notebook-b"

# Save structured export
python scripts/ask_question.py --question "Summarize" --notebook-id notebook-id --export-format markdown --save-notes
```

## Remote NotebookLM Operations

```bash
# List account notebooks
python scripts/remote_manager.py list-remote --profile work

# Create notebook remotely
python scripts/remote_manager.py create-remote --name "My Notebook" --description "What this notebook contains" --topics "topic1,topic2"
python scripts/remote_manager.py create-remote --name "My Notebook" --skip-library
python scripts/remote_manager.py create-remote --name "My Notebook" --dry-run

# List sources
python scripts/remote_manager.py list-sources --notebook-id notebook-id

# Add sources
python scripts/remote_manager.py add-source --notebook-id notebook-id --text "Some source text"
python scripts/remote_manager.py add-source --notebook-id notebook-id --url "https://example.com"
python scripts/remote_manager.py add-source --notebook-id notebook-id --file "/path/to/file.pdf"
python scripts/remote_manager.py add-source --notebook-id notebook-id --dir "/path/to/source-folder" --recursive
python scripts/remote_manager.py add-source --notebook-id notebook-id --dir "/path/to/source-folder" --include-ext "md,txt" --exclude "*.tmp" --max-size "10MB" --modified-since "7d"
python scripts/remote_manager.py add-source --notebook-id notebook-id --dir "/path/to/source-folder" --copy-to-temp
python scripts/remote_manager.py add-source --notebook-id notebook-id --dir "/path/to/source-folder" --dry-run

# Delete sources
python scripts/remote_manager.py delete-source --notebook-id notebook-id --source-title "source title"
python scripts/remote_manager.py delete-source --notebook-id notebook-id --source-title "temp" --contains --all-matches
python scripts/remote_manager.py delete-source --notebook-id notebook-id --source-title "temp" --contains --all-matches --dry-run

# Sync local desired state to notebook
python scripts/remote_manager.py sync-sources --notebook-id notebook-id --dir "/path/to/source-folder" --recursive
python scripts/remote_manager.py sync-sources --notebook-id notebook-id --dir "/path/to/source-folder" --recursive --delete-missing
python scripts/remote_manager.py sync-sources --notebook-id notebook-id --manifest ./source-manifest.json --dry-run
```

## Common Options

Use with `ask_question.py` and `remote_manager.py`:

```bash
--profile work          # Named auth profile
--retries 3             # Retry transient browser failures
--artifacts-dir /tmp/x  # Screenshot/HTML dump directory
--show-browser          # Show browser window for debugging
```
