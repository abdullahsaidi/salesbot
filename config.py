# config.py

import os

# ============ MODEL SELECTION (Hugging Face Inference Providers) ============
# We now call Qwen3-8B remotely through Hugging Face instead of running it
# locally with Ollama. This is the exact model id on the Hugging Face Hub:
#   https://huggingface.co/Qwen/Qwen3-8B
# The Inference Providers system routes this to a hosted backend
# (Together, Cerebras, Groq, Novita, DeepInfra, ...), so no GPU is needed
# on the machine running this app — which is what makes Streamlit Cloud work.
MODEL_NAME = "Qwen/Qwen3-8B"

# Which inference provider serves the model.
# "auto" lets Hugging Face pick an available provider for Qwen3-8B for you.
# You can pin a specific one later if you want (e.g. "together", "novita").
HF_PROVIDER = "auto"

# Qwen3 has a "thinking mode" (internal reasoning before answering).
# For a real-time sales chat it must be OFF: it adds seconds of delay and the
# thinking text can leak into replies. We disable it with Qwen3's built-in
# "/no_think" soft switch (see chatbot.py) and strip any leaked <think> blocks.
DISABLE_THINKING = True

# Generation options sent to the chat completion endpoint.
# NOTE: The remote API uses the OpenAI-style parameter set. Ollama-only options
# like num_ctx, top_k and repeat_penalty are not part of it, so they were
# removed. The hosted model already runs with a large context window, so the
# old "model forgets its instructions" problem does not apply here.
GEN_OPTIONS = {
    # Qwen team's recommended sampling for non-thinking chat:
    "temperature": 0.7,
    "top_p": 0.8,
    # Cap on the length of a single reply (keeps sales answers short & fast):
    "max_tokens": 512,
}

# Number of conversation TURNS (user + assistant pairs) to keep in memory.
MAX_TURNS = 12

# First message the bot sends (Arabic, per business requirement).
FIRST_MESSAGE = "مرحباً! أنا هلا، المساعدة الافتراضية من زين الأردن 👋 معي دقيقة من وقتك؟ عندنا عروض جديدة ممكن توفّر عليك."


def get_hf_token():
    """
    Return the Hugging Face access token.

    Looked up in this order so the SAME code works everywhere:
      1) Environment variable HF_TOKEN
         -> used for local runs and the command-line version (main.py).
      2) Streamlit secrets (st.secrets["HF_TOKEN"])
         -> used when deployed on Streamlit Cloud.

    Returns None if no token is configured, so the app can show a clear message.
    """
    # 1) Environment variable (local terminal, `export HF_TOKEN=...`)
    token = os.environ.get("HF_TOKEN")
    if token:
        return token.strip()

    # 2) Streamlit Cloud secrets. Wrapped in try/except because streamlit
    #    is not always running (e.g. the CLI in main.py).
    try:
        import streamlit as st
        return st.secrets["HF_TOKEN"]
    except Exception:
        return None
