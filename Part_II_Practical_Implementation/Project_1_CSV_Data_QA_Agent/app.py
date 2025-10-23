#  app.py
import os
import pandas as pd
from langchain.agents import create_csv_agent
from langchain.chat_models import ChatOpenAI

# -------------------------------
# Set your OpenAI API Key
# -------------------------------
os.environ["OPENAI_API_KEY"] = "sk-your-key-here"  # Reemplaza con tu clave

# -------------------------------
# CSV file path
# -------------------------------
csv_file = "example.csv"  # Asegúrate de tener tu CSV en la misma carpeta

# -------------------------------
# Create agent
# -------------------------------
# LangChain >0.2.0 usa 'create_csv_agent' desde langchain.agents.csv
# Si la versión actual no lo soporta, instalar langchain==0.0.267
agent = create_csv_agent(
    ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"),
    csv_file,
    verbose=True
)

# -------------------------------
# Run agent
# -------------------------------
while True:
    query = input("Ask a question about the CSV (or type 'exit'): ")
    if query.lower() in ["exit", "quit"]:
        print("Exiting agent.")
        break
    response = agent.run(query)
    print("Answer:", response)
