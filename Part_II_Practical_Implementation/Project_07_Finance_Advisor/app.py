import streamlit as st
import sys

# 1. ESTO DEBE SER LA PRIMERA LÍNEA EJECUTABLE SIEMPRE
st.set_page_config(page_title="AI Financial Analyst", page_icon="📈", layout="wide")

# 2. SISTEMA DE DIAGNÓSTICO VISUAL
st.title("📈 Project 07: AI Financial Analyst")
status_area = st.empty()
status_area.info("🚀 Iniciando sistema... (Si lees esto, Streamlit funciona)")

try:
    # 3. IMPORTS DIFERIDOS (Lazy Imports)
    # Importamos aquí dentro para atrapar errores y evitar pantalla blanca
    status_area.info("📦 Cargando librerías de IA y Finanzas...")
    
    import yfinance as yf
    import pandas as pd
    from langchain_groq import ChatGroq
    from langchain_core.prompts import ChatPromptTemplate
    from langchain.tools import tool
    from langchain.agents import AgentExecutor, create_tool_calling_agent
    from langchain.callbacks import StreamlitCallbackHandler
    
    status_area.success("✅ Librerías cargadas correctamente.")
    status_area.empty() # Limpiamos los mensajes de carga

except Exception as e:
    st.error(f"❌ ERROR CRÍTICO AL IMPORTAR: {e}")
    st.code(f"Detalles técnicos: {sys.exc_info()}")
    st.stop()

# --- 4. DEFINICIÓN DE HERRAMIENTAS ---

@tool
def get_stock_info(symbol: str):
    """Get stock fundamentals (Price, PE, etc)."""
    try:
        ticker = yf.Ticker(symbol)
        # Forzamos fast_info para evitar bloqueos de red
        price = ticker.fast_info.last_price
        return f"Current Price of {symbol}: ${price:.2f}"
    except Exception as e:
        return f"Error fetching price: {e}"

@tool
def get_historical_prices(symbol: str):
    """Get trend last month."""
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1mo")
        if hist.empty: return "No data"
        start = hist['Close'].iloc[0]
        end = hist['Close'].iloc[-1]
        change = ((end - start) / start) * 100
        return f"Start: {start:.2f}, End: {end:.2f}, Change: {change:.2f}%"
    except Exception as e:
        return f"Error: {e}"

# --- 5. LÓGICA DE LA APP ---

with st.sidebar:
    st.header("Config")
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
        st.success("API Key found")
    else:
        api_key = st.text_input("Groq API Key", type="password")

if not api_key:
    st.warning("Please enter Groq API Key")
    st.stop()

# Configuración del Agente
llm = ChatGroq(groq_api_key=api_key, model_name="llama-3.3-70b-versatile", temperature=0)
tools = [get_stock_info, get_historical_prices]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a Financial Analyst. Use tools for data."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

try:
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
except Exception as e:
    st.error(f"Error creando el agente: {e}")
    st.stop()

# Interfaz
col1, col2 = st.columns([1, 2])

with col1:
    ticker = st.text_input("Ticker", value="AAPL").upper()
    if ticker:
        try:
            # Uso básico de yfinance para el gráfico
            df = yf.Ticker(ticker).history(period="1mo")
            if not df.empty:
                st.line_chart(df['Close'], height=200)
                st.metric("Price", f"${df['Close'].iloc[-1]:.2f}")
        except Exception as e:
            st.caption(f"Could not load chart: {e}")

with col2:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if query := st.chat_input("Ask analysis..."):
        st.session_state.messages.append({"role": "user", "content": query})
        st.chat_message("user").write(query)
        
        with st.chat_message("assistant"):
            st_cb = StreamlitCallbackHandler(st.container())
            # Inyectamos contexto
            full_prompt = f"Analyze {ticker}: {query}" if ticker else query
            
            try:
                resp = agent_executor.invoke({"input": full_prompt}, {"callbacks": [st_cb]})
                st.write(resp["output"])
                st.session_state.messages.append({"role": "assistant", "content": resp["output"]})
            except Exception as e:
                st.error(f"Agent Error: {e}")
