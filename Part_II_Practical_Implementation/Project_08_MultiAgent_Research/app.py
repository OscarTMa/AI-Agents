import streamlit as st
# Importamos os para el truco de la API Key
import os
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from langchain_groq import ChatGroq
from pydantic import Field
from tavily import TavilyClient

# --- TRUCO: Configurar una API Key falsa para callar la validación de OpenAI ---
# CrewAI a veces verifica que la variable exista aunque no la use.
os.environ["OPENAI_API_KEY"] = "NA"

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="AI Research Team", page_icon="👥", layout="wide")

st.title("👥 Project 08: Multi-Agent Research Team")
st.caption("Powered by CrewAI, Groq (Llama 3.3) & Tavily")

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
    st.warning("Please enter both API Keys to activate the Crew.")
    st.stop()

# 3. DEFINICIÓN DEL LLM
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile",
    temperature=0.7
)

# --- HERRAMIENTA NATIVA DE CREWAI ---
class TavilySearchTool(BaseTool):
    name: str = "Web Search Tool"
    description: str = "Useful for searching the internet to find up-to-date information, news, and trends."
    api_key: str = Field(..., description="Tavily API Key")

    def _run(self, query: str) -> str:
        try:
            client = TavilyClient(api_key=self.api_key)
            response = client.search(query=query, search_depth="basic", max_results=3)
            return str(response)
        except Exception as e:
            return f"Error searching: {e}"

search_tool = TavilySearchTool(api_key=tavily_api_key)

# 4. DEFINICIÓN DE AGENTES
def create_crew(topic):
    # Agente 1: Investigador
    researcher = Agent(
        role='Senior Research Analyst',
        goal=f'Uncover cutting-edge developments in {topic}',
        backstory="""You are an expert analyst. You dig deep into the internet 
        to find the latest news, statistics, and trends. You want facts.""",
        verbose=True,
        allow_delegation=False,
        tools=[search_tool],
        llm=llm
    )

    # Agente 2: Escritor
    writer = Agent(
        role='Tech Content Strategist',
        goal='Write a compelling blog post based on the research',
        backstory="""You are a famous tech blogger. You take dry research reports 
        and turn them into engaging narratives formatted in Markdown.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    # 5. TAREAS
    task1 = Task(
        description=f"""Conduct a comprehensive research about '{topic}'.
        Identify key trends, latest news, and potential future impacts.""",
        expected_output="A research report with bullet points and sources.",
        agent=researcher
    )

    task2 = Task(
        description="""Write a blog post based on the research report.
        Include a catchy title, intro, body, and conclusion in Markdown.""",
        expected_output="A blog post in Markdown format.",
        agent=writer
    )

    # 6. EQUIPO (FIX: Memory False)
    crew = Crew(
        agents=[researcher, writer],
        tasks=[task1, task2],
        process=Process.sequential,
        verbose=True,
        memory=False # <--- ESTO SOLUCIONA EL ERROR DE OPENAI
    )

    return crew

# 7. INTERFAZ
topic = st.text_input("Enter a topic:", placeholder="e.g., The Future of AI Agents")

if st.button("🚀 Launch Crew"):
    if topic:
        with st.spinner("🤖 The crew is working... (This may take 1-2 minutes)"):
            try:
                my_crew = create_crew(topic)
                result = my_crew.kickoff()
                st.success("Mission Complete!")
                st.markdown("## 📝 Final Blog Post")
                st.markdown(result)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.error("Please enter a topic.")
