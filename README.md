# Customer Support Chatbot (Hugging Face + Flask + Vercel)

A ready-to-deploy customer support chatbot.

- **Backend:** Flask (`app.py`), calling Hugging Face's OpenAI-compatible
  Inference Providers router — auth'd with your **Hugging Face API key**.
- **Frontend:** `public/index.html` — a self-contained chat widget.
- **Deployment target:** Vercel (zero-config for Flask — no `vercel.json` needed).

---

## 1. Get a Hugging Face API key

https://huggingface.co/settings/tokens → create a **Read** token.

## 2. Run locally (optional, to test first)

```bash
pip install -r requirements.txt
cp .env.example .env      # then paste your HF_API_KEY into .env
python app.py
```

Backend runs at `http://localhost:5000`. Open `public/index.html` directly
in your browser to test the chat (it auto-detects local `file://` mode and
points at `localhost:5000`).

## 3. Push this project to GitHub

From inside this project folder:

```bash
git init
git add .
git commit -m "Initial commit: customer support chatbot"
```

Create the GitHub repo (pick ONE way):

**Option A — GitHub CLI (if installed):**
```bash
gh repo create customer-support-bot --public --source=. --remote=origin --push
```

**Option B — via github.com:**
1. Go to https://github.com/new, name it (e.g. `customer-support-bot`), don't
   initialize with a README (you already have one).
2. Then run:
```bash
git remote add origin https://github.com/<your-username>/customer-support-bot.git
git branch -M main
git push -u origin main
```

> Your `.env` file is git-ignored on purpose — never commit your real API key.

## 4. Connect to Vercel

**Option A — via Vercel dashboard (easiest):**
1. Go to https://vercel.com/new
2. Import the GitHub repo you just pushed
3. Framework preset: leave as "Other" (Vercel auto-detects the Flask `app`)
4. Before deploying (or right after, then redeploy), go to
   **Project → Settings → Environment Variables** and add:
   - `HF_API_KEY` = your Hugging Face token
   - `HF_MODEL` = e.g. `meta-llama/Llama-3.1-8B-Instruct:novita`
   - `COMPANY_NAME` = your company/product name
5. Click **Deploy**

**Option B — via Vercel CLI:**
```bash
npm install -g vercel
vercel login
vercel            # deploys a preview
vercel env add HF_API_KEY
vercel env add HF_MODEL
vercel env add COMPANY_NAME
vercel --prod     # deploy to production once env vars are set
```

Once deployed, your site (e.g. `https://customer-support-bot.vercel.app`)
serves the chat widget from `/` and the API from `/api/chat` — same origin,
so no CORS config needed.

## 5. Redeploying after changes

Just push to GitHub — Vercel auto-deploys on every push to `main` (and
creates preview deployments for other branches/PRs):

```bash
git add .
git commit -m "Update bot behavior"
git push
```

---

## Customizing the bot

Edit `SYSTEM_PROMPT` in `app.py` — tone, escalation rules, company policies.

## Project structure

```
customer-support-bot/
├── app.py              # Flask app — Vercel's zero-config entrypoint
├── requirements.txt
├── .env.example        # copy to .env for local dev only
├── .gitignore
├── public/
│   └── index.html      # chat widget, served as a static asset by Vercel
└── README.md
```
