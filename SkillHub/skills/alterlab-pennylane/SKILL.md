---
name: alterlab-pennylane
description: Trains and differentiates quantum circuits with PennyLane, a hardware-agnostic quantum machine-learning framework with automatic differentiation and PyTorch/JAX/TensorFlow integration. Use when training quantum circuits via gradients (parameter-shift, backprop, adjoint), building hybrid quantum-classical models or quantum neural networks, or running differentiable variational algorithms (VQE, QAOA). For IBM Quantum hardware and Qiskit Runtime prefer alterlab-qiskit; for Google Quantum AI or NISQ circuits prefer alterlab-cirq; for open-system Lindblad/master-equation dynamics prefer alterlab-qutip. Part of the AlterLab Academic Skills suite.
license: Apache-2.0
allowed-tools: Read Write Edit Bash(python:*)
compatibility: No API key required for local simulation. Runs via `uv run python`; requires the pennylane Python package. Remote hardware (IBM, IonQ, Rigetti) needs separate provider credentials.
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# PennyLane

## Overview

PennyLane is a quantum computing library that enables training quantum computers like neural networks. It provides automatic differentiation of quantum circuits, device-independent programming, and seamless integration with classical machine learning frameworks.

## Installation

Install using uv:

```bash
uv pip install pennylane
```

For quantum hardware access, install device plugins:

```bash
# IBM Quantum
uv pip install pennylane-qiskit

# Amazon Braket
uv pip install amazon-braket-pennylane-plugin

# Google Cirq
uv pip install pennylane-cirq

# Rigetti Forest
uv pip install pennylane-rigetti

# IonQ
uv pip install pennylane-ionq
```

## Quick Start

Build a quantum circuit and optimize its parameters:

```python
import pennylane as qml
from pennylane import numpy as np

# Create device
dev = qml.device('default.qubit', wires=2)

# Define quantum circuit
@qml.qnode(dev)
def circuit(params):
    qml.RX(params[0], wires=0)
    qml.RY(params[1], wires=1)
    qml.CNOT(wires=[0, 1])
    return qml.expval(qml.PauliZ(0))

# Optimize parameters
opt = qml.GradientDescentOptimizer(stepsize=0.1)
params = np.array([0.1, 0.2], requires_grad=True)

for i in range(100):
    params = opt.step(circuit, params)
```

## Core Capabilities

New to PennyLane? See `references/getting_started.md` for installation, QNodes,
devices, gradients, and a first optimization loop.

### 1. Quantum Circuit Construction

Build circuits with gates, measurements, and state preparation. See `references/quantum_circuits.md` for:
- Single and multi-qubit gates
- Controlled operations and conditional logic
- Mid-circuit measurements and adaptive circuits
- Various measurement types (expectation, probability, samples)
- Circuit inspection and debugging

### 2. Quantum Machine Learning

Create hybrid quantum-classical models. See `references/quantum_ml.md` for:
- Integration with PyTorch, JAX, TensorFlow
- Quantum neural networks and variational classifiers
- Data encoding strategies (angle, amplitude, basis, IQP)
- Training hybrid models with backpropagation
- Transfer learning with quantum circuits

### 3. Quantum Chemistry

Simulate molecules and compute ground state energies. See `references/quantum_chemistry.md` for:
- Molecular Hamiltonian generation
- Variational Quantum Eigensolver (VQE)
- UCCSD ansatz for chemistry
- Geometry optimization and dissociation curves
- Molecular property calculations

### 4. Device Management

Execute on simulators or quantum hardware. See `references/devices_backends.md` for:
- Built-in simulators (default.qubit, lightning.qubit, default.mixed)
- Hardware plugins (IBM, Amazon Braket, Google, Rigetti, IonQ)
- Device selection and configuration
- Performance optimization and caching
- GPU acceleration and JIT compilation

### 5. Optimization

Train quantum circuits with various optimizers. See `references/optimization.md` for:
- Built-in optimizers (Adam, gradient descent, momentum, RMSProp)
- Gradient computation methods (backprop, parameter-shift, adjoint)
- Variational algorithms (VQE, QAOA)
- Training strategies (learning rate schedules, mini-batches)
- Handling barren plateaus and local minima

### 6. Advanced Features

Leverage templates, transforms, and compilation. See `references/advanced_features.md` for:
- Circuit templates and layers
- Transforms and circuit optimization
- Pulse-level programming
- Catalyst JIT compilation
- Noise models and error mitigation
- Resource estimation

## Common Workflows

### Train a Variational Classifier

```python
# 1. Define ansatz
@qml.qnode(dev)
def classifier(x, weights):
    # Encode data
    qml.AngleEmbedding(x, wires=range(4))

    # Variational layers
    qml.StronglyEntanglingLayers(weights, wires=range(4))

    return qml.expval(qml.PauliZ(0))

# 2. Train
opt = qml.AdamOptimizer(stepsize=0.01)
weights = np.random.random((3, 4, 3))  # 3 layers, 4 wires

for epoch in range(100):
    for x, y in zip(X_train, y_train):
        weights = opt.step(lambda w: (classifier(x, w) - y)**2, weights)
```

### Run VQE for Molecular Ground State

```python
from pennylane import qchem

# 1. Build Hamiltonian (returns the qubit Hamiltonian and qubit count)
symbols = ['H', 'H']
coords = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.74])
H, n_qubits = qchem.molecular_hamiltonian(symbols, coords)

# 2. Set up UCCSD ansatz from the excitations
hf_state = qchem.hf_state(electrons=2, orbitals=n_qubits)
singles, doubles = qchem.excitations(electrons=2, orbitals=n_qubits)
s_wires, d_wires = qchem.excitations_to_wires(singles, doubles)

dev = qml.device('default.qubit', wires=n_qubits)

@qml.qnode(dev)
def vqe_circuit(params):
    qml.UCCSD(params, wires=range(n_qubits),
              s_wires=s_wires, d_wires=d_wires, init_state=hf_state)
    return qml.expval(H)

# 3. Optimize (one parameter per excitation)
opt = qml.AdamOptimizer(stepsize=0.1)
params = np.zeros(len(singles) + len(doubles), requires_grad=True)

for i in range(100):
    params, energy = opt.step_and_cost(vqe_circuit, params)
    print(f"Step {i}: Energy = {energy:.6f} Ha")
```

### Switch Between Devices

```python
# Define the circuit body once, bind it to a device on demand.
def circuit_body(params):
    qml.AngleEmbedding(params, wires=range(4))
    return qml.expval(qml.PauliZ(0))

def make_qnode(dev):
    return qml.qnode(dev)(circuit_body)

# Test on simulator
dev_sim = qml.device('default.qubit', wires=4)
result_sim = make_qnode(dev_sim)(params)

# Run on quantum hardware (IBM, via Qiskit Runtime)
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService(channel='ibm_quantum_platform')  # requires saved IBM Cloud credentials
backend = service.least_busy(operational=True, simulator=False)
dev_hw = qml.device('qiskit.remote', wires=4, backend=backend)
# On hardware, build the QNode with diff_method='parameter-shift' for gradients.
result_hw = make_qnode(dev_hw)(params)
```

## Best Practices

1. **Start with simulators** - Test on `default.qubit` before deploying to hardware
2. **Use parameter-shift for hardware** - Backpropagation only works on simulators
3. **Choose appropriate encodings** - Match data encoding to problem structure
4. **Initialize carefully** - Use small random values to avoid barren plateaus
5. **Monitor gradients** - Check for vanishing gradients in deep circuits
6. **Cache devices** - Reuse device objects to reduce initialization overhead
7. **Profile circuits** - Use `qml.specs()` to analyze circuit complexity
8. **Test locally** - Validate on simulators before submitting to hardware
9. **Use templates** - Leverage built-in templates for common circuit patterns
10. **Compile when possible** - Use Catalyst JIT for performance-critical code

## Resources

- Official documentation: https://docs.pennylane.ai
- Codebook (tutorials): https://pennylane.ai/codebook
- QML demonstrations: https://pennylane.ai/qml/demonstrations
- Community forum: https://discuss.pennylane.ai
- GitHub: https://github.com/PennyLaneAI/pennylane

