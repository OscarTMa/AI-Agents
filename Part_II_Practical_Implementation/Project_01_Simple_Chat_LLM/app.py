import streamlit as st
from groq import Groq  

# 1. Page Configuration
st.set_page_config(page_title="Llama 3 Chat Agent", page_icon="🦙")

st.title("🦙 Project 01: Free Chat Agent (Groq)")
st.caption("🚀 A streamlit chatbot powered by Meta Llama 3 via Groq")

# 2. Sidebar for Configuration
with st.sidebar:
    st.header("Configuration")
    # Try to get key from secrets, otherwise ask user
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
        st.success("API Key found in secrets!", icon="✅")
    else:
        api_key = st.text_input("Groq API Key", type="password")
        if not api_key:
            st.warning("Please enter your Groq API Key to proceed.", icon="⚠️")
            st.stop()
    
    # Modelos disponibles en Groq (Gratuitos)
    model_choice = st.selectbox(
        "Select Model", 
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]
    )
    
    st.markdown("---")
    st.markdown("### How it works")
    st.markdown("This agent uses **Groq** for ultra-fast inference using open-source models like Llama 3.")

# 3. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! I am running on Llama 3. How can I help you?"}]

# 4. Display Chat Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. Handle User Input
if prompt := st.chat_input("Type your message here..."):
    
    # CAMBIO 3: Cliente de Groq
    client = Groq(api_key=api_key)

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 6. Generate Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # CAMBIO 4: La estructura de llamada es idéntica a OpenAI
            stream = client.chat.completions.create(
                model=model_choice,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        
        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()

    st.session_state.messages.append({"role": "assistant", "content": full_response})
