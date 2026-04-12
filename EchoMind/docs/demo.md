# 🎬 EchoMind — Demo Guide

## Quick Start (3 Steps)

```bash
# 1. Install
pip install -r requirements.txt

# 2. Add API key to .env
GROQ_API_KEY=your_key_here

# 3. Run
python app/main.py           # Terminal
streamlit run app/streamlit_app.py   # Web UI
uvicorn app.api:app --reload         # API
```

---

## Demo Script (For Portfolio / Interviews)

Run this exact conversation to show all features:

```
You: Hi! My name is Alex and I'm a Python developer.
You: I'm building an AI project called EchoMind.
You: My favorite programming language is Python.

--- Close terminal. Reopen. ---

You: Do you remember my name?
→ EchoMind should say: "Yes! Your name is Alex."

You: What project am I working on?
→ EchoMind should say: "You're building EchoMind."

You: /stats
→ Shows memory count > 0
```

This demonstrates **true long-term memory across sessions.**

---

## What to Highlight

1. **Memory persists** — close app, reopen, still remembers you
2. **Semantic search** — doesn't just keyword match, understands meaning
3. **Auto-summarization** — conversations become compact memories
4. **Full API** — can connect any frontend

---

## Common Issues

| Problem | Fix |
|---------|-----|
| `GROQ_API_KEY not found` | Check `.env` file exists with correct key |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `ChromaDB error` | Delete `models/saved/` folder and restart |
| Port 8000 in use | Change port: `uvicorn app.api:app --port 8001` |
