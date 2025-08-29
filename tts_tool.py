import io
from gtts import gTTS
import streamlit as st

def run_tts_tool():
    st.title("🗣️ Text → Speech (TTS)")
    text = st.text_area("जिस टेक्स्ट को आवाज़ में बदलना है", height=150, placeholder="नमस्ते! यह मेरा पहला AI Studio है।")
    lang = st.selectbox("Language", ["hi", "en"], index=0)
    tld = st.selectbox("Voice Region", ["com", "co.in", "co.uk"], index=1)

    if st.button("Generate Voice", disabled=not text.strip()):
        with st.spinner("Generating..."):
            try:
                tts = gTTS(text=text.strip(), lang=lang, tld=tld)
                buf = io.BytesIO()
                tts.write_to_fp(buf)
                audio_bytes = buf.getvalue()
                st.audio(audio_bytes, format="audio/mp3")
                st.download_button("⬇️ Download MP3", audio_bytes, file_name="speech.mp3", mime="audio/mpeg")
                st.success("✅ Done!")
            except Exception as e:
                st.error(f"Failed: {e}")
