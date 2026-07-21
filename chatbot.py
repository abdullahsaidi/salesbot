# chatbot.py

import re

from groq import Groq

from config import MODEL_NAME, GEN_OPTIONS, get_groq_key
from prompts import SYSTEM_PROMPT
from offers import get_offers_prompt
from memory import ConversationMemory


THINK_TAG_RE = re.compile(r"<think>.*?</think>", re.DOTALL)


class SalesChatbot:

    def __init__(self):
        self.memory = ConversationMemory()
        self.system_prompt = SYSTEM_PROMPT + "\n" + get_offers_prompt()

        key = get_groq_key()
        if not key:
            raise RuntimeError(
                "No Groq API key found. Set GROQ_API_KEY as an environment "
                "variable, or add it to Streamlit secrets as GROQ_API_KEY."
            )

        self.client = Groq(api_key=key)

    def chat(self, user_message):
        self.memory.add_user_message(user_message)

        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.memory.get_messages())

        try:
            assistant_message = self._call_model(messages)
        except Exception as e:
            self.memory.messages.pop()
            error_text = str(e)

            if "401" in error_text or "invalid_api_key" in error_text.lower():
                return (
                    "⚠️ مفتاح Groq غير صحيح أو ناقص.\n"
                    "أنشئ مفتاح من https://console.groq.com/keys وحدّثه بالإعدادات.\n"
                    f"(Auth error: {e})"
                )
            if "429" in error_text or "rate" in error_text.lower():
                return "وصلنا الحد المؤقت للطلبات 🙏 جرّب بعد دقيقة."

            return (
                "عذراً، صار خطأ تقني مؤقت. جرّب مرة ثانية بعد لحظات 🙏\n"
                f"(Technical error: {e})"
            )

        self.memory.add_assistant_message(assistant_message)
        return assistant_message

    def _call_model(self, messages):
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            **GEN_OPTIONS,
        )
        content = response.choices[0].message.content
        content = THINK_TAG_RE.sub("", content).strip()
        return content
