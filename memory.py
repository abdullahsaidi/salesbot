# memory.py

from config import MAX_TURNS


class ConversationMemory:
    """
    Stores conversation history and trims it by WHOLE turns
    (user + assistant pairs), so the history never starts with
    an assistant message or splits a pair — which confuses models.
    """

    def __init__(self):
        self.messages = []

    def add_user_message(self, message):
        self.messages.append({"role": "user", "content": message})
        self._trim_history()

    def add_assistant_message(self, message):
        self.messages.append({"role": "assistant", "content": message})
        self._trim_history()

    def get_messages(self):
        return self.messages

    def clear(self):
        self.messages = []

    def _trim_history(self):
        max_messages = MAX_TURNS * 2
        if len(self.messages) <= max_messages:
            return

        # Cut oldest messages, then make sure history starts with a user message
        self.messages = self.messages[-max_messages:]
        while self.messages and self.messages[0]["role"] != "user":
            self.messages.pop(0)
