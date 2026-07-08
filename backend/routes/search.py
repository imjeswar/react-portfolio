from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.models.schemas import SearchRequest, SearchResponse
from backend.api.deps import get_current_user
from backend.database.models import User, Chunk
from backend.rag.chat.orchestrator import RAGChatOrchestrator

router = APIRouter(prefix="/search", tags=["Search"])
orchestrator = RAGChatOrchestrator()

@router.post("/", response_model=SearchResponse)
def search_chunks(
    request: SearchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Fetch user's chunks to execute BM25 over
    db_chunks = orchestrator._get_user_chunks(db, current_user.id)
    if not db_chunks:
        return {"chunks": []}

    # Perform Hybrid retrieval
    retrieved = orchestrator.retriever.retrieve(
        query=request.query,
        db_chunks=db_chunks,
        top_k=request.top_k or 5,
        filter_dict={"user_id": current_user.id}
    )

    formatted_chunks = []
    for chunk in retrieved:
        formatted_chunks.append({
            "id": str(chunk.get("id")),
            "text": chunk.get("text", ""),
            "metadata": chunk.get("metadata", {}),
            "score": float(chunk.get("score") or chunk.get("rrf_score") or 0.0)
        })

    return {"chunks": formatted_chunks}
