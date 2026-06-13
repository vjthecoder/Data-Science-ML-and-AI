# Deploying with Docker & Docker Compose

The capstone ships a `Dockerfile` in `week06_capstone/app/`. This guide covers building,
running, and composing the FastAPI backend + Streamlit frontend.

## Build & run (single container — FastAPI)
```bash
cd AI-Bootcamp/week06_capstone/app
docker build -t ai-career-coach .
docker run -e ANTHROPIC_API_KEY=sk-ant-... -p 8000:8000 ai-career-coach
# -> http://localhost:8000/health  and  /docs (Swagger UI)
```

## Run the Streamlit UI instead
```bash
docker run -e ANTHROPIC_API_KEY=sk-ant-... -p 8501:8501 ai-career-coach \
  streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

## Docker Compose (backend + frontend together)
Create `docker-compose.yml` in `week06_capstone/app/`:
```yaml
services:
  api:
    build: .
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    ports: ["8000:8000"]
  ui:
    build: .
    command: streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    ports: ["8501:8501"]
    depends_on: [api]
```
```bash
export ANTHROPIC_API_KEY=sk-ant-...     # compose reads it from your shell
docker compose up --build
```

## Best practices
- **Never bake secrets into the image** — pass `ANTHROPIC_API_KEY` at runtime (`-e` / compose
  `environment` / secrets manager).
- Pin a base image (`python:3.11-slim`) and `requirements.txt` versions for reproducibility.
- Use the `HEALTHCHECK` (already in the Dockerfile) so orchestrators can detect readiness.
- Keep images small: `--no-cache-dir`, copy `requirements.txt` before code for layer caching.
- Add a `.dockerignore` (`.git`, `__pycache__`, `.env`, `chroma_db/`).
