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

## 📦 Example Folder Structure
```bash
/projects/data_agent/
    ├── README.md
    ├── app.py
    ├── utils.py
    ├── requirements.txt
    └── example.csv
```
