import json
import logging
from typing import List, Dict, Any, Generator
from sqlalchemy.orm import Session

from backend.database.models import Message, Chunk
from backend.rag.chat.factory import get_llm_provider
from backend.rag.embedding.factory import get_embedding_provider
from backend.rag.vectorstore.factory import get_vector_store_provider
from backend.rag.retriever.search import HybridRetriever
from backend.rag.prompts.templates import SYSTEM_PROMPT, RETRIEVAL_PROMPT_TEMPLATE, CITATION_PROMPT, FOLLOW_UP_PROMPT

logger = logging.getLogger(__name__)

class RAGChatOrchestrator:
    def __init__(self):
        self.llm = get_llm_provider()
        self.vector_store = get_vector_store_provider()
        self.embedding = get_embedding_provider()
        self.retriever = HybridRetriever(self.vector_store, self.embedding)

    def _get_history(self, db: Session, conversation_id: int, limit: int = 6) -> List[Dict[str, str]]:
        messages = (
            db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .all()
        )
        # return list of dicts for LLM history context
        return [{"sender": msg.sender, "text": msg.text} for msg in messages[-limit:]]

    def _get_user_chunks(self, db: Session, user_id: int) -> List[Chunk]:
        # Fetch all chunks belonging to user's uploaded documents
        from backend.database.models import Document
        user_docs = db.query(Document).filter(Document.user_id == user_id, Document.status == "completed").all()
        doc_ids = [doc.id for doc in user_docs]
        if not doc_ids:
            return []
        return db.query(Chunk).filter(Chunk.document_id.in_(doc_ids)).all()

    def answer_question(
        self, 
        db: Session, 
        user_id: int, 
        conversation_id: int, 
        question: str,
        stream: bool = False
    ) -> Dict[str, Any]:
        # 1. Fetch memory
        history = self._get_history(db, conversation_id)

        # 2. Hybrid retrieve chunks
        db_chunks = self._get_user_chunks(db, user_id)
        
        # If no chunks, answer from LLM with a note that no docs are uploaded yet
        if not db_chunks:
            system_msg = SYSTEM_PROMPT + "\nNote: The user has not uploaded any documents yet. Advise them to upload documents."
            if stream:
                return {
                    "stream": self.llm.generate_stream(question, system_msg, history),
                    "sources": [],
                    "confidence": 0.5
                }
            else:
                res = self.llm.generate(question, system_msg, history)
                return {
                    "answer": res["answer"],
                    "sources": [],
                    "confidence": 0.5
                }

        # Retrieve top 5 matching chunks
        retrieved = self.retriever.retrieve(
            query=question,
            db_chunks=db_chunks,
            top_k=5,
            filter_dict={"user_id": user_id}
        )

        # 3. Format retrieved context
        context_str = ""
        sources = []
        for idx, chunk in enumerate(retrieved):
            meta = chunk.get("metadata", {})
            filename = meta.get("filename") or "Document"
            page = meta.get("page_number") or 1
            context_str += f"--- Chunk {idx+1} | Source: {filename} | Page: {page} ---\n{chunk.get('text')}\n\n"
            
            # Record sources for frontend citation lookup
            sources.append({
                "chunk_id": chunk.get("id"),
                "filename": filename,
                "page": page,
                "text": chunk.get("text")[:200] + "...",
                "score": chunk.get("score") or chunk.get("rrf_score") or 0.8
            })

        # Remove duplicate sources to keep it neat
        seen_sources = set()
        unique_sources = []
        for s in sources:
            key = (s["filename"], s["page"])
            if key not in seen_sources:
                seen_sources.add(key)
                unique_sources.append(s)

        # 4. Construct prompt
        system_prompt = SYSTEM_PROMPT + "\n" + CITATION_PROMPT
        if history:
            system_prompt += "\n" + FOLLOW_UP_PROMPT
            
        retrieval_prompt = RETRIEVAL_PROMPT_TEMPLATE.format(
            question=question,
            context=context_str if context_str else "No context retrieved."
        )

        # 5. Call LLM
        confidence = 0.85
        if retrieved:
            # Average score of top chunk
            confidence = float(retrieved[0].get("score", 0.85) or 0.85)

        if stream:
            return {
                "stream": self.llm.generate_stream(retrieval_prompt, system_prompt, history),
                "sources": unique_sources,
                "confidence": confidence
            }
        else:
            res = self.llm.generate(retrieval_prompt, system_prompt, history)
            return {
                "answer": res["answer"],
                "sources": unique_sources,
                "confidence": confidence
            }
