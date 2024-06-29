import os
import streamlit as st
import pyttsx3

# Function to generate speech using pyttsx3
def text_to_speech_pyttsx3(text):
    engine = pyttsx3.init()
    output_file = "output_pyttsx3.mp3"
    engine.save_to_file(text, output_file)
    engine.runAndWait()
    return output_file

# Streamlit app layout
st.title("Simple Text to Speech App")

st.header("Convert Text to Speech")
text_input = st.text_area("Enter text to convert to speech:", "Hello, Streamlit!")
if st.button("Convert Text to Speech"):
    output_file = text_to_speech_pyttsx3(text_input)
    audio_file = open(output_file, "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")
    audio_file.close()
    os.remove(output_file)
