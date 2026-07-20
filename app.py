# app.py

import streamlit as st

from chatbot import SalesChatbot
from config import FIRST_MESSAGE, get_hf_token


st.set_page_config(page_title="Zain Sales Bot", page_icon="🤖")

st.title("🤖 Zain Sales Bot")

# ---- Make sure a Hugging Face token is configured before doing anything ----
# On Streamlit Cloud you add it under: App settings -> Secrets  (as HF_TOKEN).
# Locally you can `export HF_TOKEN=...` before running.
if not get_hf_token():
    st.error(
        "⚠️ No Hugging Face token found.\n\n"
        "Add a secret named **HF_TOKEN** in your Streamlit Cloud app settings "
        "(App → Settings → Secrets), or set the HF_TOKEN environment variable "
        "when running locally. See the setup notes for step-by-step help."
    )
    st.stop()

# Create the chatbot once per session (after we know the token exists).
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
