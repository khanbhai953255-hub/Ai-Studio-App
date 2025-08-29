import streamlit as st

st.set_page_config(page_title="Amir Maudaha AI Studio")

st.title("Amir Maudaha AI Studio")
st.write("🎉 नमस्ते! यह मेरी पहली Streamlit ऐप है।")

name = st.text_input("अपना नाम लिखिए:")
if name:
    st.success(f"Welcome, {name}!")
