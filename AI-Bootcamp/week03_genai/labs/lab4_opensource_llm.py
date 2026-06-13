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
        # Lab 4: Open-Source LLMs (Hugging Face Transformers)

        **Goal:** Run an open-source model locally — no API key, full control, free — and embed
        text with an open-source embedding model.

        **Setup:**
        ```bash
        pip install transformers torch sentence-transformers
        ```

        ## Why open-source?
        - Privacy (data never leaves your machine)
        - Cost (no per-token charges)
        - Control (fine-tune, run offline, pin versions)
        Trade-off: you manage the compute, and small local models are less capable than frontier
        hosted models like Claude or GPT.

        ## Tasks
        1. Text generation with a small instruct model.
        2. Use the chat template correctly.
        3. Embeddings with `sentence-transformers`.
        4. Compare a local model's answer to a hosted model's answer.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 1-2. Text generation with a chat template

        ```python
        from transformers import pipeline

        # A small instruct model that runs on CPU/modest GPU. Swap for any HF model you have access to.
        pipe = pipeline("text-generation", model="Qwen/Qwen2.5-0.5B-Instruct")

        messages = [
            {"role": "system", "content": "You are a concise assistant."},
            {"role": "user", "content": "What is retrieval-augmented generation?"},
        ]
        out = pipe(messages, max_new_tokens=128)
        print(out[0]["generated_text"][-1]["content"])
        ```

        Using the model's **chat template** (applied automatically when you pass `messages`) is
        important — raw string prompts without the template produce much worse results.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 3. Embeddings with sentence-transformers

        ```python
        from sentence_transformers import SentenceTransformer, util

        model = SentenceTransformer("all-MiniLM-L6-v2")   # 384-dim, fast, local, free
        docs = ["reset your password", "billing FAQ", "fix login errors"]
        doc_emb = model.encode(docs, normalize_embeddings=True)

        q_emb = model.encode("I can't sign in", normalize_embeddings=True)
        scores = util.cos_sim(q_emb, doc_emb)[0]
        print("Best match:", docs[scores.argmax().item()])
        ```
        """
    )
    return


@app.cell
def __():
    # Offline-safe demo: a tiny rule-based "model" so the notebook runs without downloads
    def tiny_local_llm(prompt: str) -> str:
        prompt_l = prompt.lower()
        if "rag" in prompt_l or "retrieval" in prompt_l:
            return ("Retrieval-augmented generation retrieves relevant documents and feeds them "
                    "to an LLM so its answer is grounded in your data.")
        return "I'm a tiny offline stand-in. Install transformers to run a real model."

    print(tiny_local_llm("Explain RAG"))
    return (tiny_local_llm,)


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 4. Compare local vs hosted

        Run the same question through your local model and a hosted model (Claude/GPT/Gemini from
        Labs 1-3). Compare on:
        - **Quality** — is the answer correct and complete?
        - **Latency** — local on CPU can be slow
        - **Cost** — local is free per token; hosted charges per token
        - **Privacy** — local keeps data on your machine

        ## Deliverable
        A script `opensource_demo.py` that generates text and computes embeddings locally, plus a
        short markdown table comparing local vs hosted on the four dimensions above.

        ## Stretch Goal
        Quantize the model (e.g. load in 4-bit with `bitsandbytes`) and measure the
        memory/latency reduction.
        """
    )
    return


if __name__ == "__main__":
    app.run()
