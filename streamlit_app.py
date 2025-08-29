import streamlit as st

st.title("🎉 नमस्ते! यह मेरी पहली Streamlit ऐप है।")

# नाम इनपुट
name = st.text_input("अपना नाम लिखिए:")

# अगर नाम डाला है तो स्वागत संदेश दिखेगा
if name:
    st.success(f"स्वागत है, {name} जी! 🚀")
