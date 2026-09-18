# Examples

This directory contains real-world examples of using the PICT Test Designer skill.

## ATM System Testing Example

A comprehensive example demonstrating how to use PICT methodology to test a complex banking ATM system.

### Files

- **[atm-specification.md](atm-specification.md)**: Complete ATM system specification with 11 sections covering:
  - Functional requirements (withdrawals, deposits, transfers, etc.)
  - Hardware specifications (card readers, cash dispensers, displays)
  - Security requirements (encryption, authentication, physical security)
  - Network and connectivity requirements
  - Compliance and standards

- **[atm-test-plan.md](atm-test-plan.md)**: Complete test plan generated using the PICT skill, including:
  - PICT model with 8 parameters and 16 constraints
  - 31 optimized test cases (reduced from 25,920 possible combinations)
  - Expected outputs for each test case
  - Test execution guidelines
  - Coverage analysis
  - Risk-based prioritization

### Key Statistics

- **Total Parameters**: 8 (Transaction Type, Card Type, PIN Status, Account Type, Transaction Amount, Cash Availability, Network Status, Card Condition)
- **Exhaustive Combinations**: 25,920
- **PICT Test Cases**: 31
- **Reduction**: 99.88%
- **Coverage**: All pairwise (2-way) interactions
- **Constraints**: 16 business rules

### How to Use This Example

1. **Review the specification**: Read [atm-specification.md](atm-specification.md) to understand the system requirements

2. **Study the test plan**: Review [atm-test-plan.md](atm-test-plan.md) to see how the PICT skill converted requirements into test cases

3. **Try it yourself**: Ask Claude to analyze the specification:
   ```
   Using the pict-test-designer skill, analyze the ATM specification 
   and generate test cases for the security requirements
   ```

4. **Adapt for your needs**: Use this as a template for your own specifications

### Learning Points

This example demonstrates:

- **Parameter identification**: How to identify testable parameters from requirements
- **Equivalence partitioning**: Grouping values into meaningful categories
- **Constraint modeling**: Applying business rules to eliminate invalid combinations
- **Expected output determination**: Automatically determining what should happen for each test case
- **Test prioritization**: Organizing tests by risk and criticality
- **Traceability**: Linking test cases back to requirements

## Automotive Gearbox Control System Example

A sophisticated example demonstrating PICT methodology for testing a semi-automatic transmission control system with multiple operating modes and complex safety constraints.

### Files

- **[gearbox-specification.md](gearbox-specification.md)**: Comprehensive gearbox control system specification with 10 sections:
  - System components (sensors, actuators, controls)
  - Operating modes (Manual, Sport, Eco)
  - Functional requirements (shift logic, safety features)
  - Error handling and fault tolerance
  - Performance and reliability requirements
  - Environmental conditions and constraints

- **[gearbox-test-plan.md](gearbox-test-plan.md)**: Complete test plan with PICT methodology:
  - PICT model with 12 parameters and 14 constraints
  - 40 optimized test cases (from ~159 billion combinations)
  - Expected outputs with detailed system responses
  - Priority-based test execution plan
  - Coverage analysis and traceability matrix
  - Risk assessment for high-risk scenarios

### Key Statistics

- **Total Parameters**: 12 (Mode, Gear, Speed, RPM, Throttle, Brake, Shift Request, Temperature, Road Condition, Incline, Sensor Status, Hydraulic Pressure)
- **Exhaustive Combinations**: ~159,000,000,000 (159 billion)
- **PICT Test Cases**: 40
- **Reduction**: 99.999999975%
- **Coverage**: All pairwise (2-way) interactions
- **Constraints**: 14 complex business rules and safety constraints

### How to Use This Example

1. **Review the specification**: Read [gearbox-specification.md](gearbox-specification.md) for the complete system design

2. **Study the test plan**: Examine [gearbox-test-plan.md](gearbox-test-plan.md) to see complex constraint modeling

3. **Try it yourself**: Ask Claude to analyze specific scenarios:
   ```
   Using the pict-test-designer skill, analyze the gearbox specification
   and generate test cases for the safety features section
   ```

4. **Learn constraint modeling**: This example shows advanced constraint patterns for:
   - Mutually exclusive conditions (brake vs. throttle)
   - Physical limitations (gear ratios, speed limits)
   - Safety interlocks (reverse lockout, over-rev protection)
   - Environmental adaptations (ice, temperature, incline)

### Learning Points

This example demonstrates:

- **Complex parameter interactions**: 12-way parameter space with interdependencies
- **Advanced constraint modeling**: Physical, safety, and operational constraints
- **Multi-mode testing**: Different behaviors in Manual, Sport, and Eco modes
- **Fault injection testing**: Sensor failures, temperature extremes, hydraulic issues
- **Environmental testing**: Road conditions, incline, temperature variations
- **Safety-critical testing**: Over-rev protection, reverse lockout, hill start assist
- **Comprehensive traceability**: Complete mapping to specification requirements

### Additional Examples (Coming Soon)

- E-commerce checkout testing
- API endpoint testing
- Web form validation
- Mobile app configuration testing
- Database query testing

## Contributing Examples

Have a great example to share? We welcome contributions!

1. Fork the repository
2. Add your example to this directory
3. Include both the specification/requirements and the generated test plan
4. Update this README with a description
5. Submit a pull request

### Example Structure

When contributing, please include:
- Original specification or requirements document
- Generated PICT model
- Test cases with expected outputs
- Brief description of the domain and key learning points
