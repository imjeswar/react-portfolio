from typing import Dict, Type
import logging
from backend.core.interfaces import LLMProvider
from backend.core.config import settings

logger = logging.getLogger(__name__)

class LLMProviderFactory:
    _registry: Dict[str, Type[LLMProvider]] = {}

    @classmethod
    def register(cls, name: str, provider_class: Type[LLMProvider]):
        cls._registry[name.lower()] = provider_class
        logger.info(f"Registered LLM provider: {name}")

    @classmethod
    def get_provider(cls, provider_name: str) -> LLMProvider:
        # Import inside method to avoid circular imports
        from backend.services.llm_service import (
            OpenRouterLLMProvider,
            OpenAILLMProvider,
            GeminiLLMProvider,
            RuleBasedLLMProvider
        )
        
        # Initialize registry if empty
        if not cls._registry:
            cls.register("openrouter", OpenRouterLLMProvider)
            cls.register("openai", OpenAILLMProvider)
            cls.register("gemini", GeminiLLMProvider)
            cls.register("mock", RuleBasedLLMProvider)
            
        provider_key = provider_name.lower()
        if provider_key in cls._registry:
            provider_class = cls._registry[provider_key]
            
            # Instantiate with appropriate config
            if provider_key == "openrouter":
                return provider_class(
                    api_key=settings.OPENROUTER_API_KEY,
                    model=settings.OPENROUTER_MODEL,
                    fallback_model=settings.OPENROUTER_FALLBACK_MODEL
                )
            elif provider_key == "openai":
                return provider_class(api_key=settings.OPENAI_API_KEY)
            elif provider_key == "gemini":
                return provider_class(api_key=settings.GEMINI_API_KEY)
            else:
                return provider_class()
                
        # Fallback if not found
        logger.warning(f"LLM provider '{provider_name}' not found. Falling back to RuleBasedLLMProvider.")
        return RuleBasedLLMProvider()
