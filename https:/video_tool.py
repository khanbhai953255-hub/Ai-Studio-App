import streamlit as st

st.set_page_config(page_title="Video Tool - Amir Maudaha AI Studio")

st.title("🎥 Video Generator Tool")
st.write("यहाँ आप 16:9 या 9:16 format चुनकर video बना सकते हैं।")

# User से input लो
title = st.text_input("Video Title लिखिए:")

# Aspect ratio option
aspect = st.radio(
    "Aspect Ratio चुनें:",
    ("16:9", "9:16")
)

# Generate button
if st.button("Generate Video"):
    st.success(f"🎬 आपका वीडियो '{title}' {aspect} format में तैयार किया जाएगा!")
    st.info("👉 Note: अभी यह demo है। असली video generation बाद में जोड़ा जाएगा।")
