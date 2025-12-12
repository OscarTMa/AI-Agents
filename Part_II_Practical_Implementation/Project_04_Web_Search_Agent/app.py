import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler

st.set_page_config(page_title="Web Search Agent", page_icon="🌐")

st.title("🌐 Project 04: Web Search Agent")
st.caption("Powered by Groq (Llama 3.3) & DuckDuckGo")

# 1. Configuración
with st.sidebar:
    st.header("Configuration")
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
        st.success("API Key loaded!", icon="✅")
    else:
        api_key = st.text_input("Groq API Key", type="password")

if not api_key:
    st.warning("Please enter your Groq API Key.")
    st.stop()

# 2. Definir Herramientas (Tools)
# Wrapper de DuckDuckGo (Buscador gratuito)
wrapper = DuckDuckGoSearchAPIWrapper(region="wt-wt", time="d", max_results=5)
search_tool = DuckDuckGoSearchRun(name="Web Search", api_wrapper=wrapper)

# 3. Inicializar el Agente
llm = ChatGroq(
    groq_api_key=api_key, 
    model_name="llama-3.3-70b-versatile", 
    temperature=0,
    streaming=True
)

# ZERO_SHOT_REACT_DESCRIPTION es el tipo de agente que "Razona" y luego "Actúa"
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
        {"role": "assistant", "content": "Hi! I can search the web for you. Try asking about current events."}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("What do you want to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        # Callback para ver el "pensamiento" del agente en pantalla
        st_callback = StreamlitCallbackHandler(st.container())
        
        try:
            response = search_agent.run(prompt, callbacks=[st_callback])
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error: {e}")
