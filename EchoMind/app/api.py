# =============================================
# EchoMind — FastAPI Backend
# =============================================

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.pipeline import EchoMindPipeline
from src.utils import setup_logger

os.makedirs("logs", exist_ok=True)
logger = setup_logger()

# ─── FastAPI App ───────────────────────────
app = FastAPI(
    title="EchoMind API",
    description="AI Chatbot with long-term memory",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ─── Global Pipeline ───────────────────────
pipeline = EchoMindPipeline()


# ─── Request/Response Models ───────────────
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    memories_used: int
    message_count: int

class FactRequest(BaseModel):
    fact: str

class StatsResponse(BaseModel):
    messages_this_session: int
    history_length: int
    total_memories: int
    model: str
    provider: str


# ─── Routes ────────────────────────────────
@app.get("/")
def root():
    return {
        "name": "EchoMind API",
        "status": "running",
        "version": "0.1.0",
        "endpoints": ["/chat", "/stats", "/memories", "/save-fact", "/clear"]
    }


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """Send a message and get AI response."""
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        # Get memories before chat for count
        memories = pipeline.memory.retrieve(req.message)
        response = pipeline.chat(req.message)

        return ChatResponse(
            response=response,
            memories_used=len(memories),
            message_count=pipeline.message_count
        )
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats", response_model=StatsResponse)
def get_stats():
    """Get pipeline statistics."""
    return pipeline.get_stats()


@app.get("/memories")
def get_memories():
    """Get all stored memories."""
    memories = pipeline.memory.get_all()
    return {
        "count": len(memories),
        "memories": memories
    }


@app.post("/save-fact")
def save_fact(req: FactRequest):
    """Manually save a fact to memory."""
    if not req.fact.strip():
        raise HTTPException(status_code=400, detail="Fact cannot be empty")
    pipeline.save_fact(req.fact)
    return {"status": "saved", "fact": req.fact}


@app.post("/clear")
def clear_session():
    """Clear current session history."""
    pipeline.clear_history()
    return {"status": "cleared", "message": "Session history cleared"}


@app.delete("/memories")
def delete_all_memories():
    """Delete ALL memories (irreversible)."""
    pipeline.clear_all_memory()
    return {"status": "deleted", "message": "All memories deleted"}


# ─── Run ───────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)
