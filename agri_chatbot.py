import streamlit as st
from duckduckgo_search import DDGS
from langdetect import detect
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import tempfile

# Supported languages
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "ml": "Malayalam",
    "te": "Telugu",
    "ta": "Tamil",
    "kn": "Kannada"
}

# Agriculture-related keywords for filtering queries
AGRICULTURE_KEYWORDS = [
    "crop", "soil", "fertilizer", "irrigation", "pesticide", "harvest", 
    "farming", "agriculture", "planting", "seeds", "weather", "yield", "farm", 
    "livestock", "disease", "pest", "organic", "agronomy"
]

# Basic chatbot conversation keywords and responses
BASIC_CONVERSATION = {
    "hi": "Hello! How can I assist you today?",
    "hello": "Hello! How can I assist you today?",
    "bye": "Goodbye! Have a great day!",
    "goodbye": "Goodbye! Have a great day!",
    "what is your name": "I’m your agricultural assistant chatbot!",
    "where are you from": "I’m a virtual assistant here to help with agricultural queries.",
    "thank you": "You're welcome! I'm happy to help.",
    "thanks": "You're welcome! Feel free to ask more questions!",
    "what can you do": "I can assist with agriculture-related queries and basic conversation!",
    "how can you help": "I can provide you with information related to farming, crops, soil, and more!"
}

# Function to detect language and translate text
def detect_and_translate(text):
    detected_lang = detect(text)
    if detected_lang in SUPPORTED_LANGUAGES:
        translation = GoogleTranslator(source=detected_lang, target='en').translate(text)
        return detected_lang, translation
    else:
        return None, None

# Function to translate text back to the original language
def translate_back(original_lang, text):
    return GoogleTranslator(source='en', target=original_lang).translate(text)

# Function to generate audio from text in the original language
def text_to_audio(text, lang):
    tts = gTTS(text=text, lang=lang)
    temp_audio_file = tempfile.mktemp(suffix=".mp3")  # Generate a unique temporary file name
    tts.save(temp_audio_file)  # Save audio to the temporary file
    return temp_audio_file

# Function to check if the query is agriculture-related
def is_agriculture_related(query):
    query = query.lower()
    return any(keyword in query for keyword in AGRICULTURE_KEYWORDS)

# Function to check if the query is a basic conversation
def is_basic_conversation(query):
    query = query.lower().strip()  # Normalize query
    return query in BASIC_CONVERSATION

# Streamlit app
st.title("Agricultural Chatbot 💬")

# Initialize an empty message list
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello 👋, How can I help you today?"}
    ]

# Display previous messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    # Append the user message to the session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Detect and translate the prompt
    original_lang, translated_prompt = detect_and_translate(prompt)

    if original_lang is None:
        # Language not supported
        unsupported_msg = (
            "Sorry, I can only understand the following languages: "
            "English, Hindi, Malayalam, Telugu, Tamil, Kannada."
        )
        st.session_state.messages.append({"role": "assistant", "content": unsupported_msg})
        st.chat_message("assistant").write(unsupported_msg)
    else:
        # Check if the query is a basic conversation
        if is_basic_conversation(translated_prompt):
            response = BASIC_CONVERSATION[translated_prompt.lower().strip()]
        # Check if the query is agriculture-related
        elif is_agriculture_related(translated_prompt):
            # Chat with DuckDuckGo AI
            results = DDGS().chat(translated_prompt, model='claude-3-haiku')
            response = results
        else:
            # Provide a generic response for non-agriculture queries
            response = (
                "I can only assist with agriculture-related queries. "
                "Please ask about crops, farming, soil, or anything related to agriculture."
            )
        
        # Translate the response back to the original language
        translated_response = translate_back(original_lang, response)

        # Append the response to the session state
        st.session_state.messages.append({"role": "assistant", "content": translated_response})
        st.chat_message("assistant").write(translated_response)

        # Generate and play audio of the translated response in the original language
        audio_file_path = text_to_audio(translated_response, original_lang)
        st.audio(audio_file_path)
