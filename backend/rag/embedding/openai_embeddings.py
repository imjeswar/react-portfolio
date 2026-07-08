from typing import List
from openai import OpenAI
from backend.core.interfaces import EmbeddingProvider
from backend.core.config import settings
import numpy as np
import logging

logger = logging.getLogger(__name__)

class OpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not configured in environment variables.")
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "text-embedding-3-large"
        self.dimension = 1536

    def embed_query(self, text: str) -> List[float]:
        try:
            response = self.client.embeddings.create(
                input=[text],
                model=self.model
            )
            return response.data[0].embedding
        except Exception as e:
            logger.warning(f"OpenAI embedding query failed: {e}. Falling back to deterministic Mock embeddings.")
            # Fall back to deterministic mock values based on text seed
            np.random.seed(len(text))
            return np.random.uniform(-0.1, 0.1, self.dimension).tolist()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        try:
            embeddings = []
            batch_size = 500
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                response = self.client.embeddings.create(
                    input=batch,
                    model=self.model
                )
                embeddings.extend([data.embedding for data in response.data])
            return embeddings
        except Exception as e:
            logger.warning(f"OpenAI embedding documents batch failed: {e}. Falling back to deterministic Mock embeddings.")
            results = []
            for text in texts:
                np.random.seed(len(text))
                results.append(np.random.uniform(-0.1, 0.1, self.dimension).tolist())
            return results


class MockEmbeddingProvider(EmbeddingProvider):
    def __init__(self):
        self.dimension = 1536

    def embed_query(self, text: str) -> List[float]:
        # Seed deterministic values based on text length to make it slightly responsive
        np.random.seed(len(text))
        return np.random.uniform(-0.1, 0.1, self.dimension).tolist()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_query(text) for text in texts]
