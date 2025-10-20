"""
api_utils.py
-------------
Utility functions for preprocessing, loading models, and forecasting.
Used by both FastAPI and Flask apps.
"""

import pandas as pd
import joblib
from statsmodels.tsa.arima.model import ARIMAResults


def load_arima_model(model_path: str):
    """
    Load a pre-trained ARIMA model from disk.
    """
    try:
        model = ARIMAResults.load(model_path)
        return model
    except Exception as e:
        raise RuntimeError(f"Error loading ARIMA model: {e}")


def preprocess_input(data: dict) -> pd.Series:
    """
    Convert input JSON data into a Pandas Series suitable for forecasting.
    Expected format: {"2025-01-01": 40000.0, "2025-01-02": 41000.5, ...}
    """
    try:
        series = pd.Series(data)
        series.index = pd.to_datetime(series.index)
        series = series.sort_index()
        return series
    except Exception as e:
        raise ValueError(f"Invalid input format: {e}")


def forecast_arima(model, steps: int):
    """
    Generate a forecast using the loaded ARIMA model.
    """
    try:
        forecast = model.forecast(steps=steps)
        return forecast.to_dict()
    except Exception as e:
        raise RuntimeError(f"Forecasting failed: {e}")
