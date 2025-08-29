import streamlit as st
from chatbot_tool import run_chatbot
from image_tool import run_image_tool
from tts_tool import run_tts_tool
from stt_tool import run_stt_tool
from image_edit_tool import run_image_edit_tool
from video_tool import run_video_tool

st.set_page_config(page_title="Amir Maudaha AI Studio", layout="wide")

with st.sidebar:
    st.title("⚙️ Amir Maudaha AI Studio")
    page = st.radio(
        "Navigate",
        [
            "🏠 Home",
            "🤖 Chat (Playground)",
            "🖼️ Text → Image",
            "✍️ Image Editor",
            "🗣️ Text → Speech (TTS)",
            "🎤 Speech → Text (STT)",
            "🎬 Video Maker (9:16 / 16:9)",
        ],
        index=0,
    )
    st.caption("Tip: OPENAI_API_KEY (optional) जोड़ें: App → Settings → Secrets")

if page == "🏠 Home":
    st.title("🏠 Home")
    st.write("Welcome! यह आपका **Google AI Studio जैसा** मल्टी-टूल हब है — मोबाइल-फ्रेंडली और पर्सनल यूज़ के लिए।")
    name = st.text_input("अपना नाम लिखिए:")
    if name:
        st.success(f"स्वागत है, {name} जी! 🚀")

elif page == "🤖 Chat (Playground)":
    run_chatbot()

elif page == "🖼️ Text → Image":
    run_image_tool()

elif page == "✍️ Image Editor":
    run_image_edit_tool()

elif page == "🗣️ Text → Speech (TTS)":
    run_tts_tool()

elif page == "🎤 Speech → Text (STT)":
    run_stt_tool()

elif page == "🎬 Video Maker (9:16 / 16:9)":
    run_video_tool()
