import os
import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.experimental.csv.agent import create_csv_agent

# Set your OpenAI API Key
os.environ["OPENAI_API_KEY"] = "sk-your-key-here"  # Replace with your key

# CSV file path
csv_file = "example.csv"

# Create agent
agent = create_csv_agent(
    llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"),
    path=csv_file,
    verbose=True
)

# Interactive loop
while True:
    query = input("Ask a question about the CSV (or type 'exit'): ")
    if query.lower() in ["exit", "quit"]:
        break
    response = agent.run(query)
    print("Answer:", response)
