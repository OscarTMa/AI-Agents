import streamlit as st
from PIL import Image
import google.generativeai as genai

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Vision Analyst", page_icon="👁️", layout="centered")

st.title("👁️ Project 10: Vision Analyst (Gemini)")
st.caption("Powered by Google Gemini 1.5 Flash")

# 2. CREDENCIALES
with st.sidebar:
    st.header("Credentials")
    # Intentamos leer de secrets o input manual
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
    else:
        api_key = st.text_input("Google API Key", type="password")
    
    st.info("Get your key at: aistudio.google.com")

if not api_key:
    st.warning("Please enter your Google API Key.")
    st.stop()

# Configurar el cliente de Google
genai.configure(api_key=api_key)

# 3. FUNCIÓN DE ANÁLISIS
def analyze_image(image, prompt):
    """
    Envía la imagen (objeto PIL) y el prompt a Gemini Flash.
    """
    try:
        # CAMBIO: Usamos 'gemini-1.5-flash-latest' que suele ser más robusto
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # Generamos contenido (Multimodal: Texto + Imagen)
        response = model.generate_content([prompt, image])
        
        return response.text
    except Exception as e:
        return f"Error analyzing image: {e}"

# 4. INTERFAZ DE USUARIO

uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Cargar y mostrar imagen
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    st.markdown("### 🔍 Ask Gemini")
    
    col1, col2, col3 = st.columns(3)
    prompt = None
    
    if col1.button("📄 Describe"):
        prompt = "Describe this image in detail."
    
    if col2.button("📊 Extract JSON"):
        prompt = "Extract all visible text/data. Return ONLY valid JSON."
        
    if col3.button("💰 Invoice"):
        prompt = "Extract Vendor, Date, and Total Amount from this invoice."

    custom_prompt = st.chat_input("Ask something specific...")
    if custom_prompt:
        prompt = custom_prompt

    if prompt:
        with st.spinner("Gemini is looking..."):
            response = analyze_image(image, prompt)
            st.markdown("---")
            st.success("Analysis Complete")
            st.markdown(response)
