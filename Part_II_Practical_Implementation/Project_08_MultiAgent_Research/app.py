import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from langchain_groq import ChatGroq
from pydantic import Field
from tavily import TavilyClient

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="AI Research Team", page_icon="👥", layout="wide")
st.title("👥 Project 08: Multi-Agent Research Team")

# 2. SIDEBAR DE CREDENCIALES
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

# --- 🧠 EL TRUCO MAESTRO (REROUTING) ---
# Redirigimos cualquier llamada interna de OpenAI hacia Groq.
os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
os.environ["OPENAI_MODEL_NAME"] = "llama-3.3-70b-versatile"
os.environ["OPENAI_API_KEY"] = groq_api_key # Usamos la clave de Groq como si fuera de OpenAI
# ---------------------------------------

# 3. DEFINICIÓN DEL LLM (Explícito)
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile",
    temperature=0.7
)

# 4. HERRAMIENTA NATIVA
class TavilySearchTool(BaseTool):
    name: str = "Web Search Tool"
    description: str = "Useful for searching the internet to find up-to-date information."
    api_key: str = Field(..., description="Tavily API Key")

    def _run(self, query: str) -> str:
        try:
            client = TavilyClient(api_key=self.api_key)
            response = client.search(query=query, search_depth="basic", max_results=3)
            return str(response)
        except Exception as e:
            return f"Error: {e}"

search_tool = TavilySearchTool(api_key=tavily_api_key)

# 5. CREACIÓN DEL EQUIPO
def create_crew(topic):
    
    # Agente 1: Investigador
    researcher = Agent(
        role='Senior Research Analyst',
        goal=f'Uncover cutting-edge developments in {topic}',
        backstory="You are an expert analyst. You dig deep into the internet for facts.",
        verbose=True,
        allow_delegation=False,
        tools=[search_tool],
        llm=llm
    )

    # Agente 2: Escritor
    writer = Agent(
        role='Tech Content Strategist',
        goal='Write a compelling blog post',
        backstory="You are a famous tech blogger. You turn research into engaging stories.",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    # Tareas
    task1 = Task(
        description=f"Research about '{topic}'. Identify trends and news.",
        expected_output="A research report with bullet points.",
        agent=researcher
    )

    task2 = Task(
        description="Write a blog post based on the research report in Markdown.",
        expected_output="A blog post formatted in Markdown.",
        agent=writer
    )

    # Equipo
    crew = Crew(
        agents=[researcher, writer],
        tasks=[task1, task2],
        process=Process.sequential,
        verbose=True,
        memory=False, # Importante mantener desactivado
        manager_llm=llm # Forzamos al manager a usar Groq también
    )

    return crew

# 6. INTERFAZ
topic = st.text_input("Enter a topic:", placeholder="e.g., Quantum Computing")

if st.button("🚀 Launch Crew"):
    if topic:
        with st.spinner("🤖 The crew is working... (Approx 60s)"):
            try:
                # Contenedor para mostrar logs (opcional, para ver que está vivo)
                log_container = st.empty()
                log_container.info("🕵️ Researcher is starting...")
                
                my_crew = create_crew(topic)
                result = my_crew.kickoff()
                
                log_container.empty()
                st.success("Mission Complete!")
                st.markdown("## 📝 Result")
                st.markdown(result)
            except Exception as e:
                st.error(f"Error: {e}")
