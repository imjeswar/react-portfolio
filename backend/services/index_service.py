import os
import re
import chromadb
from typing import Dict, Any
from backend.core.config import settings
from backend.services.embedding_service import get_embedding_provider

class IndexService:
    @staticmethod
    def parse_metadata(filename: str, text: str, doc_title: str, section_name: str) -> Dict[str, Any]:
        """Extracts structured metadata from a chunk text based on the category."""
        category = filename.replace(".md", "").replace("_me", "").strip().lower()
        
        # Default metadata structure (ChromaDB supports string, int, float, bool)
        metadata = {
            "source": filename,
            "filename": filename,
            "category": category,
            "title": doc_title,
            "section": section_name,
            "url": "",
            "github": "",
            "tags": ""
        }
        
        # 1. Try to extract Tech Stack / Tags
        tech_match = re.search(r"Tech\s+Stack:\s*(.*)", text, re.IGNORECASE)
        if tech_match:
            tags_list = [t.strip().replace("*", "").replace("`", "") for t in tech_match.group(1).split(",") if t.strip()]
            metadata["tags"] = ", ".join(tags_list)
            
        # 2. Extract GitHub link if present
        github_match = re.search(r"https://github\.com/[^\s\)\`]+", text)
        if github_match:
            metadata["github"] = github_match.group(0).strip().rstrip(".")
            
        # 3. Extract Live demo / URL link if present
        url_match = re.search(r"(?:Live Demo Link|Demo|Link):\s*(https?://[^\s\)\`]+)", text, re.IGNORECASE)
        if url_match:
            metadata["url"] = url_match.group(1).strip().rstrip(".")
        else:
            # Fallback: search for any http/https link that is not github or linkedin or whatsapp
            all_links = re.findall(r"https?://[^\s\)\`]+", text)
            for link in all_links:
                clean_link = link.strip().rstrip(".")
                if "github.com" not in clean_link and "linkedin.com" not in clean_link and "wa.me" not in clean_link:
                    metadata["url"] = clean_link
                    break
                    
        return metadata

    @classmethod
    def index_portfolio_data(cls) -> Dict[str, Any]:
        """Reads markdown files, parses structured chunks/metadata, generates embeddings, and saves to ChromaDB."""
        embedder = get_embedding_provider()
        
        # Get path for portfolio_data
        backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(backend_dir, "portfolio_data")
        
        if not os.path.exists(data_dir):
            raise FileNotFoundError(f"Portfolio data directory '{data_dir}' not found.")
            
        files = [f for f in os.listdir(data_dir) if f.endswith(".md")]
        
        documents = []
        metadatas = []
        ids = []
        
        for filename in files:
            file_path = os.path.join(data_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Extract main doc title from the first `#` heading
            doc_title_match = re.search(r"^#\s+(.*)$", content, re.MULTILINE)
            doc_title = doc_title_match.group(1).strip() if doc_title_match else filename.replace(".md", "").title()
            
            # Split by markdown ## and ### headers using lookahead to retain the header text in chunks
            sections = re.split(r"\n(?=##\s+|###\s+)", content)
            
            # If no ## or ### headers are found, split by double newline
            if len(sections) <= 1:
                sections = [c.strip() for c in content.split("\n\n") if c.strip()]
                
            current_section = "Introduction"
            for idx, section in enumerate(sections):
                section_text = section.strip()
                if not section_text:
                    continue
                    
                # Check if this section starts with a heading to determine section_name
                heading_match = re.match(r"^(##|###)\s+(?:\d+\.\s+)?(.*)$", section_text)
                if heading_match:
                    current_section = heading_match.group(2).strip()
                    
                meta = cls.parse_metadata(filename, section_text, doc_title, current_section)
                meta["chunk_index"] = idx
                
                documents.append(section_text)
                metadatas.append(meta)
                # Clean filename for ID creation
                clean_name = filename.replace(".md", "").replace("_", "-")
                ids.append(f"portfolio_{clean_name}_{idx}")
                
        if not documents:
            return {"status": "error", "message": "No portfolio documents found to index."}
            
        # Generate embeddings using modular EmbeddingService
        embeddings = embedder.embed_documents(documents)
        
        # Save to ChromaDB portfolio_chunks collection
        os.makedirs(settings.VECTOR_DB_DIR, exist_ok=True)
        chroma_client = chromadb.PersistentClient(path=settings.VECTOR_DB_DIR)
        
        # Delete old collection to prevent dimension mismatches and clean database
        try:
            chroma_client.delete_collection(name="portfolio_chunks")
        except Exception:
            pass
            
        collection = chroma_client.get_or_create_collection(name="portfolio_chunks")
        
        collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents
        )
        
        return {
            "status": "success",
            "chunks_indexed": len(documents),
            "collection_name": "portfolio_chunks",
            "embedding_dimension": len(embeddings[0]) if embeddings else 0
        }
