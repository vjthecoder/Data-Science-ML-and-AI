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
        # Lab 3: Google Gemini API Basics

        **Goal:** Generate content, set a system instruction, and use function calling with the
        Google Gemini API.

        **Setup:**
        ```bash
        pip install google-generativeai
        export GOOGLE_API_KEY="..."   # never hardcode; use environment variables
        ```

        ## Tasks
        1. Basic content generation.
        2. System instruction to control behavior.
        3. Function calling.
        4. Structured (JSON) response.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 1-2. Generate content with a system instruction

        ```python
        import google.generativeai as genai
        import os

        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

        model = genai.GenerativeModel(
            "gemini-1.5-pro",
            system_instruction="You are a concise assistant. Answer in one sentence.",
        )
        resp = model.generate_content("What is retrieval-augmented generation?")
        print(resp.text)
        ```
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 3. Function calling

        ```python
        def get_weather(city: str) -> str:
            \"\"\"Get the current temperature for a city.\"\"\"
            return {"Paris": "18C", "Tokyo": "24C"}.get(city, "unknown")

        model = genai.GenerativeModel("gemini-1.5-pro", tools=[get_weather])
        chat = model.start_chat(enable_automatic_function_calling=True)
        resp = chat.send_message("What's the weather in Paris?")
        print(resp.text)   # SDK can auto-execute the Python function and continue
        ```
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 4. Structured JSON response

        ```python
        import json

        model = genai.GenerativeModel(
            "gemini-1.5-pro",
            generation_config={
                "response_mime_type": "application/json",
                "response_schema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "email": {"type": "string"},
                        "plan": {"type": "string"},
                    },
                    "required": ["name", "email", "plan"],
                },
            },
        )
        resp = model.generate_content("Extract: Jane, jane@x.com, Enterprise plan.")
        print(json.loads(resp.text))
        ```

        ## Deliverable
        A script `gemini_demo.py` running all four tasks.

        ## Compare-the-Providers Exercise
        Run the SAME prompt ("Summarize RAG in 2 sentences") through OpenAI (Lab 1), Anthropic
        (Lab 2), and Gemini (Lab 3). Note differences in tone, length, and latency. Which would
        you choose for a production summarizer, and why?
        """
    )
    return


if __name__ == "__main__":
    app.run()
