# Creating Prompts in Agent Platform

This guide provides instructions on how to create a new managed prompt in
Agent Platform.

## Create a Prompt (Tier M)

**Confirmation Required**: As a Tier M (Mutating) operation, the agent MUST
pause and present a confirmation prompt with the project, region, prompt display
name, and model before providing the creation code.

> [!IMPORTANT]
> **Interactive Confirmation Required (Tier M):** Before proceeding with prompt
> creation, you **MUST** present the proposed Python code in a confirmation
> prompt to the user with 'Yes' and 'No' options.
> **CRITICAL:** When presenting this confirmation prompt to the user, you MUST
> output it as a direct plain text response and stop tool execution immediately.
> Do NOT call any command execution or interactive tools in the same turn, as
> unexpected tool calls may be auto-replied by the simulation harness and cause
> an infinite loop. Yield immediately for the user's reply.

```python
import vertexai
from vertexai.preview import prompts
from vertexai.preview.prompts import Prompt

vertexai.init(project="PROJECT_ID", location="LOCATION_ID")

# Construct a local Prompt object. `prompt_name` is the display name shown
# in Agent Platform Studio; `prompt_data` is the prompt text/template
# (use `{variable_name}` placeholders for variables passed to
# `assemble_contents()`); `model_name` is the target model.
local_prompt = Prompt(
    prompt_name="my_new_prompt",
    prompt_data="Hello, how are you? {text}",
    model_name="gemini-2.5-pro",
)

# Persist the local Prompt as a new managed prompt resource. This creates
# the prompt AND its first version in a single call. The returned
# `persisted_prompt` is a Prompt object with `prompt_id` and `version_id`
# populated.
persisted_prompt = prompts.create_version(prompt=local_prompt)
print(f"Created prompt ID: {persisted_prompt.prompt_id}")
print(f"Version ID: {persisted_prompt.version_id}")
```
