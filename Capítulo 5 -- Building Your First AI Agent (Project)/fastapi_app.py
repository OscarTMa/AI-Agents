"""
fastapi_app.py
---------------
REST API built with FastAPI for Bitcoin price forecasting.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from api_utils import load_arima_model, preprocess_input, forecast_arima

# Create FastAPI app
app = FastAPI(
    title="Bitcoin Forecasting API",
    description="API REST for Bitcoin price prediction using ARIMA model.",
    version="1.0.0"
)


class ForecastRequest(BaseModel):
    """
    Expected input JSON body:
    {
        "data": {"2025-01-01": 40000.0, "2025-01-02": 41000.5},
        "steps": 7
    }
    """
    data: dict
    steps: int


@app.post("/forecast")
async def forecast(request: ForecastRequest):
    """
    POST endpoint for generating forecasts.
    """
    try:
        model = load_arima_model("models/arima_model.pkl")
        series = preprocess_input(request.data)
        forecast_result = forecast_arima(model, request.steps)
        return {"forecast": forecast_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "Welcome to the Bitcoin Forecasting FastAPI!"}
