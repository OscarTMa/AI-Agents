import streamlit as st
import yfinance as yf
from langchain_groq import ChatGroq
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain.callbacks import StreamlitCallbackHandler
from langchain_core.tools import tool

# --- HERRAMIENTAS (Definidas aquí mismo para evitar errores de importación) ---

@tool
def get_stock_info(symbol: str):
    """Get current price, P/E ratio, and fundamental info of a stock ticker."""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        data = {
            "price": info.get("currentPrice"),
            "marketCap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "recommendation": info.get("recommendationKey"),
            "summary": info.get("longBusinessSummary", "")[:200]
        }
        return str(data)
    except Exception as e:
        return f"Error: {e}"

@tool
def get_historical_prices(symbol: str):
    """Get price trend over the last month."""
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1mo")
        if hist.empty: return "No data."
        start = hist['Close'].iloc[0]
        end = hist['Close'].iloc[-1]
        change = ((end - start) / start) * 100
        return f"Start: {start:.2f}, End: {end:.2f}, Change: {change:.2f}%"
    except Exception as e:
        return f"Error: {e}"

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="AI Financial Analyst", page_icon="📈", layout="wide")
st.title("📈 Project 07: AI Financial Analyst")

with st.sidebar:
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
    else:
        api_key = st.text_input("Groq API Key", type="password")

if not api_key:
    st.stop()

# --- CEREBRO DEL AGENTE ---
llm = ChatGroq(
    groq_api_key=api_key, 
    model_name="llama-3.3-70b-versatile",
    temperature=0
)

tools = [get_stock_info, get_historical_prices]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a Financial Analyst. Use tools to get real data. Not financial advice."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# En LangChain 0.2.14, esto funciona perfectamente sin errores de Pydantic
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- INTERFAZ ---
col1, col2 = st.columns([1, 2])
with col1:
    ticker = st.text_input("Ticker:", value="NVDA").upper()
    if ticker:
        try:
            # Gráfico visual rápido
            df = yf.Ticker(ticker).history(period="3mo")
            if not df.empty:
                st.line_chart(df['Close'], height=200)
                st.metric("Price", f"${df['Close'].iloc[-1]:.2f}")
        except: pass

with col2:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if query := st.chat_input("Ask analysis..."):
        st.session_state.messages.append({"role": "user", "content": query})
        st.chat_message("user").write(query)
        
        with st.chat_message("assistant"):
            # Contexto automático
            final_prompt = f"Analyze {ticker}: {query}" if ticker else query
            
            st_cb = StreamlitCallbackHandler(st.container())
            resp = agent_executor.invoke({"input": final_prompt}, {"callbacks": [st_cb]})
            
            st.write(resp["output"])
            st.session_state.messages.append({"role": "assistant", "content": resp["output"]})
