# PufferLib Integration Guide

> Targets PufferLib **3.0.x**.
>
> **Critical rule for this whole guide:** any env wrapped via the emulation layer
> (`GymnasiumPufferEnv` / `PettingZooPufferEnv`) is *not* a native PufferEnv, so
> `pufferlib.vector.make` requires an explicit `backend=pufferlib.vector.Multiprocessing`
> (or `Serial`). The default `backend=PufferEnv` is native-only and raises
> `APIUsageError` on a wrapped env. The examples below omit it for brevity only where
> noted — add it in real code.

## Overview

PufferLib provides an emulation layer that enables seamless integration with popular RL frameworks including Gymnasium, OpenAI Gym, PettingZoo, and many specialized environment libraries. The emulation layer flattens observation and action spaces for efficient vectorization while maintaining compatibility. Many third-party suites also ship ready-made bindings under `pufferlib.environments.*` (e.g. `atari`, `procgen`, `nethack`, `minigrid`, `crafter`), each exposing an `env_creator`.

## Gymnasium Integration

### Basic Gymnasium Environments

```python
import gymnasium as gym
import pufferlib.emulation
import pufferlib.vector

# PufferLib has no string registry -- pass an environment constructor
# (callable) to `pufferlib.vector.make`. There is no top-level
# `pufferlib.emulate`/`pufferlib.make`; wrap Gymnasium envs with
# `pufferlib.emulation.GymnasiumPufferEnv`, then vectorize.

# Method 1: Wrap a single Gymnasium env, then vectorize.
# Wrapped envs require an explicit backend (default backend=PufferEnv is native-only).
def cartpole_creator():
    return pufferlib.emulation.GymnasiumPufferEnv(
        env_creator=lambda: gym.make('CartPole-v1'))

env = pufferlib.vector.make(
    cartpole_creator, num_envs=256, backend=pufferlib.vector.Multiprocessing)

# Method 2: Same pattern with an inline creator
env = pufferlib.vector.make(
    lambda: pufferlib.emulation.GymnasiumPufferEnv(
        env_creator=lambda: gym.make('CartPole-v1')),
    num_envs=256, backend=pufferlib.vector.Multiprocessing,
)

# Method 3: Custom Gymnasium environment
class MyGymEnv(gym.Env):
    def __init__(self):
        self.observation_space = gym.spaces.Box(low=-1, high=1, shape=(4,))
        self.action_space = gym.spaces.Discrete(2)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        return self.observation_space.sample(), {}

    def step(self, action):
        obs = self.observation_space.sample()
        reward = 1.0
        terminated = False
        truncated = False
        info = {}
        return obs, reward, terminated, truncated, info

# Wrap custom environment (MyGymEnv is a gym.Env, so emulate it)
env = pufferlib.vector.make(
    lambda: pufferlib.emulation.GymnasiumPufferEnv(env_creator=MyGymEnv),
    num_envs=128, backend=pufferlib.vector.Multiprocessing,
)
```

### Atari Environments

The simplest path is PufferLib's bundled Atari binding, which handles the standard
preprocessing for you:

```python
import pufferlib.environments.atari as atari
import pufferlib.vector

# The binding takes an ALE ROM name (e.g. 'breakout', 'pong') and returns an
# already-emulated env, so still pass a non-native backend.
env = pufferlib.vector.make(
    atari.env_creator('breakout'),
    num_envs=256, backend=pufferlib.vector.Multiprocessing)
```

You can also build the Gymnasium env yourself and emulate it:

```python
import functools
import gymnasium as gym
from gymnasium.wrappers import AtariPreprocessing, FrameStack
import pufferlib.emulation
import pufferlib.vector

def make_atari_env(env_name='ALE/Pong-v5'):
    env = gym.make(env_name)
    env = AtariPreprocessing(env, frame_skip=4)
    env = FrameStack(env, num_stack=4)
    return env

def atari_creator():
    return pufferlib.emulation.GymnasiumPufferEnv(env_creator=make_atari_env)

env = pufferlib.vector.make(
    atari_creator, num_envs=256, backend=pufferlib.vector.Multiprocessing)
```

### Complex Observation Spaces

```python
import numpy as np
import gymnasium as gym
from gymnasium.spaces import Dict, Box, Discrete
import pufferlib.emulation
import pufferlib.vector

class ComplexObsEnv(gym.Env):
    def __init__(self):
        # Dict observation space
        self.observation_space = Dict({
            'image': Box(low=0, high=255, shape=(84, 84, 3), dtype=np.uint8),
            'vector': Box(low=-np.inf, high=np.inf, shape=(10,), dtype=np.float32),
            'discrete': Discrete(5)
        })
        self.action_space = Discrete(4)

    def reset(self, seed=None, options=None):
        return {
            'image': np.zeros((84, 84, 3), dtype=np.uint8),
            'vector': np.zeros(10, dtype=np.float32),
            'discrete': 0
        }, {}

    def step(self, action):
        obs = {
            'image': np.random.randint(0, 256, (84, 84, 3), dtype=np.uint8),
            'vector': np.random.randn(10).astype(np.float32),
            'discrete': np.random.randint(0, 5)
        }
        return obs, 1.0, False, False, {}

# GymnasiumPufferEnv flattens Dict spaces to a Box for the trainer; recover the
# structure in the policy via pufferlib.pytorch.nativize_tensor (see policies.md).
env = pufferlib.vector.make(
    lambda: pufferlib.emulation.GymnasiumPufferEnv(env_creator=ComplexObsEnv),
    num_envs=128, backend=pufferlib.vector.Multiprocessing,
)
```

## PettingZoo Integration

### Parallel Environments

```python
from pettingzoo.butterfly import pistonball_v6
import pufferlib.emulation
import pufferlib.vector

# Multi-agent envs are wrapped with PettingZooPufferEnv, then vectorized.
# PufferLib has no string registry -- pass the constructor (callable).
def pistonball_creator():
    return pufferlib.emulation.PettingZooPufferEnv(
        env_creator=lambda: pistonball_v6.parallel_env())

env = pufferlib.vector.make(
    pistonball_creator, num_envs=128, backend=pufferlib.vector.Multiprocessing)
```

### AEC (Agent Environment Cycle) Environments

```python
from pettingzoo.classic import chess_v5
from pettingzoo.utils import aec_to_parallel
import pufferlib.emulation
import pufferlib.vector

# Convert AEC to a parallel env, wrap with PettingZooPufferEnv, then vectorize.
# PufferLib has no string registry -- pass the constructor (callable).
def chess_creator():
    return pufferlib.emulation.PettingZooPufferEnv(
        env_creator=lambda: aec_to_parallel(chess_v5.env()))

env = pufferlib.vector.make(
    chess_creator, num_envs=64, backend=pufferlib.vector.Multiprocessing)
```

### Multi-Agent Training

```python
import pufferlib.emulation
import pufferlib.vector
from pufferlib.pufferl import PuffeRL, load_config

# Create multi-agent environment. `kaz_creator` is a placeholder that wraps a
# PettingZoo env (e.g. knights_archers_zombies) with PettingZooPufferEnv.
env = pufferlib.vector.make(
    kaz_creator, num_envs=128, backend=pufferlib.vector.Multiprocessing)

# One shared policy serves all agents. PufferLib emulates PettingZoo as a single
# flat agent axis, so build the policy from the PER-AGENT spaces.
policy = create_policy(env.single_observation_space, env.single_action_space)

# Train: PuffeRL(config_dict, vecenv, policy). Loop on global_step.
args = load_config('puffer_breakout')          # or your own env config
config = {**args['train'], 'env': 'multiagent'}
trainer = PuffeRL(config, env, policy)

while trainer.global_step < config['total_timesteps']:
    trainer.evaluate()   # rollouts are batched arrays, not {agent_id: ...} dicts
    trainer.train()
    trainer.mean_and_log()
```

## Third-Party Environments

PufferLib ships bindings for these suites under `pufferlib.environments.<name>`,
each exposing an `env_creator(name, ...)` (install the underlying package first).
They are emulated, so pass `backend=pufferlib.vector.Multiprocessing`. The
`make_*` names in the GPUDrive/MicroRTS/Griddly snippets below are placeholders
for whichever creator you obtain (binding `env_creator` or your own callable).

### Procgen

```python
import pufferlib.environments.procgen as procgen
import pufferlib.vector

env = pufferlib.vector.make(
    procgen.env_creator('coinrun'),
    num_envs=256, backend=pufferlib.vector.Multiprocessing)
```

### NetHack / MiniHack

```python
import pufferlib.environments.nethack as nethack
import pufferlib.vector

env = pufferlib.vector.make(
    nethack.env_creator('nethack'),
    num_envs=128, backend=pufferlib.vector.Multiprocessing)
```

### Minigrid

```python
import pufferlib.environments.minigrid as minigrid
import pufferlib.vector

env = pufferlib.vector.make(
    minigrid.env_creator('MiniGrid-Empty-8x8-v0'),
    num_envs=256, backend=pufferlib.vector.Multiprocessing)
```

### Neural MMO

```python
import functools
import pufferlib.vector

# Large-scale multi-agent environment.
# Pass a constructor callable -- there is no string registry. `make_neuralmmo`
# is a placeholder for the env creator you provide; bind kwargs with partial.
env = pufferlib.vector.make(
    functools.partial(
        make_neuralmmo,
        num_agents=128,  # Agents per environment
        map_size=128,
    ),
    num_envs=64,
)
```

### Crafter

```python
import pufferlib.vector

# Open-ended crafting environment.
# Pass a constructor callable -- there is no string registry. `make_crafter`
# is a placeholder for the env creator you provide.
env = pufferlib.vector.make(make_crafter, num_envs=128)
```

### GPUDrive

```python
import functools
import pufferlib.vector

# GPU-accelerated driving simulator.
# Pass a constructor callable -- there is no string registry. `make_gpudrive`
# is a placeholder for the env creator you provide; bind kwargs with partial.
env = pufferlib.vector.make(
    functools.partial(make_gpudrive, num_vehicles=8),
    num_envs=1024,  # Can handle many environments on GPU
)
```

### MicroRTS

```python
import functools
import pufferlib.vector

# Real-time strategy game.
# Pass a constructor callable -- there is no string registry. `make_microrts`
# is a placeholder for the env creator you provide; bind kwargs with partial.
env = pufferlib.vector.make(
    functools.partial(make_microrts, map_size=16, max_steps=2000),
    num_envs=128,
)
```

### Griddly

```python
import pufferlib.vector

# Grid-based games.
# Pass a constructor callable -- there is no string registry. make_griddly_*
# are placeholders for the env creators you provide.
env = pufferlib.vector.make(make_griddly_clusters, num_envs=256)
env = pufferlib.vector.make(make_griddly_sokoban, num_envs=256)
```

## Custom Wrappers

There is **no `pufferlib.Wrapper`** base class. For emulated envs, wrap at the
**Gymnasium** level (subclass `gymnasium.Wrapper`) *before* passing the env to
`GymnasiumPufferEnv` — that way you keep the standard Gymnasium 5-tuple step
`(obs, reward, terminated, truncated, info)` and PufferLib handles the rest.
PufferLib also ships ready wrappers (`pufferlib.ResizeObservation`,
`pufferlib.ClipAction`, `pufferlib.EpisodeStats`). For frame stacking / action
repeat, prefer the standard `gymnasium.wrappers` (e.g. `FrameStack`).

```python
import numpy as np
import gymnasium as gym
import pufferlib.emulation
import pufferlib.vector

class RewardShaping(gym.Wrapper):
    """Add a shaped reward at the Gymnasium level."""

    def __init__(self, env, shaping_fn):
        super().__init__(env)
        self.shaping_fn = shaping_fn

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        reward = reward + self.shaping_fn(obs, action)
        return obs, reward, terminated, truncated, info

def proximity_shaping(obs, action):
    goal_pos = np.array([10, 10])
    distance = np.linalg.norm(goal_pos - obs[:2])
    return -0.1 * distance

# Apply wrappers inside the creator, then emulate + vectorize.
def shaped_creator():
    base = gym.make('CartPole-v1')
    base = RewardShaping(base, proximity_shaping)
    return pufferlib.emulation.GymnasiumPufferEnv(env_creator=lambda: base)

env = pufferlib.vector.make(
    shaped_creator, num_envs=128, backend=pufferlib.vector.Multiprocessing)
```

## Space Conversion

### Flattening Spaces

PufferLib automatically flattens complex observation/action spaces:

```python
from gymnasium.spaces import Dict, Box, Discrete
import pufferlib

# Complex space
original_space = Dict({
    'image': Box(0, 255, (84, 84, 3), dtype=np.uint8),
    'vector': Box(-np.inf, np.inf, (10,), dtype=np.float32),
    'discrete': Discrete(5)
})

# Automatically flattened by PufferLib
# Observations are presented as flat arrays for efficient processing
# But can be unflattened when needed for policy processing
```

### Recovering structure in the policy

There is no `unflatten_observations` helper. Use
`pufferlib.pytorch.nativize_dtype` (once, from `env.emulated`) plus
`pufferlib.pytorch.nativize_tensor` per batch to recover the structured dict:

```python
import pufferlib.pytorch

class PolicyWithDictObs(nn.Module):
    def __init__(self, env):
        super().__init__()
        self.dtype = pufferlib.pytorch.nativize_dtype(env.emulated)
        # ... encoders / heads ...

    def encode_observations(self, flat_observations, state=None):
        obs = pufferlib.pytorch.nativize_tensor(flat_observations, self.dtype)
        image_features = self.image_encoder(obs['image'].float() / 255.0)
        vector_features = self.vector_encoder(obs['vector'])
        # ...
```

## Environment Lookup

### Mapping Names to Constructors

PufferLib has no string registry and no `pufferlib.register`/`pufferlib.make`.
If you want name-based lookup, keep your own mapping of names to environment
constructors (callables) and pass the resolved constructor to
`pufferlib.vector.make`:

```python
import functools
import pufferlib.vector
from my_package.envs import MyEnvironment

# Your own registry: name -> constructor (callable)
ENV_REGISTRY = {
    'my-custom-env': functools.partial(MyEnvironment, param1='value1'),
}

# Resolve the name to a constructor, then vectorize
env_creator = ENV_REGISTRY['my-custom-env']
env = pufferlib.vector.make(env_creator, num_envs=256)
```

### Sharing Constructors

To make an environment easy for others to use, simply expose its constructor
(a `PufferEnv` subclass, or a function/`functools.partial` that returns one)
from your package and document the kwargs:

```python
# In my_package/envs.py
def make_my_env(default_param='default_value'):
    return MyEnvironment(param1=default_param)
```

## Compatibility Patterns

### Gymnasium to PufferLib

```python
import gymnasium as gym
import pufferlib.emulation
import pufferlib.vector

# Standard Gymnasium environment
class GymEnv(gym.Env):
    def reset(self, seed=None, options=None):
        return observation, info

    def step(self, action):
        return observation, reward, terminated, truncated, info

# Wrap with GymnasiumPufferEnv, then vectorize (pass a constructor callable)
env = pufferlib.vector.make(
    lambda: pufferlib.emulation.GymnasiumPufferEnv(env_creator=GymEnv),
    num_envs=128,
)
```

### PettingZoo to PufferLib

```python
from pettingzoo import ParallelEnv
import pufferlib.emulation
import pufferlib.vector

# PettingZoo parallel environment
class PZEnv(ParallelEnv):
    def reset(self, seed=None, options=None):
        return {agent: obs for agent, obs in ...}, {agent: info for agent in ...}

    def step(self, actions):
        return observations, rewards, terminations, truncations, infos

# Wrap with PettingZooPufferEnv, then vectorize (pass a constructor callable)
env = pufferlib.vector.make(
    lambda: pufferlib.emulation.PettingZooPufferEnv(env_creator=PZEnv),
    num_envs=128,
)
```

### Legacy Gym (v0.21) to PufferLib

```python
import gym  # Old gym
import pufferlib.emulation
import pufferlib.vector

# Legacy gym environment (returns done instead of terminated/truncated)
class LegacyEnv(gym.Env):
    def reset(self):
        return observation

    def step(self, action):
        return observation, reward, done, info

# Wrap with GymnasiumPufferEnv, then vectorize (pass a constructor callable)
env = pufferlib.vector.make(
    lambda: pufferlib.emulation.GymnasiumPufferEnv(env_creator=LegacyEnv),
    num_envs=128,
)
```

## Performance Considerations

### Efficient Integration

```python
import gymnasium as gym
import pufferlib.emulation
import pufferlib.vector

# Fast: a native PufferEnv constructor (no emulation layer).
# `make_coinrun` is a placeholder for your PufferEnv creator.
env = pufferlib.vector.make(make_coinrun, num_envs=256)

# Slower: Generic Gymnasium wrapper (emulated -> needs a non-native backend)
env = pufferlib.vector.make(
    lambda: pufferlib.emulation.GymnasiumPufferEnv(
        env_creator=lambda: gym.make('CartPole-v1')),
    num_envs=256, backend=pufferlib.vector.Multiprocessing,
)

# Slowest: Nested wrappers add overhead
def nested_creator():
    gym_env = gym.make('CartPole-v1')
    gym_env = SomeWrapper(gym_env)
    gym_env = AnotherWrapper(gym_env)
    return pufferlib.emulation.GymnasiumPufferEnv(env_creator=lambda: gym_env)

env = pufferlib.vector.make(
    nested_creator, num_envs=256, backend=pufferlib.vector.Multiprocessing)
```

### Minimize Wrapper Overhead

```python
import pufferlib.emulation
import pufferlib.vector

# BAD: Too many wrappers
def bad_creator():
    env = gym.make('CartPole-v1')
    env = Wrapper1(env)
    env = Wrapper2(env)
    env = Wrapper3(env)
    return pufferlib.emulation.GymnasiumPufferEnv(env_creator=lambda: env)

env = pufferlib.vector.make(
    bad_creator, num_envs=256, backend=pufferlib.vector.Multiprocessing)

# GOOD: Combine wrapper logic
class CombinedWrapper(gym.Wrapper):
    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        # Apply all transformations at once
        obs = self._transform_obs(obs)
        reward = self._transform_reward(reward)
        return obs, reward, terminated, truncated, info

def good_creator():
    env = CombinedWrapper(gym.make('CartPole-v1'))
    return pufferlib.emulation.GymnasiumPufferEnv(env_creator=lambda: env)

env = pufferlib.vector.make(
    good_creator, num_envs=256, backend=pufferlib.vector.Multiprocessing)
```

## Debugging Integration

### Verify Environment Compatibility

```python
import numpy as np

def test_environment(env, num_steps=100):
    """Smoke-test a single PufferEnv before vectorizing (5-tuple native API)."""
    obs, info = env.reset()
    assert isinstance(info, list), "PufferEnv reset must return an info LIST"

    for _ in range(num_steps):
        # One action per agent.
        action = np.array([env.single_action_space.sample()
                           for _ in range(env.num_agents)])
        obs, reward, terminal, truncation, info = env.step(action)

        assert np.all(np.isfinite(np.asarray(reward, dtype=float))), "Non-finite reward"
        assert isinstance(info, list), "info must be a list of dicts"

        if np.any(terminal) or np.any(truncation):
            obs, info = env.reset()

    print("Environment passed compatibility test")

# Test before vectorizing
test_environment(MyEnvironment())
```

### Compare Outputs

```python
# Verify PufferLib emulation matches original
import gymnasium as gym
import pufferlib.emulation
import pufferlib.vector
import numpy as np

gym_env = gym.make('CartPole-v1')
puffer_env = pufferlib.vector.make(
    lambda: pufferlib.emulation.GymnasiumPufferEnv(
        env_creator=lambda: gym.make('CartPole-v1')),
    num_envs=1, backend=pufferlib.vector.Multiprocessing,
)

# Both reset() calls return (obs, info). vecenv.step returns a 5-tuple:
# (obs, rewards, terminals, truncations, infos).
gym_env.reset(seed=42)
puffer_obs, _ = puffer_env.reset(seed=42)

for _ in range(100):
    action = gym_env.action_space.sample()

    gym_obs, gym_reward, gym_term, gym_trunc, gym_info = gym_env.step(action)
    puffer_obs, puffer_reward, puffer_term, puffer_trunc, *_ = \
        puffer_env.step(np.array([action]))

    # Compare outputs (accounting for the leading batch/agent dimension)
    assert np.allclose(gym_obs, puffer_obs[0])
    assert gym_reward == puffer_reward[0]
```
