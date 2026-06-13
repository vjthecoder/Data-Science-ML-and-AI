# Week 6: Final Project, Deployment & GitHub Packaging

## Capstone: Production AI Career Coach

## Learning Objectives
- Integrate everything from Weeks 1-5 into one production application
- Build a RAG-powered AI agent with multiple features
- Containerize and deploy the application
- Package the project professionally for GitHub

## Estimated Duration
25-30 hours

## Prerequisites
- Weeks 1-5 completed
- `ANTHROPIC_API_KEY` for live output (the app runs in offline stub mode without it)

## Lesson Plan
See [`LESSON_PLAN.md`](LESSON_PLAN.md) for the day-by-day schedule.

## Diagrams
See [`../diagrams/week06_capstone/`](../diagrams/week06_capstone/README.md)

## Quick Start
```bash
cd app
pip install -r requirements.txt
cp .env.example .env            # add ANTHROPIC_API_KEY (git-ignored)
python -m pytest test_app.py -q # offline smoke tests
uvicorn main:app --reload       # FastAPI at /docs
# or: streamlit run streamlit_app.py
```

## Features
1. **Resume Analysis** — parse and analyze uploaded resumes
2. **Skill Gap Detection** — compare resume skills vs target job description
3. **Interview Question Generator** — generate role-specific interview questions
4. **Learning Path Generator** — recommend a personalized learning roadmap
5. **RAG Knowledge Base** — career/industry knowledge grounding
6. **AI Agent** — orchestrates the above features via tool calling

## Architecture
See `../diagrams/week06_capstone/architecture.md`

## App Structure (`app/`)
- `app/main.py` — FastAPI backend
- `app/streamlit_app.py` — Streamlit frontend
- `app/agent.py` — AI Career Coach agent (tools + orchestration)
- `app/rag.py` — RAG knowledge base module
- `app/resume_parser.py` — Resume parsing utilities
- `app/Dockerfile`
- `app/requirements.txt`

## Notebooks
- `notebooks/01_capstone_planning.ipynb`
- `notebooks/02_resume_parsing_dev.ipynb`
- `notebooks/03_agent_dev.ipynb`

## Deployment
See `../deployment/` for guides:
- Docker
- Streamlit Community Cloud
- FastAPI on Render/Railway
- AWS / GCP

## GitHub Packaging Checklist
- [ ] README with setup, usage, screenshots
- [ ] requirements.txt / Dockerfile
- [ ] `.env.example` (no real secrets)
- [ ] LICENSE
- [ ] CI workflow (lint + tests)
- [ ] Demo video/GIF link

## Assignments
See `solutions/` for a reference implementation outline.

## Interview Questions
See `../interview-prep/week06_capstone_questions.md`

## Common Mistakes
- Hardcoding API keys in source/Docker images
- No input validation on uploaded files
- Deploying without health checks or logging

## Best Practices
- Separate config via environment variables (`.env` + `.env.example`)
- Add request validation (Pydantic models) on FastAPI endpoints
- Add structured logging and basic monitoring
- Write a clear README with architecture diagram and demo instructions

## Further Reading
- FastAPI, Streamlit, Docker official documentation
- 12-Factor App methodology
