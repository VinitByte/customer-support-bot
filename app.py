import os
import logging
from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("support-bot")

app = Flask(__name__, static_folder="public", static_url_path="")

HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL = os.getenv("HF_MODEL", "meta-llama/Llama-3.1-8B-Instruct:novita")
COMPANY_NAME = os.getenv("COMPANY_NAME", "Our Company")

if not HF_API_KEY:
    logger.warning("HF_API_KEY is not set. Set it in .env locally or in Render env vars.")

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_API_KEY,
)

SYSTEM_PROMPT = """You are a warm, professional customer support assistant for {company}.

Guidelines:
- Be concise, friendly, and to the point. Avoid corporate fluff.
- If you don't know the answer or it needs account-specific/private data you don't have, \
say so honestly and offer to escalate to a human agent.
- Ask a clarifying question if the user's request is ambiguous, instead of guessing.
- Never make up policies, prices, order details, or tracking numbers.
- Keep responses short (2-5 sentences) unless the user asks for detail.
- Stay polite even if the user is frustrated or rude.
"""

MAX_HISTORY_MESSAGES = 20


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    history = data.get("history") or []

    if not message:
        return jsonify({"error": "message is required"}), 400

    if not HF_API_KEY:
        return jsonify({
            "error": "Server is missing HF_API_KEY. Set it in Render Environment Variables."
        }), 500

    trimmed_history = history[-MAX_HISTORY_MESSAGES:]

    messages = [{"role": "system", "content": SYSTEM_PROMPT.format(company=COMPANY_NAME)}]
    messages.extend(trimmed_history)
    messages.append({"role": "user", "content": message})

    try:
        completion = client.chat.completions.create(
            model=HF_MODEL,
            messages=messages,
            max_tokens=500,
            temperature=0.6,
        )
        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as exc:
        logger.exception("HF chat completion failed")
        return jsonify({"error": f"Upstream error: {exc}"}), 502


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "model": HF_MODEL,
        "company": COMPANY_NAME,
        "hf_key_configured": bool(HF_API_KEY),
    })


if __name__ == "__main__":
    app.run(debug=True, port=int(os.getenv("PORT", "5000")))
