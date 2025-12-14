# Project 08: Multi-Agent Research Team 👥

## Overview
This project demonstrates the power of **Multi-Agent Systems** using the **CrewAI** framework.
Instead of a single agent doing all the work, we orchestrate a team of specialized agents:

1.  **🕵️ Researcher:** Scours the web for real-time information using Tavily.
2.  **✍️ Writer:** Transforms that raw data into an engaging blog post.



## Tech Stack
- **Orchestrator:** CrewAI.
- **Brain:** Groq (Llama 3.3).
- **Tools:** Tavily Search API.
- **Framework:** Streamlit.

## The Logic
We use a **Sequential Process**:
`User Input` -> `Researcher Agent (Web Search)` -> `Research Report` -> `Writer Agent` -> `Final Blog Post`.

## Usage
```bash
pip install -r requirements.txt
streamlit run app.py
