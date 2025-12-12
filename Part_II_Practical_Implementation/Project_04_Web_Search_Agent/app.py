import streamlit as st
from langchain_groq import ChatGroq
# CAMBIO 1: Importamos Tavily en lugar de DuckDuckGo
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler

st.set_page_config(page_title="Web Search Agent", page_icon="🌐")

st.title("🌐 Project 04: Web Search Agent (Tavily)")
st.caption("Powered by Groq (Llama 3.3) & Tavily AI")

# 1. Configuración
with st.sidebar:
    st.header("Configuration")
    
    # API Key de Groq
    if "GROQ_API_KEY" in st.secrets:
        groq_api_key = st.secrets["GROQ_API_KEY"]
    else:
        groq_api_key = st.text_input("Groq API Key", type="password")

    # CAMBIO 2: API Key de Tavily
    if "TAVILY_API_KEY" in st.secrets:
        tavily_api_key = st.secrets["TAVILY_API_KEY"]
    else:
        tavily_api_key = st.text_input("Tavily API Key", type="password")

if not groq_api_key or not tavily_api_key:
    st.warning("Please enter both Groq and Tavily API Keys.")
    st.stop()

# 'max_results=2' es suficiente para obtener buen contexto sin gastar tokens
search_tool = TavilySearchResults(
    tavily_api_key=tavily_api_key, 
    max_results=2
)

# 3. Inicializar el Agente
llm = ChatGroq(
    groq_api_key=groq_api_key, 
    model_name="llama-3.3-70b-versatile", 
    temperature=0,
    streaming=True
)

# ZERO_SHOT_REACT_DESCRIPTION es el cerebro que decide cuándo buscar
search_agent = initialize_agent(
    tools=[search_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose=True
)

# 4. Interfaz de Chat
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi! I am connected to the real-time web using Tavily. Ask me anything."}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("What do you want to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        
        try:
            response = search_agent.run(prompt, callbacks=[st_callback])
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error: {e}")
