# Hala — Bilingual LLM Sales Chatbot

An outbound sales chatbot prototype built during my internship in the Commercial Support department at **Zain Jordan**. The assistant, **"Hala" (هلا)**, starts the conversation, learns what the customer needs through short questions, and recommends the single best-fitting mobile or home-internet offer in a warm, natural Jordanian tone.

> **Note:** the offers in `offers.py` are **fictional placeholders** created for this prototype. They are not real Zain prices or plans.

## Features

- **Arabic, English and Arabizi**: replies in the customer's language, understands Arabic written in Latin letters (e.g. *shu el 3orood*), and never mixes two languages in one message.
- **Guided sales flow**: Hook → Discover → Recommend → Close, asking one short question per message.
- **Grounded recommendations**: the bot only recommends offers from the catalog and matches them to the customer using offer tags (budget, usage, household). It never invents prices, discounts or bundles.
- **Objection handling**: handles "it's expensive", competitor comparisons, existing-plan upgrades and "maybe later", and backs off politely after two refusals.
- **Conversation memory**: keeps the last turns, trimmed by whole user/assistant pairs so the context stays coherent.
- **Guardrails**: no personal data collection, hands support questions to the support line, strips leaked `<think>` reasoning, and falls back gracefully on API errors and rate limits.
- **Conversation logging**: every turn is saved to Google Sheets (timestamp, session ID, user message, bot reply) for review and prompt iteration.

## Tech stack

Python · Streamlit · Groq API (`openai/gpt-oss-120b`) · Prompt engineering · Google Sheets API (gspread)

## Project structure

| File | Purpose |
|---|---|
| `app.py` | Streamlit chat interface |
| `main.py` | Command-line version of the chatbot |
| `chatbot.py` | Core logic: builds the prompt, calls the model through Groq, handles errors |
| `prompts.py` | Hala's system prompt: role, language rules, sales flow, objection handling, examples |
| `offers.py` | Catalog of (fictional) mobile and internet offers, with tags used for matching |
| `memory.py` | Conversation history, trimmed by whole turns |
| `storage.py` | Logs each conversation turn to Google Sheets |
| `config.py` | Model name, generation settings, first message, API key loader |

## Run locally

```bash
pip install -r requirements.txt
```

Set your Groq API key (free at [console.groq.com](https://console.groq.com/keys)) as an environment variable, or put it in `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "your_groq_key"
```

Then start the web app:

```bash
streamlit run app.py
```

or the command-line version:

```bash
python main.py
```

**Optional: Google Sheets logging.** Add a Google service-account JSON to `.streamlit/secrets.toml` under `[gcp_service_account]` and share a sheet named `sales_chatbot_logs` with that service account. Without it, the chat works normally and logging is skipped.

`.streamlit/secrets.toml` is listed in `.gitignore`, so keys are never committed.

## Configuration

Everything tunable lives in `config.py`: `MODEL_NAME`, sampling options (`temperature`, `top_p`, `max_tokens`), `MAX_TURNS` for memory length, and `FIRST_MESSAGE`. Edit `offers.py` to change the catalog and `prompts.py` to change Hala's personality or sales rules.
