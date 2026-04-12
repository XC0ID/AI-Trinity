# 🧠 EchoMind — System Architecture

## Overview

EchoMind is a conversational AI with long-term memory. Unlike regular chatbots that forget everything when you close the tab, EchoMind stores everything in a vector database and retrieves relevant context for every new conversation.

---

## System Flow

```
User Input
    │
    ▼
┌─────────────────────────────────────┐
│           EchoMindPipeline          │
│                                     │
│  1. Clean & validate input          │
│  2. Retrieve relevant memories      │  ◄── ChromaDB (Vector DB)
│  3. Build context (memory + history)│
│  4. Send to LLM                     │  ◄── Groq / OpenAI
│  5. Get response                    │
│  6. Update short-term history       │
│  7. Auto-save memory every 5 msgs   │  ──► ChromaDB
│                                     │
└─────────────────────────────────────┘
    │
    ▼
Response to User
```

---

## Components

### 1. `EchoMindModel` — The Brain
- Connects to Groq (LLaMA3) or OpenAI (GPT)
- Sends messages with full context
- Also used for summarization

### 2. `EchoMindMemory` — The Memory
- ChromaDB vector database
- Stores conversation summaries
- Retrieves top-N relevant memories via semantic search
- Uses `all-MiniLM-L6-v2` for embeddings

### 3. `EchoMindPipeline` — The Orchestrator
- Combines Model + Memory
- Manages short-term history (last 20 messages)
- Auto-saves memory every 5 messages
- Exposes simple `chat()` interface

---

## Memory Architecture

```
Short-Term Memory          Long-Term Memory
─────────────────          ─────────────────
In-memory list             ChromaDB on disk
Last 20 messages           Unlimited storage
Lost on restart            Persists forever
Fast access                Semantic search
```

---

## API Endpoints

| Method | Endpoint        | Description              |
|--------|----------------|--------------------------|
| POST   | /chat           | Send message             |
| GET    | /stats          | Get pipeline stats       |
| GET    | /memories       | Get all memories         |
| POST   | /save-fact      | Save a fact to memory    |
| POST   | /clear          | Clear session            |
| DELETE | /memories       | Delete all memories      |

---

## Tech Stack

| Component     | Technology              |
|--------------|-------------------------|
| LLM          | Groq API (LLaMA3)       |
| Vector DB    | ChromaDB                |
| Embeddings   | sentence-transformers   |
| Web UI       | Streamlit               |
| API Backend  | FastAPI                 |
| Config       | PyYAML                  |
| Logging      | Loguru                  |
| Testing      | Pytest                  |
