# Week 4 Assignments

Complete each in a new Marimo notebook or `.py` script in this folder. Reference solutions are
in `../solutions/`. Concept assignments run offline; lab/project assignments may need keys.

> **Secrets:** load API keys from environment variables; never hardcode.

---

## Assignment 1 — RAG Architecture

1. Build the toy NumPy RAG from notebook 01 over a 10-document corpus.
2. Make `rag_answer` call a real LLM (Anthropic/OpenAI) and return the generated answer, with an
   offline fallback that prints the prompt.
3. Add a relevance threshold: if the top similarity is below it, return "I don't know."
4. In 4-5 sentences, explain when RAG is preferable to fine-tuning and vice versa.

---

## Assignment 2 — Chunking

1. Implement fixed-size (no overlap), fixed-size (with overlap), and recursive chunkers.
2. Chunk a ~1000-word document with each and report the number of chunks.
3. Construct a query whose answer spans a chunk boundary; show overlap retrieves the full
   answer where no-overlap splits it.
4. Write a markdown-heading-aware chunker that attaches the heading path as metadata.

---

## Assignment 3 — Vector Search

1. Build a FAISS `IndexFlatIP` over 15 chunks; retrieve top-3 for 3 queries.
2. Persist the same data in Chroma; re-open the client and confirm the data survives.
3. Add a score threshold so low-similarity hits are dropped; show an example query that returns
   nothing after thresholding.

---

## Assignment 4 — Hybrid Search & Reranking

1. Implement BM25 keyword scoring and vector scoring over the same 8-chunk corpus.
2. Fuse them with Reciprocal Rank Fusion; compare top-3 to vector-only and BM25-only.
3. Construct a query with an exact code/ID where hybrid clearly beats vector-only.
4. (Stretch) Add a cross-encoder reranker and report precision@3 before vs after reranking.

---

## Assignment 5 — Metadata Filtering

1. Build a corpus where each chunk has `product`, `lang`, and `date` metadata.
2. Run queries with: a single filter, an AND filter, and an OR/`in` filter.
3. Demonstrate a case where post-filtering (filter after top-k) returns fewer than k results and
   explain why pre-filtering is safer.
4. Add a mandatory `access` filter and show how it prevents retrieving restricted documents.

---

## Assignment 6 — RAG Evaluation

1. Build a 10-question eval set over your corpus with ground-truth chunk ids and reference
   answers.
2. Compute mean recall@3, precision@3, and MRR for your retriever.
3. Implement a keyword-overlap faithfulness proxy; flag answers below 0.5.
4. Change the chunk size and re-run; report how each metric moves and which config you'd ship.

---

## Assignment 7 — PDF Chatbot Project

1. Run the `projects/pdf_chatbot` app on 2-3 PDFs of your choice.
2. Add citations (source file + page) to every answer (already supported — verify).
3. Add the "I don't know" guard using a retrieval score threshold.
4. Write a 1-page README addition: architecture diagram, 3 example Q&A, and 3 limitations you
   observed.
