import streamlit as st
from google import genai
import os

# 1. Streamlit App Config
st.set_page_config(page_title="Gemini Chatbot UI", layout="centered")
st.title("My AI Chatbot powered by Google Gemini")

# 2. Load API Key
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY environment variable not found. Add it in Streamlit Secrets.")
    st.stop()

# 3. Initialize Gemini Client
try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error(f"Gemini initialization failed: {e}")
    st.stop()

MODEL_NAME = "gemini-2.5-flash"

# 4. Initialize History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. Function to call Gemini Model
def send_message(prompt):
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                {"role": "user", "parts": [{"text": prompt}]}
            ]
        )

        reply = response.text

        # Store history
        st.session_state.chat_history.append({"role": "user", "text": prompt})
        st.session_state.chat_history.append({"role": "assistant", "text": reply})

    except Exception as e:
        st.error(f"Gemini API Error: {e}")

# 6. Display Chat History
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])

# 7. Chat Input
prompt = st.chat_input("Ask me anything...")

if prompt:
    send_message(prompt)
    st.rerun()

# 8. Sidebar Info
st.sidebar.markdown("## App Info")
st.sidebar.markdown(f"**Model:** `{MODEL_NAME}`")
st.sidebar.markdown("This chatbot uses Google's Gemini 2.5 Flash model.")
st.sidebar.markdown("---")

if st.sidebar.button("Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()
