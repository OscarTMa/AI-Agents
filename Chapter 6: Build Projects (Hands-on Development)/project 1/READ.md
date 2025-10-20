## 🔍 **Project 1: Research Agent**

### 🎯 Objective

Build an AI agent capable of:
- Searching information online  
- Summarizing the results  
- Returning a structured, concise answer  

---

### 🧠 Architecture


---

### 🧰 Tech Stack

| Tool | Purpose |
|------|----------|
| **LangChain** | Agent orchestration and chaining |
| **OpenAI / Mistral** | Language model for summarization |
| **SerpAPI** | External search tool for real-time web info |
| **Streamlit** | Frontend interface |
| **Docker** | Containerization and deployment |

---

### ⚙️ Key Implementation Steps

1. **Create the LangChain flow using `initialize_agent()`**  
2. **Integrate the SerpAPI search tool**  
3. **Add a summarization module using `LLMChain` and a custom prompt**  
4. **Build a simple Streamlit web interface**  
5. **Containerize with Docker for deployment**

---

### 🖥️ **Streamlit App Code**

```python
# app.py
import streamlit as st
from langchain.agents import initialize_agent, load_tools
from langchain.llms import OpenAI

# Initialize model and tools
llm = OpenAI(temperature=0.3)
tools = load_tools(["serpapi"], llm=llm)
agent = initialize_agent(tools, llm, agent_type="zero-shot-react-description")

# Streamlit UI
st.title("🔍 Research Agent")
query = st.text_input("Ask your research question")

if query:
    with st.spinner("Searching and summarizing..."):
        response = agent.run(query)
        st.success("✅ Done!")
        st.write(response)

````
## ☁️ Deployment

### 🧱 Build the Docker image                     

```bash
docker build -t research-agent .
````

### 🧩 Run the container locally                                        

```bash
docker run -p 8501:8501 research-agent
```

### 🌐 Access the web interface                             

```bash
http://localhost:8501
````
### 🚀 (Optional) Deploy to

- Streamlit Cloud
- AWS ECS / Google Cloud Run
- Kubernetes cluster for scalable orchestration
