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
        # Lab 2: RAG Pipeline with LlamaIndex + FAISS

        **Goal:** Build the same RAG capability with LlamaIndex (a data framework for LLM apps)
        backed by a FAISS vector store, and compare the developer experience to LangChain (Lab 1).

        **Setup:**
        ```bash
        pip install llama-index llama-index-vector-stores-faiss faiss-cpu \
                    llama-index-llms-anthropic llama-index-embeddings-huggingface
        export ANTHROPIC_API_KEY="sk-ant-..."
        ```

        ## Steps
        1. Load documents from a directory.
        2. Configure embedding model + LLM.
        3. Build a FAISS-backed index.
        4. Query and inspect source nodes (citations).
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Full pipeline

        ```python
        import faiss
        from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
        from llama_index.vector_stores.faiss import FaissVectorStore
        from llama_index.llms.anthropic import Anthropic
        from llama_index.embeddings.huggingface import HuggingFaceEmbedding

        # 1. Load all files in ./data
        documents = SimpleDirectoryReader("./data").load_data()

        # 2. Configure models globally
        Settings.embed_model = HuggingFaceEmbedding(model_name="all-MiniLM-L6-v2")
        Settings.llm = Anthropic(model="claude-opus-4-8", max_tokens=1024)

        # 3. FAISS-backed index
        d = 384  # all-MiniLM-L6-v2 dimension
        faiss_index = faiss.IndexFlatIP(d)
        vector_store = FaissVectorStore(faiss_index=faiss_index)
        storage = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents(documents, storage_context=storage)

        # 4. Query with citations
        engine = index.as_query_engine(similarity_top_k=4)
        response = engine.query("What is the refund policy?")
        print(response)
        for node in response.source_nodes:                 # citations / provenance
            print(round(node.score, 3), node.metadata.get("file_name"), node.text[:80])
        ```
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## LangChain vs LlamaIndex (when to use which)

        | | LangChain | LlamaIndex |
        |---|-----------|------------|
        | Focus | general LLM app orchestration, chains, agents | data ingestion + retrieval for RAG |
        | Strength | flexible composition, many integrations | document loaders, indices, query engines |
        | Citations | manual via metadata | `source_nodes` built-in |
        | Good first pick for | complex agent workflows | document-heavy RAG |

        Both are excellent; many teams use them together (LlamaIndex for retrieval, LangChain for
        orchestration).
        """
    )
    return


@app.cell
def __():
    # Offline-safe parallel (same flow as Lab 1's mini-RAG, framed as "index → query engine")
    import numpy as np

    class MiniQueryEngine:
        def __init__(self, docs):
            self.docs = docs
            self.vecs = np.array([self._embed(d) for d in docs])

        def _embed(self, t):
            v = np.zeros(64)
            for w in t.lower().split():
                v[hash(w) % 64] += 1.0
            n = np.linalg.norm(v)
            return v / n if n else v

        def query(self, q, k=2):
            qv = self._embed(q)
            top = np.argsort(self.vecs @ qv)[::-1][:k]
            return [(self.docs[i], float((self.vecs[i] @ qv))) for i in top]

    engine = MiniQueryEngine([
        "Refunds within 30 days for Pro plans.",
        "Free plans have no refunds.",
        "Reset password from the login page.",
    ])
    for text, score in engine.query("refund eligibility"):
        print(round(score, 3), text)
    return MiniQueryEngine, engine, np


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Deliverable
        A script `llamaindex_rag.py` that indexes a `./data` directory and answers 3 questions,
        printing the source file + score for each (citations).

        ## Stretch Goal
        Persist the FAISS index to disk and reload it without re-indexing; measure the time saved
        on the second run.
        """
    )
    return


if __name__ == "__main__":
    app.run()
