# PICT Examples Reference

> **Note**: This is a placeholder file. Comprehensive examples are coming soon!
> 
> For now, check out the [examples directory](../examples/) for complete real-world examples.

## Available Examples

### Complete Examples
- **[ATM System Testing](../examples/atm-specification.md)**: Comprehensive banking ATM system with 31 test cases

### Coming Soon

#### Software Testing
- Function testing with multiple parameters
- API endpoint testing
- Database query validation
- Algorithm testing

#### Web Applications
- Form validation
- User authentication
- E-commerce checkout
- Shopping cart operations

#### Configuration Testing
- System configurations
- Feature flags
- Environment settings
- Browser compatibility

#### Mobile Testing
- Device and OS combinations
- Screen sizes
- Network conditions
- Permissions

## Pattern Library (Coming Soon)

### Common Constraint Patterns

```
# Dependency constraints
IF [FeatureA] = "Enabled" THEN [FeatureB] = "Enabled";

# Exclusive options
IF [PaymentMethod] = "Cash" THEN [InstallmentPlan] = "None";

# Platform limitations
IF [OS] = "iOS" THEN [Browser] IN {Safari, Chrome};

# Environment restrictions
IF [Environment] = "Production" THEN [LogLevel] <> "Debug";
```

### Boundary Value Patterns

```
# Numeric boundaries
Age: 0, 17, 18, 64, 65, 100

# Size categories
FileSize: 0KB, 1KB, 1MB, 100MB, 1GB

# Time periods
Duration: 0s, 1s, 30s, 60s, 3600s
```

### Negative Testing Patterns

```
# Invalid inputs (using ~ prefix in some PICT variants)
Email: Valid, Invalid, Empty, TooLong
Password: Strong, Weak, Empty, SpecialChars

# Error conditions
NetworkStatus: Connected, Slow, Disconnected, Timeout
```

## Contributing Examples

Have an example to share? We'd love to include it!

1. Create your example following the structure in [examples/README.md](../examples/README.md)
2. Include:
   - Original specification
   - PICT model
   - Test cases with expected outputs
   - Learning points
3. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.

## External Resources

- [Pairwise Testing Tutorial](https://www.pairwisetesting.com/)
- [NIST Combinatorial Testing Resources](https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software)
- [Microsoft PICT Examples](https://github.com/microsoft/pict/tree/main/doc)
