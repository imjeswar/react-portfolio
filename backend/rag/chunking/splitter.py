from typing import List, Dict, Any

def split_text_to_chunks(text: str, chunk_size_tokens: int = 800, overlap_tokens: int = 150) -> List[str]:
    # Approximating tokens: 1 token is roughly 4 characters or 0.75 words.
    # Therefore, 800 tokens is approximately 600 words, and 150 tokens is 112 words.
    words = text.split(" ")
    chunk_size_words = int(chunk_size_tokens * 0.75)
    overlap_words = int(overlap_tokens * 0.75)

    if chunk_size_words <= 0:
        chunk_size_words = 1
    if overlap_words >= chunk_size_words:
        overlap_words = chunk_size_words // 2

    if len(words) <= chunk_size_words:
        return [text]

    chunks = []
    i = 0
    while i < len(words):
        chunk_slice = words[i : i + chunk_size_words]
        chunks.append(" ".join(chunk_slice))
        # Move forward by (chunk_size - overlap)
        i += (chunk_size_words - overlap_words)
        if i >= len(words) or (i + chunk_size_words - overlap_words) >= len(words) and len(words) - i <= overlap_words:
            # Avoid a trailing chunk that's smaller than the overlap
            break

    # If there are left-over words, append them as a final chunk
    if i < len(words):
        chunks.append(" ".join(words[i:]))

    return chunks

def chunk_document(parsed_pages: List[Dict[str, Any]], chunk_size_tokens: int = 800, overlap_tokens: int = 150) -> List[Dict[str, Any]]:
    """Chunks list of parsed pages and returns chunks with metadata."""
    chunks = []
    chunk_index = 0
    
    for page_data in parsed_pages:
        page_num = page_data.get("page", 1)
        page_text = page_data.get("text", "")
        
        page_chunks = split_text_to_chunks(page_text, chunk_size_tokens, overlap_tokens)
        
        for idx, chunk_text in enumerate(page_chunks):
            chunks.append({
                "chunk_index": chunk_index,
                "page_number": page_num,
                "text": chunk_text
            })
            chunk_index += 1
            
    return chunks
