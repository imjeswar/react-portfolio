import logging
from backend.core.config import settings
from backend.rag.embedding.openai_embeddings import OpenAIEmbeddingProvider, MockEmbeddingProvider

logger = logging.getLogger(__name__)

def get_embedding_provider():
    if settings.EMBEDDING_PROVIDER == "openai":
        if not settings.OPENAI_API_KEY:
            logger.warning("OPENAI_API_KEY not found in settings. Falling back to MockEmbeddingProvider.")
            return MockEmbeddingProvider()
        try:
            return OpenAIEmbeddingProvider()
        except Exception as e:
            logger.error(f"Failed to initialize OpenAIEmbeddingProvider: {e}. Falling back to MockEmbeddingProvider.")
            return MockEmbeddingProvider()
    return MockEmbeddingProvider()
