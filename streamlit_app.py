import streamlit as st
import video_tool   # हमारा नया video tool

# ऐप का टाइटल
st.title("🎉 Amir Maudaha AI Studio")

# Sidebar Menu
menu = st.sidebar.selectbox("🔍 Choose Tool", ["Home", "Video Tool"])

# Home Page
if menu == "Home":
    name = st.text_input("अपना नाम लिखिए:")
    if name:
        st.success(f"स्वागत है, {name} जी! 🚀")

# Video Tool Page
elif menu == "Video Tool":
    video_tool.run()   # video_tool.py का function call
