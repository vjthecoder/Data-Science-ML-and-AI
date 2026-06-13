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
        # 01. Capstone Planning — AI Career Coach

        ## Goal
        Integrate everything from Weeks 1-5 into one production application: a RAG-powered AI
        agent that coaches users on their tech careers.

        ## Features (map to `app/agent.py`)
        | Feature | Function | Weeks used |
        |---------|----------|-----------|
        | Resume Analysis | `analyze_resume` | 1 (parsing), 3 (prompting), 4 (RAG) |
        | Skill Gap Detection | `detect_skill_gap` | 1, 2 (logic), 3 |
        | Interview Question Generator | `generate_interview_questions` | 3, 4 |
        | Learning Path Generator | `generate_learning_path` | 3, 4 |
        | RAG Knowledge Base | `app/rag.py` | 3, 4 |
        | AI Agent (orchestration) | `coach(action, ...)` | 3 |

        ## Architecture
        See `../../diagrams/week06_capstone/README.md` and `../README.md`.

        ```
        Streamlit UI  ─┐
                        ├─► agent.coach(action) ─► RAG context + Claude ─► grounded output
        FastAPI API   ─┘
        Deployment: Docker → Render/Railway/Cloud Run/AWS
        ```

        ## Milestones
        1. Resume parsing + skill extraction (offline, deterministic).
        2. RAG knowledge base (offline hash embeddings → optional sentence-transformers).
        3. Agent functions calling Claude, grounded in RAG context.
        4. FastAPI endpoints + Pydantic validation.
        5. Streamlit UI with all four features.
        6. Tests (offline), Dockerfile, deployment.
        7. GitHub packaging (README, .env.example, CI, demo).
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Definition of Done
        - [ ] All four features work end-to-end (offline stub + real LLM)
        - [ ] `python -m pytest` passes offline (`app/test_app.py`)
        - [ ] FastAPI `/health` returns ok; `/docs` lists all endpoints
        - [ ] Streamlit UI runs and exercises every feature
        - [ ] Dockerfile builds; container serves the API
        - [ ] README with architecture diagram, setup, demo, and limitations
        - [ ] `.env.example` present; no secrets committed; CI green

        ## Try the pieces now
        Run the offline smoke test from the app directory:
        ```bash
        cd ../app && python -m pytest test_app.py -q
        ```
        """
    )
    return


if __name__ == "__main__":
    app.run()
