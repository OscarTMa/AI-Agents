import streamlit as st
from PIL import Image
import google.generativeai as genai
import pandas as pd
import json
import re
import io

# 1. CONFIGURACIÓN
st.set_page_config(page_title="DocuVision AI", page_icon="👁️", layout="centered")

st.title("👁️ DocuVision: Intelligent OCR")
st.caption("Powered by Google Gemini 1.5 Flash")

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

# Auto-configuración
try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Error configuring API: {e}")

# 3. LÓGICA DE AUTO-SELECCIÓN DE MODELO
def find_vision_model():
    """Busca automáticamente un modelo capaz de ver imágenes."""
    try:
        models = list(genai.list_models())
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                if 'flash' in m.name: return m.name # Preferimos Flash
                if 'gemini-1.5-pro' in m.name: return m.name
        return "models/gemini-1.5-flash" # Fallback
    except:
        return "models/gemini-1.5-flash"

selected_model_name = find_vision_model()

# 4. FUNCIONES DE ANÁLISIS Y LIMPIEZA

def analyze_image(image, prompt):
    try:
        model = genai.GenerativeModel(selected_model_name)
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"Error analyzing image: {e}"

def clean_json_text(text):
    """Limpia el texto Markdown (```json) para obtener solo el JSON puro."""
    try:
        # Usamos Regex para encontrar el bloque de código JSON
        pattern = r"```json(.*?)```"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text # Si no hay markdown, devolvemos el texto tal cual
    except:
        return text

# 5. INTERFAZ DE USUARIO

uploaded_file = st.file_uploader("Upload Document (Invoice, Receipt, PO)...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Document Preview", use_column_width=True)
    
    st.markdown("### ⚡ AI Extraction Actions")
    
    # Botón 1: Análisis General
    if st.button("🔍 Analyze & Describe"):
        with st.spinner("Analyzing..."):
            res = analyze_image(image, "Describe this document in detail and identify its purpose.")
            st.info(res)

    # Botón 2: El Producto Comercial (Excel)
    if st.button("💰 Extract Data to Excel"):
        with st.spinner("Extracting structured data..."):
            # Prompt estricto para asegurar formato JSON
            prompt = """
            You are a Data Extraction Agent. Analyze this invoice/receipt.
            Extract the following fields into a pure JSON object:
            - Vendor Name
            - Date
            - Invoice Number
            - Total Amount
            - Currency
            - List of Items (as a summary string)
            
            Return ONLY the JSON. No markdown, no intro text.
            """
            
            raw_response = analyze_image(image, prompt)
            
            # Limpiamos la respuesta
            json_text = clean_json_text(raw_response)
            
            try:
                # Convertimos a Diccionario Python
                data_dict = json.loads(json_text)
                
                # Convertimos a DataFrame (Tabla)
                # Ponemos [data_dict] para que sea una fila
                df = pd.DataFrame([data_dict])
                
                st.success("✅ Extraction Successful!")
                
                # Mostrar tabla en pantalla
                st.dataframe(df)
                
                # Convertir DF a Excel en memoria
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Data')
                
                # BOTÓN DE DESCARGA
                st.download_button(
                    label="📥 Download .xlsx Report",
                    data=buffer.getvalue(),
                    file_name="invoice_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                
            except json.JSONDecodeError:
                st.error("Failed to generate valid JSON. The AI response was not structured correctly.")
                with st.expander("See Raw AI Response"):
                    st.text(raw_response)
            except Exception as e:
                st.error(f"Error creating Excel: {e}")
