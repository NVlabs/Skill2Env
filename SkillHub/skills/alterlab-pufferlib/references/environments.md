# PufferLib Environments Guide

## Overview

PufferLib provides the PufferEnv API for creating high-performance custom environments, and the Ocean suite containing 20+ pre-built environments. Environments support both single-agent and multi-agent scenarios with native vectorization.

## PufferEnv API

### Core Characteristics

PufferEnv is designed for performance through in-place operations:
- Observations, actions, and rewards are initialized from a shared buffer object
- All operations happen in-place to avoid creating and copying arrays
- Native support for both single-agent and multi-agent environments
- **Native spaces must be flat**: `single_observation_space` must be a `Box`, and `single_action_space` a `Discrete`, `MultiDiscrete`, or `Box`. A `Dict` (or other structured) observation space is **not** allowed for a native PufferEnv — the base class raises `APIUsageError`. If you need Dict/structured observations, build a Gymnasium env and use `pufferlib.emulation.GymnasiumPufferEnv`, which flattens them for you.

### Creating a PufferEnv

```python
import numpy as np
import gymnasium
import pufferlib
from pufferlib import PufferEnv

class MyEnvironment(PufferEnv):
    def __init__(self, buf=None):
        # Define spaces and num_agents BEFORE super().__init__(buf).
        # Native obs space MUST be a Box (no Dict). Here: an 84x84x3 image.
        self.single_observation_space = gymnasium.spaces.Box(
            low=0, high=255, shape=(84, 84, 3), dtype=np.uint8)
        self.single_action_space = gymnasium.spaces.Discrete(4)  # 4 discrete actions
        self.num_agents = 1

        super().__init__(buf)

    def reset(self, seed=None):
        """Reset environment to initial state. Returns (obs, info-list)."""
        # Reset internal state
        self.agent_pos = np.array([0, 0])
        self.step_count = 0

        # Return initial observation and an (empty) info LIST (asserted by PufferEnv)
        obs = np.zeros((84, 84, 3), dtype=np.uint8)
        return obs, []

    def step(self, action):
        """Execute one environment step. Returns 5 values."""
        # Update state based on action
        self.step_count += 1

        # Calculate reward
        rewards = self._compute_reward()

        # Check termination vs. truncation
        terminals = self._is_done()
        truncations = self.step_count >= 1000

        # Generate observation
        obs = self._get_observation()

        # Additional info (list of dicts; PufferEnv asserts info is a list)
        info = [{'episode': {'r': rewards, 'l': self.step_count}}] if truncations else []

        return obs, rewards, terminals, truncations, info

    def _compute_reward(self):
        """Compute reward for current state."""
        return 1.0

    def _get_observation(self):
        """Generate observation from current state (a Box-shaped array)."""
        return np.random.randint(0, 256, (84, 84, 3), dtype=np.uint8)
```

### Observation Spaces

Define spaces directly with `gymnasium.spaces` and assign them to
`self.single_observation_space` / `self.single_action_space` before calling
`super().__init__(buf)`.

#### Native observation spaces (Box only)

A native PufferEnv observation space must be a `Box`. Encode discrete or
heterogeneous state into a single Box vector/array:

```python
import gymnasium

# Flat continuous/feature vector
self.single_observation_space = gymnasium.spaces.Box(
    low=-np.inf, high=np.inf, shape=(10,), dtype=np.float32)

# Image observation
self.single_observation_space = gymnasium.spaces.Box(
    low=0, high=255, shape=(84, 84, 3), dtype=np.uint8)
```

#### Dict / structured observations (emulation path only)

`Dict` observation spaces are **not** valid for a native PufferEnv. To use them,
build a Gymnasium env and wrap it with `pufferlib.emulation.GymnasiumPufferEnv`,
which flattens the Dict to a Box for you (recover the structure in the policy via
`pufferlib.pytorch.nativize_tensor`):

```python
import gymnasium
# Inside a standard gymnasium.Env (NOT a PufferEnv):
observation_space = gymnasium.spaces.Dict({
    'image': gymnasium.spaces.Box(low=0, high=255, shape=(84, 84, 3), dtype=np.uint8),
    'vector': gymnasium.spaces.Box(low=-np.inf, high=np.inf, shape=(10,), dtype=np.float32),
})
```

### Action Spaces

```python
import gymnasium

# Discrete actions
self.single_action_space = gymnasium.spaces.Discrete(4)  # 4 actions: 0, 1, 2, 3

# Continuous actions
self.single_action_space = gymnasium.spaces.Box(
    low=-1.0, high=1.0, shape=(3,), dtype=np.float32)  # 3D continuous action

# Multi-discrete actions
self.single_action_space = gymnasium.spaces.MultiDiscrete([3, 3])  # Two 3-way discrete choices
```

## Multi-Agent Environments

PufferLib has native multi-agent support, treating single-agent and multi-agent environments uniformly: set `num_agents > 1` and use the **same** array-based API as a single-agent env. There is no `{agent_id: ...}` dict / `'__all__'` convention in native PufferEnv — that belongs to PettingZoo (use `pufferlib.emulation.PettingZooPufferEnv` for those). The native obs/reward/terminal/truncation buffers are simply sized along a leading agent axis, and `info` is a list of dicts.

### Multi-Agent PufferEnv

```python
import gymnasium
import numpy as np

class MultiAgentEnv(PufferEnv):
    def __init__(self, num_agents=4, buf=None):
        # Define spaces and num_agents BEFORE super().__init__(buf).
        # single_*_space is PER AGENT and must be a Box (obs) / Discrete-or-Box (action).
        self.num_agents = num_agents
        self.single_observation_space = gymnasium.spaces.Box(
            low=-np.inf, high=np.inf, shape=(14,), dtype=np.float32)  # e.g. pos+vel+global
        self.single_action_space = gymnasium.spaces.Discrete(5)

        super().__init__(buf)

    def reset(self, seed=None):
        """Reset all agents. Returns (obs, info-list)."""
        # obs is shaped (num_agents, *single_observation_space.shape)
        obs = np.zeros((self.num_agents, 14), dtype=np.float32)
        return obs, []

    def step(self, actions):
        """Step all agents. `actions` is an array of shape (num_agents, ...).
        Returns (obs, rewards, terminals, truncations, info-list) where the first
        four are arrays of length num_agents and info is a list of dicts."""
        obs = self._get_observations()                 # (num_agents, 14)
        rewards = self._compute_rewards()               # (num_agents,)
        terminals = self._terminated()                  # (num_agents,) bool
        truncations = self._truncated()                 # (num_agents,) bool
        info = []
        return obs, rewards, terminals, truncations, info
```

## Environments: Ocean vs. third-party bindings

PufferLib ships two distinct collections — keep them straight:

- **Ocean** (`pufferlib.ocean`) is PufferLib's own suite of fast, mostly native-C
  environments. It includes `breakout`, `pong`, `snake`, `enduro`, `freeway`,
  `connect4`, `go`, `g2048`, `tetris`, `pacman`, `nmmo3`, `moba`, `drive`,
  `rware`, `trash_pickup`, `cartpole`, `grid`, and many more (40+). These are the
  high-throughput envs the SPS benchmarks refer to.
- **Third-party bindings** (`pufferlib.environments.*`) wrap external suites:
  `atari`, `procgen`, `nethack`, `minihack`, `minigrid`, `crafter`, `craftax`,
  `butterfly` (PettingZoo), `magent`, `nmmo`, `gpudrive`, `microrts`, `griddly`,
  `pokemon_red`, `mujoco`, `dm_control`, `vizdoom`, and others. So Atari, Procgen,
  and NetHack are **bindings, not Ocean envs**.

### Using these environments

```python
import functools
import pufferlib.vector
import pufferlib.ocean

# Ocean (native): resolve a constructor with env_creator. The name is prefixed
# 'puffer_' (matching the CLI `puffer train puffer_breakout`).
breakout = pufferlib.ocean.environment.env_creator('puffer_breakout')
env = pufferlib.vector.make(breakout, num_envs=256)

# Bind constructor kwargs with functools.partial (PufferLib has no string registry).
snake = pufferlib.ocean.environment.env_creator('puffer_snake')
env = pufferlib.vector.make(functools.partial(snake, num_agents=4), num_envs=128)

# Third-party bindings live under pufferlib.environments.<name> and expose an
# `env_creator`. They are not native, so pass an explicit backend.
import pufferlib.environments.atari as atari
env = pufferlib.vector.make(
    atari.env_creator('BreakoutNoFrameskip-v4'),
    num_envs=128, backend=pufferlib.vector.Multiprocessing)
```

## Custom Environment Development

### Development Workflow

1. **Prototype in Python**: Start with pure Python PufferEnv
2. **Optimize Critical Paths**: Identify bottlenecks
3. **Implement in C**: Rewrite performance-critical code in C
4. **Create Bindings**: Use Python C API
5. **Compile**: Build as extension module
6. **Register**: Add to Ocean suite

### Performance Benchmarks

- **Pure Python**: 100k-500k steps/second
- **C Implementation**: 100M+ steps/second
- **Training with Python env**: ~400k total SPS
- **Training with C env**: ~4M total SPS

### Python Optimization Tips

```python
# Use NumPy operations instead of Python loops
# Bad
for i in range(len(array)):
    array[i] = array[i] * 2

# Good
array *= 2

# Pre-allocate arrays instead of appending
# Bad
observations = []
for i in range(n):
    observations.append(generate_obs())

# Good
observations = np.empty((n, obs_shape), dtype=np.float32)
for i in range(n):
    observations[i] = generate_obs()

# Use in-place operations
# Bad
new_state = state + delta

# Good
state += delta
```

### C Extension Example

```c
// my_env.c
#include <Python.h>
#include <numpy/arrayobject.h>

// Fast environment step implementation
static PyObject* fast_step(PyObject* self, PyObject* args) {
    PyArrayObject* state;
    int action;

    if (!PyArg_ParseTuple(args, "O!i", &PyArray_Type, &state, &action)) {
        return NULL;
    }

    // High-performance C implementation
    // ...

    return Py_BuildValue("Ofi", obs, reward, done);
}

static PyMethodDef methods[] = {
    {"fast_step", fast_step, METH_VARARGS, "Fast environment step"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "my_env_c",
    NULL,
    -1,
    methods
};

PyMODINIT_FUNC PyInit_my_env_c(void) {
    import_array();
    return PyModule_Create(&module);
}
```

## Third-Party Environment Integration

### Gymnasium Environments

```python
import gymnasium as gym
import pufferlib.emulation
import pufferlib.vector

# Wrap a Gymnasium env in a GymnasiumPufferEnv, then vectorize. Wrapped
# (non-native) envs require an explicit backend (default backend=PufferEnv is
# native-only).
def env_creator():
    return pufferlib.emulation.GymnasiumPufferEnv(
        env_creator=lambda: gym.make('CartPole-v1'))

env = pufferlib.vector.make(
    env_creator, num_envs=256, backend=pufferlib.vector.Multiprocessing)
```

### PettingZoo Environments

```python
from pettingzoo.butterfly import pistonball_v6
import pufferlib.emulation
import pufferlib.vector

# Wrap a PettingZoo env in a PettingZooPufferEnv, then vectorize.
def env_creator():
    return pufferlib.emulation.PettingZooPufferEnv(
        env_creator=lambda: pistonball_v6.parallel_env())

env = pufferlib.vector.make(
    env_creator, num_envs=128, backend=pufferlib.vector.Multiprocessing)
```

### Custom Wrappers

A PufferEnv defines `single_observation_space` / `single_action_space` — assigning
`observation_space` / `action_space` is rejected by the base class. Mirror the
wrapped env's *single* spaces, set `num_agents` before `super().__init__`, and keep
the native 5-tuple step signature.

```python
class CustomWrapper(pufferlib.PufferEnv):
    """Wrapper to modify a native PufferEnv's behavior."""

    def __init__(self, base_env, buf=None):
        self.base_env = base_env
        # Copy the per-agent spaces (NOT observation_space/action_space).
        self.single_observation_space = base_env.single_observation_space
        self.single_action_space = base_env.single_action_space
        self.num_agents = base_env.num_agents
        super().__init__(buf)

    def reset(self, seed=None):
        obs, info = self.base_env.reset(seed)
        return self._process_obs(obs), info

    def step(self, action):
        action = self._process_action(action)
        obs, rewards, terminals, truncations, info = self.base_env.step(action)
        obs = self._process_obs(obs)
        rewards = self._process_reward(rewards)
        return obs, rewards, terminals, truncations, info
```

## Environment Best Practices

### State Management

```python
# Store minimal state, compute on demand
class EfficientEnv(PufferEnv):
    def __init__(self, buf=None):
        super().__init__(buf)
        self.agent_pos = np.zeros(2)  # Minimal state

    def _get_observation(self):
        # Compute full observation on demand
        observation = np.zeros((84, 84, 3), dtype=np.uint8)
        self._render_scene(observation, self.agent_pos)
        return observation
```

### Reward Scaling

```python
# Normalize rewards to reasonable range
def step(self, action):
    # ... environment logic ...

    # Scale large rewards
    raw_reward = compute_raw_reward()
    reward = np.clip(raw_reward / 100.0, -10, 10)

    return obs, reward, terminal, truncation, info
```

### Episode Termination

PufferLib keeps termination and truncation separate (the 4th return value).
A time limit is a *truncation*; reaching a goal/failure is a *termination*.

```python
def step(self, action):
    # ... environment logic ...

    terminal = self._check_success() or self._check_failure()  # task-ending
    truncation = self.step_count >= self.max_steps             # time limit
    info = [{'success': self._check_success()}] if (terminal or truncation) else []

    return obs, reward, terminal, truncation, info
```

### Memory Efficiency

```python
# Reuse buffers instead of allocating new ones
class MemoryEfficientEnv(PufferEnv):
    def __init__(self, buf=None):
        super().__init__(buf)

        # Pre-allocate observation buffer
        self._obs_buffer = np.zeros((84, 84, 3), dtype=np.uint8)

    def _get_observation(self):
        # Reuse buffer, modify in place
        self._render_scene(self._obs_buffer)
        return self._obs_buffer  # Return view, not copy
```

## Debugging Environments

### Validation Checks

```python
# Add assertions to catch bugs. Note: PufferEnv exposes single_*_space (per agent);
# observation_space/action_space are the joint (batched) spaces set by the base class.
def step(self, action):
    obs, reward, terminal, truncation, info = self._step_impl(action)

    assert self.single_observation_space.contains(obs), "Invalid observation"
    assert np.all(np.isfinite(reward)), "Non-finite reward"

    return obs, reward, terminal, truncation, info
```

### Rendering

```python
class DebuggableEnv(PufferEnv):
    def __init__(self, buf=None, render_mode=None):
        super().__init__(buf)
        self.render_mode = render_mode

    def render(self):
        """Render environment for debugging."""
        if self.render_mode == 'human':
            # Display to screen
            self._display_scene()
        elif self.render_mode == 'rgb_array':
            # Return image
            return self._render_to_array()
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)

def step(self, action):
    logger.debug(f"Step {self.step_count}: action={action}")

    obs, reward, terminal, truncation, info = self._step_impl(action)

    if np.any(terminal) or np.any(truncation):
        logger.info(f"Episode finished: reward={self.total_reward}")

    return obs, reward, terminal, truncation, info
```
