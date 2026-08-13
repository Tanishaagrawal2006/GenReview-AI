# RAG Setup for ReviewFlow AI

This document explains how to set up and manage the Retrieval-Augmented Generation (RAG) capabilities in ReviewFlow AI.

## 1. Install Dependencies
Make sure you have installed the newly added requirements which include ChromaDB and `sentence-transformers`:

```bash
pip install -r requirements.txt
```

## 2. Bootstrapping the RAG Index
If you are deploying this RAG update to an existing database, the new `business_knowledge` schema table will be created automatically on the next application start.

However, existing businesses will not have their historical feedback indexed in the new vector store until you run the backfill script. 

Run this command once:
```bash
python scripts/backfill_rag_index.py
```

This script will loop through all existing businesses and push their resolved customer feedback into the `./chroma_store` vector database.

## 3. How RAG Works
- **Storage**: We use an embedded, local `ChromaDB` directory (`./chroma_store/`) to avoid external vector database dependencies.
- **Embedding**: We use a lightweight, local embedding model `all-MiniLM-L6-v2` via `sentence-transformers`. This prevents unnecessary API costs.
- **Multi-tenant Isolation**: Each business has its own dedicated collection named `biz_{id}` inside Chroma.
- **Ingestion Triggers**:
  - Automatically upon a new business registration.
  - Automatically when a customer accepts an AI-generated review draft.
  - Automatically when a business owner adds or deletes from their knowledge base in the dashboard.
- **Graceful Degradation**: If ChromaDB fails or the local embeddings throw an error, the pipeline soft-fails open, falling back to the standard, prompt-only review generation.
