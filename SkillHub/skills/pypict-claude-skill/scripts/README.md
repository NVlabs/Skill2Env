# Scripts

This directory contains helper scripts for working with PICT models and test cases.

## Available Scripts

### pict_helper.py

A Python utility for:
- Generating PICT models from JSON configuration
- Formatting PICT output as markdown tables
- Parsing PICT output into JSON

**Installation:**
```bash
pip install pypict --break-system-packages
```

**Usage:**

1. **Generate PICT model from config:**
   ```bash
   python pict_helper.py generate config.json > model.txt
   ```

2. **Format PICT output as markdown:**
   ```bash
   python pict_helper.py format output.txt
   ```

3. **Parse PICT output to JSON:**
   ```bash
   python pict_helper.py parse output.txt
   ```

**Example config.json:**
```json
{
    "parameters": {
        "Browser": ["Chrome", "Firefox", "Safari"],
        "OS": ["Windows", "MacOS", "Linux"],
        "Memory": ["4GB", "8GB", "16GB"]
    },
    "constraints": [
        "IF [OS] = \"MacOS\" THEN [Browser] <> \"IE\"",
        "IF [Memory] = \"4GB\" THEN [OS] <> \"MacOS\""
    ]
}
```

## Future Scripts

We welcome contributions for:
- Test automation generators
- Export to test management tools (JIRA, TestRail)
- Integration with CI/CD pipelines
- Coverage analysis tools
- Constraint validation utilities

## Contributing

Have a useful script to share?

1. Add your script to this directory
2. Update this README with usage instructions
3. Add comments and examples in your script
4. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## Dependencies

Current scripts use:
- Python 3.7+
- pypict (optional, for direct PICT integration)

All dependencies should be clearly documented in each script.
