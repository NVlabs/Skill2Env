# PufferLib Vectorization Guide

## Overview

PufferLib's vectorization system enables high-performance parallel environment simulation, achieving millions of steps per second through optimized implementation inspired by EnvPool. The system supports both synchronous and asynchronous vectorization with minimal overhead.

## Vectorization Architecture

### Key Optimizations

1. **Shared Memory Buffer**: Single unified buffer across all environments (unlike Gymnasium's per-environment buffers)
2. **Busy-Wait Flags**: Workers busy-wait on unlocked flags rather than using pipes/queues
3. **Zero-Copy Batching**: Contiguous worker subsets return observations without copying
4. **Surplus Environments**: Simulates more environments than batch size for async returns
5. **Multiple Envs per Worker**: Optimizes performance for lightweight environments

### Performance Characteristics

- **Pure Python environments**: 100k-500k SPS
- **C-based environments**: 100M+ SPS
- **With training**: 400k-4M total SPS
- **Vectorization overhead**: <5% with optimal configuration

## Creating Vectorized Environments

### Basic Vectorization

```python
import pufferlib.vector

# PufferLib has no string registry -- pass an environment constructor
# (callable) to `pufferlib.vector.make`. `env_creator` is a placeholder for
# the callable that builds your env (a PufferEnv class, or a function /
# functools.partial that returns one).

# Native PufferEnv (default backend=PufferEnv)
env = pufferlib.vector.make(env_creator, num_envs=256)

# With explicit configuration. envs-per-worker is derived as num_envs // num_workers.
env = pufferlib.vector.make(
    env_creator,
    num_envs=256,
    num_workers=8,
    backend=pufferlib.vector.Multiprocessing,
)
```

### Choosing a backend

The backends live in `pufferlib.vector` (`Serial`, `Multiprocessing`, `Ray`) — there is **no `pufferlib.vectorization` module**. In normal use you do not instantiate them directly; you pass the class as the `backend=` argument to `pufferlib.vector.make`:

```python
import pufferlib.vector

# Serial — single process, easy debugging
env = pufferlib.vector.make(
    MyEnvironment, num_envs=16, backend=pufferlib.vector.Serial)

# Multiprocessing — parallel workers (required for wrapped Gymnasium/PettingZoo envs)
env = pufferlib.vector.make(
    MyEnvironment, num_envs=256, num_workers=8,
    backend=pufferlib.vector.Multiprocessing)

# Native (default) — a native PufferEnv that handles per-process batching itself
env = pufferlib.vector.make(MyNativePufferEnv, num_envs=256)  # backend=PufferEnv
```

## Vectorization Modes

`pufferlib.vector.make` accepts only these extra kwargs: `num_workers`, `batch_size`, `zero_copy`, `overwork`, `backend` (plus `num_envs`, `seed`, `env_args`, `env_kwargs`). Passing anything else (e.g. `envs_per_worker`, `mode`, `surplus_envs`) raises `APIUsageError`.

### Serial

Best for debugging and lightweight environments — all envs run in the main process:

```python
import pufferlib.vector

env = pufferlib.vector.make(
    env_creator, num_envs=16, backend=pufferlib.vector.Serial)
```

**When to use:** development/debugging, very fast envs, small env counts, single-threaded profiling.

### Multiprocessing

Best for most production use cases and required for wrapped Gymnasium/PettingZoo envs:

```python
import pufferlib.vector

env = pufferlib.vector.make(
    env_creator, num_envs=256, num_workers=8,
    backend=pufferlib.vector.Multiprocessing)
```

**When to use:** production training, CPU-intensive envs, large-scale parallel simulation.

### Asynchronous batching (surplus envs)

There is no `mode='async'` flag. Async-style behavior comes from setting
`batch_size` smaller than `num_envs`: PufferLib simulates the surplus
environments and returns the first `batch_size` agents that are ready, which
improves GPU utilization with variable step times.

```python
env = pufferlib.vector.make(
    env_creator, num_envs=256, batch_size=128, num_workers=8,
    backend=pufferlib.vector.Multiprocessing)  # 128 surplus envs hide stragglers
```

## Optimizing Vectorization Performance

### Worker Configuration

```python
import multiprocessing

# Calculate optimal workers
num_cpus = multiprocessing.cpu_count()

# Conservative (leave headroom for training)
num_workers = num_cpus - 2

# Aggressive (maximize environment throughput)
num_workers = num_cpus

# With hyperthreading
num_workers = num_cpus // 2  # Physical cores only
```

### Envs per worker (derived, not a kwarg)

PufferLib computes envs-per-worker as `num_envs // num_workers` — there is no
`envs_per_worker` argument. Tune the ratio by choosing `num_envs` and
`num_workers`:

```python
# Fast envs -> pack many per worker (high num_envs / num_workers ratio)
env = pufferlib.vector.make(env_creator, num_envs=512, num_workers=8,    # 64 each
    backend=pufferlib.vector.Multiprocessing)

# Slow envs -> fewer per worker
env = pufferlib.vector.make(env_creator, num_envs=128, num_workers=8,    # 16 each
    backend=pufferlib.vector.Multiprocessing)
```

### Batch Size Tuning

```python
# Small batch (< 8k): Good for fast iteration
batch_size = 4096
num_envs = 256
steps_per_env = batch_size // num_envs  # 16 steps

# Medium batch (8k-32k): Good balance
batch_size = 16384
num_envs = 512
steps_per_env = 32

# Large batch (> 32k): Maximum throughput
batch_size = 65536
num_envs = 1024
steps_per_env = 64
```

## Shared Memory Optimization

### Buffer Management

PufferLib uses shared memory for zero-copy observation passing:

```python
import numpy as np
import gymnasium

class OptimizedEnv(PufferEnv):
    def __init__(self, buf=None):
        # Define spaces and num_agents BEFORE super().__init__(buf).
        # Native obs space must be a Box.
        self.single_observation_space = gymnasium.spaces.Box(
            low=0, high=255, shape=(84, 84, 3), dtype=np.uint8)
        self.single_action_space = gymnasium.spaces.Discrete(4)
        self.num_agents = 1

        # super().__init__ calls set_buffers, which allocates the shared buffers
        # self.observations / self.rewards / self.terminals / self.truncations.
        super().__init__(buf)

    def reset(self, seed=None):
        # Write directly into the shared observation buffer (no allocation).
        self._render_to_buffer(self.observations)
        return self.observations, []

    def step(self, action):
        self._update_state(action)
        self._render_to_buffer(self.observations)  # in-place into shared buffer

        # Write reward/flags into the shared buffers, then return them.
        self.rewards[:] = self._reward()
        self.terminals[:] = self._terminated()
        self.truncations[:] = self._truncated()
        return self.observations, self.rewards, self.terminals, self.truncations, []
```

### Zero-Copy Patterns

```python
# BAD: Creates copies
def get_observation(self):
    obs = np.zeros((84, 84, 3))
    # ... fill obs ...
    return obs.copy()  # Unnecessary copy!

# GOOD: Reuses buffer
def get_observation(self):
    # Use pre-allocated buffer
    self._render_to_buffer(self._obs_buffer)
    return self._obs_buffer  # No copy

# BAD: Allocates new arrays
def step(self, action):
    new_state = self.state + action  # Allocates
    self.state = new_state
    return obs, reward, terminal, truncation, info

# GOOD: In-place operations
def step(self, action):
    self.state += action  # In-place
    return obs, reward, terminal, truncation, info
```

## Advanced Vectorization

### Wrapping a vecenv

There is no public `VectorEnv` base class to subclass. To add custom behavior,
wrap the object returned by `pufferlib.vector.make` and delegate `reset`/`step`:

```python
import pufferlib.vector

class CustomVecWrapper:
    """Illustrative wrapper around a PufferLib vecenv."""

    def __init__(self, vecenv):
        self.vecenv = vecenv
        self.num_envs = vecenv.num_envs
        self.single_observation_space = vecenv.single_observation_space
        self.single_action_space = vecenv.single_action_space

    def reset(self, seed=0):
        return self.vecenv.reset(seed)

    def step(self, actions):
        return self.vecenv.step(actions)  # delegate, then post-process as needed

vecenv = pufferlib.vector.make(
    env_creator, num_envs=256, backend=pufferlib.vector.Multiprocessing)
vecenv = CustomVecWrapper(vecenv)
```

### Large-scale parallelism

PufferLib already packs `num_envs // num_workers` environments into each worker
process, so a single `make` call covers the "hierarchical" case — you do not
nest backends. Scale by raising `num_envs` and `num_workers`:

```python
# 256 envs across 8 workers => 32 envs per worker, handled internally.
env = pufferlib.vector.make(
    env_creator, num_envs=256, num_workers=8,
    backend=pufferlib.vector.Multiprocessing)
```

## Multi-Agent Vectorization

### Native Multi-Agent Support

PufferLib treats multi-agent environments as first-class citizens:

```python
import functools
import pufferlib.vector

# Multi-agent environment automatically vectorized.
# PufferLib has no string registry -- pass an environment constructor
# (callable). For PettingZoo envs, wrap them with
# pufferlib.emulation.PettingZooPufferEnv inside the creator. `MultiAgentEnv`
# here is your own multi-agent PufferEnv class / creator callable; bind
# constructor kwargs with functools.partial.
env = pufferlib.vector.make(
    functools.partial(MultiAgentEnv, num_agents=4),
    num_envs=128,
)

# Observations: {agent_id: [batch_obs]} for each agent
# Actions: {agent_id: [batch_actions]} for each agent
# Rewards: {agent_id: [batch_rewards]} for each agent
```

Multi-agent vectorization is handled internally — you do not implement a custom
vectorizer. Pass your multi-agent PufferEnv (or a PettingZooPufferEnv-wrapped
env) to `pufferlib.vector.make` and PufferLib batches across agents and envs.

## Performance Monitoring

### Profiling Vectorization

```python
import time

def profile_vectorization(vec_env, num_steps=10000):
    """Profile vectorization performance."""
    start = time.time()

    vec_env.reset()

    for _ in range(num_steps):
        actions = vec_env.action_space.sample()
        vec_env.step(actions)

    elapsed = time.time() - start
    sps = (num_steps * vec_env.num_envs) / elapsed

    print(f"Steps per second: {sps:,.0f}")
    print(f"Time per step: {elapsed/num_steps*1000:.2f}ms")

    return sps
```

### Bottleneck Analysis

```python
import cProfile
import pstats

def analyze_bottlenecks(vec_env):
    """Identify vectorization bottlenecks."""
    profiler = cProfile.Profile()

    profiler.enable()

    vec_env.reset()
    for _ in range(1000):
        actions = vec_env.action_space.sample()
        vec_env.step(actions)

    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)
```

### Real-Time Monitoring

```python
class MonitoredVecEnv:
    """Wraps a PufferLib vecenv to log throughput (no base class to subclass)."""

    def __init__(self, vecenv):
        self.vecenv = vecenv
        self.num_envs = vecenv.num_envs
        self.step_times = []
        self.step_count = 0

    def reset(self, seed=0):
        return self.vecenv.reset(seed)

    def step(self, actions):
        start = time.perf_counter()
        result = self.vecenv.step(actions)
        self.step_times.append(time.perf_counter() - start)
        self.step_count += 1

        if self.step_count % 1000 == 0:
            mean_time = np.mean(self.step_times[-1000:])
            sps = self.num_envs / mean_time
            print(f"SPS: {sps:,.0f} | Step time: {mean_time*1000:.2f}ms")

        return result
```

## Troubleshooting

### Low Throughput

```python
# Check configuration
print(f"Num envs: {vec_env.num_envs}")
print(f"Num workers: {vec_env.num_workers}")
print(f"Envs per worker: {vec_env.num_envs // vec_env.num_workers}")

# Profile single environment
single_env = MyEnvironment()
single_sps = profile_single_env(single_env)
print(f"Single env SPS: {single_sps:,.0f}")

# Compare vectorized
vec_sps = profile_vectorization(vec_env)
print(f"Vectorized SPS: {vec_sps:,.0f}")
print(f"Speedup: {vec_sps / single_sps:.1f}x")
```

### Memory Issues

```python
import pufferlib.vector

# Reduce number of environments (lowers per-worker env count too)
env = pufferlib.vector.make(
    env_creator, num_envs=128, num_workers=8,   # was num_envs=256
    backend=pufferlib.vector.Multiprocessing)

# Use the Serial backend for debugging (single process)
env = pufferlib.vector.make(
    env_creator, num_envs=16, backend=pufferlib.vector.Serial)
```

### Synchronization Problems

```python
# Ensure thread-safe operations
import threading

class ThreadSafeEnv(PufferEnv):
    def __init__(self, buf=None):
        super().__init__(buf)
        self.lock = threading.Lock()

    def step(self, action):
        with self.lock:
            return super().step(action)
```

## Best Practices

### Configuration Guidelines

Tune `num_envs` and `num_workers` (envs-per-worker is the derived ratio):

```python
# Start conservative, then scale up iteratively.
vec_kwargs = dict(num_envs=64, num_workers=4)      # 16 envs/worker
vec_kwargs = dict(num_envs=256, num_workers=8)     # 32 envs/worker

# Monitor and adjust:
#   sps below target  -> raise num_envs and/or num_workers
#   memory too high   -> lower num_envs (and consider cpu_offload in training)
```

### Environment Design

```python
# Minimize per-step allocations
class EfficientEnv(PufferEnv):
    def __init__(self, buf=None):
        super().__init__(buf)

        # Pre-allocate all buffers
        self._obs = np.zeros((84, 84, 3), dtype=np.uint8)
        self._state = np.zeros(10, dtype=np.float32)

    def step(self, action):
        # Use pre-allocated buffers
        self._update_state_inplace(action)
        self._render_to_obs()

        return self._obs, reward, terminal, truncation, info
```

### Testing

```python
import numpy as np
import pufferlib.vector

# Verify the Multiprocessing backend matches Serial for the same seed.
serial_env = pufferlib.vector.make(
    env_creator, num_envs=4, seed=42, backend=pufferlib.vector.Serial)
vec_env = pufferlib.vector.make(
    env_creator, num_envs=4, num_workers=2, seed=42,
    backend=pufferlib.vector.Multiprocessing)

serial_obs, _ = serial_env.reset(seed=42)
vec_obs, _ = vec_env.reset(seed=42)

assert np.allclose(serial_obs, vec_obs), "Vectorization mismatch!"
```
