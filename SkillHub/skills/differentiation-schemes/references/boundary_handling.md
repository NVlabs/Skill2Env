# Boundary Handling

Comprehensive guide for implementing finite difference stencils at domain boundaries.

## The Boundary Problem

Interior stencils require points outside the domain:

```
Central 5-point stencil at x = dx:
  Needs: x - 2dx, x - dx, x, x + dx, x + 2dx
  But: x - 2dx = -dx is outside domain!
```

## One-Sided Stencils

### Reducing Stencil Order

Use lower-order one-sided stencils near boundaries:

```
Left boundary (x = 0):
  Point 0: 1st-order forward
  Point 1: 2nd-order forward (if needed)
  Points 2+: Central stencil

Right boundary (x = L):
  Point n-1: 1st-order backward
  Point n-2: 2nd-order backward (if needed)
  Points <n-2: Central stencil
```

### Matching Interior Order

To maintain overall accuracy, use one-sided stencils of same order as interior:

```
Interior: 4th-order central (5 points)
Boundary: 4th-order one-sided (5 points)

First derivative at x = 0:
  f'(0) ≈ (-25f_0 + 48f_1 - 36f_2 + 16f_3 - 3f_4) / (12dx)
```

### Biased Stencils

Use asymmetric stencils that include boundary:

```
At x = dx (one point from left boundary):
  Offsets: [-1, 0, +1, +2, +3]
  A 4th-order stencil shifted to fit

Coefficients (for f'):
  [-1/4, -5/6, 3/2, -1/2, 1/12] / dx
```

## Ghost Cell Method

### Concept

Add fictitious points outside domain:

```
Physical domain: x = 0, dx, 2dx, ..., (n-1)dx
Ghost cells: x = -dx, -2dx (left), x = n*dx, (n+1)*dx (right)

Now central stencils work at all interior points!
```

### Filling Ghost Cells

The ghost values must be computed from boundary conditions.

**Dirichlet BC:** f(0) = g

```
For 2nd-order central derivative at x = dx:
  Need f(-dx)
  Use symmetry: f(-dx) = 2g - f(dx) (linear extrapolation)
  Or: f(-dx) = -f(dx) + 2f(0) (reflect through boundary value)
```

**Neumann BC:** f'(0) = h

```
For 2nd-order:
  f'(0) ≈ (f(dx) - f(-dx)) / (2dx) = h
  → f(-dx) = f(dx) - 2dx*h

For 4th-order:
  Use higher-order approximation to get f(-dx), f(-2dx)
```

**Periodic BC:**

```
f(-dx) = f((n-1)*dx)
f(-2dx) = f((n-2)*dx)
f(n*dx) = f(0)
f((n+1)*dx) = f(dx)
```

### Ghost Cell Implementation

```python
def fill_ghosts(f, bc_type, bc_value, n_ghost):
    """Fill ghost cells based on boundary condition."""
    f_ext = np.zeros(len(f) + 2 * n_ghost)
    f_ext[n_ghost:-n_ghost] = f

    if bc_type == 'dirichlet':
        # Left: reflect through boundary value
        for i in range(n_ghost):
            f_ext[n_ghost - 1 - i] = 2 * bc_value[0] - f[i]
        # Right: reflect through boundary value
        for i in range(n_ghost):
            f_ext[-n_ghost + i] = 2 * bc_value[1] - f[-1 - i]

    elif bc_type == 'neumann':
        # Left: extrapolate with derivative
        for i in range(n_ghost):
            f_ext[n_ghost - 1 - i] = f[i] - 2 * (i + 1) * dx * bc_value[0]
        # Right: extrapolate with derivative
        for i in range(n_ghost):
            f_ext[-n_ghost + i] = f[-1 - i] + 2 * (i + 1) * dx * bc_value[1]

    elif bc_type == 'periodic':
        f_ext[:n_ghost] = f[-n_ghost:]
        f_ext[-n_ghost:] = f[:n_ghost]

    return f_ext
```

## Boundary Condition Types

### Dirichlet (Specified Value)

```
f(boundary) = g(t)

Direct substitution:
  f_0 = g  (known, not part of solve)

For Laplacian discretization:
  (f_1 - 2f_0 + f_{-1}) / dx² at x = dx
  becomes: (f_1 - 2g + f_{-1}) / dx²
  where f_{-1} is ghost (computed for consistency)
```

### Neumann (Specified Derivative)

```
f'(boundary) = h(t)

Using one-sided difference at x = 0:
  (f_1 - f_0) / dx = h → f_0 = f_1 - dx * h

Or using ghost cell:
  (f_1 - f_{-1}) / (2dx) = h → f_{-1} = f_1 - 2dx * h
```

### Robin (Mixed)

```
a * f(boundary) + b * f'(boundary) = c

Combine Dirichlet and Neumann treatment.
```

### Periodic

```
f(0) = f(L), f'(0) = f'(L), etc.

Simply wrap indices:
  f_{-1} = f_{n-1}
  f_{n} = f_0
```

### Symmetry

```
Even symmetry at x = 0: f(-x) = f(x)
  → f_{-1} = f_1, f_{-2} = f_2

Odd symmetry at x = 0: f(-x) = -f(x)
  → f_{-1} = -f_1, f_{-2} = -f_2
```

## Accuracy Considerations

### Order Reduction at Boundaries

Using lower-order BC treatment reduces global accuracy:

| Interior Order | BC Treatment | Global Order |
|----------------|--------------|--------------|
| 4 | 1st-order | 1 |
| 4 | 2nd-order | 2 |
| 4 | 3rd-order | 3 |
| 4 | 4th-order | 4 |

**Rule of thumb:** BC treatment should be at least (interior order - 1).

### Consistency Requirements

For 4th-order Laplacian with Neumann BC:

```
Need: f'(0) to O(dx³) at minimum
      f(-dx), f(-2dx) consistent with this

Standard approach:
  1. Use 4th-order formula for f'(0) = h
  2. Solve for ghost values
  3. Apply interior stencil
```

## Special Cases

### Corner Boundaries (2D/3D)

At corners, multiple boundaries meet:

```
Corner at (0, 0):
  Need ghost values at (-dx, 0), (0, -dy), (-dx, -dy)

Strategy 1: Edge then corner
  Fill edge ghosts first, then extrapolate corners

Strategy 2: Direct corner treatment
  Use corner-specific stencils
```

### Moving Boundaries

For domains with moving interfaces:

```
1. Identify boundary location (between grid points)
2. Use immersed boundary or ghost fluid methods
3. Extrapolate/interpolate to find ghost values
```

### Non-Uniform Grids

Ghost cell spacing may differ from interior:

```
If dx varies:
  Use variable-coefficient stencils near boundary
  Or: Map to uniform computational coordinates
```

## Implementation Patterns

### Modular BC Application

```python
class BoundaryCondition:
    def apply(self, f, dx):
        raise NotImplementedError

class DirichletBC(BoundaryCondition):
    def __init__(self, value):
        self.value = value

    def apply(self, f, dx):
        f[0] = self.value  # Direct enforcement

class NeumannBC(BoundaryCondition):
    def __init__(self, gradient):
        self.gradient = gradient

    def apply(self, f, dx):
        # Second-order one-sided
        f[0] = f[1] - dx * self.gradient
```

### Matrix Form for Implicit

When forming Ax = b:

```
Dirichlet at i = 0:
  A[0, 0] = 1
  A[0, 1:] = 0
  b[0] = g

Neumann at i = 0 (2nd order):
  A[0, 0] = -1/dx
  A[0, 1] = 1/dx
  b[0] = h
```

## Verification

### Manufactured Solutions

Test with known solution that satisfies BCs:

```
f(x) = sin(πx) on [0, 1]
Dirichlet: f(0) = 0, f(1) = 0 ✓

f(x) = cos(πx) on [0, 1]
Neumann: f'(0) = 0, f'(1) = 0 ✓
```

### Convergence Test

Refine grid, verify expected order:

```
dx, dx/2, dx/4:
  Error should decrease as dx^p

If not: BC treatment is limiting accuracy
```

### Symmetry Test

For symmetric problems:

```
If physics is symmetric about x = L/2:
  Solution should be symmetric
  Check: max|f(x) - f(L-x)| < tolerance
```

## Common Pitfalls

### Pitfall 1: Inconsistent Ghost Values

```
Problem: Ghost values computed at wrong order
Result: Loss of accuracy, may look like noise near boundary
Fix: Ensure ghost fill matches interior stencil order
```

### Pitfall 2: Wrong Boundary Location

```
Problem: BC applied at wrong grid point (cell center vs face)
Result: O(dx) error in solution
Fix: Be clear about grid convention
```

### Pitfall 3: Time-Dependent BC Lag

```
Problem: BC evaluated at old time in implicit scheme
Result: Loss of time accuracy
Fix: Use BC at new time (may require iteration)
```

### Pitfall 4: Missing Corner Treatment

```
Problem: Corners filled by extrapolation that doesn't match physics
Result: Artifacts at corners
Fix: Proper corner BC (often requires special handling)
```
