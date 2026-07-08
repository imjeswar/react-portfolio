import logging
import chromadb
from typing import List, Dict, Any
from rank_bm25 import BM25Okapi
from backend.core.config import settings
from backend.services.embedding_service import get_embedding_provider

logger = logging.getLogger(__name__)

def tokenize(text: str) -> List[str]:
    # Basic tokenization: lowercase and split by whitespace
    return text.lower().split()

def reciprocal_rank_fusion(
    vector_results: List[Dict[str, Any]], 
    bm25_results: List[Dict[str, Any]], 
    k: int = 60
) -> List[Dict[str, Any]]:
    """Merges two ranked lists using Reciprocal Rank Fusion (RRF)"""
    rrf_scores = {}
    
    def add_ranks(results_list):
        for rank, chunk in enumerate(results_list):
            chunk_id = str(chunk.get("id"))
            if not chunk_id:
                continue
            if chunk_id not in rrf_scores:
                rrf_scores[chunk_id] = {
                    "chunk": chunk,
                    "score": 0.0
                }
            # RRF formula
            rrf_scores[chunk_id]["score"] += 1.0 / (k + rank + 1)

    add_ranks(vector_results)
    add_ranks(bm25_results)

    # Sort chunks by rrf score descending
    sorted_results = sorted(rrf_scores.values(), key=lambda x: x["score"], reverse=True)
    
    merged_chunks = []
    for item in sorted_results:
        chunk = item["chunk"]
        chunk["rrf_score"] = item["score"]
        merged_chunks.append(chunk)
        
    return merged_chunks

class PortfolioRetriever:
    def __init__(self):
        self.embedding_provider = get_embedding_provider()
        self.chroma_client = None
        self.collection = None
        self._init_chroma()

    def _init_chroma(self):
        try:
            self.chroma_client = chromadb.PersistentClient(path=settings.VECTOR_DB_DIR)
            self.collection = self.chroma_client.get_or_create_collection(name="portfolio_chunks")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB in PortfolioRetriever: {e}")

    def retrieve(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        # Ensure Chroma is initialized
        if self.collection is None:
            self._init_chroma()
        if self.collection is None:
            return []

        # 1. Vector Search
        vector_results = []
        try:
            query_vector = self.embedding_provider.embed_query(query)
            results = self.collection.query(
                query_embeddings=[query_vector],
                n_results=top_k * 2
            )
            if results and "documents" in results and results["documents"] and len(results["documents"][0]) > 0:
                docs = results["documents"][0]
                metas = results["metadatas"][0]
                ids = results["ids"][0]
                distances = results["distances"][0] if "distances" in results else [0.0] * len(docs)
                for i in range(len(docs)):
                    meta = metas[i] or {}
                    vector_results.append({
                        "id": ids[i],
                        "text": docs[i],
                        "source": meta.get("source", "portfolio_data"),
                        "filename": meta.get("filename", ""),
                        "category": meta.get("category", ""),
                        "title": meta.get("title", ""),
                        "url": meta.get("url", ""),
                        "github": meta.get("github", ""),
                        "section": meta.get("section", ""),
                        "score": max(0.0, 1.0 - distances[i])
                    })
        except Exception as e:
            logger.error(f"Vector similarity search failed: {e}")

        # 2. BM25 Keyword Search
        bm25_results = []
        try:
            # Fetch all chunks in collection to build the dynamic BM25 index
            all_chunks = self.collection.get()
            if all_chunks and "documents" in all_chunks and all_chunks["documents"] and len(all_chunks["documents"]) > 0:
                docs = all_chunks["documents"]
                metas = all_chunks["metadatas"]
                ids = all_chunks["ids"]
                
                # Tokenize corpus
                corpus = [tokenize(doc) for doc in docs]
                bm25 = BM25Okapi(corpus)
                
                query_tokens = tokenize(query)
                doc_scores = bm25.get_scores(query_tokens)
                
                scored_chunks = []
                for idx, score in enumerate(doc_scores):
                    if score > 0.0:
                        meta = metas[idx] or {}
                        scored_chunks.append({
                            "id": ids[idx],
                            "text": docs[idx],
                            "source": meta.get("source", "portfolio_data"),
                            "filename": meta.get("filename", ""),
                            "category": meta.get("category", ""),
                            "title": meta.get("title", ""),
                            "url": meta.get("url", ""),
                            "github": meta.get("github", ""),
                            "section": meta.get("section", ""),
                            "score": float(score)
                        })
                # Sort and take top_k * 2
                scored_chunks = sorted(scored_chunks, key=lambda x: x["score"], reverse=True)
                bm25_results = scored_chunks[:top_k * 2]
        except Exception as e:
            logger.error(f"BM25 keyword search failed: {e}")

        # 3. Reciprocal Rank Fusion (RRF)
        merged = reciprocal_rank_fusion(vector_results, bm25_results)
        return merged[:top_k]
