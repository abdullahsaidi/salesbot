# chatbot.py

import re

from huggingface_hub import InferenceClient

from config import (
    MODEL_NAME,
    HF_PROVIDER,
    GEN_OPTIONS,
    DISABLE_THINKING,
    get_hf_token,
)
from prompts import SYSTEM_PROMPT
from offers import get_offers_prompt
from memory import ConversationMemory


# Removes any <think>...</think> block if the model leaks one
THINK_TAG_RE = re.compile(r"<think>.*?</think>", re.DOTALL)


class SalesChatbot:

    def __init__(self):
        self.memory = ConversationMemory()
        self.system_prompt = SYSTEM_PROMPT + "\n" + get_offers_prompt()

        # Build the Hugging Face Inference client once and reuse it.
        # The token is read from HF_TOKEN (env var) or Streamlit secrets.
        token = get_hf_token()
        if not token:
            raise RuntimeError(
                "No Hugging Face token found. Set HF_TOKEN as an environment "
                "variable, or add it to Streamlit secrets as HF_TOKEN."
            )

        self.client = InferenceClient(
            provider=HF_PROVIDER,   # "auto" -> HF picks a provider for Qwen3-8B
            api_key=token,
        )

    def chat(self, user_message):
        """Receive a user message and return the chatbot response."""
        self.memory.add_user_message(user_message)

        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.memory.get_messages())

        try:
            assistant_message = self._call_model(messages)
        except Exception as e:
            # Don't save a failed turn as if the bot replied
            self.memory.messages.pop()  # remove the user message we just added
            return (
                "عذراً، صار خطأ تقني مؤقت. جرّب مرة ثانية بعد لحظات 🙏\n"
                f"(Technical error: {e})"
            )

        self.memory.add_assistant_message(assistant_message)
        return assistant_message

    def _call_model(self, messages):
        # Work on a copy so we never mutate the stored conversation memory.
        request_messages = list(messages)

        if DISABLE_THINKING:
            # Qwen3's built-in soft switch: appending "/no_think" to the last
            # user turn tells the model to skip its internal reasoning step.
            # This works across all Hugging Face inference providers without
            # any provider-specific parameter.
            last = dict(request_messages[-1])
            last["content"] = last["content"] + " /no_think"
            request_messages[-1] = last

        # OpenAI-compatible chat completion call (via huggingface_hub).
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=request_messages,
            **GEN_OPTIONS,
        )

        content = response.choices[0].message.content

        # Safety net: strip any leaked thinking block and whitespace
        content = THINK_TAG_RE.sub("", content).strip()
        return content
