# app.py
import uuid

import streamlit as st

from chatbot import SalesChatbot
from config import FIRST_MESSAGE, get_groq_key
from storage import save_turn


st.set_page_config(page_title="Zain Sales Bot", page_icon="🤖")

st.title("🤖 Zain Sales Bot")


if not get_groq_key():
    st.error(
        "⚠️ No Groq API key found.\n\n"
        "Add a secret named **GROQ_API_KEY** in your Streamlit Cloud app settings "
        "(App → Settings → Secrets), or set the GROQ_API_KEY environment variable "
        "when running locally."
    )
    st.stop()


# Generate a unique ID for this conversation once.
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Create the chatbot once per session (after we know the token exists).
if "chatbot" not in st.session_state:
    st.session_state.chatbot = SalesChatbot()


if "chatbot" not in st.session_state:
    st.session_state.chatbot = SalesChatbot()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": FIRST_MESSAGE}
    ]

# Sidebar: reset conversation
with st.sidebar:
    if st.button("🔄 محادثة جديدة / New chat"):
        st.session_state.chatbot = SalesChatbot()
        st.session_state.session_id = str(uuid.uuid4())  # new chat= new id
        st.session_state.messages = [
            {"role": "assistant", "content": FIRST_MESSAGE}
        ]
        st.rerun()


# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("اكتب رسالتك هنا... / Type your message...")

if user_input:
    # Show the user's message immediately (before the model responds)
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Generate response with a spinner
    with st.chat_message("assistant"):
        with st.spinner("..."):
            response = st.session_state.chatbot.chat(user_input)
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    save_turn(st.session_state.session_id, user_input, response)
