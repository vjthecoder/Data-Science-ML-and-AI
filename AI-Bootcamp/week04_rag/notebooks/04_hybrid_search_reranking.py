import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    return (mo,)


@app.cell
def __(mo):
    mo.md(
        r"""
        # 04. Hybrid Search & Reranking

        ## Theory

        **Level 1 (10-year-old):** Searching by *meaning* is great, but sometimes you need the
        *exact word* (like a product code "X-450"). Hybrid search does both — meaning search AND
        keyword search — then a smart helper re-sorts the results so the best ones are on top.

        **Level 2 (College Student):** **Vector search** captures semantic similarity but can miss
        exact terms, rare names, or codes. **Keyword search (BM25)** nails exact matches but
        misses synonyms. **Hybrid search** combines both (e.g. weighted score or Reciprocal Rank
        Fusion). **Reranking** then uses a cross-encoder — a model that reads the query and each
        candidate *together* — to produce a precise final ordering of the top candidates.

        **Level 3 (Industry Professional):** Hybrid + rerank is the standard recipe for
        production-grade retrieval precision. Pipeline: retrieve a broad candidate set (e.g. top-50
        from vector + BM25), fuse, then rerank the merged set down to the top-5 with a
        cross-encoder. Cross-encoders are slow (they run per query-document pair), so only rerank
        a small candidate set. RRF is a simple, robust fusion that needs no score normalization.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Visual Explanation

        ```
        Query
          ├─► Vector search ─► top-50 (semantic)   ┐
          └─► BM25 keyword  ─► top-50 (lexical)     ├─► Fuse (RRF) ─► merged top-50
                                                     ┘
          merged top-50 ─► Cross-encoder reranker ─► precise top-5 ─► prompt

        RRF score(d) = Σ over rankers of  1 / (k + rank_r(d))     (k≈60)
        Bi-encoder (fast):  embed(query)·embed(doc)
        Cross-encoder (precise, slow):  model(query, doc) → relevance score
        ```
        """
    )
    return


@app.cell
def __():
    # Simple Example: BM25-style keyword scoring + Reciprocal Rank Fusion (pure Python)
    import math
    from collections import Counter

    docs = [
        "The X-450 router supports dual-band WiFi.",
        "Our fastest wireless router for large homes.",
        "Reset instructions for network devices.",
        "The X-450 firmware update fixes connection drops.",
    ]

    def bm25_scores(query, docs, k1=1.5, b=0.75):
        tokenized = [d.lower().split() for d in docs]
        avgdl = sum(len(d) for d in tokenized) / len(tokenized)
        N = len(docs)
        df = Counter()
        for d in tokenized:
            for w in set(d):
                df[w] += 1
        scores = []
        for d in tokenized:
            tf = Counter(d)
            s = 0.0
            for w in query.lower().split():
                if w in tf:
                    idf = math.log(1 + (N - df[w] + 0.5) / (df[w] + 0.5))
                    s += idf * tf[w] * (k1 + 1) / (tf[w] + k1 * (1 - b + b * len(d) / avgdl))
            scores.append(s)
        return scores

    def rrf(rank_lists, k=60):
        fused = {}
        for ranking in rank_lists:
            for rank, idx in enumerate(ranking):
                fused[idx] = fused.get(idx, 0) + 1 / (k + rank)
        return sorted(fused, key=fused.get, reverse=True)

    # Pretend vector search returned this order (semantic): doc 1, 3, 0, 2
    vector_rank = [1, 3, 0, 2]
    bm25 = bm25_scores("X-450 router", docs)
    bm25_rank = sorted(range(len(docs)), key=lambda i: bm25[i], reverse=True)

    print("BM25 ranking   :", bm25_rank)
    print("Vector ranking :", vector_rank)
    print("Fused (RRF)    :", rrf([bm25_rank, vector_rank]))
    return Counter, bm25, bm25_rank, bm25_scores, docs, math, rrf, vector_rank


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Reranking with a cross-encoder (production)

        ```python
        # pip install sentence-transformers
        from sentence_transformers import CrossEncoder

        reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        query = "X-450 router setup"
        candidates = [docs[i] for i in fused_top50]      # from hybrid fusion
        scores = reranker.predict([(query, c) for c in candidates])
        reranked = [c for _, c in sorted(zip(scores, candidates), reverse=True)][:5]
        ```

        The cross-encoder reads (query, doc) jointly, so it judges relevance far more precisely
        than the bi-encoder used for first-stage retrieval — but it's slower, so only rerank the
        merged candidate set, not the whole corpus.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Real-World Example

        An e-commerce support bot must find docs for "X-450 keeps disconnecting." Pure vector
        search might surface generic "wireless router" articles; BM25 locks onto "X-450"; fusion +
        rerank puts the exact X-450 firmware-fix article on top.

        ## Coding Exercise

        1. Implement weighted hybrid fusion: `final = α * norm(vector) + (1-α) * norm(bm25)`.
           Compare top-3 for α = 0, 0.5, 1.0.
        2. Implement RRF (above) and compare its top-3 to weighted fusion on the same query.
        3. (Stretch) Add a real cross-encoder reranker and show it reorders the fused candidates.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Assignment
        See `../assignments/week04_assignments.md` — Assignment 4.

        ## Interview Questions
        See `../../interview-prep/week04_rag_questions.md` — Section: Hybrid Search & Reranking.

        ## Industry Use Cases
        - Product/support search where exact codes and synonyms both matter
        - Legal/medical retrieval needing high precision
        - Any RAG system where first-stage recall isn't precise enough

        ## Common Mistakes
        - Reranking the entire corpus (cross-encoders are too slow for that)
        - Fusing raw scores without normalization (use RRF to avoid this)
        - Skipping hybrid when queries contain codes/IDs/rare terms

        ## Best Practices
        - Retrieve broad (vector + BM25), fuse with RRF, rerank narrow
        - Only rerank the top candidate set (e.g. 50 → 5)
        - Measure precision@k before and after reranking

        ## Further Reading
        - BM25 / Okapi BM25 reference
        - "Reciprocal Rank Fusion" (Cormack et al.)
        - sentence-transformers cross-encoder docs
        """
    )
    return


if __name__ == "__main__":
    app.run()
