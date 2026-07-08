# Changelog

All notable changes to this project are documented in this file. Format based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), versioning follows
[Semantic Versioning](https://semver.org/).

## [Unreleased]
### Added
- Resources filled out: comprehensive glossary (terms by week), curated further-reading list,
  and cheat sheets (Pandas, Prompt Engineering). Root repo README now indexes the bootcamp.

## [1.0.0] - 2026-06-13
All six weeks of the **AI Engineering Bootcamp** are complete and ready for learners.
### Added
- Week 6: Final Project, Deployment & GitHub Packaging — complete. Production **AI Career Coach**
  capstone (`week06_capstone/app/`): resume_parser, RAG knowledge base, agent (resume analysis,
  skill-gap, interview questions, learning path) with offline stub fallback, FastAPI backend with
  Pydantic validation, Streamlit UI, offline pytest suite, Dockerfile, `.env.example`. Seven
  deployment guides (Docker, Streamlit Cloud, FastAPI, AWS, GCP, Render, Railway). Capstone
  notebooks, lesson plan, diagrams, interview questions, and grading rubric. All 6 weeks complete.
- Week 5: AI Automation with n8n — complete (7 importable workflow JSON exports: beginner,
  email automation, lead qualification, AI agent with tools+memory, CRM automation, WhatsApp
  assistant, multi-agent pipeline; workflows README with import guide; assignments, solutions,
  lesson plan, diagrams, interview questions). LLM nodes use Anthropic `claude-opus-4-8`;
  credentials use placeholders (kept out of JSON).
- Week 4: RAG (Retrieval Augmented Generation) — complete (6 Marimo notebooks on architecture,
  chunking, vector search FAISS/Chroma, hybrid search + reranking, metadata filtering,
  evaluation; 3 labs for LangChain/LlamaIndex/hybrid+rerank; PDF Chatbot project with Streamlit
  app + reusable rag_core; assignments, solutions, lesson plan, diagrams, interview questions).
  All concept notebooks run offline; generation uses Anthropic `claude-opus-4-8`.
- Week 3: GenAI Foundations & LLM Working Procedure — complete (7 Marimo notebooks on
  transformers/attention, tokens/embeddings, vector DBs, prompt engineering, tool calling,
  MCP, multi-agent systems; 5 labs for OpenAI/Anthropic/Gemini/open-source/agent; assignments,
  solutions, lesson plan, diagrams, interview questions). Anthropic examples use current SDK
  patterns (`claude-opus-4-8`, `messages.create`, tool-use loop, structured outputs).
- Course review and 2026 redesign plan (`AI-Bootcamp/COURSE_REVIEW_2026.md`)
- Week 2: Machine Learning Basics & ML Workflow — complete (7 Marimo notebooks on problem
  framing/EDA, feature engineering, regression, classification, clustering, evaluation metrics,
  cross-validation/tuning; 3 labs for lead scoring/churn/marketing response; datasets,
  assignments, solutions, lesson plan, diagrams, interview questions).
- Course review and 2026 redesign plan (`AI-Bootcamp/COURSE_REVIEW_2026.md`)
- Open-source project infrastructure: CI workflow, release workflow, pre-commit hooks,
  issue/PR templates, CONTRIBUTING guide, Code of Conduct, CODEOWNERS

## [0.2.0] - 2026-06-12
### Added
- Week 1: Python for Data Science & AI — complete (Marimo notebooks, labs, datasets,
  assignments, solutions, diagrams, interview questions, lesson plan)

## [0.1.0] - 2026-06-12
### Added
- Initial AI-Bootcamp repository skeleton (folder structure, top-level docs, weekly READMEs)
