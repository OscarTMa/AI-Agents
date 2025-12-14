import streamlit as st
import yfinance as yf
import pandas as pd
from langchain_groq import ChatGroq
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.tools import Tool
from langchain_core.prompts import ChatPromptTemplate
from langchain.callbacks import StreamlitCallbackHandler
from tools import get_stock_info, get_historical_prices

# -----------------------------------------------
# st.set_page_config(page_title="AI Financial Analyst", page_icon="📈", layout="wide")
#
# st.title("📈 Project 07: AI Financial Analyst")
# st.caption("Powered by Groq (Llama 3.3) & Yahoo Finance")
st.set_page_config(page_title="AI Financial Analyst", page_icon="📈", layout="wide")

st.write("🔄 Iniciando aplicación...") # Mensaje de debug en pantalla

try:
    import yfinance as yf
    import pandas as pd
    from langchain_groq import ChatGroq
    # Verifica que la importación de tools funcione
    from tools import get_stock_info, get_historical_prices
    st.write("✅ Librerías importadas correctamente") # Mensaje de debug
except Exception as e:
    st.error(f"❌ Error crítico importando librerías: {e}")
    st.stop()

# -----------------------------------------------
# --- 1. CONFIGURACIÓN ---
with st.sidebar:
    st.header("Configuration")
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
        st.success("API Key loaded!", icon="✅")
    else:
        api_key = st.text_input("Groq API Key", type="password")

    st.markdown("---")
    st.markdown("**Example Tickers:** AAPL, TSLA, NVDA, MSFT, BTC-USD")

if not api_key:
    st.warning("Please enter your Groq API Key.")
    st.stop()

# --- 2. CONFIGURACIÓN DEL AGENTE ---

# Definir las herramientas para LangChain
tools = [
    Tool(
        name="Get Stock Fundamentals",
        func=get_stock_info,
        description="Use this to get current price, PE ratio, and fundamental info of a stock. Input: Ticker symbol (e.g., AAPL)."
    ),
    Tool(
        name="Get Historical Trend",
        func=get_historical_prices,
        description="Use this to get the price trend over the last month. Input: Ticker symbol."
    )
]

llm = ChatGroq(
    groq_api_key=api_key, 
    model_name="llama-3.3-70b-versatile",
    temperature=0
)

# Prompt del Sistema (System Prompt) - Dando personalidad financiera
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a Wall Street Financial Analyst.
    Your goal is to help users analyze stocks using real-time data.
    
    GUIDELINES:
    1. Always use the tools to get REAL data. Do not guess prices.
    2. Analyze the P/E ratio and trends.
    3. Be professional but concise.
    4. MANDATORY: End every response with: 
       "⚠️ **Disclaimer:** This is an AI analysis, not professional financial advice. Do your own research."
    """),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- 3. INTERFAZ VISUAL DE MERCADO ---

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Market Dashboard")
    ticker_input = st.text_input("Enter Ticker Symbol:", value="AAPL").upper()
    
    if ticker_input:
        # Mini-dashboard visual sin usar IA (Datos crudos)
        try:
            stock = yf.Ticker(ticker_input)
            hist = stock.history(period="6mo")
            
            # Métricas
            current_price = hist['Close'].iloc[-1]
            prev_price = hist['Close'].iloc[-2]
            delta = current_price - prev_price
            
            st.metric("Current Price", f"${current_price:.2f}", f"{delta:.2f}")
            
            # Gráfico
            st.line_chart(hist['Close'], height=200)
            
        except Exception as e:
            st.error("Invalid Ticker")

# --- 4. INTERFAZ DE CHAT (EL AGENTE) ---

with col2:
    st.subheader("AI Analyst Chat")
    
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Hello! I can analyze stocks for you. Ask me 'Is Apple a good buy right now?' or 'Compare Tesla and Ford'."}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ask about the stock market..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.chat_message("assistant"):
            st_callback = StreamlitCallbackHandler(st.container())
            # Pasamos el contexto del Ticker seleccionado en el dashboard al chat automáticamente
            if ticker_input and ticker_input in prompt.upper():
                pass # El usuario ya mencionó el ticker
            elif ticker_input:
                # Inyección de contexto: Si el usuario dice "¿Es buena compra?", asumimos que habla del ticker en pantalla
                prompt = f"Regarding {ticker_input}: {prompt}"
            
            response = agent_executor.invoke({"input": prompt}, {"callbacks": [st_callback]})
            st.write(response["output"])
            st.session_state.messages.append({"role": "assistant", "content": response["output"]})
