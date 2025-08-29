import streamlit as st

st.title("🎉 नमस्ते! यह मेरी पहली Streamlit ऐप है।")

name = st.text_input("अपना नाम लिखिए:")
if name:
    st.success(f"स्वागत है, {name} जी! 🚀")
