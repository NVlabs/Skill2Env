# PICT Syntax Reference

> **Note**: This is a placeholder file. Complete syntax documentation is coming soon!
> 
> For now, please refer to the official PICT documentation:
> - [Microsoft PICT on GitHub](https://github.com/microsoft/pict)
> - [PICT User Guide](https://github.com/microsoft/pict/blob/main/doc/pict.md)

## Quick Reference

### Basic Model Structure

```
# Parameters
ParameterName: Value1, Value2, Value3
AnotherParameter: ValueA, ValueB, ValueC

# Constraints (optional)
IF [ParameterName] = "Value1" THEN [AnotherParameter] <> "ValueA";
```

### Parameter Definition

```
ParameterName: Value1, Value2, Value3, ...
```

### Constraint Syntax

```
IF <condition> THEN <condition>;
```

### Operators

- `=` - Equal to
- `<>` - Not equal to
- `>` - Greater than
- `<` - Less than
- `>=` - Greater than or equal to
- `<=` - Less than or equal to
- `IN` - Member of set
- `AND` - Logical AND
- `OR` - Logical OR
- `NOT` - Logical NOT

### Example Constraints

```
# Simple constraint
IF [OS] = "MacOS" THEN [Browser] <> "IE";

# Multiple conditions
IF [Environment] = "Production" AND [LogLevel] = "Debug" THEN [Approved] = "False";

# Set membership
IF [UserRole] = "Guest" THEN [Permission] IN {Read, None};
```

## Coming Soon

Detailed documentation will include:
- Complete grammar specification
- Advanced features (sub-models, aliasing, seeding)
- Negative testing patterns
- Weight specifications
- Order specifications
- Examples for each feature

## Contributing

If you'd like to help complete this documentation:
1. Fork the repository
2. Add content to this file
3. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## External Resources

- [Official PICT Documentation](https://github.com/microsoft/pict/blob/main/doc/pict.md)
- [pypict Documentation](https://github.com/kmaehashi/pypict)
- [Pairwise Testing Explained](https://www.pairwisetesting.com/)
