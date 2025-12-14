import streamlit as st
import base64
from groq import Groq
from PIL import Image
import io

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Vision Analyst", page_icon="👁️", layout="centered")

st.title("👁️ Project 10: Vision Analyst")
st.caption("Powered by Groq (Llama 3.2 Vision). Upload an image and ask questions.")

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

# 3. FUNCIONES UTILITARIAS

def encode_image(image_file):
    """
    Convierte la imagen subida a formato Base64 para enviarla a la API.
    """
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

def analyze_image(base64_image, prompt):
    """
    Envía la imagen y la pregunta al modelo de visión.
    """
    try:
        completion = client.chat.completions.create(
            # Usamos el modelo específico de visión de Llama 3.2
            model="llama-3.2-11b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.1, # Temperatura baja para ser precisos analizando
            max_tokens=1024,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error analyzing image: {e}"

# 4. INTERFAZ DE USUARIO

# Subida de imagen
uploaded_file = st.file_uploader("Upload an image (Invoice, Chart, Photo)...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Mostrar la imagen
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Opciones de análisis predefinidas
    st.markdown("### 🔍 What do you want to know?")
    
    col1, col2, col3 = st.columns(3)
    prompt = None
    
    if col1.button("📄 Describe Image"):
        prompt = "Describe this image in detail. Be specific about visual elements."
    
    if col2.button("📊 Extract Data (JSON)"):
        prompt = "Extract all visible text and data from this image. Return ONLY a valid JSON format. Do not write explanations."
        
    if col3.button("💰 Analyze Invoice"):
        prompt = "This is an invoice. Extract the Vendor Name, Total Amount, and Date. Suggest a categorization for this expense."

    # Campo de texto libre
    custom_prompt = st.chat_input("Or ask a specific question about the image...")
    if custom_prompt:
        prompt = custom_prompt

    # Ejecutar análisis
    if prompt:
        with st.spinner("Analyzing pixels..."):
            # 1. Codificar
            base64_image = encode_image(uploaded_file)
            # 2. Enviar a IA
            response = analyze_image(base64_image, prompt)
            
            st.markdown("---")
            st.success("Analysis Complete")
            st.markdown(response)
