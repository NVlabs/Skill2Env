# QuTiP Core Concepts

## Quantum Objects (Qobj)

All quantum objects in QuTiP are represented by the `Qobj` class:

```python
from qutip import *

# Create a quantum object
psi = basis(2, 0)  # Ground state of 2-level system
rho = fock_dm(5, 2)  # Density matrix for n=2 Fock state
H = sigmaz()  # Pauli Z operator
```

Key attributes:
- `.dims` - Dimension structure
- `.shape` - Matrix dimensions
- `.type` - Type (ket, bra, oper, super)
- `.isherm` - Check if Hermitian
- `.dag()` - Hermitian conjugate
- `.tr()` - Trace
- `.norm()` - Norm

## States

### Basis States

```python
# Fock (number) states
n = 2  # Excitation level
N = 10  # Hilbert space dimension
psi = basis(N, n)  # or fock(N, n)

# Coherent states
alpha = 1 + 1j
coherent(N, alpha)

# Thermal states (density matrices)
n_avg = 2.0  # Average photon number
thermal_dm(N, n_avg)
```

### Spin States

```python
# Spin-1/2 states
spin_state(1/2, 1/2)  # Spin up
spin_coherent(1/2, theta, phi)  # Coherent spin state

# Multi-qubit computational basis
basis([2,2,2], [0,1,0])  # |010⟩ for 3 qubits
```

### Composite States

```python
# Tensor products
psi1 = basis(2, 0)
psi2 = basis(2, 1)
tensor(psi1, psi2)  # |01⟩

# Bell states
bell_state('00')  # (|00⟩ + |11⟩)/√2
maximally_mixed_dm(2)  # Maximally mixed state
```

## Operators

### Creation/Annihilation

```python
N = 10
a = destroy(N)  # Annihilation operator
a_dag = create(N)  # Creation operator
n_op = num(N)  # Number operator (a†a) — don't name it `num`, that shadows the function
```

### Pauli Matrices

```python
sigmax()  # σx
sigmay()  # σy
sigmaz()  # σz
sigmap()  # σ+ = (σx + iσy)/2
sigmam()  # σ- = (σx - iσy)/2
```

### Angular Momentum

```python
# Spin operators for arbitrary j
j = 1  # Spin-1
jmat(j, 'x')  # Jx
jmat(j, 'y')  # Jy
jmat(j, 'z')  # Jz
jmat(j, '+')  # J+
jmat(j, '-')  # J-
```

### Displacement and Squeezing

```python
alpha = 1 + 1j
displace(N, alpha)  # Displacement operator D(α)

z = 0.5  # Squeezing parameter
squeeze(N, z)  # Squeezing operator S(z)
```

## Tensor Products and Composition

### Building Composite Systems

```python
# Tensor product of operators
H1 = sigmaz()
H2 = sigmax()
H_total = tensor(H1, H2)

# Identity operators
qeye([2, 2])  # Identity for two qubits

# Partial application
# σz ⊗ I for 3-qubit system
tensor(sigmaz(), qeye(2), qeye(2))
```

### Partial Trace

```python
# Composite system state
rho = bell_state('00').proj()  # |Φ+⟩⟨Φ+|

# Trace out subsystem
rho_A = ptrace(rho, 0)  # Trace out subsystem 0
rho_B = ptrace(rho, 1)  # Trace out subsystem 1
```

## Expectation Values and Measurements

```python
# Expectation values
psi = coherent(N, alpha)
expect(n_op, psi)  # ⟨n⟩

# For multiple operators
ops = [a, a_dag, n_op]
expect(ops, psi)  # Returns list

# Variance
variance(n_op, psi)  # Var(n) = ⟨n²⟩ - ⟨n⟩²
```

## Superoperators and Liouvillians

### Lindblad Form

```python
# System Hamiltonian
H = n_op

# Collapse operators (dissipation)
c_ops = [np.sqrt(0.1) * a]  # Decay rate 0.1

# Liouvillian superoperator
L = liouvillian(H, c_ops)

# Alternative: explicit form
L = -1j * (spre(H) - spost(H)) + lindblad_dissipator(a, a)
```

### Superoperator Representations

In v5 a single `to_*` family converts a superoperator/channel between
representations (the directional v4 helpers like `choi_to_super` were removed):

```python
# Build a superoperator from Kraus operators
S = kraus_to_super(kraus_ops)

# Convert any superoperator to another representation
choi = to_choi(S)     # Choi matrix
chi  = to_chi(S)       # chi (process) matrix
kr   = to_kraus(S)     # list of Kraus operators
sup  = to_super(choi)  # back to superoperator from Choi
```

## Quantum Gates (requires qutip-qip)

```python
from qutip_qip.operations import *

# Single-qubit gates
hadamard_transform()  # Hadamard
rx(np.pi/2)  # X-rotation
ry(np.pi/2)  # Y-rotation
rz(np.pi/2)  # Z-rotation
phasegate(np.pi/4)  # Phase gate
snot()  # Hadamard (alternative)

# Two-qubit gates
cnot()  # CNOT
swap()  # SWAP
iswap()  # iSWAP
sqrtswap()  # √SWAP
berkeley()  # Berkeley gate
swapalpha(alpha)  # SWAP^α

# Three-qubit gates
fredkin()  # Controlled-SWAP
toffoli()  # Controlled-CNOT

# Expanding to multi-qubit systems
N = 3  # Total qubits
target = 1
controls = [0, 2]
gate_expand_2toN(cnot(), N, [controls[0], target])
```

## Common Hamiltonians

### Jaynes-Cummings Model

```python
# Cavity mode
N = 10
a = tensor(destroy(N), qeye(2))

# Atom
sm = tensor(qeye(N), sigmam())

# Hamiltonian
wc = 1.0  # Cavity frequency
wa = 1.0  # Atom frequency
g = 0.05  # Coupling strength
H = wc * a.dag() * a + wa * sm.dag() * sm + g * (a.dag() * sm + a * sm.dag())
```

### Driven Systems

```python
# Time-dependent Hamiltonian
H0 = sigmaz()
H1 = sigmax()

def drive(t, args):
    return np.sin(args['w'] * t)

H = [H0, [H1, drive]]
args = {'w': 1.0}
```

### Spin Chains

```python
# Heisenberg chain.
# QuTiP has no `tensor_at`; build a small helper that places an operator on
# one site of an N-qubit tensor product (identity everywhere else).
def site_op(op, i, N):
    ops = [qeye(2)] * N
    ops[i] = op
    return tensor(ops)

N_spins = 5
J = 1.0  # Exchange coupling

H = 0
for i in range(N_spins - 1):
    # σᵢˣσᵢ₊₁ˣ + σᵢʸσᵢ₊₁ʸ + σᵢᶻσᵢ₊₁ᶻ
    H += J * (
        site_op(sigmax(), i, N_spins) * site_op(sigmax(), i + 1, N_spins) +
        site_op(sigmay(), i, N_spins) * site_op(sigmay(), i + 1, N_spins) +
        site_op(sigmaz(), i, N_spins) * site_op(sigmaz(), i + 1, N_spins)
    )
```

## Useful Utility Functions

```python
# Generate random quantum objects
rand_ket(N)  # Random ket
rand_dm(N)  # Random density matrix
rand_herm(N)  # Random Hermitian operator
rand_unitary(N)  # Random unitary

# Commutator and anti-commutator (anticommutator via kind='anti')
commutator(A, B)  # [A, B]
commutator(A, B, kind='anti')  # {A, B}

# Matrix exponential
(-1j * H * t).expm()  # e^(-iHt)

# Eigenvalues and eigenvectors
H.eigenstates()  # Returns (eigenvalues, eigenvectors)
H.eigenenergies()  # Returns only eigenvalues
H.groundstate()  # Ground state energy and state
```
