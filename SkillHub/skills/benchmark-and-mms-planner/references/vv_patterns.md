# Verification And Validation Patterns

Use MMS to test implementation correctness, especially source terms, boundary conditions, Jacobians, and time integration. Use canonical benchmarks to test physical behavior against known solutions or community references.

Recommended evidence ladder:

1. Unit-level operator checks.
2. MMS with observed order.
3. Canonical benchmark.
4. Problem-specific conservation or balance laws.
5. Uncertainty propagation for input parameters.

Avoid claiming validation from convergence alone. Convergence shows the code approaches some solution; it does not show that the model is physically correct.

## Observed-order acceptance band

When checking observed order of accuracy against the formal (expected) order, the planner
reports `accept_observed_order_min` as a screening threshold. This is computed as a
*relative* tolerance on the formal order rather than a fixed absolute offset:

- `accept_observed_order_min = max(1.0, expected_order * (1 - frac))`
- `frac = 0.10` for high-risk claims, `0.20` otherwise.

A relative band keeps the strictness consistent across formal orders (a fixed absolute
offset such as `expected_order - 0.5` is far stricter in relative terms for high-order
schemes, e.g. 25% of a 2nd-order scheme but only 10% of a 5th-order scheme). The floor at
`1.0` prevents the threshold from dropping below first-order convergence (or going
negative). This is an engineering screening heuristic, not a certified bound: observed
order below the threshold is a flag to investigate (mesh not asymptotic, boundary/source
errors, limiter activation), not an automatic failure. For rigorous order verification use
a Richardson/GCI study with at least three systematically refined meshes.
