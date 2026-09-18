# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Additional real-world examples (e-commerce, API testing, mobile apps)
- Enhanced PICT syntax reference documentation
- Improved helper scripts for PICT model generation
- Integration with test management tools
- Support for higher-order combinatorial testing (3-way, 4-way)

## [1.0.2] - 2025-10-19

### Added
- **Automotive Gearbox Control System example** - Advanced PICT example for safety-critical systems
- `examples/gearbox-specification.md` - Comprehensive 10-section specification (3,600+ words)
  - System components (sensors, actuators, controls)
  - Operating modes (Manual, Sport, Eco)
  - Functional requirements and safety features
  - Error handling and fault tolerance
  - Performance, environmental, and integration requirements
- `examples/gearbox-test-plan.md` - Complete PICT test plan
  - 12 parameters with complex interdependencies
  - 14 business rules and safety constraints
  - 40 test cases from ~159 billion combinations (99.999999975% reduction)
  - Expected outputs with detailed system responses
  - Priority-based execution plan, coverage analysis, traceability matrix
  - Risk assessment for safety-critical scenarios

### Changed
- Updated `examples/README.md` with gearbox example section
- Added advanced constraint modeling patterns documentation
- Expanded learning points with multi-mode testing and fault injection examples

### Documentation
- Comprehensive gearbox specification covering all aspects of transmission control
- Detailed test plan demonstrating advanced PICT usage
- Learning material for complex parameter interactions and safety constraints

## [1.0.1] - 2025-10-19

### Added
- **Claude Code Plugin Marketplace support** - Users can now install via `/plugin` commands
- `.claude-plugin/marketplace.json` - Marketplace catalog for plugin discovery
- `.claude-plugin/plugin.json` - Complete plugin metadata with keywords and repository info
- Plugin installation as Method 1 in README.md (easiest installation method)

### Changed
- Updated README.md with plugin marketplace installation instructions
- Renumbered installation methods (now 5 methods: marketplace, git clone, submodule, minimal zip, full zip)
- Updated author information: Omar Kamal Hosney <omar.wasat@gmail.com>

### Improved
- Easier installation process via plugin marketplace
- Automated updates when using plugin marketplace
- Better discoverability through Claude Code's plugin system

## [1.0.0] - 2025-10-19

### Added
- Initial release of PICT Test Designer skill
- Core functionality for test case design using PICT methodology
- Comprehensive ATM system testing example
- Installation guide for Claude Code CLI and Desktop
- MIT License with proper attributions
- Contributing guidelines
- Documentation structure (README, SKILL.md, examples)
- GitHub Actions CI workflow
- Example directory with ATM specification and test plan
- **Minimal installation package (9.3 KB)** with essential files only
- GitHub Release v1.0.0 with downloadable assets
- Multiple installation methods (git clone, submodule, minimal ZIP, full ZIP)

### Features
- Automated parameter identification from requirements
- PICT model generation with constraints
- Expected output determination
- Pairwise test case generation
- Support for multiple testing domains
- Comprehensive documentation and examples
- 80-99% test case reduction while maintaining coverage

### Fixed
- Corrected installation instructions (removed non-existent CLI commands)
- Updated to use proper manual installation via `.claude/skills/` directory
- Removed CLAUDE.md from version control (now user-specific)

### Documentation
- README.md: Corrected installation methods with 4 options
- QUICKSTART.md: Updated with accurate installation steps
- releases/README.md: Guide for using minimal package
- README-INSTALL.txt: User-friendly guide included in minimal ZIP

### Credits
- Built on Microsoft PICT
- Uses pypict Python bindings by Kenichi Maehashi
- Designed for Claude AI by Anthropic

## Version History

### Versioning Scheme

- **Major version (X.0.0)**: Incompatible API changes or major feature additions
- **Minor version (0.X.0)**: New features in a backward-compatible manner
- **Patch version (0.0.X)**: Backward-compatible bug fixes

### Release Types

- **[Unreleased]**: Changes in development but not yet released
- **[Version]**: Released version with date

### Change Categories

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security vulnerability fixes

---

## How to Contribute to Changelog

When submitting a pull request, add your changes to the [Unreleased] section under the appropriate category (Added, Changed, Fixed, etc.).

Example:
```markdown
## [Unreleased]

### Added
- New example for mobile app testing (#42)

### Fixed
- Typo in installation instructions (#38)
```

The maintainers will move items from [Unreleased] to a versioned release when publishing a new version.
