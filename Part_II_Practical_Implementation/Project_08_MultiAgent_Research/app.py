import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from pydantic import Field
from tavily import TavilyClient

# 1. CONFIGURACIÓN
st.set_page_config(page_title="AI Research Team", page_icon="👥", layout="wide")
st.title("👥 Project 08: AI Research Team (Modern)")

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

# --- 3. EL GRAN ENGAÑO (OPENAI MOCK) ---
# Las versiones nuevas de CrewAI insisten en usar OpenAI.
# Configuramos las variables de entorno para redirigir el tráfico a Groq.

os.environ["OPENAI_API_KEY"] = groq_api_key  # Usamos la clave de Groq
os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1" # Redirección
os.environ["OPENAI_MODEL_NAME"] = "llama-3.3-70b-versatile" # Modelo
# ---------------------------------------

# 4. HERRAMIENTA NATIVA (Para evitar errores de Pydantic)
class TavilySearchTool(BaseTool):
    name: str = "Web Search Tool"
    description: str = "Search the internet for up-to-date information."
    api_key: str = Field(..., description="Tavily API Key")

    def _run(self, query: str) -> str:
        try:
            client = TavilyClient(api_key=self.api_key)
            # Buscamos contexto básico
            return str(client.search(query=query, search_depth="basic", max_results=3))
        except Exception as e:
            return f"Error: {e}"

search_tool = TavilySearchTool(api_key=tavily_api_key)

# 5. DEFINICIÓN DEL EQUIPO
def create_crew(topic):
    
    # Nota: En CrewAI moderno, si configuras las variables de entorno OPENAI_*,
    # no necesitas pasar el 'llm' explícitamente, lo coge automático.

    researcher = Agent(
        role='Senior Researcher',
        goal=f'Find facts about {topic}',
        backstory="You are an expert analyst who loves facts and statistics.",
        verbose=True,
        tools=[search_tool],
        allow_delegation=False
    )

    writer = Agent(
        role='Tech Writer',
        goal='Write a blog post',
        backstory="You convert complex data into engaging stories.",
        verbose=True,
        allow_delegation=False
    )

    task1 = Task(
        description=f"Research '{topic}'. Find key trends.",
        expected_output="A summary report with 5 bullet points.",
        agent=researcher
    )

    task2 = Task(
        description="Write a short blog post based on the research.",
        expected_output="A markdown blog post.",
        agent=writer
    )

    crew = Crew(
        agents=[researcher, writer],
        tasks=[task1, task2],
        verbose=True
    )

    return crew

# 6. INTERFAZ
topic = st.text_input("Topic:", placeholder="e.g. Agents in 2025")

if st.button("🚀 Launch"):
    if topic:
        with st.spinner("Crew is working..."):
            try:
                my_crew = create_crew(topic)
                result = my_crew.kickoff()
                st.markdown("## Result")
                st.markdown(result)
            except Exception as e:
                st.error(f"Error: {e}")
