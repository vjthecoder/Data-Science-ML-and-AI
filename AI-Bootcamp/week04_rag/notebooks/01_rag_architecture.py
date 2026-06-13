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
        # 01. RAG Architecture Overview

        ## Theory

        **Level 1 (10-year-old):** An AI knows a lot but not *your* stuff — your notes, your
        company's documents. RAG lets it first *look things up* in your documents, then answer
        using what it found, like an open-book exam instead of a memory test.

        **Level 2 (College Student):** Retrieval-Augmented Generation has two phases. **Indexing
        (offline):** split documents into chunks → embed each chunk → store vectors + metadata in
        a vector DB. **Query (online):** embed the user's question → retrieve the top-k most
        similar chunks → stuff them into the prompt as context → the LLM answers grounded in those
        chunks (often with citations).

        **Level 3 (Industry Professional):** RAG reduces hallucination and keeps answers current
        without retraining the model. It separates *knowledge* (in the vector store, cheap to
        update) from *reasoning* (in the LLM). Production concerns span the whole pipeline:
        chunking strategy, embedding model choice/versioning, retrieval quality (recall),
        reranking precision, context-window budgeting, prompt construction, citation, and
        evaluation of BOTH retrieval and generation. RAG is usually cheaper and more maintainable
        than fine-tuning for knowledge-grounding use cases.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Visual Explanation

        ```
        INDEXING (offline, once per corpus):
          Documents ─► Chunk ─► Embed ─► [Vector DB: vectors + metadata]

        QUERY (online, per question):
          Question ─► Embed ─► Retrieve top-k ─► (optional rerank/filter)
                                       │
                                       ▼
          Prompt = system + retrieved chunks + question ─► LLM ─► grounded answer + citations
        ```
        See `../../diagrams/week04_rag/README.md` for the full pipeline diagram.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Why RAG vs alternatives

        | Approach | Update cost | Grounding | Best for |
        |----------|-------------|-----------|----------|
        | Plain LLM | n/a | weak (may hallucinate) | general knowledge |
        | Fine-tuning | high (retrain) | learns style, not facts well | behavior/format |
        | **RAG** | **low (re-index)** | **strong, with citations** | **your documents, fresh data** |
        | Long-context stuffing | per-request token cost | strong but expensive | small, fixed corpora |
        """
    )
    return


@app.cell
def __():
    # Minimal end-to-end RAG in ~30 lines of NumPy (no external services) to show the whole loop
    import numpy as np

    docs = [
        "The capital of France is Paris.",
        "Python is a popular programming language for data science.",
        "RAG retrieves documents and feeds them to an LLM to ground its answers.",
        "The Eiffel Tower is located in Paris, France.",
        "Vector databases store embeddings for fast similarity search.",
    ]

    def fake_embed(text):
        # Deterministic bag-of-words hash embedding (stand-in for a real embedding model)
        vec = np.zeros(64)
        for w in text.lower().split():
            vec[hash(w) % 64] += 1.0
        n = np.linalg.norm(vec)
        return vec / n if n else vec

    doc_vecs = np.array([fake_embed(d) for d in docs])

    def retrieve(query, k=2):
        q = fake_embed(query)
        sims = doc_vecs @ q
        top = np.argsort(sims)[::-1][:k]
        return [(docs[i], float(sims[i])) for i in top]

    def rag_answer(query, k=2):
        hits = retrieve(query, k)
        context = "\n".join(f"- {d}" for d, _ in hits)
        # In production, send `prompt` to an LLM (e.g. Anthropic claude-opus-4-8).
        prompt = f"Answer using ONLY this context:\n{context}\n\nQuestion: {query}"
        return prompt, hits

    prompt, hits = rag_answer("Where is the Eiffel Tower?")
    print("Retrieved:", [h[0] for h in hits])
    print("\nConstructed prompt:\n", prompt)
    return doc_vecs, docs, fake_embed, hits, np, prompt, rag_answer, retrieve


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Real-World Example

        A law firm indexes 50,000 contracts. When an associate asks "What's the termination
        notice period in the Acme MSA?", RAG retrieves the relevant clauses from *that* contract
        and the LLM answers with a citation to the exact section — grounded, current, and
        auditable, without retraining anything.

        ## Coding Exercise

        1. Add 5 more documents to the toy corpus and confirm retrieval still returns relevant
           chunks for 3 new questions.
        2. Make `rag_answer` actually call an LLM (Anthropic/OpenAI) with the constructed prompt
           and return the generated answer. Add a fallback that prints the prompt if no API key
           is set.
        3. Add a "no relevant context" guard: if the top similarity is below a threshold, return
           "I don't have information on that" instead of answering.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Assignment
        See `../assignments/week04_assignments.md` — Assignment 1.

        ## Interview Questions
        See `../../interview-prep/week04_rag_questions.md` — Section: RAG Architecture.

        ## Industry Use Cases
        - Document Q&A (legal, finance, healthcare, internal wikis)
        - Customer-support deflection grounded in help-center articles
        - Research assistants over scientific papers

        ## Common Mistakes
        - Treating RAG as one black box instead of a tunable pipeline
        - No "no relevant context" guard → confident hallucination
        - Ignoring citations/traceability

        ## Best Practices
        - Evaluate retrieval and generation separately
        - Always attach source metadata for citations
        - Add a relevance threshold and a graceful "I don't know"

        ## Further Reading
        - "Retrieval-Augmented Generation" (Lewis et al., 2020)
        - LangChain & LlamaIndex RAG guides
        - "Lost in the Middle" (long-context retrieval)
        """
    )
    return


if __name__ == "__main__":
    app.run()
