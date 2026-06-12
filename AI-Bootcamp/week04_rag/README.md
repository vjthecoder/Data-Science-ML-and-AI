# Week 4: RAG — Retrieval Augmented Generation

## Learning Objectives
- Understand the RAG pipeline end-to-end
- Implement chunking, embedding, and vector search strategies
- Apply hybrid search, reranking, and metadata filtering
- Evaluate RAG system quality
- Build RAG apps with LangChain, LlamaIndex, Chroma, and FAISS

## Estimated Duration
20-25 hours

## Prerequisites
- Week 3 (embeddings, vector databases, prompt engineering)

## Modules
1. RAG Architecture Overview
2. Chunking Strategies — fixed-size, recursive, semantic
3. Embeddings for Retrieval
4. Vector Search — FAISS, Chroma
5. Hybrid Search — keyword (BM25) + vector
6. Reranking — cross-encoder rerankers
7. Metadata Filtering
8. RAG Evaluation — faithfulness, relevance, retrieval metrics

## Theory Notes
See `notebooks/` for diagrams of the RAG pipeline and worked examples for each stage.

## Jupyter Notebooks
- `notebooks/01_rag_architecture.ipynb`
- `notebooks/02_chunking_strategies.ipynb`
- `notebooks/03_vector_search_faiss_chroma.ipynb`
- `notebooks/04_hybrid_search_reranking.ipynb`
- `notebooks/05_metadata_filtering.ipynb`
- `notebooks/06_rag_evaluation.ipynb`

## Coding Labs
- `labs/lab1_langchain_rag.ipynb` — RAG pipeline with LangChain + Chroma
- `labs/lab2_llamaindex_rag.ipynb` — RAG pipeline with LlamaIndex + FAISS
- `labs/lab3_hybrid_search.ipynb` — BM25 + vector hybrid retrieval with reranking

## Mini Projects
- **PDF Chatbot** — chat over uploaded PDFs (`../projects/pdf_chatbot/`)
- **Website Knowledge Base** — crawl + index a site, Q&A over it
- **Customer Support Bot** — RAG over a support knowledge base with metadata filters

## Real Industry Examples
- Legal/compliance: chat over contracts and policy documents
- Internal docs: company wiki Q&A assistant
- Customer support: ticket deflection bots grounded in help-center articles

## Assignments
See `assignments/`

## Interview Questions
See `../interview-prep/week04_rag_questions.md`

## Common Mistakes
- Chunking too large (loses precision) or too small (loses context)
- Not normalizing/text-cleaning before embedding
- Ignoring retrieval evaluation — only checking final answer quality
- Mixing embedding models between indexing and querying

## Best Practices
- Choose chunk size based on embedding model context and content structure
- Add metadata (source, page, date) to every chunk for filtering and citations
- Use hybrid search + reranking for higher precision
- Evaluate retrieval (recall@k) separately from generation quality

## Further Reading
- LangChain & LlamaIndex documentation
- "Lost in the Middle" (long-context retrieval research)
- FAISS and Chroma documentation
