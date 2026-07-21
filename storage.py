# storage.py

from datetime import datetime

import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

# same name in google drive
SHEET_NAME = "sales_chatbot_logs"

# headline
HEADERS = ["timestamp", "session_id", "user_message", "bot_reply"]

# read / write authrrization
_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


@st.cache_resource
def _get_worksheet():
    """connects to Google Sheets once and reuses the same connection"""
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],   # from Secrets
        scopes=_SCOPES,
    )
    client = gspread.authorize(creds)
    worksheet = client.open(SHEET_NAME).sheet1

    # if sheet is empty write the headline
    if not worksheet.get_all_values():
        worksheet.append_row(HEADERS)

    return worksheet


def save_turn(session_id, user_message, bot_reply):
    """Adds a conversation role as a class. Returns True if successful, and False if it fails (without breaking the chat)."""
    try:
        worksheet = _get_worksheet()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        worksheet.append_row([timestamp, session_id, user_message, bot_reply])
        return True
    except Exception as e:
        # log the error. without stopping the conversaiton
        print(f"[storage] تعذّر حفظ المحادثة: {e}")
        return False