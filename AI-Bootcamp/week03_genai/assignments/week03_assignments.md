# Week 3 Assignments

Complete each assignment in a new Marimo notebook or `.py` script in this folder. Reference
solutions are in `../solutions/`. API-based assignments include an offline fallback so you can
complete the logic even without keys.

> **Secrets:** Never hardcode API keys. Use environment variables (`OPENAI_API_KEY`,
> `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`) and a `.env` file that is git-ignored.

---

## Assignment 1 — Transformers & Attention

1. Implement scaled dot-product attention in NumPy (Q, K, V → output + weights).
2. Add a causal mask and verify token *i* attends only to tokens ≤ *i*.
3. Explain in 3-4 sentences why the `1/√d_k` scaling factor matters.
4. Implement a 2-head version (split embedding dim, attend per head, concatenate).

---

## Assignment 2 — Tokens & Embeddings

1. Using `sentence-transformers` (`all-MiniLM-L6-v2`), embed 8 sentences spanning 3 topics.
2. Build the 8×8 cosine-similarity matrix and confirm same-topic pairs score highest.
3. For 3 query sentences, return the top-2 most similar of the 8.
4. Count the tokens of a 200-word paragraph for an Anthropic model (`count_tokens`) and an
   OpenAI model (`tiktoken`). Report the difference and explain why they differ.

---

## Assignment 3 — Vector Databases

1. Embed 20 short documents and build a FAISS `IndexFlatIP`.
2. Run 3 queries and return the top-3 results each.
3. Build an `IndexHNSWFlat` over the same data and compute recall@3 vs the exact index.
4. In Chroma, store the 20 docs with a `category` metadata field and run a query with a
   `where` filter. Confirm only the filtered category is returned.

---

## Assignment 4 — Prompt Engineering

1. Write a system prompt that classifies support tickets into `{billing, technical, account,
   other}`, returning one word.
2. Build a 10-example eval set and a function that computes classification accuracy.
3. Compare zero-shot vs 3-shot prompts on the eval set; report both accuracies.
4. Convert the classifier to return structured JSON (`{category, confidence}`) using a JSON
   schema, and verify every output parses.

---

## Assignment 5 — Tool / Function Calling

1. Define three tools: `calculator`, `get_weather` (mock), `get_time` (mock).
2. Implement the manual agentic loop (any provider) so the model can chain tools.
3. Add error handling: a tool that raises returns `is_error: true` and the agent recovers.
4. Ask a question that requires at least two tools and print the full message trajectory.

---

## Assignment 6 — MCP

1. Using `MiniMCPServer` (from notebook 06), register `add`, `subtract`, `multiply` tools and a
   `config://app` resource.
2. Write a client function that lists tools and invokes one by name with arguments.
3. In 5-6 sentences, explain how MCP differs from writing a one-off function-calling
   integration, and one security benefit of keeping credentials server-side.
4. (Stretch) Build a real FastMCP server (`pip install mcp`) with one tool and call it from the
   Anthropic tool runner.

---

## Assignment 7 — Multi-Agent Systems

1. Implement a research → write → review pipeline (offline stand-ins are fine).
2. Add a 4th fact-checker agent that flags notes lacking a citation.
3. Add an orchestrator that chooses sequential vs parallel fan-out based on the number of
   subtopics.
4. In 4-5 sentences, describe one task where multi-agent clearly beats a single agent, and one
   where it's unnecessary overhead.
