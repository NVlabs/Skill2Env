#!/usr/bin/env python3
"""
TDC Benchmark Group Evaluation Template

This script demonstrates how to use TDC benchmark groups for systematic
model evaluation following the required 5-seed protocol.

Usage:
    python benchmark_evaluation.py
"""

from tdc.benchmark_group import admet_group
from tdc import Evaluator
import numpy as np
import pandas as pd


def load_benchmark_group():
    """
    Load the ADMET benchmark group
    """
    print("=" * 60)
    print("Loading ADMET Benchmark Group")
    print("=" * 60)

    # Initialize benchmark group
    group = admet_group(path='data/')

    # List available benchmarks (attribute name differs by TDC version;
    # fall back gracefully if it is not exposed).
    benchmark_names = getattr(group, "dataset_names", None)
    if benchmark_names:
        print("\nAvailable benchmarks in ADMET group:")
        print(f"Total: {len(benchmark_names)} datasets")
        for i, name in enumerate(benchmark_names[:10], 1):
            print(f"  {i}. {name}")
        if len(benchmark_names) > 10:
            print(f"  ... and {len(benchmark_names) - 10} more")

    return group


def single_dataset_evaluation(group, dataset_name='Caco2_Wang'):
    """
    Example: Evaluate on a single dataset with 5-seed protocol
    """
    print("\n" + "=" * 60)
    print(f"Example 1: Single Dataset Evaluation ({dataset_name})")
    print("=" * 60)

    # group.get(name) returns {'name', 'train_val', 'test'} — NOT indexed by seed.
    # The fixed test set is shared across seeds; only the train/valid partition varies.
    benchmark = group.get(dataset_name)
    name = benchmark['name']
    test = benchmark['test']
    print(f"\nBenchmark structure: keys = {list(benchmark.keys())}")
    print(f"  Fixed test size: {len(test)}")

    # Required: evaluate with 5 different seeds, one predictions dict per seed.
    predictions_list = []

    for seed in [1, 2, 3, 4, 5]:
        print(f"\n--- Seed {seed} ---")

        # Per-seed train/valid partition of train_val
        train, valid = group.get_train_valid_split(
            benchmark=name, split_type='default', seed=seed
        )
        print(f"Train size: {len(train)}  Valid size: {len(valid)}")

        # TODO: Replace with your model training
        # model = YourModel(random_state=seed)
        # model.fit(train['Drug'], train['Y'])
        # y_pred = model.predict(test['Drug'])

        # For demonstration, create dummy predictions on the fixed test set
        y_true = test['Y'].values
        np.random.seed(seed)
        y_pred = y_true + np.random.normal(0, 0.3, len(y_true))

        # Predictions dict is keyed by the benchmark name
        predictions_list.append({name: y_pred})

        # Quick per-seed sanity metric
        evaluator = Evaluator(name='MAE')
        print(f"MAE for seed {seed}: {evaluator(y_true, y_pred):.4f}")

    # Aggregate mean/std across the 5 seeds
    print("\n--- Overall Evaluation ---")
    results = group.evaluate_many(predictions_list)

    # evaluate_many lowercases the benchmark name in its keys
    key = name.lower()
    mean_score, std_score = results[key]
    print(f"\nResults for {dataset_name}:")
    print(f"  Mean MAE: {mean_score:.4f}")
    print(f"  Std MAE: {std_score:.4f}")

    return predictions_list, results


def multiple_datasets_evaluation(group):
    """
    Example: Evaluate on multiple datasets
    """
    print("\n" + "=" * 60)
    print("Example 2: Multiple Datasets Evaluation")
    print("=" * 60)

    # Select a subset of datasets for demonstration
    selected_datasets = ['Caco2_Wang', 'HIA_Hou', 'Bioavailability_Ma']

    all_predictions = {}
    all_results = {}

    for dataset_name in selected_datasets:
        print(f"\n{'='*40}")
        print(f"Evaluating: {dataset_name}")
        print(f"{'='*40}")

        benchmark = group.get(dataset_name)
        name = benchmark['name']
        test = benchmark['test']
        predictions_list = []

        # Train and predict for each seed
        for seed in [1, 2, 3, 4, 5]:
            _train, _valid = group.get_train_valid_split(
                benchmark=name, split_type='default', seed=seed
            )

            # TODO: Replace with your model
            # model = YourModel(random_state=seed)
            # model.fit(_train['Drug'], _train['Y'])
            # y_pred = model.predict(test['Drug'])

            # Dummy predictions for demonstration
            np.random.seed(seed)
            y_true = test['Y'].values
            y_pred = y_true + np.random.normal(0, 0.3, len(y_true))
            predictions_list.append({name: y_pred})

        all_predictions[dataset_name] = predictions_list

        # Evaluate this dataset across its 5 seeds
        results = group.evaluate_many(predictions_list)
        key = name.lower()
        all_results[dataset_name] = results[key]

        mean_score, std_score = results[key]
        print(f"  {dataset_name}: {mean_score:.4f} ± {std_score:.4f}")

    # Summary
    print("\n" + "=" * 60)
    print("Summary of Results")
    print("=" * 60)

    results_df = pd.DataFrame([
        {
            'Dataset': name,
            'Mean MAE': f"{mean:.4f}",
            'Std MAE': f"{std:.4f}"
        }
        for name, (mean, std) in all_results.items()
    ])

    print(results_df.to_string(index=False))

    return all_predictions, all_results


def custom_model_template():
    """
    Template for integrating your own model with TDC benchmarks
    """
    print("\n" + "=" * 60)
    print("Example 3: Custom Model Template")
    print("=" * 60)

    code_template = '''
# Template for using your own model with TDC benchmarks

from tdc.benchmark_group import admet_group
from your_library import YourModel  # Replace with your model

group = admet_group(path='data/')

predictions_list = []
for seed in [1, 2, 3, 4, 5]:
    benchmark = group.get('Caco2_Wang')      # {'name', 'train_val', 'test'}
    name = benchmark['name']
    test = benchmark['test']                 # fixed across seeds

    # Per-seed train/valid partition
    train, valid = group.get_train_valid_split(
        benchmark=name, split_type='default', seed=seed
    )

    model = YourModel(random_state=seed)
    model.fit(train['Drug'], train['Y'])
    # Optional early stopping: model.fit(..., validation_data=(valid['Drug'], valid['Y']))

    y_pred = model.predict(test['Drug'])
    predictions_list.append({name: y_pred})  # dict keyed by benchmark name

# Aggregate across seeds -> {'caco2_wang': [mean, std]}
results = group.evaluate_many(predictions_list)
print(f"Results: {results}")
'''

    print("\nCustom Model Integration Template:")
    print("=" * 60)
    print(code_template)

    return code_template


def multi_seed_statistics(predictions_list):
    """
    Example: Analyzing multi-seed prediction statistics.

    `predictions_list` is the list produced above: one {benchmark_name: y_pred}
    dict per seed.
    """
    print("\n" + "=" * 60)
    print("Example 4: Multi-Seed Statistics Analysis")
    print("=" * 60)

    # Each dict has a single benchmark-name key; pull out its prediction array.
    all_preds = np.array([next(iter(p.values())) for p in predictions_list])

    print("\nPrediction statistics across 5 seeds:")
    print(f"  Shape: {all_preds.shape}")
    print(f"  Mean prediction: {all_preds.mean():.4f}")
    print(f"  Std across seeds: {all_preds.std(axis=0).mean():.4f}")
    print(f"  Min prediction: {all_preds.min():.4f}")
    print(f"  Max prediction: {all_preds.max():.4f}")

    # Per-sample variance
    per_sample_std = all_preds.std(axis=0)
    print(f"\nPer-sample prediction std:")
    print(f"  Mean: {per_sample_std.mean():.4f}")
    print(f"  Median: {np.median(per_sample_std):.4f}")
    print(f"  Max: {per_sample_std.max():.4f}")


def leaderboard_submission_guide():
    """
    Guide for submitting to TDC leaderboards
    """
    print("\n" + "=" * 60)
    print("Example 5: Leaderboard Submission Guide")
    print("=" * 60)

    guide = """
To submit results to TDC leaderboards:

1. Evaluate your model following the 5-seed protocol:
   - Use seeds [1, 2, 3, 4, 5] exactly as provided
   - Do not modify the train/valid/test splits
   - Report mean ± std across all 5 seeds

2. Format your results (one {name: y_pred} dict per seed, collected in a list):
   results = group.evaluate_many(predictions_list)
   # Returns: {'dataset_name': [mean_score, std_score]}  (name lowercased)

3. Submit to leaderboard:
   - Visit: https://tdcommons.ai/benchmark/admet_group/
   - Click on your dataset of interest
   - Submit your results with:
     * Model name and description
     * Mean score ± standard deviation
     * Reference to paper/code (if available)

4. Best practices:
   - Report all datasets in the benchmark group
   - Include model hyperparameters
   - Share code for reproducibility
   - Compare against baseline models

5. Evaluation metrics:
   - ADMET Group uses MAE by default
   - Other groups may use different metrics
   - Check benchmark-specific requirements
"""

    print(guide)


def main():
    """
    Main function to run all benchmark evaluation examples
    """
    print("\n" + "=" * 60)
    print("TDC Benchmark Group Evaluation Examples")
    print("=" * 60)

    # Load benchmark group
    group = load_benchmark_group()

    # Example 1: Single dataset evaluation
    predictions_list, results = single_dataset_evaluation(group)

    # Example 2: Multiple datasets evaluation
    all_predictions, all_results = multiple_datasets_evaluation(group)

    # Example 3: Custom model template
    custom_model_template()

    # Example 4: Multi-seed statistics
    multi_seed_statistics(predictions_list)

    # Example 5: Leaderboard submission guide
    leaderboard_submission_guide()

    print("\n" + "=" * 60)
    print("Benchmark evaluation examples completed!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Replace dummy predictions with your model")
    print("2. Run full evaluation on all benchmark datasets")
    print("3. Submit results to TDC leaderboard")
    print("=" * 60)


if __name__ == "__main__":
    main()
