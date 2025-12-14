import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults

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

# 3. DEFINICIÓN DEL LLM Y HERRAMIENTAS
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile",
    temperature=0.7
)

# Herramienta de búsqueda (Le damos capacidad de buscar en la web)
search_tool = TavilySearchResults(tavily_api_key=tavily_api_key, max_results=3)

# 4. DEFINICIÓN DE AGENTES (LOS EMPLEADOS)

def create_crew(topic):
    # --- Agente 1: El Investigador Senior ---
    researcher = Agent(
        role='Senior Research Analyst',
        goal=f'Uncover cutting-edge developments in {topic}',
        backstory="""You are an expert analyst at a top tech think tank.
        Your job is to dig deep into the internet to find the latest news,
        statistics, and trends. You hate vague information; you want facts.""",
        verbose=True,
        allow_delegation=False,
        tools=[search_tool], # Le damos la herramienta de búsqueda
        llm=llm
    )

    # --- Agente 2: El Escritor Técnico ---
    writer = Agent(
        role='Tech Content Strategist',
        goal='Write a compelling blog post based on the research',
        backstory="""You are a famous tech blogger known for simplifying complex topics.
        You take dry research reports and turn them into engaging narratives.
        You format everything in beautiful Markdown.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    # 5. DEFINICIÓN DE TAREAS (EL TRABAJO)
    
    task1 = Task(
        description=f"""Conduct a comprehensive research about '{topic}'.
        Identify key trends, latest news, and potential future impacts.
        Compile your findings into a detailed summary.""",
        expected_output="A detailed research report with bullet points and sources.",
        agent=researcher
    )

    task2 = Task(
        description="""Using the research report provided, write a high-quality blog post.
        The post should have an engaging title, an introduction, main body sections, and a conclusion.
        Use markdown formatting (## Headers, **Bold**, etc).""",
        expected_output="A full blog post in Markdown format.",
        agent=writer
    )

    # 6. EL EQUIPO (CREW)
    crew = Crew(
        agents=[researcher, writer],
        tasks=[task1, task2],
        process=Process.sequential, # Secuencial: Primero investiga, luego escribe
        verbose=True
    )

    return crew

# 7. INTERFAZ DE USUARIO

topic = st.text_input("Enter a topic to research:", placeholder="e.g., The Future of AI Agents in 2025")

if st.button("🚀 Launch Crew"):
    if topic:
        with st.spinner("🤖 The crew is working... (This may take a minute)"):
            try:
                # Inicializar y ejecutar
                my_crew = create_crew(topic)
                result = my_crew.kickoff()
                
                st.success("Mission Complete!")
                st.markdown("## 📝 Final Blog Post")
                st.markdown(result)
                
                with st.expander("See raw output"):
                    st.write(result)
            except Exception as e:
                st.error(f"Error during execution: {e}")
    else:
        st.error("Please enter a topic.")
