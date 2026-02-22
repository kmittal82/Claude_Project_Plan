# EquityIQ — Equity Compensation Assistant

An AI-powered assistant that answers equity compensation questions at **CEP Level 1** depth. Built with Streamlit and Claude (Anthropic).

---

## Prerequisites

- Python 3.9+
- An [Anthropic API key](https://console.anthropic.com/)

---

## Local Development

### 1. Clone & navigate
```bash
git clone <your-repo-url>
cd equity-admin-bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
```bash
cp .env.example .env
```
Open `.env` and add your key:
```
ANTHROPIC_API_KEY=sk-ant-...
```

### 4. Run the app
```bash
streamlit run app.py
```

The app opens at **http://localhost:8501**

---

## Deploy to Streamlit Community Cloud (Free)

Streamlit Cloud is the easiest way to share the app publicly at no cost.

### 1. Push your code to GitHub
Make sure `.env` is in `.gitignore` (it already is). Commit and push your code.

### 2. Sign in to Streamlit Cloud
Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.

### 3. Create a new app
- Click **"New app"**
- Select your repository and branch
- Set **Main file path** to `equity-admin-bot/app.py` (or `app.py` if the repo root is the app folder)

### 4. Add your API key as a secret
In the app settings, click **"Advanced settings" → "Secrets"** and add:
```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

### 5. Deploy
Click **"Deploy!"** — your app will be live at a public URL like:
`https://your-app-name.streamlit.app`

---

## Deploy to a VPS / Server (e.g. AWS, DigitalOcean)

### 1. Install dependencies on the server
```bash
pip install -r requirements.txt
```

### 2. Set environment variables
```bash
export ANTHROPIC_API_KEY=sk-ant-...
```
Or create a `.env` file on the server.

### 3. Run with nohup (keeps it alive after logout)
```bash
nohup streamlit run app.py --server.port 8501 --server.headless true &
```

### 4. (Optional) Reverse proxy with Nginx
Point your domain to port 8501 via an Nginx reverse proxy for a clean URL and HTTPS.

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `ANTHROPIC_API_KEY` | ✅ Yes | — | Your Anthropic API key |
| `CLAUDE_MODEL` | No | `claude-opus-4-6` | Override the Claude model |

---

## Project Structure

```
equity-admin-bot/
├── app.py              # Main Streamlit application
├── system_prompt.py    # CEP Level 1 knowledge base & system prompt
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── .env                # Your local secrets (never commit this)
├── .gitignore
├── README.md
└── .streamlit/
    └── config.toml     # Dark theme configuration
```
