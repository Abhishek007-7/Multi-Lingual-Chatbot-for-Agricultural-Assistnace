import streamlit as st
from duckduckgo_search import DDGS
from langdetect import detect
from deep_translator import GoogleTranslator
from gtts import gTTS
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
        # Append the translation to the session state
        st.session_state.messages.append({"role": "assistant", "content": f"Translated to English: {translated_prompt}"})

        # Chat with DuckDuckGo AI
        results = DDGS().chat(translated_prompt, model='claude-3-haiku')

        # Translate the response back to the original language
        translated_response = translate_back(original_lang, results)

        # Append the response to the session state
        st.session_state.messages.append({"role": "assistant", "content": translated_response})
        st.chat_message("assistant").write(translated_response)

        # Generate and play audio of the translated response in the original language
        audio_file_path = text_to_audio(translated_response, original_lang)

        # Streamlit audio player
        st.audio(audio_file_path)
