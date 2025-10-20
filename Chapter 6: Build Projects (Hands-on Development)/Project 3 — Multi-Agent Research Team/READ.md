## 🧩 Project 3 — Multi-Agent Research Team

# 🧑‍💼 Project 3 — Multi-Agent Research Team

## 🎯 Objective
Develop a system where multiple agents (Researcher, Writer, Reviewer) collaborate autonomously to produce structured reports from online information.
---

## 🧠 Architecture
Researcher → Writer → Reviewer → Final Report

---

## 🧰 Tech Stack
- **CrewAI** (multi-agent coordination)
- **OpenAI GPT / Anthropic Claude**
- **LangChain**
- **Python**

---

## ⚙️ Implementation Steps

### 1️⃣ Install dependencies
```bash
pip install crewai langchain openai
```

### 2️⃣ Define agents

```python
# agents.py
from crewai import Agent

researcher = Agent(role="Researcher", goal="Collect factual data about a topic")
writer = Agent(role="Writer", goal="Draft a structured report based on research")
reviewer = Agent(role="Reviewer", goal="Validate coherence and quality")
```

### 3️⃣ Define the workflow

```python
#main.py
from crewai import Crew
from agents import researcher, writer, reviewer

crew = Crew([researcher, writer, reviewer])
result = crew.run("Latest advances in AI safety research")
print(result)
```

### ☁️ Deployment                    

- Docker container                   
- Optionally deploy via Kubernetes for multiple concurrent teams.                         

### ✅ Expected Output
A collaborative workflow where:

The Researcher gathers web data.

The Writer synthesizes insights.

The Reviewer ensures logical coherence and accuracy.


