# Project 05: YouTube AI Assistant 📺

## Overview
We all have a "Watch Later" playlist that is too long. This agent solves that problem by using **Llama 3.3** to "watch" videos for you.

It extracts the transcript from a YouTube URL and allows you to perform different cognitive tasks on the content: Summarization, Extraction of Key Points, or Educational Quizzes.



## How it Works
1. **Extraction:** Uses `youtube-transcript-api` to fetch closed captions (Human or Auto-generated).
2. **Preprocessing:** Concatenates time-stamped text into a single context block.
3. **Inference:** Sends the text to Groq (Llama 3.3) with a specific prompt strategy based on user selection.

## Features
- **Zero Cost:** Uses existing subtitles, no expensive audio-to-text processing needed.
- **Multi-Action:** Can summarize, list bullet points, or generate quizzes.
- **Visuals:** Embeds the video player directly in the app.

## Usage
```bash
pip install -r requirements.txt
streamlit run app.py
