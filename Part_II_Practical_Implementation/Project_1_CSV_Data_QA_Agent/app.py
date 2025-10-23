import os
import streamlit as st
from dotenv import load_dotenv
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from utils import save_uploaded_file

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="CSV Data Q&A Agent", page_icon="🧠", layout="wide")

st.title("🧩 CSV Data Q&A Agent")
st.markdown("Ask questions directly from your CSV file using an AI Agent powered by **LangChain + OpenAI**.")

uploaded_file = st.file_uploader("📤 Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    csv_path = save_uploaded_file(uploaded_file)
    st.success(f"✅ File uploaded successfully: {uploaded_file.name}")

    # Initialize the agent
    agent = create_csv_agent(
        OpenAI(temperature=0, openai_api_key=openai_api_key),
        csv_path,
        verbose=True
    )

    # Input for natural language questions
    user_query = st.text_input("💬 Ask your question about the CSV data:")

    if user_query:
        with st.spinner("🤔 Thinking..."):
            try:
                response = agent.run(user_query)
                st.subheader("🧠 Response:")
                st.write(response)
            except Exception as e:
                st.error(f"❌ Error: {e}")

else:
    st.info("⬆️ Please upload a CSV file to begin.")
