import streamlit as st
import requests

def run_stt_tool():
    st.title("🎤 Speech → Text (STT)")
    st.info("OPENAI_API_KEY होने पर Whisper API से ट्रांसक्रिप्शन होगा; नहीं तो demo message दिखेगा.")
    audio = st.file_uploader("Audio upload (mp3/wav/m4a)", type=["mp3","wav","m4a"])

    if st.button("Transcribe", disabled=not audio):
        api_key = st.secrets.get("OPENAI_API_KEY", None)
        if not api_key:
            st.warning("No API key — Demo: ‘Transcription will appear here.’")
            return
        try:
            files = {"file": (audio.name, audio.getvalue())}
            data = {"model": "whisper-1"}  # if model name changes, adjust here
            headers = {"Authorization": f"Bearer {api_key}"}
            r = requests.post("https://api.openai.com/v1/audio/transcriptions", headers=headers, files=files, data=data, timeout=120)
            if r.ok:
                st.success("✅ Transcription:")
                st.write(r.json().get("text", ""))
            else:
                st.error(f"API error {r.status_code}: {r.text[:200]}")
        except Exception as e:
            st.error(f"Failed: {e}")
