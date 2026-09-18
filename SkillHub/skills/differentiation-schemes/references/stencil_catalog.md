# Stencil Catalog

Comprehensive reference for finite difference stencil coefficients.

## First Derivative Stencils

### Central Differences

Symmetric stencils, no directional bias.

**2nd Order (3-point):**
```
Offsets: [-1, 0, +1]
Coefficients: [-1/2, 0, 1/2] / dx

f'(x) ≈ (f(x+dx) - f(x-dx)) / (2dx)
Error: O(dx²)
```

**4th Order (5-point):**
```
Offsets: [-2, -1, 0, +1, +2]
Coefficients: [1/12, -2/3, 0, 2/3, -1/12] / dx

f'(x) ≈ (-f(x+2dx) + 8f(x+dx) - 8f(x-dx) + f(x-2dx)) / (12dx)
Error: O(dx⁴)
```

**6th Order (7-point):**
```
Offsets: [-3, -2, -1, 0, +1, +2, +3]
Coefficients: [-1/60, 3/20, -3/4, 0, 3/4, -3/20, 1/60] / dx
Error: O(dx⁶)
```

### Forward Differences (One-Sided)

For left boundaries or upwind schemes.

**1st Order (2-point):**
```
Offsets: [0, +1]
Coefficients: [-1, 1] / dx

f'(x) ≈ (f(x+dx) - f(x)) / dx
Error: O(dx)
```

**2nd Order (3-point):**
```
Offsets: [0, +1, +2]
Coefficients: [-3/2, 2, -1/2] / dx

f'(x) ≈ (-3f(x) + 4f(x+dx) - f(x+2dx)) / (2dx)
Error: O(dx²)
```

**3rd Order (4-point):**
```
Offsets: [0, +1, +2, +3]
Coefficients: [-11/6, 3, -3/2, 1/3] / dx
Error: O(dx³)
```

**4th Order (5-point):**
```
Offsets: [0, +1, +2, +3, +4]
Coefficients: [-25/12, 4, -3, 4/3, -1/4] / dx
Error: O(dx⁴)
```

### Backward Differences (One-Sided)

For right boundaries (mirror of forward).

**1st Order (2-point):**
```
Offsets: [-1, 0]
Coefficients: [-1, 1] / dx
```

**2nd Order (3-point):**
```
Offsets: [-2, -1, 0]
Coefficients: [1/2, -2, 3/2] / dx
```

## Second Derivative Stencils

### Central Differences

**2nd Order (3-point):**
```
Offsets: [-1, 0, +1]
Coefficients: [1, -2, 1] / dx²

f''(x) ≈ (f(x+dx) - 2f(x) + f(x-dx)) / dx²
Error: O(dx²)
```

**4th Order (5-point):**
```
Offsets: [-2, -1, 0, +1, +2]
Coefficients: [-1/12, 4/3, -5/2, 4/3, -1/12] / dx²

f''(x) ≈ (-f(x+2dx) + 16f(x+dx) - 30f(x) + 16f(x-dx) - f(x-2dx)) / (12dx²)
Error: O(dx⁴)
```

**6th Order (7-point):**
```
Offsets: [-3, -2, -1, 0, +1, +2, +3]
Coefficients: [1/90, -3/20, 3/2, -49/18, 3/2, -3/20, 1/90] / dx²
Error: O(dx⁶)
```

### One-Sided Second Derivative

**2nd Order Forward (4-point):**
```
Offsets: [0, +1, +2, +3]
Coefficients: [2, -5, 4, -1] / dx²
Error: O(dx²)
```

**2nd Order Backward (4-point):**
```
Offsets: [-3, -2, -1, 0]
Coefficients: [-1, 4, -5, 2] / dx²
Error: O(dx²)
```

## Higher Derivative Stencils

### Third Derivative

**2nd Order Central (5-point):**
```
Offsets: [-2, -1, 0, +1, +2]
Coefficients: [-1/2, 1, 0, -1, 1/2] / dx³
Error: O(dx²)
```

**4th Order Central (7-point):**
```
Offsets: [-3, -2, -1, 0, +1, +2, +3]
Coefficients: [1/8, -1, 13/8, 0, -13/8, 1, -1/8] / dx³
Error: O(dx⁴)
```

### Fourth Derivative

**2nd Order Central (5-point):**
```
Offsets: [-2, -1, 0, +1, +2]
Coefficients: [1, -4, 6, -4, 1] / dx⁴
Error: O(dx²)
```

**4th Order Central (7-point):**
```
Offsets: [-3, -2, -1, 0, +1, +2, +3]
Coefficients: [-1/6, 2, -13/2, 28/3, -13/2, 2, -1/6] / dx⁴
Error: O(dx⁴)
```

## Mixed and Cross Derivatives

### First Cross Derivative (∂²f/∂x∂y)

**2nd Order (4-point):**
```
f_xy ≈ (f(x+dx,y+dy) - f(x+dx,y-dy) - f(x-dx,y+dy) + f(x-dx,y-dy)) / (4 dx dy)

Stencil (in 2D):
    [+1]      [-1]
       [0]
    [-1]      [+1]
```

**4th Order:**
```
Uses 12 points in a wider pattern
Error: O(dx⁴ + dy⁴)
```

## Compact (Padé) Schemes

Higher accuracy with smaller stencils by solving implicit system.

### 4th Order Compact First Derivative

```
α f'_{i-1} + f'_i + α f'_{i+1} = (a/dx)(f_{i+1} - f_{i-1})

where α = 1/4, a = 3/4
```

Requires solving tridiagonal system for f'.

### 6th Order Compact First Derivative

```
α f'_{i-1} + f'_i + α f'_{i+1} = (a/dx)(f_{i+1} - f_{i-1}) + (b/dx)(f_{i+2} - f_{i-2})

where α = 1/3, a = 14/9, b = 1/9
```

### Advantages of Compact Schemes

| Property | Explicit | Compact |
|----------|----------|---------|
| Stencil width | Wide | Narrow |
| Operations | O(n) | O(n) but solve required |
| Spectral resolution | Good | Excellent |
| Boundary handling | Simple | Requires closure |

## Upwind Schemes

For advection-dominated problems with u > 0.

### First-Order Upwind

```
u > 0: f'(x) ≈ (f(x) - f(x-dx)) / dx  (backward)
u < 0: f'(x) ≈ (f(x+dx) - f(x)) / dx  (forward)
```

Stable but highly diffusive.

### Second-Order Upwind

```
u > 0: f'(x) ≈ (3f(x) - 4f(x-dx) + f(x-2dx)) / (2dx)
u < 0: f'(x) ≈ (-3f(x) + 4f(x+dx) - f(x+2dx)) / (2dx)
```

Less diffusive, may oscillate.

### Third-Order Upwind (QUICK)

```
f'(x) ≈ (2f(x+dx) + 3f(x) - 6f(x-dx) + f(x-2dx)) / (6dx)
```

Good balance of accuracy and stability.

## Stencil Properties Summary

### First Derivative

| Order | Points | Width | Coefficients Sum |
|-------|--------|-------|------------------|
| 2 central | 3 | 2dx | 0 |
| 4 central | 5 | 4dx | 0 |
| 6 central | 7 | 6dx | 0 |
| 1 one-sided | 2 | dx | 0 |
| 2 one-sided | 3 | 2dx | 0 |

### Second Derivative

| Order | Points | Width | Coefficients Sum |
|-------|--------|-------|------------------|
| 2 central | 3 | 2dx | 0 |
| 4 central | 5 | 4dx | 0 |
| 6 central | 7 | 6dx | 0 |

### Stability Properties

| Scheme | Dispersion | Dissipation |
|--------|------------|-------------|
| Central | Low | None |
| Upwind | Moderate | High |
| Compact | Very low | None |
| WENO | Low | Adaptive |

## Implementation Notes

### Applying Stencils

```python
def apply_stencil(f, coeffs, offsets, dx):
    """Apply finite difference stencil."""
    result = np.zeros_like(f)
    for c, o in zip(coeffs, offsets):
        result += c * np.roll(f, -o)
    return result / dx

# Example: 4th-order central first derivative
coeffs = [1/12, -2/3, 0, 2/3, -1/12]
offsets = [-2, -1, 0, 1, 2]
df_dx = apply_stencil(f, coeffs, offsets, dx)
```

### Boundary Treatment

Interior stencils don't work at boundaries:

```
For central 4th-order (needs ±2 points):
  x = 0: use forward stencil
  x = dx: use biased stencil
  x = 2dx to x = (n-3)dx: central stencil
  x = (n-2)dx: use biased stencil
  x = (n-1)dx: use backward stencil
```

### Verification

Taylor expansion verification:

```
f(x+dx) = f(x) + dx f'(x) + dx²/2 f''(x) + dx³/6 f'''(x) + ...

Substitute into stencil, verify leading error term.
```

Grid refinement verification:

```
Run with dx, dx/2, dx/4
Error should decrease as dx^p for order p
```
