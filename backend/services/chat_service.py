import logging
from typing import List, Dict, Any, Optional
from fastapi import Request

from backend.core.interfaces import LLMProvider
from backend.services.conversation import ConversationService
from backend.services.retriever import PortfolioRetriever
from backend.prompts.portfolio_prompt import PORTFOLIO_SYSTEM_PROMPT, RETRIEVAL_PROMPT_TEMPLATE

logger = logging.getLogger(__name__)


def _get_llm_from_app_state(request: Optional[Request]) -> LLMProvider:
    """
    Retrieve the validated LLM provider from FastAPI app state.
    Falls back to re-instantiating via the factory if app state is unavailable
    (e.g. during unit tests or direct invocation outside a request context).
    """
    if request is not None:
        provider = getattr(request.app.state, "llm_provider", None)
        if provider is not None:
            return provider
    # Safety net: factory-create if state not populated yet
    logger.warning("app.state.llm_provider not found — falling back to factory instantiation.")
    from backend.services.llm_service import get_llm_provider
    return get_llm_provider()


class PortfolioChatService:
    def __init__(self, request: Optional[Request] = None):
        self.retriever = PortfolioRetriever()
        self.llm = _get_llm_from_app_state(request)

    def chat(self, question: str, history: List[Dict[str, str]], stream: bool = False) -> Dict[str, Any]:
        """Orchestrates query -> history trim -> hybrid retrieve -> prompt build -> LLM call/stream."""
        # 1. Trim and clean conversation history (avoid prompt bloat and clean error states)
        cleaned_history = ConversationService.trim_history(history, limit=8)

        # 2. Retrieve relevant context chunks using hybrid vector + BM25 keyword retrieval
        retrieved_chunks = self.retriever.retrieve(query=question, top_k=4)

        # 3. Format context string and compile source documents for citation list
        context_str = ""
        sources = []
        for chunk in retrieved_chunks:
            source = chunk.get("source", "portfolio_data")
            text = chunk.get("text", "")
            context_str += f"--- Source: {source} ---\n{text}\n\n"

            sources.append({
                "id": chunk.get("id"),
                "filename": chunk.get("filename") or source,
                "category": chunk.get("category", ""),
                "title": chunk.get("title", ""),
                "url": chunk.get("url", ""),
                "github": chunk.get("github", ""),
                "section": chunk.get("section", ""),
                "text": text[:200] + "..."  # Truncate preview text
            })

        # Remove duplicate sources to keep citations list clean
        seen_sources = set()
        unique_sources = []
        for s in sources:
            key = (s["filename"], s["title"])
            if key not in seen_sources:
                seen_sources.add(key)
                unique_sources.append(s)

        # 4. Construct prompts
        system_prompt = PORTFOLIO_SYSTEM_PROMPT.format(context=context_str if context_str else "No context retrieved.")
        user_prompt = RETRIEVAL_PROMPT_TEMPLATE.format(question=question)

        # Determine scroll actions based on keywords in the question
        actions = []
        q_lower = question.lower()
        if any(kw in q_lower for kw in ["project", "fitzone", "inkify", "health assistant", "resume analyzer"]):
            actions.append("scroll:projects")
        if any(kw in q_lower for kw in ["skill", "tech stack", "languages", "programming"]):
            actions.append("scroll:skills")
        if any(kw in q_lower for kw in ["certification", "certificate", "coursera", "nptel"]):
            actions.append("scroll:certifications")
        if any(kw in q_lower for kw in ["contact", "email", "phone", "whatsapp", "reach out"]):
            actions.append("scroll:contact")
        if any(kw in q_lower for kw in ["education", "degree", "b.tech", "study", "university"]):
            actions.append("scroll:education")
        if any(kw in q_lower for kw in ["experience", "internship", "work", "icat"]):
            actions.append("scroll:internship")
        if any(kw in q_lower for kw in ["about", "summary", "located", "where do you live"]):
            actions.append("scroll:about")
        if any(kw in q_lower for kw in ["journey", "timeline"]):
            actions.append("scroll:journey")

        # 5. Call LLM provider (handles streaming and fallbacks automatically)
        if stream:
            llm_stream = self.llm.generate_stream(user_prompt, system_prompt, cleaned_history)
            return {
                "stream": llm_stream,
                "sources": unique_sources,
                "actions": actions
            }
        else:
            llm_response = self.llm.generate(user_prompt, system_prompt, cleaned_history)
            import re
            answer = llm_response.get("answer", "")
            pattern = r"(?:\s*---\s*)?(?:\r?\n)*[-*\s]*\*\*?(?:Sources?|Citations?|References?)\*\*?:\s*.*$"
            clean_answer = re.sub(pattern, "", answer, flags=re.IGNORECASE | re.DOTALL).strip()
            return {
                "answer": clean_answer,
                "sources": unique_sources,
                "actions": actions
            }
