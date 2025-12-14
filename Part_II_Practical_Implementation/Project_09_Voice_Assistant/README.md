# Project 09: Voice AI Assistant 🎙️

## Overview
This project builds a **Multimodal AI Agent** that can hear and speak.
It demonstrates the conversion flow: `Audio -> Text -> LLM Intelligence -> Text -> Audio`.



## Tech Stack
1.  **Hearing (STT):** Groq API using `distil-whisper-large-v3` (Ultra-low latency transcription).
2.  **Thinking (LLM):** Groq API using `llama-3.3-70b`.
3.  **Speaking (TTS):** Google Text-to-Speech (`gTTS`).

## Why Groq for Voice?
Voice interfaces require speed. If the AI takes 5 seconds to answer, it feels awkward. Groq's specialized LPU chips make the transcription and reasoning almost instantaneous, creating a fluid conversation.

## Usage
1.  Allow microphone access in your browser.
2.  Click the record button.
3.  Speak a question (in English).
4.  Listen to the AI's response.
