import streamlit as st
import sys

# 1. CONFIGURACIÓN (Debe ser la primera línea ejecutada)
st.set_page_config(page_title="DocuVision AI", page_icon="👁️", layout="centered")

# --- ZONA DE DIAGNÓSTICO ---
status = st.empty()
status.info("🔄 Cargando sistema DocuVision...")

try:
    # Importamos librerías pesadas dentro de un bloque seguro
    import google.generativeai as genai
    from PIL import Image
    import pandas as pd
    import openpyxl # Esta suele ser la culpable
    import json
    import re
    import io
    status.success("✅ Librerías cargadas correctamente.")
    status.empty() # Borramos el mensaje si todo va bien
except Exception as e:
    st.error(f"❌ ERROR CRÍTICO DE IMPORTACIÓN: {e}")
    st.code(f"Detalle técnico: {sys.exc_info()}")
    st.stop()
# ---------------------------

st.title("👁️ DocuVision: Intelligent OCR")
st.caption("Powered by Google Gemini 1.5 Flash & Pandas")

# 2. CREDENCIALES
with st.sidebar:
    st.header("Credentials")
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
    else:
        api_key = st.text_input("Google API Key", type="password")

if not api_key:
    st.warning("Please enter your Google API Key.")
    st.stop()

# Configuración API
try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Error configuring API: {e}")

# 3. SELECCIÓN DE MODELO
def find_vision_model():
    try:
        models = list(genai.list_models())
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                if 'flash' in m.name: return m.name
        return "models/gemini-1.5-flash"
    except:
        return "models/gemini-1.5-flash"

selected_model_name = find_vision_model()

# 4. FUNCIONES
def analyze_image(image, prompt):
    try:
        model = genai.GenerativeModel(selected_model_name)
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"Error analyzing image: {e}"

def clean_json_text(text):
    """Limpia markdown de JSON"""
    try:
        pattern = r"```json(.*?)```"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text
    except:
        return text

# 5. INTERFAZ
uploaded_file = st.file_uploader("Upload Invoice/Document...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Preview", use_column_width=True)
    
    st.markdown("### ⚡ Actions")
    
    col1, col2 = st.columns(2)
    
    if col1.button("🔍 Describe Document"):
        with st.spinner("Analyzing..."):
            res = analyze_image(image, "Describe this document.")
            st.info(res)

    if col2.button("💰 Extract to Excel"):
        with st.spinner("Extracting data..."):
            # Prompt optimizado para facturas
            prompt = """
            Extract these fields from the invoice into JSON:
            - Vendor
            - Date
            - Invoice_No
            - Total_Amount
            - Tax_Amount
            - Items_Summary
            
            Return ONLY clean JSON.
            """
            
            raw_res = analyze_image(image, prompt)
            json_text = clean_json_text(raw_res)
            
            try:
                data = json.loads(json_text)
                df = pd.DataFrame([data])
                
                st.success("Data Extracted!")
                st.dataframe(df)
                
                # Crear Excel
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
                
                st.download_button(
                    label="📥 Download .xlsx",
                    data=buffer.getvalue(),
                    file_name="invoice_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.error(f"Conversion Error: {e}")
                st.expander("Raw Data").text(raw_res)
