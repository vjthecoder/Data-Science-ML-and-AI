import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import sys
    sys.path.insert(0, "../app")
    return mo, sys


@app.cell
def __(mo):
    mo.md(
        r"""
        # 03. Agent Development Notebook

        Develop and exercise the AI Career Coach agent (`app/agent.py`). Functions degrade to an
        offline stub without `ANTHROPIC_API_KEY`, so you can develop the orchestration logic
        first, then plug in the real LLM.
        """
    )
    return


@app.cell
def __():
    from rag import KnowledgeBase, build_context

    kb = KnowledgeBase()
    print("RAG context for 'become an AI engineer':")
    print(build_context("become an AI engineer", kb, k=3))
    return KnowledgeBase, build_context, kb


@app.cell
def __():
    from agent import coach

    # These return real Claude output when ANTHROPIC_API_KEY is set, else an offline stub.
    print("=== Interview questions ===")
    print(coach("interview_questions", role="AI Engineer", n=3)[:300])
    return (coach,)


@app.cell
def __(coach):
    print("=== Skill gap (deterministic + advice) ===")
    result = coach(
        "skill_gap",
        resume_text="Python, Pandas, SQL, scikit-learn, Excel.",
        job_description="AI Engineer: Python, PyTorch, Docker, AWS, RAG, LLM.",
    )
    print("coverage:", result["coverage"])
    print("missing:", result["missing"])
    print("advice (first 200 chars):", result["advice"][:200])
    return (result,)


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Exercises
        1. Set `ANTHROPIC_API_KEY` and re-run — compare stub vs real output.
        2. Add a 5th feature: `generate_cover_letter(resume_text, job_description)` in
           `app/agent.py`, expose it in `main.py` (FastAPI) and `streamlit_app.py` (UI).
        3. Swap the RAG backend to sentence-transformers (`USE_ST=1`) and compare retrieved
           context quality.
        4. Add an eval: 3 sample resumes + expected "missing skills" and assert the skill-gap
           logic is correct (extend `app/test_app.py`).

        ## Production notes
        - Cap `max_tokens`; cache the RAG KB; log each action + latency.
        - Validate/limit user input sizes (already enforced via Pydantic in `main.py`).
        - Never log full resumes containing PII without consent.
        """
    )
    return


if __name__ == "__main__":
    app.run()
