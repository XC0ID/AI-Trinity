# =============================================
# EchoMind — Memory Routes
# =============================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/memory", tags=["Memory"])


class FactRequest(BaseModel):
    fact: str


@router.get("/all")
def get_all_memories():
    """Get all stored memories."""
    from app.api import pipeline
    memories = pipeline.memory.get_all()
    return {"count": len(memories), "memories": memories}


@router.post("/save")
def save_memory(req: FactRequest):
    """Save a specific fact to memory."""
    from app.api import pipeline
    if not req.fact.strip():
        raise HTTPException(status_code=400, detail="Fact is empty")
    pipeline.save_fact(req.fact)
    return {"status": "saved", "fact": req.fact}


@router.get("/search")
def search_memory(query: str):
    """Search memories by query."""
    from app.api import pipeline
    memories = pipeline.memory.retrieve(query)
    return {"query": query, "results": memories}


@router.delete("/all")
def delete_all():
    """Delete all memories."""
    from app.api import pipeline
    pipeline.clear_all_memory()
    return {"status": "all memories deleted"}
