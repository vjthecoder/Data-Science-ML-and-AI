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
        # Lab 1: RAG Pipeline with LangChain + Chroma

        **Goal:** Build a complete RAG pipeline — load, chunk, embed, store, retrieve, generate —
        using LangChain and Chroma.

        **Setup:**
        ```bash
        pip install langchain langchain-community langchain-anthropic chromadb sentence-transformers
        export ANTHROPIC_API_KEY="sk-ant-..."
        ```

        ## Pipeline steps
        1. Load documents.
        2. Split into chunks.
        3. Embed + store in Chroma.
        4. Retrieve top-k for a query.
        5. Generate a grounded answer with Claude.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Full pipeline

        ```python
        from langchain_community.document_loaders import TextLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_community.embeddings import HuggingFaceEmbeddings
        from langchain_community.vectorstores import Chroma
        from langchain_anthropic import ChatAnthropic
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.runnables import RunnablePassthrough
        from langchain_core.output_parsers import StrOutputParser

        # 1. Load
        docs = TextLoader("knowledge_base.txt").load()

        # 2. Split
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(docs)

        # 3. Embed + store (local, free embeddings)
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

        # 4 + 5. Retrieve + generate
        llm = ChatAnthropic(model="claude-opus-4-8", max_tokens=1024)
        prompt = ChatPromptTemplate.from_template(
            "Answer the question using ONLY the context. If the context lacks the answer, "
            "say you don't know.\n\nContext:\n{context}\n\nQuestion: {question}"
        )

        def format_docs(docs):
            return "\n\n".join(d.page_content for d in docs)

        chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt | llm | StrOutputParser()
        )

        print(chain.invoke("What is the refund policy?"))
        ```
        """
    )
    return


@app.cell
def __():
    # Offline-safe mini-RAG so the lab runs without LangChain/keys (same conceptual flow)
    import numpy as np

    kb = [
        "Refunds are available within 30 days of purchase for Pro plans.",
        "Free plans are not eligible for refunds.",
        "To reset your password, click 'Forgot password' on the login page.",
        "Support is available 24/7 via chat for Enterprise customers.",
    ]

    def embed(t):
        v = np.zeros(64)
        for w in t.lower().split():
            v[hash(w) % 64] += 1.0
        n = np.linalg.norm(v)
        return v / n if n else v

    vecs = np.array([embed(d) for d in kb])

    def rag(query, k=2):
        q = embed(query)
        top = np.argsort(vecs @ q)[::-1][:k]
        context = "\n".join(kb[i] for i in top)
        # Stand-in for the LLM: echo the most relevant chunk
        return context, kb[top[0]]

    context, best = rag("How do I get a refund?")
    print("Retrieved context:\n", context)
    print("\n(LLM would answer grounded in:)", best)
    return best, context, embed, kb, np, rag, vecs


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Deliverable
        A script `langchain_rag.py` that builds the pipeline over a real `.txt`/`.md` knowledge
        base and answers 3 questions with citations (include `source` metadata in the output).

        ## Stretch Goal
        Add a "no answer" guard using a retrieval score threshold, and return the source filename
        + chunk for each answer.
        """
    )
    return


if __name__ == "__main__":
    app.run()
