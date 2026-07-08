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
        # 03. Vector Search with FAISS & Chroma

        ## Theory

        **Level 1 (10-year-old):** After cutting our book into pieces and turning each into
        numbers, we need a fast way to find the pieces closest in meaning to a question. That's
        what a vector search engine does.

        **Level 2 (College Student):** This is the retrieval engine of RAG. **FAISS** is an
        in-process library for fast similarity search — great for prototyping and embedded use.
        **Chroma** adds persistence, metadata storage, and a simple API (and can embed text for
        you). Both return the top-k most similar chunks for a query embedding.

        **Level 3 (Industry Professional):** Choose based on scale and ops needs: FAISS (embedded,
        you manage persistence), Chroma/pgvector (persistence + metadata, single-node to moderate
        scale), managed services (Pinecone/Weaviate, for large multi-tenant scale). Normalize
        vectors and use inner-product for cosine similarity; tune ANN parameters for the
        recall/latency trade-off; and always store metadata for filtering and citations.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Visual Explanation

        ```
        Build (once):   chunks ─embed─► vectors(+metadata) ─► index.add()
        Query (per Q):  question ─embed─► index.search(q, k) ─► top-k chunk ids + scores
                                                                       │
                                                                       ▼
                                                        fetch chunk text + metadata → prompt
        ```
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## FAISS — in-process, fast

        ```python
        # pip install faiss-cpu sentence-transformers
        import faiss, numpy as np
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("all-MiniLM-L6-v2")
        chunks = ["Paris is the capital of France.", "Python is great for data science.",
                  "The Eiffel Tower is in Paris.", "Vector DBs store embeddings."]
        emb = model.encode(chunks, normalize_embeddings=True).astype("float32")

        index = faiss.IndexFlatIP(emb.shape[1])   # inner product == cosine on normalized vectors
        index.add(emb)

        q = model.encode("Where is the Eiffel Tower?", normalize_embeddings=True).astype("float32")
        scores, ids = index.search(q.reshape(1, -1), k=2)
        for i, s in zip(ids[0], scores[0]):
            print(round(float(s), 3), chunks[i])
        ```
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Chroma — persistence + metadata

        ```python
        # pip install chromadb
        import chromadb
        client = chromadb.PersistentClient(path="./chroma_db")
        coll = client.get_or_create_collection("kb")

        coll.add(
            ids=["1", "2", "3"],
            documents=["Paris is the capital of France.",
                       "The Eiffel Tower is in Paris.",
                       "Python is great for data science."],
            metadatas=[{"topic": "geo"}, {"topic": "geo"}, {"topic": "tech"}],
        )  # Chroma embeds with a default model if you don't pass embeddings

        res = coll.query(query_texts=["Where is the Eiffel Tower?"], n_results=2)
        print(res["documents"][0])

        # Persisted: re-open the same path later and the data is still there.
        ```
        """
    )
    return


@app.cell
def __():
    # Offline-safe end-to-end retriever (no downloads) using a hash embedding
    import numpy as np

    class TinyVectorStore:
        def __init__(self, dim=128):
            self.dim = dim
            self.vecs = None
            self.docs = []
            self.meta = []

        def _embed(self, text):
            v = np.zeros(self.dim)
            for w in text.lower().split():
                v[hash(w) % self.dim] += 1.0
            n = np.linalg.norm(v)
            return v / n if n else v

        def add(self, docs, metadatas=None):
            metadatas = metadatas or [{} for _ in docs]
            new = np.array([self._embed(d) for d in docs])
            self.vecs = new if self.vecs is None else np.vstack([self.vecs, new])
            self.docs += list(docs)
            self.meta += list(metadatas)

        def query(self, text, k=2):
            q = self._embed(text)
            sims = self.vecs @ q
            top = np.argsort(sims)[::-1][:k]
            return [(self.docs[i], self.meta[i], float(sims[i])) for i in top]

    store = TinyVectorStore()
    store.add(
        ["Paris is the capital of France.", "The Eiffel Tower is in Paris.",
         "Python is great for data science.", "Vector databases store embeddings."],
        [{"topic": "geo"}, {"topic": "geo"}, {"topic": "tech"}, {"topic": "tech"}],
    )
    for doc, meta, score in store.query("Where is the Eiffel Tower?"):
        print(round(score, 3), meta, doc)
    return TinyVectorStore, np, store


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Real-World Example

        A docs site embeds every help article into Chroma with `{"product": ..., "version": ...}`
        metadata. Queries retrieve the closest articles AND filter to the user's product version —
        combining semantic search with structured filtering (covered in notebook 05).

        ## Coding Exercise

        1. Build a FAISS `IndexFlatIP` over 15 chunks and retrieve top-3 for 3 queries.
        2. Persist the same data in Chroma, then re-open the client and confirm the data survives.
        3. Add a `score_threshold` to the retriever so low-similarity hits are dropped.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Assignment
        See `../assignments/week04_assignments.md` — Assignment 3.

        ## Interview Questions
        See `../../interview-prep/week04_rag_questions.md` — Section: Vector Search.

        ## Industry Use Cases
        - The retrieval engine in every RAG application
        - Semantic site search; duplicate detection

        ## Common Mistakes
        - Not normalizing vectors before cosine/inner-product search
        - Different embedding model at index time vs query time
        - No persistence strategy (losing the index on restart)

        ## Best Practices
        - Normalize + inner-product for cosine; store metadata
        - Pin the embedding model version; persist the index
        - Add a score threshold to avoid irrelevant retrievals

        ## Further Reading
        - FAISS wiki; Chroma documentation
        - pgvector for Postgres-native vector search
        """
    )
    return


if __name__ == "__main__":
    app.run()
