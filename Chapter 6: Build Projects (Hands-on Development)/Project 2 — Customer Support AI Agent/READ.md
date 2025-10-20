# 🤖 Project 2 — Customer Support AI Agent

## 🎯 Objective
Build an intelligent customer service chatbot capable of understanding user queries, retrieving answers from a company knowledge base, and providing contextual responses.

---

## 🧠 Architecture
User → FastAPI Endpoint → LangChain LLM → Vector Database (Chroma) → Response Generator

---

## 🧰 Tech Stack
- **Python**
- **LangChain**
- **FastAPI**
- **Chroma / FAISS**
- **OpenAI API**

---

## ⚙️ Implementation Steps

### 1️⃣ Set up the project                                      
```bash
mkdir customer-support-agent
cd customer-support-agent
pip install fastapi uvicorn langchain openai chromadb python-dotenv
````
### 2️⃣ Create the main API file                                                

```python
main.py

from fastapi import FastAPI, Request
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

app = FastAPI()

embeddings = OpenAIEmbeddings()
db = Chroma(persist_directory="./data", embedding_function=embeddings)
retriever = db.as_retriever()

qa = RetrievalQA.from_chain_type(
    llm=OpenAI(temperature=0.6),
    retriever=retriever
)

@app.post("/chat")
async def chat(req: Request):
    data = await req.json()
    query = data.get("question")
    answer = qa.run(query)
    return {"response": answer}
````

### 3️⃣ Run locally                  

````python
uvicorn main:app --reload
````
## ☁️ Deployment

Use Docker or deploy directly to AWS Lambda, Render, or Google Cloud Run.

````bash
docker build -t customer-support-agent .
docker run -p 8000:8000 customer-support-agent
````

### ✅ Expected Output

Conversational, context-aware responses.

Real-time question answering using company data.

Scalable FastAPI microservice for integration in websites or apps.

