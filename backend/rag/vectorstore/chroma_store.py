import os
from typing import List, Dict, Any
import chromadb
from backend.core.interfaces import VectorStoreProvider
from backend.core.config import settings

class ChromaVectorStoreProvider(VectorStoreProvider):
    def __init__(self):
        os.makedirs(settings.VECTOR_DB_DIR, exist_ok=True)
        self.client = chromadb.PersistentClient(path=settings.VECTOR_DB_DIR)
        # Collection name must be 3-63 chars, start/end with alphanumeric, contain only alphanumeric, _ or -
        self.collection = self.client.get_or_create_collection(name="document_chunks")

    def add_chunks(self, chunks: List[Dict[str, Any]]) -> bool:
        if not chunks:
            return True
        
        ids = []
        embeddings = []
        metadatas = []
        documents = []

        for chunk in chunks:
            ids.append(str(chunk["id"]))
            embeddings.append(chunk["embedding"])
            # Chroma metadatas only support simple types: str, int, float, bool
            metadatas.append({
                "document_id": int(chunk.get("document_id", 0)) if chunk.get("document_id") is not None else 0,
                "page_number": int(chunk.get("page_number", 1)),
                "chunk_index": int(chunk.get("chunk_index", 0)),
                "user_id": int(chunk.get("user_id", 0)) if chunk.get("user_id") is not None else 0
            })
            documents.append(chunk.get("text", ""))

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents
        )
        return True

    def similarity_search(
        self, query_vector: List[float], top_k: int = 5, filter_dict: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        # Format the filter for ChromaDB: support both string and integer IDs to prevent type mismatches
        where_clause = None
        if filter_dict:
            conditions = []
            for k, v in filter_dict.items():
                if v is not None:
                    if k in ["user_id", "document_id"]:
                        try:
                            val_int = int(v)
                            val_str = str(v)
                            conditions.append({
                                "$or": [
                                    {k: val_int},
                                    {k: val_str}
                                ]
                            })
                        except (ValueError, TypeError):
                            conditions.append({k: v})
                    else:
                        conditions.append({k: v})
            
            if len(conditions) == 1:
                where_clause = conditions[0]
            elif len(conditions) > 1:
                where_clause = {"$and": conditions}

        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=top_k,
            where=where_clause
        )

        matched_chunks = []
        if results and "documents" in results and results["documents"]:
            # Chroma returns lists of lists since it supports batch queries
            docs = results["documents"][0]
            metas = results["metadatas"][0]
            ids = results["ids"][0]
            distances = results["distances"][0] if "distances" in results else [0.0] * len(docs)

            for i in range(len(docs)):
                matched_chunks.append({
                    "id": ids[i],
                    "text": docs[i],
                    "metadata": metas[i],
                    # Invert L2 distance or compute a mock confidence score
                    "score": max(0.0, 1.0 - distances[i])
                })
        return matched_chunks

    def delete_document_chunks(self, document_id: str) -> bool:
        try:
            doc_id_val = int(document_id)
            where_clause = {
                "$or": [
                    {"document_id": doc_id_val},
                    {"document_id": str(doc_id_val)}
                ]
            }
        except (ValueError, TypeError):
            where_clause = {"document_id": document_id}

        self.collection.delete(
            where=where_clause
        )
        return True


class MockVectorStoreProvider(VectorStoreProvider):
    def __init__(self):
        self.chunks_db = []

    def add_chunks(self, chunks: List[Dict[str, Any]]) -> bool:
        self.chunks_db.extend(chunks)
        return True

    def similarity_search(
        self, query_vector: List[float], top_k: int = 5, filter_dict: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        # Return first top_k matching document_id or user_id
        results = []
        count = 0
        for chunk in self.chunks_db:
            if count >= top_k:
                break
            
            # Simple filtering
            match = True
            if filter_dict:
                for k, v in filter_dict.items():
                    if k in chunk and str(chunk[k]) != str(v):
                        match = False
                    elif f"metadata" in chunk and k in chunk["metadata"] and str(chunk["metadata"][k]) != str(v):
                        match = False
            
            if match:
                results.append({
                    "id": chunk.get("id"),
                    "text": chunk.get("text"),
                    "metadata": {
                        "document_id": chunk.get("document_id"),
                        "page_number": chunk.get("page_number", 1),
                        "chunk_index": chunk.get("chunk_index", 0),
                        "user_id": chunk.get("user_id", "")
                    },
                    "score": 0.95 - (count * 0.05)
                })
                count += 1
        return results

    def delete_document_chunks(self, document_id: str) -> bool:
        self.chunks_db = [c for c in self.chunks_db if str(c.get("document_id")) != str(document_id)]
        return True
