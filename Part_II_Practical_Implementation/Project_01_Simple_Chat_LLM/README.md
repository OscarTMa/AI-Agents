# 💬 AI Chat Agent with Memory (Llama 3 + Groq)

![Project Status](https://img.shields.io/badge/Status-Completed-success)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-ff4b4b)
![Groq](https://img.shields.io/badge/AI-Llama3_70b-orange)

### 🚀 Live Demo

https://ai-agents-6uppjdpfvce83waskkym5h.streamlit.app/
---

### 📖 Overview
This project is an implementation of a **Stateful AI Conversational Agent**. Unlike standard script execution, this application maintains conversation context across user interactions using **Session State management**.

It leverages **Groq's LPU (Language Processing Unit)** inference engine to deliver near-instant responses using the **Meta Llama 3 70B** model.

### 🖼️ Demo

### 🛠️ Key Technical Features
* **State Management:** Implemented persistent memory using `st.session_state` to handle multi-turn conversations in a stateless web framework.
* **High-Performance Inference:** Integrated Groq API for sub-second latency generation.
* **Real-time Streaming:** Implemented generator patterns to stream text tokens to the UI (Typewriter effect).
* **Security:** API Keys managed via Streamlit Secrets (not hardcoded).

### 💻 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/OscarTMa/AI-Agents.git](https://github.com/OscarTMa/AI-Agents.git)
   cd AI-Agents/Part_II_Practical_Implementation/Project_01_Simple_Chat_LLM
