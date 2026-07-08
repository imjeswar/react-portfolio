from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class UserRegister(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class DocumentResponse(BaseModel):
    id: int
    filename: str
    type: str
    size: int
    status: str
    uploaded_at: datetime
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    question: str
    conversation_id: Optional[int] = None

class SourceCitation(BaseModel):
    chunk_id: Optional[str] = None
    filename: str
    page: int
    text: str
    score: float

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceCitation]
    confidence: float
    conversation_id: int

class FeedbackRequest(BaseModel):
    message_id: int
    rating: int = Field(..., ge=1, le=5)
    feedback: Optional[str] = None

class SearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

class SearchResponseChunk(BaseModel):
    id: str
    text: str
    metadata: Dict[str, Any]
    score: float

class SearchResponse(BaseModel):
    chunks: List[SearchResponseChunk]

class ConversationResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    sender: str
    text: str
    sources: Optional[str] = None
    confidence: Optional[float] = None
    created_at: datetime
    class Config:
        from_attributes = True

class AnalyticsResponse(BaseModel):
    document_count: int
    chunk_count: int
    conversation_count: int
    average_rating: float
