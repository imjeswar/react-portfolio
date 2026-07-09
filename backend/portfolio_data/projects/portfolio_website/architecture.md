---
title: Portfolio Website Architecture & RAG Pipeline
category: project
tech: FastAPI, ChromaDB, OpenRouter, Gemini, React
---

# Portfolio Website Technical Architecture

## RAG & AI Pipeline
The AI Chatbot is built as a complete Retrieval-Augmented Generation (RAG) system:
1. **Document Ingestion**: Multi-format parsing of portfolio markdown documents with custom YAML front matter metadata.
2. **Embeddings generation**: Direct REST API integration with `models/gemini-embedding-2` for 3072-dimensional vector representations.
3. **Vector Database**: ChromaDB indices the document embeddings.
4. **Hybrid Retrieval**: Combines ChromaDB vector search with BM25 keyword matching (Rank_BM25) using Reciprocal Rank Fusion (RRF) for ultimate retrieval accuracy.
5. **Intent Routing**: Directs the query to either a strict RAG context prompt or a general LLM response based on semantic intent.
6. **Chat Completion**: Calls the Llama 3.1 8B Instruct model on OpenRouter with fallbacks to Qwen.

## Engineering Challenges & Solutions
1. **Server Cold Starts & Indexing**:
   - *Challenge*: Deployed on a Render free container which restarts frequently, wiping the database.
   - *Solution*: Enabled fast REST-based Gemini embeddings to re-index the portfolio in 1.5 seconds on startup with zero CPU/RAM bottleneck.
2. **Context Leak & Hallucinations**:
   - *Challenge*: General LLMs make up details if they do not know the candidate.
   - *Solution*: Implemented strict prompt constraints for portfolio questions to refuse questions when context is not found, while enabling educational technology answers.
