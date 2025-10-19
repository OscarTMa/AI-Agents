# ==========================================
# 🌐 Flask Application for AI Agent
# ==========================================
from flask import Flask, jsonify, request
from agent_core import process_input, agent
import asyncio

app = Flask(__name__)

@app.route("/status", methods=["GET"])
def get_status():
    """Return the agent’s current state."""
    return jsonify({"name": agent.name, "status": agent.status})

@app.route("/respond", methods=["POST"])
def respond():
    """Handle user query using Flask (sync wrapper around asyncio)."""
    data = request.get_json()
    message = data.get("message", "")
    agent.status = "processing"
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    reply = loop.run_until_complete(process_input(message))
    agent.status = "idle"
    return jsonify({"response": reply})

# Example: Run with `python api/flask_app.py`
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

