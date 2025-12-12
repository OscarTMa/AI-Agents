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
    st.markdown("2. Choose an action (Summary, Quiz, etc).")
    st.markdown("3. Let AI do the watching for you.")

# --- 2. FUNCIONES DE UTILIDAD ---

def get_video_id(url):
    """Extrae el ID del video de varias formas de URL de YouTube"""
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
    return None

def get_transcript(video_id):
    """
    Obtiene subtítulos. Si no hay en inglés, busca cualquiera y lo traduce.
    """
    try:
        # 1. Obtener la lista de transcriptores disponibles (manuales y auto)
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # 2. Lógica de prioridad:
        # Intentamos buscar inglés manual o autogenerado
        try:
            transcript = transcript_list.find_transcript(['en', 'en-US', 'es', 'es-419'])
        except:
            # Si falla, tomamos el PRIMERO que exista (cualquier idioma)
            transcript = next(iter(transcript_list))
        
        # 3. Traducir si es necesario (para que Llama 3 entienda mejor)
        # Si el idioma no es inglés, lo traducimos a inglés
        if not transcript.language_code.startswith('en'):
            transcript = transcript.translate('en')

        # 4. Descargar y formatear
        transcript_pieces = transcript.fetch()
        full_text = " ".join([item['text'] for item in transcript_pieces])
        
        return full_text

    except Exception as e:
        # Esto ocurre si el video está bloqueado o NO tiene ningún subtítulo
        print(f"Error: {e}") 
        return None

# --- 3. LÓGICA DEL AGENTE ---

def analyze_video(text, action, api_key):
    llm = ChatGroq(
        groq_api_key=api_key, 
        model_name="llama-3.3-70b-versatile",
        temperature=0.3
    )

    # Definir prompts según la acción
    if action == "Summarize":
        template = """
        You are an expert summarizer. 
        Read the following YouTube video transcript and provide a concise summary.
        Include the main topic, key arguments, and the conclusion.
        Format it nicely with Markdown.
        
        TRANSCRIPT:
        {text}
        """
    elif action == "Key Points":
        template = """
        Read the transcript and extract the top 5-7 actionable key takeaways or bullet points.
        Use emojis for each bullet point.
        
        TRANSCRIPT:
        {text}
        """
    elif action == "Quiz Me":
        template = """
        Based on the transcript, generate a 3-question multiple choice quiz to test my understanding.
        Provide the answer key at the very bottom (hidden).
        
        TRANSCRIPT:
        {text}
        """
    
    prompt = PromptTemplate(template=template, input_variables=["text"])
    chain = prompt | llm
    
    return chain.invoke({"text": text}).content

# --- 4. INTERFAZ DE USUARIO ---

youtube_url = st.text_input("Paste YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

if youtube_url and groq_api_key:
    video_id = get_video_id(youtube_url)
    
    if video_id:
        # Mostrar el video
        st.video(youtube_url)
        
        # Botón para procesar
        if "transcript" not in st.session_state:
            st.session_state.transcript = None

        if st.button("📥 Load Transcript"):
            with st.spinner("Extracting subtitles..."):
                text = get_transcript(video_id)
                if text:
                    st.session_state.transcript = text
                    st.success(f"Transcript loaded! ({len(text)} characters)")
                else:
                    st.error("Could not find subtitles for this video. (Note: Auto-generated subs work, but video must have them).")

        # Si ya tenemos la transcripción, mostramos las opciones del Agente
        if st.session_state.transcript:
            st.markdown("### 🤖 Agent Actions")
            col1, col2, col3 = st.columns(3)
            
            action = None
            if col1.button("📝 Summarize"):
                action = "Summarize"
            if col2.button("🔑 Key Points"):
                action = "Key Points"
            if col3.button("❓ Quiz Me"):
                action = "Quiz Me"
            
            if action:
                with st.spinner(f"Generating {action}..."):
                    result = analyze_video(st.session_state.transcript, action, groq_api_key)
                    st.markdown("---")
                    st.markdown(result)
                    
                    # Opción para ver la transcripción cruda
                    with st.expander("See raw transcript"):
                        st.write(st.session_state.transcript)

    else:
        st.error("Invalid YouTube URL")

elif not groq_api_key:
    st.info("Please enter your API Key to start.")
