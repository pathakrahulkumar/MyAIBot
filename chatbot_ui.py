import streamlit as st
from google import genai
import os

# 1. Configuration
st.set_page_config(page_title="Gemini Chatbot UI", layout="centered")
st.title("My AI Chatbot powered by Google Gemini")

# 2. Initialize Gemini Client
# CRITICAL CHANGE: We now retrieve the key directly as an OS environment variable, 
# which is the most reliable way to access secrets in Streamlit Cloud.
try:
    # 1. Get the API key value from the environment variable (set by Streamlit secrets)
    API_KEY = os.getenv("GEMINI_API_KEY")

    if not API_KEY:
        st.error("GEMINI_API_KEY environment variable not found. Please ensure it is correctly set in Streamlit secrets.")
        st.stop()
    
    # 2. Initialize the client using the API key
    client = genai.Client(api_key=API_KEY)
    
except Exception as e:
    st.error(f"Error initializing Gemini Client: {e}")
    st.stop()

# 3. Model and Chat Initialization
MODEL_NAME = "gemini-2.5-flash"

# Initialize chat session history in Streamlit session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
# Initialize the Gemini Chat object only if it hasn't been done
if "chat_session" not in st.session_state:
    try:
        # Create a new chat session with the specified model
        st.session_state.chat_session = client.chats.create(model=MODEL_NAME)
    except Exception as e:
        # This is where the InvalidArgument error occurs if the key is bad
        st.error(f"Failed to create chat session. Please verify your API Key and Cloud permissions. Error: {e}")
        st.stop()

# 4. Function to send message and update history
def send_message(prompt):
    """Sends the user message to the Gemini API and updates the chat history."""
    try:
        # Send message to the Gemini API
        response = st.session_state.chat_session.send_message(prompt)
        
        # Append user message to history
        st.session_state.chat_history.append({"role": "user", "text": prompt})
        
        # Append model response to history
        st.session_state.chat_history.append({"role": "model", "text": response.text})

    except Exception as e:
        st.error(f"An error occurred while communicating with the API: {e}")

# 5. Display Chat History
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# 6. Chat Input Handling
prompt = st.chat_input("Ask me anything...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    
    send_message(prompt)
    
    st.rerun()

# 7. Sidebar for App Info
st.sidebar.markdown("## App Details")
st.sidebar.markdown(f"**Model:** `{MODEL_NAME}`")
st.sidebar.markdown("This chatbot uses the `gemini-2.5-flash` model for fast and conversational responses.")
st.sidebar.markdown("---")
if st.sidebar.button("Clear Chat History"):
    st.session_state.chat_history = []
    # Re-initialize a new chat session when history is cleared
    st.session_state.chat_session = client.chats.create(model=MODEL_NAME)
    st.rerun()
