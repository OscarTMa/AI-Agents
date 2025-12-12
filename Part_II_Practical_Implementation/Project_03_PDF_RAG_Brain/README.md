# Project 03: PDF RAG Brain 🧠

![Status](https://img.shields.io/badge/Status-Completed-success)
![Groq](https://img.shields.io/badge/AI-Llama3.3-orange)
![RAG](https://img.shields.io/badge/Tech-RAG-blue)
![Cost](https://img.shields.io/badge/Cost-Free-green)

## Overview
This project implements a **Retrieval Augmented Generation (RAG)** system. It allows users to upload a PDF document and chat with it.

Instead of relying on costly APIs for embeddings (like OpenAI), this project uses **HuggingFace Embeddings** running locally on the CPU, combined with **Groq's Llama 3.3** for high-speed inference.

## Features
- **Document Ingestion:** Supports PDF file uploads.
- **Vector Search:** Uses FAISS for efficient similarity search.
- **Local Embeddings:** Uses `sentence-transformers/all-MiniLM-L6-v2` (Zero cost).
- **Fast Inference:** Powered by Groq (`llama-3.3-70b-versatile`).

## Architecture
```mermaid
graph LR
    A[PDF] --> B(Chunking)
    B --> C(HuggingFace Embeddings)
    C --> D[(FAISS Vector DB)]
    E[User Question] --> F(Retriever)
    D --> F
    F --> G{Groq LLM}
    G --> H[Answer]
