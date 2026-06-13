# AI Engineering Bootcamp: From Python to Production AI Systems

A 6-week, project-based curriculum that takes you from Python fundamentals to deploying
production-ready GenAI systems (RAG, agents, automation, and a capstone career-coach app).

Each concept is taught with: Theory -> Visual Explanation -> Simple Example -> Real World
Example -> Coding Exercise -> Assignment -> Interview Questions -> Industry Use Cases.

**Status: v1.0.0 — all 6 weeks complete.** Notebooks use [Marimo](https://marimo.io)
(`.py` files, run with `marimo edit <file>`). Concept notebooks include offline-safe demos, so
the curriculum runs without paid API keys; LLM examples use the Anthropic SDK
(`claude-opus-4-8`) with keys loaded from the environment.

## Curriculum

| Week | Topic | Folder |
|------|-------|--------|
| 1 | Python for Data Science & AI | [week01_python](week01_python) |
| 2 | Machine Learning Basics & ML Workflow | [week02_ml](week02_ml) |
| 3 | GenAI Foundations & LLM Working Procedure | [week03_genai](week03_genai) |
| 4 | RAG: Retrieval Augmented Generation | [week04_rag](week04_rag) |
| 5 | AI Automation with n8n | [week05_n8n](week05_n8n) |
| 6 | Final Project, Deployment & GitHub Packaging | [week06_capstone](week06_capstone) |

## Repository Structure

```
AI-Bootcamp/
├── week01_python ... week06_capstone   # Weekly modules
├── projects/        # Larger standalone project specs
├── assignments/      # Cross-week assignment index
├── solutions/        # Cross-week solution index
├── interview-prep/   # Interview question banks by topic
├── resources/        # Further reading, cheat sheets, datasets
├── diagrams/         # Architecture & concept diagrams
└── deployment/       # Docker, cloud, and platform deployment guides
```

## Getting Started

```bash
git clone <repo-url>
cd AI-Bootcamp
conda env create -f environment.yml
conda activate ai-bootcamp
# or
pip install -r requirements.txt
```

## Audience

Absolute beginners, software engineers, data scientists, AI engineers, students, and
working professionals. Learning style: every concept explained at three levels —
a 10-year-old, a college student, and an industry professional.
