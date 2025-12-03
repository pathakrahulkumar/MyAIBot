import streamlit as st
import google.generativeai as genai
import os

# Streamlit settings
st.set_page_config(page_title="Gemini Chatbot UI", layout="centered")
st.title("My AI Chatbot powered by Google Gemini")

# Load API key from Streamlit secrets
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY not found. Please add it in Streamlit Secrets.")
    st.stop()

# Configure Gemini
genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash"

# Set up chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Create model chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = genai.Chat(model=MODEL_NAME)

# Function to send message
def send_message(prompt):
    try:
        response = st.session_state.chat_session.send_message(prompt)

        st.session_state.chat_history.append({"role": "user", "text": prompt})
        st.session_state.chat_history.append({"role": "model", "text": response.text})

    except Exception as e:
        st.error(f"API error: {e}")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# Chat input
prompt = st.chat_input("Ask me anything...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    
    send_message(prompt)

    st.rerun()

# Sidebar
st.sidebar.markdown("## App Details")
st.sidebar.markdown(f"**Model:** `{MODEL_NAME}`")
st.sidebar.markdown("---")
if st.sidebar.button("Clear Chat History"):
    st.session_state.chat_history = []
    st.session_state.chat_session = genai.Chat(model=MODEL_NAME)
    st.rerun()
