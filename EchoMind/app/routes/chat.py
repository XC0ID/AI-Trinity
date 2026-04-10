# =============================================
# EchoMind — Chat Routes
# =============================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["Chat"])


class MessageRequest(BaseModel):
    message: str
    save_memory: bool = True


@router.post("/send")
def send_message(req: MessageRequest):
    """Send message to EchoMind."""
    from app.api import pipeline

    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message is empty")

    response = pipeline.chat(req.message)
    return {"response": response}


@router.get("/history")
def get_history():
    """Get current session chat history."""
    from app.api import pipeline
    return {"history": pipeline.history}


@router.delete("/history")
def clear_history():
    """Clear session history."""
    from app.api import pipeline
    pipeline.clear_history()
    return {"status": "cleared"}
