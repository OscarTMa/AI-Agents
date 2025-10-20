"""
flask_app.py
-------------
Simple Flask API for Bitcoin price forecasting using ARIMA model.
"""

from flask import Flask, jsonify, request
from api_utils import load_arima_model, preprocess_input, forecast_arima

# Create Flask app
app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Bitcoin Forecasting Flask API!"})


@app.route("/forecast", methods=["POST"])
def forecast():
    """
    POST endpoint for generating forecasts.
    """
    try:
        json_data = request.get_json()
        model = load_arima_model("models/arima_model.pkl")
        series = preprocess_input(json_data.get("data", {}))
        steps = json_data.get("steps", 7)
        forecast_result = forecast_arima(model, steps)
        return jsonify({"forecast": forecast_result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
