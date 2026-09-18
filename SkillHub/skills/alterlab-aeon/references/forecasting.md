# Time Series Forecasting

Aeon provides forecasting algorithms for predicting future time series values.

## Naive and Baseline Methods

Simple forecasting strategies for comparison:

- `NaiveForecaster` - Strategies: last value, mean, seasonal-last
  - Parameters: `strategy` ("last", "mean", "seasonal_last"), `seasonal_period`, `horizon`
  - **Use when**: Establishing baselines or simple patterns

## Statistical Models

Classical time series forecasting methods:

### ARIMA
- `ARIMA` - AutoRegressive Integrated Moving Average
  - Parameters: `p` (AR order), `d` (differencing), `q` (MA order)
  - **Use when**: Linear patterns, stationary or difference-stationary series

### Exponential Smoothing
- `ETS` - Error-Trend-Seasonal decomposition
  - Parameters: `error`, `trend`, `seasonal` types
  - **Use when**: Trend and seasonal patterns present

### Threshold Autoregressive
- `TAR` - Threshold Autoregressive model for regime switching
- `AutoTAR` - Automated threshold discovery
  - **Use when**: Series exhibits different behaviors in different regimes

### Theta Method
- `Theta` - Classical Theta forecasting
  - Parameters: `theta`, `weights` for decomposition
  - **Use when**: Simple but effective baseline needed

### Time-Varying Parameter
- `TVP` - Time-varying parameter model with Kalman filtering
  - **Use when**: Parameters change over time

## Deep Learning Forecasters

Neural networks for complex temporal patterns:

- `TCNForecaster` - Temporal Convolutional Network
  - Dilated convolutions for large receptive fields
  - **Use when**: Long sequences, need non-recurrent architecture

- `DeepARNetwork` - Probabilistic forecasting with RNNs
  - Provides prediction intervals
  - **Use when**: Need probabilistic forecasts, uncertainty quantification

## Regression-Based Forecasting

Apply regression to lagged features:

- `RegressionForecaster` - Wraps regressors for forecasting
  - Parameters: `window_length`, `horizon`
  - **Use when**: Want to use any regressor as forecaster

## Quick Start

```python
import numpy as np
from aeon.forecasting import NaiveForecaster
from aeon.forecasting.stats import ARIMA

# Create time series
y = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)

# Naive baseline — predict() returns ONE value, `horizon` steps ahead.
naive = NaiveForecaster(strategy="last", horizon=1)
naive.fit(y)
next_naive = naive.predict()

# ARIMA — orders are separate args (p, d, q), NOT an `order` tuple.
arima = ARIMA(p=1, d=1, q=1)
arima.fit(y)
next_arima = arima.predict()
```

## Forecasting Horizon

Aeon 1.x has no sktime-style `fh` / `ForecastingHorizon` object. A forecaster
predicts a single point `self.horizon` steps ahead. For a multi-step path, use
`iterative_forecast`, which fits once and feeds its own predictions back in:

```python
# 1D ndarray of length 3 (steps t+1, t+2, t+3)
multi_step = arima.iterative_forecast(y, prediction_horizon=3)
```

## Model Selection

- **Baseline**: NaiveForecaster with seasonal strategy
- **Linear patterns**: ARIMA
- **Trend + seasonality**: ETS
- **Regime changes**: TAR, AutoTAR
- **Complex patterns**: TCNForecaster
- **Probabilistic**: DeepARNetwork
- **Long sequences**: TCNForecaster
- **Short sequences**: ARIMA, ETS

## Evaluation Metrics

Aeon forecasters return plain numpy arrays, so score them with sklearn metrics
(aeon 1.x dropped the old `aeon.performance_metrics` module):

```python
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error,
)

mae = mean_absolute_error(y_true, y_pred)
mse = mean_squared_error(y_true, y_pred)
mape = mean_absolute_percentage_error(y_true, y_pred)
```

## Exogenous Variables

Many forecasters accept exogenous features via the positional `exog` argument
(not sktime's `X=`):

```python
forecaster.fit(y, exog=exog_train)

# predict() uses the exog already seen in fit; pass new exog explicitly if needed
y_pred = forecaster.predict(exog=exog_train)
```

## Base Classes

- `BaseForecaster` - Abstract base for all forecasters
- `BaseDeepForecaster` - Base for deep learning forecasters

Extend these to implement custom forecasting algorithms.
