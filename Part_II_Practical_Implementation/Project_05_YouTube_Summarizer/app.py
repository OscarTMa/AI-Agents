import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

st.set_page_config(page_title="YouTube AI Assistant", page_icon="📺", layout="centered")

st.title("📺 Project 05: YouTube Summarizer & Chat")
st.caption("Powered by Groq (Llama 3.3) - Extract wisdom from videos instantly.")

# --- 1. CONFIGURACIÓN ---
with st.sidebar:
    st.header("Configuration")
    if "GROQ_API_KEY" in st.secrets:
        groq_api_key = st.secrets["GROQ_API_KEY"]
        st.success("API Key loaded!", icon="✅")
    else:
        groq_api_key = st.text_input("Groq API Key", type="password")

    st.markdown("---")
    st.markdown("### How to use")
    st.markdown("1. Paste a YouTube URL.")
    st.markdown("2. If auto-extraction fails (due to cloud blocking), paste text manually.")
    st.markdown("3. Choose an action.")

# --- 2. FUNCIONES DE UTILIDAD ---

def get_video_id(url):
    """Extrae el ID del video de varias formas de URL de YouTube"""
    try:
        query = urlparse(url)
        if query.hostname == 'youtu.be':
            return query.path[1:]
        if query.hostname in ('www.youtube.com', 'youtube.com'):
            if query.path == '/watch':
                p = parse_qs(query.query)
                return p['v'][0]
            if query.path[:7] == '/embed/':
                return query.path.split('/')[2]
            if query.path[:3] == '/v/':
                return query.path.split('/')[2]
    except:
        return None
    return None

def get_transcript(video_id):
    """Obtiene subtítulos con lógica de reintento y traducción"""
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        # Priorizar inglés o español
        try:
            transcript = transcript_list.find_transcript(['en', 'es', 'en-US', 'es-419'])
        except:
            transcript = next(iter(transcript_list)) # Fallback a cualquier idioma
        
        # Traducir a inglés si es necesario para Llama 3
        if not transcript.language_code.startswith('en'):
            transcript = transcript.translate('en')

        transcript_pieces = transcript.fetch()
        return " ".join([item['text'] for item in transcript_pieces])
    except Exception as e:
        # Devolvemos None para activar el modo manual en la UI
        return None 

def analyze_video(text, action, api_key):
    llm = ChatGroq(
        groq_api_key=api_key, 
        model_name="llama-3.3-70b-versatile",
        temperature=0.3
    )

    if action == "Summarize":
        template = """
        You are an expert summarizer. 
        Read the following YouTube video transcript and provide a concise summary.
        Include the main topic, key arguments, and the conclusion.
        
        TRANSCRIPT:
        {text}
        """
    elif action == "Key Points":
        template = """
        Read the transcript and extract the top 5-7 actionable key takeaways.
        Use emojis for each bullet point.
        
        TRANSCRIPT:
        {text}
        """
    elif action == "Quiz Me":
        template = """
        Generate a 3-question multiple choice quiz based on the transcript.
        Provide the answer key at the bottom.
        
        TRANSCRIPT:
        {text}
        """
    
    prompt = PromptTemplate(template=template, input_variables=["text"])
    chain = prompt | llm
    return chain.invoke({"text": text}).content

# --- 3. INTERFAZ DE USUARIO ---

youtube_url = st.text_input("Paste YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

# Inicializar estado de sesión
if "transcript" not in st.session_state:
    st.session_state.transcript = None

if youtube_url and groq_api_key:
    video_id = get_video_id(youtube_url)
    
    if video_id:
        st.video(youtube_url)
        
        # Botón principal de carga
        if st.button("📥 Try Auto-Extract Transcript"):
            with st.spinner("Connecting to YouTube..."):
                text = get_transcript(video_id)
                if text:
                    st.session_state.transcript = text
                    st.success("Success! Transcript extracted.")
                else:
                    st.session_state.transcript = None # Reset
                    st.error("⚠️ YouTube blocked the automated connection (common in Cloud Demos).")
                    st.info("💡 Solution: Copy the transcript from YouTube (Show Transcript) and paste it below.")

        # --- SECCIÓN DE FALLBACK MANUAL ---
        # Si falla la auto-extracción, mostramos este campo
        if st.session_state.transcript is None:
            manual_text = st.text_area("Or paste transcript manually here:", height=200)
            if manual_text:
                st.session_state.transcript = manual_text
                st.success("Manual transcript loaded!")

        # --- ACCIONES DEL AGENTE (Solo si hay texto) ---
        if st.session_state.transcript:
            st.markdown("### 🤖 Agent Actions")
            col1, col2, col3 = st.columns(3)
            
            action = None
            if col1.button("📝 Summarize"): action = "Summarize"
            if col2.button("🔑 Key Points"): action = "Key Points"
            if col3.button("❓ Quiz Me"): action = "Quiz Me"
            
            if action:
                with st.spinner(f"Generating {action}..."):
                    result = analyze_video(st.session_state.transcript, action, groq_api_key)
                    st.markdown("---")
                    st.markdown(result)

    else:
        st.error("Invalid YouTube URL")
