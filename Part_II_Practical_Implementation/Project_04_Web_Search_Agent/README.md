# Project 04: Web Search Agent 🌐

## Overview
This agent connects a Large Language Model (Llama 3.3) to the internet using **DuckDuckGo Search**.

Standard LLMs have a "knowledge cutoff" (they don't know what happened yesterday). This agent solves that by using a **Tool-Use Architecture**.

## How it Works
1. **User Query:** "Who won the Super Bowl this year?"
2. **Reasoning:** The Agent thinks: *"I don't know this answer. I should use the [Web Search] tool."*
3. **Action:** It queries DuckDuckGo.
4. **Observation:** It reads the search results.
5. **Final Answer:** It synthesizes the information and answers the user.

## Tech Stack
- **LangChain Agents:** Specifically `ZERO_SHOT_REACT_DESCRIPTION`.
- **Tool:** `DuckDuckGoSearchRun` (Free, no API key required).
- **LLM:** Groq.

## Usage
```bash
pip install -r requirements.txt
streamlit run app.py
