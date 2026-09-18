# Scheme Selection

Comprehensive guide for choosing numerical differentiation schemes.

## Scheme Categories

### Finite Difference (FD)

Approximate derivatives using point values on a grid.

**Characteristics:**
- Simple implementation
- Works on structured grids
- Accuracy depends on stencil width

**Best for:**
- Smooth solutions
- Structured rectangular domains
- Moderate accuracy requirements

### Finite Volume (FV)

Discretize integral conservation laws.

**Characteristics:**
- Inherently conservative
- Natural for conservation laws
- Works on unstructured meshes

**Best for:**
- Discontinuous solutions
- Conservation-critical problems
- Complex geometries

### Finite Element (FE)

Approximate solution as sum of basis functions.

**Characteristics:**
- Flexible geometry handling
- Natural for variational problems
- Higher-order possible

**Best for:**
- Complex geometries
- Multi-physics problems
- Adaptive refinement

### Spectral Methods

Represent solution in global basis (Fourier, Chebyshev).

**Characteristics:**
- Exponential accuracy for smooth problems
- Global operations (FFT)
- Sensitive to discontinuities

**Best for:**
- Periodic domains
- Very smooth solutions
- High accuracy requirements

## Decision Flowchart

```
What is the solution character?
│
├── Smooth everywhere
│   ├── Periodic domain? → Spectral (FFT)
│   ├── Simple geometry? → High-order FD
│   └── Complex geometry? → FE or FD on curvilinear
│
├── Contains discontinuities (shocks, interfaces)
│   ├── Conservation critical? → FV with limiters
│   └── Conservation not critical? → FD with WENO
│
└── Mixed (smooth regions + discontinuities)
    ├── Localized discontinuity? → Hybrid FD + shock capturing
    └── Many discontinuities? → FV with AMR
```

## Detailed Comparisons

### FD vs FV

| Aspect | Finite Difference | Finite Volume |
|--------|-------------------|---------------|
| Formulation | Pointwise derivatives | Cell-averaged fluxes |
| Conservation | Not automatic | Built-in |
| Shocks | Needs limiting | Natural handling |
| Grids | Structured preferred | Any mesh |
| Implementation | Simpler | More complex |
| Accuracy order | Easy high-order | High-order harder |

### Central vs Upwind FD

| Aspect | Central | Upwind |
|--------|---------|--------|
| Bias | None | Flow direction |
| Accuracy | Higher order | Lower order |
| Dispersion | Low | Higher |
| Dissipation | None | High |
| Stability | Needs care | Naturally stable |
| Use for | Diffusion | Advection |

### Explicit vs Implicit

| Aspect | Explicit FD | Implicit FD |
|--------|-------------|-------------|
| Time step | Limited by CFL | Not limited |
| Cost per step | Low | High (solve) |
| Stiffness | Cannot handle | Can handle |
| Parallelism | Easy | Harder |
| Implementation | Simple | Complex |

## Specific Applications

### Diffusion Equation

```
∂u/∂t = D∇²u
```

**Recommended:**
- Spatial: Central FD (2nd or 4th order)
- Time: Implicit (Crank-Nicolson) or explicit RK

**Avoid:**
- Upwind (diffusion has no direction)
- First-order time (too much numerical diffusion)

### Advection Equation

```
∂u/∂t + v·∇u = 0
```

**Recommended:**
- Upwind FD (stable, diffusive)
- Central + artificial viscosity
- WENO for sharp features
- Semi-Lagrangian for large CFL

**Avoid:**
- Pure central difference (unstable without stabilization)

### Wave Equation

```
∂²u/∂t² = c²∇²u
```

**Recommended:**
- Central FD in space
- Leap-frog or RK in time
- Symplectic for long-time accuracy

**Avoid:**
- Upwind (too diffusive)
- Low-order time stepping (phase errors)

### Convection-Diffusion

```
∂u/∂t + v·∇u = D∇²u
```

**Recommended:**
- Peclet-dependent blending
- SUPG (Streamline Upwind Petrov-Galerkin)
- High Pe: upwind-biased
- Low Pe: central

### Nonlinear Conservation Laws

```
∂u/∂t + ∇·f(u) = 0
```

**Recommended:**
- FV with Riemann solvers
- ENO/WENO
- Flux limiters (minmod, Van Leer, etc.)

### Phase-Field Equations

```
∂φ/∂t = -M δF/δφ
```

**Recommended:**
- Central FD for Laplacian
- Conservative form for Cahn-Hilliard
- High-order for interface resolution

## Order Selection

### When to Use Low Order (2nd)

- Initial development/debugging
- Solutions are smooth but not analytic
- Memory is limiting factor
- Complex boundary conditions
- Unstructured or adaptive meshes

### When to Use High Order (4th+)

- Very smooth solutions
- High accuracy needed (validation)
- Uniform structured grids
- Long-time integration (error accumulation)
- Wave propagation (reduce dispersion)

### When to Use Spectral

- Periodic domains
- Smooth, analytic solutions
- Turbulence (DNS)
- Maximum accuracy for given resolution

## Stability-Accuracy Trade-offs

### Accuracy vs Stability

| Choice | Accuracy | Stability |
|--------|----------|-----------|
| Central + fine dt | High | OK with small dt |
| Upwind | Low | Very stable |
| Central + stabilization | Medium | Stable |
| WENO | High | Stable |
| Implicit central | High | Unconditional |

### Computational Cost

| Scheme | Operations/point | Memory |
|--------|------------------|--------|
| 2nd-order central | 3 | O(1) |
| 4th-order central | 5 | O(1) |
| Compact 6th-order | 3 + solve | O(n) |
| Spectral | O(n log n) FFT | O(n) |
| WENO5 | ~15 | O(1) |

## Grid Considerations

### Uniform Grids

All schemes work well. Use highest practical order.

### Stretched Grids

Transform to computational coordinates:

```
x → ξ (uniform)
dx/dξ varies

∂f/∂x = (∂f/∂ξ) / (∂x/∂ξ)
```

Or use variable-coefficient stencils.

### Unstructured Grids

Limited options:
- FV (natural)
- FE (natural)
- FD on stencils (least-squares fitting)

### Adaptive Meshes

Need:
- Conservative interpolation at refinement boundaries
- Consistent stencils across levels
- Flux matching for conservation

## Scheme Selection Checklist

- [ ] Identified solution character (smooth/discontinuous)
- [ ] Determined conservation requirements
- [ ] Assessed grid structure (structured/unstructured)
- [ ] Balanced accuracy vs cost
- [ ] Considered stability constraints
- [ ] Checked boundary condition compatibility
- [ ] Verified with manufactured solution
- [ ] Performed grid convergence study

## Quick Reference Table

| Problem | Smooth | Periodic | Conservation | Recommended |
|---------|--------|----------|--------------|-------------|
| Diffusion | Yes | No | No | Central FD |
| Diffusion | Yes | Yes | No | Spectral |
| Advection | Yes | Any | No | Central + stab |
| Advection | No | Any | Yes | FV + limiter |
| Wave | Yes | No | No | Central + symplectic |
| Wave | Yes | Yes | No | Spectral |
| Navier-Stokes | Mixed | No | Yes | FV or FD + projection |
| Phase-field | Yes | No | Maybe | High-order FD |
