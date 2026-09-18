---
name: alterlab-pufferlib
description: Scales reinforcement learning with PufferLib — high-throughput parallel training (PuffeRL), vectorized environments, and native multi-agent systems achieving 2-10x speedups over standard implementations. Use when scaling RL to millions of steps per second, running vectorized or multi-agent setups, building custom PufferEnv tasks, or integrating game environments (Atari, Procgen, NetHack, PettingZoo). For standard single-agent algorithm implementations (PPO/SAC/DQN) or quick prototyping prefer alterlab-stable-baselines3. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: No API key required. Runs locally via `uv run python`; requires the pufferlib Python package (GPU optional for faster training). Targets PufferLib 3.0.x (the current PyPI release); the dev `4.0` branch has a different, unstable API.
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# PufferLib - High-Performance Reinforcement Learning

## Overview

PufferLib is a high-performance reinforcement learning library designed for fast parallel environment simulation and training. It achieves training at millions of steps per second through optimized vectorization, native multi-agent support, and efficient PPO implementation (PuffeRL). The library provides the Ocean suite of 20+ environments and seamless integration with Gymnasium, PettingZoo, and specialized RL frameworks.

## When to Use This Skill

Use this skill when:
- **Training RL agents** with PPO on any environment (single or multi-agent)
- **Creating custom environments** using the PufferEnv API
- **Optimizing performance** for parallel environment simulation (vectorization)
- **Integrating existing environments** from Gymnasium, PettingZoo, Atari, Procgen, etc.
- **Developing policies** with CNN, LSTM, or custom architectures
- **Scaling RL** to millions of steps per second for faster experimentation
- **Multi-agent RL** with native multi-agent environment support

## Core Capabilities

### 1. High-Performance Training (PuffeRL)

PuffeRL is PufferLib's optimized PPO trainer (CleanRL-derived, with optional LSTM via `models.LSTMWrapper`) built for high-throughput training.

**Recommended path — CLI / high-level helper.** Drive training from a config (an `.ini` in `pufferlib/config/`) rather than hand-wiring the trainer:
```bash
# CLI: env name resolves to a registered config + Ocean env
puffer train puffer_breakout --train.device cuda --train.learning-rate 0.015
```
```python
import pufferlib.pufferl as pufferl
# train(env_name, args=None, vecenv=None, policy=None, logger=None)
pufferl.train('puffer_breakout')
```

**Manual loop.** `PuffeRL(config, vecenv, policy, logger=None)` — note the first arg is a **config dict** (not flat kwargs), the env arg is `vecenv`, and the loop is driven by `global_step`. The three loop methods are real: `evaluate()`, `train()`, `mean_and_log()`.
```python
import pufferlib.vector
from pufferlib.pufferl import PuffeRL, load_config

# Native PufferEnv -> default backend=PufferEnv. For wrapped (Gymnasium/
# PettingZoo) envs you MUST pass backend=pufferlib.vector.Multiprocessing.
vecenv = pufferlib.vector.make(MyPufferEnv, num_envs=256)

# load_config returns a nested args dict (sections: 'train', 'vec', 'env', ...)
# with defaults from pufferlib/config/*.ini. PuffeRL takes the 'train' section.
args = load_config('puffer_breakout')
config = {**args['train'], 'env': 'puffer_breakout'}
config['device'] = 'cuda'

trainer = PuffeRL(config, vecenv, my_policy)
while trainer.global_step < config['total_timesteps']:
    trainer.evaluate()      # Collect rollouts
    trainer.train()         # Train on batch
    trainer.mean_and_log()  # Aggregate + log
```

**For comprehensive training guidance**, read `references/training.md` for:
- Complete training workflow and CLI options
- Hyperparameter tuning with Protein
- Distributed multi-GPU/multi-node training
- Logger integration (Weights & Biases, Neptune)
- Checkpointing and resume training
- Performance optimization tips
- Curriculum learning patterns

### 2. Environment Development (PufferEnv)

Create custom high-performance environments with the PufferEnv API.

**Basic environment structure:**
```python
import numpy as np
import gymnasium
from pufferlib import PufferEnv

class MyEnvironment(PufferEnv):
    def __init__(self, buf=None):
        # Define spaces BEFORE calling super().__init__(buf)
        self.single_observation_space = gymnasium.spaces.Box(
            low=-np.inf, high=np.inf, shape=(4,), dtype=np.float32)
        self.single_action_space = gymnasium.spaces.Discrete(4)
        self.num_agents = 1

        super().__init__(buf)

    def reset(self, seed=None):
        # Reset state and return (observation, info-list)
        obs = self._get_observation()
        return obs, []

    def step(self, action):
        # Execute action, compute reward, check termination/truncation
        obs = self._get_observation()
        rewards = self._compute_reward()
        terminals = self._is_done()
        truncations = self._is_truncated()
        info = []

        return obs, rewards, terminals, truncations, info
```

**Use the template script:** `scripts/env_template.py` provides complete single-agent and multi-agent environment templates with examples of:
- Different observation space types (vector, image, dict)
- Action space variations (discrete, continuous, multi-discrete)
- Multi-agent environment structure
- Testing utilities

**For complete environment development**, read `references/environments.md` for:
- PufferEnv API details and in-place operation patterns
- Observation and action space definitions
- Multi-agent environment creation
- Ocean suite (20+ pre-built environments)
- Performance optimization (Python to C workflow)
- Environment wrappers and best practices
- Debugging and validation techniques

### 3. Vectorization and Performance

Achieve maximum throughput with optimized parallel simulation.

**Vectorization setup:**
```python
import pufferlib.vector

# Pass an env-constructor callable. Default backend=PufferEnv is native-only;
# for wrapped (Gymnasium/PettingZoo) envs add backend=pufferlib.vector.Multiprocessing.
env = pufferlib.vector.make(env_creator, num_envs=256, num_workers=8)

# Performance benchmarks (PufferLib's published figures; vary by env/hardware):
# - Pure Python envs: 100k-500k SPS
# - C-based envs: 100M+ SPS
# - With training: 400k-4M total SPS
```

**Key optimizations:**
- Shared memory buffers for zero-copy observation passing
- Busy-wait flags instead of pipes/queues
- Surplus environments for async returns
- Multiple environments per worker

**For vectorization optimization**, read `references/vectorization.md` for:
- Architecture and performance characteristics
- Worker and batch size configuration
- Serial vs multiprocessing vs async modes
- Shared memory and zero-copy patterns
- Hierarchical vectorization for large scale
- Multi-agent vectorization strategies
- Performance profiling and troubleshooting

### 4. Policy Development

Build policies as standard PyTorch modules with optional utilities.

**Basic policy structure:**
```python
import torch.nn as nn
from pufferlib.pytorch import layer_init

class Policy(nn.Module):
    def __init__(self, observation_space, action_space):
        super().__init__()

        # Encoder
        self.encoder = nn.Sequential(
            layer_init(nn.Linear(obs_dim, 256)),
            nn.ReLU(),
            layer_init(nn.Linear(256, 256)),
            nn.ReLU()
        )

        # Actor and critic heads
        self.actor = layer_init(nn.Linear(256, num_actions), std=0.01)
        self.critic = layer_init(nn.Linear(256, 1), std=1.0)

    def forward(self, observations):
        features = self.encoder(observations)
        return self.actor(features), self.critic(features)
```

**For complete policy development**, read `references/policies.md` for:
- CNN policies for image observations
- Recurrent policies with optimized LSTM (3x faster inference)
- Multi-input policies for complex observations
- Continuous action policies
- Multi-agent policies (shared vs independent parameters)
- Advanced architectures (attention, residual)
- Observation normalization and gradient clipping
- Policy debugging and testing

### 5. Environment Integration

Seamlessly integrate environments from popular RL frameworks.

**Gymnasium integration:**
```python
import gymnasium as gym
import pufferlib.emulation
import pufferlib.vector

# Wrap a Gymnasium env in a GymnasiumPufferEnv, then vectorize.
# Wrapped (non-native) envs require an explicit backend (Serial or Multiprocessing);
# the default backend=PufferEnv is only for native PufferEnvs.
def env_creator():
    return pufferlib.emulation.GymnasiumPufferEnv(
        env_creator=lambda: gym.make('CartPole-v1'))

env = pufferlib.vector.make(
    env_creator, num_envs=256, backend=pufferlib.vector.Multiprocessing)
```

**PettingZoo multi-agent:**
```python
import pufferlib.emulation
import pufferlib.vector
from pettingzoo.butterfly import knights_archers_zombies_v10

# Wrap a PettingZoo env in a PettingZooPufferEnv, then vectorize.
def env_creator():
    return pufferlib.emulation.PettingZooPufferEnv(
        env_creator=lambda: knights_archers_zombies_v10.parallel_env())

env = pufferlib.vector.make(
    env_creator, num_envs=128, backend=pufferlib.vector.Multiprocessing)
```

**Supported frameworks:**
- Gymnasium / OpenAI Gym
- PettingZoo (parallel and AEC)
- Atari (ALE)
- Procgen
- NetHack / MiniHack
- Minigrid
- Neural MMO
- Crafter
- GPUDrive
- MicroRTS
- Griddly
- And more...

**For integration details**, read `references/integration.md` for:
- Complete integration examples for each framework
- Custom wrappers (observation, reward, frame stacking, action repeat)
- Space flattening and unflattening
- Environment registration
- Compatibility patterns
- Performance considerations
- Integration debugging

## Quick Start Workflow

### For Training Existing Environments

1. Choose environment from Ocean suite or compatible framework
2. Use `scripts/train_template.py` as starting point
3. Configure hyperparameters for your task
4. Run training with CLI or Python script
5. Monitor with Weights & Biases or Neptune
6. Refer to `references/training.md` for optimization

### For Creating Custom Environments

1. Start with `scripts/env_template.py`
2. Define observation and action spaces
3. Implement `reset()` and `step()` methods
4. Test environment locally
5. Wrap with `pufferlib.emulation.GymnasiumPufferEnv` and vectorize with `pufferlib.vector.make()`
6. Refer to `references/environments.md` for advanced patterns
7. Optimize with `references/vectorization.md` if needed

### For Policy Development

1. Choose architecture based on observations:
   - Vector observations → MLP policy
   - Image observations → CNN policy
   - Sequential tasks → LSTM policy
   - Complex observations → Multi-input policy
2. Use `layer_init` for proper weight initialization
3. Follow patterns in `references/policies.md`
4. Test with environment before full training

### For Performance Optimization

1. Profile current throughput (steps per second)
2. Check vectorization configuration (num_envs, num_workers)
3. Optimize environment code (in-place ops, numpy vectorization)
4. Consider C implementation for critical paths
5. Use `references/vectorization.md` for systematic optimization

## Resources

### scripts/

**train_template.py** - Complete training script template with:
- Environment creation and configuration
- Policy initialization
- Logger integration (WandB, Neptune)
- Training loop with checkpointing
- Command-line argument parsing
- Multi-GPU distributed training setup

**env_template.py** - Environment implementation templates:
- Single-agent PufferEnv example (grid world)
- Multi-agent PufferEnv example (cooperative navigation)
- Multiple observation/action space patterns
- Testing utilities

### references/

**training.md** - Comprehensive training guide:
- Training workflow and CLI options
- Hyperparameter configuration
- Distributed training (multi-GPU, multi-node)
- Monitoring and logging
- Checkpointing
- Protein hyperparameter tuning
- Performance optimization
- Common training patterns
- Troubleshooting

**environments.md** - Environment development guide:
- PufferEnv API and characteristics
- Observation and action spaces
- Multi-agent environments
- Ocean suite environments
- Custom environment development workflow
- Python to C optimization path
- Third-party environment integration
- Wrappers and best practices
- Debugging

**vectorization.md** - Vectorization optimization:
- Architecture and key optimizations
- Vectorization modes (serial, multiprocessing, async)
- Worker and batch configuration
- Shared memory and zero-copy patterns
- Advanced vectorization (hierarchical, custom)
- Multi-agent vectorization
- Performance monitoring and profiling
- Troubleshooting and best practices

**policies.md** - Policy architecture guide:
- Basic policy structure
- CNN policies for images
- LSTM policies with optimization
- Multi-input policies
- Continuous action policies
- Multi-agent policies
- Advanced architectures (attention, residual)
- Observation processing and unflattening
- Initialization and normalization
- Debugging and testing

**integration.md** - Framework integration guide:
- Gymnasium integration
- PettingZoo integration (parallel and AEC)
- Third-party environments (Procgen, NetHack, Minigrid, etc.)
- Custom wrappers (observation, reward, frame stacking, etc.)
- Space conversion and unflattening
- Environment registration
- Compatibility patterns
- Performance considerations
- Debugging integration

## Tips for Success

1. **Start simple**: Begin with Ocean environments or Gymnasium integration before creating custom environments

2. **Profile early**: Measure steps per second from the start to identify bottlenecks

3. **Use templates**: `scripts/train_template.py` and `scripts/env_template.py` provide solid starting points

4. **Read references as needed**: Each reference file is self-contained and focused on a specific capability

5. **Optimize progressively**: Start with Python, profile, then optimize critical paths with C if needed

6. **Leverage vectorization**: PufferLib's vectorization is key to achieving high throughput

7. **Monitor training**: Use WandB or Neptune to track experiments and identify issues early

8. **Test environments**: Validate environment logic before scaling up training

9. **Check existing environments**: Ocean suite provides 20+ pre-built environments

10. **Use proper initialization**: Always use `layer_init` from `pufferlib.pytorch` for policies

## Common Use Cases

### Training on Standard Benchmarks
```python
import pufferlib.vector

# Atari (pass an env-constructor callable)
env = pufferlib.vector.make(make_pong_env, num_envs=256)

# Procgen
env = pufferlib.vector.make(make_coinrun_env, num_envs=256)

# Minigrid
env = pufferlib.vector.make(make_minigrid_env, num_envs=256)
```

### Multi-Agent Learning
```python
import pufferlib.vector

# PettingZoo, wrapped via PettingZooPufferEnv (needs an explicit backend)
env = pufferlib.vector.make(
    make_pistonball_env, num_envs=128, backend=pufferlib.vector.Multiprocessing)

# One shared policy serves all agents (single_observation_space / single_action_space
# are per-agent). Pass config (dict), vecenv, policy positionally to PuffeRL.
policy = create_policy(env.single_observation_space, env.single_action_space)
trainer = PuffeRL(config, env, policy)
```

### Custom Task Development
```python
import pufferlib.vector

# Create custom environment (a native PufferEnv subclass)
class MyTask(PufferEnv):
    # ... implement environment ...

# Native PufferEnv -> default backend=PufferEnv is fine here.
env = pufferlib.vector.make(MyTask, num_envs=256)
trainer = PuffeRL(config, env, my_policy)  # config is a dict (see Training above)
```

### High-Performance Optimization
```python
import pufferlib.vector

# Maximize throughput (pass an env-constructor callable)
env = pufferlib.vector.make(
    my_env_creator,     # env constructor callable
    num_envs=1024,      # Large batch
    num_workers=16,     # Many workers
    backend=pufferlib.vector.Multiprocessing,
)
```

## Installation

```bash
# Pin the 3.0 line — the config-dict trainer API and import paths in this skill
# target it. The dev 4.0 branch differs.
uv pip install "pufferlib==3.0.*"
```

## Documentation

- Official docs: https://puffer.ai/docs.html
- GitHub: https://github.com/PufferAI/PufferLib
- Discord: Community support available

