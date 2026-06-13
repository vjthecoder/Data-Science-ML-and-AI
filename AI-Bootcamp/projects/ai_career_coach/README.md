# Project: AI Career Coach (Capstone)

The Week 6 capstone — a production RAG-powered AI agent that coaches users on their tech careers.

**The full implementation lives in [`../../week06_capstone/app/`](../../week06_capstone/app/).**
This folder is a pointer / standalone-project framing of the same capstone.

## Features
- Resume Analysis
- Skill Gap Detection
- Interview Question Generator
- Learning Path Generator
- RAG Knowledge Base
- AI Agent orchestration

## Quick start
```bash
cd ../../week06_capstone/app
pip install -r requirements.txt
cp .env.example .env            # add ANTHROPIC_API_KEY
uvicorn main:app --reload       # API at /docs
# or: streamlit run streamlit_app.py
```

## Deployment
See [`../../deployment/`](../../deployment/) for Docker, Streamlit Cloud, Render, Railway, AWS,
and GCP guides.

## Architecture
See [`../../diagrams/week06_capstone/`](../../diagrams/week06_capstone/README.md).
