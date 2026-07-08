from abc import ABC, abstractmethod
from typing import List, Dict, Any, Generator

class StorageProvider(ABC):
    @abstractmethod
    def save_file(self, file_bytes: bytes, filename: str) -> str:
        """Saves a file and returns its storage path/URI."""
        pass

    @abstractmethod
    def delete_file(self, file_path: str) -> bool:
        """Deletes a file from storage."""
        pass

    @abstractmethod
    def read_file(self, file_path: str) -> bytes:
        """Reads and returns raw file bytes."""
        pass


class EmbeddingProvider(ABC):
    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        """Embeds a single query string."""
        pass

    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embeds a list of text documents."""
        pass


class VectorStoreProvider(ABC):
    @abstractmethod
    def add_chunks(self, chunks: List[Dict[str, Any]]) -> bool:
        """Adds a list of chunks with metadata and embeddings to the vector database.
        Each chunk is dict with keys: id, document_id, text, page, embedding, user_id, type.
        """
        pass

    @abstractmethod
    def similarity_search(
        self, query_vector: List[float], top_k: int = 5, filter_dict: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """Performs a vector similarity search and returns matching chunks."""
        pass

    @abstractmethod
    def delete_document_chunks(self, document_id: str) -> bool:
        """Deletes all chunks associated with a document_id."""
        pass


class LLMProvider(ABC):
    @abstractmethod
    def generate(
        self, prompt: str, system_prompt: str = None, history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Generates an answer from the LLM. Returns a dict containing 'answer'."""
        pass

    @abstractmethod
    def generate_stream(
        self, prompt: str, system_prompt: str = None, history: List[Dict[str, str]] = None
    ) -> Generator[str, None, None]:
        """Streams back token responses from the LLM."""
        pass
