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
        # 05. Tool Calling & Function Calling

        ## Theory

        **Level 1 (10-year-old):** An AI by itself can only talk. But if you give it buttons —
        "look up the weather," "do math," "search the web" — it can press the right button when
        it needs to, then use the answer to keep helping you.

        **Level 2 (College Student):** Tool calling (a.k.a. function calling) lets an LLM request
        that your code run a function. You describe each tool with a name, description, and a JSON
        schema for its inputs. The model returns a structured **tool-use request**; your code
        executes the function and returns the result; the model continues with that result. This
        is how LLMs access live data, perform actions, and ground their answers.

        **Level 3 (Industry Professional):** Tool calling is the foundation of agents. Design
        principles: clear, prescriptive tool descriptions ("call this when..."), small focused
        schemas, robust error handling (return errors to the model so it can recover), and
        gating side-effecting tools (sending email, writing to a DB) behind validation or
        human approval. SDKs offer "tool runners" that automate the request→execute→continue
        loop, or you can write the loop manually for fine-grained control (logging, approvals).
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Visual Explanation

        ```
        ┌────────┐  1. prompt + tool schemas   ┌───────┐
        │  Your  │ ──────────────────────────► │  LLM  │
        │  code  │                              └───┬───┘
        │        │  2. "call get_weather(Paris)"   │  stop_reason = tool_use
        │        │ ◄───────────────────────────────┘
        │        │  3. execute get_weather("Paris") → "18°C"
        │        │ ──────────────────────────► ┌───────┐
        │        │  4. tool_result: "18°C"      │  LLM  │
        │        │ ◄─────────────────────────── └───────┘
        └────────┘  5. final answer: "It's 18°C in Paris."
        ```
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Simple Example: define a tool and run the loop (Anthropic SDK)

        ```python
        # pip install anthropic
        import anthropic

        client = anthropic.Anthropic()

        tools = [{
            "name": "get_weather",
            "description": "Get the current temperature for a city. Call this whenever the user asks about weather.",
            "input_schema": {
                "type": "object",
                "properties": {"city": {"type": "string", "description": "City name, e.g. Paris"}},
                "required": ["city"],
            },
        }]

        def get_weather(city: str) -> str:
            fake = {"Paris": "18°C", "Tokyo": "24°C"}      # stand-in for a real weather API
            return fake.get(city, "unknown")

        messages = [{"role": "user", "content": "What's the weather in Paris?"}]

        # Manual agentic loop: keep going until the model stops calling tools
        while True:
            resp = client.messages.create(
                model="claude-opus-4-8", max_tokens=1024, tools=tools, messages=messages,
            )
            if resp.stop_reason != "tool_use":
                print(next(b.text for b in resp.content if b.type == "text"))
                break

            messages.append({"role": "assistant", "content": resp.content})
            results = []
            for block in resp.content:
                if block.type == "tool_use":
                    out = get_weather(**block.input)            # execute your function
                    results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,                 # must match the request id
                        "content": out,
                    })
            messages.append({"role": "user", "content": results})
        ```
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Tool Runner (less boilerplate)

        The Anthropic Python SDK provides a beta tool runner that handles the loop for you:

        ```python
        from anthropic import beta_tool, Anthropic

        client = Anthropic()

        @beta_tool
        def get_weather(city: str) -> str:
            \"\"\"Get the current temperature for a city.

            Args:
                city: City name, e.g. Paris.
            \"\"\"
            return {"Paris": "18°C", "Tokyo": "24°C"}.get(city, "unknown")

        runner = client.beta.messages.tool_runner(
            model="claude-opus-4-8",
            max_tokens=1024,
            tools=[get_weather],
            messages=[{"role": "user", "content": "Weather in Tokyo?"}],
        )
        for message in runner:        # iterates until the model is done
            print(message)
        ```
        """
    )
    return


@app.cell
def __():
    # Offline-safe simulation of the tool-calling protocol (no API key needed)
    def get_weather(city: str) -> str:
        return {"Paris": "18°C", "Tokyo": "24°C"}.get(city, "unknown")

    def simulate_round(model_decision):
        """model_decision: dict describing what the 'model' wants to do this turn."""
        if model_decision["type"] == "tool_use":
            name = model_decision["name"]
            args = model_decision["input"]
            if name == "get_weather":
                return {"type": "tool_result", "content": get_weather(**args)}
        return {"type": "final", "content": "done"}

    # Pretend the model asked to call get_weather("Paris")
    result = simulate_round({"type": "tool_use", "name": "get_weather", "input": {"city": "Paris"}})
    print("Tool returned:", result)
    return get_weather, result, simulate_round


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Multi-Provider Note

        The concept is identical across providers; only the SDK shapes differ:
        - **OpenAI:** `tools=[{"type":"function","function":{...}}]`, response `tool_calls`
        - **Anthropic:** `tools=[{...}]`, response blocks with `type == "tool_use"`
        - **Gemini:** `tools=[Tool(function_declarations=[...])]`, `function_call` parts

        ## Coding Exercise

        1. Add a second tool `calculator(expression: str)` and a third `get_time(timezone: str)`.
        2. Implement the manual loop (or use the tool runner) so the model can chain them, e.g.
           "What's 15% of the temperature in Tokyo right now?"
        3. Add error handling: if a tool raises, return `{"type":"tool_result", "is_error": True,
           "content": "..."}` so the model can recover.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Assignment
        See `../assignments/week03_assignments.md` — Assignment 5.

        ## Interview Questions
        See `../../interview-prep/week03_genai_questions.md` — Section: Tool/Function Calling.

        ## Industry Use Cases
        - Customer-support copilots that look up orders/accounts
        - "Ask your data" assistants querying internal APIs/databases
        - Booking, scheduling, and workflow-automation agents

        ## Common Mistakes
        - Vague tool descriptions → model calls the wrong tool or never calls it
        - Not returning tool errors to the model (it can't recover)
        - Forgetting to match `tool_use_id` in the result
        - Auto-executing destructive tools with no validation/approval

        ## Best Practices
        - Write prescriptive "call this when..." descriptions; keep schemas small
        - Return informative errors with `is_error: true`
        - Gate side-effecting tools behind validation or human approval

        ## Further Reading
        - Anthropic tool use documentation
        - OpenAI function calling guide; Gemini function calling guide
        - "Toolformer" (Schick et al., 2023)
        """
    )
    return


if __name__ == "__main__":
    app.run()
