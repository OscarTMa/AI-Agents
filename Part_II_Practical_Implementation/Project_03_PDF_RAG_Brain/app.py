import os
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
# Importación directa desde langchain.chains
from langchain.chains import RetrievalQA

# Configuración de página
st.set_page_config(page_title="PDF RAG Brain", page_icon="🧠")

st.title("🧠 Project 03: Chat with PDF (RAG)")
st.caption("Powered by Groq (Llama 3.3) & HuggingFace Embeddings (Free)")

# --- 1. CONFIGURACIÓN LATERAL ---
with st.sidebar:
    st.header("Configuration")
    
    # API Key de Groq
    if "GROQ_API_KEY" in st.secrets:
        groq_api_key = st.secrets["GROQ_API_KEY"]
        st.success("Groq API Key loaded!", icon="✅")
    else:
        groq_api_key = st.text_input("Groq API Key", type="password")
    
    st.markdown("---")
    st.info("This app runs locally using HuggingFace embeddings for privacy and zero cost.")

# --- 2. FUNCIONES DE BACKEND ---
@st.cache_resource
def get_vectorstore(file_path):
    """
    Procesa el PDF y crea la base de datos vectorial (FAISS).
    Usa @st.cache_resource para no recalcular si el archivo es el mismo.
    """
    # A. Cargar PDF
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    # B. Dividir texto (Chunks)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documents)
    
    # C. Crear Embeddings (Gratis / Local)
    # Usamos un modelo pequeño y rápido: all-MiniLM-L6-v2
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # D. Crear Vector Store
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore

def get_rag_chain(vectorstore, api_key):
    """
    Crea la cadena de RAG usando Groq como LLM.
    """
    # ⚠️  Usamos el modelo actualizado Llama 3.3
    llm = ChatGroq(
        groq_api_key=api_key, 
        model_name="llama-3.3-70b-versatile",
        temperature=0
    )
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )
    return qa_chain

# --- 3. INTERFAZ PRINCIPAL ---

# Estado de sesión para historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Subida de archivo
uploaded_file = st.file_uploader("Upload your PDF Document", type="pdf")

if uploaded_file and groq_api_key:
    # Guardar archivo temporalmente
    temp_file = "./temp.pdf"
    with open(temp_file, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    try:
        with st.spinner("🧠 Processing document (Embedding)..."):
            # Crear Base de Datos Vectorial
            vectorstore = get_vectorstore(temp_file)
            # Crear Cadena de RAG
            qa_chain = get_rag_chain(vectorstore, groq_api_key)
            st.success("Document processed! Ask questions below.")
            
        # Borrar archivo temporal (limpieza)
        if os.path.exists(temp_file):
            os.remove(temp_file)

        # Mostrar historial de chat
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Input de usuario
        if prompt := st.chat_input("Ask something about the PDF..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generar respuesta
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = qa_chain.run(prompt)
                    st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.error(f"Error: {e}")

elif not groq_api_key:
    st.warning("Please enter your Groq API Key in the sidebar.")
