# 📡 EchoMind — API Documentation

## Base URL
```
http://localhost:8000
```

---

## Endpoints

### `GET /`
Health check and endpoint list.

**Response:**
```json
{
  "name": "EchoMind API",
  "status": "running",
  "version": "0.1.0"
}
```

---

### `POST /chat`
Send a message and receive an AI response.

**Request:**
```json
{
  "message": "What is my name?"
}
```

**Response:**
```json
{
  "response": "Your name is Alex, as you mentioned earlier!",
  "memories_used": 2,
  "message_count": 5
}
```

---

### `GET /stats`
Get pipeline statistics.

**Response:**
```json
{
  "messages_this_session": 10,
  "history_length": 20,
  "total_memories": 5,
  "model": "llama3-8b-8192",
  "provider": "groq"
}
```

---

### `GET /memories`
Retrieve all stored memories.

**Response:**
```json
{
  "count": 3,
  "memories": [
    "User's name is Alex. They are a Python developer working on AI projects.",
    "User prefers concise explanations. Dislikes long introductions.",
    "User is learning LangChain and ChromaDB for their EchoMind project."
  ]
}
```

---

### `POST /save-fact`
Manually save an important fact to memory.

**Request:**
```json
{
  "fact": "I wake up at 6am every day"
}
```

**Response:**
```json
{
  "status": "saved",
  "fact": "I wake up at 6am every day"
}
```

---

### `POST /clear`
Clear current session history (long-term memory preserved).

**Response:**
```json
{
  "status": "cleared",
  "message": "Session history cleared"
}
```

---

### `DELETE /memories`
Delete ALL long-term memories. **Irreversible.**

**Response:**
```json
{
  "status": "deleted",
  "message": "All memories deleted"
}
```

---

## Running the API

```bash
# From project root
uvicorn app.api:app --reload --host 0.0.0.0 --port 8000

# Interactive docs available at:
# http://localhost:8000/docs
```
