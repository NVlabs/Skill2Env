# Contributing to pypict-claude-skill

Thank you for your interest in contributing to the PICT Test Designer Claude Skill! This document provides guidelines and instructions for contributing.

## Ways to Contribute

### 1. Add Examples
- Real-world test scenarios from different domains
- Industry-specific testing patterns
- Complex constraint scenarios
- Edge cases and advanced usage

### 2. Improve Documentation
- Fix typos or unclear explanations
- Add tutorials or guides
- Translate documentation
- Improve code comments

### 3. Enhance the Skill
- Optimize test case generation
- Add new constraint patterns
- Improve expected output determination
- Extend domain support

### 4. Report Issues
- Bug reports
- Feature requests
- Documentation gaps
- Usability improvements

### 5. Share Use Cases
- Blog posts about using the skill
- Video tutorials
- Workshop materials
- Success stories

## Getting Started

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/pypict-claude-skill.git
   cd pypict-claude-skill
   ```

3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/originalowner/pypict-claude-skill.git
   ```

### Create a Branch

Create a descriptive branch name:
```bash
git checkout -b feature/add-ecommerce-example
# or
git checkout -b fix/typo-in-readme
# or
git checkout -b docs/improve-installation-guide
```

## Contribution Guidelines

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn and grow

### Quality Standards

#### For Examples
- Include complete specification/requirements
- Provide clear PICT model
- Generate comprehensive test cases
- Add expected outputs
- Document key learning points
- Follow the existing example structure

#### For Documentation
- Use clear, concise language
- Include code examples where helpful
- Test all commands and code snippets
- Follow markdown best practices
- Check spelling and grammar

#### For Skill Improvements
- Maintain backward compatibility when possible
- Add comments explaining complex logic
- Update documentation to reflect changes
- Include examples demonstrating new features
- Test thoroughly before submitting

### File Structure

When adding examples:
```
examples/
├── your-example-name/
│   ├── README.md           # Overview and learning points
│   ├── specification.md    # Original requirements
│   ├── pict-model.txt     # Generated PICT model
│   └── test-plan.md       # Complete test plan
└── README.md              # Update to list your example
```

### Commit Messages

Write clear, descriptive commit messages:

```bash
# Good
git commit -m "Add e-commerce checkout testing example"
git commit -m "Fix typo in installation instructions"
git commit -m "Improve constraint generation for negative testing"

# Not ideal
git commit -m "Update files"
git commit -m "Fix stuff"
git commit -m "WIP"
```

### Pull Request Process

1. **Update documentation** if you're changing functionality
2. **Add tests/examples** if you're adding features
3. **Update README.md** if you're adding examples or major features
4. **Ensure quality**:
   - Check for typos
   - Test all examples
   - Verify markdown renders correctly
   - Ensure links work

5. **Submit PR** with a clear description:
   ```markdown
   ## Description
   Brief description of what this PR does
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Example addition
   
   ## Testing
   How was this tested?
   
   ## Related Issues
   Fixes #123
   ```

6. **Respond to feedback** promptly and professionally

## Example Contribution Workflow

### Adding a New Example

1. Create your branch:
   ```bash
   git checkout -b example/api-testing
   ```

2. Add your files to `examples/`:
   ```bash
   mkdir examples/api-testing
   # Create your specification, model, and test plan
   ```

3. Update `examples/README.md`:
   ```markdown
   ## API Testing Example
   Demonstrates PICT testing for REST API endpoints...
   ```

4. Commit your changes:
   ```bash
   git add examples/api-testing/
   git add examples/README.md
   git commit -m "Add REST API testing example"
   ```

5. Push to your fork:
   ```bash
   git push origin example/api-testing
   ```

6. Create a Pull Request on GitHub

### Fixing Documentation

1. Create your branch:
   ```bash
   git checkout -b docs/clarify-installation
   ```

2. Make your changes

3. Commit and push:
   ```bash
   git commit -m "Clarify installation steps for Windows users"
   git push origin docs/clarify-installation
   ```

4. Create a Pull Request

## Review Process

1. **Automated checks** (if configured) will run
2. **Maintainer review** typically within 1-2 weeks
3. **Feedback and iteration** may be requested
4. **Approval and merge** once all criteria met

## Recognition

Contributors will be:
- Listed in the repository's contributors
- Mentioned in release notes (for significant contributions)
- Credited in the documentation where appropriate

## Questions?

- Open an issue for general questions
- Tag your issue with `question`
- Be patient - we're all volunteers!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Every contribution, no matter how small, helps make this skill better for everyone. We appreciate your time and effort! 🙏
