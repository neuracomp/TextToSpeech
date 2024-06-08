import os
import streamlit as st
from gtts import gTTS
from pydub import AudioSegment
from google.cloud import speech_v1p1beta1 as speech
import io

# Function to transcribe audio using Google Cloud Speech-to-Text
def transcribe_audio(file_path):
    client = speech.SpeechClient()

    with io.open(file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Update to match your audio encoding
        sample_rate_hertz=16000,  # Update to match your audio sample rate
        language_code="en-US",
        enable_automatic_punctuation=True,
    )

    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + "\n"
    return transcript

# Function to split audio into segments
def split_audio(audio_path, transcript):
    audio = AudioSegment.from_file(audio_path)
    os.makedirs("output_dir", exist_ok=True)
    lines = transcript.splitlines()

    for i, line in enumerate(lines):
        start_time = i * 10000  # Example: split every 10 seconds
        end_time = (i + 1) * 10000
        audio_segment = audio[start_time:end_time]
        segment_path = os.path.join("output_dir", f"segment_{i}.wav")
        audio_segment.export(segment_path, format="wav")

        with open(os.path.join("output_dir", "metadata.csv"), "a") as metadata_file:
            metadata_file.write(f"{segment_path}|{line.strip()}\n")

# Function to generate speech using gTTS
def text_to_speech_gtts(text, lang='en'):
    tts = gTTS(text=text, lang=lang, slow=False)
    output_file = "output_gtts.mp3"
    tts.save(output_file)
    return output_file

# Streamlit app layout
st.title("Custom Text to Speech App")

st.header("Step 1: Upload Audio File")
uploaded_file = st.file_uploader("Upload your audio file (MP3 or WAV format)", type=["mp3", "wav"])
if uploaded_file is not None:
    file_extension = uploaded_file.name.split('.')[-1]
    file_name = f"uploaded_audio.{file_extension}"
    with open(file_name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File uploaded successfully as {file_name}")

    # Transcribe uploaded audio
    transcript = transcribe_audio(file_name)
    st.text_area("Transcript", transcript, height=200)

    # Split audio
    split_audio(file_name, transcript)

    st.header("Step 2: Convert Text to Speech")
    text_input = st.text_area("Enter text to convert to speech:", "Hello, Streamlit!")
    if st.button("Convert Text to Speech"):
        output_file = text_to_speech_gtts(text_input)
        audio_file = open(output_file, "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3")
        audio_file.close()
        os.remove(output_file)
        os.remove(file_name)
        os.rmdir("output_dir")
