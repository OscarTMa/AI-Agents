import streamlit as st
from PIL import Image
import google.generativeai as genai

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Vision Analyst", page_icon="👁️", layout="centered")

st.title("👁️ Project 10: Vision Analyst (Smart)")
st.caption("Powered by Google Gemini (Auto-Detect Model)")

# 2. CREDENCIALES
with st.sidebar:
    st.header("Credentials")
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
    else:
        api_key = st.text_input("Google API Key", type="password")
    
    st.markdown("---")
    st.subheader("🛠️ Diagnostics")
    
    # Variable para guardar el modelo seleccionado automáticamente
    selected_model_name = None

if not api_key:
    st.warning("Please enter your Google API Key.")
    st.stop()

# Configurar cliente
try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Error configuring API: {e}")
    st.stop()

# 3. LÓGICA DE AUTO-SELECCIÓN DE MODELO
def find_vision_model():
    """Busca automáticamente un modelo capaz de ver imágenes."""
    try:
        models = list(genai.list_models())
        vision_models = []
        
        # Filtramos modelos que soporten 'generateContent' y sean de visión
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                # Prioridad 1: Flash (Rápido y barato)
                if 'flash' in m.name:
                    return m.name
                # Prioridad 2: Pro Vision (Legacy pero robusto)
                if 'vision' in m.name:
                    vision_models.append(m.name)
                # Prioridad 3: Gemini 1.5 Pro (Potente)
                if 'gemini-1.5-pro' in m.name:
                    vision_models.append(m.name)
        
        # Si encontramos alguno de visión en la lista secundaria, usamos el primero
        if vision_models:
            return vision_models[0]
            
        # Fallback manual si la lista falla
        return "models/gemini-1.5-flash"
        
    except Exception as e:
        st.sidebar.error(f"Error listing models: {e}")
        return "gemini-1.5-flash"

# Ejecutamos la búsqueda
selected_model_name = find_vision_model()

with st.sidebar:
    st.success(f"✅ Model Active:\n`{selected_model_name}`")

# 4. FUNCIÓN DE ANÁLISIS
def analyze_image(image, prompt):
    try:
        # Usamos el modelo que encontramos dinámicamente
        model = genai.GenerativeModel(selected_model_name)
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"Error analyzing image: {e}"

# 5. INTERFAZ DE USUARIO
uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    st.markdown("### 🔍 Ask Gemini")
    
    col1, col2 = st.columns(2)
    prompt = None
    
    if col1.button("📄 Describe Image"):
        prompt = "Describe this image in detail."
    
    if col2.button("📊 Extract Data (JSON)"):
        prompt = "Extract all visible text and data. Return ONLY valid JSON."

    custom_prompt = st.chat_input("Ask something specific...")
    if custom_prompt:
        prompt = custom_prompt

    if prompt:
        with st.spinner(f"Analyzing with {selected_model_name}..."):
            response = analyze_image(image, prompt)
            st.markdown("---")
            st.success("Analysis Complete")
            st.markdown(response)
