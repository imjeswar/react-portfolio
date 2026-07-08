import logging
from backend.core.config import settings
from backend.rag.vectorstore.chroma_store import ChromaVectorStoreProvider, MockVectorStoreProvider

logger = logging.getLogger(__name__)

def get_vector_store_provider():
    if settings.VECTOR_STORE_PROVIDER == "chromadb":
        try:
            return ChromaVectorStoreProvider()
        except Exception as e:
            logger.error(f"Failed to initialize ChromaVectorStoreProvider: {e}. Falling back to MockVectorStoreProvider.")
            return MockVectorStoreProvider()
    return MockVectorStoreProvider()
