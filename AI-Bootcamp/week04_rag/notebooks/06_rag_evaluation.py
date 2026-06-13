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
        # 06. RAG Evaluation

        ## Theory

        **Level 1 (10-year-old):** How do you know your open-book helper is doing well? You check
        two things: did it find the *right pages*, and did it give the *right answer* using them?

        **Level 2 (College Student):** Evaluate RAG in two layers. **Retrieval metrics:**
        recall@k (did the relevant chunk appear in the top-k?), precision@k, and MRR/nDCG
        (ranking quality). **Generation metrics:** **faithfulness** (is the answer supported by
        the retrieved context, i.e. not hallucinated?), **answer relevance** (does it address the
        question?), and **context relevance** (was the retrieved context on-topic?). Frameworks
        like RAGAS automate several of these using an LLM as judge.

        **Level 3 (Industry Professional):** "It looked good once" is not evaluation. Build a
        labeled eval set (questions + relevant chunk ids + reference answers), measure retrieval
        and generation separately (a great generator can't fix bad retrieval), and run evals in CI
        so prompt/chunking/model changes are measured, not guessed. LLM-as-judge scales but must
        be calibrated against human labels. Track faithfulness especially — it's the metric that
        protects against confident hallucination.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Visual Explanation

        ```
        Eval set: [(question, relevant_chunk_ids, reference_answer), ...]

        RETRIEVAL                           GENERATION
        ─────────                           ──────────
        recall@k   = |retrieved ∩ relevant| faithfulness    = claims supported by context?
                     / |relevant|           answer relevance = addresses the question?
        precision@k= |retrieved ∩ relevant| context relevance= retrieved context on-topic?
                     / k
        MRR        = 1 / rank of first hit  (LLM-as-judge can score these)

        Rule: evaluate retrieval and generation SEPARATELY.
        ```
        """
    )
    return


@app.cell
def __():
    # Simple Example: retrieval metrics in pure Python
    def recall_at_k(retrieved, relevant, k):
        top = set(retrieved[:k])
        rel = set(relevant)
        return len(top & rel) / len(rel) if rel else 0.0

    def precision_at_k(retrieved, relevant, k):
        top = retrieved[:k]
        rel = set(relevant)
        return sum(1 for d in top if d in rel) / k

    def mrr(retrieved, relevant):
        rel = set(relevant)
        for rank, d in enumerate(retrieved, start=1):
            if d in rel:
                return 1.0 / rank
        return 0.0

    retrieved = ["c3", "c1", "c7", "c2"]      # ranked retrieval result
    relevant = ["c1", "c2"]                    # ground-truth relevant chunks

    print("recall@2   :", recall_at_k(retrieved, relevant, 2))
    print("precision@2:", precision_at_k(retrieved, relevant, 2))
    print("recall@4   :", recall_at_k(retrieved, relevant, 4))
    print("MRR        :", round(mrr(retrieved, relevant), 3))
    return mrr, precision_at_k, recall_at_k, relevant, retrieved


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Faithfulness via LLM-as-judge (concept + code)

        Faithfulness asks: *is every claim in the answer supported by the retrieved context?*

        ```python
        import anthropic
        client = anthropic.Anthropic()

        def faithfulness(answer, context):
            prompt = (
                "Given the CONTEXT and an ANSWER, reply with a single number 0-1: "
                "the fraction of the answer's claims that are directly supported by the context.\n\n"
                f"CONTEXT:\n{context}\n\nANSWER:\n{answer}\n\nScore:"
            )
            r = client.messages.create(
                model="claude-opus-4-8", max_tokens=8,
                messages=[{"role": "user", "content": prompt}],
            )
            return float(next(b.text for b in r.content if b.type == "text").strip())
        ```

        Production tip: frameworks like **RAGAS** package faithfulness, answer relevance, and
        context relevance/precision out of the box. Always calibrate LLM-judge scores against a
        sample of human labels.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Real-World Example

        A team ships a chunking change that "felt better." Running the eval set reveals recall@5
        rose from 0.72 → 0.81 but faithfulness dropped from 0.95 → 0.88 (larger chunks pulled in
        off-topic text the model then over-used). The metrics turn a vibe into a decision.

        ## Coding Exercise

        1. Build a 10-question eval set over the Week 4 toy corpus with ground-truth chunk ids.
        2. Compute mean recall@3, precision@3, and MRR for your retriever.
        3. Implement a simple keyword-overlap "faithfulness" proxy (fraction of answer words
           present in the retrieved context) and flag answers below 0.5.
        4. Change the chunk size and re-run — report how each metric moves.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Assignment
        See `../assignments/week04_assignments.md` — Assignment 6.

        ## Interview Questions
        See `../../interview-prep/week04_rag_questions.md` — Section: RAG Evaluation.

        ## Industry Use Cases
        - CI gates on RAG quality before deploy
        - A/B testing chunking/embedding/model changes
        - Monitoring faithfulness to catch hallucination regressions

        ## Common Mistakes
        - Only judging final answers, never retrieval
        - No labeled eval set ("looked good once")
        - Trusting LLM-judge scores without human calibration

        ## Best Practices
        - Evaluate retrieval and generation separately
        - Track faithfulness to guard against hallucination
        - Run evals in CI; calibrate LLM-as-judge against human labels

        ## Further Reading
        - RAGAS documentation
        - "Evaluating Retrieval-Augmented Generation" literature
        - LangSmith / Phoenix / Arize for tracing + evals
        """
    )
    return


if __name__ == "__main__":
    app.run()
