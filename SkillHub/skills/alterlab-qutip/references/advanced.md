# QuTiP Advanced Features

## Floquet Theory

For time-periodic Hamiltonians H(t + T) = H(t).

### Floquet Modes and Quasi-Energies (v5 `FloquetBasis`)

In QuTiP 5 the Floquet machinery is wrapped in the `FloquetBasis` class. The
standalone `floquet_modes`/`floquet_states`/`floquet_state_decomposition`
functions still exist but are deprecated in favour of `FloquetBasis` methods.

```python
from qutip import *
import numpy as np

# Time-periodic Hamiltonian
w_d = 1.0  # Drive frequency
T = 2 * np.pi / w_d  # Period

H0 = sigmaz()
H1 = sigmax()
H = [H0, [H1, 'cos(w*t)']]
args = {'w': w_d}

# Floquet basis: quasi-energies and modes
fbasis = FloquetBasis(H, T, args=args)
f_energies = fbasis.e_quasi      # quasi-energies
f_modes_0 = fbasis.mode(0.0)     # Floquet modes at t = 0
print("Quasi-energies:", f_energies)
```

### Floquet States and Decomposition

```python
# Floquet states (mode * phase) at a given time
t = 1.0
f_states_t = fbasis.state(t)

# Decompose an initial state into the Floquet basis at t = 0
psi0 = basis(2, 0)
coeffs = fbasis.to_floquet_basis(psi0)   # column of amplitudes
psi0_back = fbasis.from_floquet_basis(coeffs)  # round-trip back to lab frame
```

### Floquet-Markov Master Equation

```python
# Time evolution with dissipation. v5 fmmesolve takes c_ops plus a spectra_cb
# list (the noise power spectrum S(w) for each c_op); omit spectra_cb for the
# default flat spectrum.
c_ops = [np.sqrt(0.1) * sigmam()]
tlist = np.linspace(0, 20, 200)

result = fmmesolve(H, psi0, tlist, c_ops=c_ops,
                   spectra_cb=[lambda w: 0.5 * (w > 0)],
                   e_ops=[sigmaz()], T=T, args=args)

import matplotlib.pyplot as plt
plt.plot(tlist, result.expect[0])
plt.xlabel('Time')
plt.ylabel('⟨σz⟩')
plt.show()
```

### Floquet Steady State

```python
# Periodic (Floquet) steady state of a driven, dissipative system
c_ops = [np.sqrt(0.1) * sigmam()]
rho_ss = steadystate_floquet(H0, c_ops, H1, w_d)
```

## Hierarchical Equations of Motion (HEOM)

For non-Markovian open quantum systems with strong system-bath coupling.

### Basic HEOM Setup

```python
from qutip import heom

# System Hamiltonian
H_sys = sigmaz()

# Bath correlation as a sum of exponentials. BosonicBath needs BOTH the real
# and imaginary expansion coefficients: (Q, ck_real, vk_real, ck_imag, vk_imag).
Q = sigmax()  # System-bath coupling operator
ck_real = [0.1]   # real coupling strengths
vk_real = [0.5]   # real bath frequencies
ck_imag = [0.0]   # imaginary coupling strengths
vk_imag = [0.5]   # imaginary bath frequencies
bath = heom.BosonicBath(Q, ck_real, vk_real, ck_imag, vk_imag)

# Initial state
rho0 = basis(2, 0) * basis(2, 0).dag()

# Create HEOM solver
max_depth = 5
hsolver = heom.HEOMSolver(H_sys, [bath], max_depth=max_depth)

# Time evolution
tlist = np.linspace(0, 10, 100)
result = hsolver.run(rho0, tlist)

# result.states already holds the reduced system density matrices (one per time)
rho_sys = result.states
```

### Multiple Baths

```python
# Define multiple baths (each needs real + imaginary coefficients)
bath1 = heom.BosonicBath(sigmax(), [0.1], [0.5], [0.0], [0.5])
bath2 = heom.BosonicBath(sigmay(), [0.05], [1.0], [0.0], [1.0])

hsolver = heom.HEOMSolver(H_sys, [bath1, bath2], max_depth=5)
```

### Drude-Lorentz Spectral Density

```python
# Common in condensed matter physics
from qutip.solver.heom import DrudeLorentzBath

lam = 0.1  # Reorganization energy
gamma = 0.5  # Bath cutoff frequency
T = 1.0  # Temperature (in energy units)
Nk = 2  # Number of Matsubara terms

bath = DrudeLorentzBath(Q, lam, gamma, T, Nk)
```

### HEOM Options

```python
# Options are a plain dict in v5 (no HEOMSolver.Options class)
options = {
    "nsteps": 2000,
    "store_states": True,
    "rtol": 1e-7,
    "atol": 1e-9,
}

hsolver = heom.HEOMSolver(H_sys, [bath], max_depth=5, options=options)
```

## Permutational Invariance

For identical particle systems (e.g., spin ensembles).

In QuTiP 5.3, the PIQS helpers must be imported from `qutip.piqs.piqs`
(`from qutip.piqs import ...` does not re-export them).

### Dicke States

```python
from qutip.piqs.piqs import dicke

# Dicke state |j, m⟩ for N spins
N = 10  # Number of spins
j = N / 2  # Total angular momentum
m = 0      # z-component

psi = dicke(N, j, m)
```

### Permutation-Invariant Operators

```python
from qutip.piqs.piqs import jspin

# Collective spin operators
N = 10
Jx = jspin(N, 'x')
Jy = jspin(N, 'y')
Jz = jspin(N, 'z')
Jp = jspin(N, '+')
Jm = jspin(N, '-')
```

### PIQS Dynamics

The `Dicke` class builds the permutation-invariant Liouvillian; feed it to
`mesolve` (it has no `.solve()` method — the in-class integrator is `pisolve`).

```python
from qutip.piqs.piqs import Dicke, dicke, jspin
from qutip import mesolve

# Setup Dicke model
N = 10
system = Dicke(N=N, emission=1.0, dephasing=0.5,
               pumping=0.0, collective_emission=0.0)

L = system.liouvillian()         # permutation-invariant Liouvillian
Jz = jspin(N, 'z')
rho0 = dicke(N, N / 2, N / 2)    # all spins up

# Time evolution via mesolve using the PIQS Liouvillian
tlist = np.linspace(0, 10, 100)
result = mesolve(L, rho0, tlist, e_ops=[Jz])

# Alternatively, integrate directly with the class method (no e_ops):
# result = system.pisolve(rho0, tlist)
```

## Non-Markovian Monte Carlo

Quantum trajectories with memory effects.

In v5, `nm_mcsolve` takes `ops_and_rates`: a list of `(collapse_op, rate)` pairs
where `rate` can be a constant, a `f(t, **kwargs)` callable, or a string
coefficient. Memory effects are encoded by rates that go **negative** in time
(the solver tracks the influence martingale).

```python
from qutip import nm_mcsolve

# System setup
H = sigmaz()
psi0 = basis(2, 0)
tlist = np.linspace(0, 10, 100)

# Time-dependent (possibly negative) rate -> non-Markovian dynamics.
# Use the pythonic f(t, **kwargs) signature (the old f(t, args) form is
# deprecated and will be removed in QuTiP 5.5).
def gamma(t, **kwargs):
    return np.exp(-t / 2.0) * np.cos(t)

result = nm_mcsolve(H, psi0, tlist,
                    ops_and_rates=[(sigmam(), gamma)],
                    ntraj=500, e_ops=[sigmaz()])
```

## Stochastic Solvers with Measurements

### Continuous Measurement

```python
# Detection scheme is selected with heterodyne=True/False (the v4 `noise`
# integer codes are gone).
sc_ops = [np.sqrt(0.1) * destroy(N)]  # measurement operator

# Homodyne detection (default)
result = ssesolve(H, psi0, tlist, sc_ops=sc_ops,
                   e_ops=[num(N)], ntraj=100, heterodyne=False)

# Heterodyne detection
result = ssesolve(H, psi0, tlist, sc_ops=sc_ops,
                   e_ops=[num(N)], ntraj=100, heterodyne=True)
```

### Photon Counting

```python
# Per-trajectory jump records require keep_runs_results (options is a dict in v5)
result = mcsolve(H, psi0, tlist, c_ops, ntraj=50,
                 options={"keep_runs_results": True})

# Extract jump times and which c_op fired, per trajectory
for i, jump_times in enumerate(result.col_times):
    print(f"Trajectory {i} jump times: {jump_times}")
    print(f"Which operator: {result.col_which[i]}")
```

## Krylov Subspace Methods

Efficient for large systems.

```python
from qutip import krylovsolve

# Use Krylov solver
result = krylovsolve(H, psi0, tlist, krylov_dim=10, e_ops=[num(N)])
```

## Bloch-Redfield Master Equation

For weak system-bath coupling.

```python
# Bath spectral density
def ohmic_spectrum(w):
    if w >= 0:
        return 0.1 * w  # Ohmic
    else:
        return 0

# Coupling operators and spectra
a_ops = [[sigmax(), ohmic_spectrum]]

# Solve
result = brmesolve(H, psi0, tlist, a_ops, e_ops=[sigmaz()])
```

### Temperature-Dependent Bath

```python
def thermal_spectrum(w):
    # Bose-Einstein distribution
    T = 1.0  # Temperature
    if abs(w) < 1e-10:
        return 0.1 * T
    n_th = 1 / (np.exp(abs(w)/T) - 1)
    if w >= 0:
        return 0.1 * w * (n_th + 1)
    else:
        return 0.1 * abs(w) * n_th

a_ops = [[sigmax(), thermal_spectrum]]
result = brmesolve(H, psi0, tlist, a_ops, e_ops=[sigmaz()])
```

## Superoperators and Quantum Channels

### Superoperator Representations

```python
# Liouvillian
L = liouvillian(H, c_ops)

# Convert between representations. v5 uses the unified to_* family
# (super_to_choi / super_to_kraus from v4 were removed).
from qutip import spre, spost, sprepost, to_choi, to_kraus, kraus_to_super

# Superoperator forms
L_spre = spre(H)  # Left multiplication
L_spost = spost(H)  # Right multiplication
L_sprepost = sprepost(H, H.dag())

# Build a CPTP superoperator first (sprepost is a valid channel; a Liouvillian
# generator is not), then convert it.
S = sprepost(H, H.dag())
choi = to_choi(S)    # Choi matrix
kraus = to_kraus(S)  # list of Kraus operators
```

### Quantum Channels

```python
# Depolarizing channel
p = 0.1  # Error probability
K0 = np.sqrt(1 - 3*p/4) * qeye(2)
K1 = np.sqrt(p/4) * sigmax()
K2 = np.sqrt(p/4) * sigmay()
K3 = np.sqrt(p/4) * sigmaz()

kraus_ops = [K0, K1, K2, K3]
E = kraus_to_super(kraus_ops)

# Apply channel
rho_out = E * operator_to_vector(rho_in)
rho_out = vector_to_operator(rho_out)
```

### Amplitude Damping

```python
# T1 decay
gamma = 0.1
K0 = Qobj([[1, 0], [0, np.sqrt(1 - gamma)]])
K1 = Qobj([[0, np.sqrt(gamma)], [0, 0]])

E_damping = kraus_to_super([K0, K1])
```

### Phase Damping

```python
# T2 dephasing
gamma = 0.1
K0 = Qobj([[1, 0], [0, np.sqrt(1 - gamma/2)]])
K1 = Qobj([[0, 0], [0, np.sqrt(gamma/2)]])

E_dephasing = kraus_to_super([K0, K1])
```

## Quantum Trajectories Analysis

### Extract Individual Trajectories

```python
# keep_runs_results=True stores every trajectory (options is a dict in v5)
result = mcsolve(H, psi0, tlist, c_ops, ntraj=100,
                 options={"keep_runs_results": True})

# runs_states[i] is the list of states for trajectory i
for i in range(len(result.runs_states)):
    trajectory = result.runs_states[i]
    # Analyze trajectory
```

### Trajectory Statistics

```python
# Averages and standard deviation come for free (no keep_runs_results needed)
result = mcsolve(H, psi0, tlist, c_ops, e_ops=[num(N)], ntraj=500)

n_mean = result.expect[0]
n_std = result.std_expect[0]

# Per-trajectory final states require keep_runs_results
runs = mcsolve(H, psi0, tlist, c_ops, ntraj=500,
               options={"keep_runs_results": True})
final_states = [traj[-1] for traj in runs.runs_states]
```

## Time-Dependent Terms Advanced

### QobjEvo

```python
from qutip import QobjEvo

# Time-dependent Hamiltonian with QobjEvo. v5 prefers the pythonic coefficient
# signature f(t, **kwargs) (the old f(t, args) form is deprecated, removed in 5.5).
def drive(t, A, w, tau, **kwargs):
    return A * np.exp(-t / tau) * np.sin(w * t)

H0 = num(N)
H1 = destroy(N) + create(N)
args = {'A': 1.0, 'w': 1.0, 'tau': 5.0}

H_td = QobjEvo([H0, [H1, drive]], args=args)

# .arguments() updates the parameters in place (returns None)
H_td.arguments({'A': 2.0, 'w': 1.5, 'tau': 10.0})
```

### Compiled Time-Dependent Terms

```python
# Fastest method (requires Cython)
H = [num(N), [destroy(N) + create(N), 'A * exp(-t/tau) * sin(w*t)']]
args = {'A': 1.0, 'w': 1.0, 'tau': 5.0}

# QuTiP compiles this for speed
result = sesolve(H, psi0, tlist, args=args)
```

### Callback Functions

```python
# Coefficient callbacks take time plus the named args (pythonic f(t, **kwargs))
def time_dependent_coeff(t, **kwargs):
    return complex_function(t, **kwargs)

H = [H0, [H1, time_dependent_coeff]]
```

> Note: time-dependent coefficients elsewhere in these docs are written with the
> legacy `f(t, args)` signature, which still works but is deprecated and will be
> removed in QuTiP 5.5. Prefer `f(t, **kwargs)` in new code.

## Parallel Processing

### Parallel Map

```python
from qutip import parallel_map

# Define task
def simulate(gamma):
    c_ops = [np.sqrt(gamma) * destroy(N)]
    result = mesolve(H, psi0, tlist, c_ops, e_ops=[num(N)])
    return result.expect[0]

# Run in parallel
gamma_values = np.linspace(0, 1, 20)
results = parallel_map(simulate, gamma_values, num_cpus=4)
```

### Serial Map (for debugging)

```python
from qutip import serial_map

# Same interface but runs serially
results = serial_map(simulate, gamma_values)
```

## File I/O

### Save/Load Quantum Objects

```python
# qsave/qload (pickle-based). Qobj has no .save() method in v5.
# A ".qu" extension is added automatically.
qsave(H, 'hamiltonian')
qsave(psi, 'state')

H_loaded = qload('hamiltonian')   # reads hamiltonian.qu
psi_loaded = qload('state')
```

### Save/Load Results

```python
# Result also has no .save()/.load(); use qsave/qload.
result = mesolve(H, psi0, tlist, c_ops, e_ops=[num(N)])
qsave(result, 'simulation')
loaded_result = qload('simulation')
```

### Export to MATLAB

```python
# Qobj has no matlab_export in v5; write the dense array with scipy.
import scipy.io as sio
sio.savemat('hamiltonian.mat', {'H': H.full()})
```

## Solver Options

### Fine-Tuning Solvers

```python
# Options is a plain dict in v5 (the Options class was removed).
options = {
    "nsteps": 10000,        # Max internal steps
    "rtol": 1e-8,           # Relative tolerance
    "atol": 1e-10,          # Absolute tolerance
    "method": "adams",      # Non-stiff (default); use 'bdf' for stiff problems
    "store_states": True,
    "store_final_state": True,
    "progress_bar": "text",  # string, not True
}

# The RNG seed is a solver keyword (not an option), e.g. for mcsolve:
result = mesolve(H, psi0, tlist, c_ops, options=options)
# result = mcsolve(H, psi0, tlist, c_ops, ntraj=500, seeds=12345, options=options)
```

### Debugging

```python
# Run trajectories serially on one core for reproducible, debuggable runs.
# (There is no `verbose` option in v5.)
result = mcsolve(H, psi0, tlist, c_ops, ntraj=10,
                 options={"map": "serial", "num_cpus": 1})
```

## Performance Tips

1. **Use sparse matrices**: QuTiP does this automatically
2. **Minimize Hilbert space**: Truncate when possible
3. **Choose right solver**:
   - Pure states: `sesolve` faster than `mesolve`
   - Stochastic: `mcsolve` for quantum jumps
   - Periodic: Floquet methods
4. **Time-dependent terms**: String format fastest
5. **Expectation values**: Only compute needed observables
6. **Parallel trajectories**: `mcsolve` uses all CPUs
7. **Krylov methods**: For very large systems
8. **Memory**: Use `store_final_state` instead of `store_states` when possible
