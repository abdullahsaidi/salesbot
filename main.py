# main.py

import sys

sys.stdout.reconfigure(encoding="utf-8")

from chatbot import SalesChatbot
from config import FIRST_MESSAGE


EXIT_COMMANDS = {
    "exit", "quit", "bye",
    "خروج", "انهاء", "إنهاء", "مع السلامة",
}


def is_exit(message):
    return message.strip().lower() in EXIT_COMMANDS


def contains_arabic(text):
    return any("\u0600" <= ch <= "\u06FF" for ch in text)


def main():
    chatbot = SalesChatbot()

    print("Bot:")
    print(FIRST_MESSAGE)

    while True:
        user_message = input("\nYou: ").strip()

        if not user_message:
            continue

        if is_exit(user_message):
            print("\nBot:")
            if contains_arabic(user_message):
                print("شكراً لوقتك، نتمنى لك يوماً سعيداً 🌟")
            else:
                print("Thank you for your time. Have a great day! 🌟")
            break  # only break on an actual exit command

        response = chatbot.chat(user_message)

        print("\nBot:")
        print(response)


if __name__ == "__main__":
    main()
