
# ==========================================
# 🚀 FastAPI Application for AI Agent
# ==========================================
from fastapi import FastAPI
from pydantic import BaseModel
from agent_core import process_input, agent

# Define request model
class Query(BaseModel):
    message: str

# Initialize the FastAPI app
app = FastAPI(title="Kairos AI Agent API", version="1.0")

@app.get("/status")
def get_status():
    """Returns the current state of the agent."""
    return {"name": agent.name, "status": agent.status}

@app.post("/respond")
async def respond(query: Query):
    """Processes a user query asynchronously."""
    agent.status = "processing"
    reply = await process_input(query.message)
    agent.status = "idle"
    return {"response": reply}

# Example: Run with `uvicorn api.fastapi_app:app --reload`
