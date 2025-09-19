"""
RAG query endpoints for DocuBotAI.
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session

from docubotai.core.database import get_db
from docubotai.core.rag import RAGEngine
from docubotai.models.database import QueryHistory

router = APIRouter(prefix="/query", tags=["query"])

class QueryRequest(BaseModel):
    """Query request model."""
    text: str
    context: Optional[str] = None
    max_results: int = 5
    min_similarity: float = 0.7

class Source(BaseModel):
    """Source document model."""
    url: str
    title: str
    relevance: float

class QueryResponse(BaseModel):
    """Query response model."""
    answer: str
    sources: List[Source]
    confidence: float
    execution_time: float

    class Config:
        from_attributes = True

@router.post("/", response_model=QueryResponse)
async def query_documents(
    request: QueryRequest,
    db: Session = Depends(get_db)
):
    """Query the RAG system."""
    try:
        rag_engine = RAGEngine()
        result = await rag_engine.query(
            query=request.text,
            context=request.context,
            max_results=request.max_results,
            min_similarity=request.min_similarity
        )
        
        # Store query history
        history = QueryHistory(
            query=request.text,
            context=request.context,
            answer=result.answer,
            confidence=result.confidence
        )
        db.add(history)
        db.commit()
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=List[QueryResponse])
async def get_query_history(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get recent query history."""
    history = db.query(QueryHistory).order_by(
        QueryHistory.created_at.desc()
    ).limit(limit).all()
    return history

@router.delete("/history")
async def clear_query_history(db: Session = Depends(get_db)):
    """Clear query history."""
    db.query(QueryHistory).delete()
    db.commit()
    return {"status": "success", "message": "Query history cleared"}