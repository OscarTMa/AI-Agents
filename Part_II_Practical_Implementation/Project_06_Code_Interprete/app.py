import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.tools import Tool
from langchain_experimental.utilities import PythonREPL
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain.callbacks import StreamlitCallbackHandler

st.set_page_config(page_title="Python Code Interpreter", page_icon="🐍", layout="wide")

st.title("🐍 Project 06: Python Code Interpreter")
st.caption("Powered by Groq (Llama 3.3) - I can solve math, logic, and plot graphs.")

# --- 1. CONFIGURACIÓN ---
with st.sidebar:
    st.header("Configuration")
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
        st.success("API Key loaded!", icon="✅")
    else:
        api_key = st.text_input("Groq API Key", type="password")
    
    st.info("💡 **Tip:** Ask me to 'Plot a sine wave' or 'Calculate the 100th Fibonacci number'.")

if not api_key:
    st.warning("Please enter your Groq API Key.")
    st.stop()

# --- 2. DEFINIR HERRAMIENTA DE EJECUCIÓN (REPL) ---
python_repl = PythonREPL()

def python_repl_wrapper(code: str):
    """
    Esta función envuelve la ejecución. 
    Intercepta intentos de graficar para asegurar que se guarden como imagen.
    """
    # Si el código usa matplotlib pero no guarda, forzamos el guardado
    if "plt.show()" in code:
        code = code.replace("plt.show()", "plt.savefig('plot.png')")
    
    try:
        result = python_repl.run(code)
        return f"Succesfully executed:\n{result}"
    except Exception as e:
        return f"Error executing code: {e}"

# Crear la Herramienta (Tool) que usará el Agente
repl_tool = Tool(
    name="python_repl",
    description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
    func=python_repl_wrapper
)

tools = [repl_tool]

# --- 3. AGENTE ---
llm = ChatGroq(
    groq_api_key=api_key, 
    model_name="llama-3.3-70b-versatile",
    temperature=0
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a Python Data Scientist. 
    You have access to a Python REPL to execute code.
    
    RULES:
    1. If asked to calculate something complex, WRITE CODE. Do not guess.
    2. If asked to plot/graph, use `matplotlib`.
    3. Always save figures to a file named 'plot.png' using `plt.savefig('plot.png')`.
    4. Provide the final answer in text based on the code output.
    """),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# --- 4. INTERFAZ DE CHAT ---

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "I am ready to write Python code for you. Try asking: 'Generate a histogram of 1000 random normal values'."}
    ]

# Mostrar historial
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
    # Si el mensaje tenía una imagen asociada (guardada en sesión), mostrarla
    if "image" in msg:
        st.image(msg["image"])

if user_input := st.chat_input("Write your request..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Limpiar gráfico anterior si existe
    if os.path.exists("plot.png"):
        os.remove("plot.png")

    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent_executor.invoke({"input": user_input}, {"callbacks": [st_callback]})
        
        output_text = response["output"]
        st.write(output_text)
        
        # Guardar en historial
        message_data = {"role": "assistant", "content": output_text}

        # Verificar si se generó un gráfico
        if os.path.exists("plot.png"):
            st.image("plot.png", caption="Generated Plot")
            message_data["image"] = "plot.png" # Guardar referencia para el historial
            
        st.session_state.messages.append(message_data)
