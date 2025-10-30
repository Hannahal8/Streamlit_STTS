import streamlit as st
import tempfile

def setup_page():
    """Setup Streamlit page configuration and styling."""
    st.set_page_config(
        page_title="VoiceFlow Assistant",
        page_icon="🎙️",
        layout="wide",
    )

    st.markdown("""
        <style>
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 0 0 20px 20px;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
        }
        .feature-card {
            background: white;
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin: 1rem 0;
            border-left: 4px solid #667eea;
        }
        .upload-area {
            border: 2px dashed #667eea;
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
            background: #f8f9ff;
            margin: 1rem 0;
        }
        .stButton button {
            width: 100%;
            border-radius: 10px;
            padding: 0.75rem;
            font-weight: 600;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="main-header">
            <h1>🎙️ VoiceFlow Assistant</h1>
            <p>Convert Speech ↔ Text seamlessly using OpenAI Whisper & gTTS</p>
        </div>
    """, unsafe_allow_html=True)


def audio_upload_section():
    """UI for uploading and transcribing audio."""
    st.markdown("### 🎧 Text to Speech")

    with st.container():
        st.markdown('<div class="upload-area">', unsafe_allow_html=True)
        audio_file = st.file_uploader(
            "Drag and drop or click to upload",
            type=["mp3", "wav"],
            label_visibility="collapsed"
        )
        if audio_file:
            st.success(f"✅ Uploaded: {audio_file.name}")
            st.audio(audio_file, format="audio/wav")
        else:
            st.markdown("<p>📁 Upload your audio file (MP3/WAV)</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        transcribe_btn = st.button("🎤 Transcribe Audio", disabled=not audio_file)
    with col2:
        if st.button("🔄 Reset"):
            st.session_state["transcribed_text"] = ""
            st.rerun()

    return audio_file, transcribe_btn


def text_to_speech_ui(default_text=""):
    st.markdown("### 🗣️ Text to Speech")
    text_input = st.text_area("Enter text to convert:", default_text, height=150)
    generate_btn = st.button("🎧 Generate Speech")
    return text_input, generate_btn