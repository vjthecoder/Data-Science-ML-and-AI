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
        # 02. Tokens & Embeddings

        ## Theory

        **Level 1 (10-year-old):** Computers don't read words — they read numbers. First we chop
        text into little pieces called **tokens** (often parts of words). Then we turn each token
        into a list of numbers (an **embedding**) so that words with similar meanings get similar
        number-lists.

        **Level 2 (College Student):** Tokenization (e.g. Byte-Pair Encoding) splits text into
        sub-word units, balancing vocabulary size against sequence length. Each token maps to a
        high-dimensional **embedding vector**. Embeddings are learned so that semantically
        similar items are close in vector space (measured by cosine similarity). Sentence/
        document embeddings (from models like `sentence-transformers` or provider embedding APIs)
        power search, clustering, and retrieval.

        **Level 3 (Industry Professional):** Token counts drive both cost and context limits —
        you pay per token, so prompt design is cost engineering. Embeddings are the backbone of
        RAG and semantic search. Critical rules: never compare embeddings across different models
        (different vector spaces), normalize vectors before cosine similarity, version your
        embedding model (re-embedding a corpus is expensive), and choose dimensionality based on
        the recall/cost/latency trade-off.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Visual Explanation

        ```
        Text:    "AI engineering"
                       │ tokenizer (BPE)
                       ▼
        Tokens:  ["AI", " engineer", "ing"]   (3 tokens — note sub-word splits)
                       │ embedding lookup
                       ▼
        Vectors: [[0.12, -0.4, ...],   ← 768 or 1536 numbers per token
                  [0.05,  0.9, ...],
                  [-0.3,  0.1, ...]]

        Cosine similarity:  cos(θ) = (a·b) / (‖a‖ ‖b‖)   ∈ [-1, 1]
        "king" ~ "queen"  → high   |   "king" ~ "banana" → low
        ```
        """
    )
    return


@app.cell
def __():
    # Simple Example: cosine similarity between toy embeddings
    import numpy as np

    def cosine(a, b):
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    king   = np.array([0.9, 0.1, 0.8])
    queen  = np.array([0.85, 0.15, 0.82])
    banana = np.array([0.1, 0.95, 0.05])

    print("king ~ queen :", round(cosine(king, queen), 3))   # high
    print("king ~ banana:", round(cosine(king, banana), 3))  # low
    return banana, cosine, king, np, queen


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Real-World Example: Semantic Search with sentence-transformers

        A help center embeds every article once. At query time it embeds the user's question and
        returns the articles with the highest cosine similarity — finding relevant docs even when
        no keywords overlap (e.g. "can't log in" matches "authentication troubleshooting").

        ```python
        # pip install sentence-transformers
        from sentence_transformers import SentenceTransformer, util

        model = SentenceTransformer("all-MiniLM-L6-v2")  # 384-dim, fast, free, local
        docs = [
            "How to reset your password",
            "Troubleshooting login and authentication issues",
            "Billing and subscription FAQ",
        ]
        doc_emb = model.encode(docs, normalize_embeddings=True)

        query = "I can't sign in to my account"
        q_emb = model.encode(query, normalize_embeddings=True)

        scores = util.cos_sim(q_emb, doc_emb)[0]
        best = scores.argmax().item()
        print("Best match:", docs[best])  # -> login/authentication article
        ```
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Token Counting (cost engineering)

        Token counts are **model-specific**. For Anthropic models, use the official count-tokens
        endpoint rather than `tiktoken` (which is OpenAI's tokenizer and undercounts Claude
        tokens):

        ```python
        # pip install anthropic
        import anthropic
        client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env
        resp = client.messages.count_tokens(
            model="claude-opus-4-8",
            messages=[{"role": "user", "content": "How many tokens is this sentence?"}],
        )
        print(resp.input_tokens)
        ```

        For OpenAI models, `tiktoken` is the correct tokenizer. The lesson: **match the tokenizer
        to the model.**
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Coding Exercise

        1. Using `all-MiniLM-L6-v2` (or the toy vectors if offline), embed these 5 sentences and
           build a 5×5 cosine-similarity matrix:
           `["I love pizza", "Pizza is my favorite food", "The stock market fell today",
             "Equities dropped sharply", "My cat is sleeping"]`
        2. Verify the two food sentences and the two finance sentences cluster together.
        3. Find, for the query "delicious Italian dinner," which of the 5 ranks highest.
        """
    )
    return


@app.cell
def __(cosine, np):
    # Offline-safe demo with deterministic pseudo-embeddings (replace with real model when online)
    rng = np.random.default_rng(1)
    # Simulate clusters: food (~), finance (~), other
    food = rng.normal(0, 0.02, 3) + np.array([1.0, 0.0, 0.0])
    food2 = rng.normal(0, 0.02, 3) + np.array([1.0, 0.0, 0.0])
    fin = rng.normal(0, 0.02, 3) + np.array([0.0, 1.0, 0.0])
    fin2 = rng.normal(0, 0.02, 3) + np.array([0.0, 1.0, 0.0])
    other = rng.normal(0, 0.02, 3) + np.array([0.0, 0.0, 1.0])

    print("food ~ food2 :", round(cosine(food, food2), 3))
    print("fin  ~ fin2  :", round(cosine(fin, fin2), 3))
    print("food ~ fin   :", round(cosine(food, fin), 3))
    return fin, fin2, food, food2, other, rng


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Assignment
        See `../assignments/week03_assignments.md` — Assignment 2.

        ## Interview Questions
        See `../../interview-prep/week03_genai_questions.md` — Section: Tokens & Embeddings.

        ## Industry Use Cases
        - Semantic search, recommendation, deduplication
        - Clustering support tickets / documents by topic
        - The retrieval half of every RAG system (Week 4)

        ## Common Mistakes
        - Comparing embeddings from two different models
        - Forgetting to normalize before cosine similarity
        - Using `tiktoken` to estimate Claude token counts

        ## Best Practices
        - Normalize embeddings; cache them; version the embedding model
        - Match the tokenizer to the model for cost estimates
        - Pick embedding dimensionality by recall/cost/latency trade-off

        ## Further Reading
        - sentence-transformers documentation
        - "Efficient Estimation of Word Representations" (word2vec, Mikolov et al.)
        - OpenAI & Anthropic embedding/token-counting docs
        """
    )
    return


if __name__ == "__main__":
    app.run()
