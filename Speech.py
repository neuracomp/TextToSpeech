import os
import streamlit as st
from gtts import gTTS
from pytube import YouTube
from pydub import AudioSegment
from google.cloud import speech_v1p1beta1 as speech
import io

# Function to download audio from YouTube with pytube
def download_audio(youtube_url):
    try:
        yt = YouTube(youtube_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_stream.download(filename='downloaded_audio.mp3')
        return 'downloaded_audio.mp3'
    except Exception as e:
        st.error(f"Error downloading audio: {e}")
        return None

# Function to transcribe audio using Google Cloud Speech-to-Text
def transcribe_audio(file_path):
    client = speech.SpeechClient()

    with io.open(file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
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
    audio = AudioSegment.from_mp3(audio_path)
    os.makedirs("output_dir", exist_ok=True)
    lines = transcript.splitlines()

    for i, line in enumerate(lines):
        start_time = i * 10000  # Example: split every 10 seconds
        end_time = (i + 1) * 10000
        audio_segment = audio[start_time:end_time]
        segment_path = os.path.join("output_dir", f"segment_{i}.mp3")
        audio_segment.export(segment_path, format="mp3")

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

st.header("Step 1: Download Audio from YouTube")
youtube_url = st.text_input("Enter YouTube URL for voice training:")
if st.button("Download Audio"):
    audio_path = download_audio(youtube_url)
    if audio_path:
        st.success(f"Audio downloaded and saved as {audio_path}")

st.header("Step 2: Upload Downloaded Audio File")
uploaded_file = st.file_uploader("Upload your downloaded audio file (MP3 format)", type="mp3")
if uploaded_file is not None:
    with open("uploaded_audio.mp3", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("File uploaded successfully")

    # Transcribe uploaded audio
    transcript = transcribe_audio("uploaded_audio.mp3")
    st.text_area("Transcript", transcript, height=200)

    # Split audio
    split_audio("uploaded_audio.mp3", transcript)

    st.header("Step 3: Convert Text to Speech")
    text_input = st.text_area("Enter text to convert to speech:", "Hello, Streamlit!")
    if st.button("Convert Text to Speech"):
        output_file = text_to_speech_gtts(text_input)
        audio_file = open(output_file, "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3")
        audio_file.close()
        os.remove(output_file)
        os.remove("uploaded_audio.mp3")
        os.remove("downloaded_audio.mp3")
        os.rmdir("output_dir")
