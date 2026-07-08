# Project: PDF Chatbot (Week 4 RAG)

A production-style RAG application that lets users chat with their PDF documents. Built with
Streamlit (UI), a vector store (Chroma), local embeddings (sentence-transformers), and Claude
for generation.

## Features
- Upload one or more PDFs
- Automatic chunking + embedding + indexing
- Ask questions; get answers grounded in the PDFs **with citations** (file + page)
- "I don't know" guard when no relevant context is found

## Architecture
```
PDF upload ─► extract text (pypdf) ─► chunk ─► embed (MiniLM) ─► Chroma
User question ─► embed ─► retrieve top-k (+score threshold) ─► prompt ─► Claude ─► answer + citations
```
See `../../diagrams/week04_rag/README.md`.

## Setup
```bash
pip install streamlit chromadb sentence-transformers pypdf anthropic
export ANTHROPIC_API_KEY="sk-ant-..."     # never hardcode
streamlit run app.py
```

## Files
- `rag_core.py` — reusable RAG functions: extract, chunk, index, retrieve, answer (provided)
- `app.py` — Streamlit application (provided)

## Usage
1. Run `streamlit run app.py`.
2. Upload PDFs in the sidebar; wait for indexing.
3. Ask questions in the chat box; answers cite the source file and page.

## Production Hardening Checklist
- [ ] Validate uploaded file type/size; sanitize filenames
- [ ] Per-user/session collection isolation (multi-tenant)
- [ ] Retrieval score threshold + graceful "I don't know"
- [ ] Logging + basic eval (recall@k, faithfulness) on a sample query set
- [ ] Secrets via environment variables / secret manager (never in code)
