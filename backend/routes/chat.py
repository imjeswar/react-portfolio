from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import json
from datetime import datetime

from backend.database.session import get_db
from backend.database.models import User, Conversation, Message, Feedback
from backend.models.schemas import ChatRequest, ChatResponse, FeedbackRequest, ConversationResponse, MessageResponse
from backend.api.deps import get_current_user
from backend.rag.chat.orchestrator import RAGChatOrchestrator

router = APIRouter(prefix="/chat", tags=["Chat"])
orchestrator = RAGChatOrchestrator()

@router.post("/", response_model=ChatResponse)
def chat_sync(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Resolve or create conversation
    if request.conversation_id:
        conversation = db.query(Conversation).filter(
            Conversation.id == request.conversation_id,
            Conversation.user_id == current_user.id
        ).first()
        if not conversation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    else:
        # Create a new conversation using the question as title template
        title = request.question[:40] + ("..." if len(request.question) > 40 else "")
        conversation = Conversation(user_id=current_user.id, title=title)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    # 2. Save user message to SQL DB
    user_msg = Message(
        conversation_id=conversation.id,
        sender="user",
        text=request.question
    )
    db.add(user_msg)
    db.commit()

    # 3. Call Orchestrator
    try:
        res = orchestrator.answer_question(
            db=db,
            user_id=current_user.id,
            conversation_id=conversation.id,
            question=request.question,
            stream=False
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in RAG generation: {e}"
        )

    # 4. Save assistant response to DB
    assistant_msg = Message(
        conversation_id=conversation.id,
        sender="assistant",
        text=res["answer"],
        sources=json.dumps(res["sources"]),
        confidence=res["confidence"]
    )
    db.add(assistant_msg)
    db.commit()

    return ChatResponse(
        answer=res["answer"],
        sources=res["sources"],
        confidence=res["confidence"],
        conversation_id=conversation.id
    )


@router.post("/stream")
def chat_stream(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Resolve or create conversation
    if request.conversation_id:
        conversation = db.query(Conversation).filter(
            Conversation.id == request.conversation_id,
            Conversation.user_id == current_user.id
        ).first()
        if not conversation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    else:
        title = request.question[:40] + ("..." if len(request.question) > 40 else "")
        conversation = Conversation(user_id=current_user.id, title=title)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    # 2. Save user message
    user_msg = Message(
        conversation_id=conversation.id,
        sender="user",
        text=request.question
    )
    db.add(user_msg)
    db.commit()

    # 3. Get Orchestrator outputs (stream + metadata)
    res = orchestrator.answer_question(
        db=db,
        user_id=current_user.id,
        conversation_id=conversation.id,
        question=request.question,
        stream=True
    )

    sources = res["sources"]
    confidence = res["confidence"]
    stream_generator = res["stream"]

    def event_generator():
        # First send metadata (sources, conversation_id, confidence)
        metadata = {
            "conversation_id": conversation.id,
            "sources": sources,
            "confidence": confidence
        }
        yield f"data: {json.dumps(metadata)}\n\n"

        # Stream actual textual chunks
        full_text_list = []
        for text_chunk in stream_generator:
            full_text_list.append(text_chunk)
            yield f"data: {json.dumps({'text': text_chunk})}\n\n"

        # Save assistant message at the end
        db_read = SessionLocal()  # Use fresh thread-local session for background write
        try:
            assistant_msg = Message(
                conversation_id=conversation.id,
                sender="assistant",
                text="".join(full_text_list),
                sources=json.dumps(sources),
                confidence=confidence
            )
            db_read.add(assistant_msg)
            db_read.commit()
        except Exception as e:
            db_read.rollback()
        finally:
            db_read.close()

    # Create thread-local Session factory to support SSE writing
    from backend.database.session import SessionLocal

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.get("/history", response_model=List[ConversationResponse])
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    history = (
        db.query(Conversation)
        .filter(Conversation.user_id == current_user.id)
        .order_by(Conversation.created_at.desc())
        .all()
    )
    return history


@router.get("/history/{conversation_id}/messages", response_model=List[MessageResponse])
def get_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    conv = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .all()
    )
    return messages


@router.delete("/history/{conversation_id}")
def delete_history(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    conv = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    db.delete(conv)
    db.commit()
    return {"message": "Conversation history deleted successfully"}


@router.post("/feedback")
def submit_feedback(
    feedback_in: FeedbackRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify message belongs to current user's conversations
    message = db.query(Message).join(Conversation).filter(
        Message.id == feedback_in.message_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    # Save feedback
    db_feedback = Feedback(
        message_id=feedback_in.message_id,
        rating=feedback_in.rating,
        feedback=feedback_in.feedback
    )
    db.add(db_feedback)
    db.commit()
    return {"message": "Feedback submitted successfully"}
