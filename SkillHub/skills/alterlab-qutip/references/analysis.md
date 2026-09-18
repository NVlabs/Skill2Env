# QuTiP Analysis and Measurement

## Expectation Values

### Basic Expectation Values

```python
from qutip import *
import numpy as np

# Single operator
psi = coherent(N, 2)
n_avg = expect(num(N), psi)

# Multiple operators
ops = [num(N), destroy(N), create(N)]
results = expect(ops, psi)  # Returns list
```

### Expectation Values for Density Matrices

```python
# Works with both pure states and density matrices
rho = thermal_dm(N, 2)
n_avg = expect(num(N), rho)
```

### Variance

```python
# Calculate variance of observable
var_n = variance(num(N), psi)

# Manual calculation
var_n = expect(num(N)**2, psi) - expect(num(N), psi)**2
```

### Time-Dependent Expectation Values

```python
# During time evolution
result = mesolve(H, psi0, tlist, c_ops, e_ops=[num(N)])
n_t = result.expect[0]  # Array of ⟨n⟩ at each time
```

## Entropy Measures

### Von Neumann Entropy

```python
from qutip import entropy_vn

# Density matrix entropy
rho = thermal_dm(N, 2)
S = entropy_vn(rho)             # natural log by default: -Tr(ρ ln ρ)
S_bits = entropy_vn(rho, base=2)  # pass base=2 for entropy in bits
```

### Linear Entropy

```python
from qutip import entropy_linear

# Linear entropy S_L = 1 - Tr(ρ²)
S_L = entropy_linear(rho)
```

### Entanglement Entropy

```python
# For bipartite systems
psi = bell_state('00')
rho = psi.proj()

# Trace out subsystem B to get reduced density matrix
rho_A = ptrace(rho, 0)

# Entanglement entropy
S_ent = entropy_vn(rho_A)
```

### Mutual Information

```python
from qutip import entropy_mutual

# For bipartite state ρ_AB
I = entropy_mutual(rho, [0, 1])  # I(A:B) = S(A) + S(B) - S(AB)
```

### Conditional Entropy

```python
from qutip import entropy_conditional

# S(A|B) = S(AB) - S(B)
S_cond = entropy_conditional(rho, 0)  # Entropy of subsystem 0 given subsystem 1
```

## Fidelity and Distance Measures

### State Fidelity

```python
from qutip import fidelity

# Fidelity between two states
psi1 = coherent(N, 2)
psi2 = coherent(N, 2.1)

F = fidelity(psi1, psi2)  # Returns value in [0, 1]
```

### Process Fidelity

`process_fidelity(oper, target=None)` compares two channels. Pass channels in a
consistent representation (both superoperators, or both unitaries) — not a
unitary against a state.

```python
from qutip import process_fidelity, to_super, propagator

# Ideal unitary channel vs. the actual (dissipative) channel after time t
U_ideal = (-1j * H * t).expm()           # ideal unitary
S_ideal = to_super(U_ideal)              # as a superoperator
S_actual = propagator(H, t, c_ops)       # open-system propagator (superoperator)

F_proc = process_fidelity(S_actual, S_ideal)
```

### Trace Distance

```python
from qutip import tracedist

# Trace distance D = (1/2) Tr|ρ₁ - ρ₂|
rho1 = coherent_dm(N, 2)
rho2 = thermal_dm(N, 2)

D = tracedist(rho1, rho2)  # Returns value in [0, 1]
```

### Hilbert-Schmidt Distance

```python
from qutip import hilbert_dist

# Hilbert-Schmidt distance
D_HS = hilbert_dist(rho1, rho2)
```

### Bures Distance

```python
from qutip import bures_dist

# Bures distance
D_B = bures_dist(rho1, rho2)
```

### Bures Angle

```python
from qutip import bures_angle

# Bures angle
angle = bures_angle(rho1, rho2)
```

## Entanglement Measures

### Concurrence

```python
from qutip import concurrence

# For two-qubit states
psi = bell_state('00')
rho = psi.proj()

C = concurrence(rho)  # C = 1 for maximally entangled states
```

### Negativity

```python
from qutip import negativity

# Negativity (partial transpose criterion)
N_ent = negativity(rho, 0)  # Partial transpose w.r.t. subsystem 0

# Logarithmic negativity
from qutip import logarithmic_negativity
E_N = logarithmic_negativity(rho, 0)
```

### Entangling Power

```python
from qutip import entangling_power

# For unitary gates
U = cnot()
E_pow = entangling_power(U)
```

## Purity Measures

### Purity

```python
# Purity P = Tr(ρ²)
P = (rho * rho).tr()

# For pure states: P = 1
# For maximally mixed: P = 1/d
```

### Checking State Properties

```python
# Is state pure?
is_pure = abs((rho * rho).tr() - 1.0) < 1e-10

# Is operator Hermitian?
H.isherm

# Is operator unitary? (property, not a method)
U.isunitary
```

## Measurement

Measurement helpers live in `qutip.measurement` (they are **not** exposed at the
top level of `qutip`). Single-shot helpers return `(outcome, collapsed_state)`;
the `*_statistics_*` helpers return every possible outcome with its probability.

### Observable Measurement

```python
from qutip.measurement import measure_observable, measurement_statistics_observable

psi = (basis(2, 0) + basis(2, 1)).unit()

# Single shot: random eigenvalue + post-measurement state
value, state_collapsed = measure_observable(psi, sigmaz())

# All outcomes: eigenvalues, projectors, probabilities
eigenvalues, projectors, probabilities = measurement_statistics_observable(psi, sigmaz())
```

### POVM Measurement

```python
from qutip.measurement import measure_povm, measurement_statistics_povm

# Projective POVM in the computational basis
M = basis(2, 0).proj()
povm = [M, qeye(2) - M]

# Single shot: index of the POVM element that fired + post-measurement state
index, state_after = measure_povm(psi, povm)

# All outcomes: post-measurement states and their probabilities
collapsed_states, probabilities = measurement_statistics_povm(psi, povm)
```

## Coherence Measures

### l1-norm Coherence

There is no built-in `coherence_l1norm`; compute the l1-norm of coherence (sum of
absolute values of the off-diagonal elements) directly from the density matrix:

```python
M = rho.full()
C_l1 = np.abs(M).sum() - np.abs(np.diag(M)).sum()
```

QuTiP does provide the optical coherence functions `coherence_function_g1` and
`coherence_function_g2` for first- and second-order field correlations.

## Correlation Functions

### Two-Time Correlation

```python
from qutip import correlation_2op_1t, correlation_2op_2t

# Single-time correlation ⟨A(t+τ)B(t)⟩
A = destroy(N)
B = create(N)
taulist = np.linspace(0, 10, 200)

corr = correlation_2op_1t(H, rho0, taulist, c_ops, A, B)

# Two-time correlation ⟨A(t)B(τ)⟩
tlist = np.linspace(0, 10, 100)
corr_2t = correlation_2op_2t(H, rho0, tlist, taulist, c_ops, A, B)
```

### Three-Operator Correlation

```python
from qutip import correlation_3op_1t, correlation_3op_2t

# ⟨A(0) B(τ) C(0)⟩ as a function of τ (single starting time)
C_op = num(N)
corr_3 = correlation_3op_1t(H, rho0, taulist, c_ops, A, B, C_op)

# ⟨A(t) B(t+τ) C(t)⟩ resolved in both t and τ
tlist = np.linspace(0, 10, 100)
corr_3_2t = correlation_3op_2t(H, rho0, tlist, taulist, c_ops, A, B, C_op)
```

QuTiP 5 ships the 2- and 3-operator correlators (`correlation_2op_1t`,
`correlation_2op_2t`, `correlation_3op_1t`, `correlation_3op_2t`); there is no
`correlation_4op_*`. Build a 4-operator correlator by passing products as the
inner operators of `correlation_3op_*`.

## Spectrum Analysis

### FFT Spectrum

```python
from qutip import spectrum_correlation_fft

# Power spectrum from correlation function
w, S = spectrum_correlation_fft(taulist, corr)
```

### Direct Spectrum Calculation

```python
from qutip import spectrum

# Emission/absorption spectrum
wlist = np.linspace(0, 2, 200)
spec = spectrum(H, wlist, c_ops, A, B)
```

## Steady State Analysis

### Finding Steady State

```python
from qutip import steadystate

# Find steady state ∂ρ/∂t = 0
rho_ss = steadystate(H, c_ops)

# Different methods
rho_ss = steadystate(H, c_ops, method='direct')  # Default
rho_ss = steadystate(H, c_ops, method='eigen')   # Eigenvalue
rho_ss = steadystate(H, c_ops, method='svd')     # SVD
rho_ss = steadystate(H, c_ops, method='power')   # Power method
```

### Steady State Properties

```python
# Verify it's steady
L = liouvillian(H, c_ops)
assert (L * operator_to_vector(rho_ss)).norm() < 1e-10

# Compute steady-state expectation values
n_ss = expect(num(N), rho_ss)
```

## Matrix Analysis

### Eigenanalysis

```python
# Eigenvalues and eigenvectors
evals, ekets = H.eigenstates()

# Just eigenvalues
evals = H.eigenenergies()

# Ground state
E0, psi0 = H.groundstate()
```

### Matrix Functions

```python
# Matrix exponential
U = (H * t).expm()

# Matrix logarithm
log_rho = rho.logm()

# Matrix square root
sqrt_rho = rho.sqrtm()

# Matrix power
rho_squared = rho ** 2
```

### Singular Value Decomposition

Qobj has no `.svd()`; take the SVD on the dense array:

```python
U, S, Vh = np.linalg.svd(H.full())
```

### Permutations

```python
# Permute subsystems (method on Qobj; there is no top-level qutip.permute)
rho_permuted = rho.permute([1, 0])  # Swap subsystems
```

## Partial Operations

### Partial Trace

```python
# Reduce to subsystem
rho_A = ptrace(rho_AB, 0)  # Keep subsystem 0
rho_B = ptrace(rho_AB, 1)  # Keep subsystem 1

# Keep multiple subsystems
rho_AC = ptrace(rho_ABC, [0, 2])  # Keep 0 and 2, trace out 1
```

### Partial Transpose

```python
from qutip import partial_transpose

# Partial transpose (for entanglement detection)
rho_pt = partial_transpose(rho, [0, 1])  # Transpose subsystem 0

# Check if entangled (PPT criterion)
evals = rho_pt.eigenenergies()
is_entangled = any(evals < -1e-10)
```

## Quantum State Tomography

### State Reconstruction

```python
from qutip_qip.tomography import state_tomography

# Prepare measurement results
# measurements = ... (experimental data)

# Reconstruct density matrix
rho_reconstructed = state_tomography(measurements, basis='Pauli')
```

### Process Tomography

```python
from qutip_qip.tomography import qpt

# Characterize quantum process
chi = qpt(U_gate, method='lstsq')  # Chi matrix representation
```

## Random Quantum Objects

Useful for testing and Monte Carlo simulations.

```python
# Random state vector
psi_rand = rand_ket(N)

# Random density matrix
rho_rand = rand_dm(N)

# Random Hermitian operator
H_rand = rand_herm(N)

# Random unitary
U_rand = rand_unitary(N)

# With specific properties
rho_rank2 = rand_dm(N, rank=2)  # Rank-2 density matrix
H_sparse = rand_herm(N, density=0.1)  # 10% non-zero elements
```

## Useful Checks

```python
# Check if operator is Hermitian
H.isherm

# Check if state is normalized
abs(psi.norm() - 1.0) < 1e-10

# Check if density matrix is physical
rho.tr() ≈ 1 and all(rho.eigenenergies() >= 0)

# Check if operators commute
commutator(A, B).norm() < 1e-10
```
