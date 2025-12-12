import streamlit as st
import pandas as pd
from utils import execute_pandas_code

st.set_page_config(page_title="CSV Data Analyst", page_icon="📊")

st.title("📊 Project 02: CSV Analyst Agent (Groq)")
st.caption("I can analyze your data by writing Python code automatically.")

# 1. Sidebar Config
with st.sidebar:
    st.header("Configuration")
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
        st.success("API Key loaded from secrets")
    else:
        api_key = st.text_input("Groq API Key", type="password")

# 2. File Uploader
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file:
    # Load Data
    df = pd.read_csv(uploaded_file)
    st.write("### Data Preview")
    st.dataframe(df.head())

    # 3. Analysis Interface
    query = st.text_area("Ask a question about your data:", 
                         placeholder="e.g., What is the average Salary? or Show me the top 3 oldest employees.")
    
    if st.button("Analyze"):
        if not api_key:
            st.error("Please provide an API Key.")
            st.stop()
            
        with st.spinner("🤖 Generating pandas code and calculating..."):
            result, code = execute_pandas_code(df, query, api_key)
            
            # 4. Display Results
            st.subheader("💡 Answer:")
            st.write(result)
            
            with st.expander("See the code I wrote"):
                st.code(code, language="python")

else:
    st.info("Please upload a CSV file to begin.")
