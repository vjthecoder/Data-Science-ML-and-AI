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
        # Lab 5: Build a Simple Tool-Using Agent

        **Goal:** Build an agent that can use a calculator and a (mock) web-search tool to answer
        multi-step questions, using the Anthropic SDK's manual agentic loop.

        **Setup:**
        ```bash
        pip install anthropic
        export ANTHROPIC_API_KEY="sk-ant-..."
        ```

        ## What you'll build
        An agent that, given "What is 15% of the population of France (approx)?", will:
        1. Call `web_search("population of France")` → ~68,000,000
        2. Call `calculator("68000000 * 0.15")` → 10,200,000
        3. Return a final natural-language answer.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## The agent (Anthropic manual loop)

        ```python
        import anthropic, json

        client = anthropic.Anthropic()

        tools = [
            {
                "name": "calculator",
                "description": "Evaluate a basic arithmetic expression. Use for any math.",
                "input_schema": {
                    "type": "object",
                    "properties": {"expression": {"type": "string"}},
                    "required": ["expression"],
                },
            },
            {
                "name": "web_search",
                "description": "Look up a fact on the web. Use for current or factual data.",
                "input_schema": {
                    "type": "object",
                    "properties": {"query": {"type": "string"}},
                    "required": ["query"],
                },
            },
        ]

        def calculator(expression: str) -> str:
            try:
                # NOTE: eval is unsafe in production; use a real parser. Restricted here for demo.
                return str(eval(expression, {"__builtins__": {}}, {}))
            except Exception as e:
                return f"error: {e}"

        def web_search(query: str) -> str:
            facts = {"population of France": "approximately 68,000,000"}
            return facts.get(query, "no result found")

        TOOL_FUNCS = {"calculator": calculator, "web_search": web_search}

        def run_agent(question: str, max_steps: int = 6) -> str:
            messages = [{"role": "user", "content": question}]
            for _ in range(max_steps):
                resp = client.messages.create(
                    model="claude-opus-4-8", max_tokens=1024, tools=tools, messages=messages,
                )
                if resp.stop_reason != "tool_use":
                    return next(b.text for b in resp.content if b.type == "text")

                messages.append({"role": "assistant", "content": resp.content})
                results = []
                for b in resp.content:
                    if b.type == "tool_use":
                        fn = TOOL_FUNCS.get(b.name)
                        try:
                            out = fn(**b.input) if fn else f"unknown tool {b.name}"
                            results.append({"type": "tool_result", "tool_use_id": b.id, "content": out})
                        except Exception as e:
                            results.append({"type": "tool_result", "tool_use_id": b.id,
                                            "content": f"error: {e}", "is_error": True})
                messages.append({"role": "user", "content": results})
            return "Stopped: reached max steps."

        print(run_agent("What is 15% of the population of France?"))
        ```
        """
    )
    return


@app.cell
def __():
    # Offline-safe simulation of the agent loop (no API key required)
    def calculator(expression: str) -> str:
        try:
            return str(eval(expression, {"__builtins__": {}}, {}))
        except Exception as e:
            return f"error: {e}"

    def web_search(query: str) -> str:
        facts = {"population of France": "68000000"}
        return facts.get(query, "no result found")

    # Hardcoded "plan" the model would have produced, to demonstrate the data flow:
    pop = web_search("population of France")          # step 1
    answer = calculator(f"{pop} * 0.15")              # step 2
    print(f"web_search -> {pop}")
    print(f"calculator -> {answer}")
    print(f"Final answer: ~{int(float(answer)):,} people")
    return answer, calculator, pop, web_search


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Coding Exercise

        1. Add a `get_time(timezone)` tool and ask a question that requires all three tools.
        2. Add a `max_steps` guard (already shown) and a per-step log so you can see the agent's
           trajectory.
        3. Make `calculator` safe: replace `eval` with a real expression parser (e.g. the `ast`
           module restricted to arithmetic nodes).

        ## Deliverable
        A script `agent.py` implementing `run_agent(question)` with at least 3 tools, error
        handling, a step limit, and trajectory logging.

        ## Stretch Goal
        Give the agent a memory: persist facts it learns to a JSON file and load them on the next
        run so repeated questions skip the search.

        ## Best Practices Recap
        - Always cap iterations (`max_steps`) to prevent infinite loops
        - Return tool errors to the model (`is_error: true`) so it can recover
        - Never use raw `eval` on untrusted input in production
        - Log the full trajectory for debugging
        """
    )
    return


if __name__ == "__main__":
    app.run()
