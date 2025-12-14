import streamlit as st
import os
from groq import Groq
from gtts import gTTS
import tempfile

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Voice Assistant", page_icon="🎙️")

st.title("🎙️ Project 09: Talking Llama")
st.caption("Powered by Groq (Whisper + Llama 3) & Google TTS")

# 2. CREDENCIALES
with st.sidebar:
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
    else:
        api_key = st.text_input("Groq API Key", type="password")

if not api_key:
    st.warning("Please enter your Groq API Key.")
    st.stop()

client = Groq(api_key=api_key)

# 3. FUNCIONES DE PROCESAMIENTO

def transcribe_audio(audio_file):
    """Convierte audio a texto usando Whisper en Groq"""
    try:
        transcription = client.audio.transcriptions.create(
            file=(audio_file.name, audio_file, "audio/wav"), # Formato requerido
            model="distil-whisper-large-v3-en", # Modelo súper rápido
            response_format="json",
            language="en", # Forzamos inglés para mejor precisión (puedes cambiar a 'es')
            temperature=0.0
        )
        return transcription.text
    except Exception as e:
        st.error(f"Error transcribing: {e}")
        return None

def get_llm_response(text):
    """Obtiene respuesta inteligente de Llama 3"""
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful voice assistant. Keep your answers concise and conversational (max 2 sentences)."},
                {"role": "user", "content": text}
            ],
            temperature=0.5,
            max_tokens=1024,
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error getting LLM response: {e}")
        return None

def text_to_speech(text):
    """Convierte la respuesta de texto a audio MP3"""
    try:
        # Usamos gTTS (Google Text-to-Speech)
        tts = gTTS(text=text, lang='en', slow=False)
        
        # Guardar en archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            return fp.name
    except Exception as e:
        st.error(f"Error generating audio: {e}")
        return None

# 4. INTERFAZ DE USUARIO

st.subheader("Start talking...")

# Widget nativo de grabación de Streamlit
audio_value = st.audio_input("Record a voice message")

if audio_value:
    st.audio(audio_value) # Reproducir lo que grabaste para confirmar

    with st.spinner("👂 Listening & Thinking..."):
        # A. Transcribir
        text_input = transcribe_audio(audio_value)
        
        if text_input:
            st.success(f"You said: {text_input}")
            
            # B. Generar Respuesta IA
            ai_response = get_llm_response(text_input)
            
            if ai_response:
                st.info(f"AI: {ai_response}")
                
                # C. Hablar (TTS)
                audio_file_path = text_to_speech(ai_response)
                if audio_file_path:
                    st.audio(audio_file_path, format="audio/mp3", autoplay=True)
                    # Limpieza del archivo temporal
                    os.remove(audio_file_path)
