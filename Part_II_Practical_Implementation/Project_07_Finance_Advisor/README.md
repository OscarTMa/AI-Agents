# Project 07: AI Financial Analyst 📈

## Overview
This agent combines **Real-Time Financial Data** with the reasoning capabilities of Llama 3.3. It acts as a financial research assistant that can analyze stock fundamentals, trends, and market sentiment.

It connects to the **Yahoo Finance API** to fetch live market data, ensuring the agent never "hallucinates" stock prices.



[Image of financial data flow diagram]


## Architecture
1. **User Interface:** Streamlit Dashboard with interactive charts.
2. **Tools:**
   - `get_stock_info`: Fetches P/E, Market Cap, Analyst ratings.
   - `get_historical_prices`: Analyzes 30-day volatility.
3. **Agent:** Llama 3.3 (Groq) interprets the numbers and provides a qualitative report.

## Tech Stack
- **Library:** `yfinance` (Free market data).
- **Visualization:** `st.line_chart` (Pandas-native plotting).
- **Logic:** LangChain Tool Calling Agent.

## Usage
```bash
pip install -r requirements.txt
streamlit run app.py
