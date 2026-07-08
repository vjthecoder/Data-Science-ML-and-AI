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
        # 07. Multi-Agent Systems

        ## Theory

        **Level 1 (10-year-old):** Instead of one helper doing everything, you have a team: one
        finds facts, one writes, one checks the work. A "manager" hands out jobs and puts the
        pieces together — like a group project that actually works.

        **Level 2 (College Student):** A multi-agent system composes several LLM "agents," each
        with its own role, tools, and prompt, into a workflow. Common patterns:
        **orchestrator-worker** (a coordinator delegates subtasks), **pipeline** (researcher →
        writer → reviewer), and **parallel fan-out** (many workers, then aggregate). Agents
        communicate by passing messages/results. Each agent is still just an LLM with tools; the
        system is the orchestration around them.

        **Level 3 (Industry Professional):** Multi-agent designs help when a task is large,
        parallelizable, or benefits from separation of concerns (e.g. a fresh-context reviewer
        catching the writer's mistakes). Trade-offs: more LLM calls (cost/latency), harder
        debugging, and error propagation. Best practices: give each agent a narrow role and clear
        success criteria; prefer asynchronous delegation for long-running sub-agents; log full
        traces; and **don't reach for multi-agent when a single well-prompted agent (or a simple
        workflow) suffices.** Managed-agent platforms can run the orchestration server-side.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Visual Explanation

        ```
        Orchestrator–Worker:                 Pipeline:
              ┌───────────────┐              Researcher → Writer → Reviewer → ✔
              │ Orchestrator  │
              └──┬────┬────┬──┘              Parallel fan-out:
                 ▼    ▼    ▼                       ┌─► Worker A ─┐
              Worker Worker Worker            Task ┼─► Worker B ─┼─► Aggregator
                 │    │    │                       └─► Worker C ─┘
                 └────┴────┴──► aggregate
        ```
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Real-World Example: researcher → writer → reviewer (Anthropic SDK)

        ```python
        import anthropic
        client = anthropic.Anthropic()

        def agent(system, user, max_tokens=1024):
            resp = client.messages.create(
                model="claude-opus-4-8", max_tokens=max_tokens,
                system=system, messages=[{"role": "user", "content": user}],
            )
            return next(b.text for b in resp.content if b.type == "text")

        topic = "the benefits of retrieval-augmented generation"

        research = agent(
            "You are a research assistant. List 5 concise, factual bullet points.",
            f"Research: {topic}",
        )
        draft = agent(
            "You are a technical writer. Write a tight 150-word paragraph from the notes.",
            f"Notes:\n{research}",
        )
        review = agent(
            "You are an editor. Improve clarity and flag any unsupported claims. Return the final text.",
            f"Draft:\n{draft}",
        )
        print(review)
        ```

        Each agent has a **distinct role and system prompt**; outputs flow down the pipeline.
        """
    )
    return


@app.cell
def __():
    # Offline-safe simulation of a 3-agent pipeline (deterministic stand-ins for LLM calls)
    def researcher(topic: str) -> list[str]:
        return [f"Fact {i} about {topic}" for i in range(1, 4)]

    def writer(notes: list[str]) -> str:
        return "Summary: " + "; ".join(notes)

    def reviewer(draft: str) -> str:
        return draft.replace("Summary:", "Final (reviewed):")

    notes = researcher("RAG")
    draft = writer(notes)
    final = reviewer(draft)
    print("Notes :", notes)
    print("Draft :", draft)
    print("Final :", final)
    return draft, final, notes, researcher, reviewer, writer


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Orchestrator–Worker (parallel fan-out) sketch

        ```python
        import concurrent.futures as cf

        def worker(subtopic):
            return agent("You are a domain expert. Answer in 2 sentences.", subtopic)

        subtopics = ["chunking", "embeddings", "reranking", "evaluation"]
        with cf.ThreadPoolExecutor() as pool:
            results = list(pool.map(worker, subtopics))

        summary = agent(
            "You are an editor. Merge these notes into one coherent overview.",
            "\n\n".join(results),
        )
        ```

        Parallel fan-out cuts wall-clock latency when subtasks are independent.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Coding Exercise

        1. Implement the offline 3-agent pipeline, then add a 4th "fact-checker" agent that
           flags any note containing the word "Fact 2" as needing a citation.
        2. Convert the pipeline to an orchestrator that decides — based on the topic length —
           whether to run sequentially or fan out to parallel workers.
        3. (Stretch, needs API key) Replace the stand-ins with real `agent()` calls and compare a
           single-agent answer vs the 3-agent pipeline on the same topic. Which is better, and is
           the extra cost worth it?
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Assignment
        See `../assignments/week03_assignments.md` — Assignment 7.

        ## Interview Questions
        See `../../interview-prep/week03_genai_questions.md` — Section: Multi-Agent Systems.

        ## Industry Use Cases
        - Research → draft → review content pipelines
        - Parallel document processing with an aggregation step
        - Coding agents that delegate to sub-agents for independent files

        ## Common Mistakes
        - Using multi-agent when one good agent would do (needless cost/latency)
        - No clear role/success criteria per agent → agents drift
        - Ignoring error propagation between stages

        ## Best Practices
        - Narrow role + explicit success criteria per agent
        - Prefer asynchronous delegation for long-running sub-agents; log full traces
        - Start simple (single agent / workflow); add agents only when justified

        ## Further Reading
        - Anthropic "Building effective agents" and multi-agent research
        - Orchestrator-worker and reflection agent patterns
        - Managed agent platforms (server-side orchestration)
        """
    )
    return


if __name__ == "__main__":
    app.run()
