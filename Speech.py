import os
import streamlit as st
from gtts import gTTS

# Function to generate speech using gTTS
def text_to_speech_gtts(text, lang='en'):
    tts = gTTS(text=text, lang=lang, slow=False)
    output_file = "output_gtts.mp3"
    tts.save(output_file)
    return output_file

# Streamlit app layout
st.title("Simple Text to Speech App")

st.header("Convert Text to Speech")
text_input = st.text_area("Enter text to convert to speech:", "Hello, Streamlit!")
if st.button("Convert Text to Speech"):
    output_file = text_to_speech_gtts(text_input)
    audio_file = open(output_file, "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")
    audio_file.close()
    os.remove(output_file)
