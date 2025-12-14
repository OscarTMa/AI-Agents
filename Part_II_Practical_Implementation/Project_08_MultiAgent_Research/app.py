import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
from langchain_core.tools import Tool
from tavily import TavilyClient

# 1. CONFIGURACIÓN
st.set_page_config(page_title="AI Research Team", page_icon="👥", layout="wide")
st.title("👥 Project 08: Multi-Agent Research Team (Stable)")

# 2. CREDENCIALES
with st.sidebar:
    st.header("🔑 Credentials")
    if "GROQ_API_KEY" in st.secrets:
        groq_api_key = st.secrets["GROQ_API_KEY"]
    else:
        groq_api_key = st.text_input("Groq API Key", type="password")

    if "TAVILY_API_KEY" in st.secrets:
        tavily_api_key = st.secrets["TAVILY_API_KEY"]
    else:
        tavily_api_key = st.text_input("Tavily API Key", type="password")

if not groq_api_key or not tavily_api_key:
    st.stop()

# 3. LLM (CEREBRO)
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile",
    temperature=0.7
)

# 4. HERRAMIENTA DE BÚSQUEDA (Simple Wrapper)
def search_tavily(query):
    try:
        client = TavilyClient(api_key=tavily_api_key)
        return client.search(query=query, search_depth="basic", max_results=3)
    except Exception as e:
        return f"Error: {e}"

# En CrewAI 0.28, las herramientas son simples objetos Tool de LangChain
search_tool = Tool(
    name="Web Search",
    func=search_tavily,
    description="Useful to search the internet for news and facts."
)

# 5. CREACIÓN DEL EQUIPO
def create_crew(topic):
    
    # Agente 1: Investigador
    researcher = Agent(
        role='Senior Research Analyst',
        goal=f'Find latest news about {topic}',
        backstory="Expert analyst who loves facts and statistics.",
        verbose=True,
        allow_delegation=False,
        tools=[search_tool],
        llm=llm # <--- IMPORTANTE: Asignamos Groq aquí
    )

    # Agente 2: Escritor
    writer = Agent(
        role='Tech Blogger',
        goal='Write a blog post',
        backstory="Famous writer who simplifies complex topics.",
        verbose=True,
        allow_delegation=False,
        llm=llm # <--- IMPORTANTE: Asignamos Groq aquí
    )

    # Tareas
    task1 = Task(
        description=f"Search for '{topic}'. Find key trends.",
        expected_output="A summary report.",
        agent=researcher
    )

    task2 = Task(
        description="Write a blog post based on the research.",
        expected_output="A markdown blog post.",
        agent=writer
    )

    # Equipo
    crew = Crew(
        agents=[researcher, writer],
        tasks=[task1, task2],
        verbose=True
        # En la versión 0.28.8 no hace falta desactivar memoria explícitamente si no se usa
    )

    return crew

# 6. INTERFAZ
topic = st.text_input("Topic:", placeholder="e.g. AI Agents")

if st.button("🚀 Start Research"):
    if topic:
        with st.spinner("Agents are working..."):
            try:
                my_crew = create_crew(topic)
                result = my_crew.kickoff()
                st.markdown("## Result")
                st.markdown(result)
            except Exception as e:
                st.error(f"Error: {e}")
