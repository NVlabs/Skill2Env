# PufferLib Training Guide

> Targets PufferLib **3.0.x**. The trainer is config-driven: `PuffeRL.__init__(self, config, vecenv, policy, logger=None)` where `config` is a **dict** (typically `args['train']` from `load_config`), not flat keyword args. The dev `4.0` branch differs.

## Overview

PuffeRL is PufferLib's high-performance training algorithm based on CleanRL's PPO with optional LSTMs, enhanced with research improvements. It achieves high training throughput through optimized vectorization and an efficient implementation.

## Training Workflow

### Basic Training Loop

The PuffeRL trainer provides three core methods:

```python
# Collect environment interactions
rollout_data = trainer.evaluate()

# Train on collected batch
train_metrics = trainer.train()

# Aggregate and log results
trainer.mean_and_log()
```

### CLI Training

Quick start via the `puffer` CLI. `env_name` resolves to a config section in `pufferlib/config/*.ini` plus its registered Ocean env. Config keys are overridden with `--<section>.<key>`:

```bash
# Basic training (Ocean Breakout)
puffer train puffer_breakout --train.device cuda

# Override config keys (note real key names: learning-rate, total-timesteps)
puffer train puffer_breakout \
    --train.device cuda \
    --train.learning-rate 0.015 \
    --train.total-timesteps 10_000_000 \
    --vec.num-envs 256
```

### Python Training Script

The supported high-level entry point is `pufferl.train(env_name, ...)`, which builds the vecenv, policy, logger, and config for you:

```python
import pufferlib.pufferl as pufferl

pufferl.train('puffer_breakout')                  # all defaults from config/*.ini
pufferl.train('puffer_breakout', vecenv=my_vec, policy=my_policy)  # override pieces
```

To drive the trainer manually, build the config dict yourself:

```python
import pufferlib.vector
from pufferlib.pufferl import PuffeRL, load_config

# Native PufferEnv -> default backend=PufferEnv. Wrapped (Gymnasium/PettingZoo)
# envs require backend=pufferlib.vector.Multiprocessing (or Serial).
vecenv = pufferlib.vector.make(env_creator, num_envs=256)

# load_config returns a nested args dict; PuffeRL takes the 'train' section (a dict).
args = load_config('puffer_breakout')
config = {**args['train'], 'env': 'puffer_breakout'}
config['device'] = 'cuda'

trainer = PuffeRL(config, vecenv, my_policy)  # (config, vecenv, policy, logger=None)

# Training loop is driven by global_step, not a fixed iteration count.
while trainer.global_step < config['total_timesteps']:
    trainer.evaluate()      # Collect rollouts
    trainer.train()         # Train on batch
    trainer.mean_and_log()  # Aggregate + log
```

## Key Training Parameters

Keys and defaults below are from `pufferlib/config/default.ini` (3.0.x); per-env `.ini` files override them. Use the exact key names — they differ from generic CleanRL/PPO conventions (e.g. `update_epochs`, not `n_epochs`; `minibatch_size`/`bptt_horizon`, not a single `num_steps`).

### Core Hyperparameters (`[train]`)

- **learning_rate**: Optimizer LR (default: `0.015`; note PufferLib's default `optimizer = muon`)
- **batch_size**: Timesteps per training batch (default: `auto`, derived from `bptt_horizon` x agents)
- **minibatch_size**: Minibatch size (default: `8192`)
- **max_minibatch_size**: Gradient accumulation above this size (default: `32768`)
- **bptt_horizon**: BPTT / rollout horizon per segment (default: `64`)
- **update_epochs**: Training epochs per batch (default: `1`)
- **total_timesteps**: Total env steps to train for (default: `10_000_000`)

### Vectorization (`[vec]`)

- **num_envs**: Parallel environments (default: `2`)
- **num_workers**: Vectorization workers (default: `auto`)
- **backend**: `Multiprocessing` (CLI default) / `Serial` / `Ray` / `PufferEnv` (native)

### PPO Parameters (`[train]`)

- **gamma**: Discount factor (default: `0.995`)
- **gae_lambda**: GAE lambda (default: `0.90`)
- **clip_coef**: PPO clipping coefficient (default: `0.2`)
- **ent_coef**: Entropy coefficient (default: `0.001`)
- **vf_coef**: Value loss coefficient (default: `2.0`)
- **vf_clip_coef**: Value clipping coefficient (default: `0.2`)
- **max_grad_norm**: Max gradient norm (default: `1.5`)

### Performance Parameters (`[train]`)

- **device**: Computing device (`cuda` / `cpu`, default `cuda`)
- **compile**: Use torch.compile (default: `False`; `compile_mode = max-autotune-no-cudagraphs`)
- **cpu_offload**: Keep observations on CPU to save GPU memory (default: `False`)

## Distributed Training

### Multi-GPU Training

Use torchrun for distributed training across multiple GPUs:

```bash
torchrun --nproc_per_node=4 train.py \
    --train.device cuda \
    --train.batch-size 131072
```

### Multi-Node Training

For distributed training across multiple nodes:

```bash
# On main node (rank 0)
torchrun --nproc_per_node=8 \
    --nnodes=4 \
    --node_rank=0 \
    --master_addr=MASTER_IP \
    --master_port=29500 \
    train.py

# On worker nodes (rank 1, 2, 3)
torchrun --nproc_per_node=8 \
    --nnodes=4 \
    --node_rank=NODE_RANK \
    --master_addr=MASTER_IP \
    --master_port=29500 \
    train.py
```

## Monitoring and Logging

### Logger Integration

Loggers live in `pufferlib.pufferl` (`WandbLogger`, `NeptuneLogger`, `NoLogger`), **not** the top-level package. Each takes the nested `args` config dict and reads keys from it (it does not take `project=`/`name=` kwargs).

The intended path is to let `pufferl.train` pick the logger from config flags:

```bash
# Weights & Biases: set --wandb plus the wandb_project / wandb_group keys
puffer train puffer_breakout --train.wandb True --train.wandb-project my_project

# Neptune: set --neptune plus neptune_name / neptune_project
puffer train puffer_breakout --train.neptune True --train.neptune-project my_project
```

To construct one manually, pass the `args` dict (with the relevant keys populated):

```python
from pufferlib.pufferl import WandbLogger, NeptuneLogger, NoLogger

# args is the nested dict from load_config(); WandbLogger reads
# args['wandb_project'], args['wandb_group'], args['tag'], args['no_model_upload'].
logger = WandbLogger(args)          # or NeptuneLogger(args), or NoLogger(args)
trainer = PuffeRL(config, vecenv, policy, logger=logger)
```

### Key Metrics

Training logs include:

- **Performance Metrics**:
  - Steps per second (SPS)
  - Training throughput
  - Wall-clock time per iteration

- **Learning Metrics**:
  - Episode rewards (mean, min, max)
  - Episode lengths
  - Value function loss
  - Policy loss
  - Entropy
  - Explained variance
  - Clipfrac

- **Environment Metrics**:
  - Environment-specific rewards
  - Success rates
  - Custom metrics

### Terminal Dashboard

PufferLib provides a real-time terminal dashboard showing:
- Training progress
- Current SPS
- Episode statistics
- Loss values
- GPU utilization

## Checkpointing

Checkpointing is **auto-managed**: PuffeRL calls `save_checkpoint()` every `config['checkpoint_interval']` epochs and on completion. The method takes **no path argument** — it writes `model_*.pt` and `trainer_state.pt` under `config['data_dir']/<env>_<run_id>/`.

```python
# Manual save (no path arg). Returns the model path written.
model_path = trainer.save_checkpoint()
```

### Resuming / loading

There is no `trainer.load_checkpoint(path)`. Loading happens at policy-build time via config keys, then training resumes from the loaded weights:

```bash
# Resume from the most recent local checkpoint
puffer train puffer_breakout --train.load-model-path latest

# Or load a specific file / a logged W&B/Neptune run id
puffer train puffer_breakout --train.load-model-path experiments/puffer_breakout_000400.pt
```

## Hyperparameter Tuning with Protein

Protein is PufferLib's Pareto-genetic / GP sweep method (`pufferlib.sweep.Protein`). You do **not** instantiate it directly with a `search_space=` kwarg — sweeps are config-driven via the `[sweep]` section and run with `pufferl.sweep()`. Sweeps **require** a wandb or neptune logger.

In the config (`.ini`), `[sweep]` selects the method and metric, and `[sweep.<section>.<key>]` blocks declare the search space:

```ini
[sweep]
method = Protein
metric = score
goal = maximize

[sweep.train.learning_rate]
distribution = log_normal
min = 1e-4
max = 1e-2

[sweep.vec.num_envs]
distribution = uniform_pow2
min = 1
max = 16
```

Run it:

```bash
puffer sweep puffer_breakout --train.wandb True --train.wandb-project my_sweep
```

```python
import pufferlib.pufferl as pufferl
pufferl.sweep(env_name='puffer_breakout')   # args must enable wandb or neptune
```

## Performance Optimization Tips

### Maximizing Throughput

1. **Batch Size**: Increase batch_size to fully utilize GPU
2. **Num Envs**: Balance between CPU and GPU utilization
3. **Compile**: Enable torch.compile for 10-20% speedup
4. **Workers**: Adjust num_workers based on environment complexity
5. **Device**: Always use 'cuda' for neural network training

### Environment Speed

- Pure Python environments: ~100k-500k SPS
- C-based environments: ~4M SPS
- With training overhead: ~1M-4M total SPS

### Memory Management

- Reduce batch_size if running out of GPU memory
- Decrease num_envs if running out of CPU memory
- Use gradient accumulation for large effective batch sizes

## Common Training Patterns

### Curriculum Learning

```python
import functools
import pufferlib.vector

# Start with easy tasks, gradually increase difficulty.
# Bind constructor kwargs with functools.partial -- there is no string
# registry, so `MyEnv` here is your own PufferEnv class / creator callable.
difficulty_levels = [0.1, 0.3, 0.5, 0.7, 1.0]

for difficulty in difficulty_levels:
    env = pufferlib.vector.make(
        functools.partial(MyEnv, difficulty=difficulty), num_envs=256)
    trainer = PuffeRL(config, env, policy)  # (config dict, vecenv, policy)

    while trainer.global_step < steps_per_level:
        trainer.evaluate()
        trainer.train()
        trainer.mean_and_log()
```

### Reward Shaping

```python
# A PufferEnv step returns a 5-tuple (obs, rewards, terminals, truncations, info).
class RewardShapedEnv(pufferlib.PufferEnv):
    def step(self, actions):
        obs, rewards, terminals, truncations, info = super().step(actions)

        # Add shaped rewards
        rewards = rewards + 0.1 * proximity_bonus

        return obs, rewards, terminals, truncations, info
```

### Multi-Stage Training

`config` is the dict passed at construction; PuffeRL reads most values once at
init, so change a stage's learning rate by rebuilding the trainer with an
updated config (or use the built-in `anneal_lr` / `min_lr_ratio` config keys).

```python
stages = [
    {'learning_rate': 1e-3, 'steps': 1_000_000},   # Exploration
    {'learning_rate': 3e-4, 'steps': 5_000_000},   # Main training
    {'learning_rate': 1e-4, 'steps': 2_000_000},   # Fine-tuning
]

for stage in stages:
    config = {**config, 'learning_rate': stage['learning_rate']}
    trainer = PuffeRL(config, vecenv, policy)
    target = trainer.global_step + stage['steps']
    while trainer.global_step < target:
        trainer.evaluate()
        trainer.train()
        trainer.mean_and_log()
```

## Troubleshooting

### Low Performance

- Check environment is vectorized correctly
- Verify GPU utilization with `nvidia-smi`
- Increase batch_size to saturate GPU
- Enable compile mode
- Profile with `torch.profiler`

### Training Instability

- Reduce learning_rate
- Decrease batch_size
- Increase num_envs for more diverse samples
- Add entropy coefficient for more exploration
- Check reward scaling

### Memory Issues

- Reduce batch_size or num_envs
- Use gradient accumulation
- Disable compile mode if causing OOM
- Check for memory leaks in custom environments
