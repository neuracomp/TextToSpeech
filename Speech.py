import streamlit as st
from gtts import gTTS
import pyttsx3
import os

# Function to generate speech using gTTS
def text_to_speech_gtts(text, lang='en'):
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save("output_gtts.mp3")
    return "output_gtts.mp3"

# Function to generate speech using pyttsx3
def text_to_speech_pyttsx3(text, voice_id=None):
    engine = pyttsx3.init()
    if voice_id:
        engine.setProperty('voice', voice_id)
    engine.save_to_file(text, 'output_pyttsx3.mp3')
    engine.runAndWait()
    return "output_pyttsx3.mp3"

# Streamlit app layout
st.title("Combined Text to Speech App")

text = st.text_area("Enter text to convert to speech:", "Hello, Streamlit!")
tts_engine = st.selectbox("Select TTS engine:", ("gTTS", "pyttsx3"))

if tts_engine == "gTTS":
    language = st.selectbox("Select language:", ("en", "es", "fr", "de"))
elif tts_engine == "pyttsx3":
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    voice_options = {voice.name: voice.id for voice in voices}
    voice_name = st.selectbox("Select voice:", list(voice_options.keys()))

if st.button("Convert"):
    if tts_engine == "gTTS":
        output_file = text_to_speech_gtts(text, language)
    elif tts_engine == "pyttsx3":
        output_file = text_to_speech_pyttsx3(text, voice_options.get(voice_name))

    if output_file:
        audio_file = open(output_file, "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3")
        audio_file.close()
        os.remove(output_file)
