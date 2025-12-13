# Project 06: Python Code Interpreter 🐍

## Overview
This is a general-purpose **AI Code Interpreter**. It gives the LLM (Llama 3.3) a "Python Sandbox" where it can write and execute code to solve problems.

Unlike standard chatbots that "guess" mathematical answers, this agent:
1. **Writes** a Python script to solve the problem.
2. **Executes** the script in a secure REPL environment.
3. **Observes** the output.
4. **Plots** data using Matplotlib if requested.



## Features
- **Math & Logic:** Solves complex calculations (Factorials, Fibonacci, Simulations) precisely.
- **Data Visualization:** Generates charts (Matplotlib) and displays them in the UI.
- **Self-Correction:** If the code fails, the agent reads the error and tries to fix the code automatically.

## Example Prompts
- *"Calculate the sum of the first 50 prime numbers."*
- *"Create a pie chart showing the distribution of 5 random variables."*
- *"Write a simulation of rolling two dice 10,000 times and plot the sum frequency."*

## Usage
```bash
pip install -r requirements.txt
streamlit run app.py
