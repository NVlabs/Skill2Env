# CMSO Validation Rules

## What Is Validated

### Schema Checker (`schema_checker.py`)
1. **Class existence**: Is the class name a valid CMSO class?
2. **Property existence**: Is each property name defined in CMSO?
3. **Domain compatibility**: Is the property applied to the correct class? (warning, not error)

### Completeness Checker (`completeness_checker.py`)
1. **Required properties**: Must be present for the class to be minimally valid
2. **Recommended properties**: Should be present for a complete description
3. **Optional properties**: Nice to have, but not necessary

### Relationship Checker (`relationship_checker.py`)
1. **Property existence**: Is the object property defined in the ontology?
2. **Domain validity**: Is the subject class compatible with the property's domain?
3. **Range validity**: Is the object class compatible with the property's range?
4. **Subclass compatibility**: Subclasses are valid where parent classes are expected

## Error Types

| Error Type | Severity | Description |
|------------|----------|-------------|
| `unknown_class` | Error | Class not found in ontology |
| `unknown_property` | Error | Property not found in ontology |
| `domain_mismatch` | Warning | Property applied to wrong class |
| `range_mismatch` | Error | Object class not compatible with property range |
| `missing_required` | Error | Required property not provided |

## Interpreting Results

- **valid = true**: All checks passed (no errors; warnings are acceptable)
- **completeness_score**: 0.0 = nothing provided, 1.0 = everything provided
- **required_missing**: These should be addressed before the annotation is considered complete
- **recommended_missing**: Improve these for better data quality
- **unrecognized**: Properties provided that the ontology doesn't define (may indicate typos)

## Constraint Sources

Constraints in `cmso_constraints.json` are curated based on CMSO documentation and best practices.
They are not derived from OWL axioms (CMSO v0.0.1 does not include cardinality restrictions).
