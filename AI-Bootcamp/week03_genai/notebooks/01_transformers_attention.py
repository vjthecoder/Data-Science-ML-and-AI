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
        # 01. Transformer Architecture & Attention

        ## Theory

        **Level 1 (10-year-old):** Imagine reading a sentence and, for each word, deciding which
        OTHER words matter most to understand it. In "The cat sat because it was tired," to know
        what "it" means, you look back at "cat." Attention is the model doing exactly that —
        looking at every word and weighing how much each one matters.

        **Level 2 (College Student):** The Transformer (Vaswani et al., 2017) replaced recurrence
        with **self-attention**. Each token is projected into Query (Q), Key (K), and Value (V)
        vectors. Attention scores are computed as the scaled dot-product of queries and keys,
        softmaxed into weights, then used to take a weighted sum of the values. Multiple
        "heads" attend to different relationships in parallel. Stacked attention + feed-forward
        layers, plus positional encodings, make up the architecture behind GPT, Claude, and
        Gemini.

        **Level 3 (Industry Professional):** Transformers scale extraordinarily well with data
        and compute, which is why they underpin all modern LLMs. Decoder-only models (GPT,
        Claude, Llama) use **causal (masked) self-attention** so a token can only attend to
        previous tokens — enabling autoregressive generation. Key engineering concerns:
        attention is O(n²) in sequence length (motivating FlashAttention, sliding-window, and
        KV-cache optimizations), and context-window limits stem directly from this cost.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Visual Explanation

        ```
        Scaled Dot-Product Attention:

            Attention(Q, K, V) = softmax( Q·Kᵀ / √d_k ) · V

        Token "it"  --Q-->  ┐
        Token "cat" --K-->  ├─ score(it, cat) = high  ─┐
        Token "sat" --K-->  ├─ score(it, sat) = low    ├─ softmax → weights → weighted sum of V
        Token "was" --K-->  ┘                           ┘

        Multi-Head: run this h times in parallel with different learned projections,
        then concatenate. Each head can capture a different relationship (syntax,
        coreference, position, ...).
        ```

        See `../../diagrams/week03_genai/README.md` for the full block diagram.
        """
    )
    return


@app.cell
def __():
    # Simple Example: scaled dot-product attention from scratch in NumPy
    import numpy as np

    def softmax(x, axis=-1):
        e = np.exp(x - x.max(axis=axis, keepdims=True))
        return e / e.sum(axis=axis, keepdims=True)

    def attention(Q, K, V):
        d_k = Q.shape[-1]
        scores = Q @ K.T / np.sqrt(d_k)
        weights = softmax(scores)
        return weights @ V, weights

    # 3 tokens, embedding dim 4 (toy values)
    rng = np.random.default_rng(0)
    Q = rng.normal(size=(3, 4))
    K = rng.normal(size=(3, 4))
    V = rng.normal(size=(3, 4))

    out, weights = attention(Q, K, V)
    print("Attention weights (each row sums to 1):\n", weights.round(3))
    print("\nOutput shape:", out.shape)
    return K, Q, V, attention, np, out, rng, softmax, weights


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Real-World Example

        When Claude reads "The contract terminates on the date specified in Section 4," and you
        ask "When does it terminate?", self-attention lets the model link "it" → "contract" and
        "date" → "Section 4," then retrieve the relevant span. The same mechanism powers code
        completion (linking a variable use to its definition) and translation (aligning words
        across languages).
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Coding Exercise

        1. Extend the `attention` function above to apply a **causal mask** (a token may only
           attend to itself and earlier tokens). Hint: set `scores[i, j] = -inf` for `j > i`
           before softmax.
        2. Verify that for a causal mask, the first token's attention weights are `[1, 0, 0]`.
        3. Implement a simple 2-head version: split the embedding dim in half, run attention on
           each half, concatenate the outputs.
        """
    )
    return


@app.cell
def __(K, Q, V, np, softmax):
    def causal_attention(Q, K, V):
        d_k = Q.shape[-1]
        scores = Q @ K.T / np.sqrt(d_k)
        n = scores.shape[0]
        mask = np.triu(np.ones((n, n)), k=1).astype(bool)  # upper triangle = future
        scores[mask] = -np.inf
        weights = softmax(scores)
        return weights @ V, weights

    _, cw = causal_attention(Q, K, V)
    print("Causal weights (lower-triangular):\n", cw.round(3))
    print("First token attends only to itself:", cw[0].round(3))
    return (causal_attention,)


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Assignment
        See `../assignments/week03_assignments.md` — Assignment 1.

        ## Interview Questions
        See `../../interview-prep/week03_genai_questions.md` — Section: Transformers & Attention.

        ## Industry Use Cases
        - Every modern LLM (GPT, Claude, Gemini, Llama) is a Transformer
        - Vision Transformers (ViT) apply the same attention to image patches
        - Long-context optimizations (FlashAttention, KV-cache) are core to serving LLMs cheaply

        ## Common Mistakes
        - Forgetting the `1/√d_k` scaling (causes vanishing gradients via saturated softmax)
        - Confusing encoder (bidirectional) vs decoder (causal) attention
        - Assuming attention weights are "explanations" — they're correlations, not proofs

        ## Best Practices
        - Use established libraries (PyTorch `scaled_dot_product_attention`) in production
        - Understand context-window cost is quadratic when designing prompts/RAG
        - Profile attention memory before scaling sequence length

        ## Further Reading
        - "Attention Is All You Need" (Vaswani et al., 2017)
        - Jay Alammar, "The Illustrated Transformer"
        - Andrej Karpathy, "Let's build GPT" (nanoGPT)
        """
    )
    return


if __name__ == "__main__":
    app.run()
