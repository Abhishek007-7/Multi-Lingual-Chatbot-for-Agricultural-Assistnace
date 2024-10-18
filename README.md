# Multi Lingual Chatbot for Agricultural Assistance 🌾💬

This is a multilingual chatbot designed to assist users with agriculture-related queries. The bot supports multiple languages and provides responses in both text and audio formats. It uses **Google Translator**, **gTTS**, and **DuckDuckGo Search** to process user inputs and deliver responses.

## Features

- **Multilingual Support**: Detects and translates inputs from English, Hindi, Malayalam, Telugu, Tamil, and Kannada.
- **Agriculture-Focused**: Answers agriculture-related questions using AI-driven responses.
- **Text and Audio Output**: Responds in the user's language with text and audio (gTTS).
- **Basic Conversation**: Handles basic greetings and questions like "hello," "how are you," etc.

## Supported Languages

- English
- Hindi
- Malayalam
- Telugu
- Tamil
- Kannada

## Prerequisites

Ensure the following Python libraries are installed:

```bash
pip install streamlit duckduckgo_search langdetect deep-translator gtts
```

## Running the Application

To run the chatbot using **Streamlit**, use the following command:

```bash
streamlit run app.py
```

## How It Works

1. The chatbot detects the input language and translates it to English for processing.
2. If the input is agriculture-related, it queries DuckDuckGo for relevant information.
3. The response is translated back to the original language and provided as both text and audio.
4. For non-agriculture queries, the bot will politely redirect users to ask agriculture-related questions.

## Example Queries

- "What crops grow best in winter?"
- "Tell me about soil irrigation in Hindi."
- "Fertilizer recommendations for tomatoes in Kannada."

## License

This project is licensed under the MIT License.

---

This README file can be customized as needed before publishing to GitHub!
