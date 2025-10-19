# 🧩 Chapter 2 – Python Foundations for Agents

## 🎯 Objective

Learn the essential Python concepts required to build AI Agents:
- `asyncio` for asynchronous execution  
- `dataclasses` for structured state management  
- API usage with `requests`, `FastAPI`, and `Flask`  
- Modular project organization  

---

## 🧠 Concept Overview

AI agents in Python rely on asynchronous logic and structured data management.  
They must:
- Maintain **state** (memory, task, status)  
- Communicate with **APIs**  
- Handle **concurrent tasks** efficiently  
- Expose an **interface** (FastAPI, Flask) for interaction  

---

### ==========================================
### 🧩 Python Foundations for AI Agents
### ==========================================

```python
# ──────────────────────────────────────────
# 1️⃣ Import Core Libraries
# ──────────────────────────────────────────
import asyncio              # For asynchronous operations
from dataclasses import dataclass
from fastapi import FastAPI
import requests

# ──────────────────────────────────────────
# 2️⃣ Define Agent State
# ──────────────────────────────────────────
@dataclass
class AgentState:
    name: str
    memory: dict
    status: str = "idle"

# Initialize the agent
agent = AgentState(name="KairosAgent", memory={})

# ──────────────────────────────────────────
# 3️⃣ Define Asynchronous Behavior
# ──────────────────────────────────────────
async def gather_information():
    """Simulate data retrieval (API or DB call)."""
    print("Fetching external data...")
    await asyncio.sleep(1)
    return {"info": "data received"}

async def process_input(user_input: str):
    """Handle user input and prepare a response."""
    data = await gather_information()
    agent.memory["last_input"] = user_input
    return f"Processed: {user_input} with {data['info']}"

# ──────────────────────────────────────────
# 4️⃣ External API Integration
# ──────────────────────────────────────────
def call_external_api():
    """Agent interacts with an external REST API."""
    response = requests.get("https://api.example.com/data")
    return response.json() if response.status_code == 200 else {"error": "API unavailable"}

# ──────────────────────────────────────────
# 5️⃣ Web API Layer (FastAPI)
# ──────────────────────────────────────────
app = FastAPI(title="Kairos AI Agent API")

@app.get("/agent/status")
def get_status():
    """Check the agent’s current state."""
    return {"name": agent.name, "status": agent.status}

@app.post("/agent/respond")
async def respond_to_user(query: str):
    """Process a user query asynchronously."""
    agent.status = "processing"
    reply = await process_input(query)
    agent.status = "idle"
    return {"response": reply}

# ──────────────────────────────────────────
# 6️⃣ Application Entry Point
# ──────────────────────────────────────────
if __name__ == "__main__":
    asyncio.run(process_input("Hello Agent"))
    print("Agent initialized and ready.")
```
````
User → FastAPI endpoint (/agent/respond)
        ↓
   process_input() → gather_information()
        ↓
   dataclass stores state and memory
        ↓
   Response generated → returned to user
````

## ✅ Key Takeaways

 - asyncio allows agents to handle multiple tasks efficiently.

 - dataclasses simplify structured state representation.

 - requests connects your agent to external APIs.

 - FastAPI exposes your agent’s logic as a RESTful API.

 - The design is modular and scalable — ready for LLM integration.
