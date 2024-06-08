import os
import streamlit as st
from gtts import gTTS
import youtube_dl
from pydub import AudioSegment
from google.cloud import speech_v1p1beta1 as speech
import io

# Function to download audio from YouTube
def download_audio(youtube_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloaded_audio.%(ext)s',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    return 'downloaded_audio.wav'

# Function to transcribe audio using Google Cloud Speech-to-Text
def transcribe_audio(file_path):
    client = speech.SpeechClient()

    with io.open(file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
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
    audio = AudioSegment.from_wav(audio_path)
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

text_input = st.text_area("Enter text to convert to speech:", "Hello, Streamlit!")
youtube_url = st.text_input("Enter YouTube URL for voice training:")

if st.button("Convert"):
    audio_path = download_audio(youtube_url)
    transcript = transcribe_audio(audio_path)
    split_audio(audio_path, transcript)

    # Here, you would normally train the TTS model, but this step is skipped for simplicity

    output_file = text_to_speech_gtts(text_input)
    audio_file = open(output_file, "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")
    audio_file.close()
    os.remove(output_file)
    os.remove(audio_path)
    os.rmdir("output_dir")
