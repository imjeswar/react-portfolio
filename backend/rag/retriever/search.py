import logging
from typing import List, Dict, Any
from rank_bm25 import BM25Okapi
from backend.core.interfaces import VectorStoreProvider, EmbeddingProvider

logger = logging.getLogger(__name__)

def tokenize(text: str) -> List[str]:
    # Simple whitespace tokenization
    return text.lower().split()

def reciprocal_rank_fusion(
    vector_results: List[Dict[str, Any]], 
    bm25_results: List[Dict[str, Any]], 
    k: int = 60
) -> List[Dict[str, Any]]:
    """Merges two ranked lists of chunks using Reciprocal Rank Fusion."""
    rrf_scores = {}
    
    # Helper to calculate rank-based scores
    def add_ranks(results_list):
        for rank, chunk in enumerate(results_list):
            chunk_id = str(chunk.get("id") or chunk.get("metadata", {}).get("chunk_id"))
            if not chunk_id:
                continue
            if chunk_id not in rrf_scores:
                rrf_scores[chunk_id] = {
                    "chunk": chunk,
                    "score": 0.0
                }
            # RRF score formula
            rrf_scores[chunk_id]["score"] += 1.0 / (k + rank + 1)

    add_ranks(vector_results)
    add_ranks(bm25_results)

    # Sort chunks by fusion score descending
    sorted_results = sorted(rrf_scores.values(), key=lambda x: x["score"], reverse=True)
    
    # Inject final score and return chunks
    merged_chunks = []
    for item in sorted_results:
        chunk = item["chunk"]
        chunk["rrf_score"] = item["score"]
        merged_chunks.append(chunk)
        
    return merged_chunks

class HybridRetriever:
    def __init__(self, vector_store: VectorStoreProvider, embedding_provider: EmbeddingProvider):
        self.vector_store = vector_store
        self.embedding_provider = embedding_provider

    def retrieve(
        self, 
        query: str, 
        db_chunks: List[Any],  # SQLAlchemy Chunk models to feed BM25
        top_k: int = 5, 
        filter_dict: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """Performs hybrid Vector + BM25 search and merges results."""
        if not db_chunks:
            return []

        # 1. Vector Search
        try:
            query_vector = self.embedding_provider.embed_query(query)
            vector_results = self.vector_store.similarity_search(
                query_vector=query_vector,
                top_k=top_k * 2,  # Fetch slightly more to allow RRF overlap
                filter_dict=filter_dict
            )
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            vector_results = []

        # 2. BM25 Keyword Search
        bm25_results = []
        try:
            # Tokenize documents
            corpus = [tokenize(chunk.text) for chunk in db_chunks]
            bm25 = BM25Okapi(corpus)
            
            # Score documents
            query_tokens = tokenize(query)
            doc_scores = bm25.get_scores(query_tokens)
            
            # Map index and scores back
            scored_chunks = []
            for idx, score in enumerate(doc_scores):
                if score > 0.0:  # Only include matching chunks
                    db_chunk = db_chunks[idx]
                    scored_chunks.append({
                        "id": str(db_chunk.id),
                        "text": db_chunk.text,
                        "metadata": {
                            "document_id": db_chunk.document_id,
                            "page_number": db_chunk.page,
                            "chunk_index": idx,
                            "filename": db_chunk.document.filename if db_chunk.document else "document"
                        },
                        "score": float(score)
                    })
            
            # Sort and take top_k * 2
            scored_chunks = sorted(scored_chunks, key=lambda x: x["score"], reverse=True)
            bm25_results = scored_chunks[:top_k * 2]
        except Exception as e:
            logger.error(f"BM25 keyword search failed: {e}")

        # 3. Reciprocal Rank Fusion (RRF)
        merged_results = reciprocal_rank_fusion(vector_results, bm25_results)
        
        # Return top_k
        return merged_results[:top_k]
