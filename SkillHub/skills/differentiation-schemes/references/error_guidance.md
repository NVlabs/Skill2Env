# Truncation Error Guidance

Comprehensive guide for understanding and controlling discretization errors.

## Truncation Error Fundamentals

### Definition

Truncation error is the difference between the continuous operator and its discrete approximation:

```
τ = L[u] - L_h[u_h]

where:
  L[u] = continuous differential operator applied to exact solution
  L_h[u_h] = discrete operator applied to grid values
```

### Order of Accuracy

A scheme is pth-order accurate if:

```
τ = O(dx^p)  as  dx → 0

Meaning: τ ≤ C × dx^p for some constant C
```

| Order p | Error Reduction with dx/2 |
|---------|---------------------------|
| 1 | 2× |
| 2 | 4× |
| 3 | 8× |
| 4 | 16× |
| 6 | 64× |

## Error Estimation

### Taylor Expansion Method

For 2nd-order central first derivative:

```
f'(x) ≈ (f(x+dx) - f(x-dx)) / (2dx)

Taylor expand:
f(x+dx) = f(x) + dx f'(x) + (dx²/2) f''(x) + (dx³/6) f'''(x) + ...
f(x-dx) = f(x) - dx f'(x) + (dx²/2) f''(x) - (dx³/6) f'''(x) + ...

Subtract: f(x+dx) - f(x-dx) = 2dx f'(x) + (dx³/3) f'''(x) + ...

Divide: (f(x+dx) - f(x-dx)) / (2dx) = f'(x) + (dx²/6) f'''(x) + ...

Error = (dx²/6) f'''(x) + O(dx⁴)
```

### Leading Error Term

The coefficient of the leading error term matters:

| Scheme | Order | Leading Coefficient |
|--------|-------|---------------------|
| Central d/dx | 2 | dx²/6 × f''' |
| Central d²/dx² | 2 | dx²/12 × f'''' |
| 4th-order d/dx | 4 | dx⁴/30 × f''''' |
| Upwind d/dx | 1 | dx/2 × f'' |

## Practical Error Estimation

### Richardson Extrapolation

Compare solutions at different resolutions:

```
Solution with dx: u_h
Solution with dx/2: u_{h/2}

For pth-order scheme:
  u_h = u_exact + C × dx^p + O(dx^{p+1})
  u_{h/2} = u_exact + C × (dx/2)^p + O(dx^{p+1})

Subtract:
  u_h - u_{h/2} ≈ C × dx^p × (1 - 1/2^p)

Error estimate:
  |u_h - u_exact| ≈ |u_h - u_{h/2}| / (2^p - 1)
```

### Order Verification

```
e_h = ||u_h - u_exact||
e_{h/2} = ||u_{h/2} - u_exact||

Observed order: p_obs = log(e_h / e_{h/2}) / log(2)

Should match theoretical order p.
```

### Convergence Study

```python
def convergence_study(exact, solve, dx_list):
    """Compute errors and observed order."""
    errors = []
    for dx in dx_list:
        u = solve(dx)
        u_exact = exact(grid(dx))
        errors.append(np.linalg.norm(u - u_exact))

    orders = []
    for i in range(len(errors) - 1):
        ratio = errors[i] / errors[i+1]
        dx_ratio = dx_list[i] / dx_list[i+1]
        orders.append(np.log(ratio) / np.log(dx_ratio))

    return errors, orders
```

## Resolution Requirements

### Points Per Feature

Minimum grid points to resolve a feature:

| Feature | Min Points | Recommended |
|---------|------------|-------------|
| Wavelength | 5 | 10-20 |
| Boundary layer | 5 | 10 |
| Phase-field interface | 3 | 5-10 |
| Shock width | 2-3 | 5+ |
| Vortex | 5 | 10-20 |

### Nyquist Limit

For oscillatory solutions:

```
Minimum: dx < λ/2 (Nyquist)
Practical: dx < λ/10 to λ/20 for accuracy
```

### Error vs Resolution

```
Error ≈ C × (dx/L_feature)^p

where L_feature is the smallest feature size.

Example: 2nd-order scheme, L = 0.1, dx = 0.01
  Error ≈ C × (0.01/0.1)² = C × 0.01 = 1% of C

To get 0.01%: dx = 0.001
```

## Common Error Sources

### Spatial Discretization Error

```
Source: Finite difference approximation
Scales as: O(dx^p)
Control: Refine grid or use higher-order scheme
```

### Temporal Discretization Error

```
Source: Time integration scheme
Scales as: O(dt^q) for qth-order time scheme
Control: Reduce dt or use higher-order integrator
```

### Roundoff Error

```
Source: Floating-point arithmetic
Scales as: O(ε_machine / dx^p) for pth derivative
Warning: Can dominate for very fine grids!
```

### Iteration Error

```
Source: Incomplete convergence of iterative solvers
Control: Tighten solver tolerance
Rule: Solver tolerance < discretization error
```

## Error Balancing

### Time-Space Error Balance

For optimal efficiency:

```
Temporal error ≈ Spatial error

dt^q ≈ dx^p

For explicit parabolic (CFL): dt ~ dx²
  If time is O(dt), space is O(dx²) → balanced for 2nd-order

For explicit hyperbolic (CFL): dt ~ dx
  If time is O(dt), space is O(dx²) → space limits accuracy
```

### Cost-Accuracy Trade-off

| Scheme | Error | Cost | Efficiency |
|--------|-------|------|------------|
| 2nd-order | O(dx²) | O(1/dx^d) | Baseline |
| 4th-order | O(dx⁴) | O(1/dx^d) | Better for smooth |
| 6th-order | O(dx⁶) | O(1/dx^d) | Best for very smooth |

For same accuracy, higher order needs fewer points.

## Validation Strategies

### Manufactured Solutions

1. Choose smooth function: u(x,t) = sin(πx)cos(t)
2. Substitute into PDE: get source term
3. Solve with source
4. Compare to known u

**Advantages:**
- Known exact solution
- Tests all error sources
- Verifies implementation

### Grid Convergence

1. Solve on dx, dx/2, dx/4
2. Compute errors vs fine grid or analytical
3. Verify expected order

```
If order drops:
  - Bug in implementation
  - Solution not smooth enough
  - Boundary conditions limiting
  - Grid not fine enough yet
```

### Conservation Check

For conservation laws:

```
∫ u dx at t=0 should equal ∫ u dx at t=T (up to BCs)

If not conserved:
  - Non-conservative scheme
  - Discretization error
  - Boundary flux errors
```

## Troubleshooting

### Order Lower Than Expected

| Symptom | Possible Cause | Fix |
|---------|----------------|-----|
| p_obs = 1 | Boundary limiting | Higher-order BC |
| p_obs = 0 | Solution not smooth | Check physics |
| p_obs varies | Pre-asymptotic | Finer grids |
| p_obs > expected | Super-convergence | Lucky, verify |

### Error Not Decreasing

| Symptom | Possible Cause | Fix |
|---------|----------------|-----|
| Error constant | Roundoff limit | Coarsen grid |
| Error increases | Instability | Check dt, scheme |
| Error oscillates | Non-monotone | Different norms |

### Unexpected Error Growth in Time

| Symptom | Possible Cause | Fix |
|---------|----------------|-----|
| Linear growth | Dispersion error | Higher order |
| Exponential growth | Instability | Check CFL |
| Bounded but large | Phase error | Smaller dt |

## Error Norms

### Common Norms

| Norm | Formula | Emphasis |
|------|---------|----------|
| L∞ (max) | max\|e_i\| | Worst point |
| L2 (RMS) | sqrt(Σ e_i² / n) | Average |
| L1 (mean) | Σ \|e_i\| / n | Mild outliers |
| Weighted | Σ w_i e_i² | Specific regions |

### Norm Selection

- **L∞**: When worst case matters (stability)
- **L2**: General accuracy assessment
- **L1**: When outliers expected (discontinuities)
- **Weighted**: Focus on region of interest

## Quick Reference

### Error Scaling Summary

| dx | 2nd-order error | 4th-order error |
|----|-----------------|-----------------|
| 0.1 | 0.01 | 0.0001 |
| 0.05 | 0.0025 | 6.25e-6 |
| 0.01 | 0.0001 | 1e-8 |

### Target Accuracy Guidelines

| Application | Typical Accuracy | Grid Requirement |
|-------------|------------------|------------------|
| Engineering | 1% | ~10 points/feature |
| Research | 0.1% | ~20 points/feature |
| Validation | 0.01% | ~50 points/feature |
| Spectral accuracy | 1e-10 | Smooth + spectral method |
