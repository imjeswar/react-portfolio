import os
import logging
from sqlalchemy.orm import Session
from backend.database.models import Document, Chunk
from backend.storage.factory import get_storage_provider
from backend.rag.loaders.parsers import parse_document
from backend.rag.chunking.splitter import chunk_document
from backend.rag.embedding.factory import get_embedding_provider
from backend.rag.vectorstore.factory import get_vector_store_provider

logger = logging.getLogger(__name__)

def process_and_index_document(db: Session, document_id: int, user_id: int):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        logger.error(f"Document {document_id} not found in database.")
        return

    try:
        # Update status to processing
        doc.status = "processing"
        db.commit()
        logger.info(f"Started indexing document {doc.filename} (ID: {doc.id})")

        # 1. Parse pages
        pages = parse_document(doc.storage_path, doc.type)
        if not pages:
            raise ValueError("No text content extracted from document.")

        # 2. Split page texts into sliding window chunks
        chunks_data = chunk_document(pages, chunk_size_tokens=800, overlap_tokens=150)

        # 3. Generate embeddings for each chunk
        embedding_provider = get_embedding_provider()
        chunk_texts = [c["text"] for c in chunks_data]
        embeddings = embedding_provider.embed_documents(chunk_texts)

        # 4. Save to relational DB (Sqlite) and Vector Store (Chroma)
        vector_store = get_vector_store_provider()
        vector_chunks = []

        for idx, (chunk_data, embedding) in enumerate(zip(chunks_data, embeddings)):
            db_chunk = Chunk(
                document_id=doc.id,
                page=chunk_data["page_number"],
                text=chunk_data["text"],
                embedding_id=f"{doc.id}_{chunk_data['chunk_index']}"
            )
            db.add(db_chunk)
            db.flush()  # Populate db_chunk.id

            vector_chunks.append({
                "id": str(db_chunk.id),
                "document_id": int(doc.id),
                "page_number": int(chunk_data["page_number"]),
                "chunk_index": int(chunk_data["chunk_index"]),
                "text": chunk_data["text"],
                "embedding": embedding,
                "user_id": int(user_id),
                "filename": doc.filename
            })

        # Insert batch into Vector Store
        vector_store.add_chunks(vector_chunks)

        # Update status to completed
        doc.status = "completed"
        db.commit()
        logger.info(f"Successfully indexed document {doc.filename}")

    except Exception as e:
        logger.error(f"Failed to process and index document {doc.filename}: {e}", exc_info=True)
        doc.status = "failed"
        db.commit()


def delete_document_from_system(db: Session, document_id: int, user_id: int) -> bool:
    doc = db.query(Document).filter(Document.id == document_id, Document.user_id == user_id).first()
    if not doc:
        return False

    try:
        # 1. Delete physical file from storage provider
        storage = get_storage_provider()
        storage.delete_file(doc.storage_path)

        # 2. Delete chunks from Vector Store
        vector_store = get_vector_store_provider()
        vector_store.delete_document_chunks(doc.id)

        # 3. Relational delete cascade takes care of Chunk records
        db.delete(doc)
        db.commit()
        logger.info(f"Successfully deleted document {document_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting document {document_id}: {e}", exc_info=True)
        return False
