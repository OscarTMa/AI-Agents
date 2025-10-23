# 🧩 Project 1: CSV Data Q&A Agent

## 🎯 Objective
Develop an intelligent agent capable of answering natural language questions from CSV data.

## 🧠 Architecture
User → LLM → CSVLoader → Pandas DataFrame → Answer

## 🧰 Stack
- Python 3.10+
- LangChain
- OpenAI API
- Pandas

## ⚙️ Steps

1. Load your CSV file:
```python
from langchain.document_loaders import CSVLoader
loader = CSVLoader(file_path='data.csv')
data = loader.load()
```

2. Initialize the agent:

```python

from langchain.agents import create_csv_agent
from langchain.llms import OpenAI

agent = create_csv_agent(OpenAI(temperature=0), 'data.csv', verbose=True)
```

3. Ask questions:

```python
response = agent.run("What is the average salary?")
print(response)
```

## ☁️ Deployment
You can deploy this as a simple Streamlit app:

```bash
streamlit run app.py
```

Or containerize it:

```bash
docker build -t csv-agent .
docker run -p 8501:8501 csv-agent
```

## 📦 Folder Structure
```bash
/projects/data_agent/
    ├── README.md
    ├── app.py
    ├── utils.py
    ├── requirements.txt
    └── example.csv
```
## 🧭 Explanation of the Code

|File|	Description|
|----------|--------------|
|app.py	|The main Streamlit web application. Handles file upload, question input, and response display.|
|utils.py	|Helper functions, e.g., saving temporary files.|
|requirements.txt	|All Python dependencies required to run the agent.|
|.env	|Contains your OpenAI API key for authentication.|
|example.csv	|A sample dataset for quick testing.|

## Key Learnings
- Using LangChain CSV Agent
- Implementing LLM reasoning over structured data
- Designing a Streamlit UI for interaction
- Optional: Deploying with Docker

## 🚀 Optional Enhancements
- Add memory using ConversationBufferMemory (LangChain)
- Integrate Pinecone for persistent embeddings
- Deploy the container to AWS ECS or Streamlit Cloud

##  🧠 Exemples of questions
- What is the average salary of employees?
- Who are the employees in the Engineering department?
- Which department has the highest average salary?
- Who has more than 5 years of experience?
- What is the total salary cost for the Marketing team?
- List all employees working in Chicago.














