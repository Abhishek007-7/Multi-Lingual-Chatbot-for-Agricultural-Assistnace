import streamlit as st
from duckduckgo_search import DDGS
from langdetect import detect
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile
import re

# Supported languages
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "ml": "Malayalam",
    "te": "Telugu",
    "ta": "Tamil",
    "kn": "Kannada"
}

# Basic chatbot functions (greetings, farewells, etc.)
BASIC_CHATBOT_RESPONSES = {
    "hello": "Hello! How can I assist you today?",
    "hi": "Hi there! How can I help you?",
    "bye": "Goodbye! Have a great day!",
    "what is your name": "I am your agricultural chatbot, here to assist you with farming and related queries.",
    "who are you": "I am a chatbot designed to assist you with agriculture-related information.",
    "how are you": "I'm just a program, but thanks for asking! How can I assist you?",
    "where are you from": "I exist in the cloud to help you with your agricultural needs."
}

# Keywords that indicate agriculture-related questions
AGRICULTURE_KEYWORDS = ['crop', 'farming', 'soil', 'irrigation', 'pests', 'harvest', 'fertilizer', 'weather', 'yield', 'planting', 'seeds', 'agriculture']

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
    # Create a temporary file to save the audio
    temp_audio_file = tempfile.mktemp(suffix=".mp3")  # Generate a unique temporary file name
    tts.save(temp_audio_file)  # Save audio to the temporary file
    return temp_audio_file

# Function to check if the query is agriculture-related
def is_agriculture_related(query):
    query = query.lower()
    for keyword in AGRICULTURE_KEYWORDS:
        if keyword in query:
            return True
    return False

# Function to handle basic chatbot functions
def handle_basic_chatbot_function(query):
    query = query.lower().strip()
    for key, response in BASIC_CHATBOT_RESPONSES.items():
        if re.search(rf"\b{key}\b", query):
            return response
    return None

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

    # Handle basic chatbot functions (like greetings, farewells, etc.) before language detection
    basic_response = handle_basic_chatbot_function(prompt)
    if basic_response:
        # Reply directly if it's a basic conversation
        st.session_state.messages.append({"role": "assistant", "content": basic_response})
        st.chat_message("assistant").write(basic_response)

    else:
        # Detect and translate the prompt if not a basic function
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
            # If agriculture-related, handle it
            if is_agriculture_related(translated_prompt):
                # Use DuckDuckGo AI for agricultural responses
                results = DDGS().chat(translated_prompt, model='claude-3-haiku')

                # Translate the response back to the original language
                translated_response = translate_back(original_lang, results)

                # Append the response to the session state
                st.session_state.messages.append({"role": "assistant", "content": translated_response})
                st.chat_message("assistant").write(translated_response)

                # Generate and play audio of the translated response
                audio_file_path = text_to_audio(translated_response, original_lang)
                st.audio(audio_file_path)
            else:
                # Non-agriculture-related response
                non_agriculture_msg = "I can only help with agriculture-related topics. Please ask about farming, crops, soil, etc."
                translated_response = translate_back(original_lang, non_agriculture_msg)
                st.session_state.messages.append({"role": "assistant", "content": translated_response})
                st.chat_message("assistant").write(translated_response)

                # Generate and play audio of the response
                audio_file_path = text_to_audio(translated_response, original_lang)
                st.audio(audio_file_path)
