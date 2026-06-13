# Week 4 Lesson Plan: RAG — Retrieval Augmented Generation

**Total Duration:** ~20-25 hours over 5-6 days

| Day | Topics | Notebook(s) / Project | Duration | Deliverable |
|-----|--------|-----------------------|----------|-------------|
| 1 | RAG architecture + Chunking | `01_rag_architecture.py`, `02_chunking_strategies.py` | 4h | Assignments 1-2 |
| 2 | Vector search (FAISS/Chroma) | `03_vector_search_faiss_chroma.py` | 3h | Assignment 3 |
| 3 | Hybrid search + Reranking | `04_hybrid_search_reranking.py`, `labs/lab3_hybrid_search.py` | 4h | Assignment 4, Lab 3 |
| 4 | Metadata filtering + Evaluation | `05_metadata_filtering.py`, `06_rag_evaluation.py` | 4h | Assignments 5-6 |
| 5 | RAG frameworks | `labs/lab1_langchain_rag.py`, `labs/lab2_llamaindex_rag.py` | 4h | Labs 1-2 |
| 6 | PDF Chatbot project | `../projects/pdf_chatbot/` | 4-5h | Assignment 7 (project) |

## Prerequisites Check (Day 0)
```bash
pip install -r AI-Bootcamp/requirements.txt
pip install pypdf streamlit rank-bm25       # extras for labs/project
export ANTHROPIC_API_KEY=...                 # for generation (offline fallbacks provided)
```
> All concept notebooks include offline-safe demos (hash embeddings, pure-Python BM25), so the
> theory and core exercises run without any API key or model download.

## Model Note
Generation examples use `claude-opus-4-8`; `claude-fable-5` is Anthropic's most capable model.
Local embeddings use `all-MiniLM-L6-v2` (free, offline). Keys come from the environment.

## Assessment
- 7 assignments — see `assignments/week04_assignments.md`
- 3 labs (LangChain, LlamaIndex, hybrid+rerank) — see `labs/`
- 1 project — PDF Chatbot (`../projects/pdf_chatbot/`)
- End-of-week quiz from `../interview-prep/week04_rag_questions.md`

## Success Criteria
By the end of Week 4, students can:
- Explain and build the full RAG pipeline end to end
- Choose chunking strategies and justify chunk size/overlap
- Use FAISS and Chroma for vector search with metadata filtering
- Implement hybrid search (BM25 + vector) with reranking
- Evaluate RAG quality (recall@k, precision@k, MRR, faithfulness)
- Ship a working PDF chatbot with citations and a "don't know" guard
