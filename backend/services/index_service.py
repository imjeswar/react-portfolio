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
        if filename.startswith("projects/"):
            category = "project"
        else:
            category = os.path.basename(filename).replace(".md", "").replace("_me", "").strip().lower()
        
        # Default metadata structure
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
            all_links = re.findall(r"https?://[^\s\)\`]+", text)
            for link in all_links:
                clean_link = link.strip().rstrip(".")
                if "github.com" not in clean_link and "linkedin.com" not in clean_link and "wa.me" not in clean_link:
                    metadata["url"] = clean_link
                    break
                    
        return metadata

    @classmethod
    def index_portfolio_data(cls) -> Dict[str, Any]:
        """Recursively reads markdown files, parses YAML metadata/structured chunks, generates embeddings, and saves to ChromaDB."""
        embedder = get_embedding_provider()
        
        # Get path for portfolio_data
        backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(backend_dir, "portfolio_data")
        
        if not os.path.exists(data_dir):
            raise FileNotFoundError(f"Portfolio data directory '{data_dir}' not found.")
            
        # Recursively find all markdown files in portfolio_data
        files = []
        for root, _, filenames in os.walk(data_dir):
            for f in filenames:
                if f.endswith(".md"):
                    files.append(os.path.join(root, f))
        
        documents = []
        metadatas = []
        ids = []
        
        for file_path in files:
            # Relative path with forward slashes (e.g. projects/fitzone/README.md)
            filename = os.path.relpath(file_path, data_dir).replace("\\", "/")
            
            with open(file_path, "r", encoding="utf-8") as f:
                raw_content = f.read()
                
            content = raw_content
            yaml_metadata = {}
            
            # Simple YAML front matter parser
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    yaml_content = parts[1].strip()
                    content = parts[2].strip()
                    
                    for line in yaml_content.split("\n"):
                        if ":" in line:
                            k, v = line.split(":", 1)
                            k = k.strip().lower()
                            v = v.strip().strip('"').strip("'")
                            
                            # Clean up list syntax if any
                            if k == "tech" or k == "tags":
                                if v.startswith("[") and v.endswith("]"):
                                    yaml_metadata[k] = ", ".join([x.strip().strip('"').strip("'") for x in v[1:-1].split(",")])
                                else:
                                    yaml_metadata[k] = v
                            else:
                                yaml_metadata[k] = v
            
            # Extract main doc title from YAML or first heading
            doc_title = yaml_metadata.get("title")
            if not doc_title:
                doc_title_match = re.search(r"^#\s+(.*)$", content, re.MULTILINE)
                doc_title = doc_title_match.group(1).strip() if doc_title_match else os.path.basename(file_path).replace(".md", "").title()
            
            # Split by headings ## or ###
            sections = re.split(r"\n(?=##\s+|###\s+)", content)
            if len(sections) <= 1:
                sections = [c.strip() for c in content.split("\n\n") if c.strip()]
                
            current_section = "Introduction"
            for idx, section in enumerate(sections):
                section_text = section.strip()
                if not section_text:
                    continue
                    
                heading_match = re.match(r"^(##|###)\s+(?:\d+\.\s+)?(.*)$", section_text)
                if heading_match:
                    current_section = heading_match.group(2).strip()
                    
                meta = cls.parse_metadata(filename, section_text, doc_title, current_section)
                
                # Apply YAML overrides
                if "category" in yaml_metadata:
                    meta["category"] = yaml_metadata["category"]
                if "github" in yaml_metadata:
                    meta["github"] = yaml_metadata["github"]
                if "url" in yaml_metadata:
                    meta["url"] = yaml_metadata["url"]
                if "tags" in yaml_metadata:
                    meta["tags"] = yaml_metadata["tags"]
                if "tech" in yaml_metadata:
                    tech_val = yaml_metadata["tech"]
                    if meta["tags"]:
                        meta["tags"] += ", " + tech_val
                    else:
                        meta["tags"] = tech_val
                
                meta["chunk_index"] = idx
                
                documents.append(section_text)
                metadatas.append(meta)
                
                # Clean ID structure
                clean_name = filename.replace(".md", "").replace("/", "-").replace("_", "-")
                ids.append(f"portfolio_{clean_name}_{idx}")
                
        if not documents:
            return {"status": "error", "message": "No portfolio documents found to index."}
            
        embeddings = embedder.embed_documents(documents)
        
        os.makedirs(settings.VECTOR_DB_DIR, exist_ok=True)
        chroma_client = chromadb.PersistentClient(path=settings.VECTOR_DB_DIR)
        
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
