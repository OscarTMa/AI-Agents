# Project 10: Vision Analyst 👁️

## Overview
This is the final capstone of the Practical Implementation series. It leverages **Multimodal AI** (Computer Vision + LLM).

Using **Llama 3.2 Vision**, this agent can "see" uploaded images and perform complex tasks like OCR (Optical Character Recognition), data extraction, or scene description.



## Tech Stack
- **Model:** `llama-3.2-90b-vision-preview` (Groq).
- **Processing:** `Pillow` & `Base64` encoding.
- **Interface:** Streamlit.

## Key Features
- **Visual Understanding:** Can interpret charts and complex scenes.
- **Structured Extraction:** Can convert an image of a table/invoice into clean JSON code.
- **Speed:** Powered by Groq's LPUs for near-instant vision inference.

## Usage
```bash
pip install -r requirements.txt
streamlit run app.py
