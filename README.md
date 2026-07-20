# Zain Sales Bot (Qwen3-8B via Hugging Face)

A bilingual (Arabic/English) outbound sales chatbot "Hala" for Zain Jordan.
It uses **Qwen3-8B** hosted on **Hugging Face Inference Providers**, so it runs
with no local GPU and can be deployed for free on **Streamlit Cloud**.

Model: https://huggingface.co/Qwen/Qwen3-8B

## 1. Get a Hugging Face token
1. Create a free account at https://huggingface.co
2. Go to https://huggingface.co/settings/tokens
3. Create a token (type: **Read** is enough) and copy it (starts with `hf_...`).

## 2. Run locally
```bash
pip install -r requirements.txt
export HF_TOKEN="hf_your_token_here"      # Windows PowerShell: $env:HF_TOKEN="hf_..."
streamlit run app.py
```
Command-line version (optional): `export HF_TOKEN=...` then `python main.py`

## 3. Deploy on Streamlit Cloud
1. Push this folder to a **public GitHub repo**.
2. Go to https://share.streamlit.io → **Create app** → pick your repo.
3. Main file path: `app.py`
4. Open **Advanced settings → Secrets** and paste:
   ```
   HF_TOKEN = "hf_your_token_here"
   ```
5. **Deploy**. You'll get a public link like `https://your-app.streamlit.app`
   that you can share with anyone.
