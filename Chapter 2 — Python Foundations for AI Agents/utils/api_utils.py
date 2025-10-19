
# ==========================================
# 🛠️ API Utilities for AI Agents
# ==========================================
import requests
import json

def fetch_external_data(api_url: str):
    """Fetch data from a public API."""
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def post_to_external_api(api_url: str, payload: dict):
    """Send data (POST) to an API endpoint."""
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(api_url, data=json.dumps(payload), headers=headers, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def format_response(agent_name: str, message: str, data: dict):
    """Format a consistent JSON response for all API layers."""
    return {
        "agent": agent_name,
        "message": message,
        "data": data
    }
