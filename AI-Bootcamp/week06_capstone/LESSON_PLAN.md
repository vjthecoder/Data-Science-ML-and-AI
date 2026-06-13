# Week 6 Lesson Plan: Final Project, Deployment & GitHub Packaging

**Total Duration:** ~25-30 hours over 6 days. Capstone: **Production AI Career Coach**.

| Day | Focus | Files | Duration | Deliverable |
|-----|-------|-------|----------|-------------|
| 1 | Plan + resume parsing | `notebooks/01_capstone_planning.py`, `notebooks/02_resume_parsing_dev.py`, `app/resume_parser.py` | 4h | Parsing + skill-gap working |
| 2 | RAG KB + agent | `notebooks/03_agent_dev.py`, `app/rag.py`, `app/agent.py` | 5h | All 4 features (stub + LLM) |
| 3 | FastAPI backend | `app/main.py` | 4h | API with /docs + validation |
| 4 | Streamlit UI | `app/streamlit_app.py` | 4h | UI exercising all features |
| 5 | Tests + Docker | `app/test_app.py`, `app/Dockerfile` | 4h | Green tests, built image |
| 6 | Deploy + GitHub packaging | `../deployment/*`, README, CI | 4-5h | Live URL + polished repo |

## Setup (Day 0)
```bash
cd AI-Bootcamp/week06_capstone/app
pip install -r requirements.txt
cp .env.example .env        # then add your ANTHROPIC_API_KEY (git-ignored)
python -m pytest test_app.py -q     # runs offline
```

## Deployment targets (pick at least one)
Docker, Streamlit Community Cloud, Render, Railway, AWS (App Runner/ECS), GCP (Cloud Run) — see
`../deployment/`.

## GitHub Packaging Checklist
- [ ] README: what it does, architecture diagram, setup, demo GIF/screenshots, live URL
- [ ] `requirements.txt` + `Dockerfile`
- [ ] `.env.example` (no real secrets); `.gitignore` covers `.env`
- [ ] Tests + CI (the repo's `.github/workflows/ci.yml` lints + compiles + tests)
- [ ] LICENSE; clean, conventional commit history
- [ ] "Limitations & future work" section

## Assessment / Success Criteria
By the end of Week 6, students have a deployed, documented, tested AI application that:
- Integrates parsing (W1), logic (W2), LLM/agents (W3), RAG (W4), and automation thinking (W5)
- Exposes a FastAPI backend and a Streamlit UI
- Runs in Docker and is deployed to at least one cloud platform
- Is packaged on GitHub to portfolio standard
