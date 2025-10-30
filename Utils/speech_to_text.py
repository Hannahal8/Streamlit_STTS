import os
from openai import OpenAI
from groq import Groq

def transcribe_with_whisper(audio_path, api_key=None):
    """
    Transcribe audio using OpenAI Whisper API first.
    If OpenAI fails or API key missing, fallback to Groq Whisper.
    """
    # Try OpenAI Whisper first
    openai_key = api_key or os.getenv("OPENAI_API_KEY")
    if openai_key:
        try:
            client = OpenAI(api_key=openai_key)
            with open(audio_path, "rb") as audio_file:
                response = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            print("✅ Transcribed with OpenAI Whisper")
            return getattr(response, "text", None) or response.get("text")
        except Exception as e:
            print(f"⚠️ OpenAI Whisper failed: {e}")

    # Fallback to Groq Whisper if OpenAI not available
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        try:
            client = Groq(api_key=groq_key)
            with open(audio_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-large-v3",
                    file=audio_file
                )
            print("✅ Transcribed with Groq Whisper")
            return transcription.text
        except Exception as e:
            raise RuntimeError(f"Both OpenAI and Groq Whisper failed: {e}")
    else:
        raise ValueError("❌ No valid API key found for OpenAI or Groq.")
