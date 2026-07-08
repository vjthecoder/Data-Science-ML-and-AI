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
        # Lab 3: Hybrid Search + Reranking

        **Goal:** Build a retrieval pipeline that combines BM25 keyword search with vector search
        (fused via Reciprocal Rank Fusion) and reranks the result with a cross-encoder. Measure
        precision before and after.

        **Setup:**
        ```bash
        pip install rank-bm25 sentence-transformers numpy
        ```

        ## Steps
        1. Build a BM25 index and a vector index over the same chunks.
        2. Retrieve top-N from each; fuse with RRF.
        3. Rerank the fused candidates with a cross-encoder.
        4. Compare precision@3 of vector-only vs hybrid vs hybrid+rerank.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Production pipeline

        ```python
        from rank_bm25 import BM25Okapi
        from sentence_transformers import SentenceTransformer, CrossEncoder, util
        import numpy as np

        chunks = [...]  # your corpus

        # BM25 (lexical)
        bm25 = BM25Okapi([c.lower().split() for c in chunks])

        # Vector (semantic)
        embedder = SentenceTransformer("all-MiniLM-L6-v2")
        emb = embedder.encode(chunks, normalize_embeddings=True)

        def rrf(rank_lists, k=60):
            fused = {}
            for ranking in rank_lists:
                for rank, idx in enumerate(ranking):
                    fused[idx] = fused.get(idx, 0) + 1 / (k + rank)
            return sorted(fused, key=fused.get, reverse=True)

        def hybrid(query, n=20):
            bm = np.argsort(bm25.get_scores(query.lower().split()))[::-1][:n]
            qv = embedder.encode(query, normalize_embeddings=True)
            vec = np.argsort(emb @ qv)[::-1][:n]
            return rrf([list(bm), list(vec)])

        reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

        def search(query, k=3):
            cand = hybrid(query)[:20]
            scores = reranker.predict([(query, chunks[i]) for i in cand])
            order = [c for _, c in sorted(zip(scores, cand), reverse=True)]
            return [chunks[i] for i in order[:k]]
        ```
        """
    )
    return


@app.cell
def __():
    # Offline-safe hybrid demo: BM25-lite + hash vectors + RRF (no downloads)
    import math
    from collections import Counter

    import numpy as np

    chunks = [
        "The X-450 router supports dual-band WiFi.",
        "Our fastest wireless router for large homes.",
        "Reset instructions for network devices.",
        "The X-450 firmware update fixes connection drops.",
        "Wireless routers can be configured via the web portal.",
    ]

    def embed(t):
        v = np.zeros(64)
        for w in t.lower().split():
            v[hash(w) % 64] += 1.0
        n = np.linalg.norm(v)
        return v / n if n else v

    emb = np.array([embed(c) for c in chunks])

    def bm25_scores(query):
        toks = [c.lower().split() for c in chunks]
        avgdl = sum(len(t) for t in toks) / len(toks)
        N, df = len(chunks), Counter()
        for t in toks:
            for w in set(t):
                df[w] += 1
        out = []
        for t in toks:
            tf, s = Counter(t), 0.0
            for w in query.lower().split():
                if w in tf:
                    idf = math.log(1 + (N - df[w] + 0.5) / (df[w] + 0.5))
                    s += idf * tf[w] * 2.5 / (tf[w] + 1.5 * (0.25 + 0.75 * len(t) / avgdl))
            out.append(s)
        return out

    def rrf(rank_lists, k=60):
        fused = {}
        for r in rank_lists:
            for rank, idx in enumerate(r):
                fused[idx] = fused.get(idx, 0) + 1 / (k + rank)
        return sorted(fused, key=fused.get, reverse=True)

    query = "X-450 router connection problem"
    vec_rank = list(np.argsort(emb @ embed(query))[::-1])
    bm_rank = list(np.argsort(bm25_scores(query))[::-1])
    fused = rrf([bm_rank, vec_rank])

    print("Vector top-3:", [chunks[i] for i in vec_rank[:3]])
    print("\nBM25   top-3:", [chunks[i] for i in bm_rank[:3]])
    print("\nHybrid top-3:", [chunks[i] for i in fused[:3]])
    return (Counter, bm25_scores, bm_rank, chunks, emb, embed, fused, math,
            np, query, rrf, vec_rank)


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Deliverable
        A script `hybrid_search.py` implementing vector-only, hybrid (RRF), and hybrid+rerank
        retrieval, with a small labeled query set and a printed precision@3 comparison of all
        three.

        ## Stretch Goal
        Plot precision@k for k = 1..5 across the three methods and write 3 sentences on when the
        added latency of reranking is worth it.
        """
    )
    return


if __name__ == "__main__":
    app.run()
