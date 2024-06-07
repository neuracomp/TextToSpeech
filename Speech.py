import streamlit as st
from gtts import gTTS
import os

# Function to generate speech
def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save("output.mp3")

# Streamlit app layout
st.title("Text to Speech App")

text = st.text_area("Enter text to convert to speech:", "Hello, Streamlit!")
language = st.selectbox("Select language:", ("en", "es", "fr", "de"))

if st.button("Convert"):
    text_to_speech(text, language)
    audio_file = open("output.mp3", "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")
    audio_file.close()
    os.remove("output.mp3")
