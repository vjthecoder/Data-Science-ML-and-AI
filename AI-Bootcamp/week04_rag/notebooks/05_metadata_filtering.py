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
        # 05. Metadata Filtering

        ## Theory

        **Level 1 (10-year-old):** Imagine searching only the *recent* books, or only the ones in
        *your* language. Metadata filtering lets the AI narrow the search before looking at
        meaning — faster and more accurate.

        **Level 2 (College Student):** Every chunk is stored with **metadata** (source, date,
        author, category, language, access level). At query time you combine semantic search with
        structured filters (`where category == "billing" AND date >= 2024`). This restricts
        retrieval to the relevant subset, improving precision and enabling permissions.

        **Level 3 (Industry Professional):** Metadata filtering is essential for multi-tenant and
        permissioned RAG — never retrieve documents a user isn't allowed to see. It also powers
        freshness (filter by date), localization (by language), and source attribution. Push
        filters into the vector index when possible (pre-filtering) rather than filtering after
        retrieval (post-filtering), which can return too few results. Design your metadata schema
        up front; it's expensive to backfill across a large corpus.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Visual Explanation

        ```
        Query: "refund policy"  +  filter: {product: "Pro", lang: "en", access: "public"}

        All chunks ──► [ filter by metadata ] ──► candidate subset ──► semantic search ──► top-k
                          (pre-filtering)

        Use cases:
          permissions: access ∈ user's allowed set   (security!)
          freshness:   date >= last_year
          locale:      lang == user_language
          source:      cite metadata["source"] in the answer
        ```
        """
    )
    return


@app.cell
def __():
    # Simple Example: metadata pre-filtering + semantic search (offline, hash embeddings)
    import numpy as np

    corpus = [
        {"text": "Pro plan refunds within 30 days.", "product": "Pro", "lang": "en"},
        {"text": "Free plan has no refunds.", "product": "Free", "lang": "en"},
        {"text": "Remboursements Pro sous 30 jours.", "product": "Pro", "lang": "fr"},
        {"text": "Pro plan billing cycle is monthly.", "product": "Pro", "lang": "en"},
    ]

    def embed(text):
        v = np.zeros(64)
        for w in text.lower().split():
            v[hash(w) % 64] += 1.0
        n = np.linalg.norm(v)
        return v / n if n else v

    def search(query, where=None, k=2):
        # 1) pre-filter by metadata
        items = [c for c in corpus if all(c.get(key) == val for key, val in (where or {}).items())]
        if not items:
            return []
        # 2) semantic search within the filtered subset
        q = embed(query)
        scored = sorted(items, key=lambda c: embed(c["text"]) @ q, reverse=True)
        return scored[:k]

    print("No filter:")
    for r in search("refund", k=3):
        print("  ", r["lang"], r["product"], "-", r["text"])

    print("\nFilter product=Pro, lang=en:")
    for r in search("refund", where={"product": "Pro", "lang": "en"}):
        print("  ", r["lang"], r["product"], "-", r["text"])
    return corpus, embed, search


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Real-World Example: Chroma metadata filter

        ```python
        results = collection.query(
            query_texts=["what is the refund policy?"],
            n_results=3,
            where={"$and": [{"product": "Pro"}, {"access": "public"}]},
        )
        ```

        For a permissioned enterprise assistant, the `where` clause restricts retrieval to
        documents the requesting user is authorized to see — making access control part of
        retrieval, not an afterthought.

        ## Coding Exercise

        1. Extend the corpus with a `date` field and add a filter `date >= 2024`.
        2. Implement an OR filter (e.g. `product in {"Pro", "Enterprise"}`).
        3. Show a case where post-filtering (filter AFTER top-k) returns fewer than k results,
           and explain why pre-filtering is safer.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Assignment
        See `../assignments/week04_assignments.md` — Assignment 5.

        ## Interview Questions
        See `../../interview-prep/week04_rag_questions.md` — Section: Metadata Filtering.

        ## Industry Use Cases
        - Permissioned/multi-tenant RAG (security-critical)
        - Freshness filtering (recent docs only)
        - Localization and source-scoped retrieval

        ## Common Mistakes
        - Post-filtering after top-k (can return too few results)
        - Designing metadata schema too late (expensive backfill)
        - Forgetting access-control filters → data leakage

        ## Best Practices
        - Pre-filter in the index; design metadata schema up front
        - Make access control a mandatory filter, not optional
        - Store source/date metadata for citations and freshness

        ## Further Reading
        - Chroma / pgvector / Pinecone metadata filtering docs
        - Multi-tenant RAG security patterns
        """
    )
    return


if __name__ == "__main__":
    app.run()
