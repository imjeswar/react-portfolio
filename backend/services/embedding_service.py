import numpy as np
from typing import List
from openai import OpenAI
from backend.core.interfaces import EmbeddingProvider
from backend.core.config import settings
from chromadb.utils import embedding_functions
import logging

logger = logging.getLogger(__name__)

class LocalEmbeddingProvider(EmbeddingProvider):
    def __init__(self):
        self.dimension = 384
        try:
            self.ef = embedding_functions.DefaultEmbeddingFunction()
        except Exception as e:
            logger.error(f"Failed to load Chroma default embedding function: {e}")
            self.ef = None

    def embed_query(self, text: str) -> List[float]:
        if self.ef is not None:
            try:
                return self.ef([text])[0]
            except Exception as e:
                logger.warning(f"Local embed_query failed: {e}. Falling back to mock.")
        # Fallback to deterministic mock
        np.random.seed(len(text))
        return np.random.uniform(-0.1, 0.1, self.dimension).tolist()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if self.ef is not None:
            try:
                return self.ef(texts)
            except Exception as e:
                logger.warning(f"Local embed_documents failed: {e}. Falling back to mock.")
        results = []
        for text in texts:
            np.random.seed(len(text))
            results.append(np.random.uniform(-0.1, 0.1, self.dimension).tolist())
        return results

class OpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = "text-embedding-3-large"
        self.dimension = 1536

    def embed_query(self, text: str) -> List[float]:
        try:
            response = self.client.embeddings.create(input=[text], model=self.model)
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"OpenAI embed_query failed: {e}")
            raise e

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        try:
            embeddings = []
            batch_size = 500
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                response = self.client.embeddings.create(input=batch, model=self.model)
                embeddings.extend([data.embedding for data in response.data])
            return embeddings
        except Exception as e:
            logger.error(f"OpenAI embed_documents failed: {e}")
            raise e

import requests

class GeminiEmbeddingProvider(EmbeddingProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.model = "models/gemini-embedding-2"
        self.dimension = 3072

    def embed_query(self, text: str) -> List[float]:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/{self.model}:embedContent?key={self.api_key}"
            payload = {
                "model": self.model,
                "content": {
                    "parts": [{"text": text}]
                }
            }
            res = requests.post(url, json=payload, timeout=15)
            res.raise_for_status()
            data = res.json()
            return data["embedding"]["values"]
        except Exception as e:
            logger.error(f"Gemini embed_query failed: {e}")
            raise e

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        try:
            embeddings = []
            batch_size = 100
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                url = f"https://generativelanguage.googleapis.com/v1beta/{self.model}:batchEmbedContents?key={self.api_key}"
                payload = {
                    "requests": [
                        {
                            "model": self.model,
                            "content": {
                                "parts": [{"text": t}]
                            }
                        } for t in batch
                    ]
                }
                res = requests.post(url, json=payload, timeout=30)
                res.raise_for_status()
                data = res.json()
                embeddings.extend([e["values"] for e in data["embeddings"]])
            return embeddings
        except Exception as e:
            logger.error(f"Gemini embed_documents failed: {e}")
            raise e

class MockEmbeddingProvider(EmbeddingProvider):
    def __init__(self):
        self.dimension = 1536

    def embed_query(self, text: str) -> List[float]:
        np.random.seed(len(text))
        return np.random.uniform(-0.1, 0.1, self.dimension).tolist()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_query(text) for text in texts]

def get_embedding_provider() -> EmbeddingProvider:
    provider = settings.EMBEDDING_PROVIDER.lower()
    if provider == "openai" and settings.OPENAI_API_KEY:
        return OpenAIEmbeddingProvider(settings.OPENAI_API_KEY)
    elif provider == "gemini" and settings.GEMINI_API_KEY:
        return GeminiEmbeddingProvider(settings.GEMINI_API_KEY)
    elif provider == "local":
        return LocalEmbeddingProvider()
    
    # Fallback cascade
    if settings.OPENAI_API_KEY:
        return OpenAIEmbeddingProvider(settings.OPENAI_API_KEY)
    if settings.GEMINI_API_KEY:
        return GeminiEmbeddingProvider(settings.GEMINI_API_KEY)
        
    logger.warning("No API keys found for embeddings. Falling back to local embedding provider.")
    return LocalEmbeddingProvider()
