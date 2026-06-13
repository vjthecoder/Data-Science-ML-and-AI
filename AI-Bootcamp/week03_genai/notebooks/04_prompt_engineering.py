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
        # 04. Prompt Engineering

        ## Theory

        **Level 1 (10-year-old):** Talking to an AI is like giving instructions to a very smart
        but very literal helper. The clearer and more specific you are — and the more examples
        you show — the better it does the job.

        **Level 2 (College Student):** Prompt engineering is the practice of structuring inputs to
        get reliable outputs. Core techniques: **zero-shot** (just ask), **few-shot** (show
        examples), **chain-of-thought** (ask the model to reason step by step), **role/system
        prompts** (set behavior and constraints), and **output formatting** (request JSON, give a
        schema). Good prompts specify role, task, constraints, and output format explicitly.

        **Level 3 (Industry Professional):** In production, prompts are versioned artifacts tuned
        against **evaluation sets** — write prompt → run on a test set → measure → iterate. Use
        structured outputs (JSON schema / tool calling) instead of parsing free text. Note that
        modern models (Claude Opus 4.x / Fable 5) follow instructions very literally, so overly
        aggressive language ("CRITICAL: YOU MUST...") can cause over-triggering — write clear,
        calm instructions. For Anthropic models, put stable instructions in the `system` prompt
        and leverage prompt caching for large fixed context.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Visual Explanation

        ```
        A well-structured prompt:
        ┌─────────────────────────────────────────────┐
        │ SYSTEM: role, persona, constraints, format    │  ← stable, cacheable
        ├─────────────────────────────────────────────┤
        │ FEW-SHOT: example 1 (input → output)          │
        │           example 2 (input → output)          │
        ├─────────────────────────────────────────────┤
        │ USER: the actual task + any context           │  ← varies per request
        └─────────────────────────────────────────────┘

        Eval-driven loop:  write prompt → run on test set → measure → iterate
        ```
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Simple Example: zero-shot vs few-shot (Anthropic SDK)

        ```python
        # pip install anthropic   (set ANTHROPIC_API_KEY in your environment)
        import anthropic
        client = anthropic.Anthropic()

        # Zero-shot
        resp = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=64,
            system="You are a sentiment classifier. Reply with exactly one word: positive, negative, or neutral.",
            messages=[{"role": "user", "content": "The delivery was late but support fixed it quickly."}],
        )
        print(next(b.text for b in resp.content if b.type == "text"))

        # Few-shot: show examples to lock in the format
        resp = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=64,
            system="Classify sentiment as positive, negative, or neutral. Reply with one word.",
            messages=[
                {"role": "user", "content": "I love this!"},
                {"role": "assistant", "content": "positive"},
                {"role": "user", "content": "It broke after a day."},
                {"role": "assistant", "content": "negative"},
                {"role": "user", "content": "The delivery was late but support fixed it quickly."},
            ],
        )
        print(next(b.text for b in resp.content if b.type == "text"))
        ```
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Real-World Example: structured output with a JSON schema

        Free-text parsing is brittle. Constrain the model to a schema so the output is always
        valid JSON your code can consume.

        ```python
        import anthropic
        client = anthropic.Anthropic()

        resp = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=512,
            messages=[{"role": "user", "content":
                "Extract contact info: Jane Doe, jane@acme.com, wants the Enterprise plan, needs a demo."}],
            output_config={"format": {"type": "json_schema", "schema": {
                "type": "object",
                "properties": {
                    "name":  {"type": "string"},
                    "email": {"type": "string"},
                    "plan":  {"type": "string"},
                    "demo_requested": {"type": "boolean"},
                },
                "required": ["name", "email", "plan", "demo_requested"],
                "additionalProperties": False,
            }}},
        )
        import json
        data = json.loads(next(b.text for b in resp.content if b.type == "text"))
        print(data)  # -> {'name': 'Jane Doe', 'email': 'jane@acme.com', 'plan': 'Enterprise', 'demo_requested': True}
        ```

        The same idea exists across providers (OpenAI "structured outputs", Gemini "response
        schema") — prefer schemas over regex.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Chain-of-Thought (CoT)

        For multi-step reasoning, asking the model to "think step by step" before answering
        improves accuracy. On Anthropic models that support **extended/adaptive thinking**, enable
        it directly instead of prompting for visible reasoning:

        ```python
        resp = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=2048,
            thinking={"type": "adaptive"},   # model decides how much to reason
            messages=[{"role": "user", "content":
                "A train leaves at 2pm going 60mph. Another leaves at 3pm going 80mph on the "
                "same track. When does the second catch the first?"}],
        )
        for b in resp.content:
            if b.type == "text":
                print(b.text)
        ```
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Coding Exercise

        1. Write a system prompt that makes the model output ONLY a JSON object with keys
           `summary` (string) and `action_items` (array of strings) for any meeting transcript.
        2. Build a 5-example evaluation set (input transcript → expected keys present) and write a
           function that checks the output parses as JSON and has both required keys.
        3. Compare a zero-shot prompt vs a 2-shot prompt on your eval set — which has a higher
           pass rate?
        """
    )
    return


@app.cell
def __():
    # Offline-safe eval harness skeleton (plug in a real client when you have an API key)
    import json

    def is_valid_output(text: str) -> bool:
        try:
            data = json.loads(text)
        except Exception:
            return False
        return isinstance(data, dict) and "summary" in data and "action_items" in data

    # Simulate two candidate outputs
    good = '{"summary": "Discussed Q3 roadmap.", "action_items": ["Ship feature X"]}'
    bad = "Here is your summary: we discussed the roadmap."
    print("good passes:", is_valid_output(good))
    print("bad passes :", is_valid_output(bad))
    return bad, good, is_valid_output, json


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Assignment
        See `../assignments/week03_assignments.md` — Assignment 4.

        ## Interview Questions
        See `../../interview-prep/week03_genai_questions.md` — Section: Prompt Engineering.

        ## Industry Use Cases
        - Classification, extraction, summarization pipelines
        - Customer-facing assistants with controlled tone and format
        - Eval-driven prompt iteration in CI for LLM apps

        ## Common Mistakes
        - Parsing free text with regex instead of using structured outputs
        - Overly aggressive "MUST/CRITICAL" language causing over-triggering on modern models
        - No evaluation set — "it looked good once" is not a metric

        ## Best Practices
        - Specify role, task, constraints, and output format explicitly
        - Use JSON schema / tool calling for machine-readable output
        - Version prompts and measure them against an eval set; cache stable context

        ## Further Reading
        - Anthropic prompt engineering guide
        - "Chain-of-Thought Prompting" (Wei et al., 2022)
        - OpenAI & Google structured-output documentation
        """
    )
    return


if __name__ == "__main__":
    app.run()
