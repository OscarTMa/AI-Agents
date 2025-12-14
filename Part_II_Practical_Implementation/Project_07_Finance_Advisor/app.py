import streamlit as st
import yfinance as yf
import pandas as pd
from langchain_groq import ChatGroq
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain.callbacks import StreamlitCallbackHandler

# Importamos las funciones ya decoradas
from tools import get_stock_info, get_historical_prices

st.set_page_config(page_title="AI Financial Analyst", page_icon="📈", layout="wide")

st.title("📈 Project 07: AI Financial Analyst")
st.caption("Powered by Groq (Llama 3.3) & Yahoo Finance")

# --- 1. CONFIGURACIÓN ---
with st.sidebar:
    st.header("Configuration")
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
    else:
        api_key = st.text_input("Groq API Key", type="password")
    
    st.markdown("Example Tickers: AAPL, NVDA, TSLA, MSFT")

if not api_key:
    st.warning("Please enter your Groq API Key.")
    st.stop()

# --- 2. CONFIGURACIÓN DEL AGENTE ---

# CAMBIO CRÍTICO: Simplemente pasamos la lista de funciones decoradas
# Ya no usamos la clase Tool(...) manual que causaba el error
tools = [get_stock_info, get_historical_prices] 

llm = ChatGroq(
    groq_api_key=api_key, 
    model_name="llama-3.3-70b-versatile",
    temperature=0
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a Wall Street Financial Analyst.
    Use the provided tools to get REAL-TIME data. 
    Do not guess prices.
    
    If the user asks about a company, ALWAYS check its fundamentals first.
    End with: "⚠️ **Disclaimer:** Not financial advice."
    """),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# Ahora el agente puede "bindear" las herramientas correctamente
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# --- 3. INTERFAZ ---

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Market Data")
    ticker_input = st.text_input("Ticker Symbol:", value="NVDA").upper()
    
    if ticker_input:
        try:
            # Gráfico simple sin IA para referencia visual
            stock = yf.Ticker(ticker_input)
            hist = stock.history(period="3mo")
            if not hist.empty:
                st.line_chart(hist['Close'], height=200)
                curr = hist['Close'].iloc[-1]
                st.metric("Price", f"${curr:.2f}")
        except:
            st.error("Ticker not found")

with col2:
    st.subheader("AI Chat")
    
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Ask me to analyze a stock!"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if user_input := st.chat_input("Ask something..."):
        # Contexto automático
        if ticker_input and ticker_input not in user_input.upper():
            full_prompt = f"Analyze {ticker_input}: {user_input}"
        else:
            full_prompt = user_input
            
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        with st.chat_message("assistant"):
            st_callback = StreamlitCallbackHandler(st.container())
            response = agent_executor.invoke(
                {"input": full_prompt}, 
                {"callbacks": [st_callback]}
            )
            output = response["output"]
            st.write(output)
            st.session_state.messages.append({"role": "assistant", "content": output})
