# utils/text_to_speech.py

from gtts import gTTS
import os

def text_to_speech(text, filename="output.mp3"):
    """Convert given text into speech and save as an MP3 file."""
    tts = gTTS(text=text, lang="en")
    tts.save(filename)
    return filename
