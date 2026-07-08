from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.database.session import get_db
from backend.database.models import User, Document, Chunk, Conversation, Feedback, Message
from backend.models.schemas import AnalyticsResponse
from backend.api.deps import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin Analytics"])

@router.get("/analytics", response_model=AnalyticsResponse)
def get_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Total documents uploaded by the user
    document_count = db.query(Document).filter(Document.user_id == current_user.id).count()

    # Total chunks created from the user's documents
    chunk_count = (
        db.query(Chunk)
        .join(Document)
        .filter(Document.user_id == current_user.id)
        .count()
    )

    # Total conversation sessions started by the user
    conversation_count = db.query(Conversation).filter(Conversation.user_id == current_user.id).count()

    # Average rating from message feedback for the user's messages
    avg_rating_query = (
        db.query(func.avg(Feedback.rating))
        .join(Message)
        .join(Conversation)
        .filter(Conversation.user_id == current_user.id)
        .scalar()
    )
    average_rating = float(avg_rating_query) if avg_rating_query is not None else 0.0

    return {
        "document_count": document_count,
        "chunk_count": chunk_count,
        "conversation_count": conversation_count,
        "average_rating": round(average_rating, 2)
    }
