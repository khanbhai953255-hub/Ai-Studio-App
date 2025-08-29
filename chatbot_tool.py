import streamlit as st
import requests

def run_chatbot():
    st.title("🤖 Chat (Playground)")
    st.info("API key ना हो तो Demo Echo mode चलेगा. Key हो तो असली AI जवाब मिलेगा.")

    if "OPENAI_API_KEY" in st.secrets:
        api_key = st.secrets["OPENAI_API_KEY"]
    else:
        api_key = st.text_input("OpenAI API Key (optional)", type="password", placeholder="sk-...")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_msg = st.text_input("Your message")
    if st.button("Send") and user_msg:
        if api_key:
            try:
                headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
                payload = {"model": "gpt-4o-mini", "input": user_msg}
                r = requests.post("https://api.openai.com/v1/responses", headers=headers, json=payload, timeout=30)
                if r.ok:
                    data = r.json()
                    out = data.get("output_text") or data.get("choices", [{}])[0].get("message", {}).get("content", "")
                    st.session_state.chat_history.append(("You", user_msg))
                    st.session_state.chat_history.append(("AI", out or "No response text."))
                else:
                    st.session_state.chat_history.append(("You", user_msg))
                    st.session_state.chat_history.append(("AI", f"[API error {r.status_code}] {user_msg}"))
            except Exception as e:
                st.session_state.chat_history.append(("You", user_msg))
                st.session_state.chat_history.append(("AI", f"[API fail: {e}] {user_msg}"))
        else:
            st.session_state.chat_history.append(("You", user_msg))
            st.session_state.chat_history.append(("AI", user_msg))  # echo

    for role, msg in st.session_state.chat_history[-20:]:
        st.write(f"**{role}:** {msg}")
