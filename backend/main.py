import uvicorn
import asyncio
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

logger = logging.getLogger("uvicorn")

from backend.core.config import settings
from backend.database.session import engine, Base
from backend.routes import auth, documents, chat, search, voice, admin, portfolio, health

# Initialize SQL Database tables
Base.metadata.create_all(bind=engine)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _print_startup_banner(
    provider_label: str,
    active_model: str,
    llm_status: str,
    fallback_model: str,
    embedding_provider: str,
    vector_db: str,
    collection_name: str,
    chunks_count: int,
    startup_seconds: float,
):
    W = 60
    def row(k, v):
        return f"  {k:<22}: {v}"
    lines = [
        "=" * W,
        "   AI PORTFOLIO ASSISTANT",
        "=" * W,
        row("LLM Provider", provider_label),
        row("LLM Model", active_model),
        row("LLM Status", llm_status),
        row("Fallback Model", fallback_model),
        row("Embedding", embedding_provider),
        row("Vector Store", vector_db),
        row("Collection", collection_name),
        row("Chunks", str(chunks_count)),
        row("Startup Time", f"{startup_seconds:.1f} s"),
        "=" * W,
    ]
    for line in lines:
        logger.info(line)


async def _recovery_loop(app: FastAPI, interval_seconds: int = 1800):
    """
    Background task: every `interval_seconds` (default 30 min) probe the
    primary OpenRouter model and switch back if it has recovered.
    """
    while True:
        await asyncio.sleep(interval_seconds)
        provider = getattr(app.state, "llm_provider", None)
        if provider is None:
            continue
        from backend.services.llm_service import OpenRouterLLMProvider, STATUS_READY, STATUS_RATE_LIMITED
        if not isinstance(provider, OpenRouterLLMProvider):
            continue
        if provider.active_model == provider.primary_model:
            continue  # already on primary, nothing to recover
        logger.info("[Recovery] Scheduled check — attempting to reclaim primary model.")
        provider.try_recover_primary()


# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context.
    All startup logic runs before yield; shutdown logic (if any) after.
    The validated LLM provider is stored on app.state.llm_provider.
    """
    t_start = time.monotonic()

    # --- 1. Embedding provider ---
    embedding_label = settings.EMBEDDING_PROVIDER.upper()
    try:
        from backend.services.embedding_service import get_embedding_provider
        embedder = get_embedding_provider()
        embedding_label = type(embedder).__name__.replace("EmbeddingProvider", "") or settings.EMBEDDING_PROVIDER.upper()
        logger.info(f"[Startup] Embedding provider initialized: {embedding_label}")
    except Exception as e:
        logger.error(f"[Startup] Embedding provider failed to initialize: {e}")

    # --- 2. ChromaDB + Retriever ---
    chunks_count = 0
    collection_name = "portfolio_chunks"
    try:
        from backend.services.retriever import PortfolioRetriever
        retriever = PortfolioRetriever()
        if retriever.collection:
            chunks_count = retriever.collection.count()
            collection_name = retriever.collection.name
        logger.info(f"[Startup] ChromaDB initialized. Collection '{collection_name}' — {chunks_count} chunks loaded.")
        
        # Auto-index portfolio data in the background if empty to prevent event loop blocking
        if chunks_count == 0:
            logger.info("[Startup] Vector database is empty. Scheduling auto-indexing in background thread...")
            from backend.services.index_service import IndexService
            
            def run_background_index():
                try:
                    res = IndexService.index_portfolio_data()
                    logger.info(f"[Startup] Background auto-indexing finished: {res}")
                except Exception as ex:
                    logger.error(f"[Startup] Background auto-indexing failed: {ex}")
            
            asyncio.create_task(asyncio.to_thread(run_background_index))
    except Exception as e:
        logger.error(f"[Startup] ChromaDB initialization check failed: {e}")

    # --- 3. LLM Provider + Validation ---
    from backend.services.llm_service import (
        OpenRouterLLMProvider, RuleBasedLLMProvider,
        STATUS_READY, STATUS_RATE_LIMITED, STATUS_DEGRADED,
        get_llm_provider,
    )

    llm_provider = get_llm_provider()
    active_model = settings.OPENROUTER_MODEL
    fallback_model = settings.OPENROUTER_FALLBACK_MODEL
    provider_label = settings.LLM_PROVIDER.upper()
    llm_status_label = "READY"

    if isinstance(llm_provider, OpenRouterLLMProvider):
        # Run key validation in a separate thread so it doesn't hang the startup lifecycle
        validation = await asyncio.to_thread(llm_provider.validate)
        active_model = llm_provider.active_model
        status = llm_provider.status

        if status == STATUS_READY:
            llm_status_label = "✅ READY"
        elif status == STATUS_RATE_LIMITED:
            llm_status_label = "⚠️  READY (rate-limited at startup)"
        else:  # DEGRADED
            llm_status_label = "🔴 DEGRADED (RuleBased fallback active)"

    elif isinstance(llm_provider, RuleBasedLLMProvider):
        llm_status_label = "⚠️  RULE-BASED (mock/offline)"
        active_model = "RuleBasedLLMProvider"
        fallback_model = "—"

    # Store validated provider on app state (accessible to all routes)
    app.state.llm_provider = llm_provider

    # --- 4. Print startup banner ---
    t_elapsed = time.monotonic() - t_start
    _print_startup_banner(
        provider_label=provider_label,
        active_model=active_model,
        llm_status=llm_status_label,
        fallback_model=fallback_model,
        embedding_provider=embedding_label,
        vector_db=settings.VECTOR_DB.upper(),
        collection_name=collection_name,
        chunks_count=chunks_count,
        startup_seconds=t_elapsed,
    )

    # --- 5. Start background recovery loop ---
    recovery_task = asyncio.create_task(_recovery_loop(app, interval_seconds=1800))

    yield  # Application runs here

    # --- Shutdown ---
    recovery_task.cancel()
    try:
        await recovery_task
    except asyncio.CancelledError:
        pass
    logger.info("[Shutdown] AI Portfolio Assistant stopped.")


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Production-grade, modular RAG Knowledge Assistant backend.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS Policy configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adapt to specific domains in production
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route segments
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(documents.router, prefix=settings.API_V1_STR)
app.include_router(chat.router, prefix=settings.API_V1_STR)
app.include_router(search.router, prefix=settings.API_V1_STR)
app.include_router(voice.router, prefix=settings.API_V1_STR)
app.include_router(admin.router, prefix=settings.API_V1_STR)
app.include_router(portfolio.router, prefix=settings.API_V1_STR)
app.include_router(health.router, prefix=settings.API_V1_STR)

# Health router is registered above


@app.get("/")
def read_root():
    return {
        "status": "online",
        "app": settings.PROJECT_NAME,
        "api_docs": "/docs"
    }


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
