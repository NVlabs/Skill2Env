# Common Pitfalls, Quality Checklist, Mistakes & Validation

The hard-won correctness rules for this skill. Read before declaring a TimesFM task done.

## Common Pitfalls

1. **Not running system check** → model load crashes on low-RAM machines. Always run `check_system.py` first.
2. **Forgetting `model.compile()`** → `RuntimeError: Model is not compiled`. Must call `compile()` before `forecast()`.
3. **Not setting `normalize_inputs=True`** → unstable forecasts for series with large values.
4. **Using v1/v2 on machines with < 32 GB RAM** → use TimesFM 2.5 (200M params) instead.
5. **Not setting `fix_quantile_crossing=True`** → quantiles may not be monotonic (q10 > q50).
6. **Huge `per_core_batch_size` on small GPU** → CUDA OOM. Start small, increase.
7. **Passing 2-D arrays** → TimesFM expects a **list of 1-D arrays**, not a 2-D matrix.
8. **Forgetting `torch.set_float32_matmul_precision("high")`** → slower inference on Ampere+ GPUs.
9. **Not handling NaN in output** → edge cases with very short series. Always check `np.isnan(point).any()`.
10. **Using `infer_is_positive=True` for series that can be negative** → clamps forecasts at zero. Set False for temperature, returns, etc.

## Quality Checklist

Run this checklist after every TimesFM task before declaring success:

- [ ] **Output shape correct** -- `point_fc` shape is `(n_series, horizon)`, `quant_fc` is `(n_series, horizon, 10)`
- [ ] **Quantile indices** -- index 0 = mean, 1 = q10, 2 = q20 ... 9 = q90. **NOT** 0 = q0, 1 = q10.
- [ ] **Frequency flag** -- TimesFM 1.0/2.0: pass `freq=[0]` for monthly data. TimesFM 2.5: no freq flag.
- [ ] **Series length** -- context must be >= 32 data points (model minimum). Warn if shorter.
- [ ] **No NaN** -- `np.isnan(point_fc).any()` should be False. Check input series for gaps first.
- [ ] **Visualization axes** -- if multiple panels share data, use `sharex=True`. All time axes must cover the same span.
- [ ] **Binary outputs in Git LFS** -- PNG and GIF files must be tracked via `.gitattributes` (repo root already configured).
- [ ] **No large datasets committed** -- any real dataset > 1 MB should be downloaded to `tempfile.mkdtemp()` and annotated in code.
- [ ] **`matplotlib.use('Agg')`** -- must appear before any pyplot import when running headless.
- [ ] **`infer_is_positive`** -- set `False` for temperature anomalies, financial returns, or any series that can be negative.

## Common Mistakes

These bugs have appeared in this skill's examples. Learn from them:

1. **Quantile index off-by-one** -- The most common mistake. `quant_fc[..., 0]` is the **mean**, not q0. q10 = index 1, q90 = index 9. Always define named constants: `IDX_Q10, IDX_Q20, IDX_Q80, IDX_Q90 = 1, 2, 8, 9`.

2. **Variable shadowing in comprehensions** -- If you build per-series covariate dicts inside a loop, do NOT use the loop variable as the comprehension variable. Accumulate into separate `dict[str, ndarray]` outside the loop, then assign.
   ```python
   # WRONG -- outer `store_id` gets shadowed:
   covariates = {store_id: arr[store_id] for store_id in stores}  # inside outer loop over store_id
   # CORRECT -- use a different name or accumulate beforehand:
   prices_by_store: dict[str, np.ndarray] = {}
   for store_id, config in stores.items():
       prices_by_store[store_id] = compute_price(config)
   ```

3. **Wrong CSV column name** -- The global-temperature CSV uses `anomaly_c`, not `anomaly`. Always `print(df.columns)` before accessing.

4. **`tight_layout()` warning with `sharex=True`** -- Harmless; suppress with `plt.tight_layout(rect=[0, 0, 1, 0.97])` or ignore.

5. **TimesFM 2.5 required for `forecast_with_covariates()`** -- TimesFM 1.0 does NOT have this method. Install `pip install timesfm[xreg]` and use checkpoint `google/timesfm-2.5-200m-pytorch`.

6. **Future covariates must span the full horizon** -- Dynamic covariates (price, promotions, holidays) must have values for BOTH the context AND the forecast horizon. You cannot pass context-only arrays.

7. **Anomaly thresholds must be defined once** -- Define `CRITICAL_Z = 3.0`, `WARNING_Z = 2.0` as module-level constants. Never hardcode `3` or `2` inline.

8. **Context anomaly detection uses residuals, not raw values** -- Always detrend first (`np.polyfit` linear, or seasonal decomposition), then Z-score the residuals. Raw-value Z-scores are misleading on trending data.

## Validation & Verification

Use the example outputs as regression baselines. If you change forecasting logic, verify:

```bash
# Anomaly detection regression check:
python -c "
import json
d = json.load(open('examples/anomaly-detection/output/anomaly_detection.json'))
ctx = d['context_summary']
assert ctx['critical'] >= 1, 'Sep 2023 must be CRITICAL'
assert any(r['date'] == '2023-09' and r['severity'] == 'CRITICAL'
           for r in d['context_detections']), 'Sep 2023 not found'
print('Anomaly detection regression: PASS')"

# Covariates regression check:
python -c "
import pandas as pd
df = pd.read_csv('examples/covariates-forecasting/output/sales_with_covariates.csv')
assert len(df) == 108, f'Expected 108 rows, got {len(df)}'
prices = df.groupby('store_id')['price'].mean()
assert prices['store_A'] > prices['store_B'] > prices['store_C'], 'Store price ordering wrong'
print('Covariates regression: PASS')"
```
