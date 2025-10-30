import streamlit as st
import os
import tempfile
from dotenv import load_dotenv
from Utils.speech_to_text import transcribe_with_whisper
from Utils.text_to_speech import text_to_speech
from Utils.Ui import setup_page, audio_upload_section, text_to_speech_ui

# ---------------------- Load Environment Variables ----------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ---------------------- Page Setup ----------------------
setup_page()

# ---------------------- Sidebar ----------------------
with st.sidebar:
    st.markdown("### ⚙️ Control Panel")
    st.success("✅ Speech-to-Text")
    st.info("🔄 Text-to-Speech")
    st.markdown("---")

# ---------------------- Main Layout ----------------------
col1, col2 = st.columns(2)

with col1:
    audio_file, transcribe_btn = audio_upload_section()

    if transcribe_btn and audio_file:
        with st.spinner("🎤 Transcribing..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                tmp.write(audio_file.read())
                tmp_path = tmp.name

            try:
                text = transcribe_with_whisper(tmp_path, OPENAI_API_KEY)
                st.session_state["transcribed_text"] = text
                st.success("✅ Transcription successful!")
                st.markdown(f"<div class='feature-card'>{text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"❌ Failed: {str(e)}")
            finally:
                os.unlink(tmp_path)

with col2:
    text_input, generate_btn = text_to_speech_ui(st.session_state.get("transcribed_text", ""))
    if generate_btn:
        if text_input.strip():
          with st.spinner("🎧 Generating audio..."):
            try:
                output_file = text_to_speech(text_input)
                st.audio(output_file, format="audio/mp3")
                st.success("✅ Audio generated successfully!")
            except Exception as e:
                st.error(f"❌ Failed: {str(e)}")
        else:
            st.warning("⚠️ Please enter some text before generating.")