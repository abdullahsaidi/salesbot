# config.py

import os


MODEL_NAME = "openai/gpt-oss-120b"

# Which inference provider serves the model.
# "auto" lets Hugging Face pick an available provider for Qwen3-8B for you.
HF_PROVIDER = "auto"
# For a real-time sales chat "thinking mode" must be OFF: it adds seconds of delay 
DISABLE_THINKING = True

# Generation options sent to the chat completion endpoint.
# NOTE: The remote API uses the OpenAI-style parameter set. Ollama-only options
# like num_ctx, top_k and repeat_penalty are not part of it, so they were
# removed. The hosted model already runs with a large context window, so the
# old "model forgets its instructions" problem does not apply here.
GEN_OPTIONS = {
    # Qwen team's recommended sampling for non-thinking chat:
    "temperature": 0.4,
    "top_p": 0.8,
    # Cap on the length of a single reply (keeps sales answers short & fast):
    "max_tokens": 256,
}

# Number of conversation TURNS (user + assistant pairs) to keep in memory.
MAX_TURNS = 6

# First message the bot sends (Arabic, per business requirement).
FIRST_MESSAGE = "مرحباً! أنا هلا، المساعدة الافتراضية من زين الأردن 👋 معي دقيقة من وقتك؟ عندنا عروض جديدة ممكن توفّر عليك."


def get_groq_key():
    """Return the Groq API key from GROQ_API_KEY env var or Streamlit secrets."""
    key = os.environ.get("GROQ_API_KEY")
    if key:
        return key.strip()
    try:
        import streamlit as st
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return None
