from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import json
import logging

from backend.services.chat_service import PortfolioChatService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/portfolio", tags=["Portfolio Chatbot"])


class PortfolioChatRequest(BaseModel):
    question: str
    history: Optional[List[Dict[str, str]]] = []


@router.post("/chat")
def portfolio_chat_stream(request: Request, body: PortfolioChatRequest):
    try:
        # Pass the Request so the chat service can read app.state.llm_provider
        chat_service = PortfolioChatService(request=request)
        res = chat_service.chat(body.question, body.history, stream=True)
    except Exception as e:
        logger.error(f"Failed to run portfolio chat service: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to run chat service: {e}")

    sources = res["sources"]
    stream_generator = res["stream"]
    actions = res.get("actions", [])

    def sse_generator():
        # First send metadata (sources, actions)
        metadata = {"sources": sources, "actions": actions}
        yield f"data: {json.dumps(metadata)}\n\n"

        # Stream actual textual chunks
        for text_chunk in stream_generator:
            yield f"data: {json.dumps({'text': text_chunk})}\n\n"

    return StreamingResponse(sse_generator(), media_type="text/event-stream")
