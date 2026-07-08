import logging
from backend.core.config import settings
from backend.rag.chat.openai_llm import OpenAILLMProvider, MockLLMProvider

logger = logging.getLogger(__name__)

def get_llm_provider():
    if settings.LLM_PROVIDER == "openai":
        if not settings.OPENAI_API_KEY:
            logger.warning("OPENAI_API_KEY not found in settings. Falling back to MockLLMProvider.")
            return MockLLMProvider()
        try:
            return OpenAILLMProvider()
        except Exception as e:
            logger.error(f"Failed to initialize OpenAILLMProvider: {e}. Falling back to MockLLMProvider.")
            return MockLLMProvider()
    return MockLLMProvider()
