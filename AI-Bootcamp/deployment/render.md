# Deploying to Render

Render deploys directly from a GitHub repo or a Docker image — a good free/low-cost option.

## Option A — Docker (recommended)
1. Push the repo to GitHub.
2. Render → **New → Web Service** → connect the repo.
3. Set **Root Directory** to `AI-Bootcamp/week06_capstone/app` and **Runtime** to Docker.
4. Render reads the `Dockerfile`; set the **Health Check Path** to `/health`.
5. Add an environment variable `ANTHROPIC_API_KEY` (Render encrypts it).
6. Deploy → public HTTPS URL.

## Option B — Native Python (no Docker)
- Root Directory: `AI-Bootcamp/week06_capstone/app`
- Build command: `pip install -r requirements.txt`
- Start command (FastAPI): `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Or Streamlit: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
- Render injects `$PORT` — bind to it, don't hardcode.

## Optional: render.yaml (infrastructure as code)
```yaml
services:
  - type: web
    name: ai-career-coach
    runtime: docker
    rootDir: AI-Bootcamp/week06_capstone/app
    healthCheckPath: /health
    envVars:
      - key: ANTHROPIC_API_KEY
        sync: false   # set in dashboard, not committed
```

## Best practices
- Bind to `$PORT`; set the health check path.
- Store the API key as an env var in the dashboard (never in the repo).
- Free instances spin down when idle — expect a cold start.
