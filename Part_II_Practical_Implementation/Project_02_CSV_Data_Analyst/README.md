# Project 02: CSV Data Analyst Agent 📊

## Overview
This agent demonstrates the **"Code Interpreter"** pattern. Instead of using the LLM's internal knowledge to answer math questions (which is unreliable), we ask the LLM to write **Pandas Python code** and then we execute that code to get the exact answer.

## Tech Stack
- **Engine:** Groq (Llama 3 70b) - High logic capability required for coding.
- **Data:** Pandas DataFrame.
- **Interface:** Streamlit.

## How it Works
1. User uploads a CSV.
2. The agent reads the column names (Schema).
3. User asks: "What is the average salary?"
4. Agent generates: `result = df['Salary'].mean()`
5. System executes code -> Returns `85000`.

## Setup
```bash
pip install -r requirements.txt
streamlit run app.py
