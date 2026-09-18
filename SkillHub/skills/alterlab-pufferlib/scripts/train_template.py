#!/usr/bin/env python3
"""
PufferLib Training Template (targets PufferLib 3.0.x)

This template provides a complete training script for reinforcement learning
with PufferLib. Customize the environment, policy, and training configuration
as needed for your use case.

Key 3.0 API facts this template respects:
- pufferlib.vector.make(env_creator, num_envs=..., backend=...). The default
  backend is PufferEnv (native vectorization); wrapped Gymnasium/PettingZoo
  envs require backend=pufferlib.vector.Multiprocessing (or Serial).
- PuffeRL(config, vecenv, policy, logger=None) -- the first arg is a config
  DICT (not flat kwargs), the env arg is the vecenv, and the loop is driven by
  trainer.global_step < config['total_timesteps'].
- Loggers (WandbLogger/NeptuneLogger/NoLogger) live in pufferlib.pufferl and
  take the nested args config dict, not project=/name= kwargs.
"""

import argparse
import numpy as np
import torch
import torch.nn as nn
import pufferlib
import pufferlib.vector
from pufferlib.pufferl import PuffeRL, NoLogger, WandbLogger, NeptuneLogger
from pufferlib.pytorch import layer_init


class Policy(nn.Module):
    """Example policy network for a flat-vector, discrete-action env.

    PufferLib does not enforce a base class, but PuffeRL calls
    `policy.forward_eval(obs, state)` and expects it to return (logits, values).
    Structuring the network as encode_observations + decode_actions (as below)
    lets you wrap it with pufferlib.models.LSTMWrapper later without rewrites.
    The constructor takes the (driver) env so it can read single_observation_space
    / single_action_space, mirroring pufferlib.models.Default.
    """

    def __init__(self, env, hidden_size=256):
        super().__init__()
        self.hidden_size = hidden_size

        obs_dim = int(np.prod(env.single_observation_space.shape))
        num_actions = env.single_action_space.n

        self.encoder = nn.Sequential(
            layer_init(nn.Linear(obs_dim, hidden_size)),
            nn.ReLU(),
            layer_init(nn.Linear(hidden_size, hidden_size)),
            nn.ReLU(),
        )
        self.actor = layer_init(nn.Linear(hidden_size, num_actions), std=0.01)
        self.critic = layer_init(nn.Linear(hidden_size, 1), std=1.0)

    def encode_observations(self, observations, state=None):
        return self.encoder(observations.float())

    def decode_actions(self, hidden):
        return self.actor(hidden), self.critic(hidden)

    def forward_eval(self, observations, state=None):
        hidden = self.encode_observations(observations, state)
        return self.decode_actions(hidden)

    def forward(self, observations, state=None):
        return self.forward_eval(observations, state)


def resolve_env_creator(env_name):
    """Map a CLI env name to an environment constructor (callable).

    PufferLib has no string registry, so you maintain this mapping yourself.
    Replace the body with your own lookup, e.g.:

        from pufferlib.ocean import Breakout, Snake
        registry = {
            'breakout': Breakout,
            'snake': functools.partial(Snake, num_agents=4),
        }
        return registry[env_name]
    """
    raise NotImplementedError(
        f"Define a constructor for {env_name!r} (see resolve_env_creator).")


def make_env():
    """Create vectorized environment. Customize this for your task.

    PufferLib has no string registry -- pass an environment constructor
    (callable) to `pufferlib.vector.make`.
    """
    # Option 1: A PufferEnv constructor (e.g. an Ocean environment).
    #   `env_creator` is a placeholder: replace it with the callable that
    #   constructs your environment, e.g. `from pufferlib.ocean import ...`.
    env_creator = None  # TODO: replace with your environment constructor (callable)
    return pufferlib.vector.make(env_creator, num_envs=256)

    # Option 2: A Gymnasium environment wrapped for PufferLib. Wrapped (non-native)
    # envs require an explicit backend -- the default backend=PufferEnv is native-only.
    # import gymnasium as gym
    # import pufferlib.emulation
    # gym_creator = lambda: pufferlib.emulation.GymnasiumPufferEnv(
    #     env_creator=lambda: gym.make('CartPole-v1'))
    # return pufferlib.vector.make(
    #     gym_creator, num_envs=256, backend=pufferlib.vector.Multiprocessing)

    # Option 3: A custom PufferEnv.
    # from my_envs import MyEnvironment
    # return pufferlib.vector.make(MyEnvironment, num_envs=256)


def create_policy(env):
    """Create policy network. PufferLib policies read single_*_space off the env."""
    return Policy(env, hidden_size=256)


def train(args):
    """Main training function."""
    # Set random seeds
    torch.manual_seed(args.seed)

    # Create environment.
    # PufferLib has no string registry -- pass an environment constructor
    # (callable) to `pufferlib.vector.make`. Resolve the CLI name to a
    # constructor here; `resolve_env_creator` is a placeholder you implement
    # (e.g. a dict mapping names to PufferEnv classes / functools.partial).
    print(f"Creating environment with {args.num_envs} parallel environments...")
    env_creator = resolve_env_creator(args.env_name)
    env = pufferlib.vector.make(
        env_creator,
        num_envs=args.num_envs,
        num_workers=args.num_workers
    )

    # Create policy
    print("Initializing policy...")
    policy = create_policy(env)

    if args.device == 'cuda' and torch.cuda.is_available():
        policy = policy.cuda()
        print(f"Using GPU: {torch.cuda.get_device_name(0)}")
    else:
        args.device = 'cpu'
        print("Using CPU")

    # Build the config DICT PuffeRL expects. In real use, prefer
    # `args = pufferlib.pufferl.load_config(env_name)` and pass `args['train']`
    # so every required key is filled from pufferlib/config/*.ini. Here we set
    # the keys this template exposes explicitly.
    config = {
        'env': args.env_name,
        'seed': args.seed,
        'torch_deterministic': True,
        'cpu_offload': False,
        'device': args.device,
        'total_timesteps': args.total_timesteps,
        'learning_rate': args.learning_rate,
        'anneal_lr': True,
        'min_lr_ratio': 0.0,
        'gamma': args.gamma,
        'gae_lambda': args.gae_lambda,
        'update_epochs': args.update_epochs,
        'clip_coef': args.clip_coef,
        'ent_coef': args.ent_coef,
        'vf_coef': args.vf_coef,
        'vf_clip_coef': 0.2,
        'max_grad_norm': args.max_grad_norm,
        'batch_size': args.batch_size,
        'minibatch_size': args.minibatch_size,
        'max_minibatch_size': args.minibatch_size,
        'bptt_horizon': args.bptt_horizon,
        'compile': args.compile,
        'use_rnn': False,
        'data_dir': args.checkpoint_dir,
        'checkpoint_interval': args.checkpoint_interval,
    }

    # Logger. The 3.0 loggers read keys from a config dict; the simplest path is
    # NoLogger. Populate wandb_*/neptune_* keys in `config` if you wire those up.
    if args.logger == 'wandb':
        logger = WandbLogger(config)
    elif args.logger == 'neptune':
        logger = NeptuneLogger(config)
    else:
        logger = NoLogger(config)

    # Create trainer: positional (config, vecenv, policy, logger).
    print("Creating trainer...")
    trainer = PuffeRL(config, env, policy, logger)

    # Training loop is driven by global_step, not a fixed iteration count.
    print(f"Training to {config['total_timesteps']:,} timesteps...")
    while trainer.global_step < config['total_timesteps']:
        trainer.evaluate()      # Collect rollouts
        trainer.train()         # Train on batch
        trainer.mean_and_log()  # Aggregate + log (PuffeRL also auto-checkpoints
                                # every config['checkpoint_interval'] epochs)

    print("Training complete!")

    # Final checkpoint (save_checkpoint takes no path; it writes under data_dir).
    final_path = trainer.save_checkpoint()
    print(f"Saved final model to {final_path}")


def main():
    parser = argparse.ArgumentParser(description='PufferLib Training')

    # Environment
    parser.add_argument('--env-name', type=str, default='my-env',
                        help='Env key resolved to a constructor by '
                             'resolve_env_creator (PufferLib has no string registry)')
    parser.add_argument('--num-envs', type=int, default=256,
                        help='Number of parallel environments')
    parser.add_argument('--num-workers', type=int, default=8,
                        help='Number of vectorization workers')

    # Training (defaults mirror pufferlib/config/default.ini, 3.0.x)
    parser.add_argument('--total-timesteps', type=int, default=10_000_000,
                        help='Total environment steps to train for')
    parser.add_argument('--learning-rate', type=float, default=0.015,
                        help='Learning rate (PufferLib default optimizer is muon)')
    parser.add_argument('--batch-size', type=int, default=32768,
                        help='Timesteps per training batch')
    parser.add_argument('--minibatch-size', type=int, default=8192,
                        help='Minibatch size (also used as max for grad accumulation)')
    parser.add_argument('--bptt-horizon', type=int, default=64,
                        help='BPTT / rollout horizon per segment')
    parser.add_argument('--update-epochs', type=int, default=1,
                        help='Training epochs per batch')
    parser.add_argument('--device', type=str, default='cuda',
                        choices=['cuda', 'cpu'], help='Device to use')

    # PPO Parameters
    parser.add_argument('--gamma', type=float, default=0.995,
                        help='Discount factor')
    parser.add_argument('--gae-lambda', type=float, default=0.90,
                        help='GAE lambda')
    parser.add_argument('--clip-coef', type=float, default=0.2,
                        help='PPO clipping coefficient')
    parser.add_argument('--ent-coef', type=float, default=0.001,
                        help='Entropy coefficient')
    parser.add_argument('--vf-coef', type=float, default=2.0,
                        help='Value function coefficient')
    parser.add_argument('--max-grad-norm', type=float, default=1.5,
                        help='Maximum gradient norm')

    # Logging
    parser.add_argument('--logger', type=str, default='none',
                        choices=['wandb', 'neptune', 'none'],
                        help='Logger to use (set wandb_*/neptune_* config keys to wire up)')

    # Checkpointing (PuffeRL auto-saves under data_dir every checkpoint_interval epochs)
    parser.add_argument('--checkpoint-dir', type=str, default='experiments',
                        help='data_dir where checkpoints are written')
    parser.add_argument('--checkpoint-interval', type=int, default=200,
                        help='Checkpoint save frequency (epochs)')

    # Misc
    parser.add_argument('--seed', type=int, default=42,
                        help='Random seed')
    parser.add_argument('--compile', action='store_true',
                        help='Use torch.compile for faster training')

    args = parser.parse_args()

    # Create checkpoint directory
    import os
    os.makedirs(args.checkpoint_dir, exist_ok=True)

    # Run training
    train(args)


if __name__ == '__main__':
    main()
