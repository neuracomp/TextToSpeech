import streamlit as st
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os

# Function to generate speech using gTTS
def text_to_speech_gtts(text, lang='en'):
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save("output_gtts.mp3")
    return "output_gtts.mp3"

# Function to generate speech using pydub
def text_to_speech_pydub(text):
    from gtts import gTTS
    tts = gTTS(text=text, lang='en')
    tts.save("output_pydub.mp3")
    sound = AudioSegment.from_mp3("output_pydub.mp3")
    return sound

# Streamlit app layout
st.title("Combined Text to Speech App")

text = st.text_area("Enter text to convert to speech:", "Hello, Streamlit!")
tts_engine = st.selectbox("Select TTS engine:", ("gTTS", "pydub"))

if tts_engine == "gTTS":
    language = st.selectbox("Select language:", ("en", "es", "fr", "de"))

if st.button("Convert"):
    if tts_engine == "gTTS":
        output_file = text_to_speech_gtts(text, language)
        audio_file = open(output_file, "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3")
        audio_file.close()
        os.remove(output_file)
    elif tts_engine == "pydub":
        sound = text_to_speech_pydub(text)
        play(sound)
        st.success("Audio played using pydub.")
