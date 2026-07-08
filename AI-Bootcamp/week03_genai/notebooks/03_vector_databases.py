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
        # 03. Vector Databases

        ## Theory

        **Level 1 (10-year-old):** A vector database is a magic library where books are arranged
        by *meaning* instead of by title. Ask for "something about brave knights" and it instantly
        hands you the closest books — even if none have "brave" in the title.

        **Level 2 (College Student):** A vector database stores embedding vectors and supports
        fast **nearest-neighbor search** — given a query vector, find the k most similar stored
        vectors. Exact search is O(n); at scale we use **Approximate Nearest Neighbor (ANN)**
        indexes like HNSW (graph-based) or IVF (cluster-based) to trade a little accuracy for
        huge speedups. Each vector carries **metadata** (source, date, tags) for filtering.

        **Level 3 (Industry Professional):** Vector DBs (Chroma, FAISS, Pinecone, Weaviate,
        pgvector) are the storage layer of RAG. Engineering decisions: HNSW (high recall, more
        memory) vs IVF (lower memory, tunable); the recall/latency trade-off via parameters
        (`ef_search`, `nprobe`); hybrid search combining vector + keyword (BM25); and metadata
        filtering pushed into the index. FAISS is an in-process library (great for prototyping
        and embedded use); Chroma adds persistence and metadata; managed services add scaling,
        replication, and multi-tenancy.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Visual Explanation

        ```
        Indexing (once):                       Querying (per request):
        docs ──embed──► vectors ──► [Vector    query ──embed──► q_vec
                         + metadata    DB ]                       │
                                        ▲                         ▼
                                        └────── k-NN search ◄── top-k similar
                                                                  + metadata filter

        Index types:
          Flat (exact)  : scan all vectors        — small data, 100% recall
          IVF (clusters): search nearest clusters — large data, tune nprobe
          HNSW (graph)  : navigate a graph        — high recall, more memory
        ```
        """
    )
    return


@app.cell
def __():
    # Simple Example: exact k-NN search in NumPy (the core idea behind every vector DB)
    import numpy as np

    rng = np.random.default_rng(0)
    corpus = rng.normal(size=(1000, 8))          # 1000 documents, dim 8
    corpus /= np.linalg.norm(corpus, axis=1, keepdims=True)

    query = rng.normal(size=8)
    query /= np.linalg.norm(query)

    sims = corpus @ query                         # cosine sim (vectors are normalized)
    top_k = np.argsort(sims)[::-1][:5]
    print("Top-5 doc indices:", top_k)
    print("Their similarities:", sims[top_k].round(3))
    return corpus, np, query, rng, sims, top_k


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Real-World Example: FAISS (in-process) and Chroma (persistent)

        ### FAISS — fast, embedded, no server
        ```python
        # pip install faiss-cpu numpy
        import faiss, numpy as np

        d = 384
        index = faiss.IndexFlatIP(d)             # inner product = cosine on normalized vectors
        index.add(doc_embeddings.astype("float32"))   # shape (N, d)

        scores, ids = index.search(query_embedding.astype("float32"), k=5)
        # For large corpora, switch to IndexHNSWFlat or IndexIVFFlat
        ```

        ### Chroma — persistence + metadata filtering
        ```python
        # pip install chromadb
        import chromadb
        client = chromadb.PersistentClient(path="./chroma_db")
        coll = client.get_or_create_collection("docs")

        coll.add(
            ids=["a", "b", "c"],
            documents=["reset password", "billing FAQ", "login errors"],
            metadatas=[{"category": "auth"}, {"category": "billing"}, {"category": "auth"}],
        )  # Chroma embeds with a default model if you don't pass embeddings

        results = coll.query(
            query_texts=["I can't sign in"],
            n_results=2,
            where={"category": "auth"},          # metadata filter pushed into the search
        )
        print(results["documents"])
        ```
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Coding Exercise

        1. Build a Flat FAISS index over the 1000 toy vectors above and confirm it returns the
           same top-5 as the NumPy brute-force search.
        2. Build an `IndexHNSWFlat` index and compare its top-5 to exact search — how many
           overlap? (This is **recall@5**.)
        3. In Chroma, add 6 documents across 2 categories and run a query with a `where` metadata
           filter. Confirm only the filtered category is returned.
        """
    )
    return


@app.cell
def __(corpus, np, query, top_k):
    # Offline-safe parallel: simulate an "approximate" index by searching a random 30% subset
    rng2 = np.random.default_rng(7)
    subset = rng2.choice(len(corpus), size=300, replace=False)
    approx_sims = corpus[subset] @ query
    approx_top = subset[np.argsort(approx_sims)[::-1][:5]]
    recall = len(set(approx_top) & set(top_k)) / 5
    print("Exact  top-5:", sorted(top_k.tolist()))
    print("Approx top-5:", sorted(approx_top.tolist()))
    print("recall@5 (approx vs exact):", recall)
    return approx_sims, approx_top, recall, rng2, subset


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Assignment
        See `../assignments/week03_assignments.md` — Assignment 3.

        ## Interview Questions
        See `../../interview-prep/week03_genai_questions.md` — Section: Vector Databases.

        ## Industry Use Cases
        - Storage/retrieval layer for RAG (Week 4)
        - Semantic product search and recommendations
        - Deduplication and near-duplicate detection at scale

        ## Common Mistakes
        - Using exact search at scale (too slow) or ANN with untuned params (low recall)
        - Storing vectors without metadata (no filtering, no citations)
        - Re-embedding with a different model than was used for indexing

        ## Best Practices
        - Normalize vectors; use inner-product index for cosine
        - Always attach metadata (source, date) for filtering + citations
        - Measure recall@k when choosing/tuning an ANN index

        ## Further Reading
        - FAISS wiki (index types, HNSW, IVF)
        - Chroma & pgvector documentation
        - "Billion-scale similarity search with GPUs" (FAISS paper)
        """
    )
    return


if __name__ == "__main__":
    app.run()
