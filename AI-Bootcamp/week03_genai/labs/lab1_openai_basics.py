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
        # Lab 1: OpenAI API Basics

        **Goal:** Make your first chat-completion and function call with the OpenAI API.

        **Setup:**
        ```bash
        pip install openai
        export OPENAI_API_KEY="sk-..."   # never hardcode keys; use environment variables
        ```

        ## Tasks
        1. Send a basic chat completion.
        2. Use a system message to control behavior.
        3. Define a function (tool) and handle the tool call.
        4. Request structured JSON output.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 1-2. Chat completion with a system message

        ```python
        from openai import OpenAI
        client = OpenAI()  # reads OPENAI_API_KEY from env

        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a concise assistant. Answer in one sentence."},
                {"role": "user", "content": "What is retrieval-augmented generation?"},
            ],
        )
        print(resp.choices[0].message.content)
        ```
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 3. Function (tool) calling

        ```python
        tools = [{
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get current temperature for a city.",
                "parameters": {
                    "type": "object",
                    "properties": {"city": {"type": "string"}},
                    "required": ["city"],
                },
            },
        }]

        messages = [{"role": "user", "content": "Weather in Paris?"}]
        resp = client.chat.completions.create(model="gpt-4o", messages=messages, tools=tools)

        msg = resp.choices[0].message
        if msg.tool_calls:
            import json
            call = msg.tool_calls[0]
            args = json.loads(call.function.arguments)
            result = {"Paris": "18C"}.get(args["city"], "unknown")   # your function
            messages.append(msg)
            messages.append({"role": "tool", "tool_call_id": call.id, "content": result})
            final = client.chat.completions.create(model="gpt-4o", messages=messages, tools=tools)
            print(final.choices[0].message.content)
        ```
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 4. Structured JSON output

        ```python
        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Extract: Jane, jane@x.com, Enterprise plan."}],
            response_format={"type": "json_schema", "json_schema": {
                "name": "contact",
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "email": {"type": "string"},
                        "plan": {"type": "string"},
                    },
                    "required": ["name", "email", "plan"],
                    "additionalProperties": False,
                },
            }},
        )
        import json
        print(json.loads(resp.choices[0].message.content))
        ```

        ## Deliverable
        A script `openai_demo.py` that runs all four tasks and prints results.

        ## Stretch Goal
        Add retry-with-backoff around the API call and handle `RateLimitError`.
        """
    )
    return


if __name__ == "__main__":
    app.run()
