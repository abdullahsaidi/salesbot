Readme · MD
🤖 Zain Sales Bot

A bilingual (Arabic / English) outbound sales chatbot for Zain Jordan. The assistant, "Hala" (هلا), proactively greets the customer, discovers their needs through short questions, and recommends the best-fitting mobile or home internet offer — all in a warm, natural Jordanian tone.

Powered by Qwen3-8B running on Hugging Face Inference Providers, so it needs no local GPU and deploys for free on Streamlit Cloud with a shareable public link.

Model: Qwen/Qwen3-8B

✨ Features
Bilingual & Arabizi-aware — replies in Arabic to Arabic, English to English, and understands Arabic written in Latin letters (e.g. shu el 3orood).
Proactive sales flow — greets first, then moves through Hook → Discover → Recommend → Close, one short question at a time.
Grounded recommendations — only suggests real offers defined in offers.py; never invents prices, discounts, or bundles.
Objection handling — responds to "it's expensive", "I already have a plan", and "maybe later", and backs off politely after two refusals.
Conversation memory — keeps the last several turns so the chat stays coherent without losing its instructions.
Fast, no-GPU inference — Qwen3's "thinking mode" is disabled for quick replies, with a safety net that strips any leaked reasoning.
📁 Project structure
File	Purpose
app.py	Streamlit web interface (the chat UI).
main.py	Command-line version of the chatbot.
chatbot.py	Core logic: calls Qwen3-8B via Hugging Face and manages a turn.
config.py	Model, generation settings, and the token loader.
prompts.py	The "Hala" system prompt (role, language rules, sales flow).
offers.py	The catalog of mobile & internet offers.
memory.py	Trims conversation history by whole turns.
requirements.txt	Python dependencies.
.streamlit/secrets.toml.example	Template for your local token file.
🔑 Prerequisites: a Hugging Face token

The app authenticates with one Hugging Face token that belongs to you, the owner — the people you share the app with do not need an account or token.

Sign up (free) at huggingface.co.
Open Settings → Access Tokens.
Create a token (type Read is enough) and copy it — it starts with hf_....

⚠️ Never commit your real token to GitHub. The included .gitignore already excludes .streamlit/secrets.toml for this reason.

💻 Run locally

Install dependencies:

bash
pip install -r requirements.txt

Provide your token, then launch. Pick the option for your shell:

Option A — a secrets file (recommended, set it once): Copy .streamlit/secrets.toml.example to .streamlit/secrets.toml and put your token inside:

HF_TOKEN = "hf_your_token_here"

Then just run:

bash
streamlit run app.py

Option B — an environment variable (per session):

bash
# Windows (CMD):        set HF_TOKEN=hf_your_token_here
# Windows (PowerShell): $env:HF_TOKEN="hf_your_token_here"
# macOS / Linux:        export HF_TOKEN="hf_your_token_here"
streamlit run app.py

The app opens at http://localhost:8501. Command-line version instead: set the token the same way, then python main.py.

🚀 Deploy on Streamlit Cloud (public link)
Push this project to a public GitHub repo (without secrets.toml).
Go to share.streamlit.io and sign in with GitHub.
Create app → select your repo → set Main file path to app.py.
Open Advanced settings → Secrets and paste:
   HF_TOKEN = "hf_your_token_here"
Click Deploy. You'll get a public URL like https://your-app.streamlit.app that anyone can open in a browser — no install, no login, no token needed on their side.

To update the token later: App → Settings → Secrets, edit it, and reboot.

⚙️ Configuration

Everything tunable lives in config.py:

MODEL_NAME — the Hugging Face model id (Qwen/Qwen3-8B).
HF_PROVIDER — "auto" lets Hugging Face pick a backend; you can pin one (e.g. "together", "cerebras") for more consistent latency.
GEN_OPTIONS — sampling settings: temperature, top_p, and max_tokens.
MAX_TURNS — how many user+assistant pairs to keep in memory.
FIRST_MESSAGE — the opening line Hala sends.

To change the offers themselves, edit offers.py. To change Hala's personality or sales rules, edit prompts.py.

📝 Notes
The Hugging Face free tier includes a small monthly inference credit — fine for demos and small teams. Heavy usage may need a PRO account or your own provider key.
A public Streamlit link is open to anyone who has it. Restricting access to specific emails requires a paid Streamlit plan.
