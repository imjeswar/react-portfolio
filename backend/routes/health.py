from fastapi import APIRouter, Request
import logging

from backend.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
def health_check(request: Request):
    """
    Returns the operational status of all backend subsystems:
    - LLM provider (provider name, active model, state)
    - Embedding provider (provider name, state)
    - Vector database (provider name, chunk count, state)
    """
    from backend.services.llm_service import (
        OpenRouterLLMProvider, RuleBasedLLMProvider,
        STATUS_READY, STATUS_RATE_LIMITED, STATUS_DEGRADED,
    )

    # --- LLM ---
    llm_provider = getattr(request.app.state, "llm_provider", None)

    if isinstance(llm_provider, OpenRouterLLMProvider):
        status_map = {
            STATUS_READY: "ready",
            STATUS_RATE_LIMITED: "ready",  # externally still "ready"; logs show detail
            STATUS_DEGRADED: "degraded",
        }
        llm_info = {
            "provider": "openrouter",
            "model": llm_provider.active_model,
            "primary_model": llm_provider.primary_model,
            "fallback_model": llm_provider.fallback_model,
            "state": status_map.get(llm_provider.status, llm_provider.status),
        }
    elif isinstance(llm_provider, RuleBasedLLMProvider):
        llm_info = {
            "provider": "rule_based",
            "model": "RuleBasedLLMProvider",
            "state": "degraded",
        }
    elif llm_provider is None:
        llm_info = {
            "provider": settings.LLM_PROVIDER,
            "model": settings.OPENROUTER_MODEL,
            "state": "unknown",
        }
    else:
        llm_info = {
            "provider": type(llm_provider).__name__,
            "model": getattr(llm_provider, "model", "unknown"),
            "state": "ready",
        }

    # --- Embeddings ---
    embedding_state = "ready"
    try:
        from backend.services.embedding_service import get_embedding_provider
        ep = get_embedding_provider()
        embedding_provider_name = settings.EMBEDDING_PROVIDER
    except Exception:
        embedding_state = "degraded"
        embedding_provider_name = settings.EMBEDDING_PROVIDER

    embeddings_info = {
        "provider": embedding_provider_name,
        "state": embedding_state,
    }

    # --- Vector DB ---
    chunks_count = 0
    vectordb_state = "ready"
    try:
        from backend.services.retriever import PortfolioRetriever
        retriever = PortfolioRetriever()
        if retriever.collection:
            chunks_count = retriever.collection.count()
        else:
            vectordb_state = "degraded"
    except Exception:
        vectordb_state = "degraded"

    vectordb_info = {
        "provider": settings.VECTOR_DB,
        "chunks": chunks_count,
        "state": vectordb_state,
    }

    # --- Overall status ---
    is_degraded = (
        llm_info["state"] == "degraded"
        or embeddings_info["state"] == "degraded"
        or vectordb_info["state"] == "degraded"
    )
    overall_status = "degraded" if is_degraded else "online"

    return {
        "status": overall_status,
        "llm": llm_info,
        "embeddings": embeddings_info,
        "vectordb": vectordb_info,
    }
