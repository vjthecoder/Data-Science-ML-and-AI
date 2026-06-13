# Week 4 Interview Questions: RAG — Retrieval Augmented Generation

## RAG Architecture
1. Walk through the two phases of RAG (indexing and query) end to end.
2. Why does RAG reduce hallucination compared to a plain LLM?
3. When would you choose RAG over fine-tuning? Over long-context stuffing?
4. What does it mean to "separate knowledge from reasoning" in RAG?
5. How would you add citations/traceability to a RAG answer?
6. What is a "no relevant context" guard and why does it matter?

## Chunking
7. What trade-off does chunk size control?
8. Why use chunk overlap? What's a reasonable overlap percentage?
9. Compare fixed-size, recursive, and semantic chunking.
10. How would you chunk a markdown document vs source code vs a table-heavy PDF?
11. Why keep metadata (heading, page, source) on each chunk?

## Vector Search
12. Why use inner product on normalized vectors for cosine similarity?
13. FAISS vs Chroma vs a managed service — when would you pick each?
14. Why must the embedding model be identical at index time and query time?
15. What is a retrieval score threshold and why add one?
16. How do you persist and reload a vector index to avoid re-indexing?

## Hybrid Search & Reranking
17. Why does pure vector search sometimes miss exact terms or codes?
18. What is BM25 and what does it capture that embeddings don't?
19. Explain Reciprocal Rank Fusion. Why is it robust without score normalization?
20. What is a cross-encoder reranker, and why only rerank a small candidate set?
21. Describe the full retrieve-broad → fuse → rerank-narrow pipeline.

## Metadata Filtering
22. Why is metadata filtering essential for multi-tenant / permissioned RAG?
23. Pre-filtering vs post-filtering — what's the difference and which is safer?
24. How would you enforce access control as part of retrieval?
25. Name three uses of metadata beyond permissions (freshness, locale, citations).

## RAG Evaluation
26. Why must you evaluate retrieval and generation separately?
27. Define recall@k, precision@k, and MRR for retrieval.
28. What is faithfulness, and why is it the key generation metric?
29. What is LLM-as-judge, and what's its main risk?
30. How would you wire RAG evals into CI to gate deploys?

## Scenario / System Design
31. Design a customer-support RAG bot over a help center. Cover chunking, embeddings, retrieval,
    filtering, generation, citations, and evaluation.
32. Your RAG bot gives confident but wrong answers. Diagnose the likely causes across the
    pipeline and propose fixes.
33. Queries with product codes return generic articles. How do you fix retrieval?
34. A user reports the bot answered using a document they shouldn't see. What went wrong, and how
    do you prevent it?
35. You changed the chunk size and answers "feel" different. How do you decide objectively
    whether to ship the change?
