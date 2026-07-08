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
        # Lab 2: Anthropic (Claude) API Basics

        **Goal:** Make your first message, use tools, stream output, and request structured JSON
        with the Anthropic Python SDK.

        **Setup:**
        ```bash
        pip install anthropic
        export ANTHROPIC_API_KEY="sk-ant-..."   # never hardcode; use environment variables
        ```

        Model used throughout: `claude-opus-4-8` (Anthropic's capable default). For the most
        advanced reasoning, `claude-fable-5` is Anthropic's most capable model.

        ## Tasks
        1. Basic message + system prompt.
        2. Tool use (manual loop).
        3. Streaming output.
        4. Structured JSON via `output_config.format`.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 1. Basic message with a system prompt

        ```python
        import anthropic
        client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

        resp = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=256,
            system="You are a concise assistant. Answer in one sentence.",
            messages=[{"role": "user", "content": "What is retrieval-augmented generation?"}],
        )
        # response.content is a list of blocks; pick the text block(s)
        print(next(b.text for b in resp.content if b.type == "text"))
        ```
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 2. Tool use (manual agentic loop)

        ```python
        tools = [{
            "name": "get_weather",
            "description": "Get current temperature for a city. Call when the user asks about weather.",
            "input_schema": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"],
            },
        }]

        def get_weather(city: str) -> str:
            return {"Paris": "18C", "Tokyo": "24C"}.get(city, "unknown")

        messages = [{"role": "user", "content": "What's the weather in Paris?"}]
        while True:
            resp = client.messages.create(
                model="claude-opus-4-8", max_tokens=1024, tools=tools, messages=messages,
            )
            if resp.stop_reason != "tool_use":
                print(next(b.text for b in resp.content if b.type == "text"))
                break
            messages.append({"role": "assistant", "content": resp.content})
            results = []
            for b in resp.content:
                if b.type == "tool_use":
                    results.append({
                        "type": "tool_result",
                        "tool_use_id": b.id,
                        "content": get_weather(**b.input),
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
        ## 3. Streaming output

        ```python
        with client.messages.stream(
            model="claude-opus-4-8",
            max_tokens=512,
            messages=[{"role": "user", "content": "Write a haiku about vectors."}],
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
            final = stream.get_final_message()
            print("\n\nTokens:", final.usage.output_tokens)
        ```

        ## 4. Structured JSON output

        ```python
        import json
        resp = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=512,
            messages=[{"role": "user", "content": "Extract: Jane, jane@x.com, Enterprise plan, wants a demo."}],
            output_config={"format": {"type": "json_schema", "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "plan": {"type": "string"},
                    "demo_requested": {"type": "boolean"},
                },
                "required": ["name", "email", "plan", "demo_requested"],
                "additionalProperties": False,
            }}},
        )
        print(json.loads(next(b.text for b in resp.content if b.type == "text")))
        ```

        ## Deliverable
        A script `anthropic_demo.py` running all four tasks.

        ## Stretch Goal
        Use `client.messages.count_tokens(...)` to estimate input cost before sending, and enable
        `thinking={"type": "adaptive"}` on a reasoning question.
        """
    )
    return


if __name__ == "__main__":
    app.run()
