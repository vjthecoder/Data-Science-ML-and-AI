# Week 6 Capstone — Reference Implementation

The **complete reference implementation** lives in [`../app/`](../app/). Build your own version
first; use this as the standard to compare against.

## Reference files
| File | Purpose |
|------|---------|
| `../app/resume_parser.py` | Resume text extraction + deterministic skill extraction / skill-gap |
| `../app/rag.py` | RAG knowledge base (offline hash embeddings → optional sentence-transformers) |
| `../app/agent.py` | The 4 coach features + `coach(action, ...)` orchestration (offline stub fallback) |
| `../app/main.py` | FastAPI backend with Pydantic-validated endpoints |
| `../app/streamlit_app.py` | Streamlit UI exercising all features |
| `../app/test_app.py` | Offline smoke tests (no API key) |
| `../app/Dockerfile` | Container image (FastAPI default; Streamlit via command override) |
| `../app/.env.example` | Secret template (never commit real `.env`) |

## Verify the reference offline
```bash
cd ../app
pip install -r requirements.txt
python -m pytest test_app.py -q          # all tests pass with no API key
python -c "from agent import coach; print(coach('interview_questions', role='AI Engineer', n=2))"
```

## Grading rubric (suggested)
| Area | Points |
|------|--------|
| All 4 features work (stub + real LLM) | 25 |
| RAG grounding implemented | 15 |
| FastAPI + validation + /health | 15 |
| Streamlit UI covering all features | 15 |
| Tests pass in CI | 10 |
| Dockerized + deployed (live URL) | 10 |
| README + .env.example + clean commits | 10 |

## Common pitfalls
- Hardcoding the API key (use `.env` / runtime env).
- No offline fallback → tests need a paid key in CI.
- Skipping input validation → oversized/malicious inputs hit the LLM.
- No "limitations" section → reviewers can't gauge engineering judgment.
