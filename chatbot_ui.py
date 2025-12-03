import streamlit as st
from google import genai
import os
import time

# ---------------------------------------------------
# 1. Streamlit Page Settings
# ---------------------------------------------------
st.set_page_config(page_title="Gemini AI Chatbot", layout="centered")
st.title("🤖 My AI Chatbot — Powered by Google Gemini 2.5 Flash")

# ---------------------------------------------------
# 2. API Key
# ---------------------------------------------------
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("❌ GEMINI_API_KEY not found. Add it in Streamlit secrets.")
    st.stop()

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash"

# ---------------------------------------------------
# 3. Chat History
# ---------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ---------------------------------------------------
# 4. Send message to Gemini Model
# ---------------------------------------------------
def send_message(prompt, image_data=None):
    try:
        contents = [{"role": "user", "parts": [{"text": prompt}]}]

        # If an image is included
        if image_data:
            contents[0]["parts"].append({"inline_data": {"data": image_data, "mime_type": "image/png"}})

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents
        )

        reply = response.text

        st.session_state.chat_history.append({"role": "user", "text": prompt})
        st.session_state.chat_history.append({"role": "assistant", "text": reply})

    except Exception as e:
        st.error(f"Gemini API Error: {e}")


# ---------------------------------------------------
# 5. Display Chat History (with UI bubble effect)
# ---------------------------------------------------
def show_typing(text):
    """Typing animation for model messages."""
    placeholder = st.empty()
    displayed = ""
    for char in text:
        displayed += char
        placeholder.markdown(displayed)
        time.sleep(0.01)


for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(f"**You:** {msg['text']}")
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["text"])


# ---------------------------------------------------
# 6. User Input + Image Upload
# ---------------------------------------------------
uploaded_img = st.file_uploader("Upload an image (optional)", type=["png", "jpg", "jpeg"])
prompt = st.chat_input("Ask me anything...")

if prompt:
    img_data = uploaded_img.read() if uploaded_img else None

    with st.chat_message("user"):
        st.markdown(prompt)

    send_message(prompt, image_data=img_data)

    # Show typing animation for last assistant response
    last_msg = st.session_state.chat_history[-1]["text"]
    with st.chat_message("assistant"):
        show_typing(last_msg)

    st.rerun()


# ---------------------------------------------------
# 7. Sidebar
# ---------------------------------------------------
st.sidebar.header("⚙️ App Settings")
st.sidebar.markdown(f"**Model:** `{MODEL_NAME}`")
st.sidebar.markdown("Gemini 2.5 Flash is optimized for speed + reasoning.")
st.sidebar.markdown("---")

if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()
