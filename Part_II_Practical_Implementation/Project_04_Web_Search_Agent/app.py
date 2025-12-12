import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain.callbacks import StreamlitCallbackHandler

st.set_page_config(page_title="Web Search Agent", page_icon="🌐")

st.title("🌐 Project 04: Search Agent (Tool Calling)")
st.caption("Powered by Groq (Llama 3.3) & Tavily AI")

# --- 1. CONFIGURACIÓN ---
with st.sidebar:
    st.header("Configuration")
    
    if "GROQ_API_KEY" in st.secrets:
        groq_api_key = st.secrets["GROQ_API_KEY"]
    else:
        groq_api_key = st.text_input("Groq API Key", type="password")

    if "TAVILY_API_KEY" in st.secrets:
        tavily_api_key = st.secrets["TAVILY_API_KEY"]
    else:
        tavily_api_key = st.text_input("Tavily API Key", type="password")

if not groq_api_key or not tavily_api_key:
    st.warning("Please enter both API Keys to continue.")
    st.stop()

# --- 2. DEFINIR HERRAMIENTAS Y LLM ---

# Herramienta de búsqueda
search_tool = TavilySearchResults(
    tavily_api_key=tavily_api_key, 
    max_results=2  # Traemos 2 resultados para no saturar al LLM
)
tools = [search_tool]

# LLM (Llama 3.3 es excelente para Tool Calling)
llm = ChatGroq(
    groq_api_key=groq_api_key, 
    model_name="llama-3.3-70b-versatile", 
    temperature=0
)

# --- 3. CREAR EL AGENTE MODERNO ---

# Prompt Template específico para Agentes con Herramientas
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. You can search the web using Tavily to answer current questions."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"), # Aquí es donde ocurre la magia del pensamiento
])

# Construcción del Agente (Usando Tool Calling nativo)
agent = create_tool_calling_agent(llm, tools, prompt)

# El Executor es el que corre el bucle (run loop)
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True,
    handle_parsing_errors=True # Si falla algo, intenta corregirse solo
)

# --- 4. INTERFAZ DE CHAT ---

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi! I'm connected to the web. Ask me about current events like Bitcoin price or Sports results."}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if user_input := st.chat_input("What do you want to know?"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        
        try:
            # Ejecutamos el agente
            response = agent_executor.invoke(
                {"input": user_input},
                {"callbacks": [st_callback]}
            )
            
            output_text = response["output"]
            st.write(output_text)
            st.session_state.messages.append({"role": "assistant", "content": output_text})
            
        except Exception as e:
            st.error(f"Error: {e}")
